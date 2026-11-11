"""Baixa a legislação do catálogo para o repositório, em texto limpo.

Uso:
    python3 scripts/baixar_materiais.py                 baixa o que falta
    python3 scripts/baixar_materiais.py --fonte alesp   só uma fonte
    python3 scripts/baixar_materiais.py --refazer       baixa tudo de novo
    python3 scripts/baixar_materiais.py --so-consolidar só regenera manifesto e NotebookLM

Só usa a biblioteca padrão do Python 3.9+.

Saídas:
    materiais/legislacao/<arquivo>.md    uma norma por arquivo, com cabeçalho de origem
    materiais/notebooklm/<grupo>.md      normas consolidadas por grupo, para subir ao NotebookLM
    materiais/MANIFESTO.md               o que foi baixado, de onde, quando, e o que falhou
    materiais/estado.json                registro usado para montar o manifesto

Cuidado central: os sites oficiais mantêm a redação revogada no texto,
marcada com tachado. Aqui esses trechos são REMOVIDOS antes da conversão,
para que redação revogada não apareça como vigente. O manifesto informa
quanto foi removido de cada norma, para conferência.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import sys
import time
import urllib.error
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from catalogo import BIBLIOGRAFIA_INDICADA, CATALOGO, PENDENTES  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
DIR_MATERIAIS = RAIZ / "materiais"
DIR_LEGISLACAO = DIR_MATERIAIS / "legislacao"
DIR_NOTEBOOKLM = DIR_MATERIAIS / "notebooklm"
ARQ_ESTADO = DIR_MATERIAIS / "estado.json"
ARQ_MANIFESTO = DIR_MATERIAIS / "MANIFESTO.md"

AGENTE = "def-sp-estudo/0.1 (uso pessoal de estudo; python-urllib)"
PAUSA_SEGUNDOS = 1.0
LIMITE_PALAVRAS_NOTEBOOKLM = 400_000  # o NotebookLM aceita até 500 mil por fonte

PLANALTO = "https://www.planalto.gov.br/ccivil_03"
ALESP = "https://www.al.sp.gov.br/repositorio/legislacao"


# --------------------------------------------------------------------------- endereços


def pasta_de_atos(ano: int) -> str | None:
    """Pasta do Planalto para atos de 2004 em diante (ex.: _ato2015-2018/2015)."""
    for inicio, fim in [(2004, 2006), (2007, 2010), (2011, 2014), (2015, 2018),
                        (2019, 2022), (2023, 2026), (2027, 2030)]:
        if inicio <= ano <= fim:
            return f"_ato{inicio}-{fim}/{ano}"
    return None


def com_ponto(numero: int) -> str:
    return f"{numero:,}".replace(",", ".")


def enderecos_planalto(item: dict) -> list[str]:
    """Endereços possíveis de uma norma federal, do mais provável ao menos.

    O Planalto não segue um padrão único, então o baixador testa em ordem e
    fica com o primeiro que responde e contém o número da norma. Versões
    compiladas (com as alterações incorporadas) vêm primeiro.
    """
    tipo, numero, ano = item["tipo"], item["numero"], item["ano"]
    if tipo == "constituicao":
        return [f"{PLANALTO}/constituicao/constituicaocompilado.htm",
                f"{PLANALTO}/constituicao/constituicao.htm"]
    if tipo == "lcp":
        return [f"{PLANALTO}/leis/lcp/lcp{numero}.htm",
                f"{PLANALTO}/leis/lcp/Lcp{numero}.htm"]
    if tipo == "decreto-lei":
        base = f"{PLANALTO}/decreto-lei/del{numero}"
        return [f"{base}compilado.htm", f"{base}.htm",
                f"{PLANALTO}/decreto-lei/Del{numero}compilado.htm",
                f"{PLANALTO}/decreto-lei/Del{numero}.htm"]

    atos = pasta_de_atos(ano)
    if tipo == "lei":
        nomes = [f"l{numero}", f"L{numero}", f"l{com_ponto(numero)}", f"L{com_ponto(numero)}"]
        pastas = [f"{atos}/lei"] if atos else []
        pastas += [f"leis/{ano}", "leis", f"leis/leis_{ano}", f"leis/LEIS_{ano}"]
        sufixos = ["compilado", "compilada", ""]
    elif tipo == "decreto":
        nomes = [f"d{numero}", f"D{numero}", f"d{numero:04d}", f"D{numero:04d}"]
        pastas = [f"{atos}/decreto"] if atos else []
        pastas += [f"decreto/{ano}", "decreto", "decreto/1990-1994", "decreto/1995-1999",
                   "decreto/1950-1969", "decreto/1970-1979", "decreto/1980-1989"]
        sufixos = ["compilado", ""]
    else:
        raise ValueError(f"tipo desconhecido: {tipo}")

    vistos: list[str] = []
    for pasta in pastas:
        for sufixo in sufixos:
            for nome in nomes:
                url = f"{PLANALTO}/{pasta}/{nome}{sufixo}.htm"
                if url not in vistos:
                    vistos.append(url)
    return vistos


def enderecos_alesp(item: dict) -> list[str]:
    tipo, numero, ano, data = item["tipo"], item["numero"], item["ano"], item["data"]
    base = f"{ALESP}/{tipo}/{ano}"
    return [f"{base}/compilacao-{tipo}-{numero}-{data}.html",
            f"{base}/{tipo}-{numero}-{data}.html"]


# --------------------------------------------------------------------------- download


class NaoEncontrado(Exception):
    pass


def baixar(url: str) -> bytes:
    pedido = urllib.request.Request(url, headers={"User-Agent": AGENTE})
    with urllib.request.urlopen(pedido, timeout=60) as resposta:
        return resposta.read()


def decodificar(bruto: bytes) -> str:
    """Planalto usa windows-1252; ALESP usa UTF-8. Respeita o que a página declara."""
    declarado = re.search(rb"charset\s*=\s*[\"']?([\w-]+)", bruto[:4000], re.I)
    tentativas = [declarado.group(1).decode("ascii").lower()] if declarado else []
    tentativas += ["utf-8", "cp1252"]
    for codificacao in tentativas:
        if codificacao in ("iso-8859-1", "latin-1", "latin1"):
            codificacao = "cp1252"  # é o que os navegadores fazem
        try:
            return bruto.decode(codificacao)
        except (UnicodeDecodeError, LookupError):
            continue
    return bruto.decode("cp1252", errors="replace")


# --------------------------------------------------------------------------- limpeza


BLOCOS = {"p", "div", "br", "tr", "li", "h1", "h2", "h3", "h4", "h5", "h6",
          "blockquote", "table", "center", "hr", "dd", "dt"}
IGNORADOS = {"script", "style", "head", "noscript", "nav", "footer", "header", "form"}
TACHADOS = {"strike", "s", "del"}
SEM_FECHAMENTO = {"br", "hr", "img", "input", "meta", "link", "area", "base", "col"}


class LimpadorDeNorma(HTMLParser):
    """Converte a página em texto, descartando o que está tachado (revogado)."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.partes: list[str] = []
        self.pilha_tachado: list[str] = []   # tags abertas que tacham o texto
        self.pilha_ignorado: list[str] = []
        self.caracteres_mantidos = 0
        self.caracteres_removidos = 0

    def handle_starttag(self, tag, atributos):
        if tag in SEM_FECHAMENTO:
            if tag in BLOCOS:
                self.partes.append("\n")
            return
        if tag in IGNORADOS:
            self.pilha_ignorado.append(tag)
            return
        estilo = (dict(atributos).get("style") or "").replace(" ", "").lower()
        if tag in TACHADOS or "line-through" in estilo:
            self.pilha_tachado.append(tag)
        elif self.pilha_tachado and tag == self.pilha_tachado[-1]:
            # mesma tag aninhada dentro do tachado: empilha para fechar no lugar certo
            self.pilha_tachado.append(tag)
        if tag in BLOCOS:
            self.partes.append("\n")

    def handle_endtag(self, tag):
        if self.pilha_ignorado and tag == self.pilha_ignorado[-1]:
            self.pilha_ignorado.pop()
            return
        if tag in self.pilha_tachado:
            # fecha até a tag correspondente (HTML oficial costuma vir desbalanceado)
            while self.pilha_tachado and self.pilha_tachado.pop() != tag:
                pass
        # Um tachado aberto e nunca fechado continua valendo nos parágrafos
        # seguintes, como no navegador. Se chegar aberto ao fim da página, o
        # manifesto avisa, porque aí pode ter sumido texto vigente.
        if tag in BLOCOS:
            self.partes.append("\n")

    def handle_data(self, dados):
        if self.pilha_ignorado:
            return
        if self.pilha_tachado:
            self.caracteres_removidos += len(dados.strip())
            return
        self.caracteres_mantidos += len(dados.strip())
        self.partes.append(dados)

    def texto(self) -> str:
        bruto = "".join(self.partes).replace("\xa0", " ")
        linhas = [re.sub(r"[ \t\r\f\v]+", " ", linha).strip() for linha in bruto.split("\n")]
        saida: list[str] = []
        for linha in linhas:
            if linha or (saida and saida[-1]):
                saida.append(linha)
        return "\n".join(saida).strip()


