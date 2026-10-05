# Meus ativos fixos

Estas informações se repetem em (quase) todo app do mesmo desenvolvedor. **Preencha os campos marcados com `[PREENCHER: ...]` uma vez** e o skill passa a reaproveitá-los em vez de gerar algo novo a cada app. Se um campo continuar com placeholder, o skill pergunta o valor em vez de inventar.

## Contato e identidade

- **Responsável:** [PREENCHER: seu nome]
- **E-mail de contato / suporte:** [PREENCHER: e-mail de suporte]
- **Empresa / razão social:** [PREENCHER: nome da empresa, ou "pessoa física"]
- **Copyright padrão da ficha:** `© <ano atual> [PREENCHER: nome que aparece no copyright]` (ajustar o ano; confirmar se algum app específico deve usar outra razão social)
- **Conta de desenvolvedor Apple:** reaproveitada entre os apps — não é preciso criar nova a cada app; só o App ID (Identifiers) e o registro do app no App Store Connect são por produto.
- **Prefixo de bundle ID:** [PREENCHER: ex. `com.suaempresa.<nomeapp>`] — confira o Bundle ID no Xcode do app em questão; o padrão costuma ser `com.<empresa>.<nome em minúsculo, sem espaço>`.

## Support URL

**Reaproveitar por padrão:** [PREENCHER: URL da página de suporte]

Uma página genérica de suporte serve para todos os apps. Texto sugerido:
> Em caso de dúvidas, dificuldades com o app ou pedidos de exclusão de conta, entre em contato: [e-mail de suporte]. Responderemos em até 48 horas úteis.

**Não use Notion (nem Coda e similares) como Support URL** — é motivo conhecido de rejeição: a Apple exige uma página real publicada, não um link de workspace, para esse campo especificamente. Um construtor de página simples (Carrd, GitHub Pages, o próprio site) resolve. Se algum app precisar de uma página de suporte própria (ex.: um FAQ mais elaborado), crie uma nova na mesma ferramenta.

## Privacy Policy URL

**Reaproveitar por padrão:** [PREENCHER: URL pública do documento de Política de Privacidade compartilhado entre os apps]

Ao contrário do Support URL, uma página pública do Notion **costuma ser aceita** para este campo, desde que seja o link de compartilhamento público do documento.

Estrutura do documento: [PREENCHER: liste as seções do seu documento, ex.: 1. Sobre a empresa / 2. Finalidade dos aplicativos / 3. Dados coletados / 4. Como usamos os dados / 5. Contato]. Se o texto atual estiver disponível na conversa, releia-o em vez de confiar nesta lista.

**Importante:** um texto de política compartilhado costuma ser escrito pensando no perfil típico dos apps de quem o escreveu (ex.: Firebase + contas + câmera/galeria/notificações). Ele **não é verdade automaticamente para todo app novo** — qualquer app que não use aquilo que o texto genérico menciona precisa de uma seção própria deixando isso explícito, senão o documento passa a afirmar uma coleta de dados que não existe (o que também contradiz uma resposta "Data Not Collected" no questionário de App Privacy — duas fontes dizendo coisas diferentes sobre o mesmo app é motivo de atrito na revisão).

Ao gerar a seção nova para um app, siga uma numeração consistente (1. Coleta de Dados / 2. Uso dos Dados / 3. Armazenamento e Segurança / 4. Compartilhamento com Terceiros / 5. Contato), mas escreva o conteúdo de cada uma a partir da spec real daquele app — nunca copie o texto de outro app sem verificar se bate.

## Categorias já usadas (para inferir a categoria de um app novo por analogia)

| App | Categoria primária | Perfil |
|---|---|---|
| [PREENCHER: app já publicado] | [categoria] | [o que o app faz] |

Use isso como referência de "que tipo de categoria a Apple aceitou para um produto parecido", não como regra fixa — a categoria certa depende sempre do produto descrito na spec. Para domínios não cobertos aqui, use o mapeamento genérico abaixo como fallback (e adicione a linha nesta tabela depois que um app novo publicar, para o próximo uso já ter o precedente):

| Domínio do produto | Categoria primária provável |
|---|---|
| Saúde, hidratação, sono, bem-estar físico | Health & Fitness |
| Finanças pessoais, investimentos, orçamento | Finance |
| Estudo, flashcards, idiomas | Education |
| Gestão de clínica/consultório, agenda profissional | Business ou Medical (depende se o usuário-alvo é o profissional ou o paciente) |
| Leitor/visualizador de arquivo, ferramenta do dia a dia | Utilities |
| Organização de tarefas, notas, hábitos | Productivity |
| Câmera, edição de foto/vídeo, catálogo fotográfico | Photo & Video |

## Mapeamento spec → categorias do questionário "App Privacy" da Apple

