# App de apoio ao X Concurso DPE-SP: avaliação, riscos, cenários e decisões

> Documento de planejamento, escrito em 11/11/2026. Nenhuma linha de código ainda.
> O objetivo é decidir **o que** construir (e o que não construir) antes de codificar.

---

## 0. Resumo executivo

1. **Verifique hoje se ela está inscrita.** Segundo os portais de concurso, as inscrições se encerram em **11/11/2026** (hoje), com boleto vencendo em 12/11. Se ela não se inscreveu, nada abaixo importa.
2. **O maior risco do projeto não é técnico, é o calendário.** A prova objetiva está marcada para **10/01/2027**: são 60 dias. Cada semana gasta construindo o app é ~12% da janela de estudo em que ela fica sem a ferramenta. Um app que fica pronto no dia 30 é pior que uma planilha no dia 1.
3. **"Nudge" não é método de estudo, é complemento.** Uma prova de 88 questões em 4h30, cobrindo 11 disciplinas, não se vence com lembretes de 3 minutos. O que mais prevê nota em prova objetiva da FCC é **resolver questões anteriores da banca** e ler **lei seca**. O plano como você descreveu não tem questões no centro; deveria ter.
4. **O conhecimento dela está 7 anos desatualizado, e isso é mais perigoso do que não saber.** Ela vai responder com confiança coisas que mudaram (Pacote Anticrime, nova LIA, nova Lei de Licitações, juiz das garantias, etc.). O recurso de maior valor que um app sob medida pode entregar é um **"delta 2019 → 2026"**: o que mudou em cada tema desde a última vez que ela estudou. Isso não estava na sua lista.
5. **Alucinação se resolve com processo, não com prompt.** Conteúdo gerado em lote, offline, com citação literal obrigatória do texto legal e validação automática de que a citação existe na fonte. Chat livre ao vivo é o ponto de maior risco e maior custo: fica para depois.
6. **Recomendação:** cenário híbrido (seção 6, cenário D). Dia 1: ferramentas prontas para ela começar a estudar já. Dias 2 a 8: MVP enxuto (plano + acompanhamento + nudges com conteúdo curado + e-mail diário). Sem chat próprio na v1.

---

## 1. Fatos do concurso (a confirmar no PDF oficial)

Os dados abaixo vêm de portais de cursinhos, **não do PDF do edital**. Baixar o edital no site da FCC é a primeira tarefa e todo número aqui deve ser reconferido nele.

| Item | Informação (fonte: portais) | Status |
|---|---|---|
| Concurso | X Concurso para Defensor(a) Público(a) do Estado de SP | a confirmar |
| Banca | Fundação Carlos Chagas (FCC) | consistente entre fontes |
| Publicação do edital | 09/10/2026 | consistente |
| Inscrições | 13/10 a **11/11/2026**, taxa R$ 250, boleto até 12/11 | consistente |
| Prova objetiva | **10/01/2027** (domingo), manhã | consistente |
| Formato | 88 questões, 5 alternativas, 4h30 | consistente |
| Nota mínima | 44 acertos (ampla) / 35 (reserva de vagas) | uma fonte |
| Disciplinas | 11 disciplinas | uma fonte; lista não obtida |
| Questões por disciplina | uma fonte diz que o edital **não fixa** | divergente, conferir |
| Convocação / locais | 04/12/2026 | uma fonte |
| 2ª e 3ª provas (dissertativas) | 03 e 04/07/2027 | uma fonte |
| Prova oral | a definir | - |

**Pontos que o edital precisa responder e que mudam o plano:**

- **Há cláusula de barreira?** 44 acertos é o mínimo, mas concursos de Defensoria costumam limitar quantos avançam para a segunda fase. Se houver, a meta real é a nota de corte histórica, não 44. Isso define o quão agressiva precisa ser a preparação.
- **Lista exata das disciplinas e do conteúdo programático.** É a espinha dorsal do app (árvore de temas).
- **Há peso ou número mínimo por disciplina/bloco?** Se sim, não dá para "abandonar" uma matéria.
- **Bibliografia indicada?** Se o edital indicar obras, isso alimenta o item 3 do seu pedido (fontes).
- **Datas de corte de legislação.** Editais costumam dizer que alterações posteriores à publicação não são cobradas.

---

## 2. Avaliação crítica de cada ideia

