"""
Calculadora de Dimensionamiento para Fabric Spine-Leaf Clos en Data Center (RFC 7348 / EVPN).
"""

from typing import Dict, Any


def calculate_spine_leaf(
    num_leafs: int = 4,
    downlinks_per_leaf: int = 48,
    downlink_speed_gbps: float = 25.0,
    uplinks_per_leaf: int = 4,
    uplink_speed_gbps: float = 100.0,
    spine_port_density: int = 32,
) -> Dict[str, Any]:
    """
    Calcula la sobresuscripción, capacidad de puertos y arquitectura física de un Data Center Spine-Leaf.
    """
    downlink_bw_per_leaf = downlinks_per_leaf * downlink_speed_gbps
    uplink_bw_per_leaf = uplinks_per_leaf * uplink_speed_gbps

    oversubscription_ratio = downlink_bw_per_leaf / uplink_bw_per_leaf if uplink_bw_per_leaf > 0 else 0

    # En una topología Clos de 2 etapas estándar:
    # Cada Leaf se conecta a TODOS los Spines mediante 1 enlace.
    # Por lo tanto, el número de Spines requeridos = enlaces de uplink por Leaf.
    required_spines = uplinks_per_leaf

    # Los Spines deben tener al menos tantos puertos como número de Leafs hay.
    spine_ports_used = num_leafs
    max_leafs_supported_by_spine = spine_port_density

    total_server_ports = num_leafs * downlinks_per_leaf
    total_downlink_throughput_tbps = (total_server_ports * downlink_speed_gbps) / 1000.0
    bisectional_bandwidth_tbps = (num_leafs * uplink_bw_per_leaf) / 1000.0

    if oversubscription_ratio <= 1.0:
        health = "1:1 (Non-Blocking / Line-Rate)"
        assessment = "Rendimiento máximo. Ideal para clústeres de IA, HPC, Ceph o almacenamiento NVMe-oF."
    elif oversubscription_ratio <= 3.0:
        health = f"{round(oversubscription_ratio, 2)}:1 (Estándar Empresa Recomendado)"
        assessment = "Excelente balance entre costo, densidad de puertos y latencia para virtualización y nube privada."
    else:
        health = f"{round(oversubscription_ratio, 2)}:1 (Sobresuscripción Alta)"
        assessment = "Precaución: Puede provocar cuellos de botella y pérdidas de paquetes en ráfagas de tráfico este-oeste."

    return {
        "num_leafs": num_leafs,
        "required_spines": required_spines,
        "total_server_ports": total_server_ports,
        "downlink_bw_per_leaf_gbps": downlink_bw_per_leaf,
        "uplink_bw_per_leaf_gbps": uplink_bw_per_leaf,
        "oversubscription_ratio": round(oversubscription_ratio, 2),
        "health": health,
        "assessment": assessment,
        "bisectional_bandwidth_tbps": round(bisectional_bandwidth_tbps, 2),
        "total_server_throughput_tbps": round(total_downlink_throughput_tbps, 2),
        "spine_port_usage": f"{spine_ports_used} / {spine_port_density} puertos por Spine",
        "fabric_expandability_leafs": max(0, max_leafs_supported_by_spine - num_leafs),
    }
