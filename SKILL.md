---
name: total-cleanup
description: >-
  Ultra-aggressive cleanup and storage optimizer for any project and system.
  Skill universal compatible con cualquier entorno: Claude Code, OpenAI Codex, Google Antigravity, OpenCode, Cursor, etc.
  Activate whenever the user says "optimizar", "limpiar", "limpieza", or requests
  to clean up workspace files or perform deep system maintenance. PURGES all previous
  APK versions, obsolete source code, temporary extraction folders, intermediate builds,
  as well as WhatsApp Web/Flatpak caches, Flutter pub-caches, Rust cargo caches,
  Gradle/NPM caches, and user system caches, preserving active code and personal docs.
---

# 🧹 Total Cleanup — Limpiador Ultra Agresivo de Proyectos y Sistema

Skill universal de optimización extrema de almacenamiento y purga de residuos para proyectos de software y mantenimiento profundo de sistema en Linux Mint / Google Antigravity 2.0. Se activa automáticamente con la palabra **"optimizar"**, **"limpieza"**, **"limpieza profunda"** o ante cualquier solicitud de recuperación de espacio en disco.

---

## 🌐 COMPATIBILIDAD UNIVERSAL MULTI-ENTORNO

Total Cleanup opera de forma agnóstica de plataforma, permitiendo sanear entornos de desarrollo y liberar espacio en cualquier arnés de IA:

| Entorno / Herramienta | Modo de Integración y Operación |
| :--- | :--- |
| **🤖 Google Antigravity (AGY 2.0)** | Integración nativa como Skill en `.gemini/config/skills/total-cleanup/` y CLI `clean-project`. Activación vía chat (`optimizar`, `limpieza`) o subagentes. |
| **🧠 Claude Code (Anthropic)** | Desplegable en `~/.claude/skills/total-cleanup` o ejecutable desde su bash tool mediante el comando global `clean-project --deep`. |
| **⚡ OpenCode CLI** | Compatible con ejecución en terminal con OpenCode CLI (`opencode`), ejecutando rutinas de purga de cachés de compilación y residuos de desarrollo. |
| **⚙️ OpenAI Codex / ChatGPT** | Utilizable en sandboxes y entornos interactivos para sanear el workspace tras ejecuciones de tests y compilaciones intermedias. |
| **💻 Cursor / VS Code / Windsurf** | Utilizable desde la terminal integrada o tareas automatizadas de mantenimiento para liberar espacio consumido por Gradle, Rust o NPM. |

---

## ⚡ Directivas Ultra Agresivas

### 1. 🛡️ Mantenimiento Profundo de Sistema
- **WhatsApp (ICE Web & Flatpak):**
  - Purga cachés HTTP, miniaturas y service workers de `~/.local/share/ice/firefox/Whatsaap*` y `~/.var/app/...WhatsAppForLinux`.
  - **Inmutable:** Conserva íntegras las sesiones, bases de datos locales (`idb`) y chats.
- **Flutter / Dart:**
  - Depura paquetes antiguos descargados y clonaciones git en `~/.pub-cache/hosted` y `~/.pub-cache/git`.
- **Rust / Cargo:**
  - Purga el registro de paquetes descomprimidos (`~/.cargo/registry/src`) y archivos comprimidos descargados (`~/.cargo/registry/cache`).
- **Node.js / NPM & Gradle:**
  - Purga la caché de descargas de NPM (`~/.npm/_cacache`) y cachés globales de compilación de Gradle (`~/.gradle/caches`, daemons huérfanos).
- **OpenCode (Desktop & CLI):**
  - Purga cachés gráficas de Chromium/Electron (`Cache`, `Code Cache`, `GPUCache`), volcados de Crashpad, logs locales y backups obsoletos (`*.bak*`), conservando íntegros `opencode.db`, credenciales y extensiones.
- **Cachés de Usuario del Sistema:**
  - Limpia miniaturas (`~/.cache/thumbnails`), cachés de navegadores y temporales de instaladores.

### 2. 📦 Purga de Versiones Anteriores en Proyectos
- Detecta versiones previas de paquetes y binarios (`.apk`, `.deb`, `.AppImage`, etc.).
- Conserva estrictamente **únicamente el artefacto de la versión más reciente**.

### 3. 🗑️ Eliminación de Código y Descompilaciones Obsoletas
- Purga scripts temporales de versiones antiguas (`build_v*.py`, `patch_injected.js`).
- Elimina carpetas de descompilación temporal (`apk_extracted/`, carpetas `smali_*` residuales).
- Elimina volcados intermedios, caches de compiladores y firmas no alineadas.

### 4. 💎 Preservación Inmutable
- Respeta estrictamente documentos personales (`~/Documentos`, `~/Descargas`, etc.) y el árbol de código fuente limpio activo.

---

### 5. 📊 Analizador de Disco Estilo Baobab (Linux Mint)
- Integra un motor de diagnóstico que replica la visualización y análisis del Analizador de Uso de Disco de Linux Mint (Baobab).
- Muestra tablas jerárquicas con tamaño, porcentaje relativo de ocupación y clasificación automática de elementos limpiables (`target/`, cachés, `.pub-cache`, `node_modules`).

---

## 🚀 Uso y Ejecución

```bash
# 1. Diagnóstico y análisis de disco estilo Baobab
clean-project --baobab
# o
clean-project --analyze

# 2. Limpieza y saneamiento profundo del sistema (WhatsApp, Flutter, Rust, Gradle, NPM, Navegadores, Cache)
clean-project --deep
# o
clean-project --system

# 3. Limpieza completa (Sistema + Proyecto actual)
clean-project --all

# 4. Limpiar el proyecto actual
clean-project .

# 5. Limpiar una ruta de proyecto específica
clean-project /ruta/al/proyecto
```
