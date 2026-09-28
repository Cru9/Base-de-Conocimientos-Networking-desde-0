# PARTE 2: OSPF SINGLE-AREA Y MULTI-AREA (EJEMPLOS 021 AL 040)

> **ENRUTAMIENTO AVANZADO Y REDES WAN - GUIA PRACTICA DEFINITIVA**


---



## EJEMPLO 021: OSPF SINGLE-AREA BASICO EN AREA 0 MEDIANTE WILDCARD


> 🏢 **ESCENARIO REAL:**
Habilitar enrutamiento dinamico OSPF en una red empresarial de campus pequeno.
Todos los routers residen en el Area 0 (Backbone). Se declaran las subredes
mediante la mascara inversa (Wildcard: 255.255.255.255 - Mascara Subred).


#### 🌐 DIAGRAMA:

```text
  [LAN SUCURSAL 1]                                           [LAN SUCURSAL 2]
  192.168.1.0/24                                             192.168.2.0/24
        |                                                          |
     +--+--+                   [AREA 0]                         +--+--+
     | R1  +----------------------------------------------------+ R2  |
     +-----+ Gi0/0/1: 10.0.0.1/30               Gi0/0/1: 10.0.0.2/30+-----+
```


#### 💻 CONFIGURACION CISCO IOS:

```cisco
! En R1:
router ospf 1
 network 192.168.1.0 0.0.0.255 area 0
 network 10.0.0.0 0.0.0.3 area 0
exit

! En R2:
router ospf 1
 network 192.168.2.0 0.0.0.255 area 0
 network 10.0.0.0 0.0.0.3 area 0
exit
```


#### 🔍 Verificación:

```cisco
R1# show ip ospf neighbor
(El estado debe decir FULL/DR o FULL/BDR).
R1# show ip route ospf
```



## EJEMPLO 022: OSPF ACTIVADO DIRECTAMENTE BAJO LA INTERFAZ FISICA


> 🏢 **ESCENARIO REAL:**
En redes modernas, calcular mascaras wildcard propicia errores humanos. El metodo
estandar actual de Cisco permite habilitar OSPF directamente dentro de la interfaz.


#### 🌐 DIAGRAMA:

```text
  [R1] (Gi0/0/1) <========= Enlace Punto a Punto =========> (Gi0/0/1) [R2]
   ip ospf 1 area 0                                          ip ospf 1 area 0
```


#### 💻 CONFIGURACION CISCO IOS:

```cisco
! En R1:
interface GigabitEthernet0/0/1
 description WAN_HACIA_R2
 ip address 10.10.10.1 255.255.255.252
 ip ospf 1 area 0       ! Activa OSPF sin comandos network
 no shutdown
exit

! En R2:
interface GigabitEthernet0/0/1
 description WAN_HACIA_R1
 ip address 10.10.10.2 255.255.255.252
 ip ospf 1 area 0
 no shutdown
exit
```


#### 🔍 Verificación:

```cisco
R1# show ip ospf interface GigabitEthernet0/0/1
```



## EJEMPLO 023: ASIGNACION MANUAL Y ESTANDARIZADA DE ROUTER-ID


> 🏢 **ESCENARIO REAL:**
Si no se configura manualmente el Router-ID, OSPF elegira la IP fisica mas alta.
Si esa interfaz parpadea o se apaga, el Router-ID puede cambiar reiniciando el arbol SPF.
Se crea una interfaz Loopback0 y se fuerza un Router-ID estatico.


#### 🌐 DIAGRAMA:

```text
     [R1]                                     [R2]
  Loopback0: 1.1.1.1                       Loopback0: 2.2.2.2
  Router-ID: 1.1.1.1                       Router-ID: 2.2.2.2
```


#### 💻 CONFIGURACION CISCO IOS:

```cisco
! En R1:
interface Loopback0
 ip address 1.1.1.1 255.255.255.255
exit
router ospf 1
 router-id 1.1.1.1
exit

! En R2:
interface Loopback0
 ip address 2.2.2.2 255.255.255.255
exit
router ospf 1
 router-id 2.2.2.2
exit
```


