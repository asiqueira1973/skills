---
name: app-store-connect
description: Gera o pacote completo de conteúdo pronto para colar no App Store Connect (nome, subtítulo, texto promocional, descrição, keywords, notas de versão, notas do App Review, resposta de App Encryption Documentation, Content Rights, Age Rating, categoria, preço/IAP e a seção de Política de Privacidade específica do app) a partir de uma spec de produto (formato SDD, normalmente spec.md) compartilhada na conversa. Reaproveita os ativos fixos do desenvolvedor — Support URL, documento de Política de Privacidade compartilhado, contato, prefixo de bundle ID — registrados em references/meus-ativos.md, em vez de inventar um processo novo a cada app. Use este skill sempre que o usuário pedir para "preencher a App Store", "montar a ficha da loja", "gerar as notas de revisão", "escrever a política de privacidade do app", "preparar o app pra publicar/submeter", ou compartilhar um spec.md pedindo ajuda com App Store Connect — mesmo que ele não use essas palavras exatas ou não cite o skill pelo nome.
---

# App Store Connect

Este skill transforma uma spec de produto (o documento que descreve o app — normalmente gerado pelo skill `sdd-spec`) no pacote de textos e decisões que o usuário precisa colar no App Store Connect na hora de publicar. Ele existe porque esse trabalho tem uma parte de copywriting (nome, descrição, keywords) e uma parte de decisões repetitivas de processo (sign-in required, encryption compliance, content rights, política de privacidade) que seguem o mesmo padrão em todo app do mesmo desenvolvedor — vale gerar tudo de uma vez, de forma consistente, em vez de reinventar a cada publicação.

## Antes de começar: leia a spec inteira

Não gere nenhum campo sem antes ler o spec.md inteiro que o usuário compartilhou (ou pediu para você ler). Cada campo depende de informação real do produto — nome, proposta de valor, features, se tem login, se tem IAP, o que o app faz com dados do usuário. Gerar a partir de suposições em vez do spec é o erro mais comum aqui: o objetivo é que o texto saia pronto pra colar, não pronto pra reescrever.

Preste atenção especial a estas seções do spec (os números variam conforme o spec, mas o conteúdo costuma estar lá):
- Visão do produto / proposta de valor (normalmente seção 1) — para nome, subtítulo, texto promocional e o parágrafo de abertura da descrição.
- Escopo do MVP / épicos (normalmente seções 3 e 8) — para a lista de features da descrição e das notas do App Review.
- Autenticação e identidade (se existir) — define se o app tem login/conta de verdade, o que muda a resposta de "Sign-in Required" e se o app precisa de Termos de Uso, opção de excluir conta, trocar senha e logout.
- Privacidade, segurança e conformidade (normalmente seção 20) — a fonte de verdade de tudo que vai na seção de Política de Privacidade e na resposta do questionário de App Privacy.
- Arquitetura (normalmente seção 4) — para saber se o app usa Firebase, backend próprio, criptografia customizada, ou só frameworks padrão da Apple (isso decide a resposta de App Encryption Documentation).
- Requisitos não-funcionais / idiomas — para localização do conteúdo.

Se a spec não cobrir algum desses pontos com clareza suficiente para decidir um campo, **pergunte ao usuário em vez de inventar** — é exatamente o tipo de detalhe que gera app rejeitado.

## Os ativos fixos do desenvolvedor

Leia `references/meus-ativos.md` antes de escrever qualquer campo — ele tem as informações que se repetem em todo app (Support URL, contato, prefixo de bundle ID, como está estruturado o documento de Política de Privacidade compartilhado, etc.) e que **não devem ser reinventadas a cada skill run**. Reaproveitar esses ativos é o que torna esse processo mais rápido do que preencher a App Store do zero.

Se algum campo desse arquivo ainda estiver com placeholder (`[PREENCHER: ...]`), pergunte o valor ao usuário e sugira que ele atualize o arquivo para as próximas vezes. Nunca invente e-mail, URL ou razão social.

