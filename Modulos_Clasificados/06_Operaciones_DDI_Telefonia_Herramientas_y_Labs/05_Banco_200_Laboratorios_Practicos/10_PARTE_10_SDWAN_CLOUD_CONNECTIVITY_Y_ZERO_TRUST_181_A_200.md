# PARTE 10: SD-WAN, CLOUD HYBRID, SASE Y ZERO-TRUST (EJEMPLOS 181 AL 200)

> **ENRUTAMIENTO AVANZADO Y REDES WAN - GUIA PRACTICA DEFINITIVA**


---



## EJEMPLO 181: CONECTIVIDAD DIRECTA AWS DIRECT CONNECT CON BGP


> 🏢 **ESCENARIO REAL:**
Una empresa financiera contrata un enlace dedicado de fibra de 10 Gbps (AWS Direct
Connect) hacia la region us-east-1 de Amazon Web Services. Se configura una subinterfaz
802.1Q (VLAN 100) y una sesion eBGP hacia la Virtual Private Gateway (VGW) de AWS.


#### 🌐 DIAGRAMA:

```text
  [ROUTER BORDE EMPRESA] <=== Fibra Direct Connect (VLAN 100) ===> [AWS DIRECT CONNECT LOCATION] ===> [VPC AWS]
  AS 65000 (IP 169.254.100.2)                                    AS 64512 (IP 169.254.100.1)
```


#### 💻 CONFIGURACION CISCO IOS-XE:

```cisco
interface GigabitEthernet0/0/1.100
 description UPLINK_AWS_DIRECT_CONNECT
 encapsulation dot1Q 100
 ip address 169.254.100.2 255.255.255.252
 no shutdown
exit

router bgp 65000
 neighbor 169.254.100.1 remote-as 64512   ! ASN de AWS
 neighbor 169.254.100.1 password ClaveAWSBgp2026!
 address-family ipv4
  network 10.0.0.0 mask 255.255.0.0      ! Anunciar red corporativa a la nube
  neighbor 169.254.100.1 activate
 exit-address-family
exit
```


#### 🔍 Verificación:

```cisco
R1# show ip bgp neighbors 169.254.100.1 routes
```



## EJEMPLO 182: CONECTIVIDAD DIRECTA MICROSOFT AZURE EXPRESSROUTE CON eBGP


> 🏢 **ESCENARIO REAL:**
Interconectar el Datacenter con Microsoft Azure mediante un circuito ExpressRoute.
Se utiliza una sesion eBGP con direccionamiento `/30` provisto por Microsoft.


#### 💻 CONFIGURACION CISCO:

```cisco
interface GigabitEthernet0/0/2.200
 description UPLINK_AZURE_EXPRESSROUTE
 encapsulation dot1Q 200
 ip address 192.168.100.2 255.255.255.252
 no shutdown
exit

router bgp 65000
 neighbor 192.168.100.1 remote-as 12076   ! ASN Publico Oficial de Microsoft Azure
 neighbor 192.168.100.1 password ClaveAzureER2026!
 address-family ipv4
  neighbor 192.168.100.1 activate
 exit-address-family
exit
```


#### 🔍 Verificación:

```cisco
R1# show ip bgp summary | include 12076
```



## EJEMPLO 183: GOOGLE CLOUD DEDICATED INTERCONNECT CON CLOUD ROUTER


> 🏢 **ESCENARIO REAL:**
Establecer sesion BGP con Google Cloud Router (GCP) mediante un VLAN Attachment (Interconnect).


#### 💻 CONFIGURACION CISCO:

```cisco
interface GigabitEthernet0/0/3.300
 description UPLINK_GOOGLE_CLOUD_INTERCONNECT
 encapsulation dot1Q 300
 ip address 169.254.200.2 255.255.255.252
exit

router bgp 65000
 neighbor 169.254.200.1 remote-as 16550   ! ASN Oficial de Google Cloud
 address-family ipv4
  neighbor 169.254.200.1 activate
 exit-address-family
exit
```



