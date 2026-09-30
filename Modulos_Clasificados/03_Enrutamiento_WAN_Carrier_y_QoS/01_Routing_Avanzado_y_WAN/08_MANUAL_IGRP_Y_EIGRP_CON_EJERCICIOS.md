# 08. MANUAL DE IGRP Y EIGRP - DE LA HISTORIA A DUAL, METRICAS Y LABORATORIO

> **ENRUTAMIENTO AVANZADO Y TECNOLOGIAS WAN (ROUTING & WAN ARCHITECTURE)**


---



## 1. HISTORIA Y ARQUITECTURA DE IGRP (INTERIOR GATEWAY ROUTING PROTOCOL)

A mediados de la decada de 1980, las redes de computadoras crecieron rapidamente.
El protocolo dominante de la epoca, RIP (RFC 1058), mostraba graves limitaciones:
- Solo admitia hasta 15 saltos de distancia.
- Evaluaba un enlace de fibra optica de alta velocidad exactamente igual que un cable
  telefonico serial de 56 Kbps (porque ambos contaban como "1 salto").

Para solucionar esto, Cisco Systems desarrollo en 1985 su protocolo propietario:
IGRP (Interior Gateway Routing Protocol).

Innovaciones de IGRP:
- Elevo el limite de saltos de 15 a 255 (por defecto 100).
- Introdujo una Metrica Compuesta de 24 bits basada en el rendimiento fisico del enlace:
  Ancho de banda (Bandwidth), Retardo (Delay), Confiabilidad (Reliability) y Carga (Load).
- Permitio balanceo de carga en enlaces de costo desigual (Unequal-Cost Load Balancing).

¿Por que murio IGRP y fue completamente retirado?
IGRP era un protocolo "Classful" (Con clase):
- No enviaba la mascara de subred en sus difusiones periodicas.
- No tenia soporte para VLSM (Variable Length Subnet Masking) ni CIDR.
- Con la explosion de Internet en los 90 y el agotamiento de direcciones IPv4, IGRP
  quedo obsoleto. Cisco lo elimino definitivamente del codigo de IOS a partir de la version 12.3.



## 2. EL NACIMIENTO DE EIGRP (ENHANCED IGRP - RFC 7868)

Para rescatar las virtudes de IGRP pero adaptandose a la era moderna, Cisco creo
EIGRP (Enhanced Interior Gateway Routing Protocol), estandarizado abiertamente
en el RFC 7868 en el ano 2013.

EIGRP es considerado un protocolo HIBRIDO AVANZADO (Vector Distancia Avanzado):
- Mantiene la facilidad de configuracion de los protocolos de vector distancia.
- Ofrece la velocidad de convergencia ultrarrapida y la operacion libre de bucles
  caracteristica de los protocolos de estado de enlace.

Distancias Administrativas de EIGRP:
- Rutas Internas (D):             90
- Rutas Externas (D EX):         170 (Rutas redistribuidas desde OSPF, RIP o estaticas)
- Rutas Sumarizadas (hacia Null0): 5



## 3. EL ALGORITMO DUAL (DIFFUSING UPDATE ALGORITHM) Y LAS 3 TABLAS DE EIGRP

EIGRP no calcula rutas mediante Bellman-Ford ni Dijkstra. Utiliza el Algoritmo DUAL,
creado por el Dr. J.J. Garcia-Luna-Aceves en SRI International.

DUAL garantiza matematicamente que la red se mantenga LIBRE DE BUCLES EN TODO MOMENTO,
incluso durante el proceso de transicion o caida de un enlace.

LAS TRES TABLAS DE EIGRP:
1. Tabla de Vecinos (Neighbor Table):
   - Registra todos los routers adyacentes con los que se comparten paquetes Hello
     (Multicast 224.0.0.10 o FF02::A en IPv6).
2. Tabla de Topologia (Topology Table):
   - Contiene TODAS las redes conocidas anunciadas por cada uno de los vecinos, junto
     con sus respectivas metricas calculadas.
3. Tabla de Enrutamiento (Routing Table / RIB):
   - Solo almacena la MEJOR ruta (el Sucesor) para cada destino.

CONCEPTOS FUNDAMENTALES DE DUAL (MEMORIZAR PARA DISENO Y CERTIFICACIONES):


### a) Feasible Distance (FD - Distancia Factible):

   - Es la metrica total mas baja calculada por el router LOCAL para llegar al destino final.