## O pacote de saída

Gere um único arquivo markdown (`app-store-connect-<nome-do-app>.md`) com as seções abaixo, nesta ordem. Use o `references/output-template.md` como estrutura de referência se precisar relembrar o formato exato — mas o conteúdo de cada seção vem da spec, nunca do template.

### 1. App Information
Nome (≤30 car.), subtítulo (≤30 car.), categoria primária/secundária (inferida do domínio do produto na spec — ver exemplos em `references/meus-ativos.md`), copyright.

### 2. Version Information
Texto promocional (≤170 car.), descrição (≤4.000 car., em prosa/parágrafos curtos com alguns blocos de destaque em MAIÚSCULAS + bullets, num tom direto — nunca em markdown com `#`/`**`, porque o campo da App Store não renderiza isso), keywords (≤100 **bytes**, não caracteres — cuidado com acentuação em português, que consome mais de 1 byte por caractere), notas da versão.

**Sempre rode `scripts/check_limits.py`** contra os textos gerados antes de entregar — não estime o tamanho de cabeça, meça. Veja o cabeçalho do script para o formato de input esperado.

Ao escrever as keywords, não repita palavras que já estão no Nome ou no Subtítulo — elas já contam para a indexação de busca da Apple, então repeti-las ali desperdiça bytes preciosos sem ganho nenhum.

### 3. App Privacy (questionário)
Baseado na seção de privacidade da spec: se o app não tem backend próprio e não coleta dado nenhum além do que fica em iCloud/CloudKit privado do usuário, a resposta é **"Data Not Collected"**. Se o app tem backend, contas, analytics (Firebase/Crashlytics) ou qualquer coleta real, diga exatamente quais categorias de dado marcar — use a tabela de mapeamento em `references/meus-ativos.md` para traduzir o que a spec descreve (e-mail, dado de saúde, localização, analytics, crash logs, ads...) para a categoria oficial da Apple, em vez de só dizer "tem coleta". Se a spec descrever monetização por anúncios, leia também a seção de ads/ATT desse mesmo arquivo — é uma combinação que costuma exigir atenção extra (e, se houver dado de categoria sensível como saúde, um alerta explícito no documento final, não só o preenchimento mecânico).

### 4. URLs obrigatórias
- **Support URL:** por padrão, reaproveitar a página de suporte registrada em `references/meus-ativos.md` — só sugerir uma página nova se o usuário pedir algo específico do app.
- **Privacy Policy URL:** por padrão, é o link do documento de política compartilhado (`references/meus-ativos.md`) — mas **gere sempre uma seção nova, específica do app**, para adicionar dentro desse documento (nunca reaproveite cegamente o texto genérico de outro app). Antes de escrever essa seção, confira contra a seção de privacidade/arquitetura da spec **quais afirmações genéricas do documento NÃO se aplicam a este app** (ex.: se o texto genérico menciona Firebase Authentication, Crashlytics/Analytics, permissões de Câmera/Galeria/Notificações — só inclua essas afirmações se a spec confirmar que o app realmente usa essas coisas; se não usar, a seção nova deve dizer isso explicitamente, para não contradizer a resposta "Data Not Collected" da seção anterior). Use uma numeração de seções consistente com o documento (ex.: 1. Coleta de Dados, 2. Uso dos Dados, 3. Armazenamento e Segurança, 4. Compartilhamento com Terceiros, 5. Contato).

### 5. Pricing and Availability
Preço da ficha (Grátis/Tier 0 se a monetização for via IAP, ou o tier correspondente se for pago fixo — ver seção de monetização da spec), disponibilidade (`All Countries or Regions` por padrão), e o produto de In-App Purchase se a spec descrever um (identificador, nome de exibição, descrição, tipo — consumível/não-consumível/assinatura conforme a spec).

