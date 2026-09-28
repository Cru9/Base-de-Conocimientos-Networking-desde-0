# 10. MANUAL INTEGRAL DE BGP - ARQUITECTURA, ATRIBUTOS Y LABORATORIO MULTIHOMING

> **ENRUTAMIENTO AVANZADO Y TECNOLOGIAS WAN (ROUTING & WAN ARCHITECTURE)**


---



## 1. ¿QUE ES BGP Y POR QUE DOMINA LA INFRAESTRUCTURA MUNDIAL DE INTERNET?

BGP (Border Gateway Protocol Version 4 - RFC 4271) es el unico protocolo de
enrutamiento exterior (EGP) que hace funcionar a Internet, interconectando a miles
de Proveedores de Servicios (ISPs), hiperescaladores (Google, AWS, Microsoft, Cloudflare)
y redes corporativas en todo el planeta.

A diferencia de los protocolos interiores (IGP como OSPF o EIGRP), que estan diseñados
para encontrar el camino mas veloz dentro de una empresa, BGP es un protocolo
VECTOR DE RUTA (Path Vector) diseñado para aplicar POLITICAS COMERCIALES, FINANCIERAS
Y DE SEGURIDAD entre organizaciones independientes.

Caracteristicas Fundamentales de BGP:
- Opera sobre el protocolo de transporte TCP en el puerto 179 (sesiones confiables punto a punto).
- No requiere transmisiones broadcast ni multicast (las sesiones de peering se configuran
  con IPs unicast explicitas).
- Escalabilidad masiva: La tabla BGP global de Internet contiene actualmente mas
  de 950,000 prefijos IPv4 y 200,000 prefijos IPv6 sin colapsar.
- Confiabilidad: Utiliza mensajes KEEPALIVE periodicos (por defecto cada 60 seg en Cisco,
  Hold-Time de 180 seg).



## 2. SISTEMAS AUTONOMOS (AS) Y TIPOS DE SESIONES: eBGP vs iBGP

Un Sistema Autonomo (AS) es un conjunto de redes IP gestionadas bajo una administracion
tecnica unica y una politica de enrutamiento uniforme. Cada AS se identifica mediante
un numero unico ASN (Autonomous System Number).

Rangos de Numeros de Sistema Autonomo (ASN):
- Formato 16 bits (Clasico): 1 a 65,535.
  * Publicos (asignados por RIRs como LACNIC, ARIN, RIPE): 1 a 64,495.
  * Privados (uso corporativo interno RFC 6996): 64,512 a 65,534.
- Formato 32 bits (Moderno): 1 a 4,294,967,295 (ej. AS13335 Cloudflare).

COMPARATIVA DETALLADA: eBGP vs iBGP

| Caracteristica | eBGP (External BGP) | iBGP (Internal BGP) |
| :--- | :--- | :--- |
| Ubicacion | Entre routers de DISTINTOS AS | Entre routers del MISMO AS |
| Distancia Administrativa | 20 (Cisco) | 200 (Cisco) |
| TTL por defecto | TTL = 1 (Enlace directo fisico) | TTL = 255 (Multisalto dentro del AS) |
| Multihop necesario | Si se usa IP Loopback | No requerido |
| Modificacion de Next-Hop | Cambia a la IP del router local | NO CAMBIA (requiere next-hop-self) |
| Regla de Reenvio | Libre | Regla de Split-Horizon iBGP |


LA REGLA DE SPLIT-HORIZON DE iBGP Y SOLUCIONES DE ESCALABILIDAD:
- Regla: "Un router iBGP NO propagara a otro vecino iBGP una ruta que el aprendio
  de un tercer vecino iBGP". Esto previene bucles dentro del Sistema Autonomo.
- El dilema: Para que todos los routers conozcan todas las rutas, se requeria una
  malla completa (Full Mesh) de sesiones iBGP: N*(N-1)/2 sesiones (con 50 routers serian
  1,225 sesiones TCP simultaneas).
- Solucion Moderna: BGP Route Reflectors (RR - RFC 4456):
  Un router central actua como concentrador y tiene permiso para retransmitir prefijos
  a sus clientes ("Route Reflector Clients"), reduciendo las conexiones a una estrella simple.



## 3. ATRIBUTOS BGP Y EL ALGORITMO BEST PATH DE CISCO

BGP no calcula un costo simple; asocia un paquete de ATRIBUTOS a cada red.

