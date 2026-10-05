Skills

Repositório onde compartilho as skills que criei e uso no dia a dia com o Claude (Anthropic). Cada skill é um pacote de instruções que ensina o Claude a executar um tipo de trabalho de um jeito específico — com o passo a passo, os cuidados e os templates que aprendi fazendo.

Fique à vontade para usar, adaptar e sugerir melhorias.

Skills disponíveis
Skill	O que faz
android-port-publish	Playbook para portar um app iOS para Android nativo (Kotlin + Jetpack Compose) com paridade de comportamento e publicá-lo na Google Play Store: decisões iniciais, spec adaptado, toolchain, mapa de tradução iOS→Android, verificação no emulador e publicação passo a passo.
app-store-connect	Gera, a partir de uma spec de produto, o pacote completo para colar no App Store Connect: nome, subtítulo, descrição, keywords, notas de revisão, privacidade, criptografia, Content Rights, classificação etária e preço — reaproveitando seus ativos fixos (suporte, política de privacidade, contato), com checagem automática dos limites de caracteres.
comercial-video-ia	Guia passo a passo para criar comerciais e vídeos curtos com IA no Higgsfield: briefing, fichas de personagem e produto, locações, tomadas com Seedance, upscale, checagem de cada rascunho e montagem no Final Cut.
sdd-spec	Cria ou atualiza uma especificação no formato SDD (Spec-Driven Development): um spec.md completo pronto para o Claude Code implementar, com modelo de dados (.dbml), prompt de design, prompt de implementação e guardrails (hooks, subagente verificador, REVIEW.md).
slides-apple-minimal	Gera slides e imagens em JPG no padrão keynote da Apple: fundo branco, texto quase-preto em Inter Display, destaque pontual em azul e nada além do texto.
Estrutura
skills/
├── <nome-da-skill>/
│   └── SKILL.md          # instruções da skill (legível direto no GitHub)
└── dist/
    └── <nome-da-skill>.skill   # pacote pronto para instalar
Como instalar uma skill

No Claude (claude.ai ou app desktop):

Baixe o arquivo .skill da pasta dist/.
Em Configurações → Capacidades → Skills, faça o upload do arquivo.
Pronto — o Claude passa a usar a skill sempre que o pedido combinar com a descrição dela.

No Claude Code:

Copie a pasta da skill (por exemplo comercial-video-ia/) para ~/.claude/skills/ (uso pessoal) ou para .claude/skills/ dentro do seu projeto.

Como adaptar

Abra o SKILL.md, ajuste o texto ao seu contexto (ferramentas, nomes, preferências) e reempacote: o arquivo .skill é só um .zip da pasta da skill.

bash
zip -r dist/minha-skill.skill minha-skill/
Autor

Alexandre Siqueira — Dab Lab