### 6. App Review Information
- **Sign-in Required:** marcar **Sim** só se a spec descrever login/conta de verdade; senão, deixar desmarcado. Apps com login precisam de credencial de teste (usuário/senha) ou de uma opção de acesso sem conta (guest) — se a spec não deixar claro qual das duas, pergunte ao usuário antes de escrever as notas. Se a spec confirma que precisa de credencial de teste mas você não tem uma conta de teste de verdade para oferecer, **não invente um e-mail/senha fictício como se fosse real** — deixe um placeholder claramente marcado (ex.: `[PREENCHER: e-mail/senha de uma conta de teste real antes de submeter]`) e liste isso no resumo final como pendência.
- **Notes:** citar proativamente, logo no início, os pontos que mais causam rejeição (ver checklist em `references/meus-ativos.md`): página de Política de Privacidade e Termos de Uso acessíveis de dentro do app (se tiver conta), opção de excluir conta, trocar senha e logout (se tiver conta), mensagens de permissão para qualquer uso de câmera/galeria/microfone/calendário/localização/bluetooth, e — se o app tiver algum mecanismo de trial/paywall — explicar exatamente como testar o fluxo completo (o revisor da Apple precisa saber como passar do trial para o estado "comprado" sem pagar de verdade). Fechar sempre com "Support website" e o contato de e-mail. Se o app tiver conta e exigir Termos de Uso, veja a seção "Termos de Uso" em `references/meus-ativos.md` antes de assumir que já existe um pronto — se não houver um ativo registrado, é uma pendência a sinalizar, não um link a inventar.

### 7. App Encryption Documentation
Resposta padrão: **"None of the algorithms mentioned above"** — vale para qualquer app que só faça chamadas HTTPS via frameworks padrão da Apple (`URLSession`, `CloudKit`, `StoreKit`, Firebase via SDK oficial) sem implementar nenhuma criptografia própria. **Só desvie dessa resposta se a spec descrever criptografia customizada/proprietária de verdade** (ex.: um esquema de criptografia ponta-a-ponta implementado pelo próprio app) — nesse caso, pare e avise o usuário, porque a resposta certa pode exigir documentação adicional de compliance de exportação dos EUA, e não é uma decisão para tomar sozinho.

### 8. Content Rights
Resposta padrão: **"No, it does not contain, show, or access third-party content"** — vale para a maioria dos apps utilitários, mesmo quando o app busca/exibe conteúdo que o próprio usuário pediu (essa pergunta da Apple é sobre conteúdo de terceiros embutido/licenciado dentro do app — fontes, imagens, trilhas — não sobre um app "visualizador" mostrar o que o usuário escolheu abrir, mesma lógica de um navegador). Só marque "Yes" se a spec descrever conteúdo licenciado de terceiros embutido no produto (ex.: banco de imagens, base de dados de terceiros redistribuída). Em caso de dúvida real, sinalize a ambiguidade para o usuário em vez de decidir sozinho — não é uma resposta 100% mecânica.

### 9. Classificação etária (Age Rating)
Dê uma **expectativa**, não a resposta oficial (só o questionário de verdade da Apple gera a classificação real): baseado na spec, diga se há conteúdo gerado por usuário visível a terceiros, rede social, chat, IA generativa livre, conteúdo adulto/violento/apostas, e estime a faixa mais provável (a maioria dos apps utilitários sem nada disso cai em **4+**).

## Depois de gerar

1. Rode `scripts/check_limits.py` nos textos finais e inclua o resultado (OK/estouro) no próprio documento entregue — é isso que evita re-trabalho na hora de colar no formulário.
2. Entregue o markdown como arquivo (não só no corpo da mensagem) para o usuário poder abrir lado a lado com o App Store Connect.
3. Resuma em texto curto, fora do arquivo: quais decisões você tomou sozinho seguindo os padrões default (Content Rights, Encryption, Sign-in) e quais precisam de confirmação do usuário antes de submeter — não deixe isso escondido dentro do documento longo.