def limpar(html: str) -> tuple[str, int, int, bool]:
    """Devolve (texto, mantidos, removidos, tachado_ficou_aberto)."""
    limpador = LimpadorDeNorma()
    limpador.feed(html)
    limpador.close()
    return (limpador.texto(), limpador.caracteres_mantidos,
            limpador.caracteres_removidos, bool(limpador.pilha_tachado))


def recortar_alesp(texto: str) -> str:
    """Na ALESP o texto da norma começa no título e termina antes do rodapé do site."""
    inicio = re.search(r"^(LEI|DECRETO|CONSTITUIÇÃO|EMENDA)[^\n]*", texto, re.M)
    return texto[inicio.start():] if inicio else texto


# --------------------------------------------------------------------------- execução


def chave(item: dict) -> str:
    return f"{item['fonte']}-{item['tipo'].replace('.', '-')}-{item['numero']}-{item['ano']}"


def nome_arquivo(item: dict) -> str:
    if item["tipo"] == "constituicao":
        return "constituicao-federal-1988.md" if item["fonte"] == "planalto" else "constituicao-sp-1989.md"
    prefixo = {"lei": "lei", "lcp": "lc", "decreto-lei": "decreto-lei", "decreto": "decreto",
               "lei.complementar": "lc"}[item["tipo"]]
    esfera = "sp-" if item["fonte"] == "alesp" else ""
    return f"{esfera}{prefixo}-{item['numero']}-{item['ano']}.md"


