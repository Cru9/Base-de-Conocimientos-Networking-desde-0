# PARTE 4: BGP ENTERPRISE, ATRIBUTOS Y MULTIHOMING (EJEMPLOS 061 AL 080)

> **ENRUTAMIENTO AVANZADO Y REDES WAN - GUIA PRACTICA DEFINITIVA**


---



## EJEMPLO 061: SESION eBGP BASICA ENTRE DOS SISTEMAS AUTONOMOS (ASNs)


> 🏢 **ESCENARIO REAL:**
Establecer una sesion eBGP (External BGP) entre el router de borde de una empresa
(AS 65001) y el router del Proveedor de Internet ISP (AS 65002) mediante sus IPs fisicas.


#### 🌐 DIAGRAMA:

```text
  [EMPRESA - AS 65001]                                       [CARRIER ISP - AS 65002]
      (R_EMPRESA)                                                    (R_ISP)
           |                                                            |
        +--+--+                  Enlace eBGP (TCP 179)               +--+--+
        | R1  +------------------------------------------------------+ R2  |
        +-----+ Gi0/1: 203.0.113.2                   Gi0/1: 203.0.113.1+-----+
```


#### 💻 CONFIGURACION CISCO IOS:

```cisco
! En Router Empresa (R1):
router bgp 65001
 bgp router-id 203.0.113.2
 neighbor 203.0.113.1 remote-as 65002
 neighbor 203.0.113.1 description PEERING_ISP
exit

! En Router ISP (R2):
router bgp 65002
 bgp router-id 203.0.113.1
 neighbor 203.0.113.2 remote-as 65001
exit
```


#### 🔍 Verificación:

```cisco
R1# show ip bgp summary
(State/PfxRcd debe mostrar un numero de prefijos o '0'; si dice Active o Idle, la sesion TCP fallo).
```



## EJEMPLO 062: ANUNCIO DE PREFIJOS EN BGP CON REGLA DE COINCIDENCIA EXACTA


> 🏢 **ESCENARIO REAL:**
Para que BGP anuncie una red con el comando `network`, dicha red DEBE existir en la
tabla de enrutamiento (RIB) con EXACTAMENTE la misma mascara de subred. Si no coincide,
BGP no la anuncia a nadie.


#### 🌐 DIAGRAMA:

```text
  [Ruta en tabla: 198.51.100.0/24] ===> BGP network 198.51.100.0 mask 255.255.255.0 ===> [ANUNCIADO]
```


#### 💻 CONFIGURACION CISCO IOS:

```cisco
! Anclar la red con una ruta de descarte Null0 si es un bloque publico asignado:
ip route 198.51.100.0 255.255.255.0 Null0

router bgp 65001
 address-family ipv4
  network 198.51.100.0 mask 255.255.255.0
 exit-address-family
exit
```


#### 🔍 Verificación:

```cisco
R1# show ip bgp | include 198.51.100.0
*> 198.51.100.0/24  0.0.0.0                  0         32768 i
```



## EJEMPLO 063: SESION eBGP SOBRE LOOPBACKS CON EBGP-MULTIHOP 2


> 🏢 **ESCENARIO REAL:**
Existen dos enlaces fisicos paralelos entre la empresa y el ISP. Para no perder la
sesion BGP si un cable se desconecta, la sesion eBGP se establece entre direcciones
Loopback. Como eBGP tiene TTL=1 por defecto, se requiere `ebgp-multihop 2`.


#### 🌐 DIAGRAMA:

```text
                   +--- Enlace Fisico 1 ---+
  [R1: Lo0 1.1.1.1]+                       +[R2: Lo0 2.2.2.2]
  AS 65001         +--- Enlace Fisico 2 ---+ AS 65002
```


#### 💻 CONFIGURACION CISCO IOS:

```cisco
! En R1:
ip route 2.2.2.2 255.255.255.255 10.0.0.2   ! Rutas estaticas para alcanzar la Loopback
ip route 2.2.2.2 255.255.255.255 10.0.1.2

router bgp 65001
 neighbor 2.2.2.2 remote-as 65002
 neighbor 2.2.2.2 update-source Loopback0
 neighbor 2.2.2.2 ebgp-multihop 2            ! Eleva el TTL a 2 saltos
exit
```


