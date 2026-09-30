# 04. FALLAS EN ENLACES AGREGADOS (PORT-CHANNEL / LACP / LAG / ETH-TRUNK)

> **RESOLUCION DE FALLAS (TROUBLESHOOTING DE SWITCHES)**


---



## 1. DESCRIPCION DEL PROBLEMA Y SINTOMAS

- La interfaz logica agregada (Port-Channel / Eth-Trunk / LAG) aparece con estado
  'Down', 'Suspended' (S) o 'Not in bundle'.
- El ancho de banda no aumenta (ej. se conectaron dos cables de 1 Gbps pero el
  enlace sigue operando a 1 Gbps en vez de 2 Gbps).
- Spanning Tree bloquea uno de los cables fisicos del grupo creyendo que se trata
  de un bucle, porque la negociacion de agregacion fallo.
- Perdida intermitente de paquetes cuando el algoritmo de hashing envia tráfico
  por el cable que no logro unirse al grupo.



## 2. PRINCIPALES CAUSAS RAIZ


### a) Discrepancia de velocidad o duplex entre los puertos miembros:

   - Para que varios puertos formen un LAG, sus caracteristicas de hardware deben
     ser IDENTICAS.
   - Si el puerto 1 negocio a 1 Gbps Full-Duplex, pero el puerto 2 tiene un pin
     doblado o un cable defectuoso y negocio a 100 Mbps, LACP rechazara unir el
     puerto 2 al grupo y lo pondra en estado 'Suspended'.


### b) Discrepancia de parametros de VLAN en los puertos fisicos:

   - Si el puerto 1 tiene permitidas las VLANs `10,20` y el puerto 2 tiene `10,20,30`,
     el protocolo de agregacion detecta inconsistencia de configuracion y deshabilita
     el Port-Channel.


### c) Incompatibilidad de modos de negociacion LACP:

   - Switch A esta en modo 'active' (LACP dinamico) pero Switch B fue configurado
     en modo 'on' (LAG estatico). Un puerto estatico nunca responde paquetes LACP.
   - Ambos conmutadores estan en modo 'passive' (ambos esperan a que el otro hable;
     ninguno inicia la negociacion y el LAG nunca levanta).


### d) Configuracion aplicada en los puertos fisicos en lugar de la interfaz logica:

   - El administrador modifico una VLAN directamente en `GigabitEthernet 0/1` en vez
     de aplicarla en `interface port-channel 1`.



## 3. COMANDOS DE DIAGNOSTICO POR MARCA

CISCO:
```cisco
  SW# show etherchannel summary
  (Banderas criticas:
     (D) Down: Canal caido.
     (P) Bundled in port-channel: Puerto operando exitosamente dentro del grupo.
     (s) Suspended: Puerto rechazado por incompatibilidad de velocidad o VLAN.
     (I) Independent: Operando como puerto individual sin agregar.)
  SW# show lacp neighbor
  SW# show interfaces GigabitEthernet 0/23 etherchannel
```

HUAWEI:
```cisco
  SW> display eth-trunk
  SW> display eth-trunk 1
  SW> display lacp statistics-eth-trunk
```

3COM / H3C:
```cisco
  SW> display link-aggregation summary
  SW> display link-aggregation verbose
```

HP PROCURVE:
```cisco
  SW# show trunks
  SW# show lacp
  SW# show lacp peer

ARUBA (AOS-CX):
  SW# show lag brief
  SW# show lag 1
  SW# show lacp interfaces
```

TP-LINK JETSTREAM:
```cisco
  SW# show etherchannel summary
  SW# show port-channel 1
  SW# show lacp 1 internal
```


## 4. SOLUCION PASO A PASO

Paso 1: Validar velocidad y duplex en todos los puertos miembros
Asegurese de que ambos cables esten negociando la misma velocidad:
```text
  SW# show interfaces status | include Gi0/23|Gi0/24
Si un puerto esta en 100M y el otro en 1G, reemplace el cable UTP defectuoso.

Paso 2: Utilizar el modo de negociacion LACP correcto
La mejor practica es usar 'active' en ambos extremos:
  (Cisco)       channel-group 1 mode active
  (Huawei)      interface Eth-Trunk 1 -> mode lacp-static
  (Aruba CX)    interface lag 1 -> lacp mode active
  (TP-Link)     channel-group 1 mode active

Paso 3: REGLA DE ORO DE CONFIGURACION DE PORT-CHANNELS
Nunca configure VLANs o descripciones directamente en los puertos fisicos miembros.
Configure SIEMPRE la interfaz logica:

Correcto en Cisco / TP-Link:
  SW(config)# interface port-channel 1
  SW(config-if)# switchport mode trunk
  SW(config-if)# switchport trunk allowed vlan 10,20,30
  (Los puertos miembros heredaran esta configuracion de forma automatica y sincronizada).

Correcto en Huawei:
  SW(config)# interface Eth-Trunk 1
  SW(config-if)# port link-type trunk
  SW(config-if)# port trunk allow-pass vlan 10 20 30
```


## 5. ALGORITMO DE BALANCEO DE CARGA (LOAD BALANCING HASH)

Por defecto, muchos conmutadores balancean el trafico usando unicamente la direccion
MAC origen (`src-mac`). Si un solo servidor realiza la mayoria de las transferencias,
todo el trafico saldra por el mismo cable fisico, saturandolo mientras el otro cable
permanece desocupado.

Solucion recomendada: Balancear por IP origen y destino (o puerto L4):
  (Cisco)       SW(config)# port-channel load-balance src-dst-ip
  (Huawei)      SW(config-if-Eth-Trunk1)# load-balance ip-based

## (TP-Link)     SW(config)# port-channel load-balance src-dst-ip
