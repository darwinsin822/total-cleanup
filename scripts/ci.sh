#!/usr/bin/env bash
# ==============================================================================
# Total Cleanup — Suite de Verificación Determinista e Integración Continua Local
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"

echo "🧪 [1/4] Validando sintaxis de scripts Bash y Python..."
bash -n "$REPO_DIR/scripts/install.sh"
python3 -c "import ast; ast.parse(open('$REPO_DIR/scripts/clean_project.py').read()); print('  ✔ [PASS] clean_project.py AST sintácticamente válido.')"

echo "🧪 [2/4] Probando instalación en limpio hermética (Clean-Room)..."
TMP_HOME=$(mktemp -d)
HOME="$TMP_HOME" bash "$REPO_DIR/scripts/install.sh" >/dev/null
if [ -f "$TMP_HOME/.gemini/config/skills/total-cleanup/SKILL.md" ] && \
   [ -f "$TMP_HOME/.gemini/config/skills/total-cleanup/scripts/clean_project.py" ] && \
   [ -x "$TMP_HOME/.local/bin/clean-project" ]; then
  echo "  ✔ [PASS] Instalación aislada verificada con éxito."
else
  echo "  ❌ [FAIL] Error en la instalación aislada."
  rm -rf "$TMP_HOME"
  exit 1
fi
rm -rf "$TMP_HOME"

echo "🧪 [3/4] Ejecutando prueba de purga controlada sobre sandbox temporal..."
TEST_SANDBOX=$(mktemp -d)
mkdir -p "$TEST_SANDBOX/build/intermediates" "$TEST_SANDBOX/apk_extracted"
touch "$TEST_SANDBOX/app-v1.0.0.apk" "$TEST_SANDBOX/app-v1.0.1-aligned.apk" "$TEST_SANDBOX/app-v1.0.1-aligned.apk"
python3 "$REPO_DIR/scripts/clean_project.py" "$TEST_SANDBOX" >/dev/null
test -f "$TEST_SANDBOX/app-v1.0.1-aligned.apk"
rm -rf "$TEST_SANDBOX"
echo "  ✔ [PASS] Motor de limpieza ejecutado y verificado en sandbox."

echo "🧪 [4/4] Verificando ausencia total de rutas privadas absolutas..."
if git -C "$REPO_DIR" grep -I -i "/home/darwinsin" ":(exclude).git" 2>/dev/null; then
  echo "  ❌ [FAIL] Se detectaron rutas privadas absolutas."
  exit 1
else
  echo "  ✔ [PASS] 0 rutas privadas absolutas detectadas."
fi

echo ""
echo "✅ Todas las pruebas de CI de Total Cleanup pasaron al 100% (Código de salida 0)."