#### 🔍 Verificación:

```cisco
R1# show ip bgp neighbors 2.2.2.2 | include External
```



## EJEMPLO 064: SESION iBGP DENTRO DEL MISMO AS MEDIANTE LOOPBACK


> 🏢 **ESCENARIO REAL:**
Dos routers en el mismo Datacenter pertenecen a la misma empresa (AS 65000).
Se establece una sesion iBGP (Internal BGP) a traves de sus direcciones Loopback.


#### 🌐 DIAGRAMA:

```text
  [R_CORE_1] (AS 65000) <===== Sesion iBGP (TTL=255) =====> [R_CORE_2] (AS 65000)
  Loopback0: 10.255.0.1                                     Loopback0: 10.255.0.2
```


#### 💻 CONFIGURACION CISCO IOS:

```cisco
! En R_CORE_1:
router bgp 65000
 neighbor 10.255.0.2 remote-as 65000   ! Mismo AS = sesion iBGP
 neighbor 10.255.0.2 update-source Loopback0
exit

! En R_CORE_2:
router bgp 65000
 neighbor 10.255.0.1 remote-as 65000
 neighbor 10.255.0.1 update-source Loopback0
exit
```


#### 🔍 Verificación:

```cisco
R_CORE_1# show ip bgp neighbors 10.255.0.2 | include Internal
```



## EJEMPLO 065: CORRECCION DE NEXT-HOP INALCANZABLE CON NEXT-HOP-SELF


> 🏢 **ESCENARIO REAL:**
R1 aprende una ruta de Internet desde el ISP y se la pasa a R2 por iBGP.
Por defecto en iBGP, el atributo Next-Hop NO cambia (sigue siendo la IP del ISP).
Como R2 no conoce la IP publica del ISP en su IGP interno, marca la ruta como invalida.
`next-hop-self` fuerza a R1 a ponerse a si mismo como Next-Hop.


#### 🌐 DIAGRAMA:

```text
  [ISP] ---> Anuncia 8.8.8.8 (NH: 203.0.113.1) ---> [R1] --- Pasa a R2 con NH: 10.255.0.1 (R1) ---> [R2]
```


#### 💻 CONFIGURACION CISCO IOS (EN R1):

```cisco
router bgp 65000
 address-family ipv4
  neighbor 10.255.0.2 next-hop-self
 exit-address-family
exit
```


#### 🔍 Verificación:

```cisco
R2# show ip bgp 8.8.8.8
(El Next Hop ahora sera 10.255.0.1 y la ruta estara marcada con el simbolo '>' como valida).
```



## EJEMPLO 066: BGP ROUTE REFLECTOR (RR) PARA SUPRIMIR FULL-MESH


> 🏢 **ESCENARIO REAL:**
Por la regla de Split-Horizon de iBGP, un router no propaga rutas aprendidas de un
vecino iBGP a otro vecino iBGP. En lugar de crear una malla completa de sesiones,
el Router Core 1 se configura como Route Reflector.


#### 🌐 DIAGRAMA:

```text
                   [R1 - ROUTE REFLECTOR]
                             |
         +-------------------+-------------------+
         |                                       |
  [R2 - RR Client]                        [R3 - RR Client]
```


#### 💻 CONFIGURACION CISCO IOS (EN EL ROUTE REFLECTOR R1):

```cisco
router bgp 65000
 neighbor 10.255.0.2 remote-as 65000
 neighbor 10.255.0.2 route-reflector-client
 neighbor 10.255.0.3 remote-as 65000
 neighbor 10.255.0.3 route-reflector-client
exit
```


#### 🔍 Verificación:

```cisco
R1# show ip bgp neighbors | include Route-Reflector
```



## EJEMPLO 067: MANIPULACION DEL ATRIBUTO WEIGHT (LOCAL A CISCO)


> 🏢 **ESCENARIO REAL:**
Un router de borde tiene dos conexiones a Internet. Se requiere forzar que el trafico
hacia el servidor DNS de Google (`8.8.8.8`) salga siempre por el ISP-A asignando
un WEIGHT de 500 (el mayor peso siempre gana en el algoritmo de seleccion de Cisco).


