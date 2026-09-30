# 🏢 Pilar 05: Data Center Fabrics, Cloud Networking Híbrido y Whitebox
## Base de Conocimientos EDC

> **CONTENIDO DEL PILAR:** Arquitecturas Spine-and-Leaf Clos, Overlays VXLAN EVPN, Nube Híbrida (AWS, Azure, GCP) y Sistemas Abiertos SONiC/FRR  
> **UBICACIÓN:** `Base de Conocimientos_EDC/Modulos_Clasificados/05_DataCenter_Cloud_y_Whitebox/README.md`

---

## 📂 Submódulos Incluidos

1. **[`01_DataCenter_Spine_Leaf_VXLAN/`](./01_DataCenter_Spine_Leaf_VXLAN/)**  
   - Topología Spine-and-Leaf Clos de 2 etapas no bloqueante.
   - Túneles Overlay VXLAN (RFC 7348) con VTEPs y VNI de 24 bits.
   - Plano de control BGP EVPN (RFC 7432 / RFC 8365) y tipos de ruta 1 a 5.
   - Redes de almacenamiento SAN/NAS (Fibre Channel, iSCSI, RoCE).
   - Configuración en conmutadores Cisco Nexus (NX-OS).

2. **[`02_Cloud_Networking_MultiCloud/`](./02_Cloud_Networking_MultiCloud/)**  
   - AWS Networking: VPC, Subnets, Internet/NAT Gateways, Transit Gateway y Direct Connect.
   - Azure Networking: VNet, VNet Peering, Virtual WAN y ExpressRoute.
   - GCP Networking: VPC Global, Cloud Router y Dedicated/Partner Interconnect.
   - Diseños de interconexión multi-nube y routers virtuales (NVAs).

3. **[`03_Sistemas_Operativos_Abiertos_Whitebox/`](./03_Sistemas_Operativos_Abiertos_Whitebox/)**  
   - Desagregación de hardware y software (ONIE bare-metal).
   - Sistema operativo SONiC (Software for Open Networking in the Cloud): Base Debian, base de datos Redis, microservicios Docker y API SAI.
   - Suite de enrutamiento FRRouting (FRR) y VyOS.

---

## 🔗 Referencia Cruzada en la Wiki
- 📘 **[`WIKI_05_DataCenter_Fabric_y_Cloud_Hybrid.md`](../../WIKI_EDC/WIKI_05_DataCenter_Fabric_y_Cloud_Hybrid.md)**
