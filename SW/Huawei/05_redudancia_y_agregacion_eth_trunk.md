# GUIA HUAWEI VRP - PARTE 5: AGREGACION DE ENLACES (ETH-TRUNK) Y SPANNING TREE (RSTP)


---



## 1. AGREGACION DE ENLACES (ETH-TRUNK / LACP)

¿Para que sirve?
Permite unir dos o mas cables fisicos (ej. dos cables de 1 Gbps) en un solo enlace
logico de 2 Gbps. Logra dos objetivos esenciales:
- Duplicar el ancho de banda.
- Tolerancia a fallos: Si un cable se corta, el trafico sigue fluyendo por el otro
  sin interrupcion ni caida de red.

Existen 2 modos:
- Modo Manual: No usa protocolo de negociacion (simple pero menos tolerante a errores).
- Modo LACP (802.3ad): El estandar de la industria, negocia dinamicamente con el otro switch.



## 2. CONFIGURACION DE ETH-TRUNK EN MODO DINAMICO LACP

(Ejemplo: Unir los puertos GigabitEthernet 0/0/23 y 0/0/24 hacia otro switch)

Paso 1: Crear la interfaz logica Eth-Trunk y definir modo LACP
```text
[HUAWEI] interface Eth-Trunk 1
[HUAWEI-Eth-Trunk1] description ENLACE_AGREGADO_HACIA_SW_DISTRIBUCION
[HUAWEI-Eth-Trunk1] mode lacp
[HUAWEI-Eth-Trunk1] quit

Paso 2: Agregar los puertos fisicos al grupo Eth-Trunk
[HUAWEI] interface GigabitEthernet 0/0/23
[HUAWEI-GigabitEthernet0/0/23] eth-trunk 1
[HUAWEI-GigabitEthernet0/0/23] quit

[HUAWEI] interface GigabitEthernet 0/0/24
[HUAWEI-GigabitEthernet0/0/24] eth-trunk 1
[HUAWEI-GigabitEthernet0/0/24] quit

Paso 3: Configurar el Eth-Trunk como Troncal (Trunk) para pasar las VLANs
Nota: La configuracion de VLANs se aplica directamente a la interfaz Eth-Trunk 1,
NO a los puertos fisicos individuales.

[HUAWEI] interface Eth-Trunk 1
[HUAWEI-Eth-Trunk1] port link-type trunk
[HUAWEI-Eth-Trunk1] port trunk allow-pass vlan 10 20 30
[HUAWEI-Eth-Trunk1] quit
```


## 3. SPANNING TREE PROTOCOL (RSTP) - PREVENCION DE BUCLES

¿Por que es critico?
Si conectas switches en anillo o con cables redundantes sin STP, se genera una
"Tormenta de Broadcast" (Loop) que satura la CPU al 100% y tumba toda la red en segundos.

Se recomienda usar RSTP (Rapid Spanning Tree) por su convergencia en menos de 1 segundo.

Paso 1: Activar RSTP globalmente
```text
[HUAWEI] stp mode rstp
[HUAWEI] stp enable

Paso 2: Definir el Switch Principal (Root Bridge)
El switch central o Core debe ser el "Jefe de la red" (Prioridad mas baja = Mayor jerarquia):
[HUAWEI] stp root primary
  -> O configurando prioridad manual: "stp priority 4096"

En el switch de respaldo (Backup):
[HUAWEI-SW2] stp root secondary
  -> O prioridad manual: "stp priority 8192"
```


## 4. OPTIMIZACION DE PUERTOS DE ACCESO (EDGED-PORT Y BPDU PROTECTION)

Por defecto, cuando conectas una computadora, STP tarda unos 30 segundos en habilitar
el puerto. Para que el puerto levante al instante sin esperar, se activa "edged-port":

```text
[HUAWEI] interface GigabitEthernet 0/0/1
[HUAWEI-GigabitEthernet0/0/1] stp edged-port enable
[HUAWEI-GigabitEthernet0/0/1] quit
```

-- SEGURIDAD: BPDU Protection (Vital)
Si alguien conecta por error o malicia otro switch a un puerto de usuario, BPDU Protection
bloquea inmediatamente ese puerto para evitar que altere la topologia de la red:
```text
[HUAWEI] stp bpdu-protection
```


## 5. COMANDOS DE COMPROBACION

- Ver estado del enlace agregado (Eth-Trunk):
```text
    <HUAWEI> display eth-trunk 1

- Ver el estado de Spanning Tree en todos los puertos (Root, Desg, Altn / FWD, BLK):
    <HUAWEI> display stp brief

- Ver quien es el Switch Root de la red:
    <HUAWEI> display stp
```
