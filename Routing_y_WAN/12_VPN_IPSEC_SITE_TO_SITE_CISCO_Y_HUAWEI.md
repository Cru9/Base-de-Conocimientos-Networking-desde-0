# 12. MANUAL DE CONEXIONES VPN IPSEC SITE-TO-SITE SOBRE ISP (CISCO Y HUAWEI)

> **ENRUTAMIENTO AVANZADO Y TECNOLOGIAS WAN (ROUTING & WAN ARCHITECTURE)**


---



## 1. ¿QUE ES UNA VPN IPSEC SITE-TO-SITE Y POR QUE SE CONSTRUYE SOBRE EL ISP?

En una arquitectura WAN empresarial, las sucursales remotas (plantas, oficinas de ventas,
almacenes) y la sede central estan separadas geograficamente por cientos o miles de
kilometros. Contratar lineas privadas dedicadas punto a punto o enlaces MPLS gestionados
para cada sucursal resulta prohibitivo en costos financieros y lento en aprovisionamiento.

La solucion estandar en la industria moderna:
Contratar conexiones a Internet de banda ancha comercial o fibra optica empresarial
con Proveedores de Servicios de Internet (ISPs) locales en cada sitio, y construir
un TUNEL VPN IPSEC SITE-TO-SITE (Sitio a Sitio) sobre la red publica del ISP.

El Rol del ISP (La Red Underlay):
- El ISP actua exclusivamente como un "Medio de Transporte Inseguro" (Untrusted Transport).
- El ISP solo ve paquetes IP con cabeceras externas que viajan entre las direcciones IP
  publicas de los routers de borde.
- Todo el contenido sensible interno (sistemas ERP, transacciones bancarias, llamadas VoIP,
  archivos confidenciales) viaja 100% CIFRADO y encapsulado dentro de IPsec.
- Ningun operador del ISP ni ningun atacante en Internet puede interceptar, alterar o
  espiar los paquetes que viajan dentro del tunel.



## 2. ARQUITECTURA DE SEGURIDAD IPSEC (ESP, IKE, DH, HASH Y NAT-T)

IPsec (Internet Protocol Security - Conjunto de RFCs del IETF) es una suite de protocolos
criptograficos que opera en la Capa 3 (Red) del modelo OSI, proporcionando:
1. Confidencialidad: Mediante cifrado simetrico de grado militar (AES-256).
2. Integridad de Datos: Mediante funciones hash criptograficas (HMAC-SHA-256 / SHA-512).
3. Autenticacion del Origen: Mediante Claves Precompartidas (PSK - Pre-Shared Keys) o
   Certificados Digitales X.509 de Infraestructura de Clave Publica (PKI).
4. Proteccion Antirreproduccion (Anti-Replay): Utiliza numeros de secuencia para rechazar
   paquetes capturados y retransmitidos maliciosamente.

LOS PROTOCOLOS INTEGRANTES DE IPSEC:
- ESP (Encapsulating Security Payload - Protocolo IP 50):
  * Cifra los datos originales, proporciona autenticacion y proteccion anti-replay.
  * Se utiliza en el 99.9% de las VPNs empresariales del mundo.
- AH (Authentication Header - Protocolo IP 51):
  * Autentica el encabezado IP pero NO CIFRA NADA (cero confidencialidad).
  * Incompatible con traductores de direcciones de red (NAT). Practicamente extinto.
- IKE (Internet Key Exchange - UDP puerto 500):
  * Protocolo de senalizacion que negocia de forma automatica y segura las claves,
    los algoritmos criptograficos y las asociaciones de seguridad (SAs).
- NAT-Traversal (NAT-T - RFC 3948 - UDP puerto 4500):
  * Si uno de los routers de la sucursal tiene una IP privada provista por el modem/ONT
    del ISP (Carrier-Grade NAT o router residencial con NAT), los paquetes ESP puros
    (IP 50) fallarian porque no tienen puertos TCP/UDP para ser traducidos.
  * NAT-T detecta automaticamente la presencia de NAT y encapsula el paquete ESP dentro
    de un datagrama UDP en el puerto 4500, permitiendo atravesar firewalls y modems del ISP.



## 3. LAS DOS FASES DE NEGOCIACION IPSEC AL DETALLE

Para que dos routers establezcan un tunel seguro a traves del ISP, deben completar
dos fases de negociacion criptografica:

FASE 1: IKE SA (ESTABLECIMIENTO DEL CANAL DE CONTROL SEGURO)
- Objetivo: Ambos routers se identifican, se autentican mutuamente y crean un canal cifrado
  seguro EXCLUSIVAMENTE para que sus CPUs hablen entre si y negocien la Fase 2.
- Parametros obligatorios que DEBEN coincidir exactamente en ambos extremos:
  1. Encryption (Cifrado): AES-256-CBC o AES-GCM-256.
  2. Hash / Integridad: SHA-256 o SHA-512.
  3. Diffie-Hellman Group (Grupo DH): Define la fortaleza matematica del algoritmo
     de intercambio de claves (Grupo 14 = 2048 bits; Grupo 19/20 = Curvas Elipticas ECDH).
  4. Authentication (Autenticacion): Pre-Shared Key (PSK) o Certificados RSA.
  5. Lifetime (Tiempo de vida): Tiempo antes de renegociar la Fase 1 (ej. 86400 seg / 24 horas).

IKEv1 vs IKEv2 (¿Cual usar en proyectos modernos?):
- IKEv1 (RFC 2409): Requiere 6 mensajes en "Main Mode" o 3 en "Aggressive Mode". Es mas
  vulnerable a ataques de denegacion de servicio y carece de soporte nativo para NAT-T.
- IKEv2 (RFC 7296): Estandar de la industria actual. Requiere solo 4 mensajes (IKE_SA_INIT
  e IKE_AUTH), soporta recuperacion automatica de conexion por aleteo (MOBIKE),
  consume menos recursos de CPU y tiene NAT-T integrado nativamente.

FASE 2: IPSEC SA (EL TUNEL DE DATOS REAL PARA EL USUARIO)
- Objetivo: Negociar los parametros con los que se cifraran y transportaran los paquetes
  reales de las computadoras, servidores y telefonos IP.
- Genera dos Asociaciones de Seguridad (SAs) unidireccionales (una para enviar y otra para recibir).
- Parametros negociados en Fase 2:
  1. Protocolo de Seguridad: ESP.
  2. Transform-Set: Algoritmo de Cifrado (AES-256) y Hash de Integridad (SHA-256).
  3. Perfect Forward Secrecy (PFS): Fuerza a ejecutar un nuevo calculo Diffie-Hellman
     cada vez que la Fase 2 expira (ej. cada 8 horas o 28800 seg), garantizando que si
     una clave temporal es comprometida, jamas se podra descifrar el trafico pasado o futuro.
  4. Selectores de Trafico (Proxy-IDs): En VPNs basadas en politicas, definen las subredes
     de origen y destino autorizadas a cruzar el tunel.



## 4. PARADIGMAS DE ARQUITECTURA: ROUTE-BASED (VTI) vs POLICY-BASED (CRYPTO MAP)


### a) VPN Basada en Politicas (Policy-Based / Crypto Maps - Modelo Clasico):

   - Utiliza una Lista de Control de Acceso (ACL) extendida:
     `permit ip 10.10.0.0 0.0.255.255 10.20.0.0 0.0.255.255`
   - El router intercepta el trafico que sale por la interfaz fisica WAN: si coincide
     con la ACL, lo cifra con IPsec; si no coincide, sale directo al ISP sin cifrar.
   - LIMITACION SEVERA EN ROUTING:
     NO permite tener interfaces virtuales de red.
     NO soporta paquetes Broadcast ni Multicast: Por lo tanto, ¡ES IMPOSIBLE ejecutar
     protocolos de enrutamiento dinamico como OSPF o BGP sobre el tunel!


### b) VPN Basada en Rutas (Route-Based / IPsec VTI o GRE over IPsec - Estandar Corporativo):

   - El router crea una interfaz virtual dedicada (ejemplo: `interface Tunnel 1`).
   - El tunel tiene su propia direccion IP de Capa 3 (ej. `172.16.100.1/30`).
   - Todo el trafico que se enruta hacia la interfaz `Tunnel 1` es cifrado automaticamente.
   - VENTAJAS EXTRAORDINARIAS:
     1. Soporta OSPF, BGP y EIGRP de forma nativa a traves del tunel cifrado.
     2. Permite aplicar politicas de Calidad de Servicio (QoS), Shapeo de trafico y ACLs
        directamente en la interfaz Tunnel.
     3. Facilita el enrutamiento con rutas estaticas sencillas (`ip route 10.20.0.0/24 Tunnel1`)
        sin complejas listas de acceso cruzadas.



## 5. EL PROBLEMA CRITICO DE MTU Y TCP MSS EN TUNELES SOBRE EL ISP

Cuando un paquete de una PC viaja por un tunel IPsec, el router anade encabezados extra:
- Cabecera IP Original del paquete: 20 Bytes.
- Cabecera ESP + Vector de Inicializacion (IV): 16 a 24 Bytes.
- Payload y Padding de Cifrado AES: 0 a 15 Bytes.
- Hash de Autenticacion ESP (ICV): 12 a 32 Bytes.
- Nueva Cabecera IP Externa del ISP: 20 Bytes.

Overhead Total: ¡Aproximadamente 56 a 76 Bytes adicionales por paquete!

La Falla Tipica en Produccion (Fragmentacion y Caida de Sistemas):
- La MTU estandar de la conexion del ISP es de 1500 Bytes.
- Si una PC intenta enviar un paquete TCP con el tamano maximo estandar (MTU 1500, MSS 1460),
  al anadir el encabezado IPsec el tamano supera los 1570 Bytes.
- Como la mayoria del trafico web y ERP tiene encendido el bit "Do Not Fragment" (DF=1),
  el router del ISP descarta silenciosamente el paquete (Black Hole):
  El usuario puede hacer `ping` exitosamente (paquetes pequenos de 64 bytes),
  pero cuando intenta abrir el portal web de la empresa, descargar un PDF o cargar un archivo,
  la sesion se queda congelada infinitamente.

LA SOLUCION OBLIGATORIA DE INGENIERIA:
Ajustar la MTU del tunel y reducir el tamano maximo de segmento TCP (TCP MSS Clamping):
- En Cisco:
  `interface Tunnel 1`
  ` ip mtu 1400`
  ` ip tcp adjust-mss 1360`
- En Huawei:
  `interface Tunnel 0/0/1`
  ` mtu 1400`
  ` tcp adjust-mss 1360`

Con esto, durante el saludo TCP de 3 vias (SYN / SYN-ACK), el router intercepta el valor MSS
y le ordena a las PCs no enviar paquetes con datos TCP mayores a 1360 bytes, evitando al 100%
la fragmentacion a traves del ISP.



## 6. ESCENARIO PRACTICO DE LA VIDA REAL: VPN SITE-TO-SITE ROUTE-BASED



#### 🎯 OBJETIVO DEL ESCENARIO:

Interconectar de forma segura dos sedes de una empresa a traves de Internet (ISP):
- Sede Central (R_CENTRAL): Conectada al ISP con IP publica fija `203.0.113.2`.
- Sucursal Remota (R_SUCURSAL): Conectada al ISP con IP publica fija `198.51.100.2`.
- Red LAN Central: `10.10.0.0/24`.
- Red LAN Sucursal: `10.20.0.0/24`.
- Enlace Logico del Tunel VTI (Capa 3): `172.16.100.0/30`.

REQUERIMIENTOS TECNICOS:
1. Seguridad IKEv2 moderna con cifrado AES-256, HMAC-SHA-256, DH Grupo 14 y PSK robusta.
2. Arquitectura Route-Based (VTI) con ajuste preventivo de MTU (1400) y MSS (1360).
3. Habilitar Dead Peer Detection (DPD) cada 10 segundos para deteccion rapida de caidas.
4. Enrutamiento dinamico OSPF sobre el tunel cifrado para aprendizaje automatico de rutas.


#### 🌐 DIAGRAMA DE LA TOPOLOGIA:

```text
  +-------------------------+                                 +-------------------------+
  |      SEDE CENTRAL       |                                 |     SUCURSAL REMOTA     |
  |     (R_CENTRAL)         |                                 |      (R_SUCURSAL)       |
  | LAN: 10.10.0.0/24       |                                 | LAN: 10.20.0.0/24       |
  | IP WAN: 203.0.113.2     |                                 | IP WAN: 198.51.100.2    |
  +------------+------------+                                 +------------+------------+
               | (Gi0/0/1)                                                 | (Gi0/0/1)
               |                                                           |
               |         +---------------------------------------+         |
               |         |         RED DE TRANSPORTE ISP         |         |
               +-------->|           (INTERNET PUBLICA)          |<--------+
                         |  (Nube no confiable / Routers ISP)    |
                         +---------------------------------------+
                                             :
```


## : (Tunel Logico IPsec Cifrado)


## [TUNEL VTI: 172.16.100.1/30 <---> 172.16.100.2/30 (OSPF)]



#### 📋 TABLA DE DIRECCIONAMIENTO:


| Dispositivo | Interfaz | Direccion IP | Mascara | Descripcion / Rol |
| :--- | :--- | :--- | :--- | :--- |
| R_CENTRAL | Gi0/0/0 | 10.10.0.1 | 255.255.255.0 | LAN Servidores Central |
| R_CENTRAL | Gi0/0/1 | 203.0.113.2 | 255.255.255.252 | Uplink Publico hacia ISP |
| R_CENTRAL | Tunnel1 | 172.16.100.1 | 255.255.255.252 | Extremo Local Tunel IPsec |
| R_SUCURSAL | Gi0/0/0 | 10.20.0.1 | 255.255.255.0 | LAN Usuarios Sucursal |
| R_SUCURSAL | Gi0/0/1 | 198.51.100.2 | 255.255.255.252 | Uplink Publico hacia ISP |
| R_SUCURSAL | Tunnel1 | 172.16.100.2 | 255.255.255.252 | Extremo Local Tunel IPsec |




## 7. IMPLEMENTACION COMPLETA EN ROUTERS CISCO (IOS / IOS-XE)


CASO: AMBOS EXTREMOS SON ROUTERS CISCO (ISR 4000 / CATALYST 8000 / ASR)


## A) CONFIGURACION EN SEDE CENTRAL (R_CENTRAL - CISCO IOS):

! 1. Configuracion de Interfaces Fisicas y Salida al ISP
```text
interface GigabitEthernet0/0/0
 description LAN_SERVIDORES_CENTRAL
 ip address 10.10.0.1 255.255.255.0
 no shutdown
!
interface GigabitEthernet0/0/1
 description WAN_INTERNET_ISP
 ip address 203.0.113.2 255.255.255.252
 no shutdown
!
! Ruta por defecto hacia el Gateway del ISP para tener conexion a Internet
ip route 0.0.0.0 0.0.0.0 203.0.113.1
!
! 2. Configuracion de IKEv2 (Fase 1)
crypto ikev2 proposal IKEV2_PROP_CORP
 encryption aes-cbc-256
 integrity sha256
 group 14
!
crypto ikev2 policy IKEV2_POL_CORP
 proposal IKEV2_PROP_CORP
!
! Definicion de la Clave Precompartida (PSK) asociada a la IP publica de la Sucursal
crypto ikev2 keyring KR_SUCURSAL
 peer R_SUCURSAL
  address 198.51.100.2
  pre-shared-key ClaveUltraSeguraVPN2026!
!
crypto ikev2 profile PROF_IKEV2_CORP
 match address local 203.0.113.2
 match identity remote address 198.51.100.2 255.255.255.255
 authentication remote pre-share
 authentication local pre-share
 keyring local KR_SUCURSAL
 dpd 10 3 on-demand   ! DPD cada 10 seg, 3 reintentos antes de declarar caida
!
! 3. Configuracion de IPsec (Fase 2)
crypto ipsec transform-set TS_IPSEC_CORP esp-aes 256 esp-sha256-hmac
 mode tunnel
!
crypto ipsec profile IPSEC_PROF_VTI
 set transform-set TS_IPSEC_CORP
 set ikev2-profile PROF_IKEV2_CORP
 set pfs group14      ! Perfect Forward Secrecy Grupo 14
!
! 4. Creacion de la Interfaz Virtual de Tunel (VTI)
interface Tunnel1
 description TUNEL_IPSEC_VTI_HACIA_SUCURSAL
 ip address 172.16.100.1 255.255.255.252
 tunnel source GigabitEthernet0/0/1
 tunnel destination 198.51.100.2
 tunnel mode ipsec ipv4
 tunnel protection ipsec profile IPSEC_PROF_VTI
 ! Mitigacion de Fragmentacion MTU y MSS
 ip mtu 1400
 ip tcp adjust-mss 1360
 no shutdown
!
! 5. Enrutamiento Dinamico OSPF a traves del Tunel Cifrado
router ospf 1
 router-id 1.1.1.1
 passive-interface GigabitEthernet0/0/0
 network 10.10.0.0 0.0.0.255 area 0
 network 172.16.100.0 0.0.0.3 area 0
exit
```


## B) CONFIGURACION EN SUCURSAL REMOTA (R_SUCURSAL - CISCO IOS):

```text
interface GigabitEthernet0/0/0
 description LAN_USUARIOS_SUCURSAL
 ip address 10.20.0.1 255.255.255.0
 no shutdown
!
interface GigabitEthernet0/0/1
 description WAN_INTERNET_ISP
 ip address 198.51.100.2 255.255.255.252
 no shutdown
!
ip route 0.0.0.0 0.0.0.0 198.51.100.1
!
crypto ikev2 proposal IKEV2_PROP_CORP
 encryption aes-cbc-256
 integrity sha256
 group 14
!
crypto ikev2 policy IKEV2_POL_CORP
 proposal IKEV2_PROP_CORP
!
crypto ikev2 keyring KR_CENTRAL
 peer R_CENTRAL
  address 203.0.113.2
  pre-shared-key ClaveUltraSeguraVPN2026!
!
crypto ikev2 profile PROF_IKEV2_CORP
 match address local 198.51.100.2
 match identity remote address 203.0.113.2 255.255.255.255
 authentication remote pre-share
 authentication local pre-share
 keyring local KR_CENTRAL
 dpd 10 3 on-demand
!
crypto ipsec transform-set TS_IPSEC_CORP esp-aes 256 esp-sha256-hmac
 mode tunnel
!
crypto ipsec profile IPSEC_PROF_VTI
 set transform-set TS_IPSEC_CORP
 set ikev2-profile PROF_IKEV2_CORP
 set pfs group14
!
interface Tunnel1
 description TUNEL_IPSEC_VTI_HACIA_CENTRAL
 ip address 172.16.100.2 255.255.255.252
 tunnel source GigabitEthernet0/0/1
 tunnel destination 203.0.113.2
 tunnel mode ipsec ipv4
 tunnel protection ipsec profile IPSEC_PROF_VTI
 ip mtu 1400
 ip tcp adjust-mss 1360
 no shutdown
!
router ospf 1
 router-id 2.2.2.2
 passive-interface GigabitEthernet0/0/0
 network 10.20.0.0 0.0.0.255 area 0
 network 172.16.100.0 0.0.0.3 area 0
exit
```



## 8. IMPLEMENTACION COMPLETA EN ROUTERS HUAWEI (VRP)


CASO: AMBOS EXTREMOS SON ROUTERS HUAWEI (SERIE AR6000 / AR1000 / NETENGINE)


## A) CONFIGURACION EN SEDE CENTRAL (R_CENTRAL - HUAWEI VRP):

# 1. Configuracion de Interfaces Fisicas y Ruta al ISP
```text
interface GigabitEthernet0/0/0
 description LAN_SERVIDORES_CENTRAL
 ip address 10.10.0.1 255.255.255.0
#
interface GigabitEthernet0/0/1
 description WAN_INTERNET_ISP
 ip address 203.0.113.2 255.255.255.252
#
ip route-static 0.0.0.0 0.0.0.0 203.0.113.1
#
# 2. Configuracion IKEv2 (Fase 1)
ike proposal 10
 encryption-algorithm aes-cbc-256
 dh group14
 authentication-algorithm sha2-256
 authentication-method pre-share
#
ike peer PEER_SUCURSAL
 undo version 1       ! Desactivar IKEv1 para usar IKEv2 estricto
 version 2
 ike-proposal 10
 pre-shared-key cipher ClaveUltraSeguraVPN2026!
 remote-address 198.51.100.2
 dpd type periodic interval 10 retry 3
#
# 3. Configuracion IPsec (Fase 2)
ipsec proposal PROP_IPSEC_CORP
 transform esp
 esp encryption-algorithm aes-256
 esp authentication-algorithm sha2-256
#
ipsec profile PROF_IPSEC_TUNNEL
 ike-peer PEER_SUCURSAL
 proposal PROP_IPSEC_CORP
 pfs dh-group14
#
# 4. Creacion de Interfaz de Tunel y Proteccion IPsec
interface Tunnel0/0/1
 description TUNEL_HACIA_SUCURSAL
 ip address 172.16.100.1 255.255.255.252
 tunnel-protocol ipsec
 source GigabitEthernet0/0/1
 destination 198.51.100.2
 ipsec profile PROF_IPSEC_TUNNEL
 mtu 1400
 tcp adjust-mss 1360
#
# 5. Enrutamiento Dinamico OSPF sobre el Tunel
ospf 1 router-id 1.1.1.1
 silent-interface GigabitEthernet0/0/0
 area 0.0.0.0
  network 10.10.0.0 0.0.0.255
  network 172.16.100.0 0.0.0.3
quit
```


## B) CONFIGURACION EN SUCURSAL REMOTA (R_SUCURSAL - HUAWEI VRP):

```text
interface GigabitEthernet0/0/0
 description LAN_USUARIOS_SUCURSAL
 ip address 10.20.0.1 255.255.255.0
#
interface GigabitEthernet0/0/1
 description WAN_INTERNET_ISP
 ip address 198.51.100.2 255.255.255.252
#
ip route-static 0.0.0.0 0.0.0.0 198.51.100.1
#
ike proposal 10
 encryption-algorithm aes-cbc-256
 dh group14
 authentication-algorithm sha2-256
 authentication-method pre-share
#
ike peer PEER_CENTRAL
 undo version 1
 version 2
 ike-proposal 10
 pre-shared-key cipher ClaveUltraSeguraVPN2026!
 remote-address 203.0.113.2
 dpd type periodic interval 10 retry 3
#
ipsec proposal PROP_IPSEC_CORP
 transform esp
 esp encryption-algorithm aes-256
 esp authentication-algorithm sha2-256
#
ipsec profile PROF_IPSEC_TUNNEL
 ike-peer PEER_CENTRAL
 proposal PROP_IPSEC_CORP
 pfs dh-group14
#
interface Tunnel0/0/1
 description TUNEL_HACIA_CENTRAL
 ip address 172.16.100.2 255.255.255.252
 tunnel-protocol ipsec
 source GigabitEthernet0/0/1
 destination 203.0.113.2
 ipsec profile PROF_IPSEC_TUNNEL
 mtu 1400
 tcp adjust-mss 1360
#
ospf 1 router-id 2.2.2.2
 silent-interface GigabitEthernet0/0/0
 area 0.0.0.0
  network 10.20.0.0 0.0.0.255
  network 172.16.100.0 0.0.0.3
quit
```



## 9. ESCENARIO MULTI-MARCA EN LA VIDA REAL: CISCO (CENTRAL) <-> HUAWEI (SUCURSAL)


Este es el reto mas comun en corporativos globales: El Core Corporativo opera con
Cisco y la nueva sucursal remota fue equipada con un router Huawei por costos de carrier.

TABLA DE CONCORDANCIA CRIPTOGRAFICA ESTRICTA:

| Parametro | Valor Lado Cisco IOS | Valor Lado Huawei VRP |
| :--- | :--- | :--- |
| Version IKE | IKEv2 | IKEv2 (`version 2`) |
| Cifrado Fase 1 | `encryption aes-cbc-256` | `encryption-algorithm aes-cbc-256` |
| Hash Integridad Fase 1 | `integrity sha256` | `authentication-algorithm sha2-256` |
| Grupo Diffie-Hellman | `group 14` (2048 bits) | `dh group14` |
| Metodo de Autenticacion | Pre-Shared Key (PSK) | Pre-Shared Key (PSK) |
| Clave Compartida | ClaveUltraSeguraVPN2026! | ClaveUltraSeguraVPN2026! |
| Protocolo de Seguridad | ESP | ESP (`transform esp`) |
| Cifrado Fase 2 | `esp-aes 256` | `esp encryption-algorithm aes-256` |
| Hash Integridad Fase 2 | `esp-sha256-hmac` | `esp authentication-algorithm sha2-256` |
| PFS (Perfect Forward) | `set pfs group14` | `pfs dh-group14` |
| Supervivencia | `dpd 10 3 on-demand` | `dpd type periodic interval 10` |


¡COMPATIBILIDAD DIRECTA!:
- Aplicando la configuracion de la Seccion 7.A en el Router Cisco de la Central.
- Y aplicando la configuracion de la Seccion 8.B en el Router Huawei de la Sucursal.
- El tunel VTI levanta en menos de 2 segundos a traves de Internet, y la adyacencia
  OSPF entre Cisco y Huawei alcanza estado FULL sin ningun tipo de incompatibilidad.



## 10. COMANDOS DE DIAGNOSTICO Y TROUBLESHOOTING EN PRODUCCION



## 1. DIAGNOSTICO EN ROUTERS CISCO:


### a) Verificar Fase 1 (IKEv2 SA):

   R_CENTRAL# show crypto ikev2 sa
   IPv4 Tunnel [1]
   Tunnel-id Local            Remote           Status  Role
   1         203.0.113.2/500  198.51.100.2/500 READY   INITIATOR
     Encr: AES-CBC, keysize: 256, Hash: SHA256, DH Grp:14, Auth: PRE-SHARED
   (El Status DEBE ser "READY". Si aparece NEGOTIATING o vacio, revisar PSK y UDP 500).


### b) Verificar Fase 2 (IPsec SA - Flujo real de paquetes cifrados):

   R_CENTRAL# show crypto ipsec sa
   interface: Tunnel1
     Crypto map tag: Tunnel1-head-0, local addr 203.0.113.2
      #pkts encaps: 14250, #pkts encrypt: 14250, #pkts digest: 14250
      #pkts decaps: 13980, #pkts decrypt: 13980, #pkts verify: 13980
      #send errors 0, #recv errors 0

   REGLA DE DIAGNOSTICO DE ORO:
   - Si `#pkts encaps` sube continuamente, pero `#pkts decaps` se queda en 0:
     Significa que tu router esta enviando los paquetes cifrados, pero el router remoto
     no contesta, o el ISP intermedio esta BLOQUEANDO el protocolo IP 50 (ESP) o UDP 4500.


### c) Verificar la sesion de extremo a extremo:

   R_CENTRAL# show crypto session detail



## 2. DIAGNOSTICO EN ROUTERS HUAWEI:


### a) Verificar Fase 1 (IKE SA):

```text
   <R_SUCURSAL> display ike sa
```


| Conn-ID | Peer | VPN | Flag(s) | Phase |
| :--- | :--- | :--- | :--- | :--- |
| 105 | 203.0.113.2:500 | RD\|ST | v2:2 |  |

   (La bandera "RD" significa Ready / Establecida; "v2:2" indica IKEv2 completado).


### b) Verificar Fase 2 (IPsec SA):


## <R_SUCURSAL> display ipsec sa brief


| Interface | Profile/Policy | In/Out Packets | In/Out Bytes |
| :--- | :--- | :--- | :--- |
| Tunnel0/0/1 | PROF_IPSEC_TUN | 14250/13980 | 1140000/1118400 |



### c) Verificar Estadisticas de Errores y Cifrado ESP:

```text
   <R_SUCURSAL> display ipsec statistics esp
```


## 3. MATRIZ DE FALLAS FRECUENTES EN LA VIDA REAL Y COMO RESOLVERLAS:


| Sintoma | Causa Raiz en Produccion | Accion Correctiva |
| :--- | :--- | :--- |
| Fase 1 se queda en | Discrepancia en parametros IKE: | Verificar que Cifrado, Hash, |
| NEGOTIATING o cae | contrasena PSK diferente, grupo DH | DH Group y PSK sean 100% |
| por timeout | distinto o version IKE desalineada. | identicos en ambos routers. |


Fase 1 nunca inicia y    El ISP o modem del proveedor         Abrir puertos UDP 500, UDP 4500
no hay paquetes vistos   bloquea el puerto UDP 500/4500 o     y permitir protocolo IP 50 en
                         la IP publica cambio (DHCP dinámico).el cortafuegos de frontera.

Fase 1 lista, pero       Discrepancia en el Transform-Set     Alinear transform-set a AES-256
Fase 2 no levanta        (ej. AES-128 vs AES-256) o en el     y asegurar mismo PFS Group.
                         grupo Diffie-Hellman de PFS.

Ping funciona pero las   Problema clasico de MTU / MSS. Los   Configurar `ip mtu 1400` y
paginas web y ERP se     paquetes con DF=1 superan la MTU     `ip tcp adjust-mss 1360` en

   - quedan cargando          de 1500 bytes del ISP.               las interfaces de tunel de ambos.
