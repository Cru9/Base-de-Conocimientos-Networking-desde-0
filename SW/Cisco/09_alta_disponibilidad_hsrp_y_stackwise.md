# GUIA CISCO IOS - PARTE 9: ALTA DISPONIBILIDAD CON HSRP Y APILAMIENTO (STACKWISE)


---



## 1. ¿QUE ES HSRP (HOT STANDBY ROUTER PROTOCOL)?

HSRP es el protocolo de redundancia de primer salto (FHRP) creado por Cisco.
Permite que dos switches multicapa compartan una misma DIRECCION IP VIRTUAL que
actua como la puerta de enlace (Gateway) de todos los usuarios de la red:

- Switch 1 (ACTIVE / Activo): Enruta todo el trafico de las computadoras.
- Switch 2 (STANDBY / Espera): Esta escuchando. Si el Switch 1 se apaga, se quema
  o pierde su enlace a Internet, el Switch 2 toma el control de la IP virtual en
  menos de 1 segundo de forma totalmente transparente para los usuarios.



## 2. CONFIGURACION DE HSRP EN PRODUCCION

Escenario para la VLAN 10:
- IP Real Switch Core 1: 192.168.10.2
- IP Real Switch Core 2: 192.168.10.3
- IP VIRTUAL (Gateway configurado en las PCs): 192.168.10.1


### A) En SWITCH CORE 1 (Configurar como ACTIVO):

Switch-Core1(config)# interface vlan 10
Switch-Core1(config-if)# ip address 192.168.10.2 255.255.255.0
-- Configurar version 2 de HSRP (Soporta rangos mas amplios y IPv6):
Switch-Core1(config-if)# standby version 2
-- Definir la IP Virtual del grupo 1:
Switch-Core1(config-if)# standby 1 ip 192.168.10.1
-- Asignar prioridad alta (120) para que sea el preferido (por defecto es 100):
Switch-Core1(config-if)# standby 1 priority 120
-- ¡COMANDO CRITICO! Preempt (Permite recuperar el rol de Activo cuando el switch reinicie):
Switch-Core1(config-if)# standby 1 preempt
-- Seguimiento de enlace (Interface Tracking):
-- Si el puerto hacia el Firewall (G0/24) se corta, descuenta 30 puntos de prioridad
-- para que Core 2 tome el mando de inmediato:
Switch-Core1(config-if)# standby 1 track GigabitEthernet 0/24 30
Switch-Core1(config-if)# exit


### B) En SWITCH CORE 2 (Configurar como STANDBY):

Switch-Core2(config)# interface vlan 10
Switch-Core2(config-if)# ip address 192.168.10.3 255.255.255.0
Switch-Core2(config-if)# standby version 2
Switch-Core2(config-if)# standby 1 ip 192.168.10.1
Switch-Core2(config-if)# standby 1 preempt
  -> No modificamos la prioridad (se queda en 100 por defecto, por lo que queda como Standby).
Switch-Core2(config-if)# exit



## 3. APILAMIENTO DE SWITCHES (CISCO STACKWISE / FLEXSTACK)

¿Que es Cisco StackWise?
Permite unir fisicamente hasta 9 switches mediante cables especiales de Stack en la 
parte trasera para que funcionen como UN SOLO SWITCH GIGANTE:

Ventajas:
- Una sola direccion IP de administracion para todos los switches.
- Tabla de enrutamiento y Spanning Tree unificados.
- La nomenclatura de puertos cambia a 3 digitos:
  GigabitEthernet 1/0/1 -> Switch 1, modulo 0, puerto 1.
  GigabitEthernet 2/0/1 -> Switch 2, modulo 0, puerto 1.

PASOS DE CONFIGURACION:
Paso 1: Asignar la maxima prioridad al Switch que queremos como Maestro (Master):
(La prioridad va de 1 a 15, 15 es la mas alta).
Switch-1# configure terminal
Switch-1(config)# switch 1 priority 15
Switch-1(config)# exit
Switch-1# write memory

Paso 2: En el segundo switch, cambiar su numero a Switch 2 y prioridad secundaria:
Switch-2# configure terminal
Switch-2(config)# switch 1 renumber 2
Switch-2(config)# switch 2 priority 14
Switch-2(config)# exit
Switch-2# write memory

Paso 3: Apagar ambos switches, conectar los cables de StackWise formando un bucle
cerrado, y encender primero el Switch 1 y luego el Switch 2.



## 4. VERIFICACION

- Ver estado de HSRP (muestra si el switch esta en Active o Standby):
```cisco
    Switch# show standby brief

- Ver estado de los switches del Stack (Master, Member, prioridades y estado):
    Switch# show switch

- Ver estado de los puertos fisicos del cable de apilamiento StackWise:
    Switch# show switch stack-ports
```
