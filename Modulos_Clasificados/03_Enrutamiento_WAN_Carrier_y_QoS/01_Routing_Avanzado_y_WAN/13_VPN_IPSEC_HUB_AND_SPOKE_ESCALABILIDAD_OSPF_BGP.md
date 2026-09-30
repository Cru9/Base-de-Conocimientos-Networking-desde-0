# 13. ARQUITECTURAS VPN IPSEC HUB-AND-SPOKE ESCALABLES, SUCURSALES EN EXPANSION

> **ENRUTAMIENTO AVANZADO Y TECNOLOGIAS WAN (ROUTING & WAN ARCHITECTURE)**

> *Y ENRUTAMIENTO DINAMICO AVANZADO CON OSPF Y BGP (CISCO Y HUAWEI)*


---



## 1. EL DESAFIO DEL CRECIMIENTO: DE 2 SEDES A CIENTOS DE SUCURSALES SOBRE EL ISP

Cuando una empresa inicia operaciones con solo dos sitios (Sede Central y una Sucursal),
un enlace IPsec Site-to-Site punto a punto (VTI estatico) es facil de implementar.
Sin embargo, cuando la empresa comienza a expandirse comercialmente:
- Se agregan Sucursales Secundarias (Centros de Distribucion CEDIS, Oficinas Regionales).
- Se suman docenas o cientos de Sucursales Terciarias (Puntos de venta, tiendas, farmacias,
  kioscos de atencion, cajeros remotos).

EL COLAPSO DEL MODELO PUNTO A PUNTO TRADICIONAL (POR QUE NO ESCALA):
Si una empresa tiene 200 sucursales y se utiliza el modelo clasico:
1. Fatiga de Configuracion en la Sede Maestra (Hub):
   - El router central requeriria 200 interfaces `interface Tunnel X` independientes,
     200 configuraciones `crypto ikev2 keyring/profile` individuales y 200 declaraciones
     de vecinos estaticos.
2. Desperdicio de Ancho de Banda y CPU:
   - Si la Sucursal A necesita comunicarse con la Sucursal B (por ejemplo, para transferir
     inventario o una llamada telefonica VoIP entre empleados), el trafico debe viajar
     obligatoriamente hasta la Sede Maestra y volver a salir a traves de su enlace de Internet
     (efecto "trombon"), duplicando la latencia y saturando la WAN central.
3. IPs Publicas Dinamicas en las Sucursales:
   - Las sucursales pequenas terciarias casi nunca tienen presupuesto para IP publica fija;
     usan enlaces FTTH baratos o modems celulares 4G/5G con IP publica dinamica o CGNAT.
     Un router central jamas podria configurar `tunnel destination <IP>` si la IP cambia
     todos los dias.



## 2. LAS 4 GRANDES VERTIENTES DE DISENO VPN IPSEC SOBRE ISP


VERTIENTE 1: HUB-AND-SPOKE MEDIANTE DYNAMIC VTI (DVTI) / FLEXVPN
- En la Sede Maestra se configura una UNICA plantilla de interfaz virtual (`interface Virtual-Template`).
- Cuando una sucursal secundaria o terciaria se conecta desde Internet, el router central
  clona la plantilla y crea una interfaz `Virtual-Access` al vuelo en memoria RAM.
- Ventaja: Cero configuracion en el router central cuando se abren nuevas sucursales.
- Limitacion: El trafico entre sucursales siempre debe atravesar el Hub.

VERTIENTE 2: REDES MULTIPUNTO DINAMICAS (DMVPN / mGRE + NHRP EN CISCO vs DSVPN EN HUAWEI)
- Utiliza tres tecnologias combinadas de forma brillante:
  1. mGRE (Multipoint GRE): Una sola interfaz logica en el Hub (`Tunnel 0`) puede hablar
     con miles de sucursales simultaneamente.
  2. NHRP (Next Hop Resolution Protocol - RFC 2332): Actua como un "servidor DNS de Capa 3".
     Cuando una sucursal terciaria se enciende, registra su IP publica cambiante del ISP
     en la base de datos NHRP de la Sede Maestra.
  3. IPsec en Modo Transporte: Cifra los paquetes mGRE con minima sobrecarga.
