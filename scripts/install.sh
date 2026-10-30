#!/usr/bin/env bash
# ==============================================================================
# Total Cleanup — Instalador Automatizado e Idempotente para Google Antigravity
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"
SKILL_DIR="${HOME}/.gemini/config/skills/total-cleanup"
BIN_DIR="${HOME}/.local/bin"

echo "🧹 Instalando Total Cleanup en Google Antigravity y entorno local..."

mkdir -p "$SKILL_DIR/scripts" "$SKILL_DIR/assets"
cp -u "$REPO_DIR/SKILL.md" "$SKILL_DIR/SKILL.md"
cp -u "$REPO_DIR/scripts/clean_project.py" "$SKILL_DIR/scripts/clean_project.py"
chmod +x "$SKILL_DIR/scripts/clean_project.py"

if [ -d "$REPO_DIR/assets" ]; then
  cp -ru "$REPO_DIR/assets/"* "$SKILL_DIR/assets/"
fi

mkdir -p "$BIN_DIR"
cat << 'BIN_EOF' > "$BIN_DIR/clean-project"
#!/usr/bin/env bash
exec python3 "${HOME}/.gemini/config/skills/total-cleanup/scripts/clean_project.py" "${1:-.}"
BIN_EOF
chmod +x "$BIN_DIR/clean-project"

echo "✔ Total Cleanup instalado correctamente:"
echo "  • Skill: $SKILL_DIR"
echo "  • CLI:   $BIN_DIR/clean-project"
echo "  Disponible en Antigravity mediante la invocación: 'optimizar', 'limpiar' o 'limpieza'."
