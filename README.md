# Skills

Skills que criei e uso no dia a dia com o Claude (Anthropic): pacotes de instruções que ensinam o Claude a executar um tipo de trabalho de um jeito específico, com o passo a passo, os cuidados e os templates que aprendi fazendo.

## Skills disponíveis

| Skill | O que faz |
| --- | --- |
| [android-port-publish](android-port-publish/SKILL.md) | Playbook para portar um app iOS para Android nativo (Kotlin + Jetpack Compose) com paridade de comportamento e publicá-lo na Google Play: decisões iniciais, spec adaptada, toolchain, mapa de tradução iOS→Android, verificação no emulador e publicação passo a passo. |
| [app-store-connect](app-store-connect/SKILL.md) | Gera, a partir de uma spec de produto, o pacote para colar no App Store Connect (nome, subtítulo, descrição, keywords, notas de revisão, privacidade, criptografia, Content Rights, classificação etária e preço), reaproveitando seus ativos fixos e checando os limites de caracteres com um script. |
| [comercial-video-ia](comercial-video-ia/SKILL.md) | Guia passo a passo para criar comerciais e vídeos curtos com IA no Higgsfield: briefing, fichas de personagem e produto, locações, tomadas com Seedance, upscale, checagem de cada rascunho e montagem no Final Cut. |
| [sdd-spec](sdd-spec/SKILL.md) | Cria ou atualiza uma especificação no formato SDD (Spec-Driven Development): um `spec.md` completo pronto para o Claude Code implementar, com modelo de dados (`.dbml`), prompt de design, prompt de implementação e guardrails (hooks, subagente verificador, `REVIEW.md`). |
| [slides-apple-minimal](slides-apple-minimal/SKILL.md) | Gera slides e imagens em JPG no padrão keynote da Apple: fundo branco, texto quase-preto em Inter Display, destaque pontual em azul e nada além do texto. |

## Stack técnica

- Markdown (`SKILL.md` com frontmatter `name` / `description`, e arquivos de referência em `references/`)
- Python 3 no script auxiliar `app-store-connect/scripts/check_limits.py` e nos trechos de código das skills
- Pacotes `.skill` (zip da pasta da skill) em `dist/`, prontos para instalar

## Como foi construído

As skills foram escritas com o Claude (Anthropic), a partir do que funcionou na prática nos apps e projetos da Dab Lab. A `sdd-spec` é a mesma metodologia SDD usada para especificar os apps (spec, modelo de dados, prompts e guardrails do Claude Code). Este repositório não tem testes automatizados nem CI; o `check_limits.py` é uma checagem usada pela própria skill durante o uso.

## Status

Publicado e em uso: as skills são as versões que uso hoje.

## Como usar

### Estrutura

```
skills/
├── <nome-da-skill>/
│   └── SKILL.md              # instruções da skill (legível direto no GitHub)
└── dist/
    └── <nome-da-skill>.skill # pacote pronto para instalar
```

### Instalar no Claude (claude.ai ou app desktop)

1. Baixe o arquivo `.skill` da pasta [`dist/`](dist/).
2. Em Configurações → Capacidades → Skills, faça o upload do arquivo.
3. O Claude passa a usar a skill sempre que o pedido combinar com a descrição dela.

### Instalar no Claude Code

Copie a pasta da skill (por exemplo `comercial-video-ia/`) para `~/.claude/skills/` (uso pessoal) ou para `.claude/skills/` dentro do seu projeto.

### Adaptar

Abra o `SKILL.md`, ajuste o texto ao seu contexto (ferramentas, nomes, preferências) e reempacote. O arquivo `.skill` é só um `.zip` da pasta da skill:

```bash
zip -r dist/minha-skill.skill minha-skill/
```

A skill `app-store-connect` tem campos `[PREENCHER: ...]` em `references/meus-ativos.md` para você completar com os seus dados.

## Licença

Licença MIT: você pode usar, copiar, adaptar e redistribuir as skills, mantendo o aviso de copyright. Veja [LICENSE](LICENSE).

## Contribuições

Issues são bem-vindas; pull requests não são aceitos. Veja [CONTRIBUTING.md](CONTRIBUTING.md).

---

Feito pela [Dab Lab](https://www.dablab.com.br/) — product studio de software e IA que constrói apps para pequenas empresas, startups e áreas dentro de grandes empresas, partindo de uma especificação (Spec-Driven Development) e com as disciplinas de engenharia de software robusta.
