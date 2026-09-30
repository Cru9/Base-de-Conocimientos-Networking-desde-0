# 05. AGREGACION DE ENLACES (LAG / LACP) Y SPANNING TREE PROTOCOL (STP)

> **TP-LINK (JETSTREAM SWITCHES) - GUIA DE COMANDOS Y CONFIGURACION**


---



## 1. AGREGACION DE ENLACES (LAG - LINK AGGREGATION GROUP / PORT-CHANNEL)

La agregacion de enlaces permite combinar varios puertos fisicos en un solo enlace
logico para aumentar el ancho de banda y proporcionar tolerancia a fallos.

Modos soportados en TP-Link:
- LACP Dinamico (802.3ad): Modo 'active' o 'passive' (recomendado para negociacion segura).
- Estatico: Modo 'on' (sin negociacion de paquetes LACP).



## 2. CONFIGURACION DE UN PORT-CHANNEL LACP DINAMICO

Escenario: Agrupar los puertos 1/0/23 y 1/0/24 en el Port-Channel 1 para enlace
troncal redundante hacia otro switch.

Paso 1: Asignar los puertos fisicos al grupo con modo LACP activo
```cisco
  SW-CORE-TPLINK(config)# interface gigabitEthernet 1/0/23
  SW-CORE-TPLINK(config-if)# description Miembro_LAG_1_A
  SW-CORE-TPLINK(config-if)# channel-group 1 mode active
  SW-CORE-TPLINK(config-if)# exit

  SW-CORE-TPLINK(config)# interface gigabitEthernet 1/0/24
  SW-CORE-TPLINK(config-if)# description Miembro_LAG_1_B
  SW-CORE-TPLINK(config-if)# channel-group 1 mode active
  SW-CORE-TPLINK(config-if)# exit

Paso 2: Configurar la interfaz logica Port-Channel resultante
  SW-CORE-TPLINK(config)# interface port-channel 1
  SW-CORE-TPLINK(config-if)# description UPLINK_LACP_TRUNK
  SW-CORE-TPLINK(config-if)# switchport mode trunk
  SW-CORE-TPLINK(config-if)# switchport trunk allowed vlan 10,20,30
  SW-CORE-TPLINK(config-if)# no shutdown
  SW-CORE-TPLINK(config-if)# exit

Algoritmo de balanceo de carga (Hashing):
  SW-CORE-TPLINK(config)# port-channel load-balance src-dst-mac
  (O balanceo por IP: port-channel load-balance src-dst-ip)
```


## 3. PROTOCOLOS DE ARBOL DE EXPANSION (SPANNING TREE - STP)

Evita la formacion de tormentas de difusion (bucles de Capa 2) en topologias con
cables redundantes.

Modos soportados en JetStream:
- STP (802.1D): Estandar clasico (convergencia lenta de hasta 50 seg).
- RSTP (802.1w): Rapid STP (convergencia ultrarrapida en 1-2 seg, recomendado).
- MSTP (802.1s): Multiple STP (agrupa multiples VLANs en instancias STP).



## 4. ACTIVACION DE RSTP Y DESIGNACION DE ROOT BRIDGE


### a) Habilitar globalmente Spanning Tree en modo RSTP:

```cisco
  SW-CORE-TPLINK(config)# spanning-tree mode rstp
  SW-CORE-TPLINK(config)# spanning-tree

b) Forzar al switch como Switch Raiz (Root Bridge):
  Configurar una prioridad menor que el valor por defecto (32768, en pasos de 4096):
  SW-CORE-TPLINK(config)# spanning-tree priority 0        (Raiz Principal)
  (o prioridad 4096 para switch de respaldo).
```


## 5. PROTECCION Y OPTIMIZACION DE PUERTOS STP


### a) PortFast (Edge Port):

  Hace que el puerto pase inmediatamente a estado de envio (Forwarding) al conectar
  una PC o servidor, sin esperar los temporizadores de escucha:
```cisco
  SW-CORE-TPLINK(config)# interface range gigabitEthernet 1/0/1-20
  SW-CORE-TPLINK(config-if-range)# spanning-tree portfast

b) BPDU Guard (Proteccion contra BPDUs):
  Deshabilita de inmediato el puerto si recibe paquetes BPDU (evita que un usuario
  conecte un switch no autorizado y altere el arbol de Spanning Tree):
  SW-CORE-TPLINK(config-if-range)# spanning-tree bpdu-guard

c) Root Guard:
  Impide que un switch no deseado se proclame como Root Bridge a traves de este puerto:
  SW-CORE-TPLINK(config)# interface gigabitEthernet 1/0/22
  SW-CORE-TPLINK(config-if)# spanning-tree root-guard
```


## 6. VERIFICACION Y COMANDOS DE DIAGNOSTICO

Visualizar resumen de los grupos Port-Channel configurados y puertos miembros:
```cisco
  SW-CORE-TPLINK# show port-channel 1
  SW-CORE-TPLINK# show etherchannel summary

Visualizar informacion de paquetes y negociacion LACP:
  SW-CORE-TPLINK# show lacp 1 internal

Visualizar el estado general de Spanning Tree y el ID del Root Bridge:
  SW-CORE-TPLINK# show spanning-tree

Visualizar el rol y estado STP de cada puerto (Forwarding, Blocking, Designated, Root):
```


## SW-CORE-TPLINK# show spanning-tree brief
