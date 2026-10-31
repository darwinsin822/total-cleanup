---
name: total-cleanup
description: >-
  Ultra-aggressive cleanup and storage optimizer for any project.
  Activate whenever the user says "optimizar", "limpiar", "limpieza", or requests
  to clean up workspace files. PURGES all previous APK versions, obsolete source code
  from earlier versions, temporary extraction folders, intermediate builds, and caches,
  leaving STRICTLY the latest active version of the project to minimize RAM and storage usage.
---

# 🧹 Total Cleanup — Limpiador Ultra Agresivo de Proyectos

Skill universal de optimización extrema de almacenamiento y purga de residuos para proyectos de software en Linux Mint / Google Antigravity 2.0 2.0. Se activa automáticamente con la palabra **"optimizar"** o ante cualquier solicitud de limpieza profunda.

---

## ⚡ Directivas Ultra Agresivas
1. **Purga de Versiones Anteriores:**
   - Detecta versiones previas de paquetes y binarios (`.apk`, `.deb`, `.AppImage`, etc.).
   - Conserva estrictamente **únicamente el artefacto de la versión más reciente**.
2. **Eliminación de Código y Descompilaciones Obsoletas:**
   - Purga scripts temporales de versiones antiguas (`build_v*.py`, `patch_injected.js`).
   - Elimina carpetas de descompilación temporal (`apk_extracted/`, carpetas `smali_*` residuales).
   - Elimina volcados intermedios, caches de compiladores y firmas no alineadas.
3. **Preservación Inmutable:**
   - Mantiene intacto el árbol de código fuente limpio activo y el artefacto productivo final.

---

## 🚀 Uso y Ejecución

```bash
# Limpiar el proyecto actual
clean-project .

# Limpiar una ruta específica
clean-project /ruta/al/proyecto
```