### b) Reported Distance / Advertised Distance (RD o AD - Distancia Reportada):

   - Es la metrica que el VECINO anuncia que el tiene para alcanzar esa red destino.
   - En palabras sencillas: "Que tan lejos esta el destino desde la perspectiva de mi vecino".


### c) Sucesor (Successor):

   - Es el vecino que ofrece la menor Feasible Distance (FD).
   - Es la RUTA PRINCIPAL activa y se instala directamente en la tabla de enrutamiento.


### d) Condicion de Factibilidad (Feasibility Condition - FC):

   - REGLA MATEMATICA CRITICA:
     `RD del vecino < FD del Sucesor actual`
   - Si la distancia que el vecino afirma tener es MENOR que la distancia total que yo
     tengo actualmente por mi mejor camino, se demuestra matematicamente que ese vecino
     NO esta pasando a traves de mi, por lo que NO EXISTE POSIBILIDAD DE BUCLE.


### e) Sucesor Factible (Feasible Successor - FS):

   - Es un router vecino que NO es la mejor ruta, pero que CUMPLE con la Condicion
     de Factibilidad (RD < FD actual).
   - Es una RUTA DE RESPALDO PRE-CALCULADA guardada en memoria RAM.
   - Si el Sucesor principal muere, el Feasible Successor se convierte en Sucesor de
     forma INSTANTANEA (menos de 5 milisegundos), sin enviar mensajes de busqueda y sin
     consumir CPU.


### f) Estados de una Ruta:

   - Estado Pasivo (Passive - 'P'): Estado normal y saludable. La ruta es estable.
   - Estado Activo (Active - 'A'): El enlace principal cayo y NO HABIA ningun Feasible
     Successor en la tabla. El router entra en estado de busqueda y envia paquetes Query
     a todos sus vecinos preguntando si tienen un camino hacia esa red.
   - Problema SIA (Stuck-In-Active): Si un router vecino no responde el Query tras
     3 minutos (por saturacion de CPU o caida unidireccional), EIGRP reinicia la vecindad
     con ese router de forma forzada.



## 4. LA METRICA COMPUESTA DE EIGRP Y LOS VALORES K

EIGRP evalua 5 metricas vectoriales a traves de coeficientes llamados "Valores K":
- K1 = Bandwidth (Ancho de banda del enlace mas lento del trayecto)
- K2 = Load (Carga de trafico en la interfaz)
- K3 = Delay (Suma acumulada del retardo de todas las interfaces de salida)
- K4 = Reliability (Confiabilidad del enlace basada en errores de trama)
- K5 = MTU (Factor de ponderacion de la unidad maxima de transmision)

Valores K por defecto en Cisco:
K1 = 1,  K2 = 0,  K3 = 1,  K4 = 0,  K5 = 0.
(Nota: Todos los routers vecinos DEBEN tener exactamente los mismos valores K o no formaran adyacencia).

FORMULA DE METRICA CLASICA EIGRP:
Al aplicar los valores por defecto (K1=1, K3=1, K2=K4=K5=0), la formula se simplifica:

  Metrica = 256 * [ (10^7 / Ancho de Banda Minimo en Kbps) + (Suma de Delays / 10) ]

- Ancho de Banda Minimo: El cuello de botella del camino (el enlace mas lento).
- Retardo (Delay): La suma de los retardos de cada interfaz en microsegundos dividido por 10.
- El factor multiplicador 256: Es exactamente la constante que permite escalar la antigua
  metrica de 24 bits de IGRP a los 32 bits de EIGRP.



## 5. CARACTERISTICAS AVANZADAS EXCLUSIVAS DE EIGRP


### a) Balanceo de Carga con Costo Desigual (Unequal-Cost Load Balancing - Comando `variance`):

   - OSPF y RIP solo pueden balancear trafico si dos rutas tienen EXACTAMENTE la misma metrica.
   - EIGRP es el UNICO protocolo IGP capaz de enviar trafico proporcionalmente a traves
     de dos caminos con velocidades distintas (ejemplo: 70% por Fibra y 30% por Microondas).
   - Requisito: La ruta secundaria DEBE ser un Feasible Successor valido.
   - Comando: `variance N` (donde N es el factor multiplicador: Metrica_Secundaria <= N * FD_Principal).


