# Etapas de desenvolvimento do app de apoio ao X Concurso DPE-SP

> Escrito em 11/11/2026. Complementa o `PLANEJAMENTO.md`. Ainda sem código: a codificação começa na Etapa 0 deste documento.
> Prova objetiva: 10/01/2027 (60 dias).

---

## 1. Decisões já tomadas

| Tema | Decisão |
|---|---|
| Inscrição | Feita |
| Cenário | B: MVP enxuto sob medida, desde já |
| Chat próprio | Fora. No lugar, um caderno no NotebookLM com o material baixado |
| Prova diagnóstica | Não haverá. Diagnóstico acontece durante o uso |
| Quem define "imprescindível" | Eu (critérios na seção 3), com ajustes quando ela pedir |
| Idioma | Tudo em português: interface, código, commits |
| Materiais | Ficam versionados no repositório |
| Telegram | **Não usar** (ver abaixo) |
| Stack | Next.js + Vercel + Supabase + e-mail transacional; LLM só no pipeline offline |

**Sobre o Telegram:** a vantagem existe (entrega mais confiável que push no iOS), mas não é "muito vantajosa" a ponto de pedir a uma pessoa sem tempo que instale e passe a olhar mais um aplicativo. Push + e-mail diário cobre o caso. Reabrimos só se o push falhar na prática.

---

## 2. O que as suas respostas mudam na minha avaliação

Três consequências que você não mencionou e que alteram o desenho:

1. **Com pouco tempo por dia, a micro-sessão deixa de ser complemento e vira o modo principal de estudo.** No documento anterior eu disse que nudge não é método. Com trabalho e dois filhos pequenos, ela não terá blocos longos, então o app precisa extrair o máximo de sessões de 5 a 15 minutos. Isso muda o conteúdo: cada sessão tem que ser de **questões reais e lei seca**, não de leitura.
2. **Cobrir o edital inteiro é impossível, e o plano precisa dizer isso por escrito.** Supondo 40 minutos por dia, são cerca de 40 horas até a prova. Para 11 disciplinas, dá menos de 4 horas por disciplina. A estratégia deixa de ser "ver tudo que é imprescindível" e passa a ser "garantir pontos onde eles são mais baratos". Ela já passou da primeira fase uma vez: a base existe, e o trabalho é reativar e atualizar, não aprender do zero.
3. **Sem prova diagnóstica, as duas primeiras semanas rodam às cegas.** Para compensar, as primeiras sessões precisam **amostrar todas as disciplinas** de propósito, mesmo as de baixa prioridade, até haver uns 15 a 20 itens respondidos em cada uma. Só então a priorização por desempenho começa a valer. Isso é uma regra do algoritmo de seleção, não um detalhe.

**Premissa que estou assumindo e que você deve corrigir:** 40 minutos por dia, fragmentados, em 6 dias por semana. Se for 20 minutos, corto mais disciplinas; se for 90, o plano afrouxa. Preciso do número real antes da Etapa 4.

---

## 3. Como vou definir "imprescindível"

Cada tema do edital recebe uma faixa (A = imprescindível, B = importante, C = só se sobrar) a partir de quatro critérios, nesta ordem de peso:

1. **Incidência histórica:** quantas questões o tema rendeu nas provas objetivas anteriores da FCC para a DPE-SP (e, como reforço, para outras Defensorias pela FCC). Dado extraído das próprias provas, não de opinião.
2. **Custo por ponto:** temas resolvidos por lei seca ou súmula (resposta literal) valem mais por minuto do que temas que pedem construção doutrinária.
3. **Mudou desde 2019:** tema alterado por lei ou por decisão vinculante sobe de faixa, porque ali o conhecimento antigo dela produz erro, não só lacuna.
4. **Desempenho dela:** entra quando houver dados. Tema com acerto alto e estável desce; tema de alta incidência com erro recorrente sobe.

O resultado é um arquivo legível (`conteudo/temas.yaml` + uma versão em tabela) que você e ela podem ler e contestar. Tudo o que ficar na faixa C está, na prática, cortado, e isso ficará explícito.

Limite honesto: o critério 1 depende de eu classificar centenas de questões antigas por tema, o que é feito com apoio de LLM e terá erros de classificação. Erro aqui desloca prioridade, não ensina Direito errado, então o risco é aceitável.

---

## 4. Dois bloqueios descobertos ao preparar este documento

### 4.1. Não consegui ler o edital

