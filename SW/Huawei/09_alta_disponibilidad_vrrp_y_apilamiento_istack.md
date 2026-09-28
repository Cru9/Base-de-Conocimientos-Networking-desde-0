# GUIA HUAWEI VRP - PARTE 9: ALTA DISPONIBILIDAD CON VRRP Y APILAMIENTO (ISTACK)


---



## 1. ¿QUE ES VRRP (VIRTUAL ROUTER REDUNDANCY PROTOCOL)?

Si tienes dos switches Core (Core 1 y Core 2), ¿cual de los dos le pones como 
puerta de enlace (gateway) a las computadoras?
Si le pones la IP del Core 1 y este se quema, todos los usuarios pierden conexion.

VRRP soluciona esto creando una "IP VIRTUAL" compartida entre los dos switches:
- Core 1 (Switch Maestro / Master): Atiende todo el trafico normalmente.
- Core 2 (Switch de Respaldo / Backup): Monitorea a Core 1. Si Core 1 falla o se
  apaga, Core 2 asume la IP virtual en menos de 1 segundo de forma totalmente
  invisible para los usuarios.



## 2. CONFIGURACION DE VRRP EN PRODUCCION

Escenario: VLAN 10 (Red 192.168.10.0/24)
- IP Real Core 1: 192.168.10.2
- IP Real Core 2: 192.168.10.3
- IP VIRTUAL (Gateway de las PCs): 192.168.10.1


### A) En SWITCH CORE 1 (Configurar como MASTER):

```text
[SW-CORE-1] interface Vlanif 10
[SW-CORE-1-Vlanif10] ip address 192.168.10.2 255.255.255.0
-- Crear grupo VRRP 1 y definir la IP Virtual:
[SW-CORE-1-Vlanif10] vrrp vrid 1 virtual-ip 192.168.10.1
-- Asignar prioridad alta (120) para que sea el Master (por defecto es 100):
[SW-CORE-1-Vlanif10] vrrp vrid 1 priority 120
-- Seguimiento de enlace (Track Uplink hacia el Firewall):
-- Si el puerto Gigabit 0/0/24 se corta, reduce su prioridad en 30 para ceder el mando a Core 2:
[SW-CORE-1-Vlanif10] vrrp vrid 1 track interface GigabitEthernet 0/0/24 reduced 30
[SW-CORE-1-Vlanif10] quit

B) En SWITCH CORE 2 (Configurar como BACKUP):
[SW-CORE-2] interface Vlanif 10
[SW-CORE-2-Vlanif10] ip address 192.168.10.3 255.255.255.0
[SW-CORE-2-Vlanif10] vrrp vrid 1 virtual-ip 192.168.10.1
  -> No cambiamos la prioridad (se queda en 100 por defecto).
[SW-CORE-2-Vlanif10] quit
```


## 3. APILAMIENTO DE SWITCHES (HUAWEI ISTACK)

¿Que es iStack?
Tecnologia que permite unir fisicamente varios switches (mediante cables dedicados de
stack o puertos DAC/SFP de 10Gbps/40Gbps) para que operen como UN SOLO SWITCH LOGICO.

Ventajas:
- Gestionas 2, 4 o mas switches con una sola direccion IP y una sola consola.
- Si un switch tiene 48 puertos y unes 2, tendras un switch gigante de 96 puertos.
- La nomenclatura de puertos cambia a: GigabitEthernet <Slot>/<Subslot>/<Puerto>
  Ejemplo: G0/0/1 (Puerto 1 del switch 1), G1/0/1 (Puerto 1 del switch 2).

PASOS BASICOS PARA ARMAR UN STACK:
Paso 1: Configurar el Switch 1 (Maestro)
```text
[SW-1] stack slot 0 priority 200     <- Mayor prioridad = Switch Maestro
[SW-1] interface stack-port 0/1
[SW-1-stack-port0/1] port interface GigabitEthernet 0/0/27 enable
[SW-1-stack-port0/1] quit

Paso 2: Configurar el Switch 2 (Esclavo / Miembro)
[SW-2] stack slot 0 renumber 1       <- Cambia su ID de Slot a 1
[SW-2] stack slot 1 priority 100
[SW-2] interface stack-port 1/1
[SW-2-stack-port1/1] port interface GigabitEthernet 0/0/27 enable
[SW-2-stack-port1/1] quit

Paso 3: Guardar cambios en ambos ("save"), apagar, conectar los cables y encender.
Ambos switches se uniran y se administraran desde una sola IP.
```


## 4. COMANDOS DE VERIFICACION

- Ver estado de VRRP (Quien es Master y quien Backup):
```text
    <HUAWEI> display vrrp brief

- Ver estado detallado del apilamiento iStack (Miembros, roles, estado del enlace):
    <HUAWEI> display stack
    <HUAWEI> display stack configuration
```
