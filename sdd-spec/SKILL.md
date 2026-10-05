---
name: sdd-spec
description: "Cria ou atualiza uma especificação de software no formato SDD (Spec-Driven Development) — um spec.md completo pronto para servir de input direto para o Claude Code. Use sempre que o usuário pedir para \"criar uma spec\", \"escrever a especificação\", \"fazer o SDD\", \"documentar o escopo de um app/produto/feature\", quando enviar PDFs/notas de escopo pedindo para transformar em especificação, ou quando pedir para atualizar/alterar um spec existente (mudar arquitetura, mover algo para a próxima release, adicionar épico, especificar uma feature nova sobre um app já implementado). Também use quando o usuário disser que vai \"pedir pro Code construir\" e precisar do documento, do prompt de implementação e dos guardrails do Claude Code (hooks, subagente verificador, REVIEW.md)."
---

﻿# SDD — Especificação de Software Orientada a Spec

Gera um `spec.md` que é a **fonte única de verdade** de um produto ou feature, no nível de detalhe necessário para um agente de código implementar sem inventar decisões.

Princípio central: **o spec decide, o código obedece.** Toda ambiguidade que sobrar no documento vira decisão arbitrária do agente de código depois — e decisão arbitrária de agente é retrabalho. Se você não sabe algo, registre como assunção declarada ou pergunta aberta em vez de escrever uma frase vaga que parece resolvida.

Segundo princípio: **regra escrita é consultiva, regra executável é garantida.** O spec e o `CLAUDE.md` tornam a violação rara; um hook a torna quase impossível. Toda regra que não pode falhar nunca (credencial privilegiada fora do frontend, migration versionada intocável, teste que não se enfraquece durante correção) sai do spec também como guardrail executável — seção 18.1 e Anexo B.

Idioma do documento: escreva o spec no idioma em que o usuário está falando (normalmente pt-BR).

---

## Convenções padrão (valem sempre, salvo pedido explícito em contrário)

Estas três decisões já estão tomadas. Escreva-as no spec como regra, não como sugestão, a menos que o usuário peça diferente:

1. **Banco de dados em português.** Nomes de tabelas, colunas, enums, funções, triggers e políticas em **português**, em `snake_case` (`metas_atribuidas`, `classificacao_final`, `departamento_id`). Só use inglês no banco se o usuário pedir explicitamente ou se o projeto for extensão de um banco existente que já está em inglês — e nesse caso declare o motivo no spec. Código, variáveis e nomes de arquivo seguem o padrão de mercado em inglês; a fronteira de idioma fica na camada de acesso a dados.

2. **Código comentado explicando o que cada rotina faz.** Toda função, hook, rotina de servidor, trigger e política leva um comentário de cabeçalho dizendo em linguagem clara o que ela faz, o que recebe, o que devolve e — quando houver — qual regra de negócio do spec ela implementa (com o número da seção). Trechos com lógica não óbvia (cálculo, condição composta, transformação, workaround) levam comentário inline. O objetivo é prático: o código precisa continuar editável por prompt meses depois, por alguém — ou algum agente — que não participou da implementação.

3. **Documentação técnica final em português.** A entrega inclui, obrigatoriamente, um documento de documentação técnica gerado ao fim da implementação (ver "Documento de documentação técnica" abaixo). Ele entra no Definition of Done: sem esse documento, a feature não está pronta.

---

## Padrão de navegação — menu lateral estilo App Store Connect [padrão, sobreponível]

Layout **default** para painéis administrativos e back-office web com **navegação lateral persistente**. É **sobreponível**: se a seção 16 (Direção visual) do produto definir outra navegação/estética, ou o usuário pedir outra coisa, ela vence. **Não** aplique este padrão em app consumer/mobile **sem menu lateral** — ali quem manda é a seção 16 (ou a proposta livre de direção visual).

Quando valer, descreva-o **explícito** na seção 16 do spec e no `prompt-design-<produto>.md`, em palavras (sem depender de código):

- **Grupos:** título em **negrito escuro**, caixa normal — nunca MAIÚSCULAS decorativas.
- **Itens:** **indentados** sob o grupo, **sem marcador/bolinha**.
- **Separação:** **traço fino (hairline)** entre os grupos.
- **Estado ativo:** **um item ativo por vez**, marcado na **cor de destaque/primária do produto** (texto na cor de destaque + leve pílula clara da mesma cor ao fundo). Se o produto não define cor primária, use azul.
- **Rodapé:** usuário + sair; quando fizer sentido, um selo de ambiente (dev/prod) discreto.
- **Forma:** cantos arredondados suaves, **hairlines** em vez de bordas pesadas, espaçamento generoso.

Cores e tipografia vêm da direção visual do produto (seção 16) — este padrão define a **estrutura** da navegação, não a paleta.

---

## Fase 1 — Coletar antes de escrever

Nunca comece a escrever o spec sem entender o produto. Nesta ordem:

1. **Leia todo material que o usuário forneceu** — PDFs de escopo, notas, prints, referências visuais, links, código existente. Se houver mais de uma fonte, procure ativamente por **inconsistências entre elas** (nomes diferentes para a mesma coisa, números que não batem, regras contraditórias). Toda inconsistência encontrada deve ser resolvida e a resolução declarada ao usuário no final.
2. **Pergunte se existe projeto de referência.** Se o usuário já tem outro sistema com stack, convenções e infraestrutura que ele quer reaproveitar, isso decide metade da arquitetura de graça — e deve ficar escrito no spec ("mesmo padrão do projeto X, para reaproveitar conhecimento").
3. **Pesquise o que for factual e datado** — versões de framework, disponibilidade de SDK, limites de plataforma, preço de API, requisitos de loja, o que a API de um serviço permite de verdade. Use WebSearch. Não escreva do conhecimento prévio nada que possa ter mudado; arquitetura escrita a partir de premissa desatualizada é o erro mais caro do documento.
4. **Pergunte via AskUserQuestion apenas o que muda o desenho** e você não pode inferir do material. Bons candidatos: plataforma-alvo, o que fica dentro e fora do MVP, quem é o usuário, quantos perfis de acesso existem, se existe backend, quem paga. Máximo 3–4 perguntas; não pergunte o que já está nos documentos.
5. Crie a lista de tarefas (TaskCreate) antes de escrever.

Se o material já responde tudo, não pergunte — escreva.

---

## Fase 2 — Estrutura do documento

Comece com um **cabeçalho de metadados**: versão do documento, autor/responsável de produto, status (`rascunho` / `pronto para revisão` / `aprovado para implementação`) e data. Specs vivem meses e recebem várias rodadas — sem versão você perde o rastro de qual foi colado no agente de código.

Depois, uma seção **"Como usar este documento"**: para que serve, que agente vai consumir, e o aviso de que a seção de assunções deve ser revisada **antes** de gerar código, porque assunção não revisada vira verdade no momento em que o agente começa a implementar.

Numere as seções e mantenha a numeração estável: o prompt de implementação e todas as conversas futuras vão referenciar "seção 8.2", "regra 11.1". Renumerar depois quebra referências.

Seções marcadas **[obrigatória]** entram sempre. As **[opcional]** entram só quando fazem sentido para o projeto — mas justifique para si mesmo antes de cortar; a maioria dos specs ruins é ruim por omissão, não por excesso.

### 0. Princípios não-negociáveis [obrigatória]
De 3 a 5 princípios, cada um com nome curto e uma frase de explicação. São as regras de desempate: quando o agente de código tiver dúvida de UX, copy ou trade-off, resolve a favor destes. Princípio bom é falsificável — exclui alternativas reais. "Ser fácil de usar" não é princípio; "nenhuma tela pede mais de um toque para registrar o dia" é. "Simplicidade antes de complexidade prematura" é um princípio útil e recorrente: ele justifica sozinho várias decisões de modelagem.

### 1. Visão e problema [obrigatória]
O que é o produto em um parágrafo, para quem, e qual dor resolve. Inclua o **anti-escopo**: o que este produto explicitamente não é (evita scope creep silencioso).

### 2. Personas e cenários de uso [opcional]
Quem usa, em que contexto físico e emocional. Vale quando o contexto de uso muda o desenho (uso na rua, uso sob estresse, uso por profissional treinado). Descreva o momento mais difícil de uso — geralmente é ele que define a arquitetura.

### 3. Escopo do MVP [obrigatória]
Duas listas explícitas: **dentro** e **fora**. Cada item do "fora" ganha destino e motivo: descartado (com o porquê) ou adiado para v2 (com o que precisa acontecer antes). Nada fica em limbo. Item adiado por dependência externa — acesso a um console, e-mail individual por pessoa, contrato com fornecedor — deve dizer qual é a dependência.

### 4. Arquitetura [obrigatória]
Stack com versões, decisões de infraestrutura, o que roda onde, dependências externas com nome e propósito, onde o código vive (repositório) e onde roda (deploy). Se houver projeto de referência, declare-o.

Para cada decisão relevante, uma linha de **por quê** e uma de **alternativa descartada** — é isso que impede a decisão de ser silenciosamente revertida três semanas depois. Marque explicitamente o que é premissa a validar.

### 5. Perfis de usuário e matriz de permissões [obrigatória quando há mais de um perfil]
Liste os perfis e monte uma **tabela ação × perfil**, com o escopo em cada célula — não basta ✅/❌, o que importa é "✅ só no próprio departamento" vs "✅ em qualquer". Uma linha por ação sensível: criar conta, editar cadastro, excluir, editar dados de outros, exportar, ver.

Esta tabela é a parte do spec que mais evita bug de segurança, porque ela força você a responder as perguntas chatas antes: quem cria conta de quem, quem promove alguém a administrador, quem consegue apagar dado de outro, quem vê o quê. Inclua também **como nasce o primeiro administrador** (seed inicial) — sistema sem isso não sobe.

Se houver escopo de dados por organização/departamento/tenant, diga qual campo define o escopo e o que acontece com usuários que não têm esse campo preenchido.

### 6. Autenticação e identidade [obrigatória quando há login]
Não trate como detalhe de implementação: é onde mais aparece restrição do mundo real que quebra a solução óbvia.

- Como a pessoa se identifica (e-mail, login, telefone, SSO) e **por quê** — se o padrão óbvio não serve, explique a restrição (ex.: pessoas compartilham e-mail de área, então o identificador é um login e o sistema traduz para um identificador interno).
- Como a conta é criada: autocadastro, convite ou criação por administrador. Se for criação por administrador, especifique quem pode, o que é gerado (senha temporária?), como é entregue, e que a operação precisa de rota de servidor com credencial privilegiada — **nunca chave de serviço no frontend**.
- Primeiro acesso e troca de senha obrigatória.
- **Recuperação de senha** — inclusive a decisão de não existir fluxo automático, e qual é o caminho oficial nesse caso. Esquecer isso gera suporte manual eterno.
- Sessão, expiração, logout.
- Autorização no banco: políticas por tabela (RLS ou equivalente), uma linha por tabela dizendo o que cada perfil pode ler e escrever, com o **nome** previsto de cada política. Permissão só no frontend não é permissão.