O ambiente em que rodo bloqueia o acesso aos sites onde o PDF está. **Preciso que você coloque o PDF do edital no repositório** (pasta `materiais/edital/`). Até lá, a lista de disciplinas e de materiais abaixo é **provisória**, baseada no padrão dos concursos anteriores da DPE-SP, e pode estar errada para este edital.

### 4.2. O script de download não roda daqui sem liberação de rede

Testei: `planalto.gov.br` também está bloqueado. Há duas saídas:

- **(a) Liberar os domínios neste ambiente.** Eu proponho a alteração e você aprova num clique. Depois disso, eu escrevo, executo e faço o commit dos materiais. Domínios: `www.planalto.gov.br`, `www.al.sp.gov.br`, `portal.stf.jus.br`, `www.stj.jus.br`, `scon.stj.jus.br`, `www.defensoria.sp.def.br`, `www.concursosfcc.com.br`. A lista final sai do edital.
- **(b) Você roda o script na sua máquina** e faz o commit da pasta. Funciona, mas a cada ajuste do script o ciclo passa por você.

Recomendo (a). Há um risco que independe da escolha: sites de governo costumam recusar acessos automatizados vindos de datacenter. Se isso acontecer com algum deles, o plano B é a opção (b) só para aquele site.

---

## 5. Materiais para o repositório e para o NotebookLM (lista provisória)

Estrutura de pastas:

```
materiais/
  edital/            edital e retificações (você fornece)
  provas/            provas objetivas anteriores + gabaritos definitivos
  legislacao/        um arquivo .md por norma, texto limpo, com URL e data de captura
  tratados/          idem, para normas internacionais
  jurisprudencia/    súmulas e teses vinculantes
  institucional/     normas e teses da própria DPE-SP
  notebooklm/        arquivos consolidados por disciplina, prontos para subir
  MANIFESTO.md       índice gerado: o que foi baixado, de onde, quando, hash
```

**Disciplinas presumidas** (padrão dos concursos anteriores; confirmar no edital): Constitucional; Administrativo e Tributário; Penal; Processual Penal; Civil; Processual Civil; Direitos Difusos e Coletivos; Criança e Adolescente; Direitos Humanos; Princípios e Atribuições Institucionais da Defensoria; Filosofia do Direito e Sociologia Jurídica.

**Legislação federal (Planalto, texto compilado):**

- Constituição Federal de 1988
- Código Penal; Código de Processo Penal; Lei de Execução Penal (7.210/84)
- Lei de Drogas (11.343/06); Maria da Penha (11.340/06); Crimes Hediondos (8.072/90); Juizados (9.099/95); Abuso de Autoridade (13.869/19); Organizações Criminosas (12.850/13)
- Código Civil; Código de Processo Civil; Lei de Alimentos (5.478/68); Lei de Locações (8.245/91)
- Código de Defesa do Consumidor (8.078/90); Ação Civil Pública (7.347/85); Mandado de Segurança (12.016/09); Mandado de Injunção (13.300/16)
- ECA (8.069/90); SINASE (12.594/12); Escuta Protegida (13.431/17); Primeira Infância (13.257/16); Henry Borel (14.344/22)
- Improbidade (8.429/92, com a reforma de 2021); Processo Administrativo (9.784/99); Licitações (14.133/21); Código Tributário Nacional
- Estatuto da Cidade (10.257/01); Regularização Fundiária (13.465/17)
- Pessoa Idosa (10.741/03); Pessoa com Deficiência (13.146/15); Saúde Mental (10.216/01); SUS (8.080/90); LOAS (8.742/93)
- Igualdade Racial (12.288/10); Crimes de Preconceito (7.716/89); Migração (13.445/17); LGPD (13.709/18)
- LC 80/94 (Lei Orgânica Nacional da Defensoria)

**Legislação estadual (ALESP):** Constituição do Estado de São Paulo; LC estadual 988/06 (Lei Orgânica da DPE-SP).

**Tratados e normas internacionais:** Convenção Americana de Direitos Humanos; Pacto de Direitos Civis e Políticos; Pacto de Direitos Econômicos, Sociais e Culturais; Convenção contra a Tortura; Convenção sobre os Direitos da Criança; CEDAW; Convenção de Belém do Pará; Convenção sobre os Direitos das Pessoas com Deficiência; Convenção 169 da OIT; Convenção Interamericana contra o Racismo; Regras de Mandela; Regras de Bangkok; 100 Regras de Brasília.

**Jurisprudência:** súmulas vinculantes e súmulas do STF; súmulas do STJ; teses de repercussão geral; teses de recursos repetitivos. Informativos ficam fora da primeira carga (volume alto, valor por minuto baixo para ela).

