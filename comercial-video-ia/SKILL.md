---
name: "comercial-video-ia"
description: "Guia passo a passo para criar comerciais/vídeos curtos com IA no Higgsfield (fichas de personagem, locações, Seedance, upscale), gerando prompts e conferindo cada etapa."
---

# Comercial em vídeo com IA (método Kaye Creatives adaptado)

Use quando o Alexandre quiser criar um comercial, spec ad, vídeo de produto ou curta com IA generativa (Higgsfield, Seedance, Nano Banana, Seedream, Soul). Baseado no workflow da Kaye Creatives (comercial do iPhone 18) e no que aprendemos fazendo o comercial da Lev Cruiser X (out/2026).

## Como conduzir

- Guiar **um passo de cada vez**. Só avançar depois que o Alexandre confirmar (print ou texto) que o passo atual saiu certo.
- Avaliar cada print com critérios explícitos (o que conferi, o que está certo, o que está errado) e dizer qual versão escolher e por quê.
- Sempre informar o custo em créditos antes de qualquer geração paga e o saldo estimado depois.
- Prompts de geração em **inglês**; explicações em **português**.
- Quando a interface do Higgsfield divergir do que eu disse, pedir print e me ajustar — a UI muda com frequência.

## Fase 0 — Briefing (perguntar antes de tudo)

1. Qual é a história? Começo, meio e desfecho (se o desfecho estiver aberto, propor 2–3 opções).
2. Produto: fotos de referência (idealmente estúdio, vários ângulos).
3. Pessoas reais no vídeo? Pedir **selfie nítida, de frente, sorrindo** de cada uma.
4. Locações (cidade/bairro) e fotos reais se houver (ex.: fachada da loja).
5. Formato (16:9 / 9:16), duração total, onde será publicado.
6. Plano e créditos disponíveis no Higgsfield.
7. Referências de estilo: sugerir buscar no **Pinterest** roupas, looks e cenários antes de escrever os prompts (usar só como referência de estilo — nunca rosto de pessoa real de terceiros).

Entregar então: roteiro em tomadas com tempos, lista de personagens, locações e orçamento de créditos.

## Regra de ouro — NUNCA ir para o vídeo sem as fichas

A ordem é sempre: **fichas de personagem → ficha de produto → locações → só então vídeo**. Não gerar prompt de vídeo enquanto todas as fichas não estiverem aprovadas. As fichas são o que garante consistência entre tomadas.

**Pessoa real = ficha + selfie.** A ficha (rosto reconstruído por IA) sozinha não segura o rosto quando a cena tem vários personagens. Em TODA tomada onde a pessoa real aparece, subir a **selfie como PRIMEIRA imagem** e marcá-la como FACE ONLY, que sobrepõe qualquer outra referência. Pedir expressão sorrindo se a selfie for sorrindo. Aprendido do jeito difícil: T1 e T2 do comercial Lev tiveram de ser refeitas.

## Modelos (Higgsfield)

| Etapa | Rota Kaye (Ultra) | Rota econômica (Plus) |
|---|---|---|
| Fichas de pessoas | Soul 2.0 | Nano Banana 2 (ilimitado nos 7 primeiros dias do Plus) ou Seedream |
| Ficha de produto | Seedream 5.0 Pro | Nano Banana 2 ou Seedream |
| Locações | Soul Cinema (no Cinema Studio) | Nano Banana 2 |
| Vídeo | Seedance 2.5 | Seedance 2.0 |
| Upscale | gerar de novo em 1080p | Edit Video → Upscale → Topaz Video, 1k |
| Locução | ElevenLabs v3, Stability "Creative" (aba Audio) | idem, ou ElevenLabs conectado ao Claude |

Regra: começar pelo modelo gratuito do plano; subir para Seedream/Soul só se a consistência não segurar.

## Gotchas do Higgsfield

- **Unlimited (imagem)**: ligar o toggle em toda geração. No Plus funciona em 2K, mas só **1 imagem por geração** (aumentar o batch volta a cobrar). Clicar Generate várias vezes para ter opções.
- **Unlimited mode (vídeo)** exige pacote extra — deixar desligado.
- **Tags só funcionam inseridas pelo @** (ficam verdes). Texto digitado como "@nome" fica vermelho e é ignorado. A numeração (@Image 1, 2…) segue a ORDEM de upload.
- Por isso, nos prompts de vídeo usar **colchetes** ([LOJA], [SELFIE]…), cada imagem citada **uma única vez** em ACTIVE REFERENCES; no resto do texto usar descrições ("the man", "the old bike"). Entregar tabela colchete → nº da imagem.
- Limpar a caixa de imagens antes de cada tomada e subir na ordem indicada. Ao trocar de aba as referências podem sumir — conferir.
- Conferir que o prompt colou inteiro (rolar até a última frase).
- Nano Banana tende a **duplicar painéis** nas fichas (5–6 em vez de 4): preferir versões com o número certo; duplicata de perfil em personagem secundário é aceitável.
- Ficha de produto com referência só lateral não fixa bem ângulos de frente — incluir a foto real do produto como referência extra no vídeo.
- Locações: pedir "no people" e checar intrusos (guidão, placas, logos duplicados).
- Upscale aceita qualquer vídeo baixado (até 50 MB): baixar o take aprovado e subir em "Add a video to upscale".

## Orçamento (valores observados em out/2026 — reconferir)