## EJEMPLO 184: ARQUITECTURA SD-WAN: DESACOPLAMIENTO DE LOS 4 PLANOS


> 🏢 **ESCENARIO REAL:**
En redes SD-WAN (Software-Defined WAN), la gestion y el control ya no se ejecutan
en cada router individual. Se divide la red en cuatro planos orquestados:
1. Plano de Orquestacion (vBond): Autentica y valida que los routers pertenezcan a la empresa.
2. Plano de Gestion (vManage): Panel grafico unico para monitoreo y despliegue de politicas.
3. Plano de Control (vSmart): Cerebro centralizado que calcula rutas y politicas de seguridad.
4. Plano de Datos (cEdge / vEdge): Routers fisicos en las sucursales que transportan paquetes.



## EJEMPLO 185: SD-WAN UNDERLAY vs OVERLAY: TUNELIZACION AUTOMATICA


> 🏢 **ESCENARIO REAL:**
- Underlay: Las conexiones fisicas contratadas (MPLS, Fibra Internet, Celular 5G).
- Overlay: Una malla de tuneles IPsec cifrados que los routers de las sucursales
  levantan automaticamente entre si a traves de cualquier transporte disponible.


#### 🌐 DIAGRAMA:

```text
  [SUCURSAL 1] =================== Malla Overlay Cifrada IPsec ===================> [SUCURSAL 2]
       ||                                                                                  ||
  +----+----+ (Transporte Underlay: MPLS + Internet de Banda Ancha + 5G)              +----+----+
```



## EJEMPLO 186: PROTOCOLO OMP (OVERLAY MANAGEMENT PROTOCOL) EN SD-WAN


> 🏢 **ESCENARIO REAL:**
Los routers cEdge no corren BGP ni OSPF entre ellos. Utilizan OMP (un protocolo similar
a BGP) para comunicarse exclusivamente con el controlador vSmart, intercambiando:
1. Rutas de servicio de los usuarios (OMP Routes).
2. TLOCs (Transport Locations: IP publica, color del transporte y clave de cifrado).


#### 💻 CONFIGURACION CISCO SD-WAN (CEDGE):

```cisco
sdwan
 omp
  no shutdown
  send-path-limit 16
  ecmp-limit 8
 exit
exit
```


#### 🔍 Verificación:

```cisco
CEDGE# show sdwan omp routes
CEDGE# show sdwan omp tlocs
```



## EJEMPLO 187: BFD PATH QUALITY MONITORING EN TIEMPO REAL


> 🏢 **ESCENARIO REAL:**
En SD-WAN, BFD no solo detecta caidas; mide continuamente la CALIDAD del enlace:
Calcula milisegundo a milisegundo: Latencia (RTT), Jitter (variacion) y Packet Loss (perdida).

COMANDO DE DIAGNOSTICO EN VIVO (CEDGE):
CEDGE# show sdwan bfd sessions
System IP       Site ID  Color        State  Latency(ms)  Jitter(ms)  Loss(%)
10.255.0.1      10       biz-internet up     12           2           0
10.255.0.1      10       mpls         up      4           1           0



## EJEMPLO 188: APPLICATION-AWARE ROUTING (AAR): CONMUTACION DINAMICA


> 🏢 **ESCENARIO REAL:**
Una llamada de VoIP viaja normalmente por Internet. Si el enlace de Internet sufre
congestion y el Jitter supera los 10 ms o la perdida sube a mas del 1%, el router
SD-WAN desvia automaticamente la llamada al enlace MPLS en menos de un segundo.


#### 💻 CONFIGURACION DE POLITICA SLA EN CONTROLADOR:

```text
policy
 sla-class SLA_VOIP
  latency 150
  jitter 10                         ! Maximo 10 ms de jitter tolerado
  loss 1                            ! Maximo 1% de paquetes perdidos
 exit
 app-aware-policy ENVIAR_VOIP_SEGURO
  sequence 10
   match
    app-list APLICACION_ZOOM_TEAMS
   action
    sla-class SLA_VOIP preferred-color mpls
   exit
 exit
exit
```



## EJEMPLO 189: CLOUD ONRAMP PARA SAAS (OFFICE 365 Y SALESFORCE)


> 🏢 **ESCENARIO REAL:**
En lugar de enviar el trafico de Microsoft Teams y Office 365 al Datacenter para salir
a Internet (aumentando la latencia), el router SD-WAN mide cual de sus dos salidas a
Internet locales tiene mejor rendimiento y entrega el trafico directo (Direct Internet Access - DIA).


#### 💻 CONFIGURACION CISCO SD-WAN:

```cisco
policy
 cloud-onramp saas
  app office365
   path-preference local-internet
  exit
 exit
exit
```



## EJEMPLO 190: INTEGRACION SASE CON ZSCALER MEDIANTE TUNELES IPSEC


> 🏢 **ESCENARIO REAL:**
Proteger a los empleados en su navegacion web mediante Security Service Edge (SSE).
El router SD-WAN de la sucursal abre dos tuneles IPsec automaticos hacia el nodo
de seguridad en la nube de Zscaler (Zscaler Internet Access - ZIA).


#### 🌐 DIAGRAMA:

```text
  [PC EMPLEADO] ===> [ROUTER SD-WAN] === Tunel IPsec Cifrado ===> [NUBE ZSCALER ZIA] ===> [INTERNET]
                                                                  (Inspeccion Antivirus/DLP)
```


#### 💻 CONFIGURACION EN CEDGE:

```text
interface Tunnel100
 description TUNEL_HACIA_ZSCALER_PRIMARIO
 ip address 172.31.254.2 255.255.255.252
 tunnel source GigabitEthernet0/1
 tunnel destination 165.225.10.1    ! IP del Data Center de Zscaler
 tunnel mode ipsec ipv4
 no shutdown
exit
```



## EJEMPLO 191: SEGMENTACION MULTI-TENANT CON VPNS DE SERVICIO (VPNs 1 A 511)


> 🏢 **ESCENARIO REAL:**
En SD-WAN, las VRFs se llaman VPNs:
- VPN 0: Transporte WAN (Underlay hacia los ISPs).
- VPN 512: Gestion fuera de banda (OOB).
- VPN 10: Datos Corporativos.
- VPN 20: Terminales Punto de Venta (PCI-DSS).


#### 💻 CONFIGURACION CISCO SD-WAN:

```cisco
vpn 10
 name DATOS_CORPORATIVOS
 interface GigabitEthernet0/0/1
  ip address 192.168.10.1 255.255.255.0
  no shutdown
 exit
exit

vpn 20
 name PUNTO_DE_VENTA_PCI
 interface GigabitEthernet0/0/2
  ip address 192.168.20.1 255.255.255.0
  no shutdown
 exit
exit
```



## EJEMPLO 192: TOPOLOGIA HUB-AND-SPOKE CONTROLADA POR VSMART


> 🏢 **ESCENARIO REAL:**
Por requerimientos de seguridad, las sucursales terciarias tienen prohibido hablar
entre ellas directamente; todo el trafico debe atravesar obligatoriamente el Hub Central.
El controlador vSmart aplica una politica centralizada que filtra los TLOCs.


#### 💻 CONFIGURACION CENTRALIZADA VSMART:

```text
policy
 control-policy FORZAR_HUB_AND_SPOKE
  sequence 10
   match route
    site-list SUCURSALES_TIENDAS
   action accept
    set tloc 10.255.0.1 color mpls   ! Forzar Next-Hop hacia el Hub
   exit
 exit
exit
```



## EJEMPLO 193: ZERO-TOUCH PROVISIONING (ZTP) DE SUCURSAL NUEVA


