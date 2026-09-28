# 05. AGREGACION DE ENLACES (LAG / LACP) Y SPANNING TREE PROTOCOL (STP)

> **ARUBA NETWORKS (ARUBAOS-CX) - GUIA DE COMANDOS Y CONFIGURACION**


---



## 1. AGREGACION DE ENLACES (LAG - LINK AGGREGATION GROUP)

Un LAG agrupa multiples enlaces fisicos en un unico enlace logico de mayor ancho
de banda y redundancia ante caidas de fibra o cable.

En ArubaOS-CX, se crea primero la interfaz logica 'interface lag <id>' y luego
se asignan los puertos fisicos a dicho LAG.

Tipos de LAG:
- Dinamico LACP (802.3ad): El mas recomendado, negocia activamente el estado de los enlaces.
- Estatico: Sin negociacion de paquetes LACP.



## 2. CONFIGURACION DE UN LAG DINAMICO CON LACP (PASO A PASO)

Escenario: Agrupar los puertos 1/1/47 y 1/1/48 en el LAG 1 como troncal hacia otro switch.

Paso 1: Crear y configurar la interfaz logica LAG
```cisco
  SW-CORE-ARUBA-01(config)# interface lag 1
  SW-CORE-ARUBA-01(config-lag-if)# description UPLINK_LACP_HACIA_DISTRIB
  SW-CORE-ARUBA-01(config-lag-if)# no routing
  SW-CORE-ARUBA-01(config-lag-if)# vlan trunk native 1
  SW-CORE-ARUBA-01(config-lag-if)# vlan trunk allowed 10,20,30,99
  SW-CORE-ARUBA-01(config-lag-if)# lacp mode active     (inicia negociacion LACP)
  SW-CORE-ARUBA-01(config-lag-if)# no shutdown
  SW-CORE-ARUBA-01(config-lag-if)# exit

Paso 2: Asignar los puertos fisicos al LAG
  SW-CORE-ARUBA-01(config)# interface 1/1/47
  SW-CORE-ARUBA-01(config-if)# description Miembro_LAG_1_Fibra_A
  SW-CORE-ARUBA-01(config-if)# no routing
  SW-CORE-ARUBA-01(config-if)# lag 1
  SW-CORE-ARUBA-01(config-if)# no shutdown

  SW-CORE-ARUBA-01(config)# interface 1/1/48
  SW-CORE-ARUBA-01(config-if)# description Miembro_LAG_1_Fibra_B
  SW-CORE-ARUBA-01(config-if)# no routing
  SW-CORE-ARUBA-01(config-if)# lag 1
  SW-CORE-ARUBA-01(config-if)# no shutdown

Nota: Al asignar un puerto a un LAG, el puerto hereda automaticamente la
configuracion de VLANs y politicas de la interfaz LAG.
```


## 3. PROTOCOLOS DE ARBOL DE EXPANSION (SPANNING TREE - STP)

Evita bucles de Capa 2 en topologias redundantes bloqueando enlaces alternos.

Modos soportados en ArubaOS-CX:
- RSTP (Rapid Spanning Tree - 802.1w): Predeterminado y recomendado para redes estandar.
- MSTP (Multiple Spanning Tree - 802.1s): Optimiza instancias para grupos de VLANs.
- RPVST+ (Rapid Per-VLAN Spanning Tree): Una instancia de RSTP por cada VLAN (compatible con Cisco).



## 4. CONFIGURACION DE RSTP / RPVST Y SELECCION DE SWITCH RAIZ (ROOT BRIDGE)


### a) Habilitar Spanning Tree globalmente en modo RSTP:

```cisco
  SW-CORE-ARUBA-01(config)# spanning-tree mode rstp
  SW-CORE-ARUBA-01(config)# spanning-tree

b) Forzar al switch a ser el Switch Raiz (Root Bridge):
  La prioridad debe ser menor que la de los demas switches (en pasos de 4096):
  SW-CORE-ARUBA-01(config)# spanning-tree priority 0        (Raiz Primario)
  (o prioridad 4096 para Raiz Secundario de respaldo).

c) Modo RPVST+ (Por VLAN):
  SW-CORE-ARUBA-01(config)# spanning-tree mode rpvst
  SW-CORE-ARUBA-01(config)# spanning-tree vlan 10,20 priority 4096
```


## 5. PROTECCION Y OPTIMIZACION DE PUERTOS STP


### a) Admin-Edge (Equivalente a PortFast de Cisco):

  Pasa inmediatamente a estado 'Forwarding' (envio) omitiendo etapas Listening/Learning:
```cisco
  SW-CORE-ARUBA-01(config)# interface 1/1/1-1/1/24
  SW-CORE-ARUBA-01(config-if<1/1/1-1/1/24>)# spanning-tree port-type admin-edge

b) BPDU Guard:
  Si un puerto de acceso recibe una BPDU (ej. un usuario conecta un switch casero),
  el puerto se deshabilita de inmediato para proteger la red:
  - Habilitacion global para todos los puertos edge:
    SW-CORE-ARUBA-01(config)# spanning-tree bpdu-guard
  - Habilitacion por interfaz individual:
    SW-CORE-ARUBA-01(config-if)# spanning-tree bpdu-guard enable

c) Root Guard:
  Evita que un switch no autorizado conectado a este puerto se convierta en Root Bridge:
  SW-CORE-ARUBA-01(config-if)# spanning-tree root-guard
```


## 6. VERIFICACION Y COMANDOS DE DIAGNOSTICO

Visualizar estado de los grupos LAG y miembros:
```cisco
  SW-CORE-ARUBA-01# show lag brief
  SW-CORE-ARUBA-01# show lag 1

Visualizar estado detallado de negociacion LACP y tasas de paquetes:
  SW-CORE-ARUBA-01# show lacp interfaces

Visualizar estado global de Spanning Tree y puente raiz:
  SW-CORE-ARUBA-01# show spanning-tree

Visualizar el rol y estado de cada puerto en el arbol (Root, Designated, Alternate, Blocking):
  SW-CORE-ARUBA-01# show spanning-tree brief

Visualizar detalles de protecciones y violaciones BPDU:
```


## SW-CORE-ARUBA-01# show spanning-tree detail
