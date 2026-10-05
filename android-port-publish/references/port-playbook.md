# Roteiro: portar um app iOS para Android (nativo) e publicar na Play Store

Referência genérica do processo que usamos. Serve de base para o prompt de qualquer port
iOS→Android da Dab Lab. **Adapte os exemplos ao app** (câmera, lembrete de remédio, etc. mudam o
"como", não o "roteiro").

Regra de ouro: **o app iOS é intocável.** O Android é um repositório separado e independente; a
paridade é de **comportamento**, não de código compartilhado.

---

## 1. Decisões iniciais (perguntar antes de codar)

- **Stack:** nativo (**Kotlin + Jetpack Compose**) vs cross-platform. Para paridade e qualidade,
  recomende **nativo** — casa com o caminho local-first e evita o pior caso do cross-platform.
  Aceite que serão **duas bases** de código.
- **Escopo da 1ª versão:** paridade total (v atual do iOS) vs core primeiro.
- **Conta e publicação:** confirmar em qual **conta de desenvolvedor** os apps já existem (conta de
  organização estabelecida → **isenta do teste fechado de 20 pessoas**; pode publicar direto em
  produção). Cuidado: conta pessoal nova/vazia cai na exigência de teste fechado.

## 2. Spec-driven (não começar do zero)

- O **spec.md e a DOCUMENTACAO-TECNICA.md do iOS são a fonte de verdade de comportamento.** A doc
  técnica captura os enhancements que o spec não tem — leia as duas.
- Escreva um **spec Android** que reaproveita o produto do iOS e detalha só o que **muda de
  tecnologia**: arquitetura, modelo de dados na tecnologia Android, as traduções de API, integrações
  de plataforma. Gere o `.dbml` do modelo de dados.
- Documente os **mecanismos que não podem ser quebrados** (encodings, migrações, regras de
  sincronização) — o que "só quem construiu sabe".

## 3. Toolchain (macOS, via Homebrew — sem GUI)

- **JDK 17 ou 21** (o AGP não aceita JDK muito novo, ex.: 25). `brew install openjdk@21`.
- **Android SDK** via `brew install --cask android-commandlinetools`; depois `sdkmanager` para
  `platform-tools`, `platforms;android-XX`, `build-tools;XX`, e **aceitar as licenças**.
- **Android Studio** (`brew install --cask android-studio`) para a pessoa usar GUI/emulador.
- **gradle** (`brew install gradle`) só para gerar o wrapper (`gradle wrapper --gradle-version X`
  num diretório com um `settings.gradle.kts` mínimo, e copiar o wrapper pro projeto).
- **Emulador (AVD):** dá pra criar e rodar headless via CLI
  (`emulator -avd NOME -no-window -gpu swiftshader_indirect ...`). Para apps de câmera, habilite a
  câmera no AVD (`hw.camera.back=virtualscene`), senão o CameraX diz "No available camera".

## 4. Esqueleto do projeto

- **Gradle Kotlin DSL** + **Version Catalog** (`libs.versions.toml`), `minSdk` coerente com o que o
  app usa (26 cobre a maioria), `applicationId` no mesmo namespace da marca (ex.: `com.dablab.*`).
- **Pastas por feature** (dados/, telas/, plataforma/, etc.).
- Convenção: **banco em português `snake_case`** (colunas via `@ColumnInfo`), **código Kotlin em
  inglês**, **comentários em português** citando a regra do spec.

## 5. Mapa de tradução iOS → Android (genérico)

| iOS | Android |
|---|---|
| SwiftUI | Jetpack Compose |
| SwiftData / Core Data | **Room** (+ DataStore p/ preferências simples) |
| Combine / @Published | StateFlow / `collectAsState` |
| `.lproj` (i18n) | `res/values` + `res/values-XX`; troca em runtime via `recreate()` |
| StoreKit | **Google Play Billing** |
| UserNotifications / alarmes | `AlarmManager` + `NotificationManager` (+ foreground service se preciso) |
| AVFoundation (câmera) | **CameraX** (+ `Camera2Interop` p/ controles manuais) |
| Core Image (filtros) | **OpenGL ES / shader GLSL** (ou RenderEffect no Android 13+) |
| Fototeca | **MediaStore** |
| App Shortcuts / Widgets / Control | App Shortcuts (`shortcuts.xml`), **Quick Settings Tile** (`TileService`), botões físicos via `dispatchKeyEvent` |
| Ícone (AppIcon) | **ícone adaptativo** (mipmap-anydpi-v26: background + foreground na zona segura) |

> Reaproveite o **ícone do iOS** para gerar o adaptativo do Android (fundo + o glyph central na
> zona segura). Serve também para o ícone 512×512 da loja.

## 6. Implementação por épicos + verificação a cada passo

- Siga a **mesma ordem de épicos do spec**; mudanças aditivas.
- **Verifique cada épico** (não acumule):
  - `./gradlew assembleDebug` (compila?) — dá pra rodar pela CLI.
  - **Testes unitários (JVM)** para regras numéricas/lógica pura (rodam sem device).
  - **Testes instrumentados** no emulador para o que precisa de Android real (DB, GPU, etc.).
  - **Screenshots do app rodando** no emulador para validar UI e pegar bugs de layout cedo.
