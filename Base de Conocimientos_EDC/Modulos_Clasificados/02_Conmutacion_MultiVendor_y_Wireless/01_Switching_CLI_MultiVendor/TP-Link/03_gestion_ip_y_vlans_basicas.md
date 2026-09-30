# 03. GESTION DE VLANS, ASIGNACION DE PUERTOS Y DIRECCIONAMIENTO IP

> **TP-LINK (JETSTREAM SWITCHES) - GUIA DE COMANDOS Y CONFIGURACION**


---



## 1. CREACION Y ADMINISTRACION DE VLANS (802.1Q)

Las VLANs permiten segmentar la red en dominios de difusion independientes para
mejorar la seguridad y el rendimiento del tráfico.


### a) Crear VLANs individualmente y asignar nombres:

```cisco
  SW-DISTRIB-TPLINK-01(config)# vlan 10
  SW-DISTRIB-TPLINK-01(config-vlan)# name Administracion
  SW-DISTRIB-TPLINK-01(config-vlan)# exit

  SW-DISTRIB-TPLINK-01(config)# vlan 20
  SW-DISTRIB-TPLINK-01(config-vlan)# name Empleados
  SW-DISTRIB-TPLINK-01(config-vlan)# exit

  SW-DISTRIB-TPLINK-01(config)# vlan 30
  SW-DISTRIB-TPLINK-01(config-vlan)# name Telefonia_VoIP
  SW-DISTRIB-TPLINK-01(config-vlan)# exit

b) Crear multiples VLANs simultaneas:
  SW-DISTRIB-TPLINK-01(config)# vlan 40,50,60-65
```


## 2. MODOS DE PUERTO EN CONMUTADORES TP-LINK JETSTREAM

TP-Link soporta tres modos de puerto:
- Access: Conecta terminales (PC, impresoras, servidores simples). Trafico sin etiqueta (untagged).
- Trunk: Conecta a otros switches o routers. Transporta multiples VLANs etiquetadas (tagged).
- General: Modo hibrido avanzado que permite combinaciones complejas de VLANs tagged y untagged.



## 3. CONFIGURACION DE PUERTOS DE ACCESO (ACCESS)

Asignar un puerto de acceso a la VLAN 20:

```cisco
  SW-DISTRIB-TPLINK-01(config)# interface gigabitEthernet 1/0/5
  SW-DISTRIB-TPLINK-01(config-if)# description PC_Empleado_Piso_1
  SW-DISTRIB-TPLINK-01(config-if)# switchport mode access
  SW-DISTRIB-TPLINK-01(config-if)# switchport access vlan 20
  SW-DISTRIB-TPLINK-01(config-if)# no shutdown

Configurar un rango de puertos en la misma VLAN de acceso:
  SW-DISTRIB-TPLINK-01(config)# interface range gigabitEthernet 1/0/1-20
  SW-DISTRIB-TPLINK-01(config-if-range)# switchport mode access
  SW-DISTRIB-TPLINK-01(config-if-range)# switchport access vlan 20
  SW-DISTRIB-TPLINK-01(config-if-range)# no shutdown
```


## 4. CONFIGURACION DE PUERTOS TRONCALES (TRUNK)

Configurar el puerto 1/0/24 como troncal hacia otro switch:

```cisco
  SW-DISTRIB-TPLINK-01(config)# interface gigabitEthernet 1/0/24
  SW-DISTRIB-TPLINK-01(config-if)# description UPLINK_HACIA_CORE
  SW-DISTRIB-TPLINK-01(config-if)# switchport mode trunk
  SW-DISTRIB-TPLINK-01(config-if)# switchport trunk allowed vlan 10,20,30
  (O permitir todas las VLANs: switchport trunk allowed vlan all)

Cambiar la VLAN Nativa (la VLAN que viaja sin etiqueta en el troncal):
  SW-DISTRIB-TPLINK-01(config-if)# switchport trunk native vlan 10
```


## 5. MODO GENERAL (HIBRIDO - UTIL PARA SERVIDORES Y ACCESS POINTS)

El modo 'General' permite definir con maxima granularidad el PVID (VLAN sin etiqueta
al ingresar) y que VLANs salen etiquetadas o sin etiquetar:

```cisco
  SW-DISTRIB-TPLINK-01(config)# interface gigabitEthernet 1/0/22
  SW-DISTRIB-TPLINK-01(config-if)# description AP_Wi-Fi_Corporativo
  SW-DISTRIB-TPLINK-01(config-if)# switchport mode general
  SW-DISTRIB-TPLINK-01(config-if)# switchport general pvid 10
  SW-DISTRIB-TPLINK-01(config-if)# switchport general allowed vlan 10 untagged
  SW-DISTRIB-TPLINK-01(config-if)# switchport general allowed vlan 20,30 tagged
  SW-DISTRIB-TPLINK-01(config-if)# no shutdown
```


## 6. INTERFAZ DE GESTION Y DIRECCIONAMIENTO IP (SVI)

Para poder administrar el switch de forma remota via SSH o Web GUI:


### a) Configurar direccion IP en la VLAN de administracion (SVI):

```cisco
  SW-DISTRIB-TPLINK-01(config)# interface vlan 10
  SW-DISTRIB-TPLINK-01(config-if)# ip address 192.168.10.15 255.255.255.0
  SW-DISTRIB-TPLINK-01(config-if)# no shutdown
  SW-DISTRIB-TPLINK-01(config-if)# exit

b) Configurar la Puerta de Enlace Predeterminada (Default Gateway):
  SW-DISTRIB-TPLINK-01(config)# ip default-gateway 192.168.10.1
  (O en switches L2+/L3: ip route 0.0.0.0 0.0.0.0 192.168.10.1)
```


## 7. VERIFICACION Y COMANDOS DE DIAGNOSTICO

Visualizar la tabla completa de VLANs y puertos miembros:
```cisco
  SW-DISTRIB-TPLINK-01# show vlan

Visualizar informacion de una VLAN especifica:
  SW-DISTRIB-TPLINK-01# show vlan id 10

Visualizar el modo y configuracion de un puerto (Access / Trunk / General):
  SW-DISTRIB-TPLINK-01# show interface switchport gigabitEthernet 1/0/24

Visualizar las interfaces IP configuradas y su estado operacional:
  SW-DISTRIB-TPLINK-01# show ip interface

Visualizar las direcciones MAC aprendidas en una VLAN:
```


## SW-DISTRIB-TPLINK-01# show mac address-table vlan 10
