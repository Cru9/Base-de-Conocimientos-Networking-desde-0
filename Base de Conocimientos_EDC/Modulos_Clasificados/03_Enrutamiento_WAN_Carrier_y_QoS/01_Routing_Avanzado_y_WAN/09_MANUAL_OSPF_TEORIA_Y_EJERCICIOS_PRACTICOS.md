# 09. MANUAL INTEGRAL DE OSPF - DE FUNDAMENTOS A MULTI-AREA Y LABORATORIO

> **ENRUTAMIENTO AVANZADO Y TECNOLOGIAS WAN (ROUTING & WAN ARCHITECTURE)**


---



## 1. ¿QUE ES OSPF Y COMO OPERA EL ALGORITMO SPF DE DIJKSTRA?

OSPF (Open Shortest Path First - RFC 2328 para IPv4 / RFC 5340 para IPv6) es el
protocolo de enrutamiento dinamico interior (IGP) mas extendido del mundo en
redes corporativas, centros de datos y campus universitarios.

A diferencia de RIP o EIGRP (que operan por "rumores" de vecinos), OSPF es un
protocolo de ESTADO DE ENLACE (Link-State):
- Cada router descubre a sus vecinos directos y el estado fisico de sus interfaces.
- Genera paquetes de estado de enlace llamados LSAs (Link State Advertisements).
- Inunda (flooding) estos LSAs a todos los demas routers dentro de su misma Area.
- Como resultado: TODOS los routers de un Area poseen EXACTAMENTE LA MISMA base
  de datos de estado de enlace (LSDB - Link-State Database).
- Cada router ejecuta de forma independiente el algoritmo SPF (Shortest Path First)
  de Edsger Dijkstra, colocandose a si mismo como la raiz de un arbol jerarquico y
  calculando el camino de menor costo matematico hacia cada subred.

Metrica de OSPF: El Costo (Cost)
  Costo = Ancho de Banda de Referencia (Reference Bandwidth) / Ancho de Banda de la Interfaz

LA TRAMPA EN REDES MODERNAS:
En el RFC original de OSPF, el ancho de banda de referencia por defecto es 100 Mbps (10^8).
Bajo esta formula clasica:
  - Interfaz FastEthernet (100 Mbps): Costo = 100M / 100M = 1
  - Interfaz GigabitEthernet (1 Gbps):  Costo = 100M / 1000M = 0.1 -> Redondeado a 1
  - Interfaz 10-Gigabit (10 Gbps):     Costo = 100M / 10000M = 0.01 -> Redondeado a 1

¡PELIGRO!: Sin configuracion adicional, un router OSPF vera una fibra de 10 Gbps con
EXACTAMENTE EL MISMO COSTO que un cable viejo de 100 Mbps.
REGLA DE PRODUCCION: En todo router moderno se debe configurar:
  `auto-cost reference-bandwidth 100000` (100 Gbps en Mbps)
para que las interfaces de 1G, 10G y 100G tengan costos diferenciados proporcionales.



## 2. LOS 5 TIPOS DE PAQUETES OSPF

OSPF no utiliza TCP ni UDP. Se encapsula directamente sobre IP usando el numero
de protocolo 89 (IP Protocol 89):

1. Paquete Hello (Tipo 1):
   - Descubre vecinos, negocia parametros y mantiene viva la adyacencia (Keepalive).
   - Enviado cada 10 seg (en Ethernet) a la direccion multicast 224.0.0.5.
2. Database Description - DBD / DDP (Tipo 2):
   - Contiene un resumen abreviado de las cabeceras de todos los LSAs en la LSDB.
   - Permite a un router verificar si su vecino conoce rutas mas recientes que el.
3. Link-State Request - LSR (Tipo 3):
   - Solicita formalmente al vecino que le envie informacion completa sobre uno o varios LSAs.
4. Link-State Update - LSU (Tipo 4):
   - Es el paquete que efectivamente transporta los LSAs completos (LSA 1, 2, 3, etc.).
5. Link-State Acknowledgment - LSAck (Tipo 5):
   - Confirmacion explicita de recibo para garantizar transmision confiable.



## 3. LOS 7 ESTADOS DE LA ADYACENCIA OSPF (MAQUINARIA DE ESTADOS)