### 2.1. Modelo "nudge" (notificações + flashcards + perguntas)

**O que está certo:** recuperação ativa (ser perguntado) e repetição espaçada são as duas técnicas de estudo com evidência mais sólida. Micro-sessões aproveitam tempo morto.

**O que está fraco:**

- **Nudge refresca, não ensina.** Funciona para o que ela já soube um dia. Para o que mudou ou para o que ela nunca dominou, um card de 2 minutos não basta. Se o app virar a atividade principal, ela terá a sensação de estar estudando sem estar.
- **Fadiga de notificação.** Depois de uma semana, notificação de app de estudo vira ruído e é silenciada. O desenho precisa partir do princípio de que ela vai ignorar a maioria.
- **Tema aleatório ≠ tema certo.** "Trazer um tema que vai cair" só tem valor se a escolha seguir uma lógica: revisão espaçada do que ela já viu + reforço do que ela errou. Tema novo por notificação é desperdício.
- **Você não sabe a rotina dela.** Ela trabalha? Quantas horas por dia tem? Em que horários o celular está na mão? Sem isso, o agendamento é chute.

**Mitigações:**

- Nudges puxam **somente** itens de revisão (temas já estudados no plano) e erros anteriores. Tema novo entra pelo plano de estudo, em bloco de estudo de verdade.
- Ela controla: quantidade por dia (padrão baixo, 3 a 4), janelas de horário, modo silêncio, "adiar 1h".
- Cada nudge é **uma pergunta respondível em menos de 60 segundos** na própria tela, não um texto para ler. Depois da resposta: gabarito, artigo de lei literal, link para aprofundar.
- Algoritmo de espaçamento pronto (FSRS ou SM-2). Não inventar.
- Medir: taxa de abertura e de resposta por horário. Se cair abaixo de ~30%, reduzir frequência automaticamente.

### 2.2. Material (edital → leis → doutrina) e alucinação

**O que está certo:** partir do edital e ancorar em texto legal oficial é o caminho correto.

**O que está fraco ou arriscado:**

- **"Baixar doutrinas que estiverem disponíveis"** é um problema. Doutrina boa e atual é protegida por direito autoral; o que está "disponível" de graça costuma ser pirata ou velho. Doutrina velha num cenário em que o problema dela é justamente desatualização é contraproducente. E há ironia evidente em construir um app para futura Defensora sobre material pirateado.
- **O modelo de linguagem também está desatualizado.** Qualquer LLM tem data de corte e mistura redações antigas e novas de artigos. Em Direito, uma resposta 95% certa é uma resposta errada, e ela não tem como distinguir.
- **Jurisprudência é o pior caso.** LLMs inventam número de súmula, de tema repetitivo e de informativo com total naturalidade.
- **Quem revisa?** Nem você (imagino que não seja da área) nem eu podemos garantir correção jurídica. A única revisora qualificada é ela, e o tempo dela é o recurso escasso.

**Mitigações (em ordem de importância):**

1. **Corpus fechado de fontes primárias oficiais.** Planalto (legislação federal compilada), ALESP (legislação estadual, incluindo a lei orgânica da DPE-SP), STF e STJ (súmulas, teses de repercussão geral e repetitivos, informativos), site da própria DPE-SP (deliberações do Conselho Superior, teses institucionais), tratados de direitos humanos em fonte oficial. Tudo baixado, versionado no repositório com data de captura.
2. **Geração em lote, offline, nunca ao vivo.** Os cards são gerados por script, viram arquivos no git, e só entram no banco depois de passar pela validação. Isso transforma "o modelo alucinou em produção" em "um diff que alguém pode ler".
3. **Citação literal obrigatória + validação mecânica.** Todo card precisa trazer o trecho exato da fonte que sustenta a resposta. Um script verifica que o trecho é substring do documento-fonte. Card sem citação válida é descartado. Isso não garante que a interpretação está certa, mas elimina artigo inventado e redação revogada.
4. **Preferir questões reais a questões geradas.** Provas anteriores da FCC para Defensorias (SP e outros estados) são públicas, com gabarito oficial. Texto de questão real tem zero alucinação e ainda treina o estilo da banca. Ressalva: gabarito antigo pode estar superado por mudança de lei, o que exige marcar a data da prova e sinalizar questões de temas alterados.
5. **Selo visível de confiança em cada item:** "texto de lei literal", "questão oficial FCC (ano)", "explicação gerada por IA, confira na fonte". Ela precisa saber em que pode confiar cegamente.
6. **Botão "isso está errado".** Um toque, o item sai de circulação e vai para uma fila. Ela é a revisora, mas com custo de um toque.
7. **Doutrina: não baixar, apontar.** Indicar obra e capítulo (do que ela já possui ou do que o edital indicar). O app não reproduz doutrina.