### b) EIGRP Stub Routing:

   - Se configura en routers de sucursales pequenas: `router eigrp 100 -> eigrp stub`.
   - Le dice a los routers Core: "Soy una sucursal final, no tengo otras redes detras.
     NUNCA me envies paquetes Query si se cae una red en otro sitio".
   - Evita por completo los problemas de caida por Stuck-In-Active (SIA) en enlaces WAN lentos.



## 6. ESCENARIO PRACTICO DE LA VIDA REAL: CAMPUS BANCARIO CON FAILOVER INSTANTANEO



#### 🎯 OBJETIVO DEL ESCENARIO:

Un banco instala una conexion redundante entre su Edificio Corporativo y la Sucursal
Financiera Principal:
- Enlace Primario: Fibra Optica MetroEthernet de 1 Gbps (Delay: 10 usec).
- Enlace Secundario: Radioenlace Microondas dedicado de 100 Mbps (Delay: 1000 usec).

REQUERIMIENTOS:
1. Formar adyacencias EIGRP autenticadas mediante algoritmo SHA-256.
2. Garantizar que el enlace de Microondas califique como "Feasible Successor" para
   lograr un Failover instantaneo (< 5 milisegundos).
3. Activar el balanceo asimetrico de carga (`variance`) para aprovechar ambos enlaces
   durante el horario pico transaccional.


#### 🌐 DIAGRAMA DE LA TOPOLOGIA:

```text
                  +-----------------------------------+
                  |   EDIFICIO CORPORATIVO (R_CORE)   |
                  |     LAN Core: 10.100.0.0/16       |
                  +--------+-----------------+--------+
                           |                 |
     Fibra Optica 1 Gbps   |                 | Radioenlace Microondas 100 Mbps
     10.1.1.0/30 (Gi0/1)   |                 | 10.1.2.0/30 (Gi0/2)
                           |                 |
                  +--------+-----------------+--------+
                  |  SUCURSAL BANCARIA (R_SUCURSAL)   |
                  |     LAN Cajas: 192.168.50.0/24    |
                  +-----------------------------------+
```


#### 📋 TABLA DE DIRECCIONAMIENTO:


| Dispositivo | Interfaz | Direccion IP | Mascara | Ancho Banda / Delay |
| :--- | :--- | :--- | :--- | :--- |
| R_CORE | Gi0/0 | 10.100.1.1 | 255.255.0.0 | 1 Gbps / 10 usec (LAN Core) |
| R_CORE | Gi0/1 | 10.1.1.1 | 255.255.255.252 | 1 Gbps / 10 usec (WAN Fibra) |
| R_CORE | Gi0/2 | 10.1.2.1 | 255.255.255.252 | 100 Mbps / 100 usec (WAN Radio) |
| R_SUCURSAL | Gi0/0 | 192.168.50.1 | 255.255.255.0 | 1 Gbps / 10 usec (LAN Cajas) |
| R_SUCURSAL | Gi0/1 | 10.1.1.2 | 255.255.255.252 | 1 Gbps / 10 usec (WAN Fibra) |
| R_SUCURSAL | Gi0/2 | 10.1.2.2 | 255.255.255.252 | 100 Mbps / 100 usec (WAN Radio) |




## CONFIGURACION COMPLETA EN CISCO IOS / IOS-XE



## 1. CONFIGURACION EN ROUTER CORPORATIVO (R_CORE):

! Configuracion de Interfaces
```text
interface GigabitEthernet0/0
 description LAN_CORE_DATACENTER
 ip address 10.100.1.1 255.255.0.0
 no shutdown
!
interface GigabitEthernet0/1
 description WAN_FIBRA_PRIMARIA_1GBPS
 ip address 10.1.1.1 255.255.255.252
 bandwidth 1000000
 delay 1
 no shutdown
!
interface GigabitEthernet0/2
 description WAN_RADIO_RESPALDO_100MBPS
 ip address 10.1.2.1 255.255.255.252
 bandwidth 100000
 delay 10
 no shutdown
!
! Configuracion EIGRP en Modo Clasico con Autenticacion
key chain EIGRP_AUTH
 key 1
  key-string ClaveSeguraBanco2026
!
interface GigabitEthernet0/1
 ip authentication mode eigrp 100 md5
 ip authentication key-chain eigrp 100 EIGRP_AUTH
!
interface GigabitEthernet0/2
 ip authentication mode eigrp 100 md5
 ip authentication key-chain eigrp 100 EIGRP_AUTH
!
router eigrp 100
 network 10.1.1.0 0.0.0.3
 network 10.1.2.0 0.0.0.3
 network 10.100.0.0 0.0.255.255
 passive-interface GigabitEthernet0/0
 ! Activar balanceo de carga en rutas desiguales (Variance)
 variance 3
 no auto-summary
exit
```


