"""
Calculadora de MTU de Ruta (PMTU), TCP MSS y Análisis de Overhead de Encapsulamiento.
"""

from typing import Dict, Any, List

ENCAPSULATION_OVERHEADS = {
    "vlan_8021q": {
        "name": "VLAN 802.1Q (Single Tag)",
        "bytes": 4,
        "layer": "L2",
    },
    "qinq_8021ad": {
        "name": "QinQ 802.1ad (Double Tag)",
        "bytes": 8,
        "layer": "L2",
    },
    "pppoe": {
        "name": "PPPoE (RFC 2516)",
        "bytes": 8,
        "layer": "L2/L3",
    },
    "gre": {
        "name": "Túnel GRE genérico (RFC 2784) sobre IPv4",
        "bytes": 24,  # 4 GRE + 20 IP externo
        "layer": "L3 Túnel",
    },
    "ipsec_esp": {
        "name": "IPsec Modo Túnel (ESP AES-256 + SHA-256 + NAT-T)",
        "bytes": 72,  # Aprox: 20 IP ext + 8 UDP/NAT-T + 8 ESP + 16 IV + 16 ICV + padding
        "layer": "L3 Seguridad",
    },
    "vxlan": {
        "name": "VXLAN EVPN Encapsulation (RFC 7348)",
        "bytes": 50,  # 14 Ethernet ext + 20 IP ext + 8 UDP + 8 VXLAN
        "layer": "L2/L3 Fabric",
    },
    "wireguard": {
        "name": "WireGuard VPN",
        "bytes": 60,  # 20 IP ext + 8 UDP + 32 WG Header
        "layer": "L3 Seguridad",
    },
    "mpls_1label": {
        "name": "Etiqueta MPLS (1 Label)",
        "bytes": 4,
        "layer": "L2.5",
    },
    "mpls_2labels": {
        "name": "Etiquetas MPLS (2 Labels - Transport + VPN)",
        "bytes": 8,
        "layer": "L2.5",
    },
}


def calculate_mtu_mss(
    base_mtu: int = 1500,
    is_ipv6: bool = False,
    active_encapsulations: List[str] = None,
) -> Dict[str, Any]:
    """
    Calcula el MTU efectivo y el MSS recomendado para TCP.

    :param base_mtu: MTU de la interfaz física (estándar Ethernet = 1500, Jumbo Frame = 9000 o 9216)
    :param is_ipv6: Si se utiliza IPv6 como capa de red cliente
    :param active_encapsulations: Lista de claves de ENCAPSULATION_OVERHEADS
    :return: Diccionario detallado con desglose de bytes y comandos CLI
    """
    if active_encapsulations is None:
        active_encapsulations = []

    ip_header = 40 if is_ipv6 else 20
    tcp_header = 20

    total_overhead = 0
    breakdown = []

    for enc_key in active_encapsulations:
        if enc_key in ENCAPSULATION_OVERHEADS:
            info = ENCAPSULATION_OVERHEADS[enc_key]
            total_overhead += info["bytes"]
            breakdown.append({
                "clave": enc_key,
                "nombre": info["name"],
                "overhead_bytes": info["bytes"],
                "capa": info["layer"],
            })

    # MTU disponible para el paquete IP cliente
    effective_ip_mtu = base_mtu - total_overhead

    if effective_ip_mtu < 576 and not is_ipv6:
        warning = "CRÍTICO: El MTU efectivo es menor a 576 bytes (mínimo obligatorio IPv4 RFC 791)."
    elif effective_ip_mtu < 1280 and is_ipv6:
        warning = "CRÍTICO: El MTU efectivo es menor a 1280 bytes (mínimo obligatorio IPv6 RFC 8200)."
    else:
        warning = None

    # MSS = MTU efectivo - Encabezado IP cliente - Encabezado TCP
    recommended_mss = effective_ip_mtu - ip_header - tcp_header
    recommended_mss = max(0, recommended_mss)

    # Generación de sintaxis de remediación CLI
    cli_remediation = {
        "cisco": f"interface <wan-interface>\n ip tcp adjust-mss {recommended_mss}",
        "huawei": f"interface <wan-interface>\n tcp adjust-mss {recommended_mss}",
        "aruba": f"interface <wan-interface>\n ip tcp-mss {recommended_mss}",
        "fortinet": f"config system interface\n edit <wan>\n  set tcp-mss {recommended_mss}\n end",
    }

    return {
        "base_mtu": base_mtu,
        "is_ipv6": is_ipv6,
        "ip_version": "IPv6 (40B)" if is_ipv6 else "IPv4 (20B)",
        "ip_header_bytes": ip_header,
        "tcp_header_bytes": tcp_header,
        "total_tunnel_overhead_bytes": total_overhead,
        "effective_ip_mtu": effective_ip_mtu,
        "recommended_tcp_mss": recommended_mss,
        "breakdown": breakdown,
        "warning": warning,
        "cli_remediation": cli_remediation,
    }
