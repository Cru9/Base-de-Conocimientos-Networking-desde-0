# PARTE 1: SWITCHING Y ENRUTAMIENTO BASICO (EJEMPLOS 001 AL 020)

> **ENRUTAMIENTO AVANZADO Y REDES WAN - GUIA PRACTICA DEFINITIVA**


---



## EJEMPLO 001: CONEXION BASICA DE DOS SWITCHES CON VLAN DE GESTION Y ACCESO


> 🏢 **ESCENARIO REAL:**
En una pequena oficina se requiere conectar dos switches de 24 puertos para ampliar
la capacidad de red de los empleados. Se debe configurar una IP de gestion (SVI)
para administracion remota via SSH/Telnet en la VLAN 1 y habilitar los puertos de acceso.


#### 🌐 DIAGRAMA:

```text
  [PC 1]                             [PC 2]
    | (Fa0/1)                          | (Fa0/1)
+---+----+                         +---+----+
|  SW-1  +=========================+  SW-2  |
+--------+        (Gi0/1)          +--------+
IP: 192.168.1.2                   IP: 192.168.1.3
              Red LAN: 192.168.1.0/24
```


#### 💻 CONFIGURACION CISCO IOS:

```cisco
! En Switch 1:
enable
configure terminal
hostname SW-1
interface vlan 1
 ip address 192.168.1.2 255.255.255.0
 no shutdown
exit
ip default-gateway 192.168.1.1
interface FastEthernet0/1
 description CONEXION_PC1
 switchport mode access
 switchport access vlan 1
 no shutdown
exit
interface GigabitEthernet0/1
 description ENLACE_HACIA_SW2
 switchport mode access
 no shutdown
exit

! En Switch 2:
enable
configure terminal
hostname SW-2
interface vlan 1
 ip address 192.168.1.3 255.255.255.0
 no shutdown
exit
ip default-gateway 192.168.1.1
interface FastEthernet0/1
 description CONEXION_PC2
 switchport mode access
 switchport access vlan 1
 no shutdown
exit
interface GigabitEthernet0/1
 description ENLACE_HACIA_SW1
 switchport mode access
 no shutdown
exit
```


#### 🔍 Verificación:

```cisco
SW-1# ping 192.168.1.3
SW-1# show ip interface brief | include Vlan1
```



## EJEMPLO 002: SEGMENTACION DEPARTAMENTAL CON VLANS (VLAN 10 VENTAS Y 20 TI)


> 🏢 **ESCENARIO REAL:**
Para evitar que los empleados de Ventas tengan acceso directo a los servidores
y computadoras del area de TI en la misma oficina, se crean dos VLANs independientes.
El switch aislara el trafico de broadcast de cada departamento a nivel de Capa 2.


#### 🌐 DIAGRAMA:

```text
     [PC_VENTAS] (192.168.10.10)        [PC_TI] (192.168.20.10)
          |                                  |
          | (Fa0/1 - VLAN 10)                | (Fa0/2 - VLAN 20)
     +----+----------------------------------+----+
     |             SWITCH ACCESO (SW-ACCESO)      |
     +--------------------------------------------+
```


#### 💻 CONFIGURACION CISCO IOS:

```cisco
vlan 10
 name VENTAS
exit
vlan 20
 name TI_SISTEMAS
exit

interface FastEthernet0/1
 description PUERTO_USUARIO_VENTAS
 switchport mode access
 switchport access vlan 10
 no shutdown
exit

interface FastEthernet0/2
 description PUERTO_USUARIO_TI
 switchport mode access
 switchport access vlan 20
 no shutdown
exit
```


#### 🔍 Verificación:

```cisco
SW-ACCESO# show vlan brief
(Debe mostrar VLAN 10 con Fa0/1 y VLAN 20 con Fa0/2).
```



## EJEMPLO 003: ENLACE TRONCAL 802.1Q CON VLAN NATIVA SEGURA


> 🏢 **ESCENARIO REAL:**
Conectar el switch de la Planta Baja con el switch del Primer Piso. A traves del
cable de interconexion deben viajar ambas VLANs (10 y 20) etiquetadas con IEEE 802.1Q.
Por seguridad, se cambia la VLAN Nativa por defecto (VLAN 1) a una VLAN muerta (VLAN 999).


