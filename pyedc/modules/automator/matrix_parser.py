"""
Parseador dinámico de tablas comparativas y cheat sheets de la Base de Conocimientos EDC.
Extrae equivalencias CLI multi-vendor y catálogo IANA desde 04_MATRIZ_TABLAS_COMPARATIVAS_Y_CHEAT_SHEETS.md.
"""

import re
from typing import List, Dict, Any, Optional
from pyedc.config import CHEAT_SHEET_FILE


def clean_markdown_cell(cell: str) -> str:
    """Limpia formato Markdown de celdas (backticks, negritas, cursivas)."""
    cell = cell.strip()
    # Remover backticks `comando`
    cell = re.sub(r"`([^`]+)`", r"\1", cell)
    # Remover negritas **texto**
    cell = re.sub(r"\*\*([^*]+)\*\*", r"\1", cell)
    # Remover cursivas *texto*
    cell = re.sub(r"\*([^*]+)\*", r"\1", cell)
    return cell.strip()


def parse_cli_matrix() -> List[Dict[str, str]]:
    """
    Lee 04_MATRIZ_TABLAS_COMPARATIVAS_Y_CHEAT_SHEETS.md y extrae la matriz de equivalencias CLI.
    """
    if not CHEAT_SHEET_FILE.exists():
        return []

    content = CHEAT_SHEET_FILE.read_text(encoding="utf-8")
    lines = content.splitlines()

    matrix_rows = []
    in_cli_section = False

    for line in lines:
        line_stripped = line.strip()
        
        # Iniciar captura en sección 1
        if "## 1. Matriz Comparativa Multi-Vendor de Comandos CLI" in line_stripped:
            in_cli_section = True
            continue

        # Detener en sección 2
        if "## 2. Cheat Sheet Maestro de Subnetting" in line_stripped:
            in_cli_section = False
            break

        if in_cli_section and line_stripped.startswith("|") and not line_stripped.startswith("| :---"):
            cells = [clean_markdown_cell(c) for c in line_stripped.split("|")[1:-1]]
            
            # Encabezado estándar tiene 7 columnas
            # Tarea Operativa | Cisco | Huawei | Aruba | HP | 3Com/H3C | TP-Link
            if len(cells) >= 7 and "Tarea" not in cells[0]:
                matrix_rows.append({
                    "task": cells[0],
                    "cisco": cells[1],
                    "huawei": cells[2],
                    "aruba": cells[3],
                    "hp_procurve": cells[4],
                    "comware": cells[5],
                    "tplink": cells[6],
                })

    return matrix_rows


def parse_iana_ports() -> List[Dict[str, Any]]:
    """Extrae el catálogo de puertos IANA con análisis de riesgo y contramedidas."""
    if not CHEAT_SHEET_FILE.exists():
        return []

    content = CHEAT_SHEET_FILE.read_text(encoding="utf-8")
    lines = content.splitlines()

    ports = []
    in_port_section = False

    for line in lines:
        line_stripped = line.strip()

        if "## 3. Catálogo de Puertos IANA" in line_stripped:
            in_port_section = True
            continue

        if "## 4. Matriz Técnica de Medios Físicos" in line_stripped:
            in_port_section = False
            break

        if in_port_section and line_stripped.startswith("|") and not line_stripped.startswith("| :-"):
            cells = [clean_markdown_cell(c) for c in line_stripped.split("|")[1:-1]]
            if len(cells) >= 7 and "Puerto" not in cells[0]:
                ports.append({
                    "port": cells[0],
                    "protocol": cells[1],
                    "layer": cells[2],
                    "service": cells[3],
                    "risk_level": cells[4],
                    "threat": cells[5],
                    "mitigation": cells[6],
                })

    return ports