- Rodar de verdade acha bugs que só apareceriam no device. Ex.: no I See Life pegamos, no emulador,
  bugs de pipeline, rotação de foto, closure obsoleto e insets — tudo antes do aparelho.

## 7. Paridade: o que não pode quebrar

- Carregue as **invariantes críticas** do iOS (encodings de dados, migrações **aditivas** — nunca
  trocar tipo de coluna existente, regras de sincronização de dados de catálogo).
- Onde a plataforma obrigar a divergir (ex.: uma API que não tem equivalente exato), **registre a
  divergência** na doc técnica. Alvo: **equivalência de comportamento/visual**, não igualdade de bits.

## 8. Documentação (no mesmo commit)

- **CLAUDE.md** (guia do agente: convenções, comandos, e as pegadinhas que não podem ser quebradas).
- **DOCUMENTACAO-TECNICA.md** ao fim (6 itens: modelo de dados, relações, lógica, mapa tela→dados,
  funcionalidades por tela, **divergências**).
- **README** com setup e comandos.

## 9. Publicação na Play Store

- **Assinatura:** gerar uma **upload key** (`keytool -genkeypair ... .jks`), guardar arquivo+senha
  em local seguro; `keystore.properties` (gitignored) lido pelo `build.gradle`; **Play App Signing**
  (o Google gerencia a chave final). Build: `./gradlew bundleRelease` → **.aab assinado**.
- **Criar o app** no Play Console (nome, idioma padrão pt-BR, App, **Free** se for grátis+IAP).
- **Ficha da loja:** reaproveitar o conteúdo do iOS **adaptado** (trocar "iPhone/iOS/Fototeca/
  StoreKit" por "Android/galeria/Google Play"). Ativos:
  - **Ícone 512×512**, **feature graphic 1024×500** (obrigatória no Play), **screenshots**.
  - Screenshots do iOS (1242×2688) são **mais altas que o 9:16** do Play → **reenquadrar** para
    1080×1920 (contain sobre fundo preto fica seamless).
- **Declarações de conteúdo:** política de privacidade (reusar o link da Dab Lab + seção do app),
  App access ("sem login"), Ads ("no ads"), Content rating (questionário → Livre), Target audience
  (18+ ou 13+, não <13), **Data safety** (se local-first: "nenhum dado coletado/compartilhado").
- **Produto in-app:** o Play renomeou "In-app products" → **"One-time products"**. Criar produto +
  **purchase option** (ID interno) + preço; **Activate**. Precisa de um build com billing já enviado.
- **License testing** (nível da conta → Settings): adicionar o e-mail do testador → compra roda de
  graça no aparelho dele.
- **Release de produção:** Test and release → Production → **Edit release** → subir o AAB → **Next**
  → revisão → **Start rollout** (irreversível — manda pro review do Google; horas a dias).

## 10. Testes / validação em aparelho

- **Comportamento de hardware valida no device** (câmera/sensores, notificações/alarmes, compra
  real via Play). O emulador não reproduz tudo.
- Se quem tem o app não tem Android, mandar um **APK de debug** para um testador (sideload); um botão
  de debug para simular estados (ex.: compra) ajuda a validar o fluxo sem a loja.
- `connectedAndroidTest` **desinstala o app** ao fim → salvar artefatos de teste em MediaStore/
  Download, não em `getExternalFilesDir`.

## 11. Pegadinhas/aprendizados (genéricos)

- **JDK novo demais** quebra o AGP → use 17/21.
- **Compose `pointerInput(Unit)`** captura estado obsoleto → keyar no estado que muda
  (`pointerInput(estado)` ou `rememberUpdatedState`).
- **Insets:** dar `systemBarsPadding()` no HUD/overlays, senão toques caem na barra do sistema.
- **Play Console é um SPA pesado** que trava automação de navegador → **guiar a pessoa clicando**
  (checklist), não tentar dirigir o navegador.
- **Idioma em runtime:** `attachBaseContext` + `recreate()` (sem AppCompat) funciona bem.
- **uiautomator** não pega "idle" com `GLSurfaceView`/animação contínua → use screenshot + coords.

---

### Modelo de prompt (colar no Claude Code do outro projeto)

```
Quero criar uma versão ANDROID NATIVA (Kotlin + Jetpack Compose) do meu app iOS [NOME], sem
alterar nada no projeto iOS (é base separada). Use o spec.md e a DOCUMENTACAO-TECNICA.md do iOS
como fonte de verdade de comportamento (paridade). Antes de codar: (1) me pergunte stack/escopo/
conta; (2) escreva um spec Android que reaproveita o produto e detalha só o que muda de tecnologia
(arquitetura, modelo Room, traduções de API, integrações de plataforma) + o .dbml; (3) monte o
projeto Gradle e implemente na ordem dos épicos, VERIFICANDO cada um (assembleDebug + testes +
screenshots no emulador). Banco em português snake_case, código em inglês, comentários em
português citando a regra. Gere CLAUDE.md e, ao fim, DOCUMENTACAO-TECNICA.md. Não toque no iOS.
Siga o roteiro de referência "roteiro-port-ios-para-android.md".
```