#### 🌐 DIAGRAMA:

```text
  +---------------+                           +---------------+
  |  SW_PLANTA_1  +===========================+  SW_PLANTA_2  |
  +---------------+          (Gi0/1)          +---------------+
   VLAN 10, 20               TRONCAL           VLAN 10, 20
                        VLAN Nativa: 999
```


#### 💻 CONFIGURACION CISCO IOS (EN AMBOS SWITCHES):

```cisco
vlan 999
 name VLAN_NATIVA_SEGURA
exit

interface GigabitEthernet0/1
 description ENLACE_TRONCAL_INTER_SWITCH
 switchport trunk encapsulation dot1q   ! (En modelos Catalyst 3750/3850)
 switchport mode trunk
 switchport trunk native vlan 999
 switchport trunk allowed vlan 10,20,999
 no shutdown
exit
```


#### 🔍 Verificación:

```cisco
SW_PLANTA_1# show interfaces trunk
(Comprobar que Gi0/1 esta en modo 'trunking' y la Native VLAN es 999).
```



## EJEMPLO 004: ROUTER-ON-A-STICK (INTER-VLAN ROUTING CON SUBINTERFACES)


> 🏢 **ESCENARIO REAL:**
Las PCs de la VLAN 10 (Ventas) necesitan comunicarse con el servidor de la VLAN 20.
Como un switch Capa 2 no enruta, se utiliza un Router conectado mediante un unico
cable fisico (Troncal) dividiendo la interfaz en subinterfaces logicas (.10 y .20).


#### 🌐 DIAGRAMA:

```text
                   [ROUTER R1]
                        | (Gi0/0/0 - Troncal Subinterfaces)
                        |  .10: 192.168.10.1 (Gateway)
                        |  .20: 192.168.20.1 (Gateway)
                        v
                 +--------------+
                 |  SWITCH L2   |
                 +---+------+---+
                     |      |
             (Fa0/1) |      | (Fa0/2)
                     v      v
              [VLAN 10]    [VLAN 20]
```


#### 💻 CONFIGURACION CISCO IOS:

```cisco
! En el Switch:
interface GigabitEthernet0/1
 description TRONCAL_HACIA_ROUTER
 switchport mode trunk
 no shutdown
exit

! En el Router R1:
interface GigabitEthernet0/0/0
 description ENLACE_FISICO_HACIA_SWITCH
 no ip address
 no shutdown
exit

interface GigabitEthernet0/0/0.10
 description GATEWAY_VLAN_10_VENTAS
 encapsulation dot1Q 10
 ip address 192.168.10.1 255.255.255.0
exit

interface GigabitEthernet0/0/0.20
 description GATEWAY_VLAN_20_TI
 encapsulation dot1Q 20
 ip address 192.168.20.1 255.255.255.0
exit
```


#### 🔍 Verificación:

```cisco
R1# show ip route
(Apareceran 192.168.10.0/24 y 192.168.20.0/24 como 'Connected').
```



## EJEMPLO 005: INTER-VLAN ROUTING EN SWITCH LAYER 3 MEDIANTE SVIs


> 🏢 **ESCENARIO REAL:**
En una empresa mediana, el enrutamiento mediante Router-on-a-Stick satura el cable
hacia el router. Se instala un Switch Multicapa (L3) para que conmute los paquetes
entre VLANs directamente en hardware (ASIC) a velocidad de varios Gigabits por segundo.


#### 🌐 DIAGRAMA:

```text
                 +-------------------------------+
                 |    SWITCH LAYER 3 (CORE_L3)   |
                 |   ip routing activado         |
                 |   SVI Vlan 10: 192.168.10.1   |
                 |   SVI Vlan 20: 192.168.20.1   |
                 +---------------+---------------+
                                 |
                 +---------------+---------------+
                 |                               |
                 v (VLAN 10)                     v (VLAN 20)
            [PC VENTAS]                     [PC FINANZAS]
           192.168.10.50                   192.168.20.50
```


#### 💻 CONFIGURACION CISCO IOS:

```cisco
! 1. Habilitar la funcion de enrutamiento IP en el switch
ip routing

! 2. Crear las VLANs en la base de datos
vlan 10
 name VENTAS
vlan 20
 name FINANZAS
exit

! 3. Crear las Interfaces Virtuales Conmutadas (SVIs)
interface Vlan10
 description GATEWAY_VLAN10
 ip address 192.168.10.1 255.255.255.0
 no shutdown
exit

interface Vlan20
 description GATEWAY_VLAN20
 ip address 192.168.20.1 255.255.255.0
 no shutdown
exit
```


#### 🔍 Verificación:

```cisco
CORE_L3# show ip route
(Verificar que ambas SVIs estan UP/UP y aparecen en la tabla de ruteo).
```



## EJEMPLO 006: PUERTO ENRUTADO DIRECTO (NO SWITCHPORT) EN SWITCH MULTICAPA


> 🏢 **ESCENARIO REAL:**
Conectar un Switch Core L3 con el Router de Salida a Internet sin usar VLANs.
Se convierte el puerto fisico del switch en un puerto de Capa 3 puro con direccion IP.


#### 🌐 DIAGRAMA:

```text
  +---------------+                              +---------------+
  |  SWITCH CORE  +------------------------------+  ROUTER BORDE |
  |     (L3)      |  Gi1/0/24          Gi0/0/1   |     (R1)      |
  +---------------+   10.0.0.1/30      10.0.0.2/30+---------------+
```


#### 💻 CONFIGURACION CISCO IOS:

```cisco
! En Switch Core:
interface GigabitEthernet1/0/24
 description ENLACE_PUNTO_A_PUNTO_HACIA_ROUTER
 no switchport                      ! Desactiva Capa 2 y activa Capa 3
 ip address 10.0.0.1 255.255.255.252
 no shutdown
exit

! En Router Borde:
interface GigabitEthernet0/0/1
 description ENLACE_HACIA_CORE_SWITCH
 ip address 10.0.0.2 255.255.255.252
 no shutdown
exit
```


#### 🔍 Verificación:

```cisco
CORE# ping 10.0.0.2
CORE# show interfaces GigabitEthernet1/0/24 | include is
```



## EJEMPLO 007: AGREGACION DE ENLACES CAPA 2 CON LACP (ETHERCHANNEL)


> 🏢 **ESCENARIO REAL:**
El enlace troncal de 1 Gbps entre el Switch de Distribucion y el Switch de Acceso
se satura en horas pico. Se agrupan dos cables fisicos (Gi0/1 y Gi0/2) en un canal
logico de 2 Gbps con tolerancia a fallas usando el protocolo estandar LACP (802.3ad).


#### 🌐 DIAGRAMA:

```text
  +-------------+    Gi0/1 (LACP)    +-------------+
  |             +====================+             |
  | SW_DISTRIB  |    Port-Channel 1  |  SW_ACCESO  |
  |             +====================+             |
  +-------------+    Gi0/2 (LACP)    +-------------+
                   (2 Gbps Agregado)
```


#### 💻 CONFIGURACION CISCO IOS (EN AMBOS SWITCHES):

```cisco
interface range GigabitEthernet0/1 - 2
 description MIEMBROS_ETHERCHANNEL_LACP
 channel-group 1 mode active       ! Modo 'active' activa LACP estandar
 no shutdown
exit

! La configuracion troncal se aplica DIRECTAMENTE en la interfaz Port-Channel logica:
interface Port-channel 1
 description TRONCAL_AGREGADO_HACIA_ACCESO
 switchport mode trunk
 switchport trunk allowed vlan 10,20,30
 no shutdown
exit
```


#### 🔍 Verificación:

```cisco
SW_DISTRIB# show etherchannel summary
(El estado debe mostrar flags 'SU': S = Layer2, U = In Use).
```



## EJEMPLO 008: ETHERCHANNEL LAYER 3 ENRUTADO ENTRE DOS SWITCHES CORE


> 🏢 **ESCENARIO REAL:**
Dos switches Core de Datacenter intercambian cientos de Megabytes de trafico inter-VLAN.
Se unen dos puertos enrutados (`no switchport`) para crear un enlace L3 redundante de 2 Gbps.


#### 🌐 DIAGRAMA:

```text
  +---------------+   Gi1/0/1 + Gi1/0/2   +---------------+
  |  CORE_SW_A    +=======================+  CORE_SW_B    |
  |               |    Port-Channel 10    |               |
  +---------------+      10.255.0.0/30    +---------------+
   10.255.0.1/30                           10.255.0.2/30
```


