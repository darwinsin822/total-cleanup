#!/usr/bin/env python3
"""
clean_project.py - Limpiador Ultra Agresivo de Proyectos y Sistema con Motor de Diagnóstico Baobab (DarwinSin)
Elimina sistemáticamente:
 1. Todas las versiones anteriores de APKs (en el proyecto y en ~/Descargas/).
 2. Scripts, parches y códigos fuente de versiones pasadas.
 3. Carpetas de descompilación temporal, cachés, volcados y archivos no alineados.
 4. Mantenimiento Profundo de Sistema:
    - Caché multimedia/HTTP de WhatsApp Web (ICE) y WhatsApp Flatpak (preserva chats y sesiones).
    - Cachés de Flutter/Dart (~/.pub-cache).
    - Cachés de Rust (~/.cargo/registry/src y cache).
    - Cachés de Gradle, NPM, pip y miniaturas del sistema.
    - Cachés de OpenCode (Desktop y CLI).
    - Cachés de navegadores (Chrome y Brave: CRX, Shaders, Service Workers).
 5. Analizador de Disco Estilo Baobab:
    - Diagnóstico de árbol jerárquico de almacenamiento, cálculo de porcentajes y detección automática de carpetas limpiables.
"""

import os
import sys
import glob
import re
import shutil
import subprocess

def get_dir_size_and_count(path):
    total_size = 0
    total_items = 0
    if os.path.isfile(path) or os.path.islink(path):
        try:
            return os.path.getsize(path), 1
        except OSError:
            return 0, 0
    for root, dirs, files in os.walk(path):
        for f in files:
            fp = os.path.join(root, f)
            if not os.path.islink(fp) and os.path.exists(fp):
                try:
                    total_size += os.path.getsize(fp)
                    total_items += 1
                except OSError:
                    pass
        total_items += len(dirs)
    return total_size, total_items

def get_dir_size(path):
    sz, _ = get_dir_size_and_count(path)
    return sz

def format_size(bytes_size):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} TB"

def extract_version_tuple(filename):
    """Extrae tupla numérica de versión para ordenamiento semántico."""
    nums = [int(n) for n in re.findall(r'\d+', filename)]
    return tuple(nums) if nums else (0,)

def purge_path_or_contents(target_path, only_contents=False):
    """Elimina de forma segura un archivo, carpeta o los contenidos de una carpeta."""
    freed = 0
    expanded_paths = glob.glob(os.path.expanduser(target_path))
    for p in expanded_paths:
        if not os.path.exists(p):
            continue
        if only_contents and os.path.isdir(p):
            for item in os.listdir(p):
                item_path = os.path.join(p, item)
                sz = get_dir_size(item_path)
                try:
                    if os.path.isdir(item_path) and not os.path.islink(item_path):
                        shutil.rmtree(item_path)
                    else:
                        os.remove(item_path)
                    freed += sz
                except OSError:
                    pass
        else:
            sz = get_dir_size(p)
            try:
                if os.path.isdir(p) and not os.path.islink(p):
                    shutil.rmtree(p)
                else:
                    os.remove(p)
                freed += sz
            except OSError:
                pass
    return freed

