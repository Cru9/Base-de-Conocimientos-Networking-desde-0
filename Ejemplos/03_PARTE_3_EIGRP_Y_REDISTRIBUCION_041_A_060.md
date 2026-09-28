# PARTE 3: EIGRP, BALANCEO DESIGUAL Y REDISTRIBUCION (EJEMPLOS 041 AL 060)

> **ENRUTAMIENTO AVANZADO Y REDES WAN - GUIA PRACTICA DEFINITIVA**


---



## EJEMPLO 041: EIGRP CLASICO BASICO CON SISTEMA AUTONOMO (AS 100)


> 🏢 **ESCENARIO REAL:**
Habilitar EIGRP en un campus universitario para interconectar el Edificio Administrativo
con la Biblioteca. El numero de Sistema Autonomo (AS 100) debe coincidir en ambos routers.


#### 🌐 DIAGRAMA:

```text
  [EDIFICIO ADMIN]                                            [BIBLIOTECA]
   (Router R1)                                                 (Router R2)
        |                                                           |
     +--+--+                   [EIGRP AS 100]                    +--+--+
     | R1  +-----------------------------------------------------+ R2  |
     +-----+ Gi0/1: 10.1.1.1/30                  Gi0/1: 10.1.1.2/30+-----+
```


#### 💻 CONFIGURACION CISCO IOS:

```cisco
! En R1:
router eigrp 100
 network 10.1.1.0
 network 192.168.10.0
 no auto-summary
exit

! En R2:
router eigrp 100
 network 10.1.1.0
 network 192.168.20.0
 no auto-summary
exit
```


#### 🔍 Verificación:

```cisco
R1# show ip eigrp neighbors
(Muestra la IP 10.1.1.2 en la interfaz Gi0/1).
```



## EJEMPLO 042: EIGRP CON MASCARAS WILDCARD EXACTAS Y NO AUTO-SUMMARY


> 🏢 **ESCENARIO REAL:**
En un router con multiples interfaces, solo se desea activar EIGRP en una subred
especifica `/28` sin encender accidentalmente puertos contiguos. Se usa mascara wildcard.


#### 🌐 DIAGRAMA:

```text
  [ROUTER R1]
   - Gi0/0 (192.168.1.0/28)   ===> EIGRP ACTIVADO (Wildcard: 0.0.0.15)
   - Gi0/1 (192.168.1.16/28)  ===> EIGRP DESACTIVADO
```


#### 💻 CONFIGURACION CISCO IOS:

```cisco
router eigrp 100
 no auto-summary
 network 192.168.1.0 0.0.0.15
exit
```


#### 🔍 Verificación:

```cisco
R1# show ip eigrp interfaces
```



## EJEMPLO 043: ROUTER-ID Y PASSIVE-INTERFACE EN EIGRP


> 🏢 **ESCENARIO REAL:**
Asignar un identificador estatico al router y bloquear el envio de paquetes Hello
hacia los switches de acceso de usuarios para evitar ataques de Denegacion de Servicio.


#### 🌐 DIAGRAMA:

```text
  [LAN USUARIOS] <--- NO Hellos (Seguridad) <--- [Gi0/0: PASSIVE] [ROUTER R1] (ID: 1.1.1.1)
```


#### 💻 CONFIGURACION CISCO IOS:

```cisco
router eigrp 100
 eigrp router-id 1.1.1.1
 passive-interface GigabitEthernet0/0
exit
```


#### 🔍 Verificación:

```cisco
R1# show ip protocols | include Passive
```



## EJEMPLO 044: DUAL: ANALISIS DE FD, RD, SUCESOR Y FEASIBLE SUCCESSOR


> 🏢 **ESCENARIO REAL:**
R1 tiene dos caminos hacia la red del Servidor: uno por Fibra y otro por Radio.
Se inspecciona la tabla de topologia para verificar si el enlace de Radio califica
como Feasible Successor (cumpliendo la regla: `RD < FD del sucesor`).


#### 🌐 DIAGRAMA:

```text
                     +----------------------------+
                     |  Fibra: FD=3072 / RD=2816  | (Sucesor - Mejor Ruta)
                  +--+  Next-Hop: 10.1.1.2        +--+
  [ROUTER R1] ====++                                 +====> [SERVIDOR]
                  +--+  Radio: FD=5632 / RD=2816  +--+ (Feasible Successor!)
                     |  Next-Hop: 10.2.2.2        |     (2816 < 3072: CUMPLE)
                     +----------------------------+
```


#### 💻 CONFIGURACION Y DIAGNOSTICO:

