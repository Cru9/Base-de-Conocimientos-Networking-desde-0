"""
Lanzador universal de PyEDC - Enterprise Data & Connectivity Suite.
Ejecuta: python run.py (Configura automáticamente el entorno si es necesario).
"""

import sys
import os
import subprocess
from pathlib import Path

# Configurar codificación UTF-8 en Windows
if sys.platform.startswith("win"):
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")
        if hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Asegurar que el directorio raíz esté en sys.path
root_dir = Path(__file__).resolve().parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))


def ensure_environment():
    """
    Verifica si las librerías necesarias están instaladas.
    Si no están disponibles, crea el entorno virtual .venv e instala las librerías automáticamente.
    """
    try:
        import rich
        import pydantic
        import jinja2
        import yaml
        return True
    except ImportError:
        pass

    venv_dir = root_dir / ".venv"
    if sys.platform.startswith("win"):
        venv_python = venv_dir / "Scripts" / "python.exe"
    else:
        venv_python = venv_dir / "bin" / "python"

    print("\n" + "=" * 65)
    print(" 🏛️ PyEDC - Configuración Automática de Entorno")
    print("=" * 65)

    # 1. Crear .venv si no existe
    if not venv_python.exists():
        print("\n[1/2] Creando entorno virtual aislado (.venv)...")
        try:
            subprocess.check_call([sys.executable, "-m", "venv", str(venv_dir)])
            print("[OK] Entorno virtual creado exitosamente.")
        except Exception as e:
            print(f"[ERROR] No se pudo crear el entorno virtual: {e}")
            sys.exit(1)

    # 2. Instalar dependencias en el .venv
    req_file = root_dir / "requirements.txt"
    if req_file.exists():
        print("\n[2/2] Instalando librerías requeridas (Rich, Pydantic, etc.)...")
        try:
            subprocess.check_call([str(venv_python), "-m", "pip", "install", "-r", str(req_file), "--quiet"])
            print("[OK] Librerías instaladas correctamente.")
        except Exception as e:
            print(f"[ERROR] No se pudieron instalar las dependencias: {e}")
            sys.exit(1)

    # 3. Relanzar el programa con el Python del entorno virtual
    print("\n[OK] Entorno preparado. Iniciando la aplicación...\n")
    ret = subprocess.call([str(venv_python), str(Path(__file__).resolve())] + sys.argv[1:])
    sys.exit(ret)


if __name__ == "__main__":
    ensure_environment()
    from pyedc.cli import main
    main()