Cuando dos routers OSPF se conectan fisicamente, atraviesan esta secuencia:

1. DOWN:
   - Estado inicial. No se han recibido paquetes Hello del vecino.
2. INIT:
   - Se recibe un Hello del vecino, pero en la lista de vecinos vistos ("Seen Neighbors")
     aun no aparece el Router-ID local. La comunicacion es unidireccional.
3. 2-WAY (Bidireccional):
   - El router local ve su propio Router-ID dentro del paquete Hello del vecino.
   - En este punto se realiza la ELECCION DE DR Y BDR (en redes multi-acceso).
   - En redes Ethernet, los routers regulares (DROTHER) permanecen permanentemente
     en estado 2-WAY entre si (no pasan a FULL).
4. EXSTART:
   - Se prepara el intercambio de la LSDB. Se determina quien es Master y quien es Slave
     segun el mayor Router-ID, y se fija el numero de secuencia inicial.
5. EXCHANGE:
   - Los routers se envian los paquetes DBD (Database Description) intercambiando
     resumenes de sus bases de datos.
6. LOADING:
   - El router envia peticiones LSR para aquellos LSAs que desconoce o estan desactualizados,
     y recibe los LSUs con los datos completos.
7. FULL:
   - Las bases de datos LSDB estan 100% sincronizadas. La adyacencia esta completa y lista.

CHECKLIST DE TROUBLESHOOTING: ¿Por que no levanta una vecindad OSPF?
Para que dos routers alcancen estado FULL deben coincidir OBLIGATORIAMENTE en:
1. Mismo Area ID.
2. Misma Subred IP y Mascara en el enlace compartido.
3. Mismos Temporizadores Hello y Dead (ej. 10s / 40s).
4. Mismo Tipo de Area (ambos Normales o ambos Stub).
5. Mismo metodo de Autenticacion y contrasena.
6. MISMA MTU en la interfaz: Si la MTU difiere (ej. 1500 vs 1492), el vecino se queda
   congelado en estado `EXSTART/EXCHANGE` eternamente.



## 4. ELECCION DE DR (DESIGNATED ROUTER) Y BDR (BACKUP DESIGNATED ROUTER)

En un segmento de red Ethernet multiacceso con N routers:
- Si cada router estableciera adyacencia FULL con todos, habria N*(N-1)/2 adyacencias.
  (Para 10 routers habria 45 sesiones, inundando el switch con copias de LSAs).
- Solucion: Se elige un "Lider" llamado DR (Designated Router) y un "Vice-Lider" llamado BDR.
- Todos los demas routers (DROTHER) solo forman adyacencia FULL con el DR y el BDR.
- Los DROTHER envian sus actualizaciones al DR/BDR mediante Multicast 224.0.0.6.
- El DR retransmite las actualizaciones al resto de los routers mediante Multicast 224.0.0.5.

Mecanismo de Eleccion:
1. Mayor Prioridad OSPF en la interfaz (`ip ospf priority 0-255`, default 1).
   - Si la prioridad es 0 (`ip ospf priority 0`), el router NUNCA sera elegido DR ni BDR.
2. Desempate: Mayor ROUTER-ID (RID):
   - 1ro: Router-ID configurado manualmente (`router-id X.X.X.X`).
   - 2do: Mayor IP en una interfaz Loopback activa.
   - 3ro: Mayor IP en una interfaz fisica activa.
3. Naturaleza "No Preventiva" (Non-preemptive):
   - Una vez electo un DR, aunque se conecte a la red un router nuevo con prioridad 255
     o un Router-ID superior, NO le quitara el puesto al DR actual para evitar
     inestabilidad y micro-cortes en la red.



## 5. ESCENARIO PRACTICO DE LA VIDA REAL: RED EMPRESARIAL MULTI-SITIO CON OSPF



#### 🎯 OBJETIVO DEL ESCENARIO:

Disenar e implementar la red corporativa de una empresa manufacturera:
- Sede Central (R_CORE): Router de Backbone en el Area 0.
- Planta de Fabricacion (R_PLANTA): Conectada al Area 10 (Area Regular de Produccion).
- Sucursal de Ventas (R_VENTAS): Conectada al Area 20 (Configurada como Area STUB
  para ahorrar memoria y proteger el enlace WAN satelital).

