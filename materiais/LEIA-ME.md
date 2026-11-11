# Materiais

Texto oficial usado pelo app e pelo caderno do NotebookLM. Nada aqui é escrito à mão: tudo vem do edital ou de sites oficiais, por script.

| Pasta | Conteúdo |
|---|---|
| `edital/` | Edital do X Concurso (PDF publicado pela FCC) |
| `legislacao/` | Uma norma por arquivo, em texto limpo, com endereço de origem e data de captura |
| `notebooklm/` | As mesmas normas consolidadas por grupo, prontas para subir ao NotebookLM |
| `MANIFESTO.md` | O que foi baixado, o que falta e o que o edital cita e ainda não está coberto |

## Como baixar a legislação federal (Planalto)

O site do Planalto recusa conexões vindas do ambiente em nuvem onde o projeto é desenvolvido, então esta parte precisa rodar em um computador comum, no Brasil:

```bash
python3 scripts/baixar_materiais.py
```

Leva alguns minutos (há uma pausa de 1 segundo entre os acessos). Ao final, confira `materiais/MANIFESTO.md` e faça o commit da pasta `materiais/`. Rodar de novo só busca o que faltou; com `--refazer`, baixa tudo outra vez e avisa quando o texto de alguma norma mudou.

## Texto revogado

Os sites oficiais mantêm a redação revogada na página, tachada. O script remove esses trechos antes de converter, para que redação antiga não apareça como vigente. O manifesto mostra quantos caracteres foram removidos de cada norma e avisa quando a página tem um tachado que nunca é fechado, caso em que pode ter sumido texto vigente e a norma precisa ser conferida no site.

A remoção foi testada com páginas reais da ALESP. Com páginas do Planalto ainda não foi, porque não há acesso daqui: depois da primeira execução, vale conferir alguns artigos sabidamente alterados (por exemplo, os do Código de Processo Penal mexidos pela Lei 13.964/2019) contra o site.

## Como montar o caderno no NotebookLM

1. Criar um caderno novo em notebooklm.google.com.
2. Adicionar como fontes todos os arquivos de `materiais/notebooklm/` e o PDF do edital.
3. Compartilhar o caderno com ela.

Sempre que o script for executado de novo, os arquivos de `notebooklm/` são regenerados e precisam ser substituídos no caderno.
