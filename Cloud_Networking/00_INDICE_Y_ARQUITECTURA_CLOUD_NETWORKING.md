# 00. INDICE GENERAL, COMPARATIVA DE NUBES Y MODELO DE RESPONSABILIDAD COMPARTIDA

> **REDES EN LA NUBE Y ARQUITECTURAS HIBRIDAS (CLOUD NETWORKING & MULTI-CLOUD)**


---



## 1. ¿QUE ES CLOUD NETWORKING Y EN QUE SE DIFERENCIA DE LAS REDES ON-PREMISES?

En un centro de datos tradicional (On-Premises), el ingeniero de redes controla
los cables de fibra, los switches fisicos, los protocolos Spanning Tree y el hardware
de enrutamiento.

En la Nube Publica (AWS, Microsoft Azure, Google Cloud):
- Todo el hardware fisico esta oculto y virtualizado mediante Redes Definidas por
  Software (SDN - Software-Defined Networking).
- NO EXISTE el trafico de broadcast ni multicast nativo en la capa virtual.
- Los protocolos de Capa 2 (como STP o ARP tradicional) han sido reemplazados por
  tablas de asignacion y encapsulaciones de hipervisor (Geneve / VPC Fabrics).
- Los puertos no se configuran con CLI clasico; se aprovisionan mediante APIs,
  consolas web y herramientas de Infraestructura como Codigo (Terraform / CloudFormation).

El Desafio del Ingeniero de Redes Cloud:
Interconectar las redes virtuales de la nube con los Datacenters y sucursales
on-premises de la empresa garantizando seguridad, baja latencia, enrutamiento BGP
dinamico y control de costos de transferencia de datos (Egress Data Transfer).



## 2. COMPARATIVA TERMINOLOGICA ENTRE LOS 3 GIGANTES DE LA NUBE


| Concepto de Red | Amazon AWS | Microsoft Azure | Google Cloud (GCP) |
| :--- | :--- | :--- | :--- |
| Red Virtual Aislada | VPC (Virtual Priv. Cloud) VNet (Virtual Network) | VPC (Global por defecto) |  |
| Alcance de la Red | Regional (por Region) | Regional | GLOBAL (Cruza regiones) |
| Segmento de Subred | Asociada a 1 Zona (AZ) | Asociada a la Region | Regional |
| Concentrador Central Hub | Transit Gateway (TGW) | Virtual WAN (vWAN) | Network Connectivity Center |
| Rutas Personalizadas | VPC Route Table | UDR (Route Table) | VPC Routes |
| Firewall por Instancia | Security Group (Stateful) NSG (Network Sec Group) Cloud Firewall Rules |  |  |
| Firewall por Subred | NACL (Stateless) | NSG aplicado a Subred | N/A (Reglas por Tags) |
| Salida a Internet Privada | NAT Gateway | NAT Gateway | Cloud NAT |
| Enlace Dedicado Directo | AWS Direct Connect | Azure ExpressRoute | Cloud Dedicated Interconnect |
| Router BGP Administrado | Virtual Private GW (VGW)Azure Route Server | Cloud Router |  |
| Enlace Privado a Servicios | AWS PrivateLink | Azure Private Endpoint | Private Service Connect |




## 3. MODELO DE RESPONSABILIDAD COMPARTIDA EN REDES CLOUD

- Responsabilidad del Proveedor Cloud (AWS / Azure / GCP):
  * Mantenimiento de la infraestructura fisica de fibra optica submarina y satelital.
  * Disponibilidad de los Datacenters y proteccion contra ataques DDoS volumetricos masivos.
  * Funcionamiento de los controladores SDN subyacentes.

- Responsabilidad de la Empresa (El Ingeniero de Redes):
  * Diseno del plan de direccionamiento IP (evitar solapamiento de subredes con On-Premises).
  * Configuracion de Tablas de Enrutamiento y gateways de transito.
  * Definicion de politicas de seguridad (Security Groups, ACLs y Firewalls NGFW virtuales).
  * Establecimiento y cifrado de tuneles VPN IPsec e interconexiones dedicadas.



## 4. INDICE DE ARCHIVOS DE LA CARPETA CLOUD_NETWORKING

[00_INDICE_Y_ARQUITECTURA_CLOUD_NETWORKING.md](./00_INDICE_Y_ARQUITECTURA_CLOUD_NETWORKING.md)
    - Fundamentos de redes cloud, comparativa de terminologias y responsabilidad compartida.

[01_AWS_NETWORKING_VPC_TRANSIT_GATEWAY_Y_PEERING.md](./01_AWS_NETWORKING_VPC_TRANSIT_GATEWAY_Y_PEERING.md)
    - Redes en Amazon Web Services: VPCs, Subnets publicas y privadas, Internet Gateway (IGW),
      NAT Gateways, Security Groups vs NACLs, VPC Peering y arquitectura Transit Gateway (TGW).

[02_AZURE_NETWORKING_VNET_VWAN_Y_EXPRESSROUTE.md](./02_AZURE_NETWORKING_VNET_VWAN_Y_EXPRESSROUTE.md)
    - Redes en Microsoft Azure: Virtual Networks (VNets), Network Security Groups (NSGs),
      rutas personalizadas (UDR), VNet Peering, Azure Virtual WAN (vWAN) y ExpressRoute.

[03_GCP_NETWORKING_VPC_GLOBAL_CLOUD_ROUTER_Y_NAT.md](./03_GCP_NETWORKING_VPC_GLOBAL_CLOUD_ROUTER_Y_NAT.md)
    - Redes en Google Cloud: VPC Global unificada, Subnets regionales, Cloud Router dinamico
      con BGP, Cloud NAT y arquitecturas Shared VPC para entornos multi-proyecto corporativos.

[04_MULTI_CLOUD_INTERCONNECT_Y_ROUTERS_VIRTUALES.md](./04_MULTI_CLOUD_INTERCONNECT_Y_ROUTERS_VIRTUALES.md)
    - Diseno Multi-Cloud real: Interconexion de AWS, Azure y GCP con Datacenter On-Premises,

despliegue de Routers Virtuales (Cisco Catalyst 8000v) y Transit VPCs con BGP.
