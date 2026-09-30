"""
Catálogo del Banco de 200 Laboratorios Prácticos y Plataformas de Emulación para PyEDC.
Basado en WIKI_10 de la Base de Conocimientos EDC.
"""

from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field


class LabBlock(BaseModel):
    part: int
    lab_range: str
    title: str
    technologies: str
    complexity: str
    certification: str
    suggested_emulator: str


LAB_BLOCKS: List[LabBlock] = [
    LabBlock(
        part=1,
        lab_range="001 - 020",
        title="Switching Base, VLANs, Trunking y Enrutamiento Estático",
        technologies="VLANs 802.1Q, VTPv3, LACP EtherChannel, Rapid-PVST+, SVI L3, Rutas flotantes",
        complexity="Asociado (Asociate)",
        certification="Cisco CCNA (200-301) / Huawei HCIA-Datacom",
        suggested_emulator="GNS3 / EVE-NG / Cisco Packet Tracer",
    ),
    LabBlock(
        part=2,
        lab_range="021 - 040",
        title="Enrutamiento OSPFv2 Single y Multi-Área, Autenticación y Timers",
        technologies="OSPFv2, tipos de redes (Point-to-Point, Broadcast), DR/BDR, Áreas Stub y NSSA, BFD",
        complexity="Profesional (Professional)",
        certification="Cisco CCNP Enterprise (350-401 ENCOR) / Huawei HCIP",
        suggested_emulator="EVE-NG / Cisco Modeling Labs (CML)",
    ),
    LabBlock(
        part=3,
        lab_range="041 - 060",
        title="EIGRP Corporativo, Named Mode y Redistribución Mutua",
        technologies="EIGRP Named Mode, sumarización manual, redistribución mutua OSPF-EIGRP con tags y Route Maps",
        complexity="Profesional (Professional)",
        certification="Cisco CCNP Enterprise (300-410 ENARSI)",
        suggested_emulator="EVE-NG / CML",
    ),
    LabBlock(
        part=4,
        lab_range="061 - 080",
        title="BGP Enterprise e ISP, Peering eBGP/iBGP y Políticas de Tráfico",
        technologies="BGP multihoming, manipulación de Local-Preference, MED, AS-Path Prepending, Route Reflectors",
        complexity="Profesional / Experto",
        certification="Cisco CCNP ENARSI / BGP Specialist",
        suggested_emulator="EVE-NG / GNS3",
    ),
    LabBlock(
        part=5,
        lab_range="081 - 100",
        title="Alta Disponibilidad FHRP y Seguridad Perimetral IPsec IKEv2",
        technologies="HSRPv2 con tracking de interfaces, VRRPv3, túneles VPN IPsec IKEv2 Site-to-Site y DMVPN",
        complexity="Profesional (Professional)",
        certification="Cisco CCNP Security / CompTIA Security+ / Fortinet NSE 4",
        suggested_emulator="EVE-NG / Containerlab",
    ),
    LabBlock(
        part=6,
        lab_range="101 - 120",
        title="Data Center Spine-Leaf, Overlays VXLAN y Control Plane BGP EVPN",
        technologies="Clos Spine-Leaf 2-Tier, VTEPs, encapsulación VXLAN (RFC 7348), EVPN Route Type 2/5 (RFC 8365)",
        complexity="Experto (Data Center)",
        certification="Cisco CCNP Data Center / Arista ACE / Huawei HCIP-DC",
        suggested_emulator="EVE-NG (Nexus 9300v / vEOS) / Containerlab",
    ),
    LabBlock(
        part=7,
        lab_range="121 - 140",
        title="Redes Carrier MPLS L3VPN, LDP e Ingeniería de Tráfico",
        technologies="MPLS Core P/PE, distribución de etiquetas LDP, VRF-Lite, BGP/MPLS L3VPN (RFC 4364) con Route Targets",
        complexity="Experto (Carrier / Service Provider)",
        certification="Cisco Service Provider (CCNP SP) / Juniper JNCIP-SP",
        suggested_emulator="EVE-NG / GNS3 (Cisco IOS-XR / Huawei NE40E)",
    ),
    LabBlock(
        part=8,
        lab_range="141 - 160",
        title="IPv6 Empresarial, Dual-Stack, SLAAC, DHCPv6 y OSPFv3",
        technologies="Direccionamiento Global IPv6, túneles 6to4, OSPFv3 multi-proceso, MP-BGP para IPv6",
        complexity="Profesional (Professional)",
        certification="Cisco CCNP Enterprise / CompTIA Network+",
        suggested_emulator="GNS3 / EVE-NG",
    ),
    LabBlock(
        part=9,
        lab_range="161 - 180",
        title="Multicast PIM-SM, IGMP Snooping y Calidad de Servicio QoS MQC",
        technologies="PIM-SM, Rendezvous Point (RP) estático y Auto-RP, QoS MQC (Class-Map, Policy-Map, LLQ, WRED)",
        complexity="Profesional (Professional)",
        certification="Cisco CCNP Enterprise / CCIE Enterprise",
        suggested_emulator="EVE-NG / CML",
    ),
    LabBlock(
        part=10,
        lab_range="181 - 200",
        title="SD-WAN Corporativo, Multi-Cloud (AWS/Azure) y Control de Acceso 802.1X",
        technologies="Topologías SD-WAN overlay, VPNs IPsec hacia AWS VPC / Azure VNet, autenticación RADIUS 802.1X",
        complexity="Especialidad Avanzada",
        certification="Multi-Cloud Specialist / Cisco SD-WAN / Security+",
        suggested_emulator="EVE-NG / CML / Containerlab",
    ),
]


class LabCatalog:
    def __init__(self):
        self.blocks = LAB_BLOCKS

    def get_all_blocks(self) -> List[LabBlock]:
        return self.blocks

    def search_labs(self, query: str) -> List[LabBlock]:
        q = query.strip().lower()
        results = []
        for b in self.blocks:
            if (q in b.title.lower() or q in b.technologies.lower() or
                q in b.certification.lower() or q in b.lab_range.lower()):
                results.append(b)
        return results