**Risco residual que não some:** explicações geradas por IA sobre *por que* uma alternativa está errada podem estar sutilmente erradas mesmo com a citação correta. A defesa é a cultura de uso: o app aponta, a lei seca decide.

### 2.3. Indicação de fontes por assunto

**É a ideia mais sólida da lista** e, ao mesmo tempo, a mitigação do item anterior. Cuidados:

- **Links profundos, não genéricos.** "Veja o CPP" não serve. Tem que ser o artigo, com âncora no Planalto. Links para jurisprudência devem ir à página oficial do tribunal.
- **Links gerados por LLM são inventados com frequência.** Toda URL deve ser montada por regra a partir do corpus (lei + artigo → URL) ou verificada por script (HTTP 200 + trecho presente na página). Nunca aceitar URL "de memória" do modelo.
- **Três níveis por tema:** (a) lei seca, artigos exatos; (b) jurisprudência vinculante/sumulada; (c) aprofundamento (doutrina por referência, material institucional da DPE-SP).

### 2.4. Plano de estudo e página de acompanhamento

**O que está certo:** sem isso, o resto é entretenimento. É a única parte que responde "vai dar tempo?".

**O que está fraco:**

- **"Ver tudo que é imprescindível" exige definir "imprescindível", e o edital não diz isso.** O edital lista tudo com o mesmo peso. A priorização vem de: (a) incidência histórica nas provas da FCC para DPE; (b) o que mudou desde 2019; (c) onde ela é fraca. Sem (c), o plano é genérico.
- **Não há diagnóstico.** Você não sabe o nível atual dela. Ela pode estar em 55% ou em 30% de acertos, e os dois casos pedem planos opostos.
- **Plano estático morre na primeira semana ruim.** Natal e Ano-Novo caem dentro da janela. O plano precisa se recalcular quando ela atrasa, cortando o menos prioritário em vez de empilhar atraso.
- **Barrinha de progresso mede o que é fácil medir.** "Temas vistos" sobe mesmo sem aprendizado. A métrica que importa é **taxa de acerto em questões por disciplina** e o resultado dos simulados.

**Mitigações:**

- **Dia 1: diagnóstico.** Ela faz a prova objetiva do concurso anterior da DPE-SP, cronometrada. Resultado por disciplina vira a entrada do plano. É também o melhor choque de realidade sobre o formato após 7 anos.
- **Orçamento de tempo explícito.** 60 dias, menos ~12 dias finais reservados a revisão e simulados, menos folgas realistas: sobram cerca de 40 dias de conteúdo novo. Horas por dia × 40 = o orçamento. Os temas cabem nisso ou são cortados, por escrito.
- **Três faixas por tema:** imprescindível / importante / se sobrar tempo. Replanejamento automático corta de baixo para cima.
- **Painel com quatro números:** dias restantes; % dos temas imprescindíveis cobertos vs. % esperado para hoje; taxa de acerto por disciplina (últimos 7 dias); revisões pendentes. Nada mais na primeira tela.
- **Simulados completos agendados** (pelo menos 3, no horário da prova: domingo de manhã, 4h30).

---

## 3. O que faltou no seu plano

1. **Questões anteriores como eixo central** (já dito; é a lacuna mais importante).
2. **Delta de atualização 2019 → 2026.** Lista inicial (não exaustiva, a validar contra o edital) do que mudou desde a última vez que ela estudou:
   - Pacote Anticrime (Lei 13.964/2019): acordo de não persecução penal, juiz das garantias (e o julgamento do STF de 2023 sobre ele), cadeia de custódia, mudanças na execução penal e nas cautelares.
   - Nova Lei de Abuso de Autoridade (Lei 13.869/2019).
   - Nova Lei de Licitações (Lei 14.133/2021).
   - Reforma da Lei de Improbidade (Lei 14.230/2021).
   - LGPD em vigor e proteção de dados como direito fundamental (EC 115/2022).
   - Lei Henry Borel (Lei 14.344/2022) e demais alterações no ECA e na proteção de crianças.
   - Feminicídio como crime autônomo (Lei 14.994/2024) e alterações na Lei Maria da Penha.
   - Reforma tributária (EC 132/2023), se Tributário estiver no edital.
   - Jurisprudência estrutural do período: ADPF 347 (estado de coisas inconstitucional do sistema prisional), ADPF 635, teses sobre saúde e fornecimento de medicamentos, população em situação de rua, entre outras.
   - Alterações na legislação institucional (LC 80/94, lei orgânica estadual) e deliberações do Conselho Superior da DPE-SP.

   Essa lista foi feita de memória por um modelo de linguagem: serve como pauta de verificação, **não como conteúdo**. Aplica-se a ela a mesma regra do resto.
