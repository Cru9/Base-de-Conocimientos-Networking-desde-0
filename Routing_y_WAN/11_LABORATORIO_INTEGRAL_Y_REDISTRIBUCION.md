# 11. LABORATORIO INTEGRAL Y REDISTRIBUCION MULTI-PROTOCOLO (OSPF, EIGRP, BGP, RIP)

> **ENRUTAMIENTO AVANZADO Y TECNOLOGIAS WAN (ROUTING & WAN ARCHITECTURE)**


---



## 1. ¿QUE ES LA REDISTRIBUCION DE RUTAS Y POR QUE ES TAN CRITICA EN PRODUCCION?

En el mundo real de las redes corporativas, es comun encontrar empresas que NO
utilizan un unico protocolo de enrutamiento:
- Una compania que compro o se fusiono con otra empresa que usaba EIGRP, mientras
  su propio Datacenter utiliza OSPF.
- Sucursales remotas antiguas o equipos SCADA industriales que solo soportan RIPv2.
- Un router de borde WAN que recibe rutas por BGP desde el proveedor y debe pasarlas
  al nucleo corporativo OSPF.

La REDISTRIBUCION es el proceso de tomar las rutas aprendidas por un protocolo
(o rutas estaticas/conectadas) e inyectarlas dentro de otro protocolo de enrutamiento
totalmente diferente.



## 2. LOS 3 PELIGROS MORTALES DE LA REDISTRIBUCION Y SUS SOLUCIONES


### a) El Problema de la Metrica Semilla (Seed Metric):

   - Cada protocolo calcula la distancia de forma diferente: OSPF usa costo en ancho
     de banda, EIGRP usa formula compuesta (ancho de banda + retardo), y RIP usa saltos.
   - Si redistribuyes rutas de OSPF hacia RIP sin definir una metrica, RIP asigna
     por defecto una metrica de INFINITO (16 saltos), haciendo que la ruta sea inalcanzable.
   - Si redistribuyes hacia EIGRP sin especificar metricas K, EIGRP asigna metrica infinita.
   - SOLUCION: Configurar SIEMPRE una "Metrica Semilla" (Seed Metric) explicita:
     * Al inyectar a OSPF: `redistribute ... metric 20 subnets` (Tipo E2 por defecto).
     * Al inyectar a EIGRP: `redistribute ... metric 10000 100 255 1 1500` (BW, Delay, Rel, Load, MTU).
     * Al inyectar a RIP: `redistribute ... metric 2`.


### b) Enrutamiento Suboptimo por Distancia Administrativa (AD):

   - Si dos routers de borde redistribuyen entre OSPF (AD 110) y EIGRP (AD 90):
     Una ruta aprendida por OSPF puede ser redistribuida a EIGRP, donde ahora tiene AD 90.
     El segundo router de borde vera que la ruta por EIGRP es mas confiable (AD 90 < 110)
     y preferira enviar los paquetes hacia EIGRP en vez de OSPF, generando trayectorias en circulo.


### c) Bucles de Enrutamiento y "Domain Loopback":

   - Ocurre cuando una ruta originada en OSPF entra a EIGRP y luego vuelve a ser
     redistribuida de EIGRP hacia OSPF.
   - SOLUCION INDUSTRIAL: ROUTE TAGGING (Etiquetado de Rutas con Route-Maps):
     * Cuando una ruta sale de OSPF hacia EIGRP, se le estampa una etiqueta numerica: `set tag 110`.
     * En el sentido contrario, el router filtra: "Si una ruta trae el tag 110, NO la aceptes de regreso".



## 3. ESCENARIO DE LABORATORIO INTEGRAL: LA EMPRESA MULTINACIONAL HIBRIDA


TOPOLOGIA DEL LABORATORIO:

 [SUCURSAL LEGACY]         [ROUTER BORDE 1]            [ROUTER CORE]           [ROUTER BORDE 2]         [PROVEEDOR ISP]
    (R_SUCURSAL)             (R_DIST_1)                  (R_CORE)                (R_BORDE_WAN)               (R_ISP)
       (RIPv2)           (RIPv2 <-> OSPF)                (OSPF)                  (OSPF <-> BGP)               (BGP)
   192.168.99.0/24                                     ÁREA 0                                               AS 65500
          |                      |                       |                       |                             |
          +====== 10.1.1.0/30 ===+====== 10.2.2.0/30 ====+=+==== 10.3.3.0/30 ===+====== 203.0.113.0/30 ======+
                                                         |
                                                         | 10.4.4.0/30
                                                         |
                                                  [ROUTER BORDE 3]
                                                     (R_DIST_2)
                                                 (OSPF <-> EIGRP)
                                                         |
                                                         | 10.5.5.0/30
                                                         |
                                                  [PLANTA MINERA]
                                                    (R_MINERIA)
                                                    (EIGRP 100)
                                                  172.16.50.0/24