def rotulo(item: dict) -> str:
    if item["tipo"] == "constituicao":
        return item["nome"]
    tipo = {"lei": "Lei", "lcp": "Lei Complementar", "decreto-lei": "Decreto-Lei",
            "decreto": "Decreto", "lei.complementar": "Lei Complementar"}[item["tipo"]]
    esfera = " Estadual (SP)" if item["fonte"] == "alesp" else ""
    return f"{tipo}{esfera} nº {com_ponto(item['numero'])}/{item['ano']} — {item['nome']}"


def contem_o_numero(item: dict, texto: str) -> bool:
    """Confere se a página é mesmo da norma pedida (evita aceitar página errada)."""
    if item["tipo"] == "constituicao":
        return "CONSTITUIÇÃO" in texto.upper()
    numero = item["numero"]
    inicio = texto[:6000]
    return bool(re.search(rf"(?<![\d.]){re.escape(com_ponto(numero))}(?!\d)", inicio)
                or re.search(rf"(?<![\d.]){numero}(?!\d)", inicio))


def obter(item: dict) -> dict:
    enderecos = enderecos_planalto(item) if item["fonte"] == "planalto" else enderecos_alesp(item)
    ultimo_erro = "nenhum endereço respondeu"
    for url in enderecos:
        time.sleep(PAUSA_SEGUNDOS)
        try:
            bruto = baixar(url)
        except urllib.error.HTTPError as erro:
            ultimo_erro = f"HTTP {erro.code}"
            continue
        except Exception as erro:  # rede fora, conexão recusada, tempo esgotado
            ultimo_erro = f"{type(erro).__name__}: {erro}"
            if item["fonte"] == "planalto":
                break  # se o site não responde, não adianta testar 30 variações
            continue
        texto, mantidos, removidos, aberto = limpar(decodificar(bruto))
        if item["fonte"] == "alesp":
            texto = recortar_alesp(texto)
        if len(texto) < 300 or not contem_o_numero(item, texto):
            ultimo_erro = "página não parece ser da norma pedida"
            continue
        compilado = "compil" in url.lower() or item["tipo"] == "constituicao"
        return {"ok": True, "url": url, "texto": texto, "mantidos": mantidos,
                "removidos": removidos, "tachado_aberto": aberto, "compilado": compilado}
    return {"ok": False, "erro": ultimo_erro}


