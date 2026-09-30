# PARTE 9: MULTICAST Y CALIDAD DE SERVICIO (QoS) WAN (EJEMPLOS 161 AL 180)

> **ENRUTAMIENTO AVANZADO Y REDES WAN - GUIA PRACTICA DEFINITIVA**


---



## EJEMPLO 161: FUNDAMENTOS DE MULTICAST IP: RANGOS Y MAPEO MAC (01:00:5E)


> 🏢 **ESCENARIO REAL:**
En aplicaciones de transmision de video en vivo (CCTV) o cotizaciones bursatiles
financieras, un servidor envia un unico flujo de paquetes a una IP de Grupo Clase D
(`224.0.0.0` a `239.255.255.255`). Los switches calculan la direccion MAC de Capa 2
mapeando los ultimos 23 bits de la IP dentro del prefijo OUI `01:00:5E`.


#### 🌐 DIAGRAMA:

```text
  [SERVIDOR VIDEO] === Envia 1 solo paquete a 239.1.1.1 ===> [RED MULTICAST] ===> [500 Espectadores reciben el flujo]
```


#### 💻 CONFIGURACION CISCO IOS:

```cisco
! Habilitar enrutamiento Multicast globalmente:
ip multicast-routing
exit
```


#### 🔍 Verificación:

```cisco
R1# show ip mroute
```



## EJEMPLO 162: IGMP SNOOPING EN SWITCHES L2 CONTRA SATURACION DE PUERTOS


> 🏢 **ESCENARIO REAL:**
Sin IGMP Snooping, los switches tratan el trafico multicast como broadcast y lo inundan
por los 48 puertos, colapsando la red. Con IGMP Snooping activado, el switch inspecciona
los mensajes IGMP Join y entrega el video EXCLUSIVAMENTE a las PCs que lo solicitaron.


#### 💻 CONFIGURACION CISCO (SWITCH):

```cisco
ip igmp snooping
ip igmp snooping vlan 10
exit
```


#### 🔍 Verificación:

```cisco
SWITCH# show ip igmp snooping groups
```



## EJEMPLO 163: PIM SPARSE-MODE (PIM-SM) CON RENDEZVOUS POINT (RP) ESTATICO


> 🏢 **ESCENARIO REAL:**
Implementar PIM Sparse-Mode (RFC 7761) en la red corporativa. Todas las fuentes de
video y todos los receptores se registran contra un router central denominado RP (Rendezvous Point).


#### 🌐 DIAGRAMA:

```text
  [CAMARA CCTV] ---> [ROUTER ORIGEN] ----> [RENDEZVOUS POINT (RP)] <---- [ROUTER RECEPTOR] <--- [PC VIGILANCIA]
```


#### 💻 CONFIGURACION CISCO IOS (EN TODOS LOS ROUTERS):

```cisco
ip multicast-routing
ip pim rp-address 10.255.0.100       ! IP fija del RP Central

interface GigabitEthernet0/0/1
 ip pim sparse-mode                  ! Habilita PIM en la interfaz
 no shutdown
exit
```


#### 🔍 Verificación:

```cisco
R1# show ip pim neighbor
R1# show ip pim rp mapping
```



## EJEMPLO 164: AUTO-RP PROPIETARIO DE CISCO CON CANDIDATE RPs Y MAPPING AGENTS


> 🏢 **ESCENARIO REAL:**
Distribuir dinamicamente la IP del RP sin configurar `ip pim rp-address` a mano en
cientos de routers. Los Candidate RPs anuncian su disponibilidad y el Mapping Agent (MA)
elige al mejor y lo difunde a todos los routers por el grupo 224.0.1.40.


#### 💻 CONFIGURACION CISCO:

```cisco
! En Router Candidato a RP (R1):
ip pim send-rp-announce Loopback0 scope 16 group-list 1
access-list 1 permit 239.0.0.0 0.255.255.255

! En Router Mapping Agent (R2):
ip pim send-rp-discovery Loopback0 scope 16
```


#### 🔍 Verificación:

```cisco
R_CLIENTE# show ip pim rp-hash 239.1.1.1
```



## EJEMPLO 165: PIM BOOTSTRAP ROUTER (BSR - RFC 5059) ESTANDAR ABIERTO


> 🏢 **ESCENARIO REAL:**
Mecanismo estandarizado para redes multi-marca (Cisco, Huawei, Juniper) que reemplaza
a Auto-RP para la eleccion automatica y tolerante a fallos del Rendezvous Point.


#### 💻 CONFIGURACION CISCO:

