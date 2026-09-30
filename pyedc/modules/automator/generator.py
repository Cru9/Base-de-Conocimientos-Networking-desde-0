"""
Generador de configuraciones de red parametrizadas multi-fabricante para PyEDC.
"""

from typing import Dict, Any, List
from pydantic import BaseModel, Field


class TemplateTask(BaseModel):
    task_type: str = Field(description="Tipo de tarea: vlan, access_port, trunk_port, lacp, ospf")
    vendor: str = Field(default="cisco", description="Fabricante objetivo")
    params: Dict[str, Any] = Field(default_factory=dict)


def generate_vlan_config(vendor: str, vlan_id: int, name: str, svi_ip: str = None, svi_mask: str = None) -> str:
    """Genera la configuración para crear una VLAN y opcionalmente su SVI."""
    v = vendor.lower()
    
    if v == "cisco":
        cfg = [f"vlan {vlan_id}", f" name {name}", "exit"]
        if svi_ip and svi_mask:
            cfg.extend([f"interface Vlan{vlan_id}", f" ip address {svi_ip} {svi_mask}", " no shutdown", "exit"])
        return "\n".join(cfg)

    elif v == "huawei":
        cfg = [f"vlan {vlan_id}", f" description {name}", "quit"]
        if svi_ip and svi_mask:
            cfg.extend([f"interface Vlanif{vlan_id}", f" ip address {svi_ip} {svi_mask}", "undo shutdown", "quit"])
        return "\n".join(cfg)

    elif v == "aruba":
        cfg = [f"vlan {vlan_id}", f" name {name}", "exit"]
        if svi_ip and svi_mask:
            cfg.extend([f"interface vlan {vlan_id}", f" ip address {svi_ip}/{svi_mask}", "no shutdown", "exit"])
        return "\n".join(cfg)

    elif v == "hp_procurve":
        cfg = [f"vlan {vlan_id}", f" name \"{name}\""]
        if svi_ip and svi_mask:
            cfg.append(f" ip address {svi_ip} {svi_mask}")
        cfg.append("exit")
        return "\n".join(cfg)

    elif v == "comware":
        cfg = [f"vlan {vlan_id}", f" description {name}", "quit"]
        if svi_ip and svi_mask:
            cfg.extend([f"interface Vlan-interface{vlan_id}", f" ip address {svi_ip} {svi_mask}", "quit"])
        return "\n".join(cfg)

    elif v == "tplink":
        cfg = [f"vlan {vlan_id}", f" name {name}", "exit"]
        if svi_ip and svi_mask:
            cfg.extend([f"interface vlan {vlan_id}", f" ip address {svi_ip} {svi_mask}", "no shutdown", "exit"])
        return "\n".join(cfg)

    return f"# Fabricante '{vendor}' no soportado para plantilla VLAN."