**Institucional (site da DPE-SP):** deliberações do Conselho Superior citadas no edital; teses institucionais.

**Provas (site da FCC):** provas objetivas e gabaritos definitivos dos concursos anteriores da DPE-SP. Em seguida, provas da FCC para outras Defensorias estaduais desde 2019.

**Fora de propósito:** doutrina (não baixamos; indicamos por referência) e textos de Filosofia e Sociologia, que são obras autorais. Para essa disciplina, o material será o programa do edital mais as questões anteriores.

### Cuidados do script (onde os erros costumam nascer)

- **Texto riscado do Planalto.** As páginas compiladas mantêm a redação revogada com tachado. Uma conversão ingênua para texto apaga o tachado e deixa a **redação revogada parecendo vigente**. O script tem que remover esses trechos antes de converter. É o erro mais perigoso de todo o pipeline, justamente para quem está 7 anos desatualizada.
- **Codificação.** As páginas do Planalto não usam UTF-8; converter errado corrompe acentos e quebra a validação de citações depois.
- **Rastreabilidade.** Cada arquivo leva cabeçalho com URL de origem, data de captura e hash. O `MANIFESTO.md` é gerado, nunca escrito à mão.
- **Idempotência.** Rodar de novo só baixa o que mudou, e mostra o que mudou (uma lei alterada em dezembro aparece como diff).
- **Limite do NotebookLM.** O plano gratuito limita a quantidade de fontes por caderno (era 50; conferir o valor atual). Por isso a pasta `notebooklm/` consolida as normas em poucos arquivos por disciplina.
- **Verificação por amostragem.** Antes de subir ao NotebookLM, conferimos à mão alguns artigos sabidamente alterados (por exemplo, dispositivos do CPP mexidos pelo Pacote Anticrime) contra o site oficial.

---

## 6. Etapas

Princípio: **cada etapa termina com algo que ela usa no celular**, e nenhuma etapa depende de uma posterior para ter valor. As durações supõem você mexendo um pouco todo dia e eu fazendo a maior parte da codificação.

### Etapa 0. Insumos (dia 1)

- Você: PDF do edital no repositório; decisão sobre a rede (4.2); minutos por dia que ela tem.
- Eu: extrair disciplinas e conteúdo programático para `conteudo/temas.yaml`; reconferir datas e regras (cláusula de barreira, penalidade por erro, data de corte da legislação); fechar a lista de materiais.
- **Artefato:** tabela de temas do edital, legível, ainda sem prioridade.

### Etapa 1. Materiais e NotebookLM (dias 1 a 2)

- Script de download e limpeza; pasta `materiais/` populada e versionada; arquivos consolidados por disciplina.
- Você cria o caderno no NotebookLM, sobe os arquivos de `materiais/notebooklm/` e compartilha com ela.
- **Artefato:** ela tem um lugar para tirar dúvidas com base em texto oficial atualizado. Primeiro ganho real, antes de existir app.

### Etapa 2. Sessão de questões (dias 2 a 4)

- Extração das provas anteriores da DPE-SP para formato estruturado (enunciado, alternativas, gabarito, ano, disciplina). Validação mecânica: contagem de questões por prova, gabarito presente, anuladas marcadas.
- Projeto Supabase + Vercel; login por link mágico; uma tela: "sessão de hoje" com N questões, resposta, gabarito, registro do resultado.
- Seleção ainda simples: rodízio entre disciplinas (é o que alimenta o diagnóstico).
- **Artefato:** ela abre um link no iPhone e resolve questões reais. A partir daqui cada resposta vira dado.
- Ressalva exibida na tela: gabarito de prova antiga pode estar superado por mudança de lei.

### Etapa 3. E-mail diário (dias 4 a 5)

- Um e-mail por manhã, no horário que ela escolher, com o link da sessão do dia e um resumo de uma linha (sequência de dias, acerto da semana).
- **Artefato:** primeiro "nudge" funcionando, pelo canal confiável. Vem antes do push de propósito: se o push der trabalho, ela já não depende dele.

### Etapa 4. Faixas, plano e painel (dias 5 a 8)

- Classificação das questões antigas por tema; cálculo de incidência; faixas A/B/C aplicadas ao `temas.yaml`.
- Plano de datas: temas A distribuídos até ~27/12, com folgas de fim de ano já previstas; últimos dias reservados a revisão.
- Painel com quatro números: dias restantes; cobertura dos temas A contra o esperado para hoje; acerto por disciplina; pendências.
- **Artefato:** a página de acompanhamento que você pediu. Você e ela passam a enxergar se vai dar tempo.