3. **Ela participa do desenho?** Tudo aqui parte do que você imagina que ela precisa. Ela pediu isso? Já tem cursinho, material, método próprio? Um app que compete com a rotina que ela já montou atrapalha. 30 minutos de conversa com ela valem mais que qualquer seção deste documento.
4. **Preparação para o formato:** resistência para 4h30, gestão de tempo (~3 min por questão), estratégia de chute (5 alternativas; conferir se há penalidade por erro). Nudge não treina isso; simulado treina.
5. **Vida útil após a objetiva.** Se ela passar, as dissertativas são em julho/2027. Conteúdo bem estruturado é reaproveitável, mas o formato muda (escrita, peças). Não construir para isso agora; apenas não fechar portas no modelo de dados.

---

## 4. Notificações no iPhone: análise específica

**Como funciona:** Web Push no iOS existe desde o iOS 16.4, **somente** para sites adicionados à Tela de Início **pelo Safari** (Compartilhar → Adicionar à Tela de Início). A permissão só pode ser pedida a partir de um toque do usuário dentro do app instalado. Aba aberta no navegador não recebe nada.

**Pontos fracos reais:**

- **Instalação é manual e nada óbvia.** Precisa de uma tela de onboarding com passo a passo, ou de você fazer isso com ela pessoalmente.
- **Entrega não é garantida.** Há relatos recorrentes de notificações que param após reinício do aparelho ou de assinaturas que expiram silenciosamente. O servidor precisa tratar erro de envio (assinatura inválida → marcar e pedir reativação na próxima abertura).
- **Modos de Foco / Não Perturbe** do iOS silenciam tudo, e durante o estudo é exatamente o que ela deveria ligar.
- **Sem garantia de execução em segundo plano.** O conteúdo do nudge tem que estar pronto no servidor; o push só carrega título + link.
- **Agendamento:** o cron do plano gratuito da Vercel é limitado (historicamente, execuções diárias). Para vários disparos por dia, usar `pg_cron` do Supabase chamando uma Edge Function. Confirmar limites atuais antes de implementar.

**Comparação de canais:**

| Canal | Confiabilidade | Esforço de dev | Fricção para ela | Observação |
|---|---|---|---|---|
| Web Push (PWA) | média | médio | média (instalar via Safari) | abre direto no card; melhor experiência quando funciona |
| E-mail | alta | baixo | nenhuma | bom para resumo diário; ruim para micro-interação; pode ir para "Promoções" |
| Telegram bot | alta | baixo | baixa, se ela já usa | tem enquete tipo quiz nativa; responde sem sair do chat |
| WhatsApp (API oficial) | alta | alto | nenhuma | exige conta Business, aprovação de templates, custo por mensagem; inviável no prazo |
| Evento no calendário | alta | muito baixo | nenhuma | serve para blocos de estudo e simulados, não para cards |

**Recomendação:** não escolher um só. **Push para os nudges + e-mail diário matinal** com o plano do dia, as revisões pendentes e links diretos. O e-mail funciona como rede de segurança: se o push morrer, ela ainda recebe o essencial e você percebe pela queda de aberturas. Se ela usa Telegram, um bot é o canal mais confiável e mais barato de todos e merece ser considerado como canal principal. Blocos de estudo e simulados vão para o calendário dela (arquivo .ics).

Sua intuição de que só push "pode ser fraco" está correta, mas a solução por e-mail tem um limite: e-mail é bom para **um** envio diário. Três e-mails por dia viram spam na percepção dela em menos de uma semana.

---

## 5. Chat de aprofundamento: construir ou não?