- En Huawei, esta arquitectura se denomina DSVPN (Dynamic Smart Virtual Private Network)
  y utiliza exactamente los mismos principios estandar (mGRE + NHRP + IPsec).
- LA REVOLUCION SPOKE-TO-SPOKE (Fases 2 y 3 de DMVPN/DSVPN):
  Si la Sucursal Terciaria 1 quiere enviar paquetes a la Sucursal Terciaria 2:
  * El primer paquete pasa por el Hub.
  * El Hub le envia un mensaje NHRP Redirect a ambas sucursales informandoles sus IPs publicas.
  * ¡Ambas sucursales abren un tunel IPsec directo entre ellas a traves del ISP sin pasar por el Hub!

VERTIENTE 3: SUCURSALES CON IP DINAMICA (DHCP / PPPoE / 4G-5G FWA)
- El Spoke no tiene IP fija. El Hub se configura con un Keyring IKEv2 comodin (Wildcard)
  o autenticacion basada en FQDN (Fully Qualified Domain Name) o identificador de grupo:
  * Cada sucursal se identifica por un nombre simbolico (ej. `sucursal-045.empresa.com`).
  * El Hub valida la identidad y la contrasena PSK o certificado digital, sin importar
    desde que direccion IP publica del ISP provenga la conexion.

VERTIENTE 4: ARQUITECTURA JERARQUICA DE TRES NIVELES (HUB-REGIONAL-SPOKE)
- En empresas transnacionales con mas de 500 sitios:
  * Nivel 1 (Sede Maestra / Datacenter Principal): Aloja el Core y concentra los Hubs Regionales.
  * Nivel 2 (Sucursales Secundarias / Hubs Regionales): Gestionan clusters de 50 a 100
    sucursales terciarias cercanas geograficamente.
  * Nivel 3 (Sucursales Terciarias / Tiendas): Se conectan en doble homing a su Hub
    Regional primario y al Datacenter de respaldo.



## 3. ENRUTAMIENTO DINAMICO A GRAN ESCALA: OSPF vs BGP

Al interconectar decenas o cientos de sucursales sobre tuneles VPN, la eleccion del
protocolo de enrutamiento es una decision critica de arquitectura:


### A) ENRUTAMIENTO CON OSPF (COMPLEJIDADES Y SOLUCION MULTI-AREA):

- El Desafio en redes Multipunto / Hub-and-Spoke:
  * OSPF es un protocolo de Estado de Enlace que asume enlaces de alta velocidad y baja perdida.
  * En una topologia Broadcast sobre un tunel multipunto, la Sede Maestra DEBE ser forzada
    como DR (`ip ospf priority 255`) y TODAS las sucursales DEBEN ser configuradas con prioridad 0
    (`ip ospf priority 0`) para que NINGUNA sucursal jamas intente ser DR o BDR.
  * O bien, configurar el tipo de red como `ip ospf network point-to-multipoint`.
- El Peligro del "Flooding" (Inundacion) de LSAs:
  * Si una tienda terciaria en un centro comercial sufre intermitencias en su cablemodem (aleteo / flap),
    CADA VEZ que el enlace cae y regresa, TODOS los routers de la empresa (incluyendo el Core
    y las demas sucursales) se ven obligados a recalcular el arbol Dijkstra SPF completo.
- LA SOLUCION OSPF: Segmentacion Jerarquica en Areas "Totally Stubby":
  * El Hub y el Datacenter residen en el Area 0 (Backbone).
  * Los grupos de sucursales se agrupan en areas especiales (ej. Area 10 Norte, Area 20 Sur).
  * Las sucursales se configuran como `area X stub no-summary` (Totally Stubby):
    Los routers de las tiendas SOLO reciben una ruta por defecto `0.0.0.0/0` inyectada por el Hub,
    bloqueando al 100% las inundaciones de LSAs cuando otra tienda fluctua.


### B) ENRUTAMIENTO CON BGP (EL ESTANDAR INDISCUTIBLE DE LA INDUSTRIA EN GRANDES REDES):