def analyze_disk_baobab(target_dir=None):
    """Escanea y despliega el árbol de almacenamiento al estilo del Analizador de Disco de Linux Mint (Baobab)."""
    target = os.path.abspath(os.path.expanduser(target_dir)) if target_dir else os.path.expanduser("~")
    print(f"📊 EJECUTANDO ANÁLISIS DE DISCO (Motor Baobab) EN: {target}\n")

    # Lista de categorías prioritarias identificadas por Baobab
    core_targets = [
        "Música", ".local", "Rimarc", "Documentos", ".config", ".var",
        "Android", "AndroidModLab", "AndroidUISkinLab", ".icons",
        "AndroidMagic", ".gradle", ".nvm", ".gemini", ".rustup",
        ".cache", ".npm", ".cargo", ".pub-cache", "Descargas", "Vídeos", "Imágenes"
    ]

    entries = []
    total_scanned_bytes = 0

    # Escanear cada ruta de forma rápida
    for item in core_targets:
        item_path = os.path.join(target, item)
        if not os.path.exists(item_path):
            continue
        try:
            out = subprocess.check_output(["du", "-sk", item_path], stderr=subprocess.DEVNULL).decode().strip()
            sz_kb = int(out.split()[0])
            sz = sz_kb * 1024
        except Exception:
            sz = get_dir_size(item_path)

        if sz > 0:
            total_scanned_bytes += sz
            entries.append({
                "name": item,
                "path": item_path,
                "size": sz,
                "is_dir": os.path.isdir(item_path)
            })

    entries.sort(key=lambda x: x["size"], reverse=True)

    header = f"{'Carpeta / Archivo':<22} | {'Tamaño':<10} | {'% Uso':<7} | {'Diagnóstico / Acción'}"
    print(header)
    print("-" * len(header))

    reclaimable_potencial = 0

    for e in entries:
        pct = (e["size"] / total_scanned_bytes * 100) if total_scanned_bytes > 0 else 0
        name = e["name"]
        sz_str = format_size(e["size"])

        # Diagnóstico inteligente de la carpeta
        rec = "Conservar (Datos de usuario)"
        if name in [".cache", ".npm", ".gradle"]:
            rec = "🧹 Limpiable (Caché de desarrollo/sistema)"
            reclaimable_potencial += e["size"] * 0.75
        elif name in [".pub-cache", ".cargo"]:
            rec = "🧹 Depurable (Registro de paquetes descargados)"
            reclaimable_potencial += e["size"] * 0.60
        elif name in ["Rimarc", "mintplayer", "Orpheon"]:
            rec = "⚡ Proyecto activo (Limpiable con clean-project)"
            reclaimable_potencial += e["size"] * 0.40
        elif name in [".var", ".local"]:
            rec = "⚙️ Runtimes y perfiles (Cachés de apps limpiables)"
            reclaimable_potencial += e["size"] * 0.20
        elif name in ["Documentos", "Música", "Imágenes", "Vídeos"]:
            rec = "💎 Archivos personales (Inmutable)"
        elif name.startswith("Android"):
            rec = "📱 Entorno Android / Laboratorio"

        if pct >= 0.5 or e["size"] >= (50 * 1024 * 1024):
            print(f"{name:<22} | {sz_str:<10} | {pct:>5.1f}% | {rec}")

    print("-" * len(header))
    print(f"📦 Total analizado en directorio: {format_size(total_scanned_bytes)}")
    if reclaimable_potencial > 0:
        print(f"💡 Espacio estimado potencialmente recuperable: ~{format_size(reclaimable_potencial)}")
    print("\nPara ejecutar la limpieza profunda automatizada ejecuta: clean-project --deep")

