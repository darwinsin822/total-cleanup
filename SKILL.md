---
name: total-cleanup
description: >-
  Ultra-aggressive cleanup and storage optimizer for any project and system.
  Activate whenever the user says "optimizar", "limpiar", "limpieza", or requests
  to clean up workspace files or perform deep system maintenance. PURGES all previous
  APK versions, obsolete source code, temporary extraction folders, intermediate builds,
  as well as WhatsApp Web/Flatpak caches, Flutter pub-caches, Rust cargo caches,
  Gradle/NPM caches, and user system caches, preserving active code and personal docs.
---

# 🧹 Total Cleanup — Limpiador Ultra Agresivo de Proyectos y Sistema

Skill universal de optimización extrema de almacenamiento y purga de residuos para proyectos de software y mantenimiento profundo de sistema en Linux Mint / Google Antigravity 2.0. Se activa automáticamente con la palabra **"optimizar"**, **"limpieza"**, **"limpieza profunda"** o ante cualquier solicitud de recuperación de espacio en disco.

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

## 🚀 Uso y Ejecución

```bash
# 1. Limpieza y saneamiento profundo del sistema (WhatsApp, Flutter, Rust, Gradle, NPM, Cache)
clean-project --deep
# o
clean-project --system

# 2. Limpieza completa (Sistema + Proyecto actual)
clean-project --all

# 3. Limpiar el proyecto actual
clean-project .

# 4. Limpiar una ruta de proyecto específica
clean-project /ruta/al/proyecto
```
