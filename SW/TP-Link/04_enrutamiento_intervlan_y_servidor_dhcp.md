# 04. ENRUTAMIENTO INTER-VLAN, SERVIDOR DHCP Y RUTAS ESTATICAS

> **TP-LINK (JETSTREAM SWITCHES) - GUIA DE COMANDOS Y CONFIGURACION**


---



## 1. HABILITACION DE ENRUTAMIENTO IP (MODELOS L2+ / L3)

Los modelos JetStream de Capa 2+ y Capa 3 (series SG3428, SG3452, SX3008F, SX3016F,
etc.) disponen de enrutamiento IPv4/IPv6 por hardware.

Para activar el reenvio de paquetes entre diferentes VLANs:
```cisco
  SW-CORE-TPLINK(config)# ip routing
```


## 2. ENRUTAMIENTO INTER-VLAN MEDIANTE SVIs (INTERFACES VIRTUALES)

Configurar el switch como Gateway por defecto para cada departamento de la red.

Paso 1: Crear las VLANs
```cisco
  SW-CORE-TPLINK(config)# vlan 10
  SW-CORE-TPLINK(config-vlan)# name Contabilidad
  SW-CORE-TPLINK(config-vlan)# exit

  SW-CORE-TPLINK(config)# vlan 20
  SW-CORE-TPLINK(config-vlan)# name Operaciones
  SW-CORE-TPLINK(config-vlan)# exit

Paso 2: Asignar direcciones IP a las interfaces virtuales (SVIs)
  SW-CORE-TPLINK(config)# interface vlan 10
  SW-CORE-TPLINK(config-if)# ip address 192.168.10.1 255.255.255.0
  SW-CORE-TPLINK(config-if)# no shutdown
  SW-CORE-TPLINK(config-if)# exit

  SW-CORE-TPLINK(config)# interface vlan 20
  SW-CORE-TPLINK(config-if)# ip address 192.168.20.1 255.255.255.0
  SW-CORE-TPLINK(config-if)# no shutdown
  SW-CORE-TPLINK(config-if)# exit

A partir de este momento, los dispositivos de la VLAN 10 pueden comunicarse con
los de la VLAN 20 a traves del switch a velocidad de cable (wire-speed).
```


## 3. CONFIGURACION DEL SERVIDOR DHCP LOCAL INTEGRADO

El switch puede asignar dinamicamente direcciones IP a los hosts conectados:


### a) Activar el servicio DHCP global:

```cisco
  SW-CORE-TPLINK(config)# service dhcp

b) Excluir direcciones estaticas reservadas (gateways, servidores, impresoras):
  SW-CORE-TPLINK(config)# ip dhcp excluded-address 192.168.20.1 192.168.20.20

c) Crear y configurar el pool de direcciones para la VLAN 20:
  SW-CORE-TPLINK(config)# ip dhcp pool POOL_OPERACIONES
  SW-CORE-TPLINK(config-dhcp-pool)# network 192.168.20.0 255.255.255.0
  SW-CORE-TPLINK(config-dhcp-pool)# default-router 192.168.20.1
  SW-CORE-TPLINK(config-dhcp-pool)# dns-server 1.1.1.1 8.8.8.8
  SW-CORE-TPLINK(config-dhcp-pool)# lease 0 8 0   (0 dias, 8 horas, 0 minutos)
  SW-CORE-TPLINK(config-dhcp-pool)# exit
```


## 4. AGENTE DE RETRANSMISION DHCP (DHCP RELAY)

Cuando se utiliza un servidor DHCP externo centralizado (ej. Windows Server):


### a) Habilitar el servicio DHCP Relay:

```cisco
  SW-CORE-TPLINK(config)# service dhcp-relay

b) Configurar la IP del servidor DHCP externo en la interfaz de la VLAN cliente:
  SW-CORE-TPLINK(config)# interface vlan 10
  SW-CORE-TPLINK(config-if)# ip dhcp-relay server-address 192.168.1.100
  SW-CORE-TPLINK(config-if)# exit
```


## 5. RUTAS ESTATICAS Y RUTA POR DEFECTO (DEFAULT ROUTE)


### a) Ruta estatica hacia una red remota:

```cisco
  SW-CORE-TPLINK(config)# ip route 10.50.0.0 255.255.0.0 10.100.1.2

b) Ruta por defecto (hacia el Firewall perimetral o Router de Internet):
  SW-CORE-TPLINK(config)# ip route 0.0.0.0 0.0.0.0 10.100.1.1
```


## 6. VERIFICACION Y COMANDOS DE DIAGNOSTICO

Visualizar la tabla de enrutamiento IPv4 completa:
```cisco
  SW-CORE-TPLINK# show ip route

Visualizar el estado de los pools DHCP locales:
  SW-CORE-TPLINK# show ip dhcp server pool

Visualizar las concesiones (leases) y clientes activos con IP asignada:
  SW-CORE-TPLINK# show ip dhcp server binding

Probar conectividad de red con Ping o Traceroute:
  SW-CORE-TPLINK# ping 192.168.10.1
```


## SW-CORE-TPLINK# traceroute 192.168.20.50
