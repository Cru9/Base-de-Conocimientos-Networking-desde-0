# 03. GESTION DE VLANS, ASIGNACION DE PUERTOS Y DIRECCIONAMIENTO IP

> **ARUBA NETWORKS (ARUBAOS-CX) - GUIA DE COMANDOS Y CONFIGURACION**


---



## 1. CREACION Y ADMINISTRACION DE VLANS

En ArubaOS-CX, las VLANs se definen globalmente y se les puede asignar un nombre
descriptivo.

Creacion individual de VLAN:
```cisco
  SW-CORE-ARUBA-01(config)# vlan 10
  SW-CORE-ARUBA-01(config-vlan-10)# name Datos_Usuarios
  SW-CORE-ARUBA-01(config-vlan-10)# no shutdown

  SW-CORE-ARUBA-01(config)# vlan 20
  SW-CORE-ARUBA-01(config-vlan-20)# name Telefonia_IP
  SW-CORE-ARUBA-01(config-vlan-20)# no shutdown

  SW-CORE-ARUBA-01(config)# vlan 99
  SW-CORE-ARUBA-01(config-vlan-99)# name Gestion_Administracion
  SW-CORE-ARUBA-01(config-vlan-99)# no shutdown

Creacion de multiples VLANs simultaneas:
  SW-CORE-ARUBA-01(config)# vlan 30,40,50,60-65
```


## 2. CONFIGURACION DE PUERTOS DE ACCESO (ACCESS PORTS)

Un puerto de acceso conecta un dispositivo final (PC, impresora, servidor sin
etiquetar) y pertenece a una unica VLAN de forma nativa/untagged.


### a) Asignar un solo puerto:

```cisco
  SW-CORE-ARUBA-01(config)# interface 1/1/5
  SW-CORE-ARUBA-01(config-if)# description PC_Contabilidad
  SW-CORE-ARUBA-01(config-if)# no routing       (asegura modo Layer 2)
  SW-CORE-ARUBA-01(config-if)# vlan access 10
  SW-CORE-ARUBA-01(config-if)# no shutdown

b) Asignar un rango de puertos a una VLAN:
  SW-CORE-ARUBA-01(config)# interface 1/1/1-1/1/20
  SW-CORE-ARUBA-01(config-if<1/1/1-1/1/20>)# vlan access 10
  SW-CORE-ARUBA-01(config-if<1/1/1-1/1/20>)# no shutdown
```


## 3. CONFIGURACION DE PUERTOS TRONCALES (TRUNK 802.1Q)

Los enlaces troncales transportan trafico de multiples VLANs etiquetadas (tagged)
hacia otros switches, firewalls, routers o hipervisores (VMware ESXi, Proxmox).


### a) Troncal permitiendo VLANs especificas (Buena practica de seguridad):

```cisco
  SW-CORE-ARUBA-01(config)# interface 1/1/49
  SW-CORE-ARUBA-01(config-if)# description Uplink_Hacia_Switch_Distribucion
  SW-CORE-ARUBA-01(config-if)# no routing
  SW-CORE-ARUBA-01(config-if)# vlan trunk native 1
  SW-CORE-ARUBA-01(config-if)# vlan trunk allowed 10,20,99
  SW-CORE-ARUBA-01(config-if)# no shutdown

b) Permitir todas las VLANs existentes en el troncal:
  SW-CORE-ARUBA-01(config-if)# vlan trunk allowed all

c) Cambiar la VLAN nativa (sin etiquetar) y etiquetarla por seguridad:
  SW-CORE-ARUBA-01(config-if)# vlan trunk native 99
  SW-CORE-ARUBA-01(config-if)# vlan trunk native 99 tag   (fuerza 802.1Q en nativa)
```


## 4. CONFIGURACION DE PUERTOS PARA TELEFONIA IP (VOICE VLAN Y LLDP-MED)

Permite conectar una computadora a traves de un telefono IP en el mismo cable:
- Los datos de la PC van sin etiquetar (VLAN de acceso).
- La voz del telefono se etiqueta mediante negociacion automatica LLDP-MED.

```cisco
  SW-CORE-ARUBA-01(config)# interface 1/1/10
  SW-CORE-ARUBA-01(config-if)# description Escritorio_Telefono_y_PC
  SW-CORE-ARUBA-01(config-if)# vlan access 10          (Trafico de datos de la PC)
  SW-CORE-ARUBA-01(config-if)# vlan voice 20           (Trafico de VoIP)
  SW-CORE-ARUBA-01(config-if)# lldp med enable         (Informa al telefono la VLAN de voz)
```


## 5. INTERFACES VIRTUALES DE SWITCH (SVI - VLAN L3 / IP DE GESTION)

Para administrar el switch remotamente o para permitir enrutamiento local:


### a) Crear la interfaz SVI de gestion:

```cisco
  SW-CORE-ARUBA-01(config)# interface vlan 99
  SW-CORE-ARUBA-01(config-if-vlan)# description SVI_Gestion_Switch
  SW-CORE-ARUBA-01(config-if-vlan)# ip address 192.168.99.10/24
  SW-CORE-ARUBA-01(config-if-vlan)# no shutdown
  SW-CORE-ARUBA-01(config-if-vlan)# exit

b) Configurar Gateway por Defecto (Default Gateway):
  En switches de Capa 2 (o Capa 3 que requieran salida a internet/gestion):
  SW-CORE-ARUBA-01(config)# ip route 0.0.0.0/0 192.168.99.1
```


## 6. VERIFICACION Y DIAGNOSTICO DE VLANS

Visualizar todas las VLANs y puertos asociados:
```cisco
  SW-CORE-ARUBA-01# show vlan

Visualizar resumen conciso de VLANs:
  SW-CORE-ARUBA-01# show vlan summary

Visualizar configuracion detallada de una VLAN especifica:
  SW-CORE-ARUBA-01# show vlan 10

Visualizar a que VLANs pertenece un puerto fisico especifico:
  SW-CORE-ARUBA-01# show vlan port 1/1/49

Visualizar resumen de todas las interfaces IP (SVI y puertos L3):
  SW-CORE-ARUBA-01# show ip interface brief

Visualizar tabla de direcciones MAC aprendidas en una VLAN:
```


## SW-CORE-ARUBA-01# show mac-address vlan 10