def gravar_norma(item: dict, resultado: dict, hoje: str) -> dict:
    texto = resultado["texto"]
    resumo = hashlib.sha256(texto.encode("utf-8")).hexdigest()
    cabecalho = [
        f"# {rotulo(item)}",
        "",
        f"- Fonte oficial: {resultado['url']}",
        f"- Capturado em: {hoje}",
        f"- Versão: {'texto compilado (com alterações)' if resultado['compilado'] else 'texto da página, sem versão compilada'}",
        f"- Trechos tachados (revogados) removidos: {resultado['removidos']} caracteres",
        f"- sha256 do texto: {resumo}",
        "",
        "---",
        "",
    ]
    (DIR_LEGISLACAO / nome_arquivo(item)).write_text("\n".join(cabecalho) + texto + "\n", "utf-8")
    return {"arquivo": nome_arquivo(item), "url": resultado["url"], "capturado_em": hoje,
            "sha256": resumo, "palavras": len(texto.split()), "removidos": resultado["removidos"],
            "tachado_aberto": resultado["tachado_aberto"], "compilado": resultado["compilado"]}


def consolidar_notebooklm(estado: dict) -> list[tuple[str, int, int]]:
    """Junta as normas baixadas em poucos arquivos por grupo."""
    DIR_NOTEBOOKLM.mkdir(parents=True, exist_ok=True)
    for antigo in DIR_NOTEBOOKLM.glob("*.md"):
        antigo.unlink()
    grupos: dict[str, list[dict]] = {}
    for item in CATALOGO:
        if estado.get(chave(item), {}).get("arquivo"):
            grupos.setdefault(item["grupo"], []).append(item)
    gerados = []
    for grupo, itens in sorted(grupos.items()):
        partes: list[list[str]] = [[]]
        palavras = [0]
        for item in itens:
            conteudo = (DIR_LEGISLACAO / nome_arquivo(item)).read_text("utf-8")
            tamanho = len(conteudo.split())
            if palavras[-1] and palavras[-1] + tamanho > LIMITE_PALAVRAS_NOTEBOOKLM:
                partes.append([])
                palavras.append(0)
            partes[-1].append(conteudo)
            palavras[-1] += tamanho
        for n, (parte, total) in enumerate(zip(partes, palavras), 1):
            nome = f"{grupo}.md" if len(partes) == 1 else f"{grupo}-parte-{n}.md"
            (DIR_NOTEBOOKLM / nome).write_text("\n\n\n".join(parte), "utf-8")
            gerados.append((nome, len(parte), total))
    return gerados