#### 🔍 Verificación:

```cisco
R1# show ip ospf | include ID
(Muestra: 'Routing Process "ospf 1" with ID 1.1.1.1').
```



## EJEMPLO 024: AJUSTE DE ANCHO DE BANDA DE REFERENCIA (AUTO-COST)


> 🏢 **ESCENARIO REAL:**
Por defecto en OSPF clasico, la formula usa 100 Mbps (`10^8`), por lo que un enlace
Gigabit (1 Gbps) y uno 10-Gigabit (10 Gbps) tienen ambos Costo = 1.
Se ajusta la referencia a 100 Gbps (100,000 Mbps) en todos los routers de la red.


#### 🌐 DIAGRAMA:

```text
  [R1] --- Fibra 10 Gbps (Costo = 10) ---> [R2]
       --- Fibra  1 Gbps (Costo = 100) --> (Diferenciacion exacta)
```


#### 💻 CONFIGURACION CISCO IOS (APLICAR EN TODOS LOS ROUTERS OSPF):

```cisco
router ospf 1
 auto-cost reference-bandwidth 100000
exit
```


#### 🔍 Verificación:

```cisco
R1# show ip ospf interface GigabitEthernet0/0/1 | include Cost
(Para una interfaz 1 Gbps debe mostrar: 'Cost: 100').
```



## EJEMPLO 025: SEGURIDAD EN OSPF MEDIANTE PASSIVE-INTERFACE DEFAULT


> 🏢 **ESCENARIO REAL:**
Por politica de Ciberseguridad Zero-Trust, ningun puerto debe enviar paquetes
Hello OSPF por defecto para evitar espionaje de topologia en los puertos de pared.
Se desactivan todas las interfaces con `passive-interface default` y solo se
encienden explicitamente los puertos inter-router.


#### 🌐 DIAGRAMA:

```text
  [ROUTER R1]
   - Gi0/0 (LAN Ventas):       PASIVA (Segura, no envia Hellos)
   - Gi0/1 (LAN Servidores):   PASIVA (Segura, no envia Hellos)
   - Gi0/2 (WAN hacia R2):     ACTIVA (Forma adyacencia OSPF)
```


#### 💻 CONFIGURACION CISCO IOS:

```cisco
router ospf 1
 passive-interface default          ! Bloquea todos los puertos
 no passive-interface GigabitEthernet0/2  ! Unico puerto autorizado para OSPF
exit
```


#### 🔍 Verificación:

```cisco
R1# show ip protocols | section Passive
```



## EJEMPLO 026: ELECCION FORZADA DE DR Y BDR MEDIANTE PRIORIDADES


> 🏢 **ESCENARIO REAL:**
En una red Ethernet con un Switch Core y 4 routers, se debe garantizar que el router
mas potente (Core 1) sea siempre el DR (Designated Router), el router Core 2 sea el BDR,
y los routers menores nunca compitan por el liderazgo.


#### 🌐 DIAGRAMA:

```text
                   [SWITCH CORE CENTRAL]
                             |
         +-----------+-------+-------+-----------+
         |           |               |           |
       [R1]        [R2]            [R3]        [R4]
     Core 1       Core 2          Suc 1       Suc 2
    Pri: 255     Pri: 100        Pri: 0      Pri: 0
     (DR)         (BDR)         (DROTHER)   (DROTHER)
```


#### 💻 CONFIGURACION CISCO IOS:

```cisco
! En R1 (Forzar como DR):
interface GigabitEthernet0/0/0
 ip ospf priority 255
exit

! En R2 (Forzar como BDR):
interface GigabitEthernet0/0/0
 ip ospf priority 100
exit

! En R3 y R4 (Descalificar de la eleccion):
interface GigabitEthernet0/0/0
 ip ospf priority 0
exit
```


#### 🔍 Verificación:

```cisco
R1# show ip ospf neighbor
(R3 y R4 apareceran con estado 'FULL/DROTHER').
```



## EJEMPLO 027: OSPF PUNTO A PUNTO EN ETHERNET PARA SUPRIMIR DR/BDR


> 🏢 **ESCENARIO REAL:**
Cuando dos routers estan conectados directamente por un cable de fibra o cobre
punto a punto sin ningun otro equipo en medio, la eleccion de DR/BDR es innecesaria
y retrasa la convergencia en 40 segundos al encender. Se cambia la red a Point-to-Point.


#### 🌐 DIAGRAMA:

```text
  [R1] (Gi0/1) <=== Cable Directo (No hay switches) ===> (Gi0/1) [R2]
   network point-to-point                                 network point-to-point
   (Adyacencia FULL instantanea sin paquetes DR)
```


#### 💻 CONFIGURACION CISCO IOS (EN AMBOS ROUTERS):

```cisco
interface GigabitEthernet0/0/1
 ip ospf network point-to-point
exit
```


#### 🔍 Verificación:

```cisco
R1# show ip ospf neighbor
Neighbor ID     Pri   State           Dead Time   Address         Interface
2.2.2.2           0   FULL/ -         00:00:35    10.0.0.2        GigabitEthernet0/0/1
(Notese que no dice DR ni BDR; el estado es directamente 'FULL/ -').
```



## EJEMPLO 028: MODIFICACION MANUAL DE COSTOS OSPF (INGENIERIA DE TRAFICO)


> 🏢 **ESCENARIO REAL:**
Entre la Sede A y la Sede B existen dos caminos: uno por Fibra (primario) y otro
por Enlace Satelital (respaldo). Como ambos puertos son GigabitEthernet, OSPF
asignaria el mismo costo balanceando trafico por el satelite. Se fuerza un costo
alto de 500 en el satelite para que solo se use si la fibra muere.


#### 🌐 DIAGRAMA:

```text
                     +---------------------------+
                     |  Fibra Optica (Costo 10)  |
                  +--+  Gi0/1                    +--+
  [ROUTER A] =====+                                 +=====> [ROUTER B]
                  +--+  Satelital (Costo 500)    +--+
                     |  Gi0/2                    |
                     +---------------------------+
```


#### 💻 CONFIGURACION CISCO IOS (EN ROUTER A):

```cisco
interface GigabitEthernet0/0/1
 description ENLACE_FIBRA_PRIMARIO
 ip ospf cost 10
exit

interface GigabitEthernet0/0/2
 description ENLACE_SATELITAL_RESPALDO
 ip ospf cost 500
exit
```


#### 🔍 Verificación:

```cisco
ROUTER_A# show ip route 192.168.20.0
(Verificar que la ruta solo apunta a Gi0/0/1 por tener menor metrica).
```



## EJEMPLO 029: PROPAGACION DE RUTA POR DEFECTO EN OSPF (ALWAYS)


> 🏢 **ESCENARIO REAL:**
El router de frontera (R_BORDE) tiene acceso a Internet. Se requiere que anuncie
la ruta 0.0.0.0/0 hacia todos los routers internos de la empresa, incluso si
la conexion con el ISP sufre micro-cortes temporales (usando el parametro `always`).


#### 🌐 DIAGRAMA:

```text
  INTERNET <=== [R_BORDE] =====================> [ROUTERS INTERNOS]
                default-information originate    Reciben LSA Tipo 5: O*E2 0.0.0.0/0
```


#### 💻 CONFIGURACION CISCO IOS:

```cisco
router ospf 1
 default-information originate always metric 10
exit
```


#### 🔍 Verificación:

```cisco
R_INTERNO# show ip route ospf
O*E2 0.0.0.0/0 [110/10] via 10.0.0.1, GigabitEthernet0/1
```



## EJEMPLO 030: AUTENTICACION CRIPTOGRAFICA OSPF CON SHA-256


