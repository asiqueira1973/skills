# Estrutura de referência do documento final

Use isto para lembrar a ordem e o formato das seções — o **conteúdo** de cada
uma vem sempre da spec do app real, nunca deste template.

```markdown
# App Store Connect — conteúdo pronto para colar (<Nome do App>)

Checado contra os limites vigentes da App Store Connect. Localização: <idioma>.

## App Information
- Nome (≤30 car.)
- Subtítulo (≤30 car.)
- Categoria primária / secundária
- Copyright

## Version Information
- Texto promocional (≤170 car.)
- Descrição (≤4.000 car.)
- Keywords (≤100 bytes)
- Notas da versão / What's New (≤4.000 car.)

## App Privacy (questionário)
- Resposta recomendada + justificativa a partir da spec

## URLs obrigatórias
- Support URL
- Privacy Policy URL + seção nova para adicionar no documento compartilhado

## Pricing and Availability
- Preço da ficha
- Disponibilidade
- Produto(s) de In-App Purchase, se houver

## App Review Information
- Sign-in Required (sim/não + justificativa)
- Contact Information
- Notes (formato com pontos de rejeição citados proativamente)

## App Encryption Documentation
- Resposta recomendada + justificativa

## Content Rights
- Resposta recomendada + justificativa (e ressalva se for um caso ambíguo)

## Classificação etária (Age Rating)
- Expectativa (não é a resposta oficial — só o questionário da Apple decide)

## Resultado da checagem de limites (scripts/check_limits.py)
- Colar aqui a saída do script
```