### 7. Modelo de dados [obrigatória]
Tabelas/entidades com campos, tipos, nullability, defaults, chaves e relações — em português, `snake_case`. Enums com todos os valores possíveis. Inclua:

- **Diagrama de relacionamento**, mesmo que em texto/ASCII — cabe em 5 linhas e evita erro de cardinalidade.
- **Constraints e índices** sugeridos: unique, checks, formato esperado de campos livres (ex.: `^[a-z0-9._-]+$` para login).
- **Estratégia de exclusão**: soft delete ou hard delete, por entidade. Se há histórico referenciando a linha, soft delete é quase sempre a resposta — mas escreva a decisão, não deixe implícita.
- **Lógica que vive no banco**: quais regras serão implementadas como trigger, função ou política, com nome previsto e o que cada uma faz. Regra escondida em trigger sem nome documentado é a coisa mais difícil de descobrir num sistema meses depois.
- **Dados de seed** e como migrations são versionadas e aplicadas.
- Nullability contada como decisão de negócio: para cada campo nullable, uma frase dizendo em que caso ele é nulo.
- Se você escolheu uma modelagem desnormalizada por simplicidade (ex.: doze colunas de mês em vez de tabela de status mensal), **declare o trade-off** e o que ela impede no futuro.

Este é o pedaço do spec que o agente de código copia mais literalmente — vale gastar tempo aqui. É também a seção-fonte do arquivo `.dbml` gerado na Fase 3: mantenha nomes, tipos, nullability e relacionamentos exatamente como escritos aqui, sem sinônimo — o `.dbml` é gerado por leitura literal desta seção, não por reinterpretação.

### 8. Épicos e critérios de aceite [obrigatória]
Um subitem por épico (8.1, 8.2, …), na ordem de implementação. Cada épico traz:

- objetivo em uma frase;
- fluxo do usuário, passo a passo, incluindo estados vazio, carregando e de erro;
- **critérios de aceite verificáveis**, em lista, cada um redigido para dar resposta binária. "Ao tocar em X, o contador na Home incrementa em 1 e a animação Y toca uma vez" — não "a experiência é fluida".

### 9. Fluxos principais ponta a ponta [opcional]
Quando o produto tem processos que atravessam vários perfis e telas (onboarding de usuário, aprovação, fechamento de período), descreva-os como numeração linear, separados dos épicos. O épico organiza a implementação; o fluxo garante que ela funciona junta. Inclua sempre o **caminho da exceção**: a pessoa que nunca vai usar o sistema, o registro sem conta, o mês sem dado.

### 10. Inventário de telas [opcional]
Uma lista de todas as telas com o perfil que a acessa no rótulo (`[Admin] Departamentos`, `[Funcionário] Minhas metas`), o que cada uma mostra, os filtros disponíveis, quais ações são de leitura vs escrita e **quais tabelas ela lê e escreve**. Vale para qualquer app com mais de 4 telas: é o que garante que nenhum perfil ficou sem caminho para o que ele precisa fazer, e é a matéria-prima da documentação técnica final.

### 11. Regras de negócio [obrigatória]
Toda lógica numérica ou condicional em **tabela**, nunca em prosa: pontuação, níveis, limites, cálculos, condições de desbloqueio, fusos e viradas de dia, cardinalidades ("um departamento tem no máximo um diretor ativo"). Diga o que acontece nos casos de borda (empate, valor zero, retroativo, mudança de fuso). Diga também o que **não** é automático — "a classificação final é preenchida à mão, sem cálculo derivado dos meses" evita que o agente invente uma fórmula. Para cada regra, diga **onde ela é aplicada**: frontend, servidor ou banco (trigger/função/política).

O agente de código não deve precisar inferir nenhum número.

### 12. Máquinas de estado e tratamento de erro [opcional]
Para qualquer entidade com ciclo de vida (pedido, sessão, assinatura, upload): estados, transições permitidas e proibidas, e o que acontece em cada falha. Vale sempre que existir "status" no modelo de dados.

### 13. Contratos de API e tipos [opcional]
Endpoints, métodos, payloads de entrada e saída, códigos de erro, autenticação, idempotência, paginação. Inclua as **rotas de servidor** exigidas pela seção 6 (as que usam credencial privilegiada), com a validação que cada uma faz antes de agir. Se for local-first sem backend, substitua por contratos dos módulos internos. Obrigatória se houver integração com terceiros.

### 14. Relatórios, exportação e importação [opcional]
Se o produto exporta ou importa arquivo, especifique com precisão de implementação: **colunas exatas e na ordem**, granularidade da linha, padrão do nome do arquivo, encoding (para CSV que abre no Excel: UTF-8 **com BOM**), separador, formato de data e número, e o que acontece com o filtro aplicado na tela. Exportação é a feature que mais volta em retrabalho por causa de detalhe não escrito.

### 15. Copy e tom de voz [opcional]
Frases oficiais do produto — títulos, mensagens de sucesso e erro, notificações, textos de estado vazio. Deixe explícito que é conteúdo final, não placeholder. Vale sempre que o texto for parte da experiência (produto de conteúdo, saúde, educação, tudo voltado a consumidor).

### 16. Direção visual / design system [opcional]
Paleta, tipografia, espaçamento, referências visuais (nomeie os produtos de referência), componentes-chave, densidade de tabela vs card, modo escuro. Separe explicitamente **cor semântica** (status, alerta, erro) de **cor de marca**, e reserve a semântica só para significado — se a cor primária compete com a de status, a grade fica ilegível.