> 🏢 **ESCENARIO REAL:**
Proteger las adyacencias OSPF contra ataques de inyeccion de paquetes falsos
utilizando el algoritmo seguro HMAC-SHA-256 en lugar del vulnerable MD5.


#### 🌐 DIAGRAMA:

```text
  [R1] <==== Hellos y LSAs firmados con HMAC-SHA-256 ====> [R2]
```


#### 💻 CONFIGURACION CISCO IOS (EN AMBOS ROUTERS):

```cisco
interface GigabitEthernet0/0/1
 ip ospf authentication message-digest
 ip ospf message-digest-key 1 md5 ClaveSeguraOSPF2026
 no shutdown
exit

! En routers modernos Cisco IOS-XE (Soporte nativo SHA):
! interface GigabitEthernet0/0/1
!  ip ospf authentication algorithm hmac-sha-256
!  ip ospf authentication key ClaveUltraSegura2026
```


#### 🔍 Verificación:

```cisco
R1# show ip ospf interface GigabitEthernet0/0/1 | include Message
```



## EJEMPLO 031: OSPF MULTI-AREA BASICO (AREA 0 BACKBONE Y AREA 10 PLANTA)


> 🏢 **ESCENARIO REAL:**
Dividir una red corporativa para evitar que las fluctuaciones de red en la Planta
de Fabricacion forcen recalculos SPF en el Datacenter. El Router ABR interconecta
el Area 0 con el Area 10.


#### 🌐 DIAGRAMA:

```text
  [AREA 0 - BACKBONE]            [ROUTER ABR]            [AREA 10 - PLANTA]
   (Router Core 1)                 (R_ABR)                 (Router Planta)
         |                            |                           |
         +====== 10.0.0.0/30 =========+======== 10.10.0.0/30 =====+
             (Area 0)                               (Area 10)
```


#### 💻 CONFIGURACION CISCO IOS (EN EL ABR):

```cisco
router ospf 1
 router-id 2.2.2.2
 network 10.0.0.0 0.0.0.3 area 0
 network 10.10.0.0 0.0.0.3 area 10
exit
```


#### 🔍 Verificación:

```cisco
R_ABR# show ip ospf
(Verificar la linea: 'It is an area border router').
```



## EJEMPLO 032: INSPECCION DE LSAs TIPO 1, 2 Y 3 EN EL ABR


> 🏢 **ESCENARIO REAL:**
Un ingeniero de redes necesita validar que los anuncios de routers (LSA 1),
redes de transito (LSA 2) y rutas inter-area (LSA 3) se estan propagando correctamente.


#### 💻 CONFIGURACION Y DIAGNOSTICO:

```text
R_ABR# show ip ospf database

                OSPF Router with ID (2.2.2.2) (Process ID 1)

                Router Link States (Area 0)  <--- LSA Tipo 1 (Generado por cada router)
Link ID         ADV Router      Age         Seq#       Checksum Link count
1.1.1.1         1.1.1.1         520         0x80000004 0x00A1B2 2
2.2.2.2         2.2.2.2         480         0x80000003 0x0084C1 2

                Net Link States (Area 0)     <--- LSA Tipo 2 (Generado por el DR)
Link ID         ADV Router      Age         Seq#       Checksum
10.0.0.2        2.2.2.2         480         0x80000001 0x00F341

                Summary Net Link States (Area 0) <--- LSA Tipo 3 (Rutas del Area 10)
Link ID         ADV Router      Age         Seq#       Checksum
192.168.10.0    2.2.2.2         120         0x80000001 0x0045D2
```



## EJEMPLO 033: SUMARIZACION INTER-AREA EN EL ABR (AREA RANGE)


> 🏢 **ESCENARIO REAL:**
En el Area 10 existen 8 subredes contiguas (`172.16.0.0/24` a `172.16.7.0/24`).
El ABR debe resumirlas en un unico prefijo `172.16.0.0/21` hacia el Area 0.


#### 🌐 DIAGRAMA:

```text
  [Area 10: 8 Subredes /24] ===> [ABR] === Anuncia solo 172.16.0.0/21 ===> [Area 0]
```


#### 💻 CONFIGURACION CISCO IOS (EN EL ABR):

```cisco
router ospf 1
 area 10 range 172.16.0.0 255.255.248.0
exit
```


#### 🔍 Verificación:

```cisco
R_CORE# show ip route ospf
O IA 172.16.0.0/21 [110/11] via 10.0.0.2, GigabitEthernet0/1
```



## EJEMPLO 034: AREA STUB EN SUCURSAL PARA AHORRAR MEMORIA


> 🏢 **ESCENARIO REAL:**
Una sucursal remota opera con un router pequeno. No necesita almacenar rutas
externas de Internet (LSA 4 y 5). Se configura el Area 10 como STUB; el ABR
bloquea las rutas externas e inyecta automaticamente una ruta por defecto `0.0.0.0/0`.


#### 🌐 DIAGRAMA:

```text
  [AREA 0] <=== LSA 5 Bloqueados <=== [ABR] === Inyecta 0.0.0.0/0 ===> [AREA 10 STUB]
```


#### 💻 CONFIGURACION CISCO IOS:

```cisco
! En el ABR:
router ospf 1
 area 10 stub
exit

! En el Router de la Sucursal (OBLIGATORIO en todos los routers del area):
router ospf 1
 area 10 stub
exit
```


#### 🔍 Verificación:

```cisco
R_SUCURSAL# show ip route ospf
O*IA 0.0.0.0/0 [110/11] via 10.10.0.1, GigabitEthernet0/1
```



## EJEMPLO 035: AREA TOTALLY STUBBY (EXCLUSIVA DE CISCO)


> 🏢 **ESCENARIO REAL:**
Optimizar al maximo un router de sucursal. Ademas de bloquear rutas externas,
se bloquean tambien las rutas de otras areas (LSA 3). El router solo ve sus
redes locales y una unica ruta por defecto.


#### 🌐 DIAGRAMA:

```text
  [ABR] --- Bloquea LSA 3, 4 y 5 ---> [ROUTER SUCURSAL: Tabla casi vacia]
```


#### 💻 CONFIGURACION CISCO IOS:

```cisco
! En el ABR unicamente:
router ospf 1
 area 10 stub no-summary     ! 'no-summary' lo convierte en Totally Stubby
exit

! En el Router de Sucursal (Permanece igual como stub):
router ospf 1
 area 10 stub
exit
```


#### 🔍 Verificación:

```cisco
R_SUCURSAL# show ip route ospf
(Unicamente aparecera: 'O*IA 0.0.0.0/0').
```



## EJEMPLO 036: AREA NSSA (NOT-SO-STUBBY AREA) CON REDISTRIBUCION EXTERNA


> 🏢 **ESCENARIO REAL:**
Una sucursal configurada como Stub adquiere una empresa socia que usa rutas estaticas.
Un area Stub tradicional prohibe tener routers ASBR. Se convierte el area a NSSA (RFC 3101):
el router inyecta la ruta como LSA 7, y el ABR la traduce a LSA 5 hacia el Area 0.


#### 🌐 DIAGRAMA:

```text
  [AREA 0] <=== LSA 5 (Traducido) <=== [ABR] <=== LSA 7 <=== [ASBR NSSA] <--- Rutas Estaticas
```


#### 💻 CONFIGURACION CISCO IOS:

```cisco
! En el ABR y en el ASBR:
router ospf 1
 area 20 nssa
exit

! En el ASBR de la sucursal (Redistribucion):
router ospf 1
 redistribute static subnets
exit
```


#### 🔍 Verificación:

```cisco
ASBR# show ip ospf database nssa-external (Muestra LSA Tipo 7).
R_CORE# show ip ospf database external      (Muestra LSA Tipo 5 traducido).
```



## EJEMPLO 037: AREA TOTALLY NSSA (NSSA NO-SUMMARY)