#### 💻 CONFIGURACION CISCO IOS:

```cisco
! En Core A:
interface range GigabitEthernet1/0/1 - 2
 no switchport
 channel-group 10 mode active
 no shutdown
exit
interface Port-channel 10
 description ENLACE_L3_CORE_HACIA_CORE_B
 no switchport
 ip address 10.255.0.1 255.255.255.252
 no shutdown
exit

! En Core B:
interface range GigabitEthernet1/0/1 - 2
 no switchport
 channel-group 10 mode active
 no shutdown
exit
interface Port-channel 10
 description ENLACE_L3_CORE_HACIA_CORE_A
 no switchport
 ip address 10.255.0.2 255.255.255.252
 no shutdown
exit
```


#### 🔍 Verificación:

```cisco
CORE_A# ping 10.255.0.2
CORE_A# show etherchannel summary
(Debe mostrar 'RU': R = Layer 3, U = In Use).
```



## EJEMPLO 009: SERVIDOR DHCP EN ROUTER CON POOLS POR VLAN Y EXCLUSIONES


> 🏢 **ESCENARIO REAL:**
En una sucursal sin servidor Windows Server dedicado, el router Cisco debe entregar
direcciones IP automaticamente a las PCs de Ventas (VLAN 10), reservando las primeras
10 IPs para impresoras y dispositivos de red fijos.


#### 🌐 DIAGRAMA:

```text
  [ROUTER R1 - SERVIDOR DHCP]
  Gateway: 192.168.10.1
  Pool: 192.168.10.0/24
  Excluidas: 192.168.10.1 a 192.168.10.10
              |
              v
     [SWITCH DE ACCESO] ----> [PCs reciben 192.168.10.11 en adelante]
```


#### 💻 CONFIGURACION CISCO IOS:

```cisco
! 1. Reservar las IPs estaticas para que DHCP no las entregue a las PCs
ip dhcp excluded-address 192.168.10.1 192.168.10.10

! 2. Crear el Pool DHCP
ip dhcp pool POOL_VENTAS
 network 192.168.10.0 255.255.255.0
 default-router 192.168.10.1
 dns-server 8.8.8.8 1.1.1.1
 domain-name empresa.local
 lease 8                    ! Concesion de 8 dias
exit
```


#### 🔍 Verificación:

```cisco
R1# show ip dhcp binding
(Muestra las direcciones MAC de los clientes que han tomado IP).
R1# show ip dhcp pool POOL_VENTAS
```



## EJEMPLO 010: AGENTE DHCP RELAY (IP HELPER-ADDRESS)


> 🏢 **ESCENARIO REAL:**
El servidor DHCP corporativo de Microsoft reside en el Datacenter (IP 10.0.0.100).
Como las peticiones DHCP Discover son paquetes Broadcast (`255.255.255.255`), los
routers las descartan por defecto. Se configura `ip helper-address` en el router
de la sucursal para convertir el broadcast en unicast y enviarlo al Datacenter.


#### 🌐 DIAGRAMA:

```text
  [SUCURSAL: PC Clientes]
  Peticion Broadcast DHCP Discover
              |
              v
  [ROUTER SUCURSAL (Gi0/0)] ---> Convierte Broadcast a Unicast ---> [DATACENTER]
  ip helper-address 10.0.0.100                                  Servidor DHCP: 10.0.0.100
```


#### 💻 CONFIGURACION CISCO IOS:

```cisco
interface GigabitEthernet0/0
 description LAN_USUARIOS_SUCURSAL
 ip address 192.168.50.1 255.255.255.0
 ! Reenviar solicitudes DHCP al servidor central en el Datacenter
 ip helper-address 10.0.0.100
 no shutdown
exit
```


#### 🔍 Verificación:

```cisco
R_SUCURSAL# show ip interface GigabitEthernet0/0 | include Helper
(Debe mostrar: Helper address is 10.0.0.100).
```



## EJEMPLO 011: RUTA ESTATICA DIRECTA PUNTO A PUNTO ENTRE DOS ROUTERS