Se houver brand ou design system da empresa, aponte para ele em vez de redefinir; se você decidiu **não** aplicar a marca (produto interno, por exemplo), registre isso como decisão para não parecer esquecimento.

Para **painéis e back-office com menu lateral**, o default de navegação é o **menu lateral estilo App Store Connect** (bloco no início deste skill): descreva-o aqui, com as cores e a tipografia da direção visual do produto — salvo se o produto pedir outra navegação (aí a sua vence). App consumer/mobile sem navegação lateral não usa este padrão.

Marque também o que é livre para o agente escolher — deixar isso explícito é melhor que o agente parar para perguntar ou inventar em silêncio.

### 17. Requisitos não-funcionais [obrigatória]
Performance (alvos numéricos: tempo de abertura, tempo de resposta), comportamento offline, acessibilidade (tamanho de fonte, contraste, leitor de tela, área mínima de toque), consumo de bateria e dados, tamanho do binário, compatibilidade mínima de dispositivo/navegador, volume esperado de dados e usuários, idiomas.

### 18. Convenções de código, documentação e estrutura do repositório [obrigatória quando o spec alimenta um agente de código]
O que faz o código continuar editável por prompt seis meses depois. Escreva estes itens como regra explícita no spec:

- **Idioma — banco em português, código em inglês.** Tabelas, colunas, enums, funções, triggers e políticas em português, `snake_case`. Código, variáveis, funções e nomes de arquivo em inglês. A fronteira de idioma fica na camada de acesso a dados: os tipos que espelham o banco mantêm os nomes em português. Exceção só se o usuário pedir, ou se o projeto estende um banco já em inglês — e aí registre o motivo.
- **Comentários obrigatórios.** Toda função, hook, rotina de servidor, trigger e política tem comentário de cabeçalho em português explicando o que faz, o que recebe, o que devolve e qual regra do spec implementa (com número da seção). Lógica não óbvia leva comentário inline. Comentário descreve intenção e regra de negócio, não repete a sintaxe — `// incrementa i` é ruído; `// desconsidera meses sem status para não puxar a média pra baixo (regra 11.4)` é o que se procura depois.
- **Organização de pastas**: módulo por feature, com componentes, hooks de dados e tipos juntos. Liste as pastas esperadas.
- **Documentação viva**: um arquivo de schema na raiz gerado a partir do banco real, para o spec e o código não divergirem; README com setup local, variáveis de ambiente e como rodar migrations. E o **documento de documentação técnica** descrito abaixo, atualizado a cada mudança relevante.
- **`CLAUDE.md` na raiz** — o guia que o agente de código (Claude Code) lê automaticamente a cada sessão: convenções, mapa da arquitetura, comandos (typecheck!), as pegadinhas que **não podem ser quebradas** e a regra de manter os docs em dia. É o guardião da manutenção por outros devs/agentes. Mantenha `CLAUDE.md`, a documentação técnica e o README atualizados **no mesmo commit** da mudança. Duas regras de manutenção, escritas no próprio arquivo: **cabe em uma página** (ele é lido inteiro a cada sessão; o que está velho só ocupa contexto — detalhe vai para o spec ou para a documentação técnica), e **quando o agente errar a mesma coisa duas vezes, a correção entra no `CLAUDE.md`** na seção "Pegadinhas". A seção "Comandos" lista cada comando de verificação (seção 22.1) com um exemplo de saída saudável.
- **Variáveis de ambiente**: quais existem, quais são públicas e quais são secretas. Deixe espaço reservado para as que entram nas próximas releases.

### 18.1 Guardrails executáveis [obrigatória quando o spec vai virar código]
Tabela **regra → mecanismo**, uma linha por regra inegociável do spec, com a seção de origem. Três mecanismos, do mais fraco ao mais forte:

| Mecanismo | Natureza | Use para |
|---|---|---|
| `CLAUDE.md` / texto do spec | consultivo — o agente segue quase sempre | convenções, estilo, preferências |
| `REVIEW.md` + subagente `verifier` | verificação depois do fato, em contexto limpo | critérios de aceite, matriz de permissões, conformidade com spec e plano |
| Hook (`.claude/settings.json`) | determinístico — bloqueia a ação antes de acontecer | o que não pode falhar nunca |

Regras mínimas que viram hook em todo projeto com banco: credencial privilegiada nunca em código de frontend (seção 20); migration já versionada não se edita, cria-se outra (seção 7); em tarefa de correção de bug, arquivo de teste não se edita (seção 22.1); em projeto Supabase, lembrete de rodar os advisors a cada migration escrita. Acrescente as regras específicas do produto que também não podem falhar. Cada hook bloqueia **explicando o motivo e o caminho certo**, é rápido e age só no arquivo que mudou — checagens pesadas (suíte inteira de testes) ficam no commit/PR, não no hook.

O conteúdo dos arquivos vai no **Anexo B** do spec. Gere-o a partir de `references/guardrails-templates.md` (leia antes de escrever esta seção), adaptando caminhos de pastas e comandos ao stack da seção 4 — nunca copie um template sem ajustar os caminhos.

### 19. Documento de documentação técnica (entregável ao fim da implementação) [obrigatória quando o spec alimenta um agente de código]
Especifique no spec que, **depois de implementar**, o agente de código deve gerar um documento em português — `DOCUMENTACAO-TECNICA.md` na raiz — descrevendo o sistema como ele ficou de fato, não como foi planejado. É o documento que permite retomar o projeto (ou trocar de agente) sem reengenharia reversa. Conteúdo mínimo, nesta ordem:

1. **Modelo de dados explicado em português** — cada tabela: para que serve, o que cada coluna significa em linguagem de negócio (não só o tipo), quais valores os enums aceitam e o que cada valor quer dizer.
2. **Relacionamento entre as tabelas** — diagrama em texto e, para cada relação, uma frase explicando a cardinalidade no vocabulário do negócio ("um departamento tem muitos funcionários; um funcionário pertence a exatamente um departamento").
3. **Regras de negócio que vivem no banco** — lista de todas as triggers, funções e políticas (RLS) criadas, com **nome exato**, tabela onde atuam, quando disparam e o que fazem em português. Deve dar para ler essa lista e entender toda a lógica que o frontend não vê.
4. **Mapa tela → tabelas** — para cada tela da aplicação, quais tabelas ela lê, quais escreve, e por quais políticas/funções ela passa. Este mapa é o que evita que uma alteração de schema quebre uma tela sem ninguém perceber.
5. **Lógica das principais funcionalidades por tela** — para cada tela, o que acontece em cada ação principal: o que é validado, o que é gravado, o que é calculado e onde (frontend, servidor ou banco), e o que o usuário vê em caso de erro.
6. **Divergências em relação ao spec** — o que foi implementado diferente do especificado e por quê. Sem esta seção o documento envelhece mentindo.

Regra de manutenção: toda mudança em schema, trigger, política ou lógica de tela atualiza este documento no mesmo commit.

### 20. Privacidade, segurança e conformidade [obrigatória]
Que dados são coletados e por quê, onde ficam, quem acessa, quanto tempo são retidos, como o usuário exporta e apaga. Dados sensíveis (saúde, financeiro, menores, biometria) exigem tratamento explícito e citação da base legal — LGPD/GDPR conforme o público. Onde ficam segredos e chaves, e a regra de que credencial privilegiada só existe no servidor. Se o backend for **Supabase**, rode os **advisors (`get_advisors` — segurança e performance) regularmente, sobretudo após DDL** (pegam RLS faltando, `SECURITY DEFINER` exposto, `search_path` mutável, FK sem índice); em outros backends, use o linter/scanner equivalente. Prático, não acadêmico — priorize risco real.

Se o produto embute IA, defina os **guardrails** e o que acontece quando o modelo falha: qual detecção não depende do modelo, qual resposta fixa sobrepõe a resposta gerada, e em que situações. Guardrail que depende do próprio modelo julgar não é guardrail.

### 21. Métricas de sucesso e telemetria [opcional]
Como se sabe que funcionou: 2–4 métricas de produto com alvo e prazo. Se houver analytics, liste os eventos com nome e propriedades. Respeite a seção 20 — evento que carrega dado sensível é vazamento com outro nome.

### 22. Estratégia de teste [opcional; 22.1 obrigatória quando o spec vai virar código]
O que precisa de teste automatizado (as regras da seção 11 quase sempre precisam, e as políticas de permissão das seções 5/6 sempre), o que é validado manualmente, casos de borda a cobrir, e como se testa fluxo dependente de tempo, de rede ou de perfil de acesso.

#### 22.1 Loop de verificação
O agente de código precisa conseguir provar sozinho que o trabalho funciona antes de um humano olhar. Especifique:

- **Comandos únicos** de verificação — teste, build, typecheck/lint — cada um um comando só, que termina com erro quando falha (`npm test`, `npm run build`, `xcodebuild test …`, conforme o stack). Se verificar hoje exige uma sequência de passos, especifique o script que a encapsula.
- **Evidência obrigatória**: nenhum épico é declarado pronto sem rodar os três comandos e colar a saída. "Testei e funciona" sem saída não conta.
- **Critério quantificável por épico**, derivado dos critérios de aceite da seção 8 (ex.: "todos os testes de `regras_pontuacao` passam", "screenshot confere com a tela aprovada no Claude Design").
- **Bug se corrige com teste primeiro**: reproduzir o bug como teste, rodar e confirmar que falha pelo motivo esperado, commitar o teste; só então corrigir o código **sem editar o teste** (garantido pelo hook de proteção de testes da seção 18.1).
- **UI**: quando houver ferramenta de navegador ou screenshot disponível ao agente, fechar o loop visual — implementar, capturar, comparar com o design aprovado, ajustar.
- **Regra de ouro**, escrita literalmente no `CLAUDE.md`: se um teste falhar, corrija o código, não o teste; nunca pule nem apague teste que falha.

### 23. Riscos e mitigação [obrigatória]
Tabela: risco, impacto, probabilidade, mitigação. Inclua risco técnico, de produto e de dependência externa. Seja específico o suficiente para agir — "risco de performance" não é risco, "inferência local em aparelho de entrada pode passar de 5s e quebrar o alvo de 17.1" é.

### 24. Assunções declaradas [obrigatória]
Distinta das perguntas abertas: aqui vão as decisões que **você tomou sem perguntar**, por serem de baixo impacto ou por não valer uma rodada de conversa. Uma linha por assunção, com o que você escolheu, o porquê, e a alternativa caso o usuário discorde ("se você quiser exclusão definitiva, é só avisar que eu ajusto").

Esta seção é o que torna o spec confiável em vez de presunçoso. Escreva no cabeçalho o aviso: **assunção não revisada vira verdade no minuto em que o agente começa a codar.**

### 25. Perguntas abertas [obrigatória]
O que ficou sem decisão porque só o usuário pode decidir, quem decide e até quando. Instrua explicitamente que o agente de código deve **perguntar em vez de assumir** quando cruzar com um item desta seção. Spec com esta seção vazia normalmente está escondendo decisão não tomada.