#### 💻 CONFIGURACION CISCO IOS:

```cisco
ip prefix-list DNS_GOOGLE permit 8.8.8.8/32

route-map PREFERIR_ISPA_WEIGHT permit 10
 match ip address prefix-list DNS_GOOGLE
 set weight 500
exit
route-map PREFERIR_ISPA_WEIGHT permit 20
exit

router bgp 65001
 neighbor 203.0.113.1 route-map PREFERIR_ISPA_WEIGHT in
exit
```


#### 🔍 Verificación:

```cisco
R1# show ip bgp 8.8.8.8 | include Weight
(Muestra: 'Weight 500', ganando sobre el otro enlace que tiene Weight 0).
```



## EJEMPLO 068: CONTROL DE TRAFICO DE SALIDA CON LOCAL PREFERENCE


> 🏢 **ESCENARIO REAL:**
La empresa cuenta con dos routers de borde (R_BORDE_A conectado a ISP-1 de 1 Gbps,
y R_BORDE_B conectado a ISP-2 de 100 Mbps). Se requiere que TODA la empresa salga
por ISP-1. Se asigna `local-preference 200` en R_BORDE_A (el estandar es 100).
Local-Pref se propaga por todo el Sistema Autonomo.


#### 🌐 DIAGRAMA:

```text
  [ISP-1 (Fibra 1G)] <===================================== [ISP-2 (Respaldo 100M)]
          ^                                                         ^
          | (LocPrf 200 - GANA!)                                    | (LocPrf 100)
    [R_BORDE_A] <========== Sesion iBGP (LocPrf=200) ==========> [R_BORDE_B]
```


#### 💻 CONFIGURACION CISCO IOS (EN R_BORDE_A):

```cisco
route-map SET_LOCAL_PREF_200 permit 10
 set local-preference 200
exit

router bgp 65001
 neighbor 203.0.113.1 route-map SET_LOCAL_PREF_200 in
exit
```


#### 🔍 Verificación:

```cisco
R_BORDE_B# show ip bgp 0.0.0.0
*> 0.0.0.0          10.255.0.1             200      0 65100 i (Gana por LocPrf 200).
```



## EJEMPLO 069: CONTROL DE TRAFICO DE ENTRADA CON AS-PATH PREPENDING


> 🏢 **ESCENARIO REAL:**
Los clientes de Internet deben entrar a los servidores web de la empresa por ISP-1.
Hacia el ISP-2 secundario, la empresa anuncia su propio numero de AS repetido 3 veces
(`as-path prepend 65001 65001 65001`) para que el camino se vea artificialmente largo
y los proveedores mundiales prefieran entrar por ISP-1.


#### 🌐 DIAGRAMA:

```text
  Internet ve camino por ISP-1: [65100 65001] (2 saltos) <--- MAS CORTO (GANA!)
  Internet ve camino por ISP-2: [65200 65001 65001 65001 65001] (5 saltos - Descartado)
```


#### 💻 CONFIGURACION CISCO IOS (EN ROUTER HACIA ISP-2):

```cisco
route-map PREPEND_ISP2 permit 10
 set as-path prepend 65001 65001 65001
exit

router bgp 65001
 neighbor 198.18.1.1 route-map PREPEND_ISP2 out
exit
```


#### 🔍 Verificación:

```cisco
R1# show ip bgp neighbors 198.18.1.1 advertised-routes
Path: 65001 65001 65001 i
```



## EJEMPLO 070: CONTROL DE ENTRADA CON MED (MULTI-EXIT DISCRIMINATOR)


> 🏢 **ESCENARIO REAL:**
La empresa tiene dos conexiones al MISMO proveedor de Internet (ISP-A Guadalajara
e ISP-A Ciudad de Mexico). Para sugerirle al ISP por cual de sus dos enlaces debe
entregar los datos a la empresa, se envia el atributo MED (menor MED gana).


#### 💻 CONFIGURACION CISCO IOS:

```cisco
! En Enlace Primario:
route-map SET_MED_PRIMARIO permit 10
 set metric 50      ! Menor metrica
exit
router bgp 65001
 neighbor 203.0.113.1 route-map SET_MED_PRIMARIO out
exit

! En Enlace Secundario:
route-map SET_MED_SECUNDARIO permit 10
 set metric 200     ! Mayor metrica
exit
router bgp 65001
 neighbor 203.0.113.5 route-map SET_MED_SECUNDARIO out
exit
```


#### 🔍 Verificación:

```cisco
R_ISP# show ip bgp | include 198.51.100.0
```



## EJEMPLO 071: FILTRADO DE PREFIJOS ENTRANTES CON PREFIX-LISTS


> 🏢 **ESCENARIO REAL:**
Un router de borde solo contrato salida a Internet con ruta por defecto. Por error,
el ISP comienza a enviarle la tabla completa de 950,000 rutas saturando la RAM.
Se configura una Prefix-List estricta para aceptar EXCLUSIVAMENTE la ruta `0.0.0.0/0`.


#### 💻 CONFIGURACION CISCO IOS:

```cisco
ip prefix-list SOLO_DEFAULT permit 0.0.0.0/0

router bgp 65001
 neighbor 203.0.113.1 prefix-list SOLO_DEFAULT in
exit
```


#### 🔍 Verificación:

```cisco
R1# show ip bgp summary
(PfxRcd debe mostrar exactamente '1').
```



## EJEMPLO 072: BLOQUEO PARA EVITAR SER SISTEMA AUTONOMO DE TRANSITO


> 🏢 **ESCENARIO REAL:**
Si una empresa tiene dos ISPs y anuncia las rutas de ISP-1 hacia ISP-2, terceros
podrian usar los enlaces de la empresa para enviar trafico entre si. Se filtran
los anuncios para exportar unicamente rutas originadas localmente (Regex `^$`).


#### 💻 CONFIGURACION CISCO IOS:

```cisco
ip as-path access-list 1 permit ^$   ! ^$ coincide unicamente con rutas propias

router bgp 65001
 neighbor 203.0.113.1 filter-list 1 out
 neighbor 198.18.1.1 filter-list 1 out
exit
```


#### 🔍 Verificación:

```cisco
R1# show ip bgp regexp ^$
```



## EJEMPLO 073: USO DE BGP COMMUNITIES PARA MARCAR PREFIJOS


> 🏢 **ESCENARIO REAL:**
Marcar los prefijos de las sucursales bancarias con la comunidad `65000:100` para
que el router Core de la Sede Central aplique politicas de QoS y seguridad automaticas.


#### 💻 CONFIGURACION CISCO IOS:

```cisco
route-map MARCAR_SUCURSAL permit 10
 set community 65000:100
exit

router bgp 65000
 neighbor 10.255.0.1 send-community   ! OBLIGATORIO para enviar la comunidad
 neighbor 10.255.0.1 route-map MARCAR_SUCURSAL out
exit
```


#### 🔍 Verificación:

```cisco
R_CORE# show ip bgp community 65000:100
```



## EJEMPLO 074: AGREGACION Y SUMARIZACION CON AGGREGATE-ADDRESS SUMMARY-ONLY


> 🏢 **ESCENARIO REAL:**
La empresa posee 4 subredes contiguas (`198.51.100.0/26` a `.192/26`). Hacia Internet
debe anunciar solo el bloque `/24` suprimiendo las subredes hijas con `summary-only`.


#### 💻 CONFIGURACION CISCO IOS:

```cisco
router bgp 65001
 aggregate-address 198.51.100.0 255.255.255.0 summary-only
exit
```


#### 🔍 Verificación:

```cisco
R1# show ip bgp 198.51.100.0/24
(Muestra: 'Atomic-aggregate, summarized').
```



## EJEMPLO 075: BGP SOFT RECONFIGURATION Y ROUTE REFRESH


> 🏢 **ESCENARIO REAL:**
Despues de modificar un Route-Map, se requiere aplicar las politicas de inmediato
sin reiniciar la sesion TCP BGP (`clear ip bgp *` tiraria la red de la empresa).

