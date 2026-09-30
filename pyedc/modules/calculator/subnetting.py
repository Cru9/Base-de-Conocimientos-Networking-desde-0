"""
Motor de cálculo de Subnetting, VLSM y Supernetting IPv4/IPv6 para PyEDC.
"""

import ipaddress
import math
from typing import List, Dict, Any, Tuple


def calculate_subnet_info(cidr_str: str) -> Dict[str, Any]:
    """Calcula todos los parámetros técnicos de una red o subred IPv4."""
    try:
        network = ipaddress.IPv4Network(cidr_str, strict=False)
    except ValueError as e:
        raise ValueError(f"Dirección o prefijo CIDR inválido '{cidr_str}': {e}")

    netmask = network.netmask
    wildcard_int = int(ipaddress.IPv4Address("255.255.255.255")) - int(netmask)
    wildcard = str(ipaddress.IPv4Address(wildcard_int))

    total_hosts = network.num_addresses
    usable_hosts = max(0, total_hosts - 2) if network.prefixlen < 31 else (2 if network.prefixlen == 31 else 1)

    first_host = str(network.network_address + 1) if usable_hosts > 0 else str(network.network_address)
    last_host = str(network.broadcast_address - 1) if usable_hosts > 0 else str(network.broadcast_address)
    broadcast = str(network.broadcast_address)

    # Clasificación de uso
    is_private = network.is_private
    is_loopback = network.is_loopback
    is_link_local = network.is_link_local
    is_multicast = network.is_multicast

    tipo = "Pública"
    if is_private:
        tipo = "Privada (RFC 1918)"
    elif is_loopback:
        tipo = "Loopback (RFC 1122)"
    elif is_link_local:
        tipo = "Link-Local (RFC 3927)"
    elif is_multicast:
        tipo = "Multicast (RFC 5771)"

    return {
        "network": str(network.network_address),
        "prefix": network.prefixlen,
        "cidr": str(network),
        "netmask": str(netmask),
        "wildcard": wildcard,
        "first_host": first_host,
        "last_host": last_host,
        "broadcast": broadcast,
        "total_hosts": total_hosts,
        "usable_hosts": usable_hosts,
        "tipo": tipo,
        "binary_mask": ".".join(f"{int(o):08b}" for o in str(netmask).split(".")),
    }


def calculate_vlsm(parent_network_str: str, requirements: List[Tuple[str, int]]) -> Dict[str, Any]:
    """
    Calcula la asignación óptima de subredes con VLSM (Variable Length Subnet Masking).
    
    :param parent_network_str: Red raíz en formato CIDR (ej: '192.168.1.0/24')
    :param requirements: Lista de tuplas (nombre_subred, cantidad_hosts_requeridos)
    :return: Diccionario con la asignación por subred, resumen de eficiencia y sobrante.
    """
    parent = ipaddress.IPv4Network(parent_network_str, strict=False)
    
    # Ordenar requerimientos de mayor a menor número de hosts (regla de oro VLSM)
    sorted_reqs = sorted(requirements, key=lambda x: x[1], reverse=True)
    
    allocated = []
    current_ip = int(parent.network_address)
    parent_end = int(parent.broadcast_address)
    
    total_requested_hosts = 0
    total_allocated_capacity = 0

    for name, req_hosts in sorted_reqs:
        if req_hosts <= 0:
            continue
        
        total_requested_hosts += req_hosts

        # En IPv4 normal: requerimos req_hosts + 2 (red + broadcast)
        # Si req_hosts == 2 (enlaces punto a punto), prefix = 30 (o 31 en RFC 3021)
        needed_addresses = req_hosts + 2
        power = math.ceil(math.log2(needed_addresses))
        prefix = 32 - power

        # No permitir prefijos menores a 0 o mayores a 32
        prefix = max(0, min(32, prefix))
        subnet_size = 2 ** (32 - prefix)

        # Alinear current_ip al límite del tamaño del bloque
        if current_ip % subnet_size != 0:
            current_ip = ((current_ip // subnet_size) + 1) * subnet_size

        if current_ip + subnet_size - 1 > parent_end:
            raise ValueError(
                f"Capacidad excedida: La red raíz '{parent}' no tiene suficiente espacio para la subred '{name}' ({req_hosts} hosts)."
            )

        sub_net = ipaddress.IPv4Network((current_ip, prefix))
        total_allocated_capacity += sub_net.num_addresses

        info = calculate_subnet_info(str(sub_net))
        info["name"] = name
        info["requested_hosts"] = req_hosts
        info["waste"] = info["usable_hosts"] - req_hosts
        allocated.append(info)

        current_ip += subnet_size

    efficiency = (total_requested_hosts / parent.num_addresses) * 100
    free_addresses = (parent_end - current_ip + 1) if current_ip <= parent_end else 0

    return {
        "parent_network": str(parent),
        "parent_total_addresses": parent.num_addresses,
        "subnets": allocated,
        "total_requested_hosts": total_requested_hosts,
        "total_allocated_addresses": total_allocated_capacity,
        "free_addresses_remaining": max(0, free_addresses),
        "efficiency_percent": round(efficiency, 2),
    }


def summarize_routes(subnets: List[str]) -> List[str]:
    """Calcula el resumen de rutas óptimo (supernetting) para una lista de redes."""
    nets = [ipaddress.IPv4Network(s, strict=False) for s in subnets]
    collapsed = list(ipaddress.collapse_addresses(nets))
    return [str(c) for c in collapsed]