- Seedance 2.0, 480p, Standard: **6 s = 18 créditos, 8 s = 24 créditos**.
- Upscale Topaz Video 1k: **14 créditos**.
- Plus = 1.000 créditos/mês. Comercial de 4 tomadas custou ~270 créditos no total, incluindo retrabalho.
- Estratégia: **todos os rascunhos em 480p, batch 1 → aprovar → upscale do take aprovado** (mais barato que regerar em 1080p e preserva o take; regerar é um sorteio novo).
- Se uma tomada falhar 2x, simplificar o prompt (menos personagens/ações) antes de tentar de novo.

## Templates de prompt

### Ficha de personagem (pessoa real)
```
Character reference sheet of the man in [SELFIE] — same face, same identity, same skin tone, same hair. One single horizontal 16:9 image: a collage of EXACTLY FOUR PANELS on a clean seamless light grey studio backdrop, thin white gutters, soft even editorial lighting identical in every panel. THE SAME PERSON IN EVERY PANEL: identity, build, clothing and proportions locked.
THE CHARACTER: [traços visíveis da selfie]. Keep his real age exactly as in the selfie — no de-aging.
WARDROBE, identical in every panel: [roupa — ideal vir de referência do Pinterest]. [acessório/capacete se houver].
PANEL 1 — full length, front, from the base of the neck down to the feet; head outside the frame.
PANEL 2 — same framing from behind.
PANEL 3 — head-and-shoulders close-up, straight-on, natural smile, eyes to camera.
PANEL 4 — strict side-profile head-and-shoulders close-up [com acessório, se houver].
Panels 3 and 4 in macro realism: pores, fine lines, individual hairs. Neutral documentary editorial style, true-to-life colour, fine grain.
NEGATIVE: no text, no logos, no beauty filter, no airbrushing, no plastic skin, no de-aging, no change of identity or clothing between panels, no extra panels, no props, no style drift.
```
Personagens fictícios: mesmo esqueleto, sem selfie, descrevendo idade, etnia, traços, roupa e um acessório marcante (cor de capacete, óculos) que facilite reconhecer no vídeo.

### Ficha de produto
5 painéis em fundo branco: perfil lado A, perfil lado B, 3/4 frente, 3/4 trás, macro do logo. Descrever cada peça visível, cor e textos exatos. Incluir regra de consistência ("identical to [REF] in every panel") para peças que o modelo tende a trocar.

### Locação
Descrever o lugar real (bairro, arquitetura, vegetação, chão), câmera (altura, lente, enquadramento) e luz/horário que a cena vai usar. Sempre: "no people, no pedestrians, no readable text, no logos". Se houver foto real, usá-la como referência e mandar remover pessoas/objetos.

### Tomada de vídeo (estrutura)
```
SCENE CONTEXT — 2–3 frases do que acontece.
ACTIVE REFERENCES — uma linha por imagem: [SELFIE] FACE ONLY primeiro; [PERSONAGEM] identidade/roupa; [PRODUTO] PRODUCT ONLY; [LOCAÇÃO] LOCATION ONLY, ignore its lighting.
FORMAT — duração, cortes, aspect ratio, NO MUSIC.
HARD RULES — quem pode aparecer, quantos de cada coisa.
CAMERA — tipo de movimento, lente, distância (começar perto quando o rosto importa).
THE ACTION — beats cronometrados (0.0–1.8s…).
PHYSICS / LIGHTING / AUDIO / STYLE AND GRADE.
POSITIVE CONSTRAINTS / NEGATIVE.
```
Dicas: uma ação marcante por tomada (o modelo pula detalhes finos, ex.: cachorro baixando óculos); 6 s para cenas simples, 8 s para cenas com efeito ou corte; máx. 1 corte seco por tomada; continuidade de direção de movimento entre tomadas.

## Checagem de cada rascunho

1. **Rosto de perto** (ampliar/abrir em tela cheia — o player pequeno engana). Só fazer upscale depois de aprovar o rosto.
2. Produto fiel (forma, logo, cor).
3. Sem duplicatas (logos, personagens, placas).
4. Ação principal aconteceu.
5. Nada absurdo no movimento (pedais, pés deslizando, corpos fundidos).
Pedir ao Alexandre prints de 3 momentos (início, meio, fim) + o print do rosto.

## Montagem (Final Cut)

- Clipes 1080p em ordem, cortes secos casando o movimento entre tomadas.
- Freeze Frame (Option+F) de ~1 s no último quadro + cartela de 2 s com logo e frase.
- Som ambiente original das tomadas por cima da trilha nos momentos de efeito.
- Trilha: Suno (Custom + Instrumental). Exemplo que funcionou como direção: "chill lo-fi hip hop, laid-back boom bap groove, warm jazzy Rhodes chords, mellow bassline, crisp head-nod drums, subtle Brazilian percussion shaker, cool confident urban vibe, cinematic ad music, builds gently then resolves, 90 BPM". Checar termos de uso comercial do plano gratuito.
- Peça com marca de terceiros: publicar como **fan-made / não oficial** e marcar a marca.

## Organização de arquivos

Pasta do projeto com nomes fixos e minúsculos: `selfie.jpg`, `<produto>_ref.jpg`, fichas (`alexandre.png`, `<produto>.png`, `<personagem>.png`), locações (`<lugar>.png`), takes (`T1_1080p.mp4`…). Dar ♡ em todo take aprovado no Higgsfield.