# 04. INTERCONEXION MULTI-CLOUD, ROUTERS VIRTUALES (NVA) Y ENRUTAMIENTO BGP

> **REDES EN LA NUBE Y ARQUITECTURAS HIBRIDAS (CLOUD NETWORKING & MULTI-CLOUD)**


---



## 1. ARQUITECTURA MULTI-CLOUD: POR QUE Y COMO CONECTAR MULTIPLES NUBES

Hoy en dia, las empresas maduras no concentran todos sus servicios en un solo
proveedor de nube. Una estrategia Multi-Cloud e Hibrida responde a:
1. Resiliencia y Disaster Recovery (DR): Si una region de AWS sufre un corte masivo,
   las cargas criticas pueden conmutar a Microsoft Azure o Google Cloud.
2. Evitar "Vendor Lock-In": Negociacion de precios y no depender de una sola API.
3. Servicios especializados: Por ejemplo, procesar analitica e IA en Google Cloud
   (BigQuery/Vertex), mientras el Active Directory y bases de datos SQL residen en
   Azure, y los microservicios de cara al usuario corren en AWS EKS.

DIAGRAMA GENERAL DE INTERCONEXION MULTI-CLOUD:
```text
+-------------------+       IPsec / Megaport BGP      +--------------------+
|    AMAZON AWS     | <=============================> |  MICROSOFT AZURE   |
| (AWS Transit GW)  |                                 | (Azure Virtual WAN)|
|  ASN Privado:     |                                 |   ASN Privado:     |
|      64512        | \                             / |      65515         |
+-------------------+  \                           /  +--------------------+
                        \                         /
            Direct       \                       /   ExpressRoute
            Connect       \                     /
                           +-------------------+
                           |  ON-PREMISES HQ   |
                           |    DATACENTER     |
                           |  Cisco Catalyst / |
                           |   Huawei Routers  |
                           |   ASN: 65001      |
                           +-------------------+
                                     ^
                                     | Cloud Interconnect
                                     v
                           +-------------------+
                           |   GOOGLE CLOUD    |
                           |  (Cloud Router)   |
                           |   ASN: 65534      |
                           +-------------------+
```


## 2. METODOS DE INTERCONEXION CLOUD-TO-CLOUD

Existen dos formas principales de interconectar nubes publicas:

A. Tuneles VPN IPsec cifrados sobre Internet Publica:
   - Ventajas: Costo minimo, aprovisionamiento inmediato en minutos sin contratos.
   - Desventajas: Latencia variable, jitter no garantizado, throughput limitado a
     1.25 Gbps por tunel IPsec (requiere ECMP para agregar ancho de banda).

B. Cloud Interconnect Fabric (Megaport, Equinix Fabric, PacketFabric):
   - Red troncal privada de Capa 2 / Capa 3 que interconecta AWS Direct Connect,
     Azure ExpressRoute y Google Cloud Interconnect dentro del mismo Datacenter
     de colocation (Meet-Me Room - MMR).
   - Ventajas: Latencias ultra bajas (< 2 ms entre nubes vecinas), anchos de banda
     desde 1 Gbps hasta 100 Gbps, SLAs del 99.999%, sin exponer trafico a Internet.



## 3. DESPLIEGUE DE NETWORK VIRTUAL APPLIANCES (NVA) / ROUTERS VIRTUALES

En lugar de depender exclusivamente de las puertas de enlace administradas por el
proveedor (que a veces carecen de funciones avanzadas de ruteo como BFD subsegundo,
redistribucion compleja o inspeccion de paquetes profunda), las arquitecturas
empresariales despliegan "Transit VPCs" o "Security Hubs" con Routers Virtuales:
- Cisco Catalyst 8000v (sucesor del afamado Cisco CSR1000v)
- Fortinet FortiGate-VM / Palo Alto VM-Series

Topologia con Cisco Catalyst 8000v en AWS y Azure:
   Subnet AWS (10.100.0.0/16)                      Subnet Azure (10.200.0.0/16)
          |                                                   |
   [AWS TGW o VPC]                                    [Azure vWAN / VNet]
          |                                                   |
```text
   [C8000v en AWS] <==== Tunel IPsec IKEv2 / BGP ====> [C8000v en Azure]
```

    WAN IP: 54.210.1.10                                WAN IP: 20.40.80.20
    ASN: 64512                                         ASN: 65515



## 4. CONFIGURACION PRACTICA: CISCO CATALYST 8000V (AWS)

! Configuracion del Router Virtual en AWS EC2 (c8000v-aws)
hostname C8000V-AWS