Clasificacion de Atributos:
1. Well-Known Mandatory (Obligatorios y reconocidos por todos):
   - AS-Path (Secuencia de ASNs por donde ha viajado el prefijo; previene bucles si el propio AS aparece).
   - Next-Hop (La IP del siguiente salto).
   - Origin (IGP 'i', EGP 'e', Incomplete '?').
2. Well-Known Discretionary (Reconocidos por todos, pero opcionales en el update):
   - Local Preference (Preferencia dentro del AS local).
   - Atomic Aggregate.
3. Optional Transitive (Opcionales, pero si un router no los soporta los reenvia intactos):
   - BGP Communities (Etiquetas numericas para marcar trafico y automatizar politicas).
4. Optional Non-Transitive (Opcionales; si no se soportan o no aplican se descartan):
   - MED (Multi-Exit Discriminator).

ALGORITMO PASO A PASO: SELECCION DE LA MEJOR RUTA (BEST PATH)
Cuando un router recibe multiples caminos hacia la misma IP de destino, aplica esta
cascada eliminatoria estricta (¡Regla de Oro de Ingenieria!):

1. MAYOR WEIGHT (Peso):
   - 0 a 65,535. Exclusivo de Cisco, local al router (no se envia a ningun vecino).
2. MAYOR LOCAL PREFERENCE (Preferencia Local):
   - Estandar de la industria. Se propaga dentro de todo el AS local. Por defecto = 100.
   - ¡HERRAMIENTA PRINCIPAL PARA CONTROLAR EL TRAFICO DE SALIDA (OUTBOUND)!
3. ORIGEN LOCAL:
   - Prefiere rutas originadas localmente (`network` o `redistribute`) sobre las aprendidas.
4. AS-PATH MAS CORTO:
   - Prefiere la ruta que atraviese la menor cantidad de Sistemas Autonomos.
   - ¡HERRAMIENTA PRINCIPAL PARA CONTROLAR EL TRAFICO DE ENTRADA (INBOUND)!
   - Tecnica: AS-Path Prepending (agregar copias repetidas del propio ASN para que
     el camino se vea mas largo y los clientes externos prefieran la otra ruta).
5. CODIGO DE ORIGEN MAS BAJO:
   - Prefiere IGP (i) sobre EGP (e), y este sobre Incomplete (?).
6. MENOR MED (Multi-Exit Discriminator):
   - Se anuncia a un ISP vecino para sugerirle por cual de sus enlaces entrar a nuestra empresa.
7. eBGP SOBRE iBGP:
   - Prefiere rutas aprendidas por vecinos eBGP sobre vecinos iBGP.
8. MENOR COSTO METRICO IGP AL NEXT-HOP:
   - Prefiere el camino mas corto internamente (menor costo OSPF/EIGRP hacia el router de borde).
9. MENOR ROUTER-ID:
   - Desempate definitivo por la IP mas baja del identificador BGP.



## 4. ESCENARIO PRACTICO DE LA VIDA REAL: MULTIHOMING CORPORATIVO CON DUAL-ISP



#### 🎯 OBJETIVO DEL ESCENARIO:

Una empresa de servicios financieros adquiere su propio bloque publico asignado:
`198.51.100.0/24` y su Sistema Autonomo privado `AS 65000`.
Se conecta a dos proveedores de Internet diferentes:
1. ISP-1 (AS 65100): Enlace de Fibra Optica Primario de 1 Gbps (Carrier Telmex / Lumen).
2. ISP-2 (AS 65200): Enlace de Respaldo Microondas de 100 Mbps (Carrier Alestra / Cogent).

POLITICAS DE TRAFICO EXIGIDAS EN PRODUCCION:
1. Control de Salida (Outbound Traffic):
   - El 100% de la navegacion y consumo de Internet de la empresa DEBE salir por ISP-1.
   - Si el enlace ISP-1 cae, el trafico saliente debe conmutar automaticamente a ISP-2.
   - Metodo tecnico: Asignar `Local-Preference 200` a las rutas de ISP-1 y `100` a ISP-2.
2. Control de Entrada (Inbound Traffic):
   - Todo el trafico de clientes mundiales que visitan los servidores web corporativos
     DEBE ingresar a traves de ISP-1.
   - Si ISP-1 cae, deben ingresar por ISP-2.
   - Metodo tecnico: Anunciar el prefijo limpio a ISP-1, y aplicar `as-path prepend 65000 65000 65000`
     hacia ISP-2 para penalizar la ruta alternativa a nivel mundial.