REQUERIMIENTOS DE PRODUCCION:
1. Estandarizar el Reference Bandwidth a 100 Gbps (`100000`).
2. Asignar Router-IDs basados en direcciones Loopback consistentes.
3. Forzar al Router Central como DR en el switch Core (`priority 255`).
4. Proteger todas las redes LAN de usuarios mediante interfaces pasivas.
5. Activar autenticacion criptografica SHA-256 en los enlaces inter-sitios.


#### 🌐 DIAGRAMA DE LA TOPOLOGIA:

```text
                        +-------------------------------------+
                        |      SEDE CENTRAL (R_CORE / ABR)    |
                        |      Router-ID: 1.1.1.1             |
                        |      LAN Datacenter: 10.0.0.0/24    |
                        |              [AREA 0]               |
                        +--------+-------------------+--------+
                                 |                   |
            Enlace WAN Planta    |                   | Enlace WAN Ventas
            172.16.1.0/30 (Gi0/1)|                   | 172.16.2.0/30 (Gi0/2)
                                 |                   |
               [AREA 10]         |                   | [AREA 20 - STUB]
                        +--------+                   +--------+
                        |                                     |
                        v                                     v
             +--------------------+                +--------------------+
             | R_PLANTA           |                | R_VENTAS           |
             | Router-ID: 2.2.2.2 |                | Router-ID: 3.3.3.3 |
             | LAN Maquinaria:    |                | LAN Oficinas:      |
             | 10.10.0.0/24       |                | 10.20.0.0/24       |
             +--------------------+                +--------------------+
```


#### 📋 TABLA DE DIRECCIONAMIENTO:


| Dispositivo | Interfaz | Direccion IP | Mascara | Area OSPF | Rol |
| :--- | :--- | :--- | :--- | :--- | :--- |
| R_CORE | Lo0 | 1.1.1.1 | 255.255.255.255 | Area 0 | Router-ID |
| R_CORE | Gi0/0 | 10.0.0.1 | 255.255.255.0 | Area 0 | LAN Datacenter |
| R_CORE | Gi0/1 | 172.16.1.1 | 255.255.255.252 | Area 10 | ABR (Hacia Planta) |
| R_CORE | Gi0/2 | 172.16.2.1 | 255.255.255.252 | Area 20 | ABR (Hacia Ventas) |
| R_PLANTA | Lo0 | 2.2.2.2 | 255.255.255.255 | Area 10 | Router-ID |
| R_PLANTA | Gi0/0 | 10.10.0.1 | 255.255.255.0 | Area 10 | LAN Maquinaria |
| R_PLANTA | Gi0/1 | 172.16.1.2 | 255.255.255.252 | Area 10 | WAN Hacia Core |
| R_VENTAS | Lo0 | 3.3.3.3 | 255.255.255.255 | Area 20 | Router-ID |
| R_VENTAS | Gi0/0 | 10.20.0.1 | 255.255.255.0 | Area 20 | LAN Oficinas |
| R_VENTAS | Gi0/2 | 172.16.2.2 | 255.255.255.252 | Area 20 | WAN Hacia Core |




## CONFIGURACION PASO A PASO EN CISCO IOS / IOS-XE



## 1. CONFIGURACION EN ROUTER CORE (R_CORE - ABR):

interface Loopback0
```text
 ip address 1.1.1.1 255.255.255.255
!
interface GigabitEthernet0/0
 description LAN_DATACENTER_CORE
 ip address 10.0.0.1 255.255.255.0
 ip ospf priority 255
 no shutdown
!
interface GigabitEthernet0/1
 description WAN_HACIA_PLANTA_AREA10
 ip address 172.16.1.1 255.255.255.252
 ip ospf authentication message-digest
 ip ospf message-digest-key 1 md5 ClaveSeguraArea10
 no shutdown
!
interface GigabitEthernet0/2
 description WAN_HACIA_VENTAS_AREA20
 ip address 172.16.2.1 255.255.255.252
 ip ospf authentication message-digest
 ip ospf message-digest-key 1 md5 ClaveSeguraArea20
 no shutdown
!
router ospf 1
 router-id 1.1.1.1
 auto-cost reference-bandwidth 100000
 passive-interface GigabitEthernet0/0
 ! Definicion del Area 20 como Stub
 area 20 stub
 ! Redes anunciadas
 network 1.1.1.1 0.0.0.0 area 0
 network 10.0.0.0 0.0.0.255 area 0
 network 172.16.1.0 0.0.0.3 area 10
 network 172.16.2.0 0.0.0.3 area 20
exit
```


