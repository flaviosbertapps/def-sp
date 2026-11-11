"""Extrai o conteúdo programático (Anexo II) do edital para arquivos legíveis.

Uso:
    python3 scripts/extrair_programa.py

Requer o utilitário `pdftotext` (pacote poppler-utils).

Gera:
    conteudo/programa/<disciplina>.md   texto do programa, um tópico por linha
    conteudo/temas.json                 árvore disciplina -> tópicos, para o app
"""

from __future__ import annotations

import json
import re
import subprocess
import unicodedata
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
EDITAL = RAIZ / "materiais" / "edital" / "edital-x-concurso-dpesp.pdf"
SAIDA_MD = RAIZ / "conteudo" / "programa"
SAIDA_JSON = RAIZ / "conteudo" / "temas.json"

# Títulos de seção do Anexo II, na ordem em que aparecem, e a matéria da prova
# objetiva (item 9.1 do edital) a que cada um pertence.
SECOES = [
    ("DIREITO CONSTITUCIONAL", "Direito Constitucional"),
    ("DIREITO ADMINISTRATIVO", "Direito Administrativo e Direito Tributário"),
    ("DIREITO TRIBUTÁRIO", "Direito Administrativo e Direito Tributário"),
    ("DIREITO PENAL", "Direito Penal"),
    ("DIREITO PROCESSUAL PENAL", "Direito Processual Penal"),
    ("DIREITO CIVIL", "Direito Civil e Direito Empresarial"),
    ("DIREITO EMPRESARIAL", "Direito Civil e Direito Empresarial"),
    ("DIREITO PROCESSUAL CIVIL", "Direito Processual Civil"),
    ("DIREITOS DIFUSOS E COLETIVOS", "Direitos Difusos e Coletivos"),
    (
        "PRINCÍPIOS E ATRIBUIÇÕES INSTITUCIONAIS DA DEFENSORIA PÚBLICA DO ESTADO",
        "Princípios e Atribuições Institucionais da Defensoria Pública do Estado",
    ),
    ("DIREITO DA CRIANÇA E DO ADOLESCENTE", "Direito da Criança e do Adolescente"),
    ("DIREITOS HUMANOS", "Direitos Humanos"),
    (
        "FILOSOFIA DO DIREITO E SOCIOLOGIA JURÍDICA",
        "Filosofia do Direito e Sociologia Jurídica",
    ),
]


def slug(texto: str) -> str:
    sem_acento = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", sem_acento.lower()).strip("-")


def texto_do_anexo() -> str:
    bruto = subprocess.run(
        ["pdftotext", "-layout", str(EDITAL), "-"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    inicio = bruto.index("ANEXO II", bruto.index("ANEXO I") + 10)
    # O Anexo I também cita "ANEXO II"; o anexo de verdade é a última ocorrência
    # isolada em uma linha antes do Anexo III.
    ocorrencias = [m.start() for m in re.finditer(r"^\s*ANEXO II\s*$", bruto, re.M)]
    if ocorrencias:
        inicio = ocorrencias[-1]
    fim = [m.start() for m in re.finditer(r"^\s*ANEXO III\s*$", bruto, re.M)][-1]
    linhas = []
    for linha in bruto[inicio:fim].splitlines():
        linha = re.sub(r"\s+", " ", linha).strip()
        if not linha or re.fullmatch(r"\d{1,3}", linha):  # vazias e nº de página
            continue
        linhas.append(linha)
    return "\n".join(linhas)


def dividir_em_secoes(texto: str) -> list[tuple[str, str, str]]:
    posicoes = []
    for titulo, materia in SECOES:
        achado = re.search(rf"^{re.escape(titulo)}$", texto, re.M)
        if not achado:
            raise SystemExit(f"Seção não encontrada no edital: {titulo}")
        posicoes.append((achado.start(), achado.end(), titulo, materia))
    posicoes.sort()
    secoes = []
    for i, (_, fim_titulo, titulo, materia) in enumerate(posicoes):
        fim = posicoes[i + 1][0] if i + 1 < len(posicoes) else len(texto)
        secoes.append((titulo, materia, texto[fim_titulo:fim].strip()))
    return secoes


def dividir_em_topicos(corpo: str) -> list[str]:
    """Junta as linhas e quebra nos tópicos numerados ("1. ", "2 ", ...).

    Só aceita a numeração em sequência (1, 2, 3...), para não confundir com
    números soltos no meio do texto (artigos, leis, subitens como 2.1).
    """
    corrido = " ".join(corpo.split("\n"))
    topicos: list[str] = []
    esperado = 1
    inicio_atual = 0
    for achado in re.finditer(r"(?:(?<=\s)|^)(\d{1,2})\.? (?=[A-ZÁÉÍÓÚÂÊÔÃÕÇ“\"])", corrido):
        if int(achado.group(1)) != esperado:
            continue
        trecho = corrido[inicio_atual : achado.start()].strip()
        if trecho:
            topicos.append(trecho)
        inicio_atual = achado.start()
        esperado += 1
    resto = corrido[inicio_atual:].strip()
    if resto:
        topicos.append(resto)
    return topicos


def main() -> None:
    SAIDA_MD.mkdir(parents=True, exist_ok=True)
    arvore = []
    for titulo, materia, corpo in dividir_em_secoes(texto_do_anexo()):
        topicos = dividir_em_topicos(corpo)
        nome = titulo.title().replace(" Do ", " do ").replace(" Da ", " da ")
        nome = nome.replace(" E ", " e ").replace(" De ", " de ")
        identificador = slug(titulo)
        linhas = [
            f"# {nome}",
            "",
            f"Matéria da prova objetiva: **{materia}**",
            "",
            "Fonte: Anexo II do edital do X Concurso DPE-SP. Extração automática;",
            "em caso de dúvida, vale o PDF em `materiais/edital/`.",
            "",
        ]
        linhas += [f"- {t}" for t in topicos]
        (SAIDA_MD / f"{identificador}.md").write_text("\n".join(linhas) + "\n", "utf-8")
        arvore.append(
            {
                "id": identificador,
                "nome": nome,
                "materia_da_prova": materia,
                "topicos": [
                    {"id": f"{identificador}-{n:02d}", "texto": t}
                    for n, t in enumerate(topicos, 1)
                ],
            }
        )
        print(f"{nome}: {len(topicos)} tópicos, {len(corpo.split())} palavras")
    SAIDA_JSON.write_text(
        json.dumps(arvore, ensure_ascii=False, indent=2) + "\n", "utf-8"
    )


if __name__ == "__main__":
    main()