```text
R1# show ip eigrp topology 10.100.0.0/16
EIGRP-IPv4 Topology Entry for AS(100)/ID(1.1.1.1) for 10.100.0.0/16
  State is Passive, 1 Successor(s), FD is 3072
  Descriptor Blocks:
  10.1.1.2 (GigabitEthernet0/1), from 10.1.1.2, Send flag is 0x0
      Composite metric is (3072/2816), route is Internal  <--- SUCESOR
  10.2.2.2 (GigabitEthernet0/2), from 10.2.2.2, Send flag is 0x0
      Composite metric is (5632/2816), route is Internal  <--- FEASIBLE SUCCESSOR
```



## EJEMPLO 045: BALANCEO DE CARGA EN RUTAS DESIGUALES CON VARIANCE


> 🏢 **ESCENARIO REAL:**
Aprovechar ambos enlaces (Fibra 3072 y Radio 5632) simultaneamente.
Como EIGRP es el unico IGP que permite balanceo desigual, se fija `variance 2`:
Metrica_Secundaria (5632) <= 2 * FD (3072 = 6144). ¡Califica para balancear!


#### 🌐 DIAGRAMA:

```text
  [ROUTER R1] === Reparte trafico proporcional: 60% Fibra / 40% Radio ===> [DESTINO]
```


#### 💻 CONFIGURACION CISCO IOS:

```cisco
router eigrp 100
 variance 2
exit
```


#### 🔍 Verificación:

```cisco
R1# show ip route 10.100.0.0
Routing Descriptor Blocks:
* 10.1.1.2, via GigabitEthernet0/1, share count 18
* 10.2.2.2, via GigabitEthernet0/2, share count 10
(Ambas rutas instaladas en la tabla de enrutamiento).
```



## EJEMPLO 046: EIGRP STUB ROUTING CONTRA CONSULTAS SIA (STUCK-IN-ACTIVE)


> 🏢 **ESCENARIO REAL:**
Una sucursal remota conectada por un enlace WAN lento satura su CPU cuando el Core
le envia paquetes Query durante caidas en otros sitios. Se declara como `stub`.


#### 🌐 DIAGRAMA:

```text
  [CORE DATACENTER] --- NO enviar Queries si cae otra red ---> [SUCURSAL STUB]
```


#### 💻 CONFIGURACION CISCO IOS (EN ROUTER SUCURSAL):

```cisco
router eigrp 100
 eigrp stub connected summary
exit
```


#### 🔍 Verificación:

```cisco
R_CORE# show ip eigrp neighbors detail
(Muestra: 'Stub Peer Advertising (CONNECTED , SUMMARY ) Routes').
```



## EJEMPLO 047: SUMARIZACION MANUAL EN INTERFACES DE SALIDA EIGRP


> 🏢 **ESCENARIO REAL:**
En lugar de propagar 4 prefijos `/24` hacia el enlace WAN, se sumarizan en `/22`
directamente sobre la interfaz fisica hacia el router vecino.


#### 💻 CONFIGURACION CISCO IOS:

```cisco
interface GigabitEthernet0/0/1
 description WAN_HACIA_CORE
 ip summary-address eigrp 100 192.168.0.0 255.255.252.0
exit
```


#### 🔍 Verificación:

```cisco
R_CORE# show ip route eigrp | include 192.168.0.0/22
```



## EJEMPLO 048: AUTENTICACION CRIPTOGRAFICA MD5 CON KEY-CHAIN EN EIGRP


> 🏢 **ESCENARIO REAL:**
Prevenir que routers no autorizados formen vecindad EIGRP en los enlaces inter-sitios.


#### 💻 CONFIGURACION CISCO IOS (EN AMBOS ROUTERS):

```cisco
key chain LLAVE_EIGRP
 key 1
  key-string ClaveSeguraEIGRP2026
exit

interface GigabitEthernet0/0/1
 ip authentication mode eigrp 100 md5
 ip authentication key-chain eigrp 100 LLAVE_EIGRP
 no shutdown
exit
```


#### 🔍 Verificación:

```cisco
R1# show ip eigrp neighbors
(Si la clave no coincide, la vecindad cae inmediatamente).
```



## EJEMPLO 049: EIGRP NAMED MODE (MODO NOMBRADO MODERNO DE CISCO)


> 🏢 **ESCENARIO REAL:**
Cisco reemplazo la configuracion clasica dispersa de EIGRP por el "Named Mode",
que centraliza la configuracion de IPv4, IPv6, interfaces y VRFs en un unico bloque.


#### 🌐 DIAGRAMA:

```text
  [CONFIGURACION UNIFICADA EN MODO NOMBRADO: router eigrp EMPRESA_WAN]
```


#### 💻 CONFIGURACION CISCO IOS-XE:

```cisco
router eigrp EMPRESA_WAN
 address-family ipv4 unicast autonomous-system 100
  network 10.0.0.0 0.255.255.255
  network 192.168.1.0 0.0.0.255
  ! Configuracion de interfaces centralizada:
  af-interface GigabitEthernet0/0
   passive-interface
  exit-af-interface
  af-interface GigabitEthernet0/1
   hello-interval 5
   hold-time 15
  exit-af-interface
  topology base
   variance 2
  exit-af-topology
 exit-address-family
exit
```


#### 🔍 Verificación:

```cisco
R1# show ip protocols | include Named
```



## EJEMPLO 050: AUTENTICACION HMAC-SHA-256 EN EIGRP NAMED MODE


> 🏢 **ESCENARIO REAL:**
Configurar autenticacion criptografica SHA-256 nativa directamente dentro del
Modo Nombrado sin necesidad de crear key-chains antiguos.


#### 💻 CONFIGURACION CISCO IOS-XE:

```cisco
router eigrp EMPRESA_WAN
 address-family ipv4 unicast autonomous-system 100
  af-interface GigabitEthernet0/1
   authentication mode hmac-sha-256 ClaveUltraSeguraSHA2026!
  exit-af-interface
 exit-address-family
exit
```


#### 🔍 Verificación:

```cisco
R1# show ip eigrp interface detail GigabitEthernet0/1 | include Authentication
```



## EJEMPLO 051: REDISTRIBUCION DE RUTAS CONECTADAS HACIA OSPF CON SUBNETS


> 🏢 **ESCENARIO REAL:**
El router R1 tiene interfaces de gestion conectadas directamente que no estan en OSPF.
Se inyectan al dominio OSPF. Es OBLIGATORIO incluir la palabra `subnets` o Cisco
solo redistribuira prefijos con clase clasica (/8, /16, /24).


#### 🌐 DIAGRAMA:

```text
  [Subredes Conectadas /28] ===> [ROUTER R1] === Redistribute ===> [DOMINIO OSPF]
```


#### 💻 CONFIGURACION CISCO IOS:

```cisco
router ospf 1
 redistribute connected metric 20 subnets
exit
```


#### 🔍 Verificación:

```cisco
R_VECINO# show ip route ospf
O E2 192.168.100.0/28 [110/20] via 10.0.0.1
```



## EJEMPLO 052: REDISTRIBUCION DE RUTAS ESTATICAS HACIA EIGRP (METRICA K1-K5)


> 🏢 **ESCENARIO REAL:**
EIGRP exige una metrica semilla de 5 vectores (Bandwidth, Delay, Reliability,
Load, MTU) al recibir rutas estaticas. Sin ella, la metrica seria infinito.


#### 💻 CONFIGURACION CISCO IOS:

```cisco
router eigrp 100
 ! Valores: BW=1000000 (1G), Delay=10 (100usec), Rel=255, Load=1, MTU=1500
 redistribute static metric 1000000 10 255 1 1500
exit
```


#### 🔍 Verificación:

```cisco
R_VECINO# show ip route eigrp
D EX 172.20.0.0/16 [170/3072] via 10.1.1.1
```



## EJEMPLO 053: REDISTRIBUCION MUTUA OSPF <-> EIGRP EN ROUTER FRONTERA


> 🏢 **ESCENARIO REAL:**
Dos empresas se fusionaron. El corporativo usa OSPF y la planta usa EIGRP.
El router de frontera R_GW debe permitir comunicacion bidireccional completa.


#### 🌐 DIAGRAMA:

```text
  [DOMINIO OSPF] <====== [ROUTER FRONTERA R_GW] ======> [DOMINIO EIGRP]
                          Redistribucion Mutua
```


#### 💻 CONFIGURACION CISCO IOS:

```cisco
router ospf 1
 redistribute eigrp 100 metric 30 subnets
exit

router eigrp 100
 redistribute ospf 1 metric 1000000 10 255 1 1500
exit
```


#### 🔍 Verificación:

```cisco
R_GW# show ip protocols | include Redistributing
```



## EJEMPLO 054: PREVENCION DE BUCLES CON ROUTE-TAGGING (TAGS 90 Y 110)


> 🏢 **ESCENARIO REAL:**
Cuando hay dos routers de frontera entre OSPF y EIGRP, las rutas pueden re-inyectarse
al dominio original provocando bucles. Se etiquetan con tags para bloquearlas.


#### 🌐 DIAGRAMA:

```text
  [OSPF] ---> Inyecta a EIGRP con Tag 110 ---> Si regresa con Tag 110: ¡DENEGAR!
```


#### 💻 CONFIGURACION CISCO IOS:

```cisco
! 1. Route-maps de salida hacia EIGRP y filtro de retorno
route-map OSPF_A_EIGRP permit 10
 set tag 110
exit

route-map EIGRP_A_OSPF deny 10
 match tag 110        ! Bloquear rutas que nacieron en OSPF
exit
route-map EIGRP_A_OSPF permit 20
 set tag 90
exit

! 2. Aplicacion en los procesos
router eigrp 100
 redistribute ospf 1 metric 1000000 10 255 1 1500 route-map OSPF_A_EIGRP
exit

router ospf 1
 redistribute eigrp 100 metric 20 subnets route-map EIGRP_A_OSPF
exit
```


#### 🔍 Verificación:

```cisco
R_CORE# show ip route 10.50.0.0 | include tag
(Muestra: 'Route tag 90').
```



## EJEMPLO 055: FILTRADO GRANULAR EN REDISTRIBUCION CON PREFIX-LISTS


> 🏢 **ESCENARIO REAL:**
Solo se permite redistribuir la red de Servidores ERP (`10.10.50.0/24`) desde EIGRP
hacia OSPF; las demas subredes internas de la planta deben permanecer privadas.


#### 💻 CONFIGURACION CISCO IOS:

```cisco
ip prefix-list ERP_UNICO permit 10.10.50.0/24

route-map FILTRO_ERP permit 10
 match ip address prefix-list ERP_UNICO
exit

router ospf 1
 redistribute eigrp 100 metric 20 subnets route-map FILTRO_ERP
exit
```


#### 🔍 Verificación:

```cisco
R_OSPF# show ip route ospf | include 10.10.50.0
```



## EJEMPLO 056: REDISTRIBUCION RIPv2 A OSPF: METRICA E1 vs E2


> 🏢 **ESCENARIO REAL:**
- Tipo E2 (Defecto): El costo externo permanece fijo (ej. 20) a traves de todo el campus.
- Tipo E1: Suma el costo externo mas el costo interno acumulado de cada salto OSPF.


#### 💻 CONFIGURACION CISCO IOS:

```cisco
router ospf 1
 ! Configurar como Tipo E1 para reflejar distancia real:
 redistribute rip metric 50 metric-type 1 subnets
exit
```


#### 🔍 Verificación:

```cisco
R_CORE# show ip route ospf
O E1 192.168.99.0/24 [110/60] via 10.1.1.1 (Costo base 50 + salto interno 10).
```



## EJEMPLO 057: MODIFICACION DE DISTANCIA ADMINISTRATIVA (ADJUST AD)


> 🏢 **ESCENARIO REAL:**
Rutas externas de EIGRP tienen AD 170 y OSPF tiene AD 110. Para resolver una
preferencia erronea de caminos, se reduce la AD de las rutas EIGRP externas a 105.


#### 💻 CONFIGURACION CISCO IOS:

```cisco
router eigrp 100
 distance eigrp 90 105   ! Internas = 90, Externas = 105
exit
```


#### 🔍 Verificación:

```cisco
R1# show ip protocols | section Distance
```



## EJEMPLO 058: INYECCION DE RUTA POR DEFECTO DESDE EIGRP A OSPF


> 🏢 **ESCENARIO REAL:**
El router Core EIGRP tiene la salida a Internet. El router frontera debe propagar
esa ruta por defecto hacia la red OSPF.


#### 💻 CONFIGURACION CISCO IOS:

```cisco
router ospf 1
 default-information originate metric 10 metric-type 1
exit
```


#### 🔍 Verificación:

```cisco
R_OSPF# show ip route ospf | include 0.0.0.0/0
```



## EJEMPLO 059: AFINACION DE HELLO Y HOLD-TIME EN ENLACES SATELITALES


> 🏢 **ESCENARIO REAL:**
Un enlace satelital tiene latencia alta de 600 ms. Los temporizadores estandar
de EIGRP (Hello 5s, Hold 15s) provocan desconexiones falsas. Se elevan los tiempos.


#### 💻 CONFIGURACION CISCO IOS:

```cisco
interface GigabitEthernet0/0/1
 description ENLACE_SATELITAL
 ip hello-interval eigrp 100 20
 ip hold-time eigrp 100 60
exit
```


#### 🔍 Verificación:

```cisco
R1# show ip eigrp interfaces detail GigabitEthernet0/0/1
```



## EJEMPLO 060: DIAGNOSTICO DE ERROR POR DISCREPANCIA DE VALORES K


> 🏢 **ESCENARIO REAL:**
Dos routers no forman adyacencia EIGRP. El log muestra:
`%DUAL-5-NBRCHANGE: K-value mismatch`.
Se diagnostica y se restablecen los valores K a sus valores por defecto (1 0 1 0 0).


#### 💻 CONFIGURACION DE REPARACION:

```text
router eigrp 100
 metric weights 0 1 0 1 0 0
exit
```


#### 🔍 Verificación:

```cisco
R1# show ip protocols | include Metric weight
```


## (Debe mostrar: K1=1, K2=0, K3=1, K4=0, K5=0).
