# Modelos de guardrails do Claude Code (Anexo B do spec)

Modelos para gerar o Anexo B. **Sempre adapte** caminhos de pastas, extensões de arquivo e comandos ao stack da seção 4 do spec. Um hook cujo `case` não casa com as pastas reais não bloqueia nada.

Semântica que os scripts usam: o hook recebe um JSON na entrada padrão com `tool_name` e `tool_input` (em `Write`: `file_path` e `content`; em `Edit`: `file_path`, `old_string`, `new_string`). Em `PreToolUse`, **exit 2 bloqueia a ação** e o texto do stderr volta para o Claude como motivo; exit 0 libera. Em `PostToolUse`, a ação já aconteceu; exit 2 apenas devolve o stderr ao Claude como aviso. Todos os scripts dependem de `jq` e **falham fechado**: sem `jq`, bloqueiam em vez de liberar em silêncio (um guardrail que desliga sozinho é pior que nenhum). Confira a referência atual em code.claude.com/docs/en/hooks antes de usar um recurso novo.

---

## `.claude/settings.json`

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          { "type": "command", "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/guard-secrets.sh" },
          { "type": "command", "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/guard-migrations.sh" },
          { "type": "command", "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/guard-tests.sh" }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          { "type": "command", "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/remind-advisors.sh" }
        ]
      }
    ]
  }
}
```

Remova do `settings.json` a linha de qualquer hook que não se aplica ao projeto (ex.: `remind-advisors.sh` em app sem Supabase; `guard-migrations.sh` em app local sem migrations SQL).

---

## `.claude/hooks/guard-secrets.sh` — credencial privilegiada fora do frontend (seção 20)

```bash
#!/bin/bash
# Bloqueia a escrita de credencial privilegiada em código que roda no cliente.
# Implementa a regra da seção 20: credencial privilegiada só existe no servidor.
command -v jq >/dev/null || { echo "Guardrail inativo: jq não está instalado. Instale o jq (brew install jq) antes de continuar." >&2; exit 2; }
input=$(cat)
path=$(echo "$input" | jq -r '.tool_input.file_path // empty')
content=$(echo "$input" | jq -r '.tool_input.content // .tool_input.new_string // empty')

# AJUSTE: pastas de código de cliente do projeto (seção 18 — organização de pastas).
case "$path" in
  */src/app/*|*/src/components/*|*/src/features/*|*/src/hooks/*) ;;
  *) exit 0 ;;
esac

# AJUSTE: nomes de variáveis/segredos privilegiados do projeto (seção 18 — variáveis de ambiente).
if echo "$content" | grep -qiE 'service_role|SUPABASE_SERVICE_ROLE_KEY|SECRET_KEY'; then
  echo "Bloqueado: credencial privilegiada em código de frontend (seção 20). Mova a operação para uma rota de servidor (seção 13) e chame essa rota do cliente." >&2
  exit 2
fi
exit 0
```

---

## `.claude/hooks/guard-migrations.sh` — migration versionada é imutável (seção 7)

```bash
#!/bin/bash
# Impede editar uma migration que já está no git; mudança de schema vira migration nova.
# Implementa a regra de versionamento de migrations da seção 7.
command -v jq >/dev/null || { echo "Guardrail inativo: jq não está instalado. Instale o jq (brew install jq) antes de continuar." >&2; exit 2; }
input=$(cat)
path=$(echo "$input" | jq -r '.tool_input.file_path // empty')

# AJUSTE: pasta de migrations do projeto.
case "$path" in
  */supabase/migrations/*) ;;
  *) exit 0 ;;
esac

rel="${path#"$CLAUDE_PROJECT_DIR"/}"
if git -C "$CLAUDE_PROJECT_DIR" ls-files --error-unmatch "$rel" >/dev/null 2>&1; then
  echo "Bloqueado: $rel já está versionada. Não se edita migration aplicada; crie uma nova migration com a alteração (seção 7)." >&2
  exit 2
fi
exit 0
```

Arquivo novo (ainda não versionado) passa; só a edição de migration commitada é bloqueada.

---

## `.claude/hooks/guard-tests.sh` — teste intocável durante correção (seção 22.1)

```bash
#!/bin/bash
# Durante uma tarefa de correção de bug, impede o agente de editar testes para "fazer passar".
# Ativo só quando existe o arquivo .claude/fix-mode (criado pelo humano no início da correção).
# Implementa a regra da seção 22.1: bug se corrige no código, não no teste.
[ -f "$CLAUDE_PROJECT_DIR/.claude/fix-mode" ] || exit 0

command -v jq >/dev/null || { echo "Guardrail inativo: jq não está instalado. Instale o jq (brew install jq) antes de continuar." >&2; exit 2; }
input=$(cat)
path=$(echo "$input" | jq -r '.tool_input.file_path // empty')

# AJUSTE: padrões de arquivo de teste do stack.
case "$path" in
  *.test.ts|*.test.tsx|*.spec.ts|*/__tests__/*|*/tests/*|*Tests.swift|*Test.kt)
    echo "Bloqueado: modo de correção ativo (.claude/fix-mode). Corrija o código, não o teste (seção 22.1). Se o teste estiver errado de fato, pare e explique ao humano." >&2
    exit 2 ;;
esac
exit 0
```

Uso: `touch .claude/fix-mode` depois de commitar o teste que reproduz o bug; `rm .claude/fix-mode` ao terminar. Coloque `.claude/fix-mode` no `.gitignore`.

---

## `.claude/hooks/remind-advisors.sh` — advisors do Supabase após DDL (seção 20)

```bash
#!/bin/bash
# Depois de escrever uma migration, lembra o agente de rodar os advisors de segurança e performance.
# Implementa a regra da seção 20 para projetos Supabase.
command -v jq >/dev/null || { echo "Guardrail inativo: jq não está instalado. Instale o jq (brew install jq) antes de continuar." >&2; exit 2; }
input=$(cat)
path=$(echo "$input" | jq -r '.tool_input.file_path // empty')
case "$path" in
  */supabase/migrations/*)
    echo "Migration escrita. Depois de aplicá-la, rode get_advisors (security e performance) e resolva alertas críticos antes de seguir (seção 20)." >&2
    exit 2 ;;
esac
exit 0
```

---

## `.claude/agents/verifier.md`

```markdown
---
name: verifier
description: Confere em contexto limpo se o épico implementado cumpre os critérios de aceite do spec. Use ao terminar cada épico, antes de declarar pronto.
tools: Bash, Read, Grep
---
Você verifica; não corrige nada.

1. Leia no spec.md a seção 8.X do épico indicado, a matriz de permissões (seção 5) e as regras de negócio (seção 11) que o épico toca.
2. Leia o plano em plans/ correspondente e o git diff do épico.
3. Rode os comandos de verificação listados no CLAUDE.md e guarde a saída.
4. Para cada critério de aceite, responda: cumprido / não cumprido / não verificável — sempre com evidência (saída de comando ou arquivo:linha).
5. Para cada tela tocada, confira se o que cada perfil pode fazer bate com a seção 5, inclusive o escopo ("só no próprio departamento").
6. Liste divergências entre o diff e o plano.

Termine com uma linha: PRONTO ou NÃO PRONTO, e os itens que impedem.
```

---

## `REVIEW.md`

```markdown
# Instruções de revisão

## Passes
Faça três passes e marque cada achado com o passe:
- Bugs: erro de lógica, caso de borda quebrado, regressão.
- Segurança: matriz de permissões (spec seção 5) e políticas por tabela (seção 6) respeitadas; credencial privilegiada só no servidor; dado sensível fora de log e mensagem de erro (seção 20).
- Conformidade: a mudança bate com spec.md (épicos da seção 8, regras da seção 11), com o plano em plans/ e com as convenções da seção 18 — banco em português snake_case, rotinas comentadas com a regra que implementam.

## O que é Importante
Importante é o que quebra comportamento, vaza dado ou viola regra do spec. Estilo e nome são detalhe.

## Limite de detalhes
No máximo cinco detalhes por revisão; resuma o resto como contagem.

## Não reportar
Arquivos gerados e o que o lint/CI já garante.
```