def clean_system_deep():
    """Ejecuta el saneamiento y mantenimiento profundo del sistema."""
    print("🔥 INICIANDO MANTENIMIENTO PROFUNDO DEL SISTEMA (Total Cleanup)")
    freed_bytes = 0
    results = []

    # 1. WhatsApp (ICE SSB & Flatpak) - Solo cachés, nunca sesiones ni idb
    wa_ice_cache = purge_path_or_contents("~/.local/share/ice/firefox/Whatsaap*/storage/default/https+++web.whatsapp.com/cache", only_contents=True)
    wa_flatpak_cache = purge_path_or_contents("~/.var/app/com.github.eneshecan.WhatsAppForLinux/cache/whatsapp-for-linux", only_contents=True)
    wa_total = wa_ice_cache + wa_flatpak_cache
    freed_bytes += wa_total
    if wa_total > 0:
        results.append(f"Caché de WhatsApp (ICE + Flatpak): {format_size(wa_total)} (Sesiones y chats protegidos)")

    # 2. Flutter / Dart (~/.pub-cache)
    pub_freed = purge_path_or_contents("~/.pub-cache/hosted", only_contents=True) + purge_path_or_contents("~/.pub-cache/git", only_contents=True)
    freed_bytes += pub_freed
    if pub_freed > 0:
        results.append(f"Caché de Flutter/Dart (~/.pub-cache): {format_size(pub_freed)}")

    # 3. Rust / Cargo Registry (~/.cargo/registry)
    cargo_freed = purge_path_or_contents("~/.cargo/registry/src", only_contents=True) + purge_path_or_contents("~/.cargo/registry/cache", only_contents=True)
    freed_bytes += cargo_freed
    if cargo_freed > 0:
        results.append(f"Caché de Rust/Cargo (~/.cargo/registry): {format_size(cargo_freed)}")

    # 4. Node / NPM Caches
    npm_freed = purge_path_or_contents("~/.npm/_cacache", only_contents=True) + purge_path_or_contents("~/.npm/_prebuilds", only_contents=True) + purge_path_or_contents("~/.npm/_npx", only_contents=True)
    freed_bytes += npm_freed
    if npm_freed > 0:
        results.append(f"Caché de Node/NPM (~/.npm): {format_size(npm_freed)}")

    # 5. Gradle Global Caches
    gradle_freed = purge_path_or_contents("~/.gradle/caches", only_contents=True) + purge_path_or_contents("~/.gradle/daemon", only_contents=True)
    freed_bytes += gradle_freed
    if gradle_freed > 0:
        results.append(f"Caché de Gradle (~/.gradle): {format_size(gradle_freed)}")

    # 6. Miniaturas, instaladores y cachés de usuario
    user_cache_freed = (
        purge_path_or_contents("~/.cache/thumbnails", only_contents=True) +
        purge_path_or_contents("~/.cache/@opencodedesktop-updater", only_contents=True) +
        purge_path_or_contents("~/.cache/mintinstall", only_contents=True) +
        purge_path_or_contents("~/.cache/pip", only_contents=True) +
        purge_path_or_contents("~/.cache/google-chrome/Default/Cache", only_contents=True) +
        purge_path_or_contents("~/.cache/google-chrome/Default/Code Cache", only_contents=True)
    )
    freed_bytes += user_cache_freed
    if user_cache_freed > 0:
        results.append(f"Caché de usuario (~/.cache / Chrome / Miniaturas): {format_size(user_cache_freed)}")

    # 7. Cachés de Navegadores (Chrome & Brave: CRX, Shaders, Service Workers)
    browser_cache_freed = (
        purge_path_or_contents("~/.config/google-chrome/extensions_crx_cache", only_contents=True) +
        purge_path_or_contents("~/.config/google-chrome/component_crx_cache", only_contents=True) +
        purge_path_or_contents("~/.config/google-chrome/GrShaderCache", only_contents=True) +
        purge_path_or_contents("~/.config/google-chrome/*/Service Worker/CacheStorage", only_contents=True) +
        purge_path_or_contents("~/.config/BraveSoftware/Brave-Origin-Nightly/extensions_crx_cache", only_contents=True) +
        purge_path_or_contents("~/.config/BraveSoftware/Brave-Origin-Nightly/component_crx_cache", only_contents=True) +
        purge_path_or_contents("~/.config/BraveSoftware/Brave-Origin-Nightly/GrShaderCache", only_contents=True) +
        purge_path_or_contents("~/.config/BraveSoftware/Brave-Origin-Nightly/*/Service Worker/CacheStorage", only_contents=True)
    )
    freed_bytes += browser_cache_freed
    if browser_cache_freed > 0:
        results.append(f"Cachés de navegadores (Chrome/Brave CRX & Service Workers): {format_size(browser_cache_freed)}")

    # 8. OpenCode (Desktop / CLI Caches, Logs, Snapshots, Backups)
    opencode_freed = (
        purge_path_or_contents("~/.config/ai.opencode.desktop/Cache", only_contents=True) +
        purge_path_or_contents("~/.config/ai.opencode.desktop/Code Cache", only_contents=True) +
        purge_path_or_contents("~/.config/ai.opencode.desktop/compile-cache", only_contents=True) +
        purge_path_or_contents("~/.config/ai.opencode.desktop/GPUCache", only_contents=True) +
        purge_path_or_contents("~/.config/ai.opencode.desktop/GPUPersistentCache", only_contents=True) +
        purge_path_or_contents("~/.config/ai.opencode.desktop/DawnGraphiteCache", only_contents=True) +
        purge_path_or_contents("~/.config/ai.opencode.desktop/DawnWebGPUCache", only_contents=True) +
        purge_path_or_contents("~/.config/ai.opencode.desktop/Crashpad", only_contents=True) +
        purge_path_or_contents("~/.config/ai.opencode.desktop/logs", only_contents=True) +
        purge_path_or_contents("~/.local/share/opencode/log", only_contents=True) +
        purge_path_or_contents("~/.local/share/opencode/snapshot", only_contents=True) +
        purge_path_or_contents("~/.cache/opencode-wallpaper", only_contents=True) +
        purge_path_or_contents("~/.config/opencode/*.bak*", only_contents=False) +
        purge_path_or_contents("~/.gentle-ai/cache/opencode-v2", only_contents=True)
    )
    freed_bytes += opencode_freed
    if opencode_freed > 0:
        results.append(f"Caché y logs de OpenCode: {format_size(opencode_freed)} (Base de datos y configuraciones protegidas)")

    print(f"\n⚡ MANTENIMIENTO PROFUNDO FINALIZADO")
    print(f"🗑️  Espacio total liberado en sistema: {format_size(freed_bytes)}")
    for r in results:
        print(f"   ✅ {r}")

    return freed_bytes