TABLA RESUMEN DE PROTOCOLOS Y REDES:

| Segmento Red | Protocolo Nativo | Dispositivos Involucrados |
| :--- | :--- | :--- |
| 192.168.99.0/24 | RIPv2 | LAN Sucursal Legacy (R_SUCURSAL) |
| 10.1.1.0/30 | RIPv2 | Enlace WAN R_SUCURSAL <-> R_DIST_1 |
| 10.2.2.0/30 | OSPF Area 0 | Enlace Core R_DIST_1 <-> R_CORE |
| 10.3.3.0/30 | OSPF Area 0 | Enlace Core R_CORE <-> R_BORDE_WAN |
| 10.4.4.0/30 | OSPF Area 0 | Enlace Core R_CORE <-> R_DIST_2 |
| 10.5.5.0/30 | EIGRP AS 100 | Enlace WAN R_DIST_2 <-> R_MINERIA |
| 172.16.50.0/24 | EIGRP AS 100 | LAN Servidores Mineria (R_MINERIA) |
| 203.0.113.0/30 | eBGP (AS65001-65500)Enlace Internet R_BORDE_WAN <-> R_ISP |  |




## CONFIGURACION DE LOS PUNTOS DE REDISTRIBUCION (CISCO IOS)



## PUNTO 1: ROUTER DE DISTRIBUCION 1 (R_DIST_1 - REDISTRIBUCION RIPv2 <-> OSPF):

! 1. Interfaces
```text
interface GigabitEthernet0/1
 description ENLACE_HACIA_SUCURSAL_RIP
 ip address 10.1.1.2 255.255.255.252
 no shutdown
!
interface GigabitEthernet0/2
 description ENLACE_HACIA_CORE_OSPF
 ip address 10.2.2.1 255.255.255.252
 no shutdown
!
! 2. Politica de Prevencion de Bucles con Route Tagging
route-map RIP_A_OSPF permit 10
 set tag 120
 metric 30
 metric-type type-2
!
route-map OSPF_A_RIP permit 10
 match ip address prefix-list REDES_VALIDAS
!
ip prefix-list REDES_VALIDAS permit 172.16.50.0/24
ip prefix-list REDES_VALIDAS permit 10.0.0.0/8 le 30
!
! 3. Proceso RIP con inyeccion de OSPF
router rip
 version 2
 no auto-summary
 network 10.1.1.0
 ! Inyectar rutas OSPF hacia RIP con metrica semilla de 2 saltos
 redistribute ospf 1 metric 2 route-map OSPF_A_RIP
exit
!
! 4. Proceso OSPF con inyeccion de RIP
router ospf 1
 router-id 11.11.11.11
 network 10.2.2.0 0.0.0.3 area 0
 ! Inyectar rutas RIP hacia OSPF con el tag 120 para trazabilidad
 redistribute rip subnets route-map RIP_A_OSPF
exit
```


## PUNTO 2: ROUTER DE DISTRIBUCION 2 (R_DIST_2 - REDISTRIBUCION EIGRP <-> OSPF):

! 1. Interfaces
```text
interface GigabitEthernet0/1
 description ENLACE_HACIA_MINERIA_EIGRP
 ip address 10.5.5.1 255.255.255.252
 no shutdown
!
interface GigabitEthernet0/2
 description ENLACE_HACIA_CORE_OSPF
 ip address 10.4.4.2 255.255.255.252
 no shutdown
!
! 2. Route-Maps para etiquetar y evitar retro-alimentacion
route-map EIGRP_A_OSPF permit 10
 set tag 90
!
route-map OSPF_A_EIGRP deny 10
 match tag 90        ! Si la ruta ya vino de EIGRP, ¡NO volver a enviarla a EIGRP!
!
route-map OSPF_A_EIGRP permit 20
!
! 3. Proceso OSPF
router ospf 1
 router-id 22.22.22.22
 network 10.4.4.0 0.0.0.3 area 0
 ! Inyectar EIGRP hacia OSPF como rutas externas E2 con tag 90
 redistribute eigrp 100 subnets route-map EIGRP_A_OSPF
exit
!
! 4. Proceso EIGRP con metrica semilla obligatoria de 5 vectores (K1-K5)
router eigrp 100
 network 10.5.5.0 0.0.0.3
 no auto-summary
 ! Inyectar OSPF con: Bandwidth=1000000 (1G), Delay=10 (100usec), Rel=255, Load=1, MTU=1500
 redistribute ospf 1 metric 1000000 10 255 1 1500 route-map OSPF_A_EIGRP
exit
```