> 🏢 **ESCENARIO REAL:**
Un tecnico de campo llega a una nueva tienda en Cancun, saca el router Cisco de la caja,
conecta el cable de Internet del ISP y lo enciende. El router contacta automaticamente
al servidor `ztp.cisco.com`, descarga sus certificados y levanta la red en 5 minutos.

VERIFICACION EN CONSOLA LOCAL:
CEDGE# show sdwan control connections
(Muestra sesiones TLS/DTLS activas hacia vManage, vBond y vSmart en estado 'up').



## EJEMPLO 194: CONEXION HIBRIDA MULTI-CLOUD (AWS DIRECT CONNECT + AZURE ER)


> 🏢 **ESCENARIO REAL:**
Una arquitectura empresarial aloja sus bases de datos en Amazon AWS y sus aplicaciones
analiticas en Microsoft Azure. El router de borde WAN Core conmuta paquetes entre
ambas nubes publicas a velocidad de fibra con latencia menor a 5 ms.


#### 🌐 DIAGRAMA:

```text
  [AWS VPC] <--- Direct Connect ---> [ROUTER CORE EDGE] <--- ExpressRoute ---> [AZURE VNET]
```



## EJEMPLO 195: FAILOVER INTELIGENTE CON POLITICA DE COSTO FINANCIERO (5G METERED)


> 🏢 **ESCENARIO REAL:**
La sucursal tiene un enlace de Fibra Optica (tarifa plana ilimitada) y un respaldo
celular 5G (con cobro por Gigabyte consumido). El router solo activa el modem 5G
si la fibra cae por completo, e inmediatamente bloquea YouTube y streaming para
no agotar el plan de datos.


#### 💻 CONFIGURACION EN CEDGE:

```text
policy
 data-policy BLOQUEAR_STREAMING_EN_5G
  sequence 10
   match
    app-family streaming
   action drop
  exit
  sequence 20
   action accept
  exit
 exit
exit
```



## EJEMPLO 196: HUAWEI NETENGINE SD-WAN CON IMASTER NCE


> 🏢 **ESCENARIO REAL:**
Implementacion de SD-WAN en routers Huawei NetEngine (AR6000 / AR1000) gestionados
por el controlador centralizado iMaster NCE.


#### 💻 CONFIGURACION HUAWEI VRP:

```text
# 1. Registro del router con el controlador iMaster NCE
agile-controller
 controller-ip 198.51.100.10 port 10020
 source-interface GigabitEthernet0/0/1
#
# 2. Habilitar EVPN en el Overlay SD-WAN
evpn
#
```


#### 🔍 Verificación:

```cisco
<ROUTER_HW> display agile-controller status
```



## EJEMPLO 197: SEGURIDAD ZERO-TRUST EN BORDE WAN CON 802.1X Y MACSEC


> 🏢 **ESCENARIO REAL:**
Para evitar que un atacante desconecte el cable de red de una computadora y conecte
su propia laptop para infiltrarse en la sucursal, se habilita autenticacion por
puerto IEEE 802.1X con servidor RADIUS (Cisco ISE) y cifrado de hardware MACsec (802.1AE).


#### 💻 CONFIGURACION CISCO:

```cisco
dot1x system-auth-control

interface GigabitEthernet1/0/1
 description PUERTO_USUARIO_ZERO_TRUST
 switchport mode access
 authentication port-control auto
 dot1x pae authenticator
 macsec
exit
```


#### 🔍 Verificación:

```cisco
SWITCH# show authentication sessions interface GigabitEthernet1/0/1
```



## EJEMPLO 198: ENRUTAMIENTO SIMETRICO PARA CLUSTERS DE FIREWALLS (ECMP AFFINITY)


> 🏢 **ESCENARIO REAL:**
Dos Firewalls de Proxima Generacion (Fortinet / Palo Alto) operan en modo Activo/Activo.
Para evitar que el paquete de ida cruce por FW1 y el de regreso por FW2 (rompiendo
la sesion TCP), los routers Core aplican Symmetric Hashing basado en IP origen y destino.