3. Prevenir ser Sistema de Transito (Transit AS):
   - La empresa JAMAS debe retransmitir las rutas de ISP-1 hacia ISP-2; de lo contrario,
     trafico de terceros que no le pertenece cruzaria por sus enlaces WAN saturandolos.


#### 🌐 DIAGRAMA DE LA TOPOLOGIA:

```text
                        +----------------------+
                        |   INTERNET GLOBAL    |
                        +----+------------+----+
                             |            |
                     +-------+            +-------+
                     |                            |
           +---------+---------+        +---------+---------+
           |       ISP-1       |        |       ISP-2       |
           |      AS 65100     |        |      AS 65200     |
           |   (Primario 1G)   |        |  (Respaldo 100M)  |
           +---------+---------+        +---------+---------+
                     |                            |
        203.0.113.1  |                            | 198.18.1.1
                     |                            |
        203.0.113.2  |                            | 198.18.1.2
           +---------+----------------------------+---------+
           |                ROUTER BORDE                    |
           |           EMPRESA (R_BORDE_EMPRESA)            |
           |                   AS 65000                     |
           |      Prefijo Publico: 198.51.100.0/24          |
           +-----------------------+------------------------+
                                   | LAN Interna: 10.0.0.0/16
                                   v
```


#### 📋 TABLA DE DIRECCIONAMIENTO:


| Dispositivo | Interfaz | Direccion IP | Mascara | ASN | Rol |
| :--- | :--- | :--- | :--- | :--- | :--- |
| R_BORDE_EMPRESA | Gi0/1 | 203.0.113.2 | 255.255.255.252 | 65000 | Uplink hacia ISP-1 |
| R_BORDE_EMPRESA | Gi0/2 | 198.18.1.2 | 255.255.255.252 | 65000 | Uplink hacia ISP-2 |
| R_BORDE_EMPRESA | Lo0 | 198.51.100.1 | 255.255.255.0 | 65000 | Prefijo Publico |
| ISP-1 | Gi0/1 | 203.0.113.1 | 255.255.255.252 | 65100 | Carrier Primario |
| ISP-2 | Gi0/2 | 198.18.1.1 | 255.255.255.252 | 65200 | Carrier Respaldo |




## CONFIGURACION PASO A PASO EN CISCO IOS / IOS-XE



## 1. CONFIGURACION DEL ROUTER DE BORDE DE LA EMPRESA (R_BORDE_EMPRESA):

! Configuracion de Interfaces
interface Loopback0
 description BLOQUE_PUBLICO_EMPRESA
```text
 ip address 198.51.100.1 255.255.255.0
!
interface GigabitEthernet0/1
 description ENLACE_PRIMARIO_FIBRA_ISP1
 ip address 203.0.113.2 255.255.255.252
 no shutdown
!
interface GigabitEthernet0/2
 description ENLACE_RESPALDO_MICROONDAS_ISP2
 ip address 198.18.1.2 255.255.255.252
 no shutdown
!
! Crear ruta de descarte Null0 para anclar el bloque publico y evitar caidas de anuncio
ip route 198.51.100.0 255.255.255.0 Null0
!
! -----------------------------------------------------------------------------
! DEFINICION DE PREFIX-LISTS: Seguridad Estricta
! -----------------------------------------------------------------------------
! Solo permitir anunciar NUESTRO prefijo publico a los proveedores (Anti-Transito)
ip prefix-list NUESTRO_PREFIJO permit 198.51.100.0/24
!
! Aceptar cualquier ruta que nos envie el ISP
ip prefix-list RUTA_POR_DEFECTO permit 0.0.0.0/0
!
! -----------------------------------------------------------------------------
! DEFINICION DE ROUTE-MAPS: Ingenieria de Trafico
! -----------------------------------------------------------------------------
! Politica de Entrada desde ISP-1: Forzar salida por aqui con Local-Preference 200
route-map RM_IN_ISP1 permit 10
 set local-preference 200
!
! Politica de Entrada desde ISP-2: Prioridad normal (100)
route-map RM_IN_ISP2 permit 10
 set local-preference 100
!
! Politica de Salida hacia ISP-1: Anunciar nuestro prefijo normal y limpio
route-map RM_OUT_ISP1 permit 10
 match ip address prefix-list NUESTRO_PREFIJO
!
! Politica de Salida hacia ISP-2: Anunciar con AS-Path Prepending (Castigar 3 saltos)
route-map RM_OUT_ISP2 permit 10
 match ip address prefix-list NUESTRO_PREFIJO
 set as-path prepend 65000 65000 65000
!
! -----------------------------------------------------------------------------
! PROCESO BGP PRINCIPAL
! -----------------------------------------------------------------------------
router bgp 65000
 bgp router-id 198.51.100.1
 bgp log-neighbor-changes
 ! Anunciar nuestro bloque en la tabla global
 network 198.51.100.0 mask 255.255.255.0
 !
 ! Vecino ISP-1 (Primario)
 neighbor 203.0.113.1 remote-as 65100
 neighbor 203.0.113.1 description PEERING_PRIMARIO_FIBRA_ISP1
 neighbor 203.0.113.1 route-map RM_IN_ISP1 in
 neighbor 203.0.113.1 route-map RM_OUT_ISP1 out
 !
 ! Vecino ISP-2 (Respaldo)
 neighbor 198.18.1.1 remote-as 65200
 neighbor 198.18.1.1 description PEERING_RESPALDO_MICROONDAS_ISP2
 neighbor 198.18.1.1 route-map RM_IN_ISP2 in
 neighbor 198.18.1.1 route-map RM_OUT_ISP2 out
exit
```


