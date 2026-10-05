---
name: slides-apple-minimal
description: "Gera slides/imagens em JPG no padrão Apple keynote — fundo branco, texto quase-preto em Inter Display, destaques pontuais em azul, nada além do texto. Use sempre que o pedido for criar um slide, uma imagem de frase, um card ou um conjunto de telas minimalistas para apresentação interna: \"faz um slide com o texto X\", \"gera uma imagem com essa frase\", \"slide da abertura da reunião\", \"cria os slides do workshop\", \"quero isso em JPG para projetar\", \"card para o time\", \"imagem no estilo Apple/keynote\" — mesmo que não citem Apple, JPG nem a palavra skill. Também para versões em quadrado ou vertical da mesma frase."
---

# Slides no padrão Apple (JPG)

Slides de frase única para reuniões, workshops e apresentações internas.
Um slide = uma ideia. Fundo branco, texto quase-preto, no máximo um destaque em azul.

**Esta skill não aplica identidade visual de marca.** É o padrão Apple puro, sem logo,
sem assinatura, sem cores de marca. Se o usuário pedir logo ou cores da empresa, use a
skill de marca dele (se houver) em vez desta.

## O padrão

| Elemento | Valor |
|---|---|
| Fundo | `#FFFFFF` |
| Texto | `#1D1D1F` (o quase-preto da Apple — não use `#000`) |
| Destaque | `#0071E3` (azul de ação da Apple) |
| Texto secundário | `#6E6E73` |
| Fonte | Inter Display 600, tracking `-0.028em`, leading `1.06` |
| Formato padrão | 16:9 · 1920×1080 · JPG |

Regras de composição, na ordem de importância:

1. **Uma ideia por slide.** Frase curta. Se precisar de duas frases, quebre em dois slides.
2. **Destaque só quando muda a leitura.** Uma expressão em azul por slide, no máximo. Um slide todo preto é o default correto; azul é exceção.
3. **Nunca bullet points.** Se o conteúdo pede lista, gere um slide por item.
4. **Sem logo, sem rodapé, sem número de página, sem linha decorativa.** O vazio é o design.
5. Texto centralizado por padrão. `align: left` só quando houver kicker + subtítulo juntos.

## Como gerar

### 1. Garanta a fonte (uma vez por sessão)

```bash
fc-list | grep -qi "Inter" || apt-get install -y --no-install-recommends fonts-inter
```

Sem a Inter o script cai para Helvetica/Liberation Sans — funciona, mas perde o desenho.

### 2. Escreva o script

Crie `slide_apple.py` no diretório de trabalho com o conteúdo da seção
**Script** abaixo, exatamente como está. Depende de `playwright` + Chromium
(já presentes no ambiente) e de `pillow`.

### 3. Rode

Um slide:

```bash
python3 slide_apple.py --title "Que problemas estamos querendo **resolver**?" --out ./slides
```

Vários slides (preferível — abre o navegador uma única vez):

```bash
cat > slides.json <<'JSON'
[
  {"title": "Comece pelo **problema**."},
  {"title": "Que problemas estamos querendo **resolver**?"},
  {"kicker": "Inovação · Tecnologia",
   "title": "Nosso trabalho não é entregar software.\nÉ **remover atrito** do dia da operação.",
   "subtitle": "Três frentes para o próximo trimestre.",
   "align": "left"}
]
JSON
python3 slide_apple.py --json slides.json --out ./slides
```

Sintaxe do texto: `**assim**` vira azul; `\n` força quebra de linha.

Opções úteis: `--format 1x1|9x16|4x3`, `--size 2400x1350`, `--png`,
`--accent "#0071E3"`, `--align left`, `--name meu-arquivo`.

### 4. Verifique antes de entregar

**Obrigatório:** abra cada JPG gerado com a ferramenta Read e confirme que o texto
não está cortado nem transbordando. O auto-fit é confiável, mas uma verificação
visual custa uma chamada e evita entregar um slide quebrado.

### 5. Entregue

`SendUserFile` com cada JPG. Quando o usuário não disser onde quer o destaque azul,
entregue duas versões — uma toda preta e uma com o destaque — e deixe ele escolher.
Se houver pasta conectada no computador dele, grave também com `device_commit_files`.

## Script