#### 💻 CONFIGURACION CISCO:

```cisco
ip cef load-sharing algorithm include-ports source destination symmetric
exit
```


#### 🔍 Verificación:

```cisco
CORE# show ip cef exact-route 10.1.1.50 172.16.1.100
```



## EJEMPLO 199: RESILIENCIA WAN INTEGRADA: BGP BFD + IP SLA + FAST REROUTE


> 🏢 **ESCENARIO REAL:**
En una institucion bursatil, la perdida de conectividad durante 1 segundo causa
perdidas millonarias. Se integran BFD en el plano de control (300 ms) junto con
BGP PIC (Prefix Independent Convergence) en el plano de datos para lograr una
conmutacion completa en MENOS DE 50 MILISEGUNDOS.


#### 💻 CONFIGURACION CISCO IOS-XE:

```cisco
router bgp 65000
 address-family ipv4
  bgp additional-paths select backup ! Pre-calcula ruta de respaldo en hardware
  neighbor 10.0.0.2 advertise additional-paths backup
 exit-address-family
exit
```


#### 🔍 Verificación:

```cisco
R1# show ip cef 0.0.0.0/0 internal | include Repair
```



## EJEMPLO 200: ARQUITECTURA MAESTRA CORPORATIVA INTEGRAL DEFINITIVA


> 🏢 **ESCENARIO REAL:**
La cumbre de la ingenieria de redes empresariales modernas: Una infraestructura
completa interconectando:
1. Datacenter Principal: Fabric Spine-Leaf con VXLAN BGP EVPN y Anycast Gateway.
2. Interconexion Multi-Cloud: Nube hibrida conectando Amazon AWS (Direct Connect)
   y Microsoft Azure (ExpressRoute) en Capa 3 con BGP.
3. Backbone de Transporte Carrier: Red MPLS L3VPN con Segment Routing (SR-MPLS).
4. Red WAN Empresarial: SD-WAN inteligente con conmutacion automatica por Jitter (AAR),
   cifrado IPsec IKEv2 y aceleracion BFD en 200 sucursales secundarias y terciarias.
5. Seguridad Perimetral y Borde: Firewalls NGFW en cluster Activo/Activo con
   enrutamiento simetrico, redireccion SASE Zscaler y politicas Zero-Trust en puertos LAN.

DIAGRAMA MAESTRO DE LA INFRAESTRUCTURA:
```text
                     +---------------------------------------+
                     |           NUBE MULTI-CLOUD            |
                     |   [AWS Direct Connect]   [Azure ER]   |
                     +-------------------+-------------------+
                                         |
                                         v
   +-------------------------------------+-------------------------------------+
   |                      DATACENTER CORPORATIVO CORE                          |
   |              Spine-Leaf Fabric (VXLAN BGP EVPN + L3VNI)                   |
   |              Firewalls NGFW en Alta Disponibilidad + VRRP                 |
   +-------------------------------------+-------------------------------------+
                                         |
                                         v
                     +---------------------------------------+
                     |         WAN EMPRESARIAL SD-WAN        |
                     |  (MPLS L3VPN + Fibra Internet + 5G)   |
                     |  Plano de Control OMP / BFD Tracking  |
                     +-------------------+-------------------+
                                         |
         +-------------------------------+-------------------------------+
         |                                                               |
         v                                                               v
  [SUCURSALES REGIONALES]                                         [200 SUCURSALES TIENDAS]
  (Dual cEdge / Dual-ISP)                                         (IP Dinamica / ZTP / SASE)

COMANDOS FINALES DE AUDITORIA Y GESTION MAESTRA:
# show ip route summary
# show bgp l2vpn evpn summary
# show mpls forwarding-table
# show sdwan control connections
# show sdwan bfd sessions
```


## # show bfd neighbors