## 2. CONFIGURACION DE VERIFICACION EN LOS ROUTERS ISP (PARA LABORATORIO)

! En ISP-1 (AS 65100):
router bgp 65100
 neighbor 203.0.113.2 remote-as 65000
 default-information originate
 neighbor 203.0.113.2 default-originate
exit

! En ISP-2 (AS 65200):
router bgp 65200
 neighbor 198.18.1.2 remote-as 65000
 default-information originate
 neighbor 198.18.1.2 default-originate
exit



## DIAGNOSTICO Y COMPROBACION DE INGENIERIA DE TRAFICO

1. Verificar estado de las sesiones BGP (debe mostrar prefijos en State/PfxRcd):
   R_BORDE_EMPRESA# show ip bgp summary
   Neighbor        V    AS    MsgRcvd MsgSent   TblVer  InQ OutQ Up/Down  State/PfxRcd
   203.0.113.1     4 65100         45      48        7    0    0 00:32:15        1
   198.18.1.1      4 65200         44      47        7    0    0 00:31:50        1

2. Analisis de la tabla BGP y seleccion de la mejor ruta (Best Path):
   R_BORDE_EMPRESA# show ip bgp
   BGP table version is 7, local router ID is 198.51.100.1
   Status codes: s suppressed, d damped, h history, * valid, > best, i - internal
   Origin codes: i - IGP, e - EGP, ? - incomplete

      Network          Next Hop            Metric LocPrf Weight Path
   *> 0.0.0.0          203.0.113.1                    200      0 65100 i  <--- GANA (LocPrf 200!)
   *  0.0.0.0          198.18.1.1                     100      0 65200 i
   *> 198.51.100.0/24  0.0.0.0                  0         32768 i

   Explicacion:
   La ruta `0.0.0.0` a traves de ISP-1 tiene el simbolo `>` (Best Path) porque su
   `LocPrf` es 200, mientras que ISP-2 tiene `LocPrf` 100.
   Por tanto, todo el trafico de salida de la empresa viajara por ISP-1.

3. Comprobar que rutas le estamos anunciando a cada ISP:
   Hacia ISP-1 (Ruta limpia, sin penalizacion):
   R_BORDE_EMPRESA# show ip bgp neighbors 203.0.113.1 advertised-routes
      Network          Next Hop            Metric LocPrf Weight Path
   *> 198.51.100.0/24  0.0.0.0                  0         32768 i

   Hacia ISP-2 (Ruta con Prepending para desviar el trafico de entrada):
   R_BORDE_EMPRESA# show ip bgp neighbors 198.18.1.1 advertised-routes
      Network          Next Hop            Metric LocPrf Weight Path
   *> 198.51.100.0/24  0.0.0.0                  0         32768 65000 65000 65000 i

   ¡VALIDACION EXITOSA!:
   En Internet, el resto de los routers del planeta veran que para llegar a la empresa
   por ISP-2 deben cruzar 4 saltos de AS (65200 65000 65000 65000), mientras que por
   ISP-1 solo deben cruzar 2 saltos (65100 65000). Por regla del AS-Path mas corto,

el 100% del trafico entrante llegara por la fibra primaria de ISP-1.
