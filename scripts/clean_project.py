#!/usr/bin/env python3
"""
clean_project.py - Limpiador Ultra Agresivo de Proyectos (DarwinSin)
Elimina sistemáticamente:
 1. Todas las versiones anteriores de APKs (en el proyecto y en ~/Descargas/).
 2. Scripts, parches y códigos fuente de versiones pasadas.
 3. Carpetas de descompilación temporal, cachés, volcados y archivos no alineados.
Deja ÚNICAMENTE la versión actual más reciente y el árbol de código activo.
"""

import os
import sys
import glob
import re
import shutil

def get_dir_size(path):
    total = 0
    if os.path.isfile(path) or os.path.islink(path):
        return os.path.getsize(path)
    for root, dirs, files in os.walk(path):
        for f in files:
            fp = os.path.join(root, f)
            if not os.path.islink(fp) and os.path.exists(fp):
                total += os.path.getsize(fp)
    return total

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

def clean_project(target_dir):
    target_dir = os.path.abspath(target_dir)
    if not os.path.exists(target_dir):
        print(f"Error: Directorio no existe: {target_dir}")
        return

    print(f"🔥 INICIANDO LIMPIEZA TOTAL ULTRA AGRESIVA EN: {target_dir}")
    freed_bytes = 0
    removed_items = []
    preserved_items = []

    # Determinar prefijo del proyecto
    dir_name = os.path.basename(target_dir)
    prefix_match = re.match(r'^([a-zA-Z0-9]+(?:-[a-zA-Z0-9]+)*?)(?:-v?\d+.*)?$', dir_name)
    project_prefix = prefix_match.group(1).split('-')[0] if prefix_match else dir_name

    descargas_dir = os.path.expanduser("~/Descargas")

    # ─────────────────────────────────────────────────────────────────────────
    # 1. PURGA AGRESIVA DE PAQUETES ANTIGUOS (.apk, .deb, .AppImage)
    # ─────────────────────────────────────────────────────────────────────────
    package_extensions = ["*.apk", "*.deb", "*.AppImage"]
    
    for ext in package_extensions:
        local_pkgs = glob.glob(os.path.join(target_dir, ext))
        descargas_pkgs = []
        if os.path.exists(descargas_dir):
            descargas_pkgs = glob.glob(os.path.join(descargas_dir, f"{project_prefix}*{ext[1:]}"))
            if not descargas_pkgs and '-' in dir_name:
                alt_prefix = dir_name.split('-')[0]
                descargas_pkgs = glob.glob(os.path.join(descargas_dir, f"{alt_prefix}*{ext[1:]}"))

        all_pkgs = list(set(local_pkgs + descargas_pkgs))
        if not all_pkgs:
            continue

        if ext == "*.apk":
            aligned_apks = [a for a in all_pkgs if "unaligned" not in a.lower()]
            candidates = aligned_apks if aligned_apks else all_pkgs
        else:
            candidates = all_pkgs

        # Ordenar por versión semántica y fecha de modificación
        candidates.sort(key=lambda f: (extract_version_tuple(os.path.basename(f)), os.path.getmtime(f)))
        latest_pkg = candidates[-1]
        latest_name = os.path.basename(latest_pkg)
        preserved_items.append(f"{latest_name} ({format_size(get_dir_size(latest_pkg))})")

        # Eliminar versiones obsoletas
        for pkg in all_pkgs:
            if os.path.abspath(pkg) != os.path.abspath(latest_pkg):
                sz = get_dir_size(pkg)
                freed_bytes += sz
                try:
                    os.remove(pkg)
                    removed_items.append(f"Paquete anterior: {os.path.basename(pkg)} ({format_size(sz)})")
                except OSError as e:
                    print(f"Error al eliminar {pkg}: {e}")

                # Eliminar firma .asc asociada si existe
                asc_file = pkg + ".asc"
                if os.path.exists(asc_file):
                    asc_sz = get_dir_size(asc_file)
                    freed_bytes += asc_sz
                    try:
                        os.remove(asc_file)
                        removed_items.append(f"Firma obsoleta: {os.path.basename(asc_file)} ({format_size(asc_sz)})")
                    except OSError:
                        pass

    # ─────────────────────────────────────────────────────────────────────────
    # 2. PURGA DE ESPACIOS DE TRABAJO REDUNDANTES PREVIOS EN SCRATCH
    # ─────────────────────────────────────────────────────────────────────────
    parent_dir = os.path.dirname(target_dir)
    if os.path.basename(parent_dir) == "scratch" or "scratch" in target_dir:
        for sibling in glob.glob(os.path.join(parent_dir, f"{project_prefix}*")):
            if os.path.isdir(sibling) and os.path.abspath(sibling) != os.path.abspath(target_dir):
                sib_name = os.path.basename(sibling)
                sib_ver = extract_version_tuple(sib_name)
                target_ver = extract_version_tuple(dir_name)
                if sib_ver <= target_ver and sib_name != dir_name:
                    sz = get_dir_size(sibling)
                    freed_bytes += sz
                    try:
                        shutil.rmtree(sibling)
                        removed_items.append(f"Workspace previo redundante: {sib_name} ({format_size(sz)})")
                    except OSError as e:
                        print(f"Error al eliminar {sibling}: {e}")

    # ─────────────────────────────────────────────────────────────────────────
    # 3. PURGA DE CÓDIGO FUENTE Y SCRIPTS DE VERSIONES PASADAS
    # ─────────────────────────────────────────────────────────────────────────
    build_scripts = glob.glob(os.path.join(target_dir, "build_*.py"))
    if build_scripts:
        build_scripts.sort(key=lambda f: (extract_version_tuple(os.path.basename(f)), os.path.getmtime(f)))
        latest_build_script = build_scripts[-1]
        for script in build_scripts:
            if script != latest_build_script:
                sz = get_dir_size(script)
                freed_bytes += sz
                try:
                    os.remove(script)
                    removed_items.append(f"Script de versión anterior: {os.path.basename(script)} ({format_size(sz)})")
                except OSError:
                    pass

    intermediate_patterns = [
        # Carpetas descompiladas y temporales
        "apk_extracted", "apktool_out*",
        # Archivos APK intermedios y firmas
        "*unaligned*.apk", "*unsigned*.apk", "*.idsig",
        # Residuos de compilación DEX y manifiestos intermedios
        "classes*_patched.dex", "AndroidManifest_*.xml", "*.dex.dump", "*.ap_",
        # Scripts temporales de pruebas y parches obsoletos
        "test_*.py", "apply_patch.py", "patch_*.py", "build_js.py",
        # JS intermedios volcados
        "*_injected.js", "original_injected.js", "test_*.js",
        # Backups y códigos obsoletos
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

    # ─────────────────────────────────────────────────────────────────────────
    # 3. LIMPIEZA DE CACHÉS DE DESARROLLO (Python, Gradle, Node, etc.)
    # ─────────────────────────────────────────────────────────────────────────
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
            if os.path.isdir(match):
                shutil.rmtree(match)
            else:
                os.remove(match)
            removed_items.append(f"{os.path.relpath(match, target_dir)} ({format_size(sz)})")

    # ─────────────────────────────────────────────────────────────────────────
    # 4. REPORTE FINAL DE LIMPIEZA
    # ─────────────────────────────────────────────────────────────────────────
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

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    clean_project(target)