## 2. CONFIGURACION EN ROUTER PLANTA (R_PLANTA - AREA 10 REGULAR):

interface Loopback0
```text
 ip address 2.2.2.2 255.255.255.255
!
interface GigabitEthernet0/0
 description LAN_MAQUINARIA_PRODUCCION
 ip address 10.10.0.1 255.255.255.0
 no shutdown
!
interface GigabitEthernet0/1
 description WAN_HACIA_CORE
 ip address 172.16.1.2 255.255.255.252
 ip ospf authentication message-digest
 ip ospf message-digest-key 1 md5 ClaveSeguraArea10
 no shutdown
!
router ospf 1
 router-id 2.2.2.2
 auto-cost reference-bandwidth 100000
 passive-interface GigabitEthernet0/0
 network 2.2.2.2 0.0.0.0 area 10
 network 10.10.0.0 0.0.0.255 area 10
 network 172.16.1.0 0.0.0.3 area 10
exit
```


## 3. CONFIGURACION EN ROUTER SUCURSAL VENTAS (R_VENTAS - AREA 20 STUB):

interface Loopback0
```text
 ip address 3.3.3.3 255.255.255.255
!
interface GigabitEthernet0/0
 description LAN_USUARIOS_VENTAS
 ip address 10.20.0.1 255.255.255.0
 no shutdown
!
interface GigabitEthernet0/2
 description WAN_HACIA_CORE
 ip address 172.16.2.2 255.255.255.252
 ip ospf authentication message-digest
 ip ospf message-digest-key 1 md5 ClaveSeguraArea20
 no shutdown
!
router ospf 1
 router-id 3.3.3.3
 auto-cost reference-bandwidth 100000
 passive-interface GigabitEthernet0/0
 ! Declaracion obligatoria de Stub en el router interno
 area 20 stub
 network 3.3.3.3 0.0.0.0 area 20
 network 10.20.0.0 0.0.0.255 area 20
 network 172.16.2.0 0.0.0.3 area 20
exit
```


## VALIDACION Y VERIFICACION EN PRODUCCION

1. Verificar que las adyacencias OSPF estan en estado FULL:
   R_CORE# show ip ospf neighbor
   Neighbor ID     Pri   State           Dead Time   Address         Interface
   2.2.2.2           1   FULL/BDR        00:00:34    172.16.1.2      GigabitEthernet0/1
   3.3.3.3           1   FULL/BDR        00:00:36    172.16.2.2      GigabitEthernet0/2

2. Observar la Base de Datos OSPF (LSDB) en el ABR (R_CORE):
   R_CORE# show ip ospf database
   Contendra:
   - Router Link States (Area 0, Area 10, Area 20) -> LSA Tipo 1
   - Summary Net Link States (Area 10, Area 20)   -> LSA Tipo 3 (Rutas Inter-Area anunciadas)

3. Comprobar la tabla de enrutamiento en la Sucursal Ventas (Area Stub):
   R_VENTAS# show ip route ospf
   Gateway of last resort is 172.16.2.1 to network 0.0.0.0

   O*IA  0.0.0.0/0 [110/101] via 172.16.2.1, 00:08:12, GigabitEthernet0/2
   O IA  10.0.0.0/24 [110/101] via 172.16.2.1, 00:08:12, GigabitEthernet0/2
   O IA  10.10.0.0/24 [110/201] via 172.16.2.1, 00:08:12, GigabitEthernet0/2

   ¡EFECTO DEL AREA STUB!:
   El router de ventas aprende automaticamente la ruta por defecto `O*IA 0.0.0.0/0`

inyectada por el ABR, evitando almacenar rutas externas innecesarias.
