<div align="center">

# 🧹 Total Cleanup
### Ultra-Aggressive Project & System Storage Purge Engine for Linux & Antigravity 2.0

<img src="./assets/total-cleanup.jpg" alt="Total Cleanup Engine Banner" width="380px" style="border-radius: 12px; margin: 16px 0; box-shadow: 0 8px 24px rgba(0,0,0,0.5);" />

[![GitHub License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Compatible](https://img.shields.io/badge/Antigravity%202.0_Skill-Verified-blue.svg)](https://github.com/darwinsin822/total-cleanup)
[![Purge Engine](https://img.shields.io/badge/Engine-Ultra_Aggressive_Purge-emerald.svg)](#-evidencia-de-ejecución-en-vivo)
[![CI](https://img.shields.io/badge/CI-Passing-brightgreen.svg)](scripts/ci.sh)

</div>

**Total Cleanup** es el motor ultra agresivo de saneamiento de almacenamiento, purga de residuos de compilación, optimización de disco para proyectos de software y mantenimiento profundo de sistema en Linux Mint y Google Antigravity 2.0. Elimina sistemáticamente versiones anteriores obsoletas, árboles de descompilación temporal, cachés de WhatsApp (ICE y Flatpak), paquetes de Flutter/Dart, registros de Rust/Cargo y cachés de desarrollo, preservando de forma inmutable únicamente el artefacto final activo, los documentos personales y el código fuente limpio.

---

## ⚡ Directivas de Limpieza y Saneamiento

1. **🛡️ Mantenimiento Profundo de Sistema:**
   - **WhatsApp (ICE SSB & Flatpak):** Purgado de gigabytes de cachés multimedia HTTP y service workers de WhatsApp Web (`~/.local/share/ice/firefox/Whatsaap*` y `~/.var/app/...WhatsAppForLinux`), protegiendo siempre chats, bases de datos y sesiones.
   - **Flutter / Dart:** Limpieza y vaciado de paquetes y repositorios temporales de `~/.pub-cache`.
   - **Rust / Cargo:** Saneamiento de crates descargados y descomprimidos en `~/.cargo/registry`.
   - **NPM & Gradle:** Limpieza de cachés globales (`~/.npm/_cacache`, `~/.gradle/caches`, daemons).
   - **Cachés de Usuario:** Purga de miniaturas (`~/.cache/thumbnails`), cachés web y temporales de instaladores.

2. **📦 Purga de Paquetes Obsoletos:**
   - Detecta versiones previas de paquetes y binarios (`.apk`, `.deb`, `.AppImage`).
   - Elimina duplicados antiguos y conserva exclusivamente el paquete más reciente.

3. **🗑️ Purga de Descompilaciones y Scripts Temporales:**
   - Elimina carpetas de descompilación (`apk_extracted/`, carpetas `smali_*` residuales).
   - Purga volcados de JavaScript (`*_injected.js`), volcados de DEX y firmas intermedias (`.idsig`).
   - Limpia cachés de Gradle (`build/intermediates`) y temporales no alineados.

4. **💎 Preservación Inmutable:**
   - Conserva el árbol de código fuente limpio (`src/`), documentos personales y el artefacto activo productivo.

---

## 🚀 Instalación y Despliegue Rápido

Para instalar la CLI globalmente (`clean-project`) y como skill en Google Antigravity 2.0:

```bash
git clone https://github.com/darwinsin822/total-cleanup.git
cd total-cleanup
./scripts/install.sh
```

---

## 💻 Uso de la CLI

```bash
# 1. Saneamiento profundo del sistema (WhatsApp, Flutter, Rust, Gradle, NPM, Cache)
clean-project --deep

# 2. Limpieza completa (Sistema + Directorio actual)
clean-project --all

# 3. Limpiar el proyecto en el directorio actual
clean-project .

# 4. Limpiar un proyecto específico
clean-project /ruta/al/proyecto
```

---

## 📄 Licencia

Distribuido bajo la Licencia MIT. Consulta el archivo `LICENSE` para más información.