## PUNTO 3: ROUTER BORDE WAN (R_BORDE_WAN - REDISTRIBUCION OSPF <-> BGP):

! 1. Interfaces
```text
interface GigabitEthernet0/1
 description ENLACE_HACIA_CORE_OSPF
 ip address 10.3.3.2 255.255.255.252
 no shutdown
!
interface GigabitEthernet0/2
 description ENLACE_HACIA_ISP_INTERNET
 ip address 203.0.113.2 255.255.255.252
 no shutdown
!
! 2. Proceso OSPF
router ospf 1
 router-id 33.33.33.33
 network 10.3.3.0 0.0.0.3 area 0
 ! Inyectar unicamente la ruta por defecto aprendida de BGP hacia OSPF
 default-information originate
exit
!
! 3. Proceso BGP: Anunciar las redes corporativas internas hacia el ISP
ip prefix-list BLOQUE_CORPORATIVO permit 192.168.99.0/24
ip prefix-list BLOQUE_CORPORATIVO permit 172.16.50.0/24
!
route-map OSPF_A_BGP permit 10
 match ip address prefix-list BLOQUE_CORPORATIVO
!
router bgp 65001
 bgp router-id 33.33.33.33
 neighbor 203.0.113.1 remote-as 65500
 neighbor 203.0.113.1 description UPLINK_CARRIER
 ! Redistribuir las redes autorizadas de OSPF hacia BGP
 redistribute ospf 1 route-map OSPF_A_BGP
exit
```


## VERIFICACION DEL ESCENARIO COMPLETO EN EL ROUTER CORE (R_CORE)

1. Inspeccionar la tabla de rutas del Router Core (`show ip route`):
   R_CORE# show ip route
   Gateway of last resort is 10.3.3.2 to network 0.0.0.0

   O*E2  0.0.0.0/0 [110/1] via 10.3.3.2, 00:04:15, GigabitEthernet0/3  (Ruta por defecto via BGP)
   O     10.1.1.0/30 [110/2] via 10.2.2.1, 00:12:08, GigabitEthernet0/1
   O     10.5.5.0/30 [110/2] via 10.4.4.2, 00:12:08, GigabitEthernet0/2
   O E2  172.16.50.0/24 [110/20] via 10.4.4.2, 00:11:45, GigabitEthernet0/2 (Tag 90 - Desde EIGRP)
   O E2  192.168.99.0/24 [110/30] via 10.2.2.1, 00:09:30, GigabitEthernet0/1 (Tag 120 - Desde RIPv2)

   ANALISIS CLAVE:
   - Todas las redes de la empresa aparecen unificadas en la tabla del Core bajo el formato `O E2`
     (Rutas externas de OSPF Tipo 2).
   - Tanto la sucursal antigua que habla RIP como la planta minera que habla EIGRP
     pueden comunicarse entre si de extremo a extremo sin que ninguno de los dos
     sepa que el otro usa un protocolo diferente.

2. Prueba de Conectividad Extremo a Extremo (Ping desde Sucursal RIP hasta Mineria EIGRP):
   R_SUCURSAL# ping 172.16.50.1 source GigabitEthernet0/0
   Type escape sequence to abort.
   Sending 5, 100-byte ICMP Echos to 172.16.50.1, timeout is 2 seconds:
   Packet sent with a source address of 192.168.99.1
   !!!!!
   Success rate is 100 percent (5/5), round-trip min/avg/max = 4/8/12 ms

3. Comprobacion de Etiquetas de Ruta (Route Tags) para Auditoria:
   R_CORE# show ip route 172.16.50.0
   Routing entry for 172.16.50.0/24
     Known via "ospf 1", distance 110, metric 20, type extern 2, forward metric 1

## Route tag 90   <--- ¡Etiqueta preservada que previene bucles de retorno!
