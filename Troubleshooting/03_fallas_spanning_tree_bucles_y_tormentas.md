# 03. FALLAS DE SPANNING TREE, BUCLES DE CAPA 2 Y TORMENTAS DE DIFUSION

> **RESOLUCION DE FALLAS (TROUBLESHOOTING DE SWITCHES)**


---



## 1. SINTOMAS DE UNA TORMENTA DE DIFUSION (BROADCAST STORM / LOOP L2)

Un bucle de conmutacion es la falla mas destructiva en una red local:
- Todos los LEDs de actividad del switch parpadean de forma sincronizada y a
  frecuencia maxima (apariencia de "arbol de navidad").
- El uso de CPU del conmutador se dispara al 99% - 100%.
- La sesion por SSH o consola se vuelve extremadamente lenta o se congela por
  completo (el plano de control esta saturado procesando millones de broadcasts).
- Perdida masiva de paquetes en pruebas de Ping (70% a 100% de perdida).
- En los registros (logs) aparecen cientos de alertas de aleteo de direcciones MAC:
  "%SW_MATM-4-MACFLAP_NOTIF: Host 0015.5d01.a2b4 in vlan 1 is flapping between
  port GigabitEthernet0/5 and GigabitEthernet0/12"



## 2. PRINCIPALES CAUSAS RAIZ


### a) Bucle fisico sin proteccion Spanning Tree:

   - Un usuario o tecnico conecto ambos extremos de un cable de red a dos tomas
     de pared distintas en la misma oficina.
   - Conectar dos cables entre dos conmutadores creyendo que se duplicaria la
     velocidad, sin haber configurado un canal agregado (LACP / Port-Channel).
   - Un switch casero no administrado con un bucle propio conectado a la red.


### b) Secuestro involuntario del Switch Raiz (Root Bridge Takeover):

   - El switch Core fue dejado con la prioridad por defecto (32768).
   - Se conecto un switch de acceso nuevo o viejo que tenia una direccion MAC base
     inferior o prioridad menor.
   - Consecuencia: El switch pequeño de acceso se convirtio en el Root Bridge de
     toda la empresa, forzando a que todo el tráfico de la red viaje a traves de
     sus puertos de 100M/1G, saturandolo y colapsando la topologia.


### c) Discrepancia de modos de Spanning Tree (MSTP vs RSTP vs PVST+):

   - Conmutadores que no logran entender sus paquetes BPDU y no bloquean el enlace
     redundante, creyendo que no hay bucle.



## 3. PROTOCOLO DE AISLAMIENTO DE EMERGENCIA (COMO DETENER EL BUCLE)

¡ATENCION! NO REINICIE EL SWITCH.
Si reinicia el switch mientras el cable en bucle sigue conectado, en cuanto el
switch termine de encender la red volvera a colapsar de inmediato.

Paso 1: Identificar los puertos causantes mediante el log de MAC Flapping
  En Cisco / TP-Link:
```cisco
    SW# show logging | include MACFLAP
  En Huawei / 3Com:
    SW> display logbuffer | include MAC-FLAPPING
  En HP / Aruba:
    SW# show log -r | include "flapping"

El log indicara entre que dos puertos esta saltando la direccion MAC (ej. Gi0/5 y Gi0/12).

Paso 2: Apagar uno de los dos puertos sospechosos
  SW(config)# interface GigabitEthernet 0/5
  SW(config-if)# shutdown
Si el trafico se normaliza de inmediato y los LEDs dejan de titilar como tormenta,
ese puerto tenia el cable en bucle o el switch casero.
```


## 4. COMANDOS DE DIAGNOSTICO DE SPANNING TREE

CISCO:
```cisco
  SW# show spanning-tree
  (Verificar quien es el Root: 'This bridge is the root' o direccion MAC del raiz)
  SW# show spanning-tree brief
  SW# show spanning-tree detail | include is the root|from
```

HUAWEI:
```cisco
  SW> display stp brief
  SW> display stp root
```

3COM / H3C:
```cisco
  SW> display stp brief
  SW> display stp root
```

HP PROCURVE:
```cisco
  SW# show spanning-tree
  SW# show spanning-tree detail

ARUBA (AOS-CX):
  SW# show spanning-tree
  SW# show spanning-tree brief
```

TP-LINK JETSTREAM:
```cisco
  SW# show spanning-tree
  SW# show spanning-tree brief
```


## 5. GUIA DEFINITIVA DE PROTECCION CONTRA BUCLES

Para que su red NUNCA vuelva a caerse por un bucle, aplique estas 3 directrices:

1. Fije la prioridad del Switch Core Principal en 0 o 4096:
   (Cisco)     SW(config)# spanning-tree vlan 1 priority 4096
   (Huawei)    SW(config)# stp priority 4096
   (HP/Aruba)  SW(config)# spanning-tree priority 4096
   (TP-Link)   SW(config)# spanning-tree priority 4096

2. Active BPDU Guard en TODOS los puertos de acceso de usuarios:
   (Cisco)     SW(config)# spanning-tree portfast bpduguard default
   (Huawei)    SW(config)# stp bpdu-protection
   (HP)        SW(config)# spanning-tree 1-23 bpdu-protection
   (Aruba CX)  SW(config)# spanning-tree bpdu-guard
   (TP-Link)   SW(config)# interface range Gi1/0/1-23 -> spanning-tree bpdu-guard

3. Active Root Guard en puertos de bajada hacia switches secundarios:
   Evita que cualquier switch externo pueda proclamarse como Raiz.
   (Cisco)     SW(config-if)# spanning-tree root-guard
   (Huawei)    SW(config-if)# stp root-protection

## (HP/Aruba)  SW(config-if)# spanning-tree root-guard