```python
#!/usr/bin/env python3
"""
slide_apple.py — gera slides JPG no padrao Apple keynote:
fundo branco, texto quase-preto, destaques em azul, minimalista.
"""

import argparse
import asyncio
import html
import json
import os
import re
import subprocess
import sys
import unicodedata

FORMATS = {
    "16x9": (1920, 1080),
    "1x1": (1080, 1080),
    "9x16": (1080, 1920),
    "4x3": (1600, 1200),
}

INK = "#1D1D1F"      # quase-preto da Apple
BLUE = "#0071E3"     # azul de acao da Apple
GREY = "#6E6E73"     # cinza de texto secundario
BG = "#FFFFFF"

FONT_STACK = ("'Inter Display','Inter','SF Pro Display',-apple-system,"
              "'Helvetica Neue','Liberation Sans',Arial,sans-serif")


def check_font():
    try:
        out = subprocess.run(["fc-list"], capture_output=True, text=True, timeout=20).stdout
    except Exception:
        return
    if "Inter" not in out:
        print("[aviso] Fonte Inter nao encontrada. Instale com:\n"
              "        apt-get install -y --no-install-recommends fonts-inter\n"
              "        (sem ela o slide cai para Helvetica/Liberation Sans)", file=sys.stderr)


def slugify(text, fallback="slide"):
    text = re.sub(r"\*\*|__", "", text)
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    text = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
    return (text[:60] or fallback)


def markup(text, accent):
    """Escapa HTML, converte **x** em destaque azul e \\n em <br>."""
    out, last = [], 0
    for m in re.finditer(r"\*\*(.+?)\*\*", text, flags=re.S):
        out.append(html.escape(text[last:m.start()]))
        out.append(f'<span style="color:{accent}">{html.escape(m.group(1))}</span>')
        last = m.end()
    out.append(html.escape(text[last:]))
    return "".join(out).replace("\\n", "<br>").replace("\n", "<br>")


def build_html(slide, w, h, ink, accent, bg):
    align = slide.get("align", "center")
    kicker = slide.get("kicker") or ""
    subtitle = slide.get("subtitle") or ""
    title = slide.get("title") or ""

    pad_x = round(w * (0.085 if align == "center" else 0.095))
    pad_y = round(h * 0.10)
    max_title = round(h * 0.170)
    min_title = round(h * 0.042)
    kicker_size = round(h * 0.030)
    sub_size = round(h * 0.040)
    justify = "center" if align == "center" else "flex-start"

    kicker_el = (f'<div class="kicker">{markup(kicker, accent)}</div>' if kicker else "")
    sub_el = (f'<div class="sub">{markup(subtitle, accent)}</div>' if subtitle else "")

    return f"""<!doctype html><meta charset="utf-8"><style>
  *{{margin:0;padding:0;box-sizing:border-box}}
  html,body{{width:{w}px;height:{h}px;background:{bg};
    -webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility}}
  body{{padding:{pad_y}px {pad_x}px;font-family:{FONT_STACK}}}
  #box{{width:100%;height:100%;display:flex;flex-direction:column;
    justify-content:center;align-items:stretch;overflow:hidden}}
  /* flex:none e obrigatorio: sem isso o flex encolhe #inner e o transbordo
     fica escondido dentro dele, quebrando a medicao do auto-fit. */
  #inner{{flex:none;width:100%;text-align:{align};display:flex;
    flex-direction:column;align-items:{justify}}}
  .kicker{{font-size:{kicker_size}px;font-weight:600;color:{accent};
    letter-spacing:.005em;line-height:1.25;margin-bottom:{round(kicker_size*1.15)}px}}
  #title{{width:100%;font-weight:600;color:{ink};letter-spacing:-.028em;
    line-height:1.06;font-size:{max_title}px;text-wrap:balance}}
  .sub{{font-size:{sub_size}px;font-weight:400;color:{GREY};letter-spacing:-.012em;
    line-height:1.38;margin-top:{round(sub_size*1.05)}px;max-width:74%;text-wrap:pretty}}
</style>
<div id="box" data-max="{max_title}" data-min="{min_title}" data-h="{h}"><div id="inner">{kicker_el}<div id="title">{markup(title, accent)}</div>{sub_el}</div></div>"""


# O auto-fit roda a partir do Python, DEPOIS de document.fonts.ready. Rodar inline
# no <script> mede com a fonte de fallback e o resultado sai errado ou instavel.
FIT_JS = """() => {
  const box = document.getElementById('box');
  const inner = document.getElementById('inner');
  const t = document.getElementById('title');
  const H = +box.dataset.h, MAX = +box.dataset.max, MIN = +box.dataset.min;
  // Teto por numero de linhas: 1 linha pode ser enorme, 3+ linhas pedem tipo menor.
  const cap = n => n <= 1 ? H * 0.170
                 : n === 2 ? H * 0.120
                 : n === 3 ? H * 0.098
                 : n === 4 ? H * 0.082
                 : H * 0.070;
  // Mede #inner direto: um flex centralizado nao reporta transbordo em scrollHeight.
  const fits = (px) => {
    t.style.fontSize = px + 'px';
    const lines = Math.max(1, Math.round(t.offsetHeight / (px * 1.06)));
    return px <= cap(lines)
        && inner.offsetHeight <= box.clientHeight
        && t.scrollWidth <= t.clientWidth + 1;
  };
  let best = MIN;
  for (let px = MAX; px >= MIN; px -= 1) {
    if (fits(px)) { best = px; break; }
  }
  fits(best);
  return best;
}"""


async def render(slides, w, h, outdir, ink, accent, bg, quality, fmt, scale):
    from playwright.async_api import async_playwright

    os.makedirs(outdir, exist_ok=True)
    paths = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(args=["--font-render-hinting=none",
                                                "--disable-lcd-text"])
        page = await browser.new_page(viewport={"width": w, "height": h},
                                      device_scale_factor=scale)
        for i, slide in enumerate(slides, 1):
            await page.set_content(build_html(slide, w, h, ink, accent, bg))
            await page.evaluate("() => document.fonts.ready")
            await page.evaluate(FIT_JS)          # ajusta o corpo do titulo
            await page.evaluate(FIT_JS)          # 2a passada: converge apos o reflow
            await page.wait_for_timeout(80)
            name = slide.get("name") or f"{i:02d}-{slugify(slide.get('title',''))}"
            path = os.path.join(outdir, f"{name}.{'jpg' if fmt == 'jpeg' else fmt}")
            shot = os.path.join(outdir, f".raw-{i}.png") if scale > 1 else path
            if scale > 1:
                await page.screenshot(path=shot, type="png")
            else:
                await page.screenshot(path=path, type=fmt,
                                      quality=quality if fmt == "jpeg" else None)
            if scale > 1:
                from PIL import Image
                img = Image.open(shot).convert("RGB").resize((w, h), Image.LANCZOS)
                if fmt == "jpeg":
                    img.save(path, "JPEG", quality=quality, subsampling=0, optimize=True)
                else:
                    img.save(path, "PNG")
                os.remove(shot)
            paths.append(path)
        await browser.close()
    return paths


def main():
    ap = argparse.ArgumentParser(description="Slides JPG no padrao Apple")
    ap.add_argument("--title", help="texto do slide; **assim** vira azul")
    ap.add_argument("--kicker", help="linha curta acima do titulo, em azul")
    ap.add_argument("--subtitle", help="linha de apoio abaixo, em cinza")
    ap.add_argument("--align", choices=["center", "left"], default="center")
    ap.add_argument("--json", dest="json_path", help="arquivo JSON com uma lista de slides")
    ap.add_argument("--out", default="./slides", help="pasta de saida")
    ap.add_argument("--name", help="nome do arquivo (sem extensao) no modo --title")
    ap.add_argument("--format", dest="ratio", default="16x9", choices=list(FORMATS))
    ap.add_argument("--size", help="tamanho custom, ex. 2000x1250 (sobrepoe --format)")
    ap.add_argument("--png", action="store_true", help="salva PNG em vez de JPG")
    ap.add_argument("--quality", type=int, default=94)
    ap.add_argument("--ink", default=INK)
    ap.add_argument("--accent", default=BLUE)
    ap.add_argument("--bg", default=BG)
    ap.add_argument("--scale", type=int, default=2, help="supersampling (2 = mais nitido)")
    args = ap.parse_args()

    if args.json_path:
        with open(args.json_path, encoding="utf-8") as f:
            slides = json.load(f)
        if isinstance(slides, dict):
            slides = [slides]
    elif args.title:
        slides = [{k: v for k, v in
                   {"title": args.title, "kicker": args.kicker,
                    "subtitle": args.subtitle, "align": args.align,
                    "name": args.name}.items() if v}]
    else:
        ap.error("informe --title ou --json")

    if args.size:
        w, h = (int(x) for x in args.size.lower().split("x"))
    else:
        w, h = FORMATS[args.ratio]

    check_font()
    paths = asyncio.run(render(slides, w, h, args.out, args.ink, args.accent,
                               args.bg, args.quality,
                               "png" if args.png else "jpeg", args.scale))
    for p in paths:
        print(p)


if __name__ == "__main__":
    main()
```

## Armadilhas já resolvidas (não "simplifique" isso)

- **`#inner` precisa de `flex:none`.** Como item de um flex column, ele encolhe por
  padrão e esconde o transbordo dentro de si — o auto-fit passa a medir errado e o
  título sai cortado.
- **O auto-fit tem que rodar depois de `document.fonts.ready`,** chamado do Python.
  Rodando inline no `<script>` ele mede com a fonte de fallback e o resultado varia
  entre execuções.
- **Não meça transbordo por `scrollHeight` de um flex centralizado** — ele não
  reporta o que vaza para cima. Meça `inner.offsetHeight` contra `box.clientHeight`.
- **O teto por número de linhas é intencional.** Uma linha pode ocupar 17% da altura;
  quatro linhas, 8,2%. Sem isso um texto de três linhas fica gigante e perde o ar.
- `--scale 2` renderiza em 2× e reduz com LANCZOS. É o que deixa o texto nítido.