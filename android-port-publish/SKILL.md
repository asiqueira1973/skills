---
name: android-port-publish
description: >-
  Playbook para portar um app iOS existente para Android NATIVO (Kotlin + Jetpack Compose) e
  publicá-lo na Google Play Store. Use SEMPRE que o usuário quiser criar uma versão Android de um
  app iOS que já existe, "portar para Android", "fazer o mesmo app no Android", manter as duas
  versões (iOS + Android), ou publicar/enviar um app Android para a Play Store (Play Console, ficha
  da loja, produto in-app, release de produção) — mesmo que ele não diga "port" ou "skill". Cobre o
  processo inteiro: decisões iniciais, spec adaptado do iOS, toolchain Android via Homebrew, mapa de
  tradução iOS→Android, implementação por épicos com verificação no emulador, documentação e a
  publicação passo a passo na Play. Não use para apps Android novos do zero sem contraparte iOS, nem
  para builds cross-platform (Flutter/RN).
---

# Portar iOS → Android nativo e publicar na Play

Este playbook captura um processo comprovado de **portar um app iOS para Android nativo** mantendo
**paridade de comportamento**, e depois **publicar na Play Store**. Ele existe porque um port bem
feito não é reescrever no escuro: é reaproveitar o produto do iOS como fonte de verdade, traduzir a
tecnologia com cuidado, e **verificar cada passo rodando de verdade** — o que pega, cedo, bugs que
só apareceriam no aparelho.

**Regra de ouro: o app iOS é intocável.** O Android é um repositório separado e independente. A
paridade é de **comportamento**, nunca de código compartilhado. Nunca abra, edite ou dependa do
projeto iOS.

## Como usar este skill

Há dois documentos de referência detalhados (leia o relevante quando chegar na fase):

- **`references/port-playbook.md`** — o processo completo do port (decisões, spec, toolchain,
  scaffold, épicos, verificação, docs). Leia no início de um port.
- **`references/play-store-playbook.md`** — só a publicação na Play (assinatura, AAB, criar app,
  ficha, declarações, produto in-app, license testing, release/review). Leia quando o app Android
  estiver pronto para publicar (ou se o usuário só quer a parte da loja).

O corpo abaixo é o resumo orquestrador; os detalhes e comandos exatos estão nas referências.

## Fase 1 — Decidir antes de codar (pergunte)

Um port é grande; alinhe o que muda produto/negócio antes de escrever código:

- **Stack:** recomende **nativo (Kotlin + Compose)** — casa com paridade e qualidade, e é o melhor
  caminho para camera/câmera, sensores e integrações. Aceite que serão **duas bases de código**.
  Só considere cross-platform se o usuário priorizar explicitamente uma base única sobre qualidade.
- **Escopo da 1ª versão:** paridade total (versão atual do iOS) vs. core primeiro.
- **Conta de publicação:** confirme em qual conta de desenvolvedor os apps já existem — **conta de
  organização estabelecida é isenta do teste fechado de 20 pessoas** e pode ir direto pra produção.

Seja honesto sobre o que o ambiente permite: você consegue **escrever e compilar** o Android (e até
rodar testes/emulador headless), mas o ajuste fino de sensores/câmera/cores e a compra real
**validam no aparelho** — igual foi no iOS.

## Fase 2 — Spec-driven (não comece do zero)

O `spec.md` **e** a `DOCUMENTACAO-TECNICA.md` do iOS são a fonte de verdade de **comportamento** —
leia as duas (a doc técnica captura enhancements que o spec não tem; onde divergirem, siga a doc
técnica = o que foi de fato construído). Escreva um **spec Android** que reaproveita o produto e
detalha só o que **muda de tecnologia** (arquitetura, modelo Room, traduções de API, integrações de
plataforma) + o `.dbml`. Documente as **invariantes que não podem ser quebradas** (encodings,
migrações aditivas, regras de sincronização de dados) — o que "só quem construiu sabe".

## Fase 3 — Toolchain (macOS, sem GUI)

Ver `references/port-playbook.md` §3. Resumo: **JDK 17/21** (o AGP não aceita JDK muito novo, ex.:
25), Android SDK via `android-commandlinetools` (+ licenças), Android Studio, e um AVD (habilite a
câmera no AVD se o app for de câmera). Dá pra compilar e rodar emulador **headless pela CLI**.

## Fase 4 — Scaffold + convenções

Gradle Kotlin DSL + Version Catalog, `minSdk` coerente, `applicationId` no mesmo namespace da marca.
Convenção: **banco em português `snake_case`** (colunas via `@ColumnInfo`), **código Kotlin em
inglês**, **comentários em português** citando a regra do spec.

## Fase 5 — Mapa de tradução iOS → Android

Adapte ao app (o "como" muda; o mapa é o mesmo):

| iOS | Android |
|---|---|
| SwiftUI | Jetpack Compose |
| SwiftData / Core Data | Room (+ DataStore p/ preferências simples) |
| Combine / @Published | StateFlow / `collectAsState` |
| `.lproj` (i18n) | `res/values` + `values-XX`; troca em runtime via `attachBaseContext` + `recreate()` |
| StoreKit | Google Play Billing |
| UserNotifications / alarmes | `AlarmManager` + `NotificationManager` (permissões de exact alarm/notification; cuidado com Doze) |
| AVFoundation (câmera) | CameraX (+ `Camera2Interop` p/ manual) |
| Core Image (filtros) | OpenGL ES / shader GLSL (ou RenderEffect no Android 13+) |
| Fototeca | MediaStore |
| App Shortcuts / Widgets / Control | App Shortcuts (`shortcuts.xml`), Quick Settings Tile (`TileService`), botões físicos via `dispatchKeyEvent` |
| Ícone (AppIcon) | Ícone adaptativo (mipmap-anydpi-v26: background + foreground na zona segura) — **derive do ícone do iOS**; serve também para o 512×512 da loja |

## Fase 6 — Implementar por épicos, VERIFICANDO cada um

Siga a mesma ordem de épicos do spec, mudanças aditivas. **Não acumule sem verificar:**
`./gradlew assembleDebug` (compila), **testes unitários JVM** (regras/lógica pura), **testes
instrumentados** no emulador (DB/GPU/etc.), e **screenshots do app rodando** para validar UI. Rodar
de verdade acha bugs cedo (pipeline, orientação, closures obsoletos, insets — todos pegos no
emulador, não no aparelho).

## Fase 7 — Paridade e documentação

Carregue as invariantes críticas do iOS; onde a plataforma obrigar a divergir, **registre a
divergência** (alvo: equivalência de comportamento/visual, não de bits). Entregue **CLAUDE.md** (com
as pegadinhas que não podem quebrar) e, ao fim, **DOCUMENTACAO-TECNICA.md** (6 itens, incluindo
divergências). Mantenha os docs no mesmo commit da mudança.

## Fase 8 — Publicar na Play

Quando o app estiver pronto, siga **`references/play-store-playbook.md`** passo a passo. Pontos
altos: gerar **upload key** + Play App Signing + **`bundleRelease` (AAB assinado)**; escolher a
conta certa; **criar o app**; **ficha da loja** reaproveitando o conteúdo do iOS adaptado (ícone
512, **feature graphic 1024×500**, screenshots **9:16** — reenquadre as do iOS que são mais altas);
**declarações** (privacidade reusada, data safety "nenhum dado" se local-first, content rating,
target audience); **produto in-app** (o Play chama de **"One-time products"**); **license testing**
para testar a compra de graça; e **release de produção → review**.

> O Play Console é um **SPA que trava automação de navegador** — não tente dirigi-lo. O papel do
> agente é **preparar tudo** (build, ícone, feature graphic, screenshots, e um `.md` com todos os
> textos/respostas prontos) e **guiar a pessoa clicando**. Ações irreversíveis (criar app, ativar
> produto, iniciar rollout) são confirmadas pela pessoa.

## Pegadinhas (aprendidas na prática)

- **JDK novo demais** quebra o AGP → 17/21.
- **Compose `pointerInput(Unit)`** captura estado obsoleto → keyar no estado que muda
  (`pointerInput(estado)` ou `rememberUpdatedState`).
- **Insets:** `systemBarsPadding()` no HUD/overlays, senão toques caem na barra do sistema.
- **`connectedAndroidTest` desinstala o app** ao fim → salvar artefatos em MediaStore/Download, não
  em `getExternalFilesDir`.
- **uiautomator** não pega "idle" com `GLSurfaceView`/animação → use screenshot + coords.
- **Play:** screenshots 9:16; "In-app products" virou "One-time products"; o produto in-app precisa
  de um build com billing já enviado; compra de graça só com License testing; feature graphic é
  obrigatória; conta pessoal nova cai no teste fechado, conta de organização é isenta.

## Se ninguém tem aparelho Android

Comportamento de hardware (sensores, câmera, notificações/alarmes, compra real) valida no device.
Se quem tem o app não tem Android, mande um **APK de debug** para um testador (sideload); um botão
de debug para simular estados (ex.: compra) ajuda a validar o fluxo sem a loja.
