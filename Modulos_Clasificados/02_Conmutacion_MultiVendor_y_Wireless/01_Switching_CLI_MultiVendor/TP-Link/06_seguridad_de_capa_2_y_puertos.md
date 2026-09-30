# 06. SEGURIDAD DE CAPA 2 (PORT SECURITY, DHCP SNOOPING, DAI, STORM CONTROL)

> **TP-LINK (JETSTREAM SWITCHES) - GUIA DE COMANDOS Y CONFIGURACION**


---



## 1. SEGURIDAD DE PUERTO (PORT SECURITY)

Port Security restringe el acceso al puerto permitiendo unicamente una cantidad
determinada de direcciones MAC aprendidas o estaticas.


### a) Habilitar en un puerto de usuario limitando a 1 direccion MAC:

```cisco
  SW-DISTRIB-TPLINK-01(config)# interface gigabitEthernet 1/0/5
  SW-DISTRIB-TPLINK-01(config-if)# switchport mode access
  SW-DISTRIB-TPLINK-01(config-if)# switchport port-security
  SW-DISTRIB-TPLINK-01(config-if)# switchport port-security maximum 1
  SW-DISTRIB-TPLINK-01(config-if)# switchport port-security mac-address sticky
  SW-DISTRIB-TPLINK-01(config-if)# switchport port-security violation shutdown
  SW-DISTRIB-TPLINK-01(config-if)# exit

Opciones de accion de violacion:
- shutdown: Deshabilita el puerto completamente (err-disabled) al detectar una MAC no autorizada.
- restrict: Descarta los paquetes de la MAC no autorizada y genera un registro de alerta en el log.
- protect: Descarta los paquetes silenciosamente sin generar registro.
```


## 2. DHCP SNOOPING (PROTECCION CONTRA SERVIDORES DHCP NO AUTORIZADOS)

Evita ataques donde un dispositivo pirata o un router casero entrega direcciones
IP erroneas y puertas de enlace fraudulentas.
- Puertos Confiables (Trusted): Conectan al servidor DHCP oficial o enlaces troncales.
- Puertos No Confiables (Untrusted): Todos los puertos de acceso de computadoras.


### a) Activar DHCP Snooping globalmente y en las VLANs requeridas:

```cisco
  SW-DISTRIB-TPLINK-01(config)# ip dhcp snooping
  SW-DISTRIB-TPLINK-01(config)# ip dhcp snooping vlan 10,20,30

b) Configurar el puerto troncal / uplink como confiable:
  SW-DISTRIB-TPLINK-01(config)# interface gigabitEthernet 1/0/24
  SW-DISTRIB-TPLINK-01(config-if)# ip dhcp snooping trust
  SW-DISTRIB-TPLINK-01(config-if)# exit
```


## 3. DYNAMIC ARP INSPECTION (DAI - INSPECCION DINAMICA DE ARP)

Protege la red local contra ataques de intermediario (Man-in-the-Middle) e
intoxicacion de tablas ARP (ARP Spoofing / Poisoning). DAI valida los paquetes ARP
contra la base de datos de DHCP Snooping.


### a) Habilitar DAI en las VLANs correspondientes:

```cisco
  SW-DISTRIB-TPLINK-01(config)# ip arp inspection vlan 10,20,30

b) Configurar el puerto de uplink como confiable para trafico ARP:
  SW-DISTRIB-TPLINK-01(config)# interface gigabitEthernet 1/0/24
  SW-DISTRIB-TPLINK-01(config-if)# ip arp inspection trust
  SW-DISTRIB-TPLINK-01(config-if)# exit
```


## 4. CONTROL DE TORMENTAS DE TRAFICO (STORM CONTROL)

Evita que tormentas de difusion colapsen el procesador del switch y saturen los
enlaces de los usuarios.

Configurar en el rango de puertos de acceso (ejemplo limitando a 5% del ancho de banda):
```cisco
  SW-DISTRIB-TPLINK-01(config)# interface range gigabitEthernet 1/0/1-20
  SW-DISTRIB-TPLINK-01(config-if-range)# storm-control broadcast level 5
  SW-DISTRIB-TPLINK-01(config-if-range)# storm-control multicast level 5
  SW-DISTRIB-TPLINK-01(config-if-range)# storm-control unicast level 5
  SW-DISTRIB-TPLINK-01(config-if-range)# exit
```


## 5. DETECCION DE BUCLES (LOOPBACK DETECTION - LBD)

Detecta rapidamente si un usuario conecta ambos extremos de un cable de red en dos
rosetas o a traves de un hub o switch no administrado:


### a) Habilitar globalmente:

```cisco
  SW-DISTRIB-TPLINK-01(config)# loopback-detection enable
  SW-DISTRIB-TPLINK-01(config)# loopback-detection interval 5

b) Habilitar en los puertos de usuario:
  SW-DISTRIB-TPLINK-01(config)# interface range gigabitEthernet 1/0/1-20
  SW-DISTRIB-TPLINK-01(config-if-range)# loopback-detection
  SW-DISTRIB-TPLINK-01(config-if-range)# exit
```


## 6. VERIFICACION Y COMANDOS DE DIAGNOSTICO

Visualizar estado de Port Security y direcciones aprendidas:
```cisco
  SW-DISTRIB-TPLINK-01# show port-security
  SW-DISTRIB-TPLINK-01# show port-security interface gigabitEthernet 1/0/5
  SW-DISTRIB-TPLINK-01# show port-security address

Visualizar estado de DHCP Snooping y puertos confiables:
  SW-DISTRIB-TPLINK-01# show ip dhcp snooping

Visualizar la base de datos de enlaces IP-MAC aprendidos (Snooping Binding Table):
  SW-DISTRIB-TPLINK-01# show ip dhcp snooping binding

Visualizar estado y estadisticas de Dynamic ARP Inspection:
  SW-DISTRIB-TPLINK-01# show ip arp inspection

Visualizar parametros configurados de Storm Control:
```


## SW-DISTRIB-TPLINK-01# show storm-control
