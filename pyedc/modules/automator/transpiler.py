"""
Motor Transpilador de Comandos y Configuraciones Multi-Vendor (Cisco, Huawei, Aruba, HP, Comware, TP-Link).
"""

import re
from typing import Dict, List, Optional, Tuple, Any
from .matrix_parser import parse_cli_matrix
from pyedc.config import SUPPORTED_VENDORS, VENDOR_DISPLAY_NAMES


class TranspilerEngine:
    def __init__(self):
        self.matrix = parse_cli_matrix()

    def get_supported_vendors(self) -> Dict[str, str]:
        return VENDOR_DISPLAY_NAMES

    def find_matches(self, query: str, source_vendor: Optional[str] = None) -> List[Dict[str, str]]:
        """Busca coincidencias en la matriz por tarea o por comando."""
        q = query.strip().lower()
        results = []

        for row in self.matrix:
            matched = False
            if q in row["task"].lower():
                matched = True
            elif source_vendor and source_vendor in row:
                if q in row[source_vendor].lower():
                    matched = True
            else:
                for v in SUPPORTED_VENDORS:
                    if q in row.get(v, "").lower():
                        matched = True
                        break
            if matched:
                results.append(row)

        return results

    def translate_command(self, command: str, from_vendor: str, to_vendor: str) -> Dict[str, Any]:
        """
        Traduce un comando individual entre dos fabricantes.
        Maneja variables dinámicas como número de VLAN, interfaz o IPs.
        """
        from_v = from_vendor.lower()
        to_v = to_vendor.lower()

        if from_v not in SUPPORTED_VENDORS:
            raise ValueError(f"Fabricante origen '{from_vendor}' no soportado. Opciones: {list(SUPPORTED_VENDORS)}")
        if to_v not in SUPPORTED_VENDORS:
            raise ValueError(f"Fabricante destino '{to_vendor}' no soportado. Opciones: {list(SUPPORTED_VENDORS)}")

        clean_cmd = command.strip()

        # 1. Búsqueda exacta en la matriz
        for row in self.matrix:
            src_cmd = row.get(from_v, "").strip()
            if src_cmd.lower() == clean_cmd.lower():
                return {
                    "original": clean_cmd,
                    "from_vendor": VENDOR_DISPLAY_NAMES[from_v],
                    "to_vendor": VENDOR_DISPLAY_NAMES[to_v],
                    "translated": row.get(to_v, "No especificado"),
                    "task": row["task"],
                    "confidence": 1.0,
                }

        # 2. Reglas parametrizadas avanzadas (VLANs, Interfaces, LACP, Enrutamiento)
        # Asignar VLAN de acceso
        # Cisco: switchport access vlan X -> Huawei: port default vlan X -> Aruba: vlan access X
        vlan_match = re.search(r"(?:vlan\s+|access\s+vlan\s+)(\d+)", clean_cmd, re.IGNORECASE)
        if ("access" in clean_cmd.lower() or "default vlan" in clean_cmd.lower()) and vlan_match:
            vlan_id = vlan_match.group(1)
            patterns = {
                "cisco": f"switchport access vlan {vlan_id}",
                "huawei": f"port default vlan {vlan_id}",
                "aruba": f"vlan access {vlan_id}",
                "hp_procurve": f"vlan {vlan_id} untagged <port>",
                "comware": f"port default vlan {vlan_id}",
                "tplink": f"switchport access vlan {vlan_id}",
            }
            return {
                "original": clean_cmd,
                "from_vendor": VENDOR_DISPLAY_NAMES[from_v],
                "to_vendor": VENDOR_DISPLAY_NAMES[to_v],
                "translated": patterns.get(to_v, f"vlan {vlan_id}"),
                "task": f"Asignar VLAN de acceso {vlan_id}",
                "confidence": 0.95,
            }

        # Modo Troncal
        if "trunk" in clean_cmd.lower() and "allowed" not in clean_cmd.lower() and "native" not in clean_cmd.lower():
            patterns = {
                "cisco": "switchport mode trunk",
                "huawei": "port link-type trunk",
                "aruba": "no routing",  # En CX el puerto L2 permite troncales directamente
                "hp_procurve": "(Configurado mediante etiquetado 'tagged')",
                "comware": "port link-type trunk",
                "tplink": "switchport mode trunk",
            }
            return {
                "original": clean_cmd,
                "from_vendor": VENDOR_DISPLAY_NAMES[from_v],
                "to_vendor": VENDOR_DISPLAY_NAMES[to_v],
                "translated": patterns.get(to_v, "mode trunk"),
                "task": "Configurar puerto en modo troncal",
                "confidence": 0.95,
            }

        # Guardar Configuración
        if clean_cmd.lower() in ["write memory", "write", "copy run start", "save"]:
            patterns = {
                "cisco": "write memory",
                "huawei": "save",
                "aruba": "write memory",
                "hp_procurve": "write memory",
                "comware": "save",
                "tplink": "copy running-config startup-config",
            }
            return {
                "original": clean_cmd,
                "from_vendor": VENDOR_DISPLAY_NAMES[from_v],
                "to_vendor": VENDOR_DISPLAY_NAMES[to_v],
                "translated": patterns.get(to_v, "save"),
                "task": "Guardar configuración activa",
                "confidence": 1.0,
            }

        # Búsqueda difusa por token principal
        for row in self.matrix:
            src_cmd = row.get(from_v, "").strip()
            # Si el comando fuente empieza con los mismos primeros 2 tokens
            cmd_tokens = clean_cmd.lower().split()
            src_tokens = src_cmd.lower().split()
            if len(cmd_tokens) >= 2 and len(src_tokens) >= 2:
                if cmd_tokens[:2] == src_tokens[:2]:
                    return {
                        "original": clean_cmd,
                        "from_vendor": VENDOR_DISPLAY_NAMES[from_v],
                        "to_vendor": VENDOR_DISPLAY_NAMES[to_v],
                        "translated": row.get(to_v, "N/A"),
                        "task": row["task"],
                        "confidence": 0.80,
                    }

        return {
            "original": clean_cmd,
            "from_vendor": VENDOR_DISPLAY_NAMES[from_v],
            "to_vendor": VENDOR_DISPLAY_NAMES[to_v],
            "translated": f"# Sintaxis no mapeada automáticamente para: {clean_cmd}",
            "task": "Comando no catalogado",
            "confidence": 0.0,
        }

    def translate_batch(self, script_text: str, from_vendor: str, to_vendor: str) -> List[Dict[str, Any]]:
        """Traduce un bloque o archivo de configuración línea por línea."""
        lines = script_text.splitlines()
        translated_lines = []

        for line in lines:
            trimmed = line.strip()
            if not trimmed or trimmed.startswith("!") or trimmed.startswith("#"):
                translated_lines.append({
                    "original": line,
                    "translated": line,
                    "task": "Comentario / Vacío",
                    "confidence": 1.0,
                })
                continue

            res = self.translate_command(trimmed, from_vendor, to_vendor)
            translated_lines.append(res)

        return translated_lines


_engine = TranspilerEngine()


def translate_command(command: str, from_vendor: str, to_vendor: str) -> Dict[str, Any]:
    return _engine.translate_command(command, from_vendor, to_vendor)


def translate_batch(script_text: str, from_vendor: str, to_vendor: str) -> List[Dict[str, Any]]:
    return _engine.translate_batch(script_text, from_vendor, to_vendor)


def get_supported_vendors() -> Dict[str, str]:
    return _engine.get_supported_vendors()


def find_equivalent_task(query: str, source_vendor: Optional[str] = None) -> List[Dict[str, str]]:
    return _engine.find_matches(query, source_vendor)
