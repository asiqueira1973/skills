# Roteiro: publicar um app Android na Google Play Store

Guia genérico e reutilizável do processo de **publicação na Play Console**, do zero até "em
revisão". Serve de orientação para o agente (Claude Code) em qualquer projeto Android da Dab Lab.

Substitua os placeholders: `[NOME]`, `[com.dablab.app]`, `[PRODUCT_ID]`, `[PREÇO]`, `[CATEGORIA]`.

> **Importante:** o Play Console é um SPA pesado que **trava automação de navegador**. O papel do
> agente é **preparar tudo** (build assinado, ícone, feature graphic, screenshots, textos, respostas
> dos formulários) e **guiar a pessoa clicando** com um checklist. Ações irreversíveis (criar app,
> ativar produto, iniciar rollout, aceitar termos) são **confirmadas pela pessoa**.

---

## 0. Pré-requisito: build de release assinado (.aab)

O agente prepara isto localmente:

1. **Gerar uma upload key** (uma vez por app). Comando (a pessoa escolhe/guarda a senha):
   ```bash
   keytool -genkeypair -v -keystore ~/keys/[NOME]-upload.jks -alias [alias] \
     -keyalg RSA -keysize 2048 -validity 10000
   ```
   Guardar **arquivo + senha** em local seguro (se perder, dá pra pedir *reset da upload key* ao
   Google, já que o Play App Signing gerencia a chave final).
2. **`keystore.properties`** na raiz do projeto (gitignored):
   ```
   storeFile=/Users/.../keys/[NOME]-upload.jks
   storePassword=...
   keyAlias=[alias]
   keyPassword=...
   ```
3. **`app/build.gradle.kts`** lê o arquivo e assina o release:
   ```kotlin
   val ksFile = rootProject.file("keystore.properties")
   val ks = java.util.Properties().apply { if (ksFile.exists()) ksFile.inputStream().use { load(it) } }
   android {
     signingConfigs { if (ksFile.exists()) create("release") {
       storeFile = file(ks["storeFile"] as String); storePassword = ks["storePassword"] as String
       keyAlias = ks["keyAlias"] as String; keyPassword = ks["keyPassword"] as String
     } }
     buildTypes { release { if (ksFile.exists()) signingConfig = signingConfigs.getByName("release") } }
   }
   ```
4. **Gerar o AAB:** `./gradlew :app:bundleRelease` → `app/build/outputs/bundle/release/app-release.aab`.

## 1. Escolher a conta certa

- Entrar em **play.google.com/console** e selecionar a **conta de desenvolvedor correta** (onde os
  outros apps já existem). Confirme o **ID/URL** (`.../u/N/developers/ID/...`).
- **Conta de organização estabelecida** → **isenta** do teste fechado de 20 pessoas/14 dias; pode
  publicar **direto em produção**. (Conta pessoal nova/vazia **não** é isenta — cai no teste fechado.)

## 2. Criar o app

Home da conta → **Create app**:
- **App name:** `[NOME]`
- **Default language:** `Português (Brasil) – pt-BR`
- **App or game:** App
- **Free or paid:** **Free** (⚠️ se grátis+IAP; não dá pra mudar Free→Paid depois)
- **Declarations:** marcar as duas (políticas + leis de exportação dos EUA) → **Create app**.

## 3. Ficha da loja (Store listing)

Grow users → Store presence → **Store listings** (idioma pt-BR):
- **App name:** `[NOME]`
- **Short description (≤80 chars):** uma frase forte.
- **Full description (≤4000):** texto adaptado do iOS (trocar "iPhone/iOS/Fototeca/StoreKit" por
  "Android/galeria/Google Play"; incluir integrações Android específicas).
- **App icon (512×512):** derivar do ícone do iOS (PNG 512, com fundo, sem transparência).
- **Feature graphic (1024×500):** **obrigatória**. O agente gera (fundo da marca + nome + tagline).
- **Phone screenshots:** mín. 2 (ideal 4–8), **9:16** (ex.: 1080×1920), lado 320–3840 px.
  - As do iOS (ex.: 1242×2688) são **mais altas** que 9:16 → **reenquadrar** para 1080×1920
    (contain sobre fundo preto fica seamless). O agente faz isso com PIL.