Você menciona "aprofundar na conversa via chat do app". É o componente mais caro e mais arriscado de todos:

- Chat ao vivo é exatamente onde a alucinação acontece sem chance de revisão prévia.
- Fazer bem feito (busca no corpus, citação obrigatória, recusa quando não há fonte) custa, sozinho, mais do que todo o resto do MVP.
- Já existem produtos que fazem isso: um Projeto no Claude ou um caderno no NotebookLM, carregado com o edital e as leis do corpus, responde com base nos documentos e mostra de onde tirou.

**Recomendação:** v1 sem chat próprio. Cada card tem um botão "aprofundar" que abre a fonte oficial e, opcionalmente, um link para o Projeto/caderno externo já carregado com o corpus. Chat próprio com busca no corpus só entra se o MVP estiver estável antes do dia 20 e ela pedir.

---

## 6. Cenários

### Cenário A: sem código (ferramentas prontas)

Anki (flashcards com repetição espaçada, tem app iOS com notificação nativa) + plataforma de questões filtrada por FCC/Defensoria + planilha de acompanhamento por tema do edital + Projeto no Claude ou NotebookLM com edital e leis + eventos no calendário.

- **Vantagens:** pronto em 1 dia; ferramentas maduras; zero risco de bug na reta final; notificação nativa confiável; ela começa a estudar amanhã.
- **Desvantagens:** cinco ferramentas desconectadas; nada é específico para o edital; o delta 2019→2026 não existe pronto; acompanhamento manual; apps pagos (Anki iOS e plataforma de questões têm custo).
- **Quando escolher:** se você tem menos de ~10h livres nesta semana, ou se ela já tem método próprio e só precisa de estrutura.

### Cenário B: MVP enxuto sob medida

PWA com: árvore de temas do edital, plano com três faixas de prioridade, painel de acompanhamento, sessão de revisão (cards + questões reais), nudges por push, e-mail diário. Conteúdo gerado em lote e validado. Sem chat.

- **Vantagens:** tudo num lugar; específico para o edital; delta de atualização embutido; acompanhamento automático; você enxerga o progresso dela (se ela quiser).
- **Desvantagens:** 5 a 8 dias até ficar usável, com ela sem ferramenta nesse intervalo; o gargalo real é o **conteúdo**, não o código; risco de bug em produção perto da prova; push no iOS pode falhar.
- **Quando escolher:** nunca sozinho. Só faz sentido combinado com A (ver D).

### Cenário C: produto completo

B + chat com busca no corpus + plano adaptativo automático + simulados cronometrados dentro do app + estatísticas detalhadas.

- **Vantagens:** é o app que você imaginou.
- **Desvantagens:** 3 a 5 semanas; fica pronto quando metade da janela já passou; maior superfície de alucinação; você passa dezembro corrigindo bug em vez de alimentar conteúdo.
- **Avaliação:** não recomendado para este concurso. Faz sentido como evolução se ela passar para a segunda fase ou se você quiser transformar isso em produto.

### Cenário D: híbrido (recomendado)

- **Dia 1 (amanhã):** conversa de 30 min com ela; edital baixado; ela faz a prova diagnóstica no fim de semana; planilha simples de temas + Projeto/caderno externo com o corpus para ela não ficar parada.
- **Dias 2 a 8:** construir B em fatias utilizáveis (ordem na seção 8). A planilha é aposentada quando o painel do app a substitui.
- **Dia 9 em diante:** congelar funcionalidades. Seu tempo vai para conteúdo (mais temas, mais questões, correção do que ela reportar).
- **Últimos 10 dias:** congelamento total de código. Só correção crítica.

- **Vantagens:** ela não espera por você; o app nasce validado pelo uso real; se o app atrasar ou falhar, o plano A segue funcionando.
- **Desvantagens:** pequena duplicação de esforço na primeira semana; exige disciplina sua para congelar o escopo.

### Variante B': bot de Telegram no lugar da PWA

Mesma lógica e mesmo banco, mas a interface de nudge é um bot. Painel de acompanhamento continua sendo uma página web simples.

- **Vantagens:** entrega confiável; sem instalação via Safari; quiz nativo; metade do código de front-end.
- **Desvantagens:** só serve se ela já usa Telegram; notificação compete com outras conversas; formatação limitada para trechos longos de lei.

---

## 7. Arquitetura proposta (cenário B/D)

**Stack**

