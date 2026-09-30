# GUIA CISCO IOS - PARTE 5: AGREGACION DE ENLACES (ETHERCHANNEL) Y SPANNING TREE (RAPID-PVST+)


---



## 1. AGREGACION DE ENLACES (CISCO ETHERCHANNEL)

¿Que es EtherChannel?
Permite agrupar hasta 8 puertos fisicos (ej. dos enlaces de 1 Gbps) para que operen
como un solo enlace logico virtual (Port-Channel de 2 Gbps).
- Aumenta el ancho de banda.
- Proporciona redundancia: si un cable falla, el trafico no se corta.

Protocolos disponibles:
- LACP (802.3ad - Estandar abierto): Modos ACTIVE (inicia negociacion) y PASSIVE.
- PAgP (Propietario de Cisco): Modos DESIRABLE y AUTO.
- Manual (Sin protocolo): Modo ON.
¡Recomendacion en la industria!: Usar siempre LACP (modo ACTIVE).



## 2. CONFIGURACION DE ETHERCHANNEL CON LACP

(Ejemplo: Unir GigabitEthernet 0/23 y 0/24 hacia otro switch)

Paso 1: Entrar al rango de interfaces y asignarlas al grupo de canal:
```cisco
Switch(config)# interface range GigabitEthernet 0/23 - 24
Switch(config-if-range)# channel-group 1 mode active
Switch(config-if-range)# exit
  -> Cisco creara automaticamente la interfaz virtual: "interface Port-channel 1".

Paso 2: Configurar la interfaz Port-Channel como Troncal (Trunk):
¡REGLA FUNDAMENTAL!: La configuracion de VLANs y Trunk se hace sobre la interfaz
Port-channel 1, NUNCA sobre los puertos individuales.

Switch(config)# interface Port-channel 1
Switch(config-if)# description ETHERCHANNEL_HACIA_CORE
Switch(config-if)# switchport mode trunk
Switch(config-if)# switchport trunk allowed vlan 10,20,30,100
Switch(config-if)# exit

-- (Opcional) Metodo de balanceo de carga (por IP de origen y destino):
Switch(config)# port-channel load-balance src-dst-ip
```


## 3. SPANNING TREE PROTOCOL (RAPID-PVST+)

¿Por que es indispensable?
Cualquier bucle fisico accidental (dos cables entre los mismos switches) creara
una tormenta de broadcast que tumba la red en 10 segundos. STP bloquea los puertos
redundantes y solo los abre si el enlace principal falla.

Cisco utiliza por defecto PVST+ (Per-VLAN Spanning Tree). Se debe cambiar a 
RAPID-PVST+ para que la convergencia sea inmediata (menos de 1 segundo):

Paso 1: Activar Rapid-PVST+
```cisco
Switch(config)# spanning-tree mode rapid-pvst

Paso 2: Definir el Switch Raiz (Root Bridge)
El Switch Core principal debe ser el centro del arbol de Spanning Tree.
(Prioridad mas baja = Gana la eleccion).

En el Switch Core 1 (Principal):
Switch-Core1(config)# spanning-tree vlan 10,20,30,100 root primary
  -> O configurando manualmente la prioridad:
     Switch-Core1(config)# spanning-tree vlan 10,20 priority 4096

En el Switch Core 2 (Respaldo):
Switch-Core2(config)# spanning-tree vlan 10,20,30,100 root secondary
  -> O prioridad:
     Switch-Core2(config)# spanning-tree vlan 10,20 priority 8192
```


## 4. OPTIMIZACION DE PUERTOS DE USUARIO (PORTFAST Y BPDU GUARD)

Por defecto, STP tarda 30 a 50 segundos en habilitar un puerto para escuchar si
hay bucles. Con PortFast, el puerto levanta inmediatamente en cuanto conectas una PC.

-- Activar PortFast y BPDU Guard a nivel global en todos los puertos de acceso:
```cisco
Switch(config)# spanning-tree portfast default
Switch(config)# spanning-tree portfast bpduguard default

-- O activarlo por puerto individual:
Switch(config)# interface GigabitEthernet 0/1
Switch(config-if)# spanning-tree portfast
Switch(config-if)# spanning-tree bpduguard enable
Switch(config-if)# exit

* ¿Que hace BPDU Guard?: Si un usuario conecta un switch personal a un puerto de acceso,
  el switch detecta los paquetes BPDU y apaga el puerto inmediatamente (err-disable)
  para proteger la red.
```


## 5. VERIFICACION

- Ver estado del EtherChannel (Debe mostrar flags "SU" = Layer2 & In-Use, y puertos con "P" = Bundled):
```cisco
    Switch# show etherchannel summary

- Ver que puertos estan bloqueados o transmitiendo en Spanning Tree:
    Switch# show spanning-tree brief

- Ver quien es el Root Bridge para una VLAN:
    Switch# show spanning-tree vlan 10
```
