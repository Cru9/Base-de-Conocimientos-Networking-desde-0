# GUIA 3COM COMWARE - PARTE 9: ALTA DISPONIBILIDAD CON VRRP Y APILAMIENTO (XRN / IRF)


---



## 1. ¿QUE ES VRRP EN SWITCHES 3COM?

VRRP (Virtual Router Redundancy Protocol) permite que dos switches multicapa compartan
una sola DIRECCION IP VIRTUAL que sirve como la puerta de enlace (Gateway) de todos
los equipos de la red:

- Switch 1 (MASTER / Maestro): Enruta todo el trafico de las computadoras activamente.
- Switch 2 (BACKUP / Respaldo): Monitorea a Switch 1. Si Switch 1 se apaga o falla,
  Switch 2 asume el control de la IP virtual en menos de 1 segundo de forma totalmente
  transparente para los usuarios.



## 2. CONFIGURACION DE VRRP EN PRODUCCION

Escenario para la VLAN 10 (Red 192.168.10.0/24):
- IP Real Switch Core 1: 192.168.10.2
- IP Real Switch Core 2: 192.168.10.3
- IP VIRTUAL (Gateway de las PCs): 192.168.10.1


### A) En SWITCH CORE 1 (Configurar como MASTER):

```text
[SW-CORE-1] interface Vlan-interface 10
[SW-CORE-1-Vlan-interface10] ip address 192.168.10.2 255.255.255.0
-- Definir la IP Virtual del grupo VRRP 1:
[SW-CORE-1-Vlan-interface10] vrrp vrid 1 virtual-ip 192.168.10.1
-- Asignar prioridad alta (120) para que sea el Master (por defecto es 100):
[SW-CORE-1-Vlan-interface10] vrrp vrid 1 priority 120
-- Seguimiento de enlace (Interface Tracking):
-- Si el puerto hacia el Firewall (G1/0/24) se corta, descuenta 30 puntos de prioridad
-- para que Core 2 tome el mando de inmediato:
[SW-CORE-1-Vlan-interface10] vrrp vrid 1 track interface GigabitEthernet 1/0/24 reduced 30
[SW-CORE-1-Vlan-interface10] quit

B) En SWITCH CORE 2 (Configurar como BACKUP):
[SW-CORE-2] interface Vlan-interface 10
[SW-CORE-2-Vlan-interface10] ip address 192.168.10.3 255.255.255.0
[SW-CORE-2-Vlan-interface10] vrrp vrid 1 virtual-ip 192.168.10.1
  -> No modificamos la prioridad (se queda en 100, quedando como Backup).
[SW-CORE-2-Vlan-interface10] quit
```


## 3. APILAMIENTO RESILIENTE (3COM XRN / IRF)

¿Que es XRN / IRF?
3Com fue pionero en la industria con su tecnologia XRN (eXpandable Resilient Networking),
evolucionada posteriormente como IRF (Intelligent Resilient Framework).
Permite interconectar fisicamente varios switches mediante cables de stack o puertos SFP+
para que operen como UN SOLO SWITCH VIRTUAL GIGANTE.

Ventajas:
- Una sola direccion IP y una sola consola para administrar 2 o mas switches fisicos.
- Los puertos se identifican por Unidad/Ranura/Puerto:
  GigabitEthernet 1/0/1 -> Switch 1, puerto 1.
  GigabitEthernet 2/0/1 -> Switch 2, puerto 1.

PASOS BASICOS DE CONFIGURACION:
Paso 1: En el Switch 1 (Maestro), asignar mayor prioridad:
```text
[SW-1] irf member 1 priority 32
[SW-1] save

Paso 2: En el Switch 2, cambiar su numero de unidad a 2:
[SW-2] irf member 1 renumber 2
[SW-2] save

Paso 3: Apagar ambos equipos, conectar los cables de apilamiento en bucle cerrado,
y encender primero el Switch 1 y despues el Switch 2. Ambos se sincronizaran.
```


## 4. VERIFICACION

- Ver estado de VRRP (muestra quien es Master y quien Backup):
```text
    <3Com> display vrrp brief

- Ver estado de los switches del Stack (Unidad maestra, miembros y estado):
    <3Com> display irf
```