> 🏢 **ESCENARIO REAL:**
La sucursal tiene un ASBR que redistribuye rutas externas hacia la empresa, pero
no quiere recibir rutas de otras areas. Se bloquean los LSA 3 con `no-summary`.


#### 💻 CONFIGURACION CISCO IOS:

```cisco
! En el ABR:
router ospf 1
 area 20 nssa no-summary
exit

! En el Router de Sucursal:
router ospf 1
 area 20 nssa
exit
```


#### 🔍 Verificación:

```cisco
R_SUCURSAL# show ip route ospf
(Solo muestra rutas locales intra-area y la ruta por defecto inyectada por el ABR).
```



## EJEMPLO 038: ENLACE VIRTUAL OSPF (VIRTUAL-LINK)


> 🏢 **ESCENARIO REAL:**
Por una reestructuracion fisica de cables, el Area 30 quedo conectada al Area 10,
pero NO tiene conexion fisica directa con el Area 0 (violando la regla de oro de OSPF).
Se crea un tunel logico no cifrado (Virtual-Link) a traves del Area 10 para unirla al Area 0.


#### 🌐 DIAGRAMA:

```text
  [AREA 0] <=====> [ABR 1 (ID 1.1.1.1)] <=== Area 10 (Transito) ===> [ABR 2 (ID 2.2.2.2)] <=====> [AREA 30]
                               :............... Virtual Link ...............:
```


#### 💻 CONFIGURACION CISCO IOS:

```cisco
! En ABR 1 (Conectado a Area 0 y Area 10):
router ospf 1
 area 10 virtual-link 2.2.2.2   ! Apunta al Router-ID de ABR 2
exit

! En ABR 2 (Conectado a Area 10 y Area 30):
router ospf 1
 area 10 virtual-link 1.1.1.1   ! Apunta al Router-ID de ABR 1
exit
```


#### 🔍 Verificación:

```cisco
ABR1# show ip ospf virtual-links
(El estado debe decir: 'OSPF_VL0 to router 2.2.2.2 is up').
```



## EJEMPLO 039: AFINACION DE TIMERS Y BFD PARA CONVERGENCIA EN MILISEGUNDOS


> 🏢 **ESCENARIO REAL:**
El tiempo de deteccion de falla de 40 segundos de OSPF corta llamadas de voz.
Se habilita BFD (Bidirectional Forwarding Detection) para detectar caidas en 150 ms.


#### 🌐 DIAGRAMA:

```text
  [R1] <==== Sondeos BFD de hardware cada 50 ms ====> [R2]
```


#### 💻 CONFIGURACION CISCO IOS (EN AMBOS ROUTERS):

```cisco
interface GigabitEthernet0/0/1
 bfd interval 50 min_rx 50 multiplier 3
 ip ospf bfd
 no shutdown
exit
```


#### 🔍 Verificación:

```cisco
R1# show bfd neighbors
(Estado UP en interfaz GigabitEthernet0/0/1).
```



## EJEMPLO 040: FILTRADO DE RUTAS INTER-AREA MEDIANTE FILTER-LIST EN EL ABR


> 🏢 **ESCENARIO REAL:**
La red confidencial de Servidores de Seguridad (`10.99.0.0/24`) en el Area 10
no debe ser conocida por los routers del Area 0. El ABR bloquea el LSA 3 hacia el Area 0.


#### 🌐 DIAGRAMA:

```text
  [Area 10: Red 10.99.0.0/24] ===> [ABR - Bloquea con Filter-List] =X=> [Area 0]
```


#### 💻 CONFIGURACION CISCO IOS (EN EL ABR):

```cisco
ip prefix-list FILTRO_SEGURIDAD deny 10.99.0.0/24
ip prefix-list FILTRO_SEGURIDAD permit 0.0.0.0/0 le 32

router ospf 1
 area 10 filter-list prefix FILTRO_SEGURIDAD out
exit
```


#### 🔍 Verificación:

```cisco
R_CORE# show ip route 10.99.0.0
```


## % Subnet not in table