> 🏢 **ESCENARIO REAL:**
Conectar la Sede Central (R1) con el Almacen Norte (R2) a traves de un enlace punto
a punto. Para que los usuarios de R1 alcancen la red del almacen, se agrega una
ruta estatica apuntando a la IP del router remoto.


#### 🌐 DIAGRAMA:

```text
  [LAN CENTRAL]                                             [LAN ALMACEN]
  192.168.1.0/24                                            192.168.2.0/24
        |                                                         |
     +--+--+                  Enlace WAN WAN                   +--+--+
     | R1  +---------------------------------------------------+ R2  |
     +-----+ Gi0/0/1: 10.0.0.1/30            Gi0/0/1: 10.0.0.2/30+-----+
```


#### 💻 CONFIGURACION CISCO IOS:

```cisco
! En R1 (Para llegar a la LAN de R2):
ip route 192.168.2.0 255.255.255.0 10.0.0.2

! En R2 (Para llegar a la LAN de R1):
ip route 192.168.1.0 255.255.255.0 10.0.0.1
```


#### 🔍 Verificación:

```cisco
R1# show ip route static
S    192.168.2.0/24 [1/0] via 10.0.0.2
R1# ping 192.168.2.1 source GigabitEthernet0/0/0
```



## EJEMPLO 012: RUTA POR DEFECTO (0.0.0.0/0) HACIA EL PROVEEDOR ISP


> 🏢 **ESCENARIO REAL:**
El router de frontera corporativo no necesita conocer las 950,000 rutas de Internet.
Simplemente envia cualquier paquete cuyo destino no este en la LAN interna hacia
la IP del Gateway proporcionado por el proveedor de Internet (ISP).


#### 🌐 DIAGRAMA:

```text
  [RED CORPORATIVA] ===> [ROUTER BORDE] -------------> [MODEM/ROUTER ISP] ===> INTERNET
   10.0.0.0/16           Gi0/0/1: 203.0.113.2          IP Gateway: 203.0.113.1
```


#### 💻 CONFIGURACION CISCO IOS:

```cisco
interface GigabitEthernet0/0/1
 description UPLINK_HACIA_ISP
 ip address 203.0.113.2 255.255.255.252
 no shutdown
exit

! Ruta por defecto (Gateway of Last Resort):
ip route 0.0.0.0 0.0.0.0 203.0.113.1
```


#### 🔍 Verificación:

```cisco
ROUTER# show ip route 0.0.0.0
Routing entry for 0.0.0.0/0, supernet
  Known via "static", distance 1, metric 0
  * 203.0.113.1
```



## EJEMPLO 013: RUTA ESTATICA FLOTANTE CON DISTANCIA ADMINISTRATIVA 10


> 🏢 **ESCENARIO REAL:**
Una empresa cuenta con un enlace principal de Fibra de 200 Mbps y un enlace de
respaldo por Microondas de 20 Mbps. La ruta flotante hacia la Microondas tiene una
Distancia Administrativa de 10 (mayor que el valor por defecto de 1), por lo que
permanece oculta y solo entra en accion si el cable de fibra se desconecta.


#### 🌐 DIAGRAMA:

```text
                        +---------------------------+
                        |  Fibra Primaria (AD = 1)  |
                     +--+  Next-Hop: 10.1.1.2       +--+
     +------------+  |  +---------------------------+  |  +------------+
     |  ROUTER A  +--+                                 +--+  ROUTER B  |
     +------------+  |  +---------------------------+  |  +------------+
                     +--+  Microondas (AD = 10)     +--+
                        |  Next-Hop: 10.2.2.2       |
                        +---------------------------+
```


#### 💻 CONFIGURACION CISCO IOS:

```cisco
! Ruta Primaria (AD = 1 por defecto):
ip route 172.16.0.0 255.255.0.0 10.1.1.2

! Ruta Flotante de Respaldo (AD = 10 explicitamente declarada al final):
ip route 172.16.0.0 255.255.0.0 10.2.2.2 10
```


#### 🔍 Verificación:

```cisco
ROUTER_A# show ip route 172.16.0.0
(Normalmente mostrara 10.1.1.2. Al apagar la interfaz primaria, mostrara 10.2.2.2).
```



## EJEMPLO 014: RUTA DE HOST (/32) HACIA UN SERVIDOR ESPECIFICO