### Etapa 5. Instalação no iPhone e push (dias 8 a 10)

- Manifesto e service worker; tela de instrução para adicionar à Tela de Início pelo Safari; pedido de permissão; agendamento de envios; tratamento de assinatura expirada.
- Dois a três nudges por dia, em horários definidos por ela, cada um abrindo direto em **uma** questão.
- **Artefato:** micro-sessões ao longo do dia. O e-mail continua como redundância.

### Etapa 6. Repetição espaçada e cards de lei seca (dias 10 a 14)

- Algoritmo de espaçamento pronto (FSRS) sobre os erros dela: o que ela errou volta em intervalos crescentes.
- Pipeline de cards gerados a partir do corpus, com citação literal validada por script contra `materiais/`. Começa pelos temas A com marca "mudou desde 2019".
- Cada item com selo de origem e botão "isso está errado".
- **Artefato:** o app passa de "banco de questões" a "sistema de revisão" e entrega o delta de atualização.

### Etapa 7. Seleção adaptativa e replanejamento (dias 14 a 18)

- A seleção passa a pesar faixa × desempenho × tempo desde a última revisão.
- Atrasou? O plano se recalcula cortando de baixo para cima e mostra o que foi cortado.
- **Artefato:** o plano deixa de ser estático.

### Contínuo, a partir da Etapa 6

- Ampliar conteúdo: mais disciplinas no pipeline de cards, provas da FCC de outras Defensorias.
- Corrigir o que ela reportar.

### Congelamento

- **Até 20/12:** fim de funcionalidades novas. Depois disso, só conteúdo e correções.
- **A partir de 31/12:** nenhuma mudança de código, salvo defeito que impeça o uso.

### O que fica de fora, de propósito

Chat próprio, simulado cronometrado dentro do app, estatísticas detalhadas, múltiplos usuários, modo offline. Se sobrar tempo, o primeiro candidato é o simulado, porque resistência para 4h30 não se treina em micro-sessões. Sem ele, recomendo que ela faça ao menos uma prova inteira em papel num domingo de dezembro.

---

## 7. A defesa do cenário D, na versão mais simples possível

Você rejeitou D para não perder tempo aprendendo Anki ou outro produto. Concordo com o motivo: para alguém sem tempo, ferramenta nova é custo puro. Mas D não precisa de ferramenta nenhuma. Na versão que proponho, ele se reduz a isto:

- **Hoje:** você manda para ela, pelo WhatsApp, o PDF da prova objetiva do último concurso da DPE-SP e o gabarito em arquivo separado.
- **Todo dia, até a Etapa 2 ficar pronta (3 a 4 dias):** ela resolve 10 questões no próprio PDF, no celular, e responde a você com uma linha: `1A 2C 3E ...`.
- **Quando a Etapa 2 entrar no ar:** eu carrego essas respostas no banco. O app nasce com 30 a 40 respostas dela, ou seja, com o começo do diagnóstico que hoje não temos.

Custo para você: cinco minutos hoje. Custo para ela: zero aprendizado, e o mesmo tempo que ela gastaria estudando de qualquer forma. O que isso compra:

- **Três ou quatro dias de estudo** que no cenário B puro são dias de espera. Em 60, é cerca de 6% da janela.
- **Dados de diagnóstico mais cedo**, o que compensa em parte a falta da prova diagnóstica.
- **Um teste do hábito antes do app.** Se ela não conseguir fazer 10 questões por dia com um PDF, o problema não é de ferramenta, e é melhor descobrir isso agora do que depois de dez dias de desenvolvimento.

O argumento contrário mais forte: a prova do último concurso é a melhor amostra que temos, e "gastá-la" em doses de 10 pode parecer desperdício. Não é, porque ela não fará simulado diagnóstico de qualquer forma, e questões resolvidas no PDF voltam a aparecer no app via repetição espaçada.

Se ainda assim preferir B puro, nada no plano de etapas muda.

---

## 8. O que preciso de você para começar a Etapa 0

1. **PDF do edital** (e retificações, se houver) em `materiais/edital/`.
2. **Rede:** opção (a), liberar domínios aqui, ou (b), você roda o script localmente?
3. **Minutos por dia** que ela realmente tem, e os horários em que o celular está à mão.
4. **D mínimo:** sim ou não?
5. **Contas:** você cria os projetos no Supabase e na Vercel e me passa as chaves pelo mecanismo seguro do ambiente (nunca coladas na conversa), ou prefere que eu deixe tudo pronto para você configurar?
6. **O repositório é privado?** Precisa ser, já que vai conter provas, respostas dela e o material baixado.
