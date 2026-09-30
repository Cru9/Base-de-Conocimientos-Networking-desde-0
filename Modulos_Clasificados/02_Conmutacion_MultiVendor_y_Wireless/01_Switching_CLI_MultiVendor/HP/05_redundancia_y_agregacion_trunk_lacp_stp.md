# GUIA HP PROCURVE / ARUBA - PARTE 5: AGREGACION DE ENLACES (TRUNK LACP) Y SPANNING TREE (RSTP)


---



## 1. ¡CUIDADO CON LA TERMINOLOGIA! (TRUNK EN HP vs CISCO)

En Cisco, "Trunk" significa pasar varias VLANs por un cable.
En HP ProCurve, ¡"TRUNK" SIGNIFICA AGREGAR CABLES (Link Aggregation / EtherChannel)!
Para pasar varias VLANs en HP se usa la palabra "TAGGED".

¿Para que sirve un Trunk LACP en HP?
Une 2 o mas cables fisicos (ej. puertos 23 y 24) en un canal virtual (trk1) de 2 Gbps.
- Duplica la velocidad del enlace.
- Proporciona tolerancia a fallos: si un cable se corta, el servicio continua activo.



## 2. CONFIGURACION DE TRUNK LACP EN HP

Ejemplo: Unir los puertos 23 y 24 hacia otro switch usando LACP (802.3ad):

Paso 1: Crear el grupo de agregacion LACP:
```cisco
SW-HP(config)# trunk 23-24 trk1 lacp
  -> "trk1": Es el nombre de la interfaz agregada logica creada.
  -> "lacp": Usa el protocolo dinamico estandar de la industria.

Paso 2: Pasar las VLANs a traves del nuevo canal (trk1):
¡RECUERDA!: En HP se configuran las VLANs entrando a cada una de ellas:
SW-HP(config)# vlan 10
SW-HP(vlan-10)# tagged trk1
SW-HP(vlan-10)# exit

SW-HP(config)# vlan 20
SW-HP(vlan-20)# tagged trk1
SW-HP(vlan-20)# exit

SW-HP(config)# vlan 30
SW-HP(vlan-30)# tagged trk1
SW-HP(vlan-30)# exit
```


## 3. SPANNING TREE PROTOCOL (RSTP) - PREVENCION DE BUCLES

¿Por que es indispensable?
Cualquier bucle accidental de cables tumbara la red en segundos por una tormenta
de broadcast. Spanning Tree apaga logicamente los caminos redundantes y los enciende
solo si el camino principal se corta.

Paso 1: Habilitar Spanning Tree en modo RSTP (Rapid Spanning Tree):
```cisco
SW-HP(config)# spanning-tree
SW-HP(config)# spanning-tree protocol rstp

Paso 2: Definir el Switch Principal (Root Bridge)
El Switch Core principal debe ganar la eleccion de Spanning Tree.
(Prioridad mas baja = Gana la eleccion. Rango: 0 a 61440 en pasos de 4096).

En Switch Core 1 (Principal):
SW-HP-Core1(config)# spanning-tree priority 0

En Switch Core 2 (Respaldo):
SW-HP-Core2(config)# spanning-tree priority 4096
```


## 4. OPTIMIZACION DE PUERTOS DE ACCESO (ADMIN-EDGE-PORT Y BPDU PROTECTION)

Por defecto, STP tarda unos 30 segundos en habilitar un puerto cuando conectas
una PC. Para que levante inmediatamente (equivalente a PortFast de Cisco):

```cisco
SW-HP(config)# spanning-tree 1-20 admin-edge-port

-- PROTECCION BPDU (Vital en puertos de usuario):
Si un usuario conecta un switch casero a una roseta de red, el switch detecta
los paquetes BPDU y desactiva el puerto de inmediato para proteger la red:
SW-HP(config)# spanning-tree 1-20 bpdu-protection
```


## 5. COMANDOS DE DIAGNOSTICO Y VERIFICACION

- Ver estado de los enlaces agregados (Trunks LACP):
```cisco
    SW-HP# show trunks
    SW-HP# show lacp

- Ver el estado de Spanning Tree en todos los puertos (Blocking / Forwarding):
    SW-HP# show spanning-tree

- Ver quien es el Root Bridge de la red:
    SW-HP# show spanning-tree root
```