! Interfaz publica WAN (asociada a Elastic IP en AWS)
```text
interface GigabitEthernet1
 description CONEXION_INTERNET_AWS_IGW
 ip address 10.100.0.10 255.255.255.0
 no shutdown

! Interfaz LAN privada interna hacia la VPC
interface GigabitEthernet2
 description CONEXION_LAN_INTERNA_AWS
 ip address 10.100.1.1 255.255.255.0
 no shutdown

! Fase 1 IKEv2 hacia el Router Virtual en Azure
crypto ikev2 proposal PROP-IKEV2-AZURE
 encryption aes-gcm-256
 prf sha384
 group 19 20

crypto ikev2 policy POL-IKEV2-AZURE
 proposal PROP-IKEV2-AZURE

crypto ikev2 keyring KEYRING-AZURE
 peer AZURE-PEER
  address 20.40.80.20
  pre-shared-key EnterpriseMultiCloudSecretKey2026!

crypto ikev2 profile PROF-IKEV2-AZURE
 match identity remote address 20.40.80.20 255.255.255.255
 identity local address 54.210.1.10
 authentication remote pre-share
 authentication local pre-share
 keyring local KEYRING-AZURE
 lifetime 28800

! Fase 2 IPsec Transform-Set y Perfil
crypto ipsec transform-set TS-GCM-256 esp-gcm 256
 mode transport

crypto ipsec profile IPSEC-PROF-AZURE
 set transform-set TS-GCM-256
 set ikev2-profile PROF-IKEV2-AZURE

! Tunel VTI (Virtual Tunnel Interface)
interface Tunnel100
 description TUNEL_VTI_A_AZURE_C8000V
 ip address 169.254.100.1 255.255.255.252
 ip mtu 1400
 ip tcp adjust-mss 1360
 tunnel source GigabitEthernet1
 tunnel mode ipsec ipv4
 tunnel destination 20.40.80.20
 tunnel protection ipsec profile IPSEC-PROF-AZURE

! Enrutamiento BGP Dinamico Multi-Cloud
router bgp 64512
 bgp router-id 10.100.0.10
 bgp log-neighbor-changes
 neighbor 169.254.100.2 remote-as 65515
 neighbor 169.254.100.2 description BGP_PEER_AZURE_C8000V
 neighbor 169.254.100.2 timers 10 30
 !
 address-family ipv4
  network 10.100.0.0 mask 255.255.0.0
  neighbor 169.254.100.2 activate
  neighbor 169.254.100.2 soft-reconfiguration inbound
 exit-address-family
```


## 5. CONFIGURACION PRACTICA: CISCO CATALYST 8000V (AZURE)

! Configuracion del Router Virtual en Azure VM (c8000v-azure)
hostname C8000V-AZURE

```text
interface GigabitEthernet1
 description CONEXION_INTERNET_AZURE_PIP
 ip address 10.200.0.10 255.255.255.0
 no shutdown

interface GigabitEthernet2
 description CONEXION_LAN_INTERNA_AZURE
 ip address 10.200.1.1 255.255.255.0
 no shutdown

crypto ikev2 proposal PROP-IKEV2-AWS
 encryption aes-gcm-256
 prf sha384
 group 19 20

crypto ikev2 policy POL-IKEV2-AWS
 proposal PROP-IKEV2-AWS

crypto ikev2 keyring KEYRING-AWS
 peer AWS-PEER
  address 54.210.1.10
  pre-shared-key EnterpriseMultiCloudSecretKey2026!

crypto ikev2 profile PROF-IKEV2-AWS
 match identity remote address 54.210.1.10 255.255.255.255
 identity local address 20.40.80.20
 authentication remote pre-share
 authentication local pre-share
 keyring local KEYRING-AWS
 lifetime 28800

crypto ipsec transform-set TS-GCM-256 esp-gcm 256
 mode transport

crypto ipsec profile IPSEC-PROF-AWS
 set transform-set TS-GCM-256
 set ikev2-profile PROF-IKEV2-AWS

interface Tunnel100
 description TUNEL_VTI_A_AWS_C8000V
 ip address 169.254.100.2 255.255.255.252
 ip mtu 1400
 ip tcp adjust-mss 1360
 tunnel source GigabitEthernet1
 tunnel mode ipsec ipv4
 tunnel destination 54.210.1.10
 tunnel protection ipsec profile IPSEC-PROF-AWS

router bgp 65515
 bgp router-id 10.200.0.10
 bgp log-neighbor-changes
 neighbor 169.254.100.1 remote-as 64512
 neighbor 169.254.100.1 description BGP_PEER_AWS_C8000V
 neighbor 169.254.100.1 timers 10 30
 !
 address-family ipv4
  network 10.200.0.0 mask 255.255.0.0
  neighbor 169.254.100.1 activate
  neighbor 169.254.100.1 soft-reconfiguration inbound
 exit-address-family
```


## 6. MANEJO DE IPS SOLAPADAS (OVERLAPPING IP ADDRESSES)

Un problema muy frecuente en Multi-Cloud y adquisiciones corporativas es que
ambos entornos utilizan el mismo rango (por ejemplo, AWS usa 10.0.0.0/16 y Azure
tambien usa 10.0.0.0/16).

Solucion: Doble NAT (Twice NAT) en el Router Virtual (NVA):
1. Se crea un pool de direcciones virtuales no conflictivas (ej. 172.16.10.0/24).
2. Cuando el servidor en AWS envia paquetes hacia Azure, la direccion de destino
   es una IP virtual. El router NVA traduce tanto la IP origen como la destino:

! Configuracion de NAT 1:1 estatico para IPs solapadas en Cisco C8000v:
ip nat inside source static 10.0.1.50 172.16.10.50
ip nat outside source static 10.0.1.80 172.16.20.80

! De esta forma, el trafico fluye sin que ninguno de los dos extremos
! se entere de que comparten el mismo espacio de direccionamiento RFC 1918.



## 7. VERIFICACION Y RESOLUCION DE PROBLEMAS (TROUBLESHOOTING)

Comandos para verificar el estado de la interconexion Multi-Cloud:

1. Verificar que el tunel IKEv2 este establecido:
```text
   show crypto ikev2 sa
   ! Debe mostrar: Status: UP-ACTIVE

2. Verificar que la asociacion de seguridad IPsec este cifrando paquetes:
   show crypto ipsec sa
   ! Verificar que los contadores "#pkts encaps" y "#pkts decaps" se incrementen.

3. Verificar la sesion BGP entre AWS y Azure:
   show ip bgp summary
   ! Neighbor: 169.254.100.2  Up/Down: 02:45:12  State: Estab

4. Verificar que se estan recibiendo las rutas de la otra nube:
   show ip bgp neighbors 169.254.100.2 routes
   show ip route bgp

5. Prueba de conectividad punto a punto con control de MTU:
```


`cisco
ping 169.254.100.2 size 1360 df-bit
`
