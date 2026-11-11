"""Catálogo dos materiais a baixar para o repositório e para o NotebookLM.

Cada item diz O QUE é a norma; ONDE ela está é resolvido pelo baixador
(scripts/baixar_materiais.py), que testa os endereços possíveis no site oficial.

Campos:
    fonte   "planalto" (federal) ou "alesp" (estadual paulista)
    tipo    planalto: "constituicao", "lei", "lcp", "decreto-lei", "decreto"
            alesp:    "constituicao", "lei", "lei.complementar", "decreto"
    numero  número da norma, sem pontos
    ano     ano de publicação
    data    só para a ALESP: "dd.mm.aaaa" (faz parte do endereço)
    nome    nome usual
    grupo   arquivo consolidado do NotebookLM em que a norma entra
    origem  "edital" = citada nominalmente no Anexo II
            "materia" = não citada pelo número, mas é a lei de regência de
            assunto que consta do programa

A lista foi montada a partir do Anexo II do edital. Normas citadas só pelo
nome do assunto (por exemplo "licitação") entram com origem "materia".
"""

from __future__ import annotations


def _p(tipo, numero, ano, nome, grupo, origem="edital"):
    return {
        "fonte": "planalto",
        "tipo": tipo,
        "numero": numero,
        "ano": ano,
        "nome": nome,
        "grupo": grupo,
        "origem": origem,
    }


def _a(tipo, numero, data, nome, grupo, origem="edital"):
    return {
        "fonte": "alesp",
        "tipo": tipo,
        "numero": numero,
        "ano": int(data[-4:]),
        "data": data,
        "nome": nome,
        "grupo": grupo,
        "origem": origem,
    }