```cisco
! En el Router elegido como BSR Central:
ip pim bsr-candidate Loopback0 0

! En el Router Candidato a RP:
ip pim rp-candidate Loopback0
```


#### 🔍 Verificación:

```cisco
R1# show ip pim bsr-router
```



## EJEMPLO 166: ANYCAST RP CON MSDP PARA ALTA DISPONIBILIDAD Y BALANCEO


> 🏢 **ESCENARIO REAL:**
Si un unico RP falla, toda la red multicast muere. Con Anycast RP, dos routers RP
distintos comparten la misma direccion IP Loopback (`10.255.255.255/32`) y sincronizan
las fuentes activas mediante MSDP (Multicast Source Discovery Protocol).


#### 🌐 DIAGRAMA:

```text
  [RP 1: 10.255.255.255] <===== Sesion MSDP (TCP 639) =====> [RP 2: 10.255.255.255]
  (Sede Monterrey)                                           (Sede Queretaro)
```


#### 💻 CONFIGURACION CISCO (RP 1):

```cisco
interface Loopback100
 description ANYCAST_RP_VIP
 ip address 10.255.255.255 255.255.255.255
 ip pim sparse-mode
exit

ip msdp peer 10.255.0.2 connect-source Loopback0
ip msdp originator-id Loopback0
```


#### 🔍 Verificación:

```cisco
RP1# show ip msdp peer
RP1# show ip msdp sa-cache
```



## EJEMPLO 167: PIM SOURCE-SPECIFIC MULTICAST (SSM - RANGO 232.0.0.0/8)


> 🏢 **ESCENARIO REAL:**
Para servicios de streaming modernos donde el cliente conoce de antemano la IP del
servidor emisor, PIM-SSM elimina por completo la necesidad de Rendezvous Points (RPs).
El arbol de distribucion (*,G) se reemplaza inmediatamente por un arbol directo (S,G).


#### 💻 CONFIGURACION CISCO:

```cisco
ip pim ssm default                  ! Habilita el rango 232.0.0.0/8 para SSM
```


#### 🔍 Verificación:

```cisco
R1# show ip pim group-map 232.1.1.1
```



## EJEMPLO 168: PIM BIDIRECTIONAL (BIDIR-PIM) PARA MUCHOS A MUCHOS


> 🏢 **ESCENARIO REAL:**
En aplicaciones de teleconferencias interactivas donde miles de usuarios emiten y
reciben video a la vez, los arboles de origen (S,G) saturarian la memoria del router.
Bidir-PIM construye un arbol compartido bidireccional unico mediante Designated Forwarders (DF).


#### 💻 CONFIGURACION CISCO:

```cisco
ip pim bidir-enable
ip pim rp-address 10.255.0.1 bidir
```


#### 🔍 Verificación:

```cisco
R1# show ip pim df
```



## EJEMPLO 169: MULTICAST SOBRE MPLS L3VPN (mVPN PROFILE 0 / ROSEN GRE)


> 🏢 **ESCENARIO REAL:**
Un banco transmite cotizaciones de acciones a 200 sucursales a traves de su red MPLS
L3VPN privada. El Carrier utiliza un Default MDT (Multicast Distribution Tree) encapsulado.


#### 💻 CONFIGURACION CISCO (ROUTER PE):

```cisco
vrf definition CLIENTE_BANCO
 rd 65000:100
 route-target export 65000:100
 route-target import 65000:100
 address-family ipv4
  mdt default 239.1.1.100           ! Grupo multicast en el Core del Carrier
 exit-address-family
exit
```


#### 🔍 Verificación:

```cisco
PE1# show ip pim vrf CLIENTE_BANCO mdt
```



## EJEMPLO 170: IGMP QUERIER EN SWITCHES L2 CUANDO NO HAY ROUTER MULTICAST


> 🏢 **ESCENARIO REAL:**
En una red cerrada aislada de camaras de seguridad NVR (sin salida a routers),
el IGMP Snooping deja de funcionar porque nadie envia los mensajes periodicos
IGMP General Query. Se configura un switch como IGMP Querier maestro.


#### 💻 CONFIGURACION CISCO (SWITCH L2):

```cisco
ip igmp snooping querier
ip igmp snooping querier address 192.168.10.254
exit
```


#### 🔍 Verificación:

```cisco
SWITCH# show ip igmp snooping querier
```



## EJEMPLO 171: ARQUITECTURA DIFFSERV: DSCP (CS, AF, EF) Y CLASIFICACION


