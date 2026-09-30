"""
Motor de Troubleshooting y Diagnóstico Guiado de Redes y Protocolos para PyEDC.
Basado en WIKI_09 (Wireshark/Metrología) y módulos operativos de la Base de Conocimientos EDC.
"""

from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field


class DiagnosticCase(BaseModel):
    id: str
    title: str
    layer: str
    symptoms: List[str]
    root_causes: List[str]
    wireshark_display_filter: str
    wireshark_capture_filter: str
    cisco_commands: List[str]
    huawei_commands: List[str]
    remediation_steps: List[str]
    related_rfc: str = ""


CASES: List[DiagnosticCase] = [
    DiagnosticCase(
        id="tcp_retransmissions",
        title="Retransmisiones TCP Excesivas y Lentitud de Aplicación",
        layer="Capa 4 (Transporte)",
        symptoms=[
            "Carga intermitente o congelamiento de aplicaciones web y transferencias de archivos.",
            "Alto porcentaje de paquetes retransmitidos (> 2% del total de paquetes TCP).",
            "Latencia percibida muy superior al RTT medido por ping.",
        ],
        root_causes=[
            "Pérdida de paquetes en la red WAN o enlaces Wi-Fi congestionados.",
            "MTU/MSS mal configurado con bit DF (Don't Fragment) activado provocando 'Black Hole'.",
            "Duplex Mismatch (un extremo en Full-Duplex y el otro en Half-Duplex).",
            "Bufferbloat o buffers saturados en switches/routers intermedios.",
        ],
        wireshark_display_filter="tcp.analysis.retransmission || tcp.analysis.duplicate_ack || tcp.analysis.zero_window",
        wireshark_capture_filter="tcp and not port 22",
        cisco_commands=[
            "show interfaces | include drops|errors|duplex|CRC",
            "show ip tcp statistics",
            "show ip interface <wan-if> | include MTU",
        ],
        huawei_commands=[
            "display interface brief",
            "display tcp status",
            "display ip statistics",
        ],
        remediation_steps=[
            "Calcular el TCP MSS óptimo con la calculadora PyEDC (`pyedc calc mss`) y aplicar `ip tcp adjust-mss <valor>`.",
            "Auditar colisiones en interfaces de acceso; forzar `speed` y `duplex full` si la autonegociación falla.",
            "Inspeccionar valores de RTT en Wireshark (Time-Sequence Graph Stevenson/TCPOption).",
        ],
        related_rfc="RFC 9293 (TCP Master Specification) / RFC 8985 (TCP RACK-TLP)",
    ),
    DiagnosticCase(
        id="l2_loop_stp",
        title="Bucle de Capa 2 (Loop L2) y Tormenta de Broadcast",
        layer="Capa 2 (Enlace de Datos)",
        symptoms=[
            "CPU del conmutador al 100% de forma sostenida.",
            "LEDs de puertos parpadeando con máxima intensidad y sincronía en todo el switch.",
            "Mensajes en consola: 'MAC Flapping' (la misma dirección MAC se aprende en dos puertos distintos).",
            "Pérdida completa de conectividad de gestión hacia el equipo.",
        ],
        root_causes=[
            "Cable de parcheo conectado accidentalmente entre dos bocas del mismo switch o switch no gestionado.",
            "Fallo de protocolo Spanning Tree (STP) por filtrado inadvertido de tramas BPDU.",
            "VLANs inconsistentes en enlaces troncales con etiquetado 802.1Q erróneo.",
        ],
        wireshark_display_filter="eth.type == 0x0806 || stp || cdp",
        wireshark_capture_filter="broadcast or stp",
        cisco_commands=[
            "show spanning-tree",
            "show mac address-table notification change",
            "show storm-control",
            "show processes cpu sorted | include STP|ARP",
        ],
        huawei_commands=[
            "display stp brief",
            "display mac-address flapping",
            "display cpu-usage",
        ],
        remediation_steps=[
            "Habilitar BPDU Guard en todos los puertos de usuario final (`spanning-tree bpduguard enable` / `stp bpdu-protection`).",
            "Habilitar Storm Control en puertos de acceso (`storm-control broadcast level 5.0`).",
            "Activar Root Guard en puertos que interconectan switches de distribución hacia acceso.",
        ],
        related_rfc="IEEE 802.1w (RSTP) / IEEE 802.1Q (VLAN Bridging)",
    ),
    DiagnosticCase(
        id="ospf_adjacency_fail",
        title="Fallo de Adyacencia OSPF (Vecindad Down o Pegada en ExStart/Init)",
        layer="Capa 3 (Red)",
        symptoms=[
            "El router vecino OSPF permanece en estado 'EXSTART', 'EXCHANGE' o 'INIT'.",
            "Rutas dinámicas del router vecino no aparecen en la tabla de enrutamiento.",
            "Vecindad oscila (flapping) periódicamente.",
        ],
        root_causes=[
            "MTU Mismatch: El router A tiene MTU 1500 y el router B tiene MTU 1476 o 9000 (el intercambio DBD falla en ExStart).",
            "Área OSPF o Tipo de Área (Stub, NSSA, Normal) diferente en ambos extremos.",
            "Temporizadores Hello/Dead desiguales entre los dos routers.",
            "Subred o máscara de subred incompatible en la interfaz punto a punto.",
            "Fallo de autenticación OSPF (MD5 / HMAC-SHA).",
        ],
        wireshark_display_filter="ospf || ip.proto == 89",
        wireshark_capture_filter="ip proto 89",
        cisco_commands=[
            "show ip ospf neighbor",
            "show ip ospf interface <if-name>",
            "debug ip ospf adj",
            "debug ip ospf hello",
        ],
        huawei_commands=[
            "display ospf peer brief",
            "display ospf error",
            "display ospf routing",
        ],
        remediation_steps=[
            "Verificar que el MTU coincida exactamente en ambos extremos con `show ip interface`.",
            "Si hay un túnel intermedio que altera el MTU, usar temporalmente `ip ospf mtu-ignore` para confirmar el diagnóstico.",
            "Verificar que el Hello y Dead interval coincidan exactamente (ej: 10s / 40s).",
        ],
        related_rfc="RFC 2328 (OSPF Version 2) / RFC 5340 (OSPF for IPv6)",
    ),
    DiagnosticCase(
        id="bgp_peering_down",
        title="Sesión BGP Pegada en 'Active' o 'Idle'",
        layer="Capa 3 / Capa 4 (TCP 179)",
        symptoms=[
            "El estado de BGP muestra 'Active' (intentando abrir conexión TCP) o 'Idle' de forma indefinida.",
            "No se reciben prefijos en la tabla BGP (`Prefixes Received = 0`).",
        ],
        root_causes=[
            "Filtro de firewall o ACL bloqueando el puerto TCP 179 entre las IPs de peering.",
            "Ruta inexistente hacia la IP del vecino (el router no sabe cómo llegar al next-hop).",
            "IP de origen incorrecta en la sesión (se originó con la física en lugar de la Loopback).",
            "Omisión del comando `ebgp-multihop` cuando el peering eBGP se establece hacia una Loopback.",
            "Número de Sistema Autónomo (ASN) remoto configurado erróneamente.",
        ],
        wireshark_display_filter="tcp.port == 179 || bgp",
        wireshark_capture_filter="tcp port 179",
        cisco_commands=[
            "show ip bgp summary",
            "show ip bgp neighbors <neighbor-ip>",
            "show tcp brief",
            "show ip route <neighbor-ip>",
        ],
        huawei_commands=[
            "display bgp peer",
            "display bgp peer <neighbor-ip> verbose",
            "display ip routing-table <neighbor-ip>",
        ],
        remediation_steps=[
            "Probar conectividad en Capa 4: `telnet <neighbor-ip> 179` o captura Wireshark buscando paquetes SYN y RST.",
            "Si el peering es con Loopback: verificar `neighbor <ip> update-source Loopback0` y `neighbor <ip> ebgp-multihop 2`.",
            "Confirmar que la contraseña MD5 (`neighbor <ip> password <pwd>`) sea idéntica en ambos extremos.",
        ],
        related_rfc="RFC 4271 (BGP-4) / RFC 5492 (Capabilities Advertisement)",
    ),
    DiagnosticCase(
        id="ipsec_vpn_down",
        title="Fallo de Negociación en Túnel VPN IPsec (Fase 1 vs Fase 2)",
        layer="Capa 3 (Seguridad / Criptografía)",
        symptoms=[
            "El estado de la SA IPsec muestra 'MM_NO_STATE' o 'DOWN'.",
            "El tráfico entre redes LAN remotas no cruza y se descarta en el router.",
        ],
        root_causes=[
            "Fase 1 (IKE SA): Clave precompartida (PSK) diferente, propuesta de cifrado o grupo Diffie-Hellman incompatible.",
            "Fase 2 (IPsec SA): Desajuste en selectores de tráfico / Proxy-ID (la ACL de cifrado no es simétrica).",
            "Bloqueo de puertos UDP 500 (IKE), UDP 4500 (NAT-T) o Protocolo IP 50 (ESP) en el proveedor de Internet.",
            "PFS (Perfect Forward Secrecy) habilitado en un extremo y deshabilitado en el otro.",
        ],
        wireshark_display_filter="udp.port == 500 || udp.port == 4500 || esp",
        wireshark_capture_filter="udp port 500 or udp port 4500 or proto esp",
        cisco_commands=[
            "show crypto isakmp sa",
            "show crypto ipsec sa",
            "show crypto session detail",
            "debug crypto isakmp",
        ],
        huawei_commands=[
            "display ike sa",
            "display ipsec sa",
            "display ipsec statistics",
        ],
        remediation_steps=[
            "Verificar si la Fase 1 sube: si `QM_IDLE` (Cisco) o `RD` (Huawei), la Fase 1 está OK y el fallo es de Fase 2.",
            "Verificar que las ACLs de tráfico interesante sean estrictamente reflejadas (Origen A -> Destino B en un lado, Origen B -> Destino A en el otro).",
            "Si hay NAT intermedio en la WAN, forzar NAT-Traversal (`crypto isakmp nat keepalive 20`).",
        ],
        related_rfc="RFC 7296 (IKEv2) / RFC 4303 (IPsec ESP)",
    ),
    DiagnosticCase(
        id="rogue_dhcp",
        title="Servidor DHCP No Autorizado (Rogue DHCP) y Conflicto IP",
        layer="Capa 7 / Capa 2 (Servicios DDI)",
        symptoms=[
            "Usuarios reciben IPs en rangos extraños (ej: 192.168.1.X en lugar de la red corporativa 10.X.X.X).",
            "Puerta de enlace predeterminada apunta a un router residencial o PC no autorizado.",
            "Interrupción masiva de Internet y servicios corporativos.",
        ],
        root_causes=[
            "Un usuario conectó un router doméstico Wi-Fi a una boca del conmutador por su puerto LAN.",
            "Ataque de Man-in-the-Middle malicioso mediante DHCP Spoofing.",
            "Ausencia de mecanismos de mitigación L2 (DHCP Snooping).",
        ],
        wireshark_display_filter="bootp.option.dhcp == 2 || bootp.option.type == 53",
        wireshark_capture_filter="port 67 or port 68",
        cisco_commands=[
            "show ip dhcp snooping",
            "show ip dhcp snooping binding",
            "show ip dhcp conflict",
        ],
        huawei_commands=[
            "display dhcp snooping configuration",
            "display dhcp snooping user-bind all",
        ],
        remediation_steps=[
            "Habilitar DHCP Snooping globalmente en todos los conmutadores L2 (`ip dhcp snooping`).",
            "Configurar únicamente los puertos troncales hacia el router corporativo como confiables (`ip dhcp snooping trust`).",
            "Todos los puertos de usuario final quedan como no confiables (Untrusted) por defecto, bloqueando respuestas DHCPOFFER no autorizadas.",
        ],
        related_rfc="RFC 2131 (Dynamic Host Configuration Protocol) / RFC 3046 (DHCP Relay Agent)",
    ),
    DiagnosticCase(
        id="voip_jitter_qos",
        title="Degradación de Voz sobre IP (VoIP), Jitter Alto y Audio Robótico",
        layer="Capa 7 / Capa 4 (UDP / RTP / QoS)",
        symptoms=[
            "Audio entrecortado, ecos, retraso notable o llamadas que se caen a los 30 segundos.",
            "Valor de Jitter superior a 30 ms o pérdida de paquetes RTP superior al 1%.",
            "MOS (Mean Opinion Score) inferior a 3.6.",
        ],
        root_causes=[
            "Falta de clasificación y priorización QoS en la red LAN y WAN (tráfico VoIP compitiendo con descargas masivas).",
            "Ausencia de encolamiento de baja latencia (LLQ - Low Latency Queuing) en routers de salida.",
            "Inspección SIP ALG (Application Layer Gateway) en firewalls alterando puertos en el payload SDP.",
        ],
        wireshark_display_filter="rtp || sip",
        wireshark_capture_filter="udp and not port 53",
        cisco_commands=[
            "show policy-map interface",
            "show mls qos interface",
            "show ip nbar protocol-discovery",
        ],
        huawei_commands=[
            "display qos policy interface",
            "display qos queue statistics interface",
        ],
        remediation_steps=[
            "Marcar el tráfico RTP de audio con DSCP EF (Expedited Forwarding - 46) y la señalización SIP con CS3 o AF31.",
            "Configurar cola de prioridad estricta (Priority Queue) para la clase de voz garantizando ancho de banda reservado.",
            "Deshabilitar SIP ALG en todos los routers y firewalls perimetrales.",
        ],
        related_rfc="RFC 3550 (RTP Audio/Video) / RFC 4594 (DiffServ QoS Architecture)",
    ),
]


class TroubleshooterEngine:
    def __init__(self):
        self.cases = CASES

    def get_all_cases(self) -> List[DiagnosticCase]:
        return self.cases

    def get_case(self, case_id: str) -> Optional[DiagnosticCase]:
        for c in self.cases:
            if c.id == case_id:
                return c
        return None

    def search_cases(self, query: str) -> List[DiagnosticCase]:
        q = query.strip().lower()
        results = []
        for c in self.cases:
            if (q in c.title.lower() or q in c.layer.lower() or q in c.related_rfc.lower() or
                any(q in s.lower() for s in c.symptoms) or any(q in r.lower() for r in c.root_causes)):
                results.append(c)
        return results