CATALOGO = [
    # ---------------------------------------------------------------- constitucional
    _p("constituicao", 0, 1988, "Constituição Federal", "constitucional"),
    _a("constituicao", 0, "05.10.1989", "Constituição do Estado de São Paulo", "constitucional"),
    _p("lei", 13445, 2017, "Lei de Migração", "constitucional"),
    _p("lei", 12016, 2009, "Mandado de Segurança", "constitucional", "materia"),
    _p("lei", 13300, 2016, "Mandado de Injunção", "constitucional", "materia"),
    _p("lei", 9868, 1999, "ADI e ADC", "constitucional", "materia"),
    _p("lei", 9882, 1999, "ADPF", "constitucional", "materia"),
    # ---------------------------------------------------------------- institucional
    _p("lcp", 80, 1994, "Lei Orgânica Nacional da Defensoria Pública", "institucional"),
    _a("lei.complementar", 988, "09.01.2006", "Lei Orgânica da Defensoria Pública de SP", "institucional"),
    _p("lei", 12527, 2011, "Lei de Acesso à Informação", "institucional"),
    _p("lei", 13709, 2018, "Lei Geral de Proteção de Dados", "institucional"),
    # ---------------------------------------------------------------- administrativo e tributário
    _a("lei", 10261, "28.10.1968", "Estatuto dos Funcionários Públicos Civis de SP", "administrativo"),
    _a("lei.complementar", 207, "05.01.1979", "Lei Orgânica da Polícia de SP", "administrativo"),
    _a("lei.complementar", 893, "09.03.2001", "Regulamento Disciplinar da Polícia Militar de SP", "administrativo"),
    _a("lei", 10177, "30.12.1998", "Processo Administrativo Estadual", "administrativo"),
    _a("lei", 14187, "19.07.2010", "Penalidades por discriminação racial (SP)", "administrativo"),
    _a("lei", 10948, "05.11.2001", "Penalidades por discriminação por orientação sexual (SP)", "administrativo"),
    _a("lei", 11199, "12.07.2002", "Proibição de discriminação a pessoas com HIV (SP)", "administrativo"),
    _p("lei", 15263, 2025, "Lei 15.263/2025", "administrativo"),
    _p("lei", 10639, 2003, "Ensino de história e cultura afro-brasileira", "administrativo"),
    _p("lei", 14133, 2021, "Licitações e Contratos", "administrativo", "materia"),
    _p("lei", 8429, 1992, "Improbidade Administrativa", "administrativo", "materia"),
    _p("lei", 9784, 1999, "Processo Administrativo Federal", "administrativo", "materia"),
    _p("lcp", 101, 2000, "Lei de Responsabilidade Fiscal", "administrativo", "materia"),
    _p("lei", 5172, 1966, "Código Tributário Nacional", "administrativo", "materia"),
    # ---------------------------------------------------------------- penal
    _p("decreto-lei", 2848, 1940, "Código Penal", "penal", "materia"),
    _p("decreto-lei", 3688, 1941, "Lei das Contravenções Penais", "penal"),
    _p("lei", 7210, 1984, "Lei de Execução Penal", "penal"),
    _p("lei", 1521, 1951, "Crimes contra a Economia Popular", "penal"),
    _p("lei", 6001, 1973, "Estatuto do Índio", "penal"),
    _p("lei", 7716, 1989, "Crimes de Preconceito", "penal"),
    _p("lei", 8072, 1990, "Crimes Hediondos", "penal"),
    _p("lei", 8137, 1990, "Crimes contra a Ordem Tributária", "penal"),
    _p("lei", 9455, 1997, "Lei de Tortura", "penal"),
    _p("lei", 9503, 1997, "Código de Trânsito Brasileiro", "penal"),
    _p("lei", 9605, 1998, "Crimes Ambientais", "penal"),
    _p("lei", 9613, 1998, "Lavagem de Dinheiro", "penal"),
    _p("lei", 10216, 2001, "Reforma Psiquiátrica", "penal"),
    _p("lei", 10826, 2003, "Estatuto do Desarmamento", "penal"),
    _p("decreto", 9847, 2019, "Regulamento do Estatuto do Desarmamento", "penal"),
    _p("lei", 11340, 2006, "Lei Maria da Penha", "penal"),
    _p("lei", 11343, 2006, "Lei de Drogas", "penal"),
    _p("lei", 12847, 2013, "Sistema Nacional de Prevenção e Combate à Tortura", "penal"),
    _p("lei", 12850, 2013, "Organizações Criminosas", "penal"),
    _p("lei", 13869, 2019, "Abuso de Autoridade", "penal"),
    # ---------------------------------------------------------------- processo penal
    _p("decreto-lei", 3689, 1941, "Código de Processo Penal", "processo-penal", "materia"),
    _p("lei", 9099, 1995, "Juizados Especiais", "processo-penal", "materia"),
    _p("lei", 9296, 1996, "Interceptação Telefônica", "processo-penal", "materia"),
    _p("lei", 12037, 2009, "Identificação Criminal", "processo-penal", "materia"),
    # ---------------------------------------------------------------- civil e empresarial
    _p("lei", 10406, 2002, "Código Civil", "civil", "materia"),
    _p("decreto-lei", 4657, 1942, "Lei de Introdução às Normas do Direito Brasileiro", "civil"),
    _p("lei", 5478, 1968, "Lei de Alimentos", "civil"),
    _p("lei", 6015, 1973, "Registros Públicos", "civil"),
    _p("lei", 6766, 1979, "Parcelamento do Solo Urbano", "civil"),
    _p("lei", 8009, 1990, "Bem de Família", "civil"),
    _p("lei", 8245, 1991, "Lei de Locações", "civil"),
    _p("lei", 10257, 2001, "Estatuto da Cidade", "civil"),
    _p("lei", 11804, 2008, "Alimentos Gravídicos", "civil"),
    _p("lei", 13465, 2017, "Regularização Fundiária", "civil"),
    _a("lei", 10705, "28.12.2000", "ITCMD (SP)", "civil"),
    # ---------------------------------------------------------------- processo civil
    _p("lei", 13105, 2015, "Código de Processo Civil", "processo-civil"),
    _p("lei", 13140, 2015, "Lei de Mediação", "processo-civil"),
    _p("lei", 7347, 1985, "Ação Civil Pública", "processo-civil", "materia"),
    _p("lei", 4717, 1965, "Ação Popular", "processo-civil", "materia"),
    # ---------------------------------------------------------------- difusos e coletivos
    _p("lei", 8078, 1990, "Código de Defesa do Consumidor", "difusos"),
    _p("lei", 14181, 2021, "Lei do Superendividamento", "difusos"),
    _p("decreto", 7962, 2013, "Comércio Eletrônico", "difusos"),
    _p("decreto", 11414, 2023, "Decreto 11.414/2023", "difusos"),
    _p("decreto", 12710, 2025, "Decreto 12.710/2025", "difusos"),
    _p("lei", 9656, 1998, "Planos de Saúde", "difusos"),
    _p("lei", 12965, 2014, "Marco Civil da Internet", "difusos"),
    _p("lei", 8080, 1990, "Lei Orgânica da Saúde", "difusos"),
    _p("lei", 8742, 1993, "Lei Orgânica da Assistência Social", "difusos"),
    _p("lei", 9394, 1996, "Diretrizes e Bases da Educação", "difusos"),
    _p("lei", 13005, 2014, "Plano Nacional de Educação", "difusos"),
    _p("lei", 11947, 2009, "Alimentação Escolar", "difusos"),
    _p("lei", 11346, 2006, "Segurança Alimentar e Nutricional", "difusos"),
    _p("lei", 10741, 2003, "Estatuto da Pessoa Idosa", "difusos"),
    _p("lei", 13146, 2015, "Estatuto da Pessoa com Deficiência", "difusos"),
    _p("lei", 10098, 2000, "Acessibilidade", "difusos"),
    _p("lei", 14126, 2021, "Visão Monocular", "difusos"),
    _p("lei", 12288, 2010, "Estatuto da Igualdade Racial", "difusos"),
    _p("decreto", 7053, 2009, "Política Nacional para a População em Situação de Rua", "difusos"),
    _p("decreto", 7405, 2010, "Programa Pró-Catador", "difusos"),
    _p("decreto", 9073, 2017, "Acordo de Paris", "difusos"),
    _p("lei", 13812, 2019, "Política Nacional de Busca de Pessoas Desaparecidas", "difusos"),
    _p("lei", 12587, 2012, "Mobilidade Urbana", "difusos"),
    _p("lei", 11445, 2007, "Saneamento Básico", "difusos"),
    _p("lei", 14026, 2020, "Novo Marco do Saneamento", "difusos"),
    _p("lei", 9008, 1995, "Fundo de Defesa de Direitos Difusos", "difusos"),
    _a("lei", 6536, "13.11.1989", "Fundo Estadual de Interesses Difusos (SP)", "difusos"),
    _p("lei", 6938, 1981, "Política Nacional do Meio Ambiente", "ambiental"),
    _p("lei", 9433, 1997, "Recursos Hídricos", "ambiental"),
    _p("lei", 9795, 1999, "Educação Ambiental", "ambiental"),
    _p("lei", 9985, 2000, "Unidades de Conservação", "ambiental"),
    _p("lei", 10650, 2003, "Acesso à Informação Ambiental", "ambiental"),
    _p("lei", 12187, 2009, "Política Nacional sobre Mudança do Clima", "ambiental"),
    _p("lei", 12305, 2010, "Resíduos Sólidos", "ambiental"),
    _p("lei", 12334, 2010, "Segurança de Barragens", "ambiental"),
    _p("lei", 12608, 2012, "Proteção e Defesa Civil", "ambiental"),
    _p("lei", 12651, 2012, "Código Florestal", "ambiental"),
    _p("lei", 14119, 2021, "Pagamento por Serviços Ambientais", "ambiental"),
    _p("lei", 14750, 2023, "Lei 14.750/2023", "ambiental"),
    _p("lei", 14755, 2023, "Populações Atingidas por Barragens", "ambiental"),
    _p("lei", 14850, 2024, "Lei 14.850/2024", "ambiental"),
    _p("lei", 14904, 2024, "Adaptação à Mudança do Clima", "ambiental"),
    _p("lei", 14926, 2024, "Lei 14.926/2024", "ambiental"),
    _p("lei", 15042, 2024, "Mercado de Carbono", "ambiental"),
    _p("lei", 15190, 2025, "Lei Geral do Licenciamento Ambiental", "ambiental"),
    _p("lei", 15432, 2026, "Lei 15.432/2026", "ambiental"),
    _p("lei", 15506, 2026, "Lei 15.506/2026", "ambiental"),
    # ---------------------------------------------------------------- criança e adolescente
    _p("lei", 8069, 1990, "Estatuto da Criança e do Adolescente", "crianca"),
    _p("lei", 12594, 2012, "SINASE", "crianca"),
    _p("lei", 12852, 2013, "Estatuto da Juventude", "crianca"),
    _p("lei", 13185, 2015, "Combate à Intimidação Sistemática", "crianca"),
    _p("lei", 13257, 2016, "Marco Legal da Primeira Infância", "crianca"),
    _p("lei", 13431, 2017, "Escuta Protegida", "crianca"),
    _p("lei", 14344, 2022, "Lei Henry Borel", "crianca"),
    _p("lei", 15211, 2025, "Lei 15.211/2025", "crianca"),
    _p("decreto", 99710, 1990, "Convenção sobre os Direitos da Criança", "crianca", "materia"),
    _p("decreto", 3087, 1999, "Convenção de Haia sobre Adoção Internacional", "crianca"),
    # ---------------------------------------------------------------- direitos humanos (tratados internalizados)
    _p("decreto", 678, 1992, "Convenção Americana sobre Direitos Humanos", "humanos", "materia"),
    _p("decreto", 592, 1992, "Pacto Internacional sobre Direitos Civis e Políticos", "humanos", "materia"),
    _p("decreto", 591, 1992, "Pacto Internacional sobre Direitos Econômicos, Sociais e Culturais", "humanos", "materia"),
    _p("decreto", 3321, 1999, "Protocolo de San Salvador", "humanos", "materia"),
    _p("decreto", 40, 1991, "Convenção contra a Tortura", "humanos", "materia"),
    _p("decreto", 4377, 2002, "Convenção sobre a Eliminação da Discriminação contra a Mulher", "humanos"),
    _p("decreto", 1973, 1996, "Convenção de Belém do Pará", "humanos", "materia"),
    _p("decreto", 6949, 2009, "Convenção sobre os Direitos das Pessoas com Deficiência", "humanos", "materia"),
    _p("decreto", 10932, 2022, "Convenção Interamericana contra o Racismo", "humanos", "materia"),
    _p("decreto", 65810, 1969, "Convenção sobre a Eliminação da Discriminação Racial", "humanos", "materia"),
    _p("decreto", 10088, 2019, "Convenções da OIT consolidadas (inclui a 169)", "humanos"),
    _p("decreto", 5051, 2004, "Convenção 169 da OIT (decreto original, revogado)", "humanos"),
    _p("decreto", 4388, 2002, "Estatuto de Roma", "humanos", "materia"),
    _p("decreto", 7030, 2009, "Convenção de Viena sobre o Direito dos Tratados", "humanos", "materia"),
]