Quando o app **tem** coleta de dados real (diferente do caso "Data Not Collected"), a Apple pede para marcar cada tipo de dado numa lista fechada de categorias — não é texto livre. Use esta tabela para traduzir o que a spec descreve para a categoria oficial mais próxima:

| O que a spec descreve | Categoria da Apple |
|---|---|
| E-mail, nome, telefone de cadastro/login | Contact Info |
| Peso, sono, exercício, consumo de água/calorias, dado de condição física | Health & Fitness |
| Saldo, transação, gasto, investimento | Financial Info |
| Foto/vídeo enviado pelo usuário | User Content → Photos or Videos |
| Texto livre, anotação, mensagem digitada pelo usuário | User Content → Other User Content |
| Localização precisa/aproximada | Location |
| Token de push notification, identificador de instalação | Identifiers → Device ID (ou User ID, se vinculado à conta) |
| Dado de uso de tela/feature (Firebase Analytics, Mixpanel, etc.) | Usage Data |
| Log de erro/crash (Crashlytics, Sentry) | Diagnostics → Crash Data / Performance Data |
| Dado usado para anúncio direcionado (rede de ads, ID de publicidade) | Identifiers → Device ID, **e** marcar "Used for Third-Party Advertising" |

**Atenção a combinações de risco:** a Apple restringe o uso de dado de categoria **Health & Fitness** (e outras categorias sensíveis) para fins de publicidade — se a spec tiver *ao mesmo tempo* dado de saúde/sono/hidratação/etc. **e** monetização por anúncios, isso merece uma nota explícita de atenção no documento final, não só o preenchimento mecânico da tabela — o SDK de ads usado importa (alguns já vêm com salvaguardas, outros não), então sinalize a pendência em vez de assumir que está tudo certo.

## Monetização por anúncios (ads)

Além do padrão "grátis + IAP" e "pago fixo", alguns apps monetizam por anúncios (rede de ads embutida via SDK, ex.: AdMob). Quando a spec descrever isso:
- Isso quase sempre implica coleta de **Identifiers** para publicidade (ver tabela acima) e possivelmente **App Tracking Transparency (ATT)** — se o SDK de ads rastrear entre apps/sites de terceiros, o app precisa do prompt de permissão ATT do iOS antes de rastrear.
- Se a spec não citar qual SDK de anúncios será usado, **não assuma** que não precisa de ATT nem qual categoria de dado marcar — sinalize como pendência para o usuário confirmar, junto com o nome do SDK escolhido.

## Termos de Uso

**Documento compartilhado de Termos de Uso:** [PREENCHER: URL, ou "não existe"]

Se não existir um documento de Termos de Uso registrado aqui, para um app que tenha conta/cadastro (onde os Termos de Uso costumam ser esperados além da Política de Privacidade — ver checklist abaixo), não invente uma URL nem assuma que o "Apple's Standard License Agreement" padrão é suficiente sem confirmar com o usuário — sinalize como pendência real no resumo final, já que é um ativo que precisa ser criado (ou decidido que não é necessário) antes da submissão.

## Checklist de itens que costumam causar rejeição

Resolver **antes** de submeter, quando aplicável ao app em questão:

- App com página de Política de Privacidade — **sempre obrigatório**, todo app.
- App com página de Termos de Uso — obrigatório se o app tiver conta/cadastro ou regras de uso específicas além do padrão da Apple; se o app não tiver conta nenhuma, o "Apple's Standard License Agreement" (padrão, já preenchido automaticamente na ficha) costuma bastar, e criar um Termos de Uso próprio é opcional.
- Opção de excluir a conta — obrigatório **somente** se o app tiver sistema de conta/cadastro.
- Opção de trocar a senha — obrigatório **somente** se o app tiver login com senha própria (não se aplica a apps que só usam Sign in with Apple/Google, nem a apps sem login).
- Opção de sair do app (logout) — obrigatório **somente** se o app tiver conta.
- Opção de entrada sem conta (modo convidado) — recomendado para apps que têm conta mas querem reduzir fricção; não se aplica a apps sem conta nenhuma.
- Se o app usa câmera, galeria, microfone, calendário, localização, bluetooth ou outros sensores/dados sensíveis: incluir a mensagem de permissão (`Info.plist` / equivalente) explicando por que o app precisa daquele acesso — a Apple rejeita se a descrição estiver genérica demais ou ausente.
- App Encryption Documentation ("Missing Compliance" no build) — sempre precisa ser respondido antes de conseguir submeter (ver seção 7 do SKILL.md para o critério de resposta padrão).

Para apps **sem** sistema de conta, a maior parte desta lista simplesmente não se aplica — mas vale sempre checar item por item contra a spec, em vez de assumir que "não tem conta" já resolve tudo (por exemplo, permissão de câmera pode ser necessária mesmo sem conta nenhuma).