def clean_project(target_dir):
    target_dir = os.path.abspath(target_dir)
    if not os.path.exists(target_dir):
        print(f"Error: Directorio no existe: {target_dir}")
        return 0

    print(f"🔥 INICIANDO LIMPIEZA TOTAL ULTRA AGRESIVA EN: {target_dir}")
    freed_bytes = 0
    removed_items = []

    # Determinar prefijo del proyecto
    dir_name = os.path.basename(target_dir)
    prefix_match = re.match(r'^([a-zA-Z0-9]+(?:-[a-zA-Z0-9]+)*?)(?:-v?\d+.*)?$', dir_name)
    project_prefix = prefix_match.group(1).split('-')[0] if prefix_match else dir_name

    descargas_dir = os.path.expanduser("~/Descargas")

    # 1. PURGA AGRESIVA DE PAQUETES ANTIGUOS (.apk, .deb, .AppImage)
    locations = [target_dir]
    if os.path.exists(descargas_dir):
        locations.append(descargas_dir)

    for loc in locations:
        for ext in ["apk", "deb", "AppImage"]:
            pattern = os.path.join(loc, f"*{project_prefix}*.{ext}")
            packages = glob.glob(pattern)
            if not packages:
                continue

            packages_with_versions = []
            for pkg in packages:
                fname = os.path.basename(pkg)
                v_tuple = extract_version_tuple(fname)
                packages_with_versions.append((v_tuple, pkg))

            packages_with_versions.sort(key=lambda x: x[0])

            if len(packages_with_versions) > 1:
                obsolete_packages = packages_with_versions[:-1]
                for _, pkg_path in obsolete_packages:
                    sz = get_dir_size(pkg_path)
                    freed_bytes += sz
                    try:
                        os.remove(pkg_path)
                        removed_items.append(f"{os.path.basename(pkg_path)} ({format_size(sz)})")
                    except OSError:
                        pass

    # 2. PURGA DE ARCHIVOS INTERMEDIOS Y DESCOMPILACIONES RESIDUALES
    intermediate_patterns = [
        "apk_extracted*", "build_extracted*", "temp_unaligned*",
        "smali_patch*", "smali_*_bak", "apk_decompiled*",
        "*unaligned*.apk", "*unsigned*.apk", "*.idsig",
        "classes*_patched.dex", "AndroidManifest_*.xml", "*.dex.dump", "*.ap_",
        "test_*.py", "apply_patch.py", "patch_*.py", "build_js.py",
        "*_injected.js", "original_injected.js", "test_*.js",
        "*_old", "*_bak", "*.bak", "*.old", "backup*", "src_old", "src_v*"
    ]

    for pattern in intermediate_patterns:
        for match in glob.glob(os.path.join(target_dir, pattern)):
            sz = get_dir_size(match)
            freed_bytes += sz
            try:
                if os.path.isdir(match):
                    shutil.rmtree(match)
                else:
                    os.remove(match)
                removed_items.append(f"{os.path.basename(match)} ({format_size(sz)})")
            except OSError:
                pass

    # 3. LIMPIEZA DE CACHÉS DE DESARROLLO (Python, Gradle, Node, etc.)
    general_clean_patterns = [
        "__pycache__", "*.pyc", ".pytest_cache", ".mypy_cache",
        "build/intermediates", ".gradle/caches", ".gradle/daemon",
        ".parcel-cache", ".next/cache", ".turbo", ".eslintcache",
        "*.tmp", "*.temp", "*.log"
    ]

    for pattern in general_clean_patterns:
        for match in glob.glob(os.path.join(target_dir, "**", pattern), recursive=True):
            sz = get_dir_size(match)
            freed_bytes += sz
            try:
                if os.path.isdir(match):
                    shutil.rmtree(match)
                else:
                    os.remove(match)
                removed_items.append(f"{os.path.relpath(match, target_dir)} ({format_size(sz)})")
            except OSError:
                pass

    # 4. REPORTE FINAL DE LIMPIEZA
    print(f"\n⚡ LIMPIEZA ULTRA AGRESIVA FINALIZADA")
    print(f"🗑️  Espacio total liberado: {format_size(freed_bytes)}")
    if removed_items:
        print(f"🔥 Elementos eliminados ({len(removed_items)}):")
        for item in removed_items[:12]:
            print(f"   ❌ {item}")
        if len(removed_items) > 12:
            print(f"   ... y {len(removed_items) - 12} elementos más.")

    remaining = [f for f in os.listdir(target_dir) if not f.startswith('.')]
    print(f"\n💎 ÚNICA VERSIÓN CONSERVADA PARA TRABAJAR ({len(remaining)} elementos):")
    for f in remaining:
        fp = os.path.join(target_dir, f)
        sz = format_size(get_dir_size(fp))
        print(f"   ✅ {f} [{sz}]")

    return freed_bytes

if __name__ == "__main__":
    args = sys.argv[1:]
    if any(arg in ["--baobab", "--analyze", "--scan", "-scan", "analyze", "baobab"] for arg in args):
        target = next((a for a in args if not a.startswith("-") and a not in ["analyze", "baobab"]), None)
        analyze_disk_baobab(target)
    elif not args or args[0] in [".", ""]:
        clean_project(os.getcwd())
    elif any(arg in ["--system", "--deep", "system", "deep", "-s"] for arg in args):
        clean_system_deep()
    elif any(arg in ["--all", "-a"] for arg in args):
        clean_system_deep()
        clean_project(os.getcwd())
    else:
        clean_project(args[0])