def generate_access_port_config(vendor: str, interface: str, vlan_id: int, enable_portfast: bool = True, enable_bpduguard: bool = True) -> str:
    """Genera la configuración de un puerto de acceso seguro para usuario final."""
    v = vendor.lower()

    if v == "cisco":
        cfg = [
            f"interface {interface}",
            " switchport mode access",
            f" switchport access vlan {vlan_id}",
            " switchport nonegotiate",
        ]
        if enable_portfast:
            cfg.append(" spanning-tree portfast")
        if enable_bpduguard:
            cfg.append(" spanning-tree bpduguard enable")
        cfg.extend([" no shutdown", "exit"])
        return "\n".join(cfg)

    elif v == "huawei":
        cfg = [
            f"interface {interface}",
            " port link-type access",
            f" port default vlan {vlan_id}",
        ]
        if enable_portfast:
            cfg.append(" stp edged-port enable")
        if enable_bpduguard:
            cfg.append(" stp bpdu-protection")
        cfg.extend([" undo shutdown", "quit"])
        return "\n".join(cfg)

    elif v == "aruba":
        cfg = [
            f"interface {interface}",
            " no routing",
            f" vlan access {vlan_id}",
        ]
        if enable_portfast:
            cfg.append(" spanning-tree port-type admin-edge")
        if enable_bpduguard:
            cfg.append(" spanning-tree bpdu-guard")
        cfg.extend([" no shutdown", "exit"])
        return "\n".join(cfg)

    elif v == "hp_procurve":
        cfg = [
            f"vlan {vlan_id} untagged {interface}",
        ]
        if enable_portfast:
            cfg.append(f"spanning-tree {interface} admin-edge-port")
        if enable_bpduguard:
            cfg.append(f"spanning-tree {interface} bpdu-filter")
        return "\n".join(cfg)

    elif v == "comware":
        cfg = [
            f"interface {interface}",
            " port link-type access",
            f" port default vlan {vlan_id}",
        ]
        if enable_portfast:
            cfg.append(" stp edged-port enable")
        if enable_bpduguard:
            cfg.append(" stp bpdu-protection")
        cfg.append("quit")
        return "\n".join(cfg)

    elif v == "tplink":
        cfg = [
            f"interface {interface}",
            " switchport mode access",
            f" switchport access vlan {vlan_id}",
        ]
        if enable_portfast:
            cfg.append(" spanning-tree portfast")
        if enable_bpduguard:
            cfg.append(" spanning-tree bpdu-guard")
        cfg.extend([" no shutdown", "exit"])
        return "\n".join(cfg)

    return f"# Fabricante '{vendor}' no soportado para plantilla puerto de acceso."


def generate_trunk_port_config(vendor: str, interface: str, allowed_vlans: str, native_vlan: int = 99) -> str:
    """Genera la configuración de un puerto troncal seguro."""
    v = vendor.lower()

    if v == "cisco":
        return "\n".join([
            f"interface {interface}",
            " switchport mode trunk",
            f" switchport trunk allowed vlan {allowed_vlans}",
            f" switchport trunk native vlan {native_vlan}",
            " no shutdown",
            "exit",
        ])

    elif v == "huawei":
        # Huawei usa espacios en vez de comas para vlan permitidas: 10 20 30
        hw_vlans = allowed_vlans.replace(",", " ")
        return "\n".join([
            f"interface {interface}",
            " port link-type trunk",
            f" port trunk allow-pass vlan {hw_vlans}",
            f" port trunk pvid vlan {native_vlan}",
            " undo shutdown",
            "quit",
        ])

    elif v == "aruba":
        return "\n".join([
            f"interface {interface}",
            " no routing",
            f" vlan trunk allowed {allowed_vlans}",
            f" vlan trunk native {native_vlan}",
            " no shutdown",
            "exit",
        ])

    return f"# Configuración troncal genérica para {vendor}"


def generate_device_config(task_type: str, vendor: str, params: Dict[str, Any]) -> str:
    """Función de despacho para generar cualquier configuración soportada."""
    tt = task_type.lower()
    if tt == "vlan":
        return generate_vlan_config(
            vendor=vendor,
            vlan_id=params.get("vlan_id", 10),
            name=params.get("name", "VLAN_DEFAULT"),
            svi_ip=params.get("svi_ip"),
            svi_mask=params.get("svi_mask"),
        )
    elif tt == "access_port":
        return generate_access_port_config(
            vendor=vendor,
            interface=params.get("interface", "Gi0/1"),
            vlan_id=params.get("vlan_id", 10),
            enable_portfast=params.get("portfast", True),
            enable_bpduguard=params.get("bpduguard", True),
        )
    elif tt == "trunk_port":
        return generate_trunk_port_config(
            vendor=vendor,
            interface=params.get("interface", "Gi0/24"),
            allowed_vlans=params.get("allowed_vlans", "10,20,30"),
            native_vlan=params.get("native_vlan", 99),
        )
    else:
        raise ValueError(f"Tipo de tarea '{task_type}' no reconocida. Opciones: vlan, access_port, trunk_port")