# Itens do edital que o baixador ainda NÃO cobre. Ficam registrados aqui para
# não se perderem; cada um exige descobrir o endereço oficial e, em alguns
# casos, liberar mais um site.
PENDENTES = [
    "Lei 13.512/2026 (citada em Difusos; a numeração não bate com o ano, conferir no edital)",
    "Lei Estadual 10.365/1999 e Decretos Estaduais 55.334/2010 e 55.370/2010 (Civil): falta a data exata para o endereço da ALESP",
    "Deliberações CSDP 63/08, 89/08, 120/09, 134/09, 187/10, 219/11, 249/12, 270/13, 291/14, 296/14, 297/14, 373/20 e 400/22 (site da DPE-SP)",
    "Atos Normativos DPG 146/18, 183/20, 216/22 e 295/2025 (site da DPE-SP)",
    "Resoluções CNJ 35/2007, 125/2010, 213/2015, 287/2019, 345/2021, 372/2021, 385/2021, 412/2021, 414/2021, 425/2021, 492/2023, 598/2024; Recomendação CNJ 163/2025; Provimento CNJ 16/2012 (site do CNJ, ainda não liberado)",
    "Resoluções CONANDA 113/2006 e 119/2006; Resolução Conjunta CNAS/CONANDA 1/2009",
    "Resolução Condege 1/2024",
    "Súmulas vinculantes e súmulas do STF; súmulas do STJ; teses de repercussão geral e de repetitivos",
    "Documentos internacionais sem decreto: Regras de Mandela, de Bangkok e de Brasília; Protocolos de Istambul e de Minnesota; Opiniões Consultivas 23/2017 e 32/2025 da Corte IDH; Carta Africana",
    "Provas objetivas anteriores (VIII e IX concursos) e gabaritos: a FCC só expõe os gabaritos por formulário; os cadernos de questões não estão mais na página",
]

# Obras indicadas no edital para Filosofia do Direito e Sociologia Jurídica
# ("de cujos conteúdos serão extraídas as questões"). São livros protegidos:
# não são baixados; ficam aqui como referência.
BIBLIOGRAFIA_INDICADA = [
    "DELGADO, R.; STEFANCIC, J. Teoria crítica da raça: uma introdução. 3. ed. Contracorrente, 2021.",
    "FOUCAULT, M. A verdade e as formas jurídicas. 4. ed. Nau, 2013.",
    "KELSEN, H. Teoria geral do direito e do Estado. 5. ed. Martins Fontes, 2016.",
    "MBEMBE, A. Necropolítica. n-1 edições, 2018.",
    "PLATÃO. A República. Martins Fontes, 2006.",
]