- ¿Por que los gigantes minoristas, bancos y corporativos prefieren BGP sobre VPN?
  1. Aislamiento de Fallas Radical: BGP es un protocolo de Vector de Ruta. Si una tienda
     cae, se retira su prefijo de la tabla sin recalcular matrices matematicas complejas.
  2. BGP Route Reflector (RR) en la Sede Maestra:
     * El Hub actua como Route Reflector (RR) y todas las sucursales secundarias y terciarias
       son clientes (RR Clients). Se elimina por completo la necesidad de malla completa iBGP.
  3. BGP DYNAMIC NEIGHBORS (VECINOS DINAMICOS BGP):
     * ¡LA HERRAMIENTA MAS PODEROSA DE INGENIERIA!:
     * En el Hub se configura una sola linea: `bgp listen range 172.16.0.0/16 peer-group SPOKES`.
     * Cuando abres la tienda numero 145 o la 380, ¡NO TIENES QUE ENTRAR AL ROUTER CENTRAL
       A ESCRIBIR NINGUN COMANDO! La tienda levanta su tunel IPsec, inicia la sesion BGP
       hacia el Hub y el Hub la acepta de forma transparente asociandola al peer-group.



## 4. TOPOLOGIA DE LABORATORIO: SEDE MAESTRA Y CRECIMIENTO DE SUCURSALES



> 🏢 **ESCENARIO REAL:**
Una cadena comercial cuenta con su Sede Central Maestra y experimenta una expansion
rapida, requiriendo integrar:
- Sucursal Secundaria (Oficina Regional / Hub Secundario).
- Sucursal Terciaria 1 (Tienda Minorista con Router Cisco).
- Sucursal Terciaria 2 (Tienda Minorista con Router Huawei e IP publica Dinamica).

DIAGRAMA DE LA ARQUITECTURA:

```text
                     +---------------------------------------+
                     |         SEDE CENTRAL MAESTRA          |
                     |         (R_HUB_MAESTRA - CISCO)       |
                     |         IP WAN Fija: 203.0.113.1      |
                     |         LAN Datacenter: 10.0.0.0/16   |
                     |         BGP AS 65000 (Route Reflector)|
                     +-------------------+-------------------+
                                         | (Gi0/0/1)
                                         |
                                         v
                         +-------------------------------+
                         |      NUBE PUBLICA DEL ISP     |
                         |           (INTERNET)          |
                         +-------+---------------+-------+
                                 |               |
                 +---------------+               +---------------+
                 |                                               |
                 v (IP Fija: 198.51.100.2)                       v (IP Dinamica / DHCP ISP)
   +-----------------------------+               +-----------------------------+
   |     SUCURSAL SECUNDARIA     |               |     SUCURSAL TERCIARIA      |
   |      (R_SECUNDARIA_REGIONAL)|               |       (R_TERCIARIA_TIENDA)  |
   |           (CISCO)           |               |           (HUAWEI AR)       |
   |  LAN Regional: 10.10.0.0/20 |               |  LAN Tienda: 10.20.1.0/24   |
   |  BGP AS 65000 (RR Client)   |               |  BGP AS 65000 (RR Client)   |
   +-----------------------------+               +-----------------------------+
```


## :                                               :


## [RED OVERLAY VPN: 172.16.100.0/24 - mGRE / VTI]


TABLA DE DIRECCIONAMIENTO DEL PROYECTO:

| Dispositivo | IP WAN Fisica | IP Tunel VPN | Red LAN Local | Rol BGP / OSPF |
| :--- | :--- | :--- | :--- | :--- |
| R_HUB_MAESTRA | 203.0.113.1 (Fija) 172.16.100.1/24 | 10.0.0.0/16 | BGP RR / OSPF Hub |  |
| R_SECUNDARIA_REGIONAL | 198.51.100.2(Fija) 172.16.100.10/24 | 10.10.0.0/20 | BGP Client / OSPF Spoke |  |
| R_TERCIARIA_TIENDA (HW) DHCP (Dinamica) | 172.16.100.20/24 | 10.20.1.0/24 | BGP Client / OSPF Spoke |  |




## 5. IMPLEMENTACION PASO A PASO: SEDE MAESTRA ESCALABLE CON BGP DINAMICO



## A) CONFIGURACION EN LA SEDE CENTRAL MAESTRA (CISCO IOS-XE / CATALYST 8000 / ASR):

! 1. Interfaz Fisica de Salida hacia el ISP
```text
interface GigabitEthernet0/0/1
 description UPLINK_INTERNET_ISP_FIBRA
 ip address 203.0.113.1 255.255.255.248
 no shutdown
exit
ip route 0.0.0.0 0.0.0.0 203.0.113.6  ! Gateway del Carrier

! 2. IKEv2 Configurado para recibir conexiones desde CUALQUIER IP PUBLICA (Wildcard)
crypto ikev2 proposal IKEV2_PROP_HUB
 encryption aes-cbc-256
 integrity sha256
 group 14
exit

crypto ikev2 policy IKEV2_POL_HUB
 proposal IKEV2_PROP_HUB
exit

! Keyring con comodin 0.0.0.0 para admitir sucursales terciarias con IP dinamica
crypto ikev2 keyring KR_HUB_GLOBAL
 peer SUCURSALES_EMPRESA
  address 0.0.0.0 0.0.0.0
  pre-shared-key ClaveCorporativaExpansion2026!
exit

crypto ikev2 profile PROF_IKEV2_HUB
 match identity remote address 0.0.0.0 0.0.0.0
 authentication remote pre-share
 authentication local pre-share
 keyring local KR_HUB_GLOBAL
 dpd 10 3 on-demand
exit

! 3. IPsec Transform-Set en Modo Transporte (Optimizado para encapsulacion GRE)
crypto ipsec transform-set TS_IPSEC_TRANSPORT esp-aes 256 esp-sha256-hmac
 mode transport
exit

crypto ipsec profile IPSEC_PROF_MGRE
 set transform-set TS_IPSEC_TRANSPORT
 set ikev2-profile PROF_IKEV2_HUB
 set pfs group14
exit

! 4. Interfaz Multipunto mGRE (Una sola interfaz para atender a cientos de sucursales)
interface Tunnel0
 description INTERFAZ_MULTIPUNTO_VPN_CENTRAL
 ip address 172.16.100.1 255.255.255.0
 no ip redirects
 ip mtu 1400
 ip tcp adjust-mss 1360
 ! Configuracion mGRE y NHRP (Servidor Central)
 tunnel source GigabitEthernet0/0/1
 tunnel mode gre multipoint
 tunnel key 12345
 tunnel protection ipsec profile IPSEC_PROF_MGRE
 ip nhrp network-id 1
 ip nhrp redirect    ! Permite atajos Spoke-to-Spoke directos
 no shutdown
exit

! 5. BGP DINAMICO CON ROUTE REFLECTOR (CERO CONFIGURACION PARA NUEVAS TIENDAS)
router bgp 65000
 bgp router-id 172.16.100.1
 bgp log-neighbor-changes
 ! Crear plantilla de grupo para todas las sucursales
 neighbor GRUPO_SPOKES peer-group
 neighbor GRUPO_SPOKES remote-as 65000
 neighbor GRUPO_SPOKES update-source Tunnel0
 neighbor GRUPO_SPOKES route-reflector-client
 ! Habilitar deteccion automatica en todo el segmento de tunel (172.16.100.0/24)
 bgp listen range 172.16.100.0/24 peer-group GRUPO_SPOKES
 !
 address-family ipv4
  network 10.0.0.0 mask 255.255.0.0
  neighbor GRUPO_SPOKES activate
  ! Inyectar ruta por defecto automatica para que las sucursales naveguen por el Hub
  neighbor GRUPO_SPOKES default-originate
 exit-address-family
exit
```



## 6. CONFIGURACION DE LAS SUCURSALES (SPOKES)



## B) SUCURSAL SECUNDARIA REGIONAL (ROUTER CISCO - IP FIJA):

```text
interface GigabitEthernet0/0/1
 description WAN_INTERNET_ISP_REGIONAL
 ip address 198.51.100.2 255.255.255.252
 no shutdown
exit
ip route 0.0.0.0 0.0.0.0 198.51.100.1

crypto ikev2 proposal IKEV2_PROP_SPOKE
 encryption aes-cbc-256
 integrity sha256
 group 14
exit

crypto ikev2 policy IKEV2_POL_SPOKE
 proposal IKEV2_PROP_SPOKE
exit

crypto ikev2 keyring KR_SPOKE
 peer R_HUB_MAESTRA
  address 203.0.113.1
  pre-shared-key ClaveCorporativaExpansion2026!
exit

crypto ikev2 profile PROF_IKEV2_SPOKE
 match identity remote address 203.0.113.1 255.255.255.255
 authentication remote pre-share
 authentication local pre-share
 keyring local KR_SPOKE
 dpd 10 3 on-demand
exit

crypto ipsec transform-set TS_IPSEC_TRANSPORT esp-aes 256 esp-sha256-hmac
 mode transport
exit

crypto ipsec profile IPSEC_PROF_SPOKE
 set transform-set TS_IPSEC_TRANSPORT
 set ikev2-profile PROF_IKEV2_SPOKE
 set pfs group14
exit

! Interfaz de Tunel hacia el Hub Maestra
interface Tunnel0
 description TUNEL_HACIA_HUB_MAESTRA
 ip address 172.16.100.10 255.255.255.0
 ip mtu 1400
 ip tcp adjust-mss 1360
 tunnel source GigabitEthernet0/0/1
 tunnel mode gre multipoint
 tunnel key 12345
 tunnel protection ipsec profile IPSEC_PROF_SPOKE
 ! Registro NHRP en el Hub
 ip nhrp network-id 1
 ip nhrp shortcut
 ip nhrp map 172.16.100.1 203.0.113.1
 ip nhrp map multicast 203.0.113.1
 ip nhrp nhs 172.16.100.1
 no shutdown
exit

! Sesion BGP hacia el Hub
router bgp 65000
 bgp router-id 172.16.100.10
 neighbor 172.16.100.1 remote-as 65000
 neighbor 172.16.100.1 update-source Tunnel0
 address-family ipv4
  neighbor 172.16.100.1 activate
  network 10.10.0.0 mask 255.255.240.0
 exit-address-family
exit
```


## C) SUCURSAL TERCIARIA (TIENDA CON ROUTER HUAWEI AR - IP DINAMICA POR ISP):

# 1. Interfaz WAN conectada al modem del ISP (obtiene IP por DHCP automaticamente)
```text
interface GigabitEthernet0/0/1
 description WAN_INTERNET_ISP_MODEM_DHCP
 ip address dhcp-alloc
#

# 2. Configuracion IKEv2 y asociacion con la IP fija del Hub Central
ike proposal 10
 encryption-algorithm aes-cbc-256
 dh group14
 authentication-algorithm sha2-256
 authentication-method pre-share
#
ike peer PEER_HUB_CENTRAL
 undo version 1
 version 2
 ike-proposal 10
 pre-shared-key cipher ClaveCorporativaExpansion2026!
 remote-address 203.0.113.1
 dpd type periodic interval 10 retry 3
#

# 3. IPsec Proposal en modo transporte
ipsec proposal PROP_IPSEC_TRANSPORT
 encapsulation-mode transport
 transform esp
 esp encryption-algorithm aes-256
 esp authentication-algorithm sha2-256
#
ipsec profile PROF_IPSEC_SPOKE_HW
 ike-peer PEER_HUB_CENTRAL
 proposal PROP_IPSEC_TRANSPORT
 pfs dh-group14
#

# 4. Interfaz mGRE / DSVPN en Huawei
interface Tunnel0/0/0
 description TUNEL_HACIA_HUB_MAESTRA
 ip address 172.16.100.20 255.255.255.0
 tunnel-protocol gre p2mp
 source GigabitEthernet0/0/1
 gre key 12345
 ipsec profile PROF_IPSEC_SPOKE_HW
 mtu 1400
 tcp adjust-mss 1360
 # Configuracion de Cliente NHRP apuntando al Hub
 nhrp network-id 1
 nhrp entry 172.16.100.1 203.0.113.1 register
#

# 5. Sesion BGP de la Tienda Terciaria hacia el Hub Central
bgp 65000
 router-id 172.16.100.20
 peer 172.16.100.1 as-number 65000
 peer 172.16.100.1 connect-interface Tunnel0/0/0
 #
 ipv4-family unicast
  undo synchronization
  network 10.20.1.0 255.255.255.0
  peer 172.16.100.1 enable
quit
```



## 7. ALTERNATIVA: ENRUTAMIENTO CON OSPF JERARQUICO MULTI-AREA SOBRE VPN


Si la organizacion exige utilizar OSPF en lugar de BGP debido a politicas internas:

REGLAS DE DISENO OBLIGATORIAS PARA QUE OSPF NO COLAPSE EL HUB:
1. En la interfaz `Tunnel0` del Hub Maestra:
   - Forzar el tipo de red: `ip ospf network point-to-multipoint`
   - O si se usa Broadcast, forzar al Hub como DR indiscutible:
     `ip ospf priority 255`
2. En TODAS las sucursales secundarias y terciarias:
   - `ip ospf priority 0` (¡Jamás competir por el rol de DR!).
3. Segmentar mediante OSPF Totally Stubby:
   - Hub Central:
     `router ospf 1`
     ` area 10 stub no-summary`
     ` area 20 stub no-summary`
   - Spoke Sucursales:
     `router ospf 1`
     ` area 10 stub`
   (Efecto: El Hub inyecta una sola ruta `0.0.0.0/0`. Si una tienda terciaria se desconecta
   en Monterrey, los routers de Guadalajara y Cancún no sufren recalculo SPF).



## 8. DIAGNOSTICO Y VALIDACION EN LA SEDE CENTRAL EN PLENA EXPANSION


1. Verificar que el Hub Cisco esta escuchando y aceptando vecinos BGP dinamicos:
   R_HUB_MAESTRA# show ip bgp summary
   BGP router identifier 172.16.100.1, local AS number 65000
   BGP table version is 45, main routing table version 45
   2 network entries using 496 bytes of memory
   2 path entries using 240 bytes of memory
   2 BGP path attribute entries using 528 bytes of memory
   Neighbor        V           AS MsgRcvd MsgSent   TblVer  InQ OutQ Up/Down  State/PfxRcd
   *172.16.100.10  4        65000     125     130       45    0    0 01:45:12        1
   *172.16.100.20  4        65000      89      94       45    0    0 01:12:05        1

   ¡OBSERVACION CLAVE!:
   El asterisco `*` al inicio de la IP del vecino indica que fue aceptado DINAMICAMENTE
   gracias al comando `bgp listen range`. No hubo necesidad de pre-configurar su IP.

2. Verificar la Base de Datos NHRP (Mapeo dinamico de IPs de tunel a IPs publicas):
   R_HUB_MAESTRA# show ip nhrp
   172.16.100.10/32 via 172.16.100.10
       Tunnel0 created 01:45:15, expire 01:44:45
       Type: dynamic, Flags: unique registered used
       NBMA address: 198.51.100.2 (IP publica fija de la Secundaria)
   172.16.100.20/32 via 172.16.100.20
       Tunnel0 created 01:12:08, expire 01:47:52
       Type: dynamic, Flags: unique registered used
       NBMA address: 187.132.45.88 (IP publica DINAMICA del ISP en la Tienda Huawei)

3. Verificar en el Router Huawei que la tienda terciaria recibio las rutas del Core:
```text
   <R_TERCIARIA_TIENDA> display ip routing-table protocol bgp
   Destination/Mask    Proto   Pre  Cost      Flags NextHop         Interface
          0.0.0.0/0    IBGP    255  0           D   172.16.100.1    Tunnel0/0/0
        10.0.0.0/16    IBGP    255  0           D   172.16.100.1    Tunnel0/0/0
       10.10.0.0/20    IBGP    255  0           D   172.16.100.10   Tunnel0/0/0

   ¡CONFIRMACION DE REVOLUCION SPOKE-TO-SPOKE!:
   Para llegar a la Sucursal Secundaria (10.10.0.0/20), el NextHop es directamente
   `172.16.100.10`. El router Huawei abrira una sesion IPsec directa hacia la Sucursal
```


## Secundaria a traves del ISP sin triangular el trafico de datos por la Sede Central.