### 26. Definition of Done [obrigatória]
Checklist final de release — funcional, não-funcional, permissões, privacidade, testes, publicação. Inclua sempre, como itens verificáveis:

- banco em português conforme a convenção, sem tabela ou coluna fora do padrão;
- todas as rotinas, triggers e políticas comentadas;
- `DOCUMENTACAO-TECNICA.md` gerado e conferido contra o sistema implementado;
- `CLAUDE.md` criado/atualizado (convenções, arquitetura, comandos, pegadinhas) e README em dia;
- (se Supabase) advisors de segurança + performance rodados após DDL, sem alerta crítico pendente;
- guardrails do Anexo B instalados em `.claude/` e **cada hook testado uma vez** (provocar a violação e ver o bloqueio);
- `plans/` com o plano aprovado de cada épico ou feature, consistente com o código entregue (ou divergência registrada no próprio plano);
- saída dos comandos de verificação (seção 22.1) colada no fechamento de cada épico, e relatório do subagente `verifier` sem critério "não cumprido".

Cada item verificável. É o que se usa para dizer "acabou" sem discussão.

### 27. Próximos passos operacionais [opcional]
O que acontece fora do código: revisão da seção de assunções pelo usuário, ordem de execução (ex.: gerar o schema do banco primeiro, depois o app), criação do repositório, conexão com o deploy, quem publica. Curto, numerado, acionável.

### 28. Roadmap: próximas releases [opcional]
Tudo que saiu do MVP mas já foi especificado. **Preserve o detalhe original** — não resuma trabalho já feito. Quando o usuário pedir para tirar algo do MVP, mova para cá em vez de apagar; a próxima release começa com spec pronta.

### 29. Protocolo de mudanças incrementais [obrigatória quando o spec vai virar código]
Instruções para o usuário depois do v1 pronto — evita que um ajuste pequeno vire reescrita do app:

1. Commit de checkpoint antes de qualquer mudança, para ter um `git diff` confiável.
2. Não colar o spec inteiro de novo: colar só o trecho novo ou alterado, ou um spec adicional específico da feature.
3. Escrever a instrução como diff, não como recomeço — deixar explícito que o projeto já existe e funciona.
4. Delimitar nominalmente o que **não** deve mudar.
5. Pedir o plano em plan mode — arquivos que serão criados/alterados, ordem e testes que provam a mudança — **antes** do código, aprovar e commitar como `plans/<feature>.md`. Se for bug, o plano começa pelo teste que reproduz a falha (seção 22.1).
6. Revisar o `git diff` contra o `plans/<feature>.md`; reverter arquivo que passou do escopo e refazer o pedido mais específico. Se a implementação precisou divergir do plano, o plano é atualizado no mesmo commit.
7. Exigir a atualização do `DOCUMENTACAO-TECNICA.md` no mesmo commit da mudança.

Inclua um modelo de prompt curto pronto para colar.

### Anexo — Fontes [obrigatória quando houve pesquisa]
Links de tudo que foi pesquisado, com data de consulta.

### Anexo B — Kit de guardrails do Claude Code [obrigatória quando o spec vai virar código]
Conteúdo literal, em blocos de código com o caminho de cada arquivo no título, dos arquivos que o épico 0 cria: `.claude/settings.json`, cada script em `.claude/hooks/`, `.claude/agents/verifier.md` e `REVIEW.md`. Tudo derivado das seções 5, 7, 8, 11, 18.1, 20 e 22.1 — nenhum hook nem item de revisão que não corresponda a uma regra escrita no spec. Partir dos modelos em `references/guardrails-templates.md`.

---

## Fase 3 — Entrega

1. Salve como `spec.md` (ou `SDD-<produto>.md`) na pasta de saída e apresente com `present_files`.
2. **Sempre que a seção 7 (Modelo de dados) existir no spec** — em spec novo ou em atualização — gere também um arquivo `.dbml` com o modelo de dados dessa seção, pronto para colar direto no dbdiagram.io. Salve como `modelo-<produto>.dbml` na mesma pasta do `spec.md` e entregue junto com os demais arquivos (mesmo `present_files`/mesma leva de entrega, não à parte).

   Regras do `.dbml`:
   - Reflita **exatamente** o que está na seção 7 — tabelas, colunas, tipos, nullability, defaults, chaves primárias e estrangeiras, relacionamentos. Não invente nada que não esteja explícito no spec; se um tipo, default ou constraint não estiver claro na seção 7, resolva com o que você mesmo escreveu lá, nunca com um palpite novo.
   - Nomes de tabela e coluna em **português**, `snake_case`, idênticos aos da seção 7 — mesma convenção de idioma do banco, sem tradução nem sinônimo.
   - Modele os **enums** da seção 7 como `enum` do DBML, com os valores exatos e na mesma ordem.
   - Modele toda chave estrangeira com `Ref`, respeitando a **cardinalidade** descrita no spec: `>` um-para-muitos, `<` muitos-para-um, `-` um-para-um, `<>` muitos-para-muitos.
   - Marque `pk`, `not null` (quando o campo não é nullable), `default` e `unique` conforme a seção 7. Campo nullable fica sem `not null`, refletindo a decisão de negócio já registrada na seção 7 — não a repita nem a contradiga.
   - Sintaxe de referência:
     ```dbml
     Table nome_tabela {
       id uuid [pk, default: `gen_random_uuid()`]
       campo_obrigatorio texto [not null]
       campo_opcional texto
       status status_pedido [not null, default: 'pendente']
       outra_tabela_id uuid [not null]

       Note: 'descrição curta da tabela, se a seção 7 tiver uma'
     }

     enum status_pedido {
       pendente
       aprovado
       cancelado
     }

     Ref: nome_tabela.outra_tabela_id > outra_tabela.id
     ```
   - Constraint, índice ou estratégia de exclusão (soft/hard delete) que a seção 7 descreve mas que não tem campo estrutural equivalente no DBML entra como comentário `//` acima da tabela ou coluna — não fica de fora do arquivo por limitação de sintaxe.
   - Ao atualizar um spec existente: se a mudança alterar a seção 7 (nova tabela, campo, enum, relação ou constraint), atualize o `.dbml` **no mesmo passo**, sem que o usuário precise pedir separadamente — é parte da mesma entrega.