> 🏢 **ESCENARIO REAL:**
En enlaces WAN de telecomunicaciones, la voz sobre IP (VoIP), el trafico critico
de bases de datos ERP y la navegacion web recreativa compiten por el ancho de banda.
El modelo Differentiated Services (DiffServ - RFC 2474) utiliza el campo ToS de 6 bits
(DSCP) en el encabezado IP para etiquetar paquetes en la entrada de la red:
- EF (Expedited Forwarding - DSCP 46): Trafico de maxima prioridad (Voz VoIP).
- AF (Assured Forwarding - ej. AF31, AF21): Aplicaciones empresariales criticas.
- CS (Class Selector / Default - DSCP 0): Trafico Best-Effort (Internet, YouTube).



## EJEMPLO 172: MARCADOS DSCP vs CoS DE CAPA 2 (802.1p)


> 🏢 **ESCENARIO REAL:**
Un telefono IP de escritorio envia tramas Ethernet marcadas con CoS 5 (Capa 2).
El switch de acceso debe traducir ese CoS 5 a DSCP EF (valor decimal 46) en Capa 3
para que la prioridad sobreviva a traves de todos los routers de la red WAN.


#### 💻 CONFIGURACION CISCO (SWITCH ACCESO):

```cisco
mls qos
mls qos map cos-dscp 0 8 16 24 32 46 48 56   ! CoS 5 mapea a DSCP 46 (EF)

interface FastEthernet0/1
 description TELEFONO_IP_CISCO
 switchport mode access
 switchport voice vlan 100
 mls qos trust cos                  ! Confia en el marcado del telefono
exit
```



## EJEMPLO 173: MARCADOS MQC: CLASS-MAP Y POLICY-MAP MODULAR


> 🏢 **ESCENARIO REAL:**
Clasificar el trafico de los servidores de Bases de Datos SAP (`puerto TCP 3200`)
y marcarlo con DSCP AF31 para garantizar prioridad frente al trafico comun.


#### 💻 CONFIGURACION CISCO IOS:

```cisco
ip access-list extended ACL_TRAFICO_SAP
 permit tcp any any eq 3200
exit

class-map match-all CLASE_SAP_ERP
 match access-group name ACL_TRAFICO_SAP
exit

policy-map POLITICA_MARCADO_ENTRADA
 class CLASE_SAP_ERP
  set dscp af31
 class class-default
  set dscp default
exit

interface GigabitEthernet0/0/0
 service-policy input POLITICA_MARCADO_ENTRADA
exit
```


#### 🔍 Verificación:

```cisco
R1# show policy-map interface GigabitEthernet0/0/0
```



## EJEMPLO 174: TRAFFIC POLICING (VIGILANCIA CON DESCARTE DE EXCESOS)


> 🏢 **ESCENARIO REAL:**
La red Wi-Fi de Invitados no debe consumir mas de 10 Mbps del enlace WAN.
Traffic Policing mide la velocidad con el algoritmo Token Bucket: si los invitados
superan 10 Mbps, el exceso se DESCARTA INMEDIATAMENTE en el acto sin buffer.


#### 💻 CONFIGURACION CISCO IOS:

```cisco
class-map match-any CLASE_INVITADOS
 match access-group name ACL_INVITADOS
exit

policy-map POLITICA_LIMITAR_INVITADOS
 class CLASE_INVITADOS
  police 10000000 conform-action transmit exceed-action drop
exit

interface GigabitEthernet0/0/1
 service-policy output POLITICA_LIMITAR_INVITADOS
exit
```


#### 🔍 Verificación:

```cisco
R1# show policy-map interface GigabitEthernet0/0/1 | include drop
```



## EJEMPLO 175: TRAFFIC SHAPING (MOLDEADO CON BUFFER DE ESPERA PARA WAN)


> 🏢 **ESCENARIO REAL:**
La empresa tiene una interfaz GigabitEthernet (1 Gbps) conectada al carrier, pero
solo contrato un enlace de 100 Mbps con el ISP. Si el router envia a 1 Gbps, el ISP
descartara los paquetes. Traffic Shaping retrasa suavemente los paquetes en memoria
(buffers) modulando la salida a exactamente 100 Mbps continuos.


#### 💻 CONFIGURACION CISCO IOS:

```cisco
policy-map SHAPE_WAN_100M
 class class-default
  shape average 100000000           ! 100 Mbps
exit

interface GigabitEthernet0/0/1
 service-policy output SHAPE_WAN_100M
exit
```


#### 🔍 Verificación:

```cisco
R1# show policy-map interface GigabitEthernet0/0/1
```



## EJEMPLO 176: CBWFQ (CLASS-BASED WEIGHTED FAIR QUEUEING)


