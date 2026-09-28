# GUIA 3COM COMWARE - PARTE 5: AGREGACION DE ENLACES (LINK-AGGREGATION) Y SPANNING TREE (RSTP)


---



## 1. AGREGACION DE ENLACES (LINK-AGGREGATION / LACP)

¿Para que sirve?
Permite unir dos o mas cables fisicos (ej. dos enlaces Gigabit) para formar un solo
enlace logico con el doble de velocidad y alta tolerancia a fallos:
- Si un cable se corta, el trafico continua fluyendo por el otro sin cortes de red.
- Balancea la carga entre los cables disponibles.

En 3Com Comware existen dos modos:
- Modo Manual: Sin protocolo de negociacion.
- Modo Dinamico (LACP 802.3ad): El estandar de la industria con negociacion activa.



## 2. CONFIGURACION DE ENLACE AGREGADO CON LACP

(Ejemplo: Unir los puertos GigabitEthernet 1/0/23 y 1/0/24 hacia otro switch)

Paso 1: Crear el grupo de agregacion en modo dinamico LACP:
```text
[3Com] link-aggregation group 1 mode dynamic

Paso 2: Agregar los puertos fisicos al grupo:
[3Com] interface GigabitEthernet 1/0/23
[3Com-GigabitEthernet1/0/23] port link-aggregation group 1
[3Com-GigabitEthernet1/0/23] quit

[3Com] interface GigabitEthernet 1/0/24
[3Com-GigabitEthernet1/0/24] port link-aggregation group 1
[3Com-GigabitEthernet1/0/24] quit

Paso 3: Configurar el enlace agregado como Troncal (Trunk):
En 3Com, la configuracion de troncal se aplica a los miembros o a la interfaz virtual
Bridge-Aggregation segun el modelo:
[3Com] interface GigabitEthernet 1/0/23
[3Com-GigabitEthernet1/0/23] port link-type trunk
[3Com-GigabitEthernet1/0/23] port trunk permit vlan 10 20 30 100
[3Com-GigabitEthernet1/0/23] quit

[3Com] interface GigabitEthernet 1/0/24
[3Com-GigabitEthernet1/0/24] port link-type trunk
[3Com-GigabitEthernet1/0/24] port trunk permit vlan 10 20 30 100
[3Com-GigabitEthernet1/0/24] quit
```


## 3. SPANNING TREE PROTOCOL (RSTP) - PREVENCION DE BUCLES

¿Por que es critico?
Si se conectan switches en circulo o con enlaces redundantes sin STP, se produce
una tormenta de broadcast instantanea que colapsa la red corporativa al 100%.

Se debe activar RSTP (Rapid Spanning Tree) para una recuperacion en menos de 1 segundo:

Paso 1: Habilitar RSTP globalmente:
```text
[3Com] stp mode rstp
[3Com] stp enable

Paso 2: Definir el Switch Principal (Root Bridge)
El Switch Core principal debe ser el centro del arbol de Spanning Tree.
(Prioridad mas baja = Gana la eleccion).

En Switch Core 1 (Principal):
[3Com-Core1] stp root primary
  -> O configurando prioridad numerica manual:
     [3Com-Core1] stp priority 4096

En Switch Core 2 (Respaldo):
[3Com-Core2] stp root secondary
  -> O prioridad:
     [3Com-Core2] stp priority 8192
```


## 4. OPTIMIZACION DE PUERTOS DE ACCESO (EDGE-PORT Y BPDU PROTECTION)

Para que los puertos de computadoras enciendan de inmediato sin esperar 30 segundos:

```text
[3Com] interface GigabitEthernet 1/0/1
[3Com-GigabitEthernet1/0/1] stp edged-port enable
[3Com-GigabitEthernet1/0/1] quit

-- PROTECCION BPDU (Vital en puertos de usuario):
Si un usuario conecta un switch no autorizado a una roseta de red, BPDU Protection
apaga el puerto de inmediato para evitar que afecte a la topologia de la red:
[3Com] stp bpdu-protection
```


## 5. COMANDOS DE VERIFICACION

- Ver estado de los enlaces agregados (puertos activos, modo y velocidad):
```text
    <3Com> display link-aggregation summary
    <3Com> display link-aggregation verbose 1

- Ver el estado de Spanning Tree en los puertos (Forwarding, Discarding, Root, Desg):
    <3Com> display stp brief

- Ver quien es el Root Bridge actual de la red:
    <3Com> display stp root
```