> 🏢 **ESCENARIO REAL:**
Una sucursal remota accede a todos los servicios del Datacenter (`10.0.0.0/16`)
a traves de una WAN lenta. Sin embargo, el Servidor de Cobranzas (`10.0.50.25/32`)
requiere maxima velocidad y debe desviarse exclusivamente por una VPN directa dedicada.
Por la regla de "Prefijo mas largo" (Longest Prefix Match), la ruta /32 gana.


#### 🌐 DIAGRAMA:

```text
  [SUCURSAL] ---> Trafico general 10.0.0.0/16 ---------> [Enlace WAN Estandar]
              ---> Servidor Critico 10.0.50.25/32 ====> [Enlace VIP Dedicado]
```


#### 💻 CONFIGURACION CISCO IOS:

```cisco
! Ruta general para el bloque /16:
ip route 10.0.0.0 255.255.0.0 192.168.100.1

! Ruta de Host especifica para el servidor /32:
ip route 10.0.50.25 255.255.255.255 192.168.200.1
```


#### 🔍 Verificación:

```cisco
ROUTER# show ip route 10.0.50.25
Routing entry for 10.0.50.25/32
  Known via "static", distance 1, metric 0
  * 192.168.200.1 (Prefiere la ruta mas especifica)
```



## EJEMPLO 015: RUTA DE DESCARTE (NULL0 / BLACKHOLE)


> 🏢 **ESCENARIO REAL:**
Para evitar bucles de enrutamiento al sumarizar redes, y para mitigar ataques de
denegacion de servicio (DoS) dirigidos hacia IPs inutilizadas de un bloque publico,
se crea una ruta apuntando a la interfaz logica Null0 (el "triturador de paquetes").


#### 🌐 DIAGRAMA:

```text
  [PAQUETE HACIA IP INVALIDA] ===> [ROUTER] ===> Descarte en Hardware [Null0] (0% CPU)
```


#### 💻 CONFIGURACION CISCO IOS:

```cisco
! Descartar cualquier trafico dirigido hacia subredes no asignadas del bloque 10.10.0.0/16:
ip route 10.10.0.0 255.255.0.0 Null0 254
```


#### 🔍 Verificación:

```cisco
ROUTER# show ip route 10.10.0.0
Routing entry for 10.10.0.0/16
  Known via "static", distance 254, metric 0 (connected)
  * directly connected, via Null0
```



## EJEMPLO 016: RIPv2 BASICO ENTRE DOS ROUTERS SIN AUTO-SUMARIZACION


> 🏢 **ESCENARIO REAL:**
Conectar dos routers antiguos en una planta fabril utilizando RIPv2. Es indispensable
escribir `version 2` y `no auto-summary` para que el router envie las mascaras de
subred (VLSM) y no colapse las subredes en su mascara de clase tradicional A, B o C.


#### 🌐 DIAGRAMA:

```text
  [LAN PLANTA A]                                             [LAN PLANTA B]
  172.16.10.0/24                                             172.16.20.0/24
        |                                                          |
     +--+--+                   Enlace WAN                       +--+--+
     | R1  +----------------------------------------------------+ R2  |
     +-----+ Gi0/1: 10.0.0.1/30                 Gi0/1: 10.0.0.2/30+-----+
```


#### 💻 CONFIGURACION CISCO IOS:

```cisco
! En R1:
router rip
 version 2
 no auto-summary
 network 10.0.0.0
 network 172.16.0.0
exit

! En R2:
router rip
 version 2
 no auto-summary
 network 10.0.0.0
 network 172.16.0.0
exit
```


#### 🔍 Verificación:

```cisco
R1# show ip route rip
R    172.16.20.0/24 [120/1] via 10.0.0.2, GigabitEthernet0/1
```



## EJEMPLO 017: RIPv2 CON INTERFACES PASIVAS (PASSIVE-INTERFACE)


> 🏢 **ESCENARIO REAL:**
Por defecto, RIP envia paquetes broadcast/multicast cada 30 segundos por todos los
puertos. En la interfaz LAN donde estan las computadoras de los empleados, esto
satura los enlaces y permite que un atacante escuche la tabla o inyecte rutas falsas.
`passive-interface` desactiva el envio de actualizaciones hacia la LAN.


#### 🌐 DIAGRAMA:

```text
  [LAN USUARIOS] <--- NO enviar updates RIP (Seguridad) <--- [Gi0/0: PASSIVE]
                                                             [ROUTER R1]
  [ROUTER VECINO] <=== SI enviar updates RIP (Vecindad) <=== [Gi0/1: ACTIVA ]
```


#### 💻 CONFIGURACION CISCO IOS:

```cisco
router rip
 version 2
 no auto-summary
 network 192.168.1.0
 network 10.0.0.0
 passive-interface GigabitEthernet0/0   ! Puerto hacia los usuarios
exit
```


#### 🔍 Verificación:

```cisco
R1# show ip protocols | include Passive
(Debe listar GigabitEthernet0/0 como pasiva).
```



## EJEMPLO 018: INYECCION DE RUTA POR DEFECTO EN RIPv2


> 🏢 **ESCENARIO REAL:**
El Router Principal (R1) tiene salida a Internet. Para que los routers de las
sucursales secundarias (R2 y R3) sepan navegar sin tener que configurar una ruta
estatica en cada uno, R1 inyecta dinamicamente la ruta 0.0.0.0/0 dentro de RIP.


#### 🌐 DIAGRAMA:

```text
  INTERNET <=== [R1 (CENTRAL)] ====================> [R2 (SUCURSAL)]
                ip route 0.0.0.0 0.0.0.0 ISP        Aprende 0.0.0.0/0 via RIP
                default-information originate
```


#### 💻 CONFIGURACION CISCO IOS:

```cisco
! En Router Central (R1):
ip route 0.0.0.0 0.0.0.0 203.0.113.1   ! Ruta hacia el ISP
router rip
 version 2
 default-information originate         ! Inyectar la ruta por defecto a los vecinos
exit
```


#### 🔍 Verificación:

```cisco
R2# show ip route rip
R*   0.0.0.0/0 [120/1] via 10.0.0.1, GigabitEthernet0/1
```



## EJEMPLO 019: RIPv2 CON AUTENTICACION CRIPTOGRAFICA MD5


> 🏢 **ESCENARIO REAL:**
Proteger los enlaces WAN para que solo routers autorizados de la empresa puedan
intercambiar rutas RIP. Se configura una cadena de claves (Key-Chain) con cifrado MD5.


#### 🌐 DIAGRAMA:

```text
  +--------+              Paquetes RIP con Hash MD5              +--------+
  |   R1   +=====================================================+   R2   |
  +--------+         Key 1: "ClaveSecretaEmpresa2026"            +--------+
```


#### 💻 CONFIGURACION CISCO IOS (EN AMBOS ROUTERS):

```cisco
key chain CLAVE_RIP
 key 1
  key-string ClaveSecretaEmpresa2026
exit

interface GigabitEthernet0/1
 description ENLACE_WAN
 ip rip authentication mode md5
 ip rip authentication key-chain CLAVE_RIP
 no shutdown
exit
```


#### 🔍 Verificación:

```cisco
R1# debug ip rip
(Debe mostrar: 'RIP: received packet with MD5 authentication').
```



## EJEMPLO 020: SUMARIZACION MANUAL EN RIPv2 POR INTERFAZ WAN


> 🏢 **ESCENARIO REAL:**
Un router local administra 4 subredes contiguas (`192.168.0.0/24`, `192.168.1.0/24`,
`192.168.2.0/24`, `192.168.3.0/24`). Hacia el enlace WAN lento, en lugar de enviar
4 actualizaciones independientes, envia un unico supernet sumarizado `/22`.


#### 🌐 DIAGRAMA:

```text
  [LANs Internas]
  192.168.0.0/24
  192.168.1.0/24  ===> [ROUTER R1] === Anuncia solo 192.168.0.0/22 ===> [WAN LENTA]
  192.168.2.0/24
  192.168.3.0/24
```


#### 💻 CONFIGURACION CISCO IOS:

```cisco
interface GigabitEthernet0/1
 description ENLACE_WAN_HACIA_VECINO
 ip summary-address rip 192.168.0.0 255.255.252.0
exit
```


#### 🔍 Verificación:

```cisco
R2# show ip route rip
```


## R    192.168.0.0/22 [120/1] via 10.0.0.1, GigabitEthernet0/1