> 🏢 **ESCENARIO REAL:**
Repartir un enlace de 50 Mbps de forma equitativa: 40% para el Sistema ERP, 30% para
la navegacion web comercial, y 30% restante para el correo electronico y respaldos.


#### 💻 CONFIGURACION CISCO IOS:

```cisco
policy-map CBWFQ_REPARTO
 class CLASE_ERP
  bandwidth percent 40
 class CLASE_WEB
  bandwidth percent 30
 class class-default
  bandwidth percent 30
exit

interface GigabitEthernet0/0/1
 service-policy output CBWFQ_REPARTO
exit
```



## EJEMPLO 177: LLQ (LOW LATENCY QUEUEING) CON COLA PRIORITARIA PARA VOIP


> 🏢 **ESCENARIO REAL:**
Garantizar que los paquetes de voz VoIP jamas esperen detras de una descarga de archivo.
El comando `priority` crea una cola estricta (Strict Priority Queue) que atiende
los paquetes de voz antes que cualquier otra clase de trafico.


#### 💻 CONFIGURACION CISCO IOS:

```cisco
class-map match-any CLASE_VOZ
 match ip dscp ef
exit

policy-map POLITICA_EMPRESARIAL_LLQ
 class CLASE_VOZ
  priority 15000                    ! Reserva 15 Mbps prioritarios absolutos
 class CLASE_ERP
  bandwidth 25000                   ! 25 Mbps garantizados
 class class-default
  fair-queue
exit

interface GigabitEthernet0/0/1
 service-policy output POLITICA_EMPRESARIAL_LLQ
exit
```


#### 🔍 Verificación:

```cisco
R1# show policy-map interface GigabitEthernet0/0/1
```



## EJEMPLO 178: PREVENCION DE CONGESTION CON WRED (WEIGHTED RED)


> 🏢 **ESCENARIO REAL:**
Evitar el problema de "Sincronizacion Global TCP" (cuando todas las descargas TCP
frenan a la vez al llenarse el buffer de la interfaz). WRED descarta paquetes
aleatoriamente de forma preventiva ANTES de que el buffer se sature por completo.


#### 💻 CONFIGURACION CISCO IOS:

```cisco
policy-map POLITICA_CONGESTION
 class class-default
  random-detect dscp-based          ! WRED basado en valores DSCP
exit

interface GigabitEthernet0/0/1
 service-policy output POLITICA_CONGESTION
exit
```


#### 🔍 Verificación:

```cisco
R1# show policy-map interface GigabitEthernet0/0/1
```



## EJEMPLO 179: REPLICACION DE DSCP EN TUNELES IPSEC (QoS OVER IPsec)


> 🏢 **ESCENARIO REAL:**
Cuando un router cifra un paquete de voz (DSCP EF) con IPsec, el encabezado IPsec ESP
externo oculta el valor original. Los routers del Carrier no sabrian que es voz y lo
tratarian como Best-Effort. Se fuerza la copia del DSCP interno al encabezado externo.


#### 💻 CONFIGURACION CISCO:

```cisco
crypto ipsec profile PROF_IPSEC_QOS
 set transform-set TS_IPSEC
 ! Por defecto en IOS-XE moderno se copia el ToS; en IOS clasico:
 qos pre-classify                   ! Permite clasificar antes de cifrar
exit

interface Tunnel1
 qos pre-classify
 service-policy output POLITICA_EMPRESARIAL_LLQ
exit
```


#### 🔍 Verificación:

```cisco
R1# show policy-map interface Tunnel1
```



## EJEMPLO 180: QoS COMPLETA EN ROUTERS HUAWEI VRP (CLASSIFIER, BEHAVIOR, POLICY)


> 🏢 **ESCENARIO REAL:**
Implementacion de clasificacion y cola de baja latencia equivalente en routers Huawei AR.


#### 💻 CONFIGURACION HUAWEI VRP:

```text
# 1. Traffic Classifier
traffic classifier CLASIFICAR_VOZ
 if-match dscp ef
#
# 2. Traffic Behavior
traffic behavior ACCION_VOZ
 queue priority bandwidth 15000     ! 15 Mbps de LLQ
#
# 3. Traffic Policy
traffic policy POLITICA_QOS_HUAWEI
 classifier CLASIFICAR_VOZ behavior ACCION_VOZ
#
# 4. Aplicacion en interfaz WAN
interface GigabitEthernet0/0/1
 traffic-policy POLITICA_QOS_HUAWEI outbound
#
```


#### 🔍 Verificación:


## <ROUTER_HW> display traffic policy applied-record