3. **Sempre que a seção 10 (Inventário de telas) existir no spec** — em spec novo ou em atualização — gere também um `prompt-design-<produto>.md`: um prompt pronto para colar no Claude Design, para criar todas as telas do app seguindo a especificação gerada. Salve na mesma pasta do `spec.md` e entregue junto com os demais arquivos (mesma leva de entrega, não à parte).

   Regras do prompt de design:
   - Liste **todas** as telas da seção 10, agrupadas por perfil de acesso (mesmo agrupamento do inventário), com o que cada uma mostra e as ações principais. Não invente tela que não esteja na seção 10.
   - Para cada tela, inclua os **estados** (vazio, carregando, erro) descritos no épico correspondente (seção 8), quando existirem.
   - Resuma a **matriz de permissões** (seção 5) por tela, para que cada estado de UI reflita o que aquele perfil pode e não pode fazer — o que aparece habilitado, desabilitado ou oculto conforme o perfil.
   - Quando a seção 9 (Fluxos principais) existir, inclua o fluxo principal entre telas, para o design respeitar a sequência e não desenhar telas soltas.
   - Quando a seção 16 (Direção visual) existir, referencie-a literalmente — paleta, tipografia, referências visuais, densidade, modo escuro. Se a seção 16 **não** existir no spec, o prompt deve pedir explicitamente ao Claude Design para propor uma direção visual coerente com o produto, e declarar isso no próprio prompt (para não parecer esquecimento — mesma lógica da seção 16 do spec).
   - **Menu lateral estilo App Store Connect (painéis/back-office):** salvo direção própria na seção 16, o prompt de design deve descrever **explicitamente** o padrão de menu lateral (bloco no início deste skill) — grupos em negrito escuro, itens indentados sem bolinha, hairline entre grupos, item ativo na cor de destaque — usando as cores e a tipografia da direção visual do produto. Vale **mesmo quando a seção 16 não existir** (nesse caso substitui o "peça ao Claude Design para propor"). **Exceção:** app consumer/mobile **sem** navegação lateral mantém a regra anterior (seção 16, ou proposta livre).
   - Quando a seção 15 (Copy e tom de voz) existir, use a copy literal dela. Quando não existir, use placeholder de texto claramente marcado como tal (ex.: `[placeholder: título da tela]`) — nunca invente copy final.
   - Ao atualizar um spec existente: se a mudança alterar o inventário de telas (seção 10) ou a direção visual (seção 16), atualize o `prompt-design-<produto>.md` **no mesmo passo**, sem que o usuário precise pedir separadamente — inclusive quando o app já está implementado e a mudança virou um spec adicional de feature (nesse caso, atualize ou gere o trecho correspondente do prompt de design junto com o spec adicional).
4. Escreva o **prompt de implementação** para o usuário colar no Claude Code, em bloco de código, contendo:
   - caminho do documento;
   - instrução de montar plano e lista de tarefas **antes de codar** (em plan mode) e mostrar para aprovação; o plano aprovado é **salvo e commitado** em `plans/<épico-ou-feature>.md` (arquivos que mudam, ordem, riscos, testes que provam) e atualizado no mesmo commit sempre que a implementação divergir dele;
   - **épico 0 — guardrails**: antes de qualquer feature, criar os arquivos do Anexo B (`.claude/settings.json`, `.claude/hooks/`, `.claude/agents/verifier.md`, `REVIEW.md`), tornar os scripts executáveis e testar cada hook provocando a violação uma vez;
   - ordem de implementação por número de seção — em projeto com banco, schema e políticas de permissão primeiro, telas depois;
   - escopo explícito, com o que **não** implementar (as seções de roadmap, nominalmente);
   - os princípios da seção 0 como regra de desempate;
   - **a convenção de idioma**: tabelas, colunas, enums, funções, triggers e políticas em português (`snake_case`); código e variáveis em inglês;
   - **a exigência de comentar todas as rotinas** em português, explicando o que cada uma faz e qual regra do spec implementa;
   - instrução de seguir literalmente as tabelas de permissões e de regras de negócio, sem inventar valores;
   - instrução de validar cada épico contra seus critérios de aceite antes de seguir: rodar os comandos de verificação da seção 22.1 e **colar a saída**, depois acionar o subagente `verifier` e só avançar com todos os critérios "cumprido";
   - regra de teste: se um teste falhar, corrigir o código, não o teste; bug se corrige com teste que falha primeiro;
   - ao fim de cada épico, revisar o próprio diff contra o `REVIEW.md` e o `plans/` correspondente;
   - instrução de perguntar em vez de assumir diante de qualquer item das perguntas abertas;
   - **ao final, gerar o `DOCUMENTACAO-TECNICA.md`** com os seis itens da seção 19, escrito a partir do que foi realmente implementado.