## 2. CONFIGURACION EN ROUTER SUCURSAL (R_SUCURSAL):

key chain EIGRP_AUTH
 key 1
  key-string ClaveSeguraBanco2026
!
```text
interface GigabitEthernet0/0
 description LAN_CAJAS_Y_VENTANILLAS
 ip address 192.168.50.1 255.255.255.0
 no shutdown
!
interface GigabitEthernet0/1
 description WAN_FIBRA_PRIMARIA_1GBPS
 ip address 10.1.1.2 255.255.255.252
 bandwidth 1000000
 delay 1
 ip authentication mode eigrp 100 md5
 ip authentication key-chain eigrp 100 EIGRP_AUTH
 no shutdown
!
interface GigabitEthernet0/2
 description WAN_RADIO_RESPALDO_100MBPS
 ip address 10.1.2.2 255.255.255.252
 bandwidth 100000
 delay 10
 ip authentication mode eigrp 100 md5
 ip authentication key-chain eigrp 100 EIGRP_AUTH
 no shutdown
!
router eigrp 100
 network 10.1.1.0 0.0.0.3
 network 10.1.2.0 0.0.0.3
 network 192.168.50.0 0.0.0.255
 passive-interface GigabitEthernet0/0
 ! Configuracion Stub: Protege a la sucursal de recibir Queries en caidas del Core
 eigrp stub connected summary
 variance 3
 no auto-summary
exit
```


## VERIFICACION TECNICA Y COMPROBACION DE DUAL

1. Verificar vecinos formados y timers:
   R_SUCURSAL# show ip eigrp neighbors
   EIGRP-IPv4 Neighbors for AS(100)
   H   Address      Interface      Hold  Uptime    SRTT   RTO   Q   Seq
                                   (sec)           (ms)        Cnt  Num
   0   10.1.1.1     Gi0/1            13  00:14:02     1   200   0   12
   1   10.1.2.1     Gi0/2            12  00:14:01     3   200   0   11

2. Analisis de la Tabla de Topologia (Demostracion del Feasible Successor):
   R_SUCURSAL# show ip eigrp topology 10.100.0.0/16
   EIGRP-IPv4 Topology Entry for AS(100)/ID(192.168.50.1) for 10.100.0.0/16
     State is Passive, Query origin flag is 1, 2 Successor(s), FD is 3072
     Descriptor Blocks:
     10.1.1.1 (GigabitEthernet0/1), from 10.1.1.1, Send flag is 0x0
         Composite metric is (3072/2816), route is Internal
```text
         [FD = 3072,  RD = 2816]  <--- SUCESOR (Mejor ruta)
     10.1.2.1 (GigabitEthernet0/2), from 10.1.2.1, Send flag is 0x0
         Composite metric is (5632/2816), route is Internal
         [FD = 5632,  RD = 2816]  <--- FEASIBLE SUCCESSOR

   ¡COMPROBACION DE LA CONDICION DE FACTIBILIDAD!:
   - FD del Sucesor = 3072
   - RD del enlace secundario = 2816
   - ¿Es 2816 < 3072? SI! Por lo tanto Gi0/2 es un Feasible Successor garantizado.

3. Comprobar el balanceo de carga asimetrico en la tabla de rutas:
   R_SUCURSAL# show ip route 10.100.0.0
   Routing entry for 10.100.0.0/16
     Known via "eigrp 100", distance 90, metric 3072, type internal
     Redistributing via eigrp 100
     Routing Descriptor Blocks:
     * 10.1.1.1, from 10.1.1.1, via GigabitEthernet0/1
         Route metric is 3072, share count 18
       10.1.2.1, from 10.1.2.1, via GigabitEthernet0/2
         Route metric is 5632, share count 10

   Notese el "share count": Por cada 18 paquetes enviados por la fibra de 1 Gbps,
   EIGRP envia 10 paquetes por la microondas de 100 Mbps, aprovechando al maximo
```


el ancho de banda disponible sin provocar sobrecarga.