- **Next.js na Vercel**: PWA (manifest + service worker), páginas de painel, sessão de revisão e plano.
- **Supabase**: Postgres, Auth por link mágico (um usuário, ou dois se você quiser acompanhar), `pg_cron` para agendar, Edge Functions para disparar push e e-mail.
- **Web Push** com chaves VAPID; assinaturas guardadas no banco.
- **E-mail transacional** (Resend ou similar, plano gratuito basta).
- **API de LLM usada apenas no pipeline offline de conteúdo**, rodando da sua máquina ou em script do repositório. Nenhuma chamada de LLM em tempo de execução na v1.

**Pipeline de conteúdo (o coração do projeto)**

```
edital.pdf ──► árvore de temas (revisada à mão) ──► temas.yaml
fontes oficiais ──► corpus/ (texto + URL + data de captura)
provas FCC anteriores ──► questoes/ (enunciado, alternativas, gabarito, ano)

para cada tema:
  selecionar trechos do corpus ──► gerar cards (com citação literal obrigatória)
  ──► validar: citação é substring da fonte? URL responde? ──► descartar reprovados
  ──► arquivo no git (diff revisável) ──► carga no banco
```

**Modelo de dados mínimo**

- `disciplinas`, `temas` (árvore do edital, com prioridade e flag "mudou desde 2019")
- `fontes` (documento oficial, URL, data de captura) e `trechos`
- `itens` (card ou questão; tipo; selo de confiança; tema; trecho-fonte)
- `revisoes` (histórico de respostas, base do espaçamento)
- `plano_dias` (o que está previsto para cada data) e `progresso_temas`
- `nudges` (agendados, enviados, abertos, respondidos)
- `push_subscriptions`, `reportes_erro`

**Custos esperados:** planos gratuitos de Vercel e Supabase bastam para um usuário. O gasto real é a API de LLM no pipeline de conteúdo (ordem de dezenas de dólares, dependendo do volume) e, no cenário A/D, as ferramentas pagas.

**Privacidade:** dados de estudo de uma pessoa só; RLS ativo no Supabase; nada sensível. Combinar com ela se você terá acesso ao painel de progresso: ser observada pode motivar ou constranger.

---

## 8. Ordem de construção (se cenário D)

Cada fatia entrega algo que ela usa, e a ordem é a de maior valor por dia:

1. **Árvore de temas + plano + painel** (substitui a planilha). Sem conteúdo ainda: ela marca manualmente o que estudou e registra acertos.
2. **Sessão de revisão com questões reais da FCC** de uma disciplina piloto. Valida o pipeline de ponta a ponta.
3. **E-mail diário** (plano do dia + pendências). Canal confiável funcionando antes do canal frágil.
4. **PWA + push** com nudges de revisão.
5. **Cards do delta 2019→2026**, disciplina por disciplina, na ordem de prioridade do diagnóstico.
6. **Replanejamento automático** quando há atraso.
7. (Só se sobrar tempo e ela pedir) chat com busca no corpus.

O gargalo previsível é o item 5 em diante: produzir e validar conteúdo para 11 disciplinas é mais trabalho que todo o código. Planeje cobrir bem 4 ou 5 disciplinas prioritárias em vez de cobrir mal as 11.

---

## 9. Quadro de riscos

| # | Risco | Prob. | Impacto | Mitigação |
|---|---|---|---|---|
| 1 | Ela não está inscrita | ? | total | confirmar hoje |
| 2 | App fica pronto tarde demais | alta | alto | cenário D; fatias; congelamento no dia 9 |
| 3 | Conteúdo com erro jurídico | alta sem processo | muito alto | corpus fechado, citação validada, selo, botão de reporte |
| 4 | Conhecimento antigo dela aplicado com confiança | alta | alto | delta 2019→2026 como prioridade de conteúdo |
| 5 | Nudges substituem estudo de verdade | média | alto | nudge só revisa; plano com blocos de estudo e simulados |
| 6 | Push no iOS falha silenciosamente | média | médio | e-mail diário redundante; detecção de assinatura morta |
| 7 | Fadiga de notificação | alta | médio | padrão baixo, controle dela, redução automática |
| 8 | Ela não queria/precisava disso | desconhecida | alto | conversar antes de codificar |
| 9 | Plano irreal para as horas que ela tem | alta | alto | orçamento de horas explícito; três faixas; cortes por escrito |
| 10 | Gabarito de questão antiga superado | média | médio | data na questão; alerta em temas com flag de mudança |
| 11 | Você vira gargalo de conteúdo | alta | médio | priorizar 4-5 disciplinas; questões reais exigem menos curadoria |
| 12 | Bug na semana da prova | média | alto | congelamento de código nos últimos 10 dias |
| 13 | Uso de material protegido | baixa se seguir o plano | médio | só fontes oficiais; doutrina por referência |
| 14 | Festas de fim de ano quebram o ritmo | alta | médio | folgas já previstas no plano, não descobertas depois |