5. No resumo em chat (curto), destaque: inconsistências que você resolveu e como, as assunções que mais precisam de revisão, premissas técnicas a validar, e os 1–2 pontos que mais merecem o olhar do usuário — e confirme que o `.dbml` foi entregue junto (ou diga por que não, se a seção 7 não existir no spec) e que o `prompt-design-<produto>.md` foi entregue junto (ou diga por que não, se a seção 10 não existir no spec), e liste em uma linha quais regras viraram hook no Anexo B. Não recapitule o documento — ele pode ler.

---

## Atualizando um spec existente

Quando o usuário pedir alteração:

- Leia o documento inteiro antes de editar. Mudança de arquitetura raramente é local: ela reverbera em modelo de dados, autenticação, permissões, critérios de aceite, riscos, não-funcionais e DoD. **Propague até o fim** ou o spec fica internamente contraditório — e spec contraditório é pior que spec incompleto, porque o agente de código segue a metade errada com confiança.
- Se a mudança elimina um risco, remova o risco. Se cria riscos novos, adicione-os.
- Ao tirar escopo do MVP, mova para a seção de roadmap com todo o detalhe intacto.
- Mantenha a numeração das seções estável; se precisar inserir, use subitens.
- Incremente a versão no cabeçalho.
- Se o app já está implementado, prefira um **spec adicional só da feature** em vez de reescrever o documento principal — e entregue junto o prompt incremental do protocolo da seção 29, incluindo a atualização da documentação técnica.
- **Se a mudança tocar a seção 7 (Modelo de dados)**, regenere/atualize também o `modelo-<produto>.dbml` no mesmo passo — tabela nova, campo novo, enum alterado, relação nova ou removida, mudança de tipo ou de nullability entram no `.dbml` junto com o spec, sem o usuário precisar pedir separadamente. Se o spec adicional for só de feature (app já implementado) e ele também alterar a seção 7, entregue o `.dbml` atualizado junto com o spec adicional.
- **Se a mudança tocar a seção 10 (Inventário de telas) ou a seção 16 (Direção visual)**, regenere/atualize também o `prompt-design-<produto>.md` no mesmo passo — tela nova, tela removida, mudança de ações/estados/permissões por tela, ou nova direção visual entram no prompt junto com o spec, sem o usuário precisar pedir separadamente. Isso vale mesmo quando o app já está implementado e a mudança virou um spec adicional de feature: entregue o prompt de design atualizado (ou o trecho novo correspondente) junto com o spec adicional.
- **Se a mudança criar, alterar ou remover uma regra inegociável** (permissão, credencial, regra de banco, convenção que não pode falhar), atualize a tabela da seção 18.1 e o Anexo B no mesmo passo. Em spec adicional de feature, entregue só os arquivos de guardrail novos ou alterados.
- Ao final, liste em chat o que mudou por seção (e, se aplicável, que o `.dbml` e/ou o `prompt-design-<produto>.md` foram atualizados).

## Erros a evitar

- Tabela ou coluna em inglês sem o usuário ter pedido — o padrão é português.
- Código sem comentário de intenção, ou comentário que só repete a sintaxe.
- Terminar a implementação sem gerar a documentação técnica em português.
- Prosa onde cabia tabela. Número em frase corrida é número que vai ser ignorado.
- Critério de aceite subjetivo ("intuitivo", "rápido", "agradável").
- Matriz de permissões com ✅/❌ sem o escopo ("✅ **só no próprio departamento**" é a informação que importa).
- Deixar autenticação, recuperação de senha e criação do primeiro administrador como "detalhe de implementação".
- Regra de negócio implementada em trigger sem nome nem descrição documentada.
- Decisão de arquitetura ou de modelagem sem o "por quê" e sem o trade-off — vira reversão silenciosa depois.
- Confundir assunção (você decidiu, revise) com pergunta aberta (ninguém decidiu, precisa decidir). São duas seções.
- Especificar exportação sem colunas, ordem, encoding e nome de arquivo.
- Resumir trabalho já especificado ao movê-lo para o roadmap.
- Escrever premissa técnica datada sem verificar.
- Entregar o spec sem o `.dbml` quando a seção 7 existe, ou deixar o `.dbml` desatualizado depois de uma mudança na seção 7.
- Inventar tipo, default, constraint ou cardinalidade no `.dbml` que não está escrito na seção 7 — o `.dbml` só pode conter o que o spec já diz.
- Entregar o spec sem o `prompt-design-<produto>.md` quando a seção 10 existe, ou deixar o prompt de design desatualizado depois de uma mudança na seção 10 ou 16.
- Inventar tela ou copy no prompt de design que não está no spec — toda tela vem literalmente da seção 10, toda copy final vem da seção 15; sem seção 15, a copy entra como placeholder marcado, nunca como texto final inventado.
- Deixar regra que não pode falhar só como texto — credencial privilegiada, migration versionada e proteção de teste precisam de hook (seção 18.1).
- Hook genérico copiado do template sem ajustar os caminhos de pastas do stack real — hook que não casa com o caminho não bloqueia nada e dá falsa segurança.
- Prompt de implementação que aceita "épico pronto" sem saída de comando colada, ou plano aprovado que não é salvo em `plans/`.
- `CLAUDE.md` que cresce sem limite — passou de uma página, o detalhe vai para o spec ou para a documentação técnica.
- Gerar o prompt de design de um **painel/back-office com menu lateral** sem descrever o padrão de menu lateral (estilo App Store Connect) quando ele se aplica — ou, no oposto, **forçá-lo** num app sem navegação lateral.

