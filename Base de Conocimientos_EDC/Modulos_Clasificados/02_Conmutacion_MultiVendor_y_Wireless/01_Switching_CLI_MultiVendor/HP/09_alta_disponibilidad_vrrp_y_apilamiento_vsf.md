# GUIA HP PROCURVE / ARUBA - PARTE 9: ALTA DISPONIBILIDAD CON VRRP Y APILAMIENTO (VSF)


---



## 1. ¿QUE ES VRRP EN SWITCHES HP?

VRRP (Virtual Router Redundancy Protocol) permite que dos switches multicapa compartan
una sola DIRECCION IP VIRTUAL que sirve como la puerta de enlace (Gateway) de todos
los equipos de la red:

- Switch 1 (MASTER / Maestro): Enruta todo el trafico de las computadoras activamente.
- Switch 2 (BACKUP / Respaldo): Monitorea al Switch 1. Si el Switch 1 se apaga,
  se quema o pierde conexion, Switch 2 toma el control de la IP virtual en menos
  de 1 segundo sin interrumpir a los usuarios.



## 2. CONFIGURACION DE VRRP EN PRODUCCION

Escenario para la VLAN 10 (Red 192.168.10.0/24):
- IP Real Switch Core 1: 192.168.10.2
- IP Real Switch Core 2: 192.168.10.3
- IP VIRTUAL (Gateway configurado en las PCs): 192.168.10.1


### A) En SWITCH CORE 1 (Configurar como MASTER):

```cisco
SW-HP-Core1(config)# vlan 10
SW-HP-Core1(vlan-10)# ip address 192.168.10.2 255.255.255.0
-- Iniciar el grupo VRRP 1 en la VLAN:
SW-HP-Core1(vlan-10)# vrrp vrid 1
-- Definir la IP Virtual del Gateway:
SW-HP-Core1(vlan-10-vrid-1)# virtual-ip-address 192.168.10.1
-- Asignar prioridad alta (120) para que sea el Master (por defecto es 100):
SW-HP-Core1(vlan-10-vrid-1)# priority 120
-- Habilitar Preempt (recuperar el rol cuando el switch reinicie):
SW-HP-Core1(vlan-10-vrid-1)# preempt
-- Seguimiento de enlace (si el puerto 24 hacia el Firewall se corta, reduce prioridad):
SW-HP-Core1(vlan-10-vrid-1)# track-port 24 30
-- Activar el grupo VRRP:
SW-HP-Core1(vlan-10-vrid-1)# enable
SW-HP-Core1(vlan-10-vrid-1)# exit
SW-HP-Core1(vlan-10)# exit

B) En SWITCH CORE 2 (Configurar como BACKUP):
SW-HP-Core2(config)# vlan 10
SW-HP-Core2(vlan-10)# ip address 192.168.10.3 255.255.255.0
SW-HP-Core2(vlan-10)# vrrp vrid 1
SW-HP-Core2(vlan-10-vrid-1)# virtual-ip-address 192.168.10.1
SW-HP-Core2(vlan-10-vrid-1)# preempt
SW-HP-Core2(vlan-10-vrid-1)# enable
  -> No modificamos la prioridad (se queda en 100, quedando como Backup).
SW-HP-Core2(vlan-10-vrid-1)# exit
```


## 3. APILAMIENTO MODERNO (ARUBA / HP VSF - VIRTUAL SWITCHING FRAMEWORK)

¿Que es VSF?
En modelos modernos (ej. Aruba 2930F, 5400R), VSF permite apilar switches usando
cables comunes de fibra o DAC de 10 Gbps (puertos SFP+ estándar), ¡sin cables de
apilamiento propietarios costosos!

Ventajas:
- Opera multiples switches fisicos como un solo switch logico gigante.
- Una sola direccion IP y una sola consola de administracion.
- Nomenclatura de puertos en el stack: Miembro/Puerto (ej. 1/1, 1/2 ... 2/1, 2/2).

PASOS DE CONFIGURACION:
Paso 1: En el Switch 1 (Comandante / Commander):
```cisco
SW-1(config)# vsf enable domain 1
SW-1(config)# vsf member 1 priority 128    <- Maxima prioridad = Maestro
SW-1(config)# vsf member 1 link 1 25,26   <- Usa los puertos 10G 25 y 26 como enlace de stack
SW-1(config)# write memory

Paso 2: En el Switch 2 (En espera / Standby):
SW-2(config)# vsf enable domain 1
SW-2(config)# vsf member 2 priority 100
SW-2(config)# vsf member 2 link 1 25,26
SW-2(config)# write memory

Paso 3: Conectar los cables de 10G cruzados entre los puertos 25/26 de ambos switches.
Los switches se reiniciaran y se fusionaran en un solo sistema.
```


## 4. COMANDOS DE VERIFICACION

- Ver estado de VRRP (Master / Backup y estado de IP virtual):
```cisco
    SW-HP# show vrrp
    SW-HP# show vrrp brief

- Ver estado del apilamiento VSF (Miembros, roles Commander/Standby y estado de enlaces):
    SW-HP# show vsf
    SW-HP# show vsf link
    SW-HP# show vsf detail
```
