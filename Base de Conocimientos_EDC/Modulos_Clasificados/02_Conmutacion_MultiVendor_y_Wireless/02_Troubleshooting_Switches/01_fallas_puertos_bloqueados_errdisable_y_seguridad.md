# 01. PUERTOS BLOQUEADOS (ERR-DISABLED / SHUTDOWN POR SEGURIDAD Y BPDU GUARD)

> **RESOLUCION DE FALLAS (TROUBLESHOOTING DE SWITCHES)**


---



## 1. DESCRIPCION DEL PROBLEMA Y SINTOMAS

Un usuario reporta que repentinamente perdio conexion ("cable de red desconectado").
Al revisar fisicamente el switch, el LED del puerto se encuentra en color Ambar /
Naranja solido o completamente apagado.
Al consultar el CLI, el estado de la interfaz aparece como:
- En Cisco / TP-Link: 'err-disabled'
- En Huawei / 3Com: 'ERROR-DOWN' o 'Administratively Down'
- En HP ProCurve / Aruba: 'Disabled' o 'Security Disabled'



## 2. PRINCIPALES CAUSAS RAIZ


### a) Violacion de Port Security (Psecure-Violation):

   - El puerto estaba configurado para un maximo de 2 direcciones MAC.
   - El usuario conecto una laptop a traves de una docking station, o encendio
     maquinas virtuales (VMware / VirtualBox) que generan MACs virtuales nuevas,
     o conecto un switch/hub casero para compartir el cable con un companero.


### b) Disparo de BPDU Guard (BPDU-Protection):

   - El puerto tenia activado PortFast / Edge-port y BPDU Guard.
   - Alguien conecto un switch no administrado, un access point casero o un cable
     entre dos puertos de red provocando que el switch reciba tramas BPDU de Spanning
     Tree en un puerto exclusivo para clientes.


### c) Disparo de Storm Control:

   - Tormenta de difusion (Broadcast) que supero el porcentaje maximo permitido (ej. 5%).



## 3. COMANDOS DE DIAGNOSTICO POR MARCA

Para confirmar exactamente por que razon el switch bloqueo el puerto:

CISCO:
```cisco
  SW# show interfaces status err-disabled
  SW# show port-security interface GigabitEthernet 0/5
  SW# show logging | include %PM-4-ERR_DISABLE
```

HUAWEI:
```cisco
  SW> display interface brief (buscar puertos con estado 'ERROR-DOWN')
  SW> display port-security
  SW> display error-down recovery
  SW> display logbuffer | include ERROR-DOWN
```

3COM / H3C:
```cisco
  SW> display interface brief
  SW> display port-security
  SW> display logbuffer
```

HP PROCURVE:
```cisco
  SW# show interfaces brief (buscar puertos con status 'Disabled')
  SW# show port-security
  SW# show log -r | include "Security violation"
  SW# show log -r | include "BPDU"

ARUBA (AOS-CX):
  SW# show interface brief
  SW# show port-access security violation
  SW# show events -r | include "security-violation"
  SW# show events -r | include "bpdu"
```

TP-LINK JETSTREAM:
```cisco
  SW# show interface status
  SW# show port-security
  SW# show log
```


## 4. SOLUCION PASO A PASO: REACTIVACION MANUAL DEL PUERTO

Antes de reactivar el puerto, DEBE corregirse la causa (desconectar el equipo no
autorizado o el switch intruso):

Paso 1: Identificar el puerto y la MAC ofensora en el log.
Paso 2: Retirar el dispositivo causante.
Paso 3: Reiniciar administrativamente el puerto:

En Cisco / TP-Link:
```cisco
  SW(config)# interface GigabitEthernet 0/5
  SW(config-if)# shutdown
  SW(config-if)# no shutdown

En Huawei:
  SW(config)# interface GigabitEthernet 0/0/5
  SW(config-if)# shutdown
  SW(config-if)# undo shutdown

En 3Com:
  SW(config)# interface GigabitEthernet 1/0/5
  SW(config-if)# shutdown
  SW(config-if)# undo shutdown

En HP ProCurve:
  SW(config)# interface 5
  SW(config-if)# disable
  SW(config-if)# enable

En Aruba (AOS-CX):
  SW(config)# interface 1/1/5
  SW(config-if)# shutdown
  SW(config-if)# no shutdown
```


## 5. MEJOR PRACTICA DEFINITIVA: AUTORRECUPERACION (SELF-HEALING)

Para evitar que el personal de soporte de TI tenga que entrar al CLI por cada
violacion accidental, configure la recuperacion automatica tras 300 segundos:

En Cisco:
  errdisable recovery cause bpduguard
  errdisable recovery cause psecure-violation
  errdisable recovery cause storm-control
  errdisable recovery interval 300

En Huawei:
  error-down auto-recovery cause bpdu-protection interval 300
  error-down auto-recovery cause port-security interval 300
  error-down auto-recovery cause storm-control interval 300

En HP ProCurve:
  spanning-tree bpdu-protection-timeout 300

En ArubaOS-CX:
  interface 1/1/1-1/1/23
   port-access security violation recovery-timer 300

En TP-Link JetStream:
  errdisable recovery cause bpdu-guard
  errdisable recovery cause port-security

`cisco
errdisable recovery interval 300
`
