#!/usr/bin/env bash
# ==============================================================================
# Total Cleanup — Instalador Automatizado e Idempotente Universal
# Compatible con: Google Antigravity, Claude Code, OpenCode CLI & Linux
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"
SKILL_DIR="${HOME}/.gemini/config/skills/total-cleanup"
BIN_DIR="${HOME}/.local/bin"

echo "🧹 Instalando / Actualizando Total Cleanup (Universal)..."

# 1. Antigravity 2.0 (Target principal)
mkdir -p "$SKILL_DIR/scripts" "$SKILL_DIR/assets"
if [ "$REPO_DIR" != "$SKILL_DIR" ]; then
  cp -u "$REPO_DIR/SKILL.md" "$SKILL_DIR/SKILL.md"
  cp -u "$REPO_DIR/scripts/clean_project.py" "$SKILL_DIR/scripts/clean_project.py"
fi
chmod +x "$SKILL_DIR/scripts/clean_project.py"

if [ -d "$REPO_DIR/assets" ] && [ "$REPO_DIR" != "$SKILL_DIR" ]; then
  cp -ru "$REPO_DIR/assets/"* "$SKILL_DIR/assets/"
fi

# 2. Instalar CLI global en ~/.local/bin
mkdir -p "$BIN_DIR"
cat << 'BIN_EOF' > "$BIN_DIR/clean-project"
#!/usr/bin/env bash
exec python3 "${HOME}/.gemini/config/skills/total-cleanup/scripts/clean_project.py" "$@"
BIN_EOF
chmod +x "$BIN_DIR/clean-project"

# 3. Claude Code (Si el directorio ~/.claude existe)
if [ -d "${HOME}/.claude" ]; then
  CLAUDE_TARGET="${HOME}/.claude/skills/total-cleanup"
  mkdir -p "$CLAUDE_TARGET"
  cp -u "$REPO_DIR/SKILL.md" "$CLAUDE_TARGET/SKILL.md"
  echo "✔ Total Cleanup vinculado a Claude Code: $CLAUDE_TARGET"
fi

# 4. OpenCode CLI (Si el directorio ~/.config/opencode existe)
if [ -d "${HOME}/.config/opencode" ]; then
  OPENCODE_TARGET="${HOME}/.config/opencode/skills/total-cleanup"
  mkdir -p "$OPENCODE_TARGET"
  cp -u "$REPO_DIR/SKILL.md" "$OPENCODE_TARGET/SKILL.md"
  echo "✔ Total Cleanup vinculado a OpenCode CLI: $OPENCODE_TARGET"
fi

echo "✔ Total Cleanup actualizado correctamente:"
echo "  • Skill: $SKILL_DIR"
echo "  • CLI:   $BIN_DIR/clean-project"
echo "  Disponible en Antigravity y terminal mediante: 'optimizar', 'limpiar', 'limpieza' o 'clean-project --deep'."