COMANDO EN VIVO (CISCO IOS):
```cisco
R1# clear ip bgp 203.0.113.1 soft in    ! Re-evalua filtros entrantes en caliente
R1# clear ip bgp 203.0.113.1 soft out   ! Re-evalua filtros salientes en caliente
```



## EJEMPLO 076: BGP MULTIPATH (MAXIMUM-PATHS) PARA BALANCEO ECMP


> 🏢 **ESCENARIO REAL:**
Un router de borde tiene dos enlaces directos con el mismo ISP. Se habilita el
balanceo de carga ECMP para que el router instale ambas rutas en la tabla FIB.


#### 💻 CONFIGURACION CISCO IOS:

```cisco
router bgp 65001
 maximum-paths 2        ! Para sesiones eBGP paralelas
 maximum-paths ibgp 2   ! Para sesiones iBGP paralelas
exit
```


#### 🔍 Verificación:

```cisco
R1# show ip route bgp | include 0.0.0.0/0
(Mostrara dos saltos con asterisco '*' balanceando flujos).
```



## EJEMPLO 077: CONEXION MULTIHOMING DUAL-ISP CON FAILOVER


> 🏢 **ESCENARIO REAL:**
Empresa con AS 65100 conectada a ISP-1 (Primario) e ISP-2 (Respaldo).
Salida preferida por ISP-1 con Local-Pref 200, entrada preferida por ISP-1 con Prepend en ISP-2.


#### 💻 CONFIGURACION CISCO IOS:

```cisco
router bgp 65100
 network 198.51.100.0 mask 255.255.255.0
 ! Vecino ISP-1
 neighbor 203.0.113.1 remote-as 65200
 neighbor 203.0.113.1 route-map IN_ISP1 in
 ! Vecino ISP-2
 neighbor 198.18.1.1 remote-as 65300
 neighbor 198.18.1.1 route-map OUT_ISP2 out
exit

route-map IN_ISP1 permit 10
 set local-preference 200
exit

route-map OUT_ISP2 permit 10
 set as-path prepend 65100 65100 65100
exit
```



## EJEMPLO 078: BGP DYNAMIC NEIGHBORS (BGP LISTEN RANGE)


> 🏢 **ESCENARIO REAL:**
El router Central de un Datacenter conecta 300 sucursales por VPN. Para no agregar
manualmente a cada sucursal en el archivo de configuracion, se activa escucha dinamica.


#### 💻 CONFIGURACION CISCO IOS:

```cisco
router bgp 65000
 neighbor GRUPO_TIENDAS peer-group
 neighbor GRUPO_TIENDAS remote-as 65000
 neighbor GRUPO_TIENDAS route-reflector-client
 bgp listen range 172.16.100.0/24 peer-group GRUPO_TIENDAS
exit
```


#### 🔍 Verificación:

```cisco
R_CORE# show ip bgp summary
(Los vecinos que se conecten apareceran marcados con un asterisco '*').
```



## EJEMPLO 079: AUTENTICACION TCP MD5 EN SESIONES BGP


> 🏢 **ESCENARIO REAL:**
Proteger la sesion BGP contra ataques de reinicio TCP RST falsificados por hackers.


#### 💻 CONFIGURACION CISCO IOS (EN AMBOS EXTREMOS):

```cisco
router bgp 65001
 neighbor 203.0.113.1 password ClaveSecretaPeering2026!
exit
```


#### 🔍 Verificación:

```cisco
R1# show ip tcp tcb detail | include MD5
```



## EJEMPLO 080: ACELERACION BGP CON BFD EN 300 MILISEGUNDOS


> 🏢 **ESCENARIO REAL:**
Reducir el tiempo de conmutacion de BGP de 3 minutos a 300 ms acoplando BFD.


#### 💻 CONFIGURACION CISCO IOS:

```cisco
interface GigabitEthernet0/0/1
 bfd interval 100 min_rx 100 multiplier 3
exit

router bgp 65001
 neighbor 203.0.113.1 fall-over bfd
exit
```


#### 🔍 Verificación:

```cisco
R1# show ip bgp neighbors 203.0.113.1 | include BFD
```


## (Muestra: 'Fallover configured for BFD').