def escrever_manifesto(estado: dict, consolidados: list[tuple[str, int, int]]) -> None:
    baixados = [(i, estado[chave(i)]) for i in CATALOGO if estado.get(chave(i), {}).get("arquivo")]
    falhas = [(i, estado.get(chave(i), {})) for i in CATALOGO if not estado.get(chave(i), {}).get("arquivo")]
    linhas = [
        "# Manifesto dos materiais",
        "",
        "Arquivo gerado por `scripts/baixar_materiais.py`. Não editar à mão.",
        "",
        f"- Normas no catálogo: {len(CATALOGO)}",
        f"- Baixadas: {len(baixados)}",
        f"- Faltando: {len(falhas)}",
        "",
        "## Baixadas",
        "",
        "| Norma | Arquivo | Versão | Palavras | Tachado removido | Capturado em | Origem |",
        "|---|---|---|---|---|---|---|",
    ]
    for item, reg in baixados:
        alerta = " ⚠ tachado não fechado na página, conferir" if reg.get("tachado_aberto") else ""
        linhas.append(
            f"| [{rotulo(item)}]({reg['url']}) | `legislacao/{reg['arquivo']}` | "
            f"{'compilada' if reg['compilado'] else 'não compilada'} | {reg['palavras']} | "
            f"{reg['removidos']} caracteres{alerta} | {reg['capturado_em']} | {item['origem']} |"
        )
    linhas += ["", "## Faltando", ""]
    if falhas:
        linhas += ["| Norma | Fonte | Último erro |", "|---|---|---|"]
        for item, reg in falhas:
            linhas.append(f"| {rotulo(item)} | {item['fonte']} | {reg.get('erro', 'ainda não tentado')} |")
    else:
        linhas.append("Nada faltando.")
    linhas += ["", "## Arquivos para o NotebookLM", "",
               "| Arquivo | Normas | Palavras |", "|---|---|---|"]
    linhas += [f"| `notebooklm/{nome}` | {quantas} | {palavras} |" for nome, quantas, palavras in consolidados]
    linhas += ["", "## Citado no edital e ainda fora do baixador", ""]
    linhas += [f"- {p}" for p in PENDENTES]
    linhas += ["", "## Bibliografia indicada no edital (Filosofia e Sociologia)", "",
               "O edital diz que as questões serão extraídas destas obras. São livros",
               "protegidos por direito autoral e não são baixados.", ""]
    linhas += [f"- {b}" for b in BIBLIOGRAFIA_INDICADA]
    ARQ_MANIFESTO.write_text("\n".join(linhas) + "\n", "utf-8")


def main() -> None:
    opcoes = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    opcoes.add_argument("--fonte", choices=["planalto", "alesp"], help="baixa só desta fonte")
    opcoes.add_argument("--refazer", action="store_true", help="baixa de novo o que já existe")
    opcoes.add_argument("--so-consolidar", action="store_true", help="não baixa nada")
    args = opcoes.parse_args()

    DIR_LEGISLACAO.mkdir(parents=True, exist_ok=True)
    estado = json.loads(ARQ_ESTADO.read_text("utf-8")) if ARQ_ESTADO.exists() else {}
    hoje = dt.date.today().isoformat()
    fonte_fora_do_ar: set[str] = set()

    for item in CATALOGO if not args.so_consolidar else []:
        if args.fonte and item["fonte"] != args.fonte:
            continue
        registro = estado.get(chave(item), {})
        ja_tem = registro.get("arquivo") and (DIR_LEGISLACAO / registro["arquivo"]).exists()
        if ja_tem and not args.refazer:
            continue
        if item["fonte"] in fonte_fora_do_ar:
            estado[chave(item)] = {"erro": "site não respondeu nesta execução"}
            continue
        print(f"{rotulo(item)} ... ", end="", flush=True)
        resultado = obter(item)
        if resultado["ok"]:
            novo = gravar_norma(item, resultado, hoje)
            mudou = registro.get("sha256") not in (None, novo["sha256"])
            estado[chave(item)] = novo
            print("ok" + (" (TEXTO MUDOU desde a última captura)" if mudou else ""))
        else:
            if not ja_tem:
                estado[chave(item)] = {"erro": resultado["erro"]}
            print(f"FALHOU: {resultado['erro']}")
            if "HTTP" not in resultado["erro"] and "norma pedida" not in resultado["erro"]:
                fonte_fora_do_ar.add(item["fonte"])
                print(f"  -> {item['fonte']} não está respondendo; pulando os demais itens desta fonte.")
        ARQ_ESTADO.write_text(json.dumps(estado, ensure_ascii=False, indent=2, sort_keys=True) + "\n", "utf-8")

    consolidados = consolidar_notebooklm(estado)
    escrever_manifesto(estado, consolidados)
    total = sum(1 for i in CATALOGO if estado.get(chave(i), {}).get("arquivo"))
    print(f"\n{total} de {len(CATALOGO)} normas no repositório. Detalhes em materiais/MANIFESTO.md")


if __name__ == "__main__":
    main()
