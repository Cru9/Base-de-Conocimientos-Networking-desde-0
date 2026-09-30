"""
Configuración central y rutas maestras del ecosistema PyEDC.
"""

from pathlib import Path
import sys

# Directorio raíz del repositorio Base de Conocimientos EDC
BASE_DIR = Path(__file__).resolve().parent.parent

# Rutas clave de contenido
WIKI_DIR = BASE_DIR / "WIKI_EDC"
MODULOS_DIR = BASE_DIR / "Modulos_Clasificados"
CHEAT_SHEET_FILE = BASE_DIR / "04_MATRIZ_TABLAS_COMPARATIVAS_Y_CHEAT_SHEETS.md"
GLOSSARY_FILE = BASE_DIR / "02_DICCIONARIO_DEFINICIONES_Y_GLOSARIO_TECNICO.md"
BIBLIO_FILE = BASE_DIR / "03_BIBLIOTECA_DOCUMENTAL_Y_RECURSOS_OFICIALES.md"
ARCH_FILE = BASE_DIR / "01_ARQUITECTURA_Y_MAPA_GLOBAL_EDC.md"

# Directorio para almacenar caché o exportaciones
DATA_DIR = BASE_DIR / "pyedc" / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Fabricantes soportados en la matriz multi-vendor
SUPPORTED_VENDORS = [
    "cisco",
    "huawei",
    "aruba",
    "hp_procurve",
    "comware",
    "tplink",
]

VENDOR_DISPLAY_NAMES = {
    "cisco": "Cisco IOS / IOS-XE",
    "huawei": "Huawei VRP",
    "aruba": "Aruba ArubaOS-CX",
    "hp_procurve": "HP ProCurve (AOS-S)",
    "comware": "3Com / H3C Comware",
    "tplink": "TP-Link JetStream",
}