Store settings → **categoria** `[CATEGORIA]` (ex.: Photography) + **contato** (e-mail, site).

## 4. Declarações de conteúdo (App content)

Painel → "Set up your app" (ou **Policy → App content**). Respostas típicas de app **local-first
sem login**:
- **Privacy policy:** URL (reaproveitar o documento da Dab Lab; adicionar uma seção do app).
- **App access:** "All functionality available without special access" (sem login/conta).
- **Ads:** "No ads".
- **Content rating (questionário IARC):** categoria "Utility/Other"; todas as perguntas de conteúdo
  **Não** → classificação **Livre**. Informar e-mail.
- **Target audience:** faixas **18+** (ou 13+); **não** marcar <13 (evita política de Famílias).
- **Data safety:** se nada é enviado pra fora do aparelho → **"Nenhum dado coletado/compartilhado"**.
  (Fotos/arquivos ficam no dispositivo = não é "coleta"; permissões são acesso, não coleta.)
- **Government / Financial / Health:** No (salvo se o app for disso).

## 5. Produto in-app (se houver compra)

Monetize with Play → Products → **One-time products** (o Play renomeou "In-app products") →
**Create product**:
- **Product ID:** `[PRODUCT_ID]` ⚠️ (não muda depois; use o mesmo do iOS p/ consistência).
- **Name / Description.**
- **Purchase option:** ID interno (ex.: `padrao`); **Purchase type:** Buy.
- **Price:** `[PREÇO]`; **Availability:** países.
- **Activate** (o produto precisa ficar Active).
> Só dá pra criar/ativar **depois** de ter subido um **AAB com a permissão de billing**
> (`com.android.vending.BILLING`) numa release.

## 6. Testador de licença (testar compra de graça)

Nível da conta (All apps → **Settings**) → **License testing** → adicionar o **Gmail do testador**
+ License response **RESPOND_NORMALLY**. Assim a compra roda como teste (sem cobrar), inclusive em
produção, no aparelho daquele e-mail.

## 7. Release de produção (submeter)

Test and release → **Production** → **Create new release**:
- **Play App Signing:** Continue (Google gerencia a chave final).
- **App bundles → Upload:** o `app-release.aab`.
- **Release name** (auto) + **Release notes** (pt-BR).
- **Next** → tela de **revisão**: ela lista qualquer pendência (declarações incompletas etc.) com
  link pra corrigir.
- Quando tudo verde: **Start rollout to production** (⚠️ irreversível — a pessoa confirma). Isso
  **manda pro review do Google** (não publica na hora).
- **Publishing overview → Submission activity** mostra o status **"In review"**. A 1ª revisão leva
  de **horas a alguns dias**; chega um **e-mail** com aprovação ou o motivo da recusa.

## 8. Depois de submeter

- **Nada mais a fazer** até a revisão voltar.
- **Validar em aparelho real** o que o emulador não reproduz (sensores, notificações/alarmes, compra
  real). Se ninguém tem Android, mandar um **APK de debug** a um testador (sideload); um botão de
  debug (ex.: "simular compra") ajuda a validar o fluxo sem a loja.
- Aprovado → app **no ar**; o testador de licença instala pela Play e testa a compra de graça.
- Ajuste posterior → **subir o versionCode/versionName** e publicar uma nova release.

---

## Pegadinhas da Play
- **Play Console trava automação de navegador** → guiar a pessoa clicando (não tentar dirigir).
- **Screenshots 9:16** (as do iOS costumam ser mais altas → reenquadrar).
- **"In-app products" virou "One-time products".**
- **Produto in-app** exige um build com billing já enviado antes de ativar.
- **Compra de graça** no teste só com **License testing** configurado.
- **Feature graphic 1024×500 é obrigatória.**
- **`connectedAndroidTest` desinstala o app** ao fim → salvar artefatos em MediaStore/Download.
- **Conta pessoal nova** cai no teste fechado de 20 pessoas; **conta de organização** estabelecida é
  isenta.

## Ativos que o agente entrega antes de começar o Play Console
- `app-release.aab` assinado.
- Ícone 512×512 + feature graphic 1024×500 + screenshots 9:16.
- Um `.md` com **todos os textos e respostas dos formulários** (ficha, descrições, privacidade,
  data safety, content rating, produto in-app, release notes) prontos para copiar e colar.