---

## 10. Decisões que você precisa tomar antes de codificarmos

**Bloqueantes (sem isso não começo):**

1. **Ela está inscrita?** (sim/não)
2. **Ela sabe do projeto e topa participar?** Preciso de respostas dela para: horas de estudo por dia e em quais horários; se já tem cursinho/material/método; se usa Telegram; versão do iOS; se aceita que você veja o progresso.
3. **Cenário:** A, B, D ou B'? Minha recomendação é **D**. Se você tem menos de ~10h livres nos próximos 7 dias, a resposta honesta é **A**.
4. **Quanto tempo você tem** por semana até 10/01? Define o tamanho do MVP.

**De produto:**

5. **Canal de nudge:** push + e-mail (recomendado), Telegram, ou só e-mail?
6. **Chat próprio na v1?** Recomendo **não**; link para Projeto/caderno externo.
7. **Ela faz a prova diagnóstica antes?** Recomendo **sim**, neste fim de semana. Sem isso, a priorização é chute.
8. **Quem define "imprescindível"?** Opções: incidência histórica nas provas (dado), diagnóstico (dado), opinião dela (experiência), ou combinação. Recomendo combinação com a palavra final dela.
9. **Disciplinas piloto:** quais 1 ou 2 entram primeiro no pipeline de conteúdo? Sugestão: as de pior desempenho no diagnóstico entre as de maior incidência.

**Técnicas:**

10. **Stack confirmada?** Next.js + Vercel + Supabase + Resend, LLM apenas offline.
11. **Orçamento** para API de LLM e para ferramentas pagas do cenário A.
12. **Onde ficam as provas e leis baixadas:** no próprio repositório (simples, versionado; o repositório deve ser privado) ou em storage separado?
13. **Idioma do código e da interface:** interface em português; código e commits em português ou inglês?

**Primeiro passo concreto após as decisões:** obter o PDF do edital no site da FCC, extrair a lista de disciplinas e o conteúdo programático para `temas.yaml` e reconferir todos os números da seção 1.

---

## Fontes consultadas

Dados do concurso (portais, não oficiais; reconferir no edital):

- [Estratégia Carreira Jurídica: edital DPE-SP Defensor publicado](https://cj.estrategia.com/portal/concurso-dpe-sp-defensor-edital-publicado-2026/)
- [Estratégia Carreira Jurídica: concurso DPE-SP Defensor](https://cj.estrategia.com/portal/concurso-dpe-sp-defensor/)
- [Gran Cursos: edital DPE-SP Defensor](https://blog.grancursosonline.com.br/concurso-dpe-sp-defensor-edital-publicado-2026/)
- [QConcursos: PDF do edital do X Concurso](https://arquivos.qconcursos.com/regulamento/arquivo/102414/dpe-sp-2026-x-concurso-defensor-publico-edital.pdf)
- [Escola Até Aprovação: concurso DPE-SP 2026](https://escolaateaprovacao.com.br/blog/concurso-dpe-sp-2026)
- [Magistrar: cronograma e encerramento das inscrições](https://magistrarcursos.com.br/blog/concurso-dpe-sp-defensor-inscricoes-encerram-em-breve-veja-o-cronograma/)

Web Push no iOS (blogs de fornecedores; conferir nas notas de versão do WebKit):

- [MagicBell: PWA iOS limitations and Safari support](https://www.magicbell.com/blog/pwa-ios-limitations-safari-support-complete-guide)
- [Pushpad: iOS special requirements for web push](https://pushpad.xyz/blog/ios-special-requirements-for-web-push-notifications)
- [Webscraft: PWA push notifications on iOS in 2026](https://webscraft.org/blog/pwa-pushspovischennya-na-ios-u-2026-scho-realno-pratsyuye?lang=en)
