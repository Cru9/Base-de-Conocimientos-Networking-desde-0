# 04. ENRUTAMIENTO INTER-VLAN, PUERTOS ENRUTADOS Y SERVIDOR DHCP

> **ARUBA NETWORKS (ARUBAOS-CX) - GUIA DE COMANDOS Y CONFIGURACION**


---



## 1. CONCEPTOS DE ENRUTAMIENTO EN ARUBAOS-CX

Los conmutadores ArubaOS-CX con capacidades de Capa 3 (modelos CX 6200, 6300,
6400, 8320, 8360, etc.) tienen el motor de reenvio de paquetes IPv4/IPv6 activo
por hardware.

El enrutamiento se puede realizar de dos formas:

### a) SVI (Switch Virtual Interface): Una IP en cada VLAN para actuar como gateway.


### b) Puertos Enrutados (Routed Ports): Un puerto fisico convertido en interfaz L3 pura

   mediante el comando 'routing', sin asignacion a ninguna tabla de VLAN.



## 2. CONFIGURACION DE ENRUTAMIENTO INTER-VLAN MEDIANTE SVIs

En este escenario, el switch es el Gateway predeterminado para todos los hosts
de cada una de las VLANs de la organizacion.

Paso 1: Crear las VLANs
```cisco
  SW-CORE-ARUBA-01(config)# vlan 10
  SW-CORE-ARUBA-01(config-vlan-10)# name Finanzas
  SW-CORE-ARUBA-01(config-vlan-10)# no shutdown

  SW-CORE-ARUBA-01(config)# vlan 20
  SW-CORE-ARUBA-01(config-vlan-20)# name Ingenieria
  SW-CORE-ARUBA-01(config-vlan-20)# no shutdown

Paso 2: Asignar direcciones IP a las interfaces virtuales (SVIs)
  SW-CORE-ARUBA-01(config)# interface vlan 10
  SW-CORE-ARUBA-01(config-if-vlan)# description Gateway_VLAN_Finanzas
  SW-CORE-ARUBA-01(config-if-vlan)# ip address 192.168.10.1/24
  SW-CORE-ARUBA-01(config-if-vlan)# no shutdown

  SW-CORE-ARUBA-01(config)# interface vlan 20
  SW-CORE-ARUBA-01(config-if-vlan)# description Gateway_VLAN_Ingenieria
  SW-CORE-ARUBA-01(config-if-vlan)# ip address 192.168.20.1/24
  SW-CORE-ARUBA-01(config-if-vlan)# no shutdown

En este punto, el trafico entre la VLAN 10 y la VLAN 20 se enruta de forma
automatica y a velocidad de cable (wire-speed).
```


## 3. CONFIGURACION DE PUERTOS ENRUTADOS (ROUTED PORTS L3)

Ideal para enlaces punto a punto hacia routers de frontera o firewalls:

```cisco
  SW-CORE-ARUBA-01(config)# interface 1/1/48
  SW-CORE-ARUBA-01(config-if)# description Enlace_Punto_A_Punto_Hacia_Firewall
  SW-CORE-ARUBA-01(config-if)# routing                   (convierte el puerto a L3)
  SW-CORE-ARUBA-01(config-if)# ip address 10.100.1.2/30
  SW-CORE-ARUBA-01(config-if)# no shutdown
```


## 4. AGENTE DE RETRANSMISION DHCP (DHCP RELAY / IP HELPER)

Cuando los clientes en sus respectivas VLANs necesitan solicitar direccion IP a
un servidor DHCP centralizado (ej. Windows Server, Infoblox o Linux):

```cisco
  SW-CORE-ARUBA-01(config)# interface vlan 10
  SW-CORE-ARUBA-01(config-if-vlan)# ip helper-address 192.168.1.100
  SW-CORE-ARUBA-01(config-if-vlan)# ip helper-address 192.168.1.101 (servidor secundario)

  SW-CORE-ARUBA-01(config)# interface vlan 20
  SW-CORE-ARUBA-01(config-if-vlan)# ip helper-address 192.168.1.100
```


## 5. CONFIGURACION DEL SERVIDOR DHCP LOCAL EN ARUBAOS-CX

AOS-CX permite hospedar pools de DHCP integrados directamente en el switch:


### a) Habilitar y definir el Pool para la VLAN 10:

```cisco
  SW-CORE-ARUBA-01(config)# dhcp-server
  SW-CORE-ARUBA-01(config-dhcp-server)# pool POOL_FINANZAS
  SW-CORE-ARUBA-01(config-dhcp-server-pool)# network 192.168.10.0/24
  SW-CORE-ARUBA-01(config-dhcp-server-pool)# range 192.168.10.50 192.168.10.200
  SW-CORE-ARUBA-01(config-dhcp-server-pool)# default-router 192.168.10.1
  SW-CORE-ARUBA-01(config-dhcp-server-pool)# dns-server 1.1.1.1 8.8.8.8
  SW-CORE-ARUBA-01(config-dhcp-server-pool)# domain-name empresa.local
  SW-CORE-ARUBA-01(config-dhcp-server-pool)# lease 08:00:00   (8 horas)
  SW-CORE-ARUBA-01(config-dhcp-server-pool)# exit

b) Activar el servicio DHCP en el switch:
  SW-CORE-ARUBA-01(config-dhcp-server)# enable
  SW-CORE-ARUBA-01(config-dhcp-server)# exit
```


## 6. RUTAS ESTATICAS Y RUTA POR DEFECTO (STATIC ROUTES)


### a) Ruta estatica hacia una red remota:

```cisco
  SW-CORE-ARUBA-01(config)# ip route 10.20.0.0/16 10.100.1.1

b) Ruta por defecto (Default Route / Gateway of Last Resort):
  SW-CORE-ARUBA-01(config)# ip route 0.0.0.0/0 10.100.1.1

c) Ruta flotante de respaldo (con distancia administrativa mayor, ej. 200):
  SW-CORE-ARUBA-01(config)# ip route 0.0.0.0/0 10.200.1.1 200
```


## 7. COMANDOS DE VERIFICACION Y PRUEBAS

Visualizar la tabla de enrutamiento IPv4:
```cisco
  SW-CORE-ARUBA-01# show ip route

Visualizar solo rutas estaticas o conectadas:
  SW-CORE-ARUBA-01# show ip route static
  SW-CORE-ARUBA-01# show ip route connected

Visualizar concesiones (leases) activas del servidor DHCP:
  SW-CORE-ARUBA-01# show dhcp-server leases

Visualizar estado y estadisticas del servidor DHCP:
  SW-CORE-ARUBA-01# show dhcp-server

Probar conectividad desde una interfaz o VLAN de origen:
  SW-CORE-ARUBA-01# ping 192.168.10.50
```


## SW-CORE-ARUBA-01# traceroute 192.168.20.50
