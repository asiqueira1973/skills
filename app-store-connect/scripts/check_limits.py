#!/usr/bin/env python3
"""
Confere os campos de texto do App Store Connect contra os limites de
caracteres/bytes vigentes. Meça sempre com este script antes de entregar o
pacote de conteúdo — não estime de cabeça, especialmente com acentuação em
português (o campo de keywords é limitado em BYTES, não caracteres, e letras
acentuadas consomem mais de 1 byte em UTF-8).

Uso:
    python3 check_limits.py campos.json

Onde campos.json tem este formato (todos os campos são opcionais — só
verifica os que estiverem presentes):

{
  "nome": "Meu App",
  "subtitulo": "Subtítulo do app",
  "texto_promocional": "...",
  "descricao": "...",
  "keywords": "md,readme,github,...",
  "notas_versao": "...",
  "notas_revisao_app_review": "..."
}

Os limites abaixo refletem o que foi observado na App Store Connect na época
em que este skill foi escrito. A Apple pode mudar essas regras — se um campo
"estourar" por pouco ou o comportamento na tela parecer diferente do
esperado, confirme o limite atual diretamente no App Store Connect antes de
insistir no valor gerado.
"""
import json
import sys

# (rótulo, chave no JSON, limite, se o limite é em bytes em vez de caracteres)
LIMITS = [
    ("Nome", "nome", 30, False),
    ("Subtítulo", "subtitulo", 30, False),
    ("Texto promocional", "texto_promocional", 170, False),
    ("Descrição", "descricao", 4000, False),
    ("Keywords", "keywords", 100, True),
    ("Notas da versão (What's New)", "notas_versao", 4000, False),
    ("Notas de revisão (App Review)", "notas_revisao_app_review", 4000, False),
]


def check(fields):
    all_ok = True
    for label, key, limit, is_bytes in LIMITS:
        if key not in fields or fields[key] is None:
            continue
        value = fields[key]
        n = len(value.encode("utf-8")) if is_bytes else len(value)
        unit = "bytes" if is_bytes else "caracteres"
        ok = n <= limit
        all_ok = all_ok and ok
        status = "OK" if ok else "ESTOURO"
        print(f"{label}: {n}/{limit} {unit} [{status}]")
        if not ok:
            over = n - limit
            print(f"  -> passou do limite em {over} {unit}. Corte o texto antes de colar no App Store Connect.")
    return all_ok


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        fields = json.load(f)
    ok = check(fields)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
