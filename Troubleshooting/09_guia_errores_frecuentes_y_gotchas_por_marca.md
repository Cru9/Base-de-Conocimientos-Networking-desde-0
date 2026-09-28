# 09. GUIA DE ERRORES FRECUENTES Y PECULIARIDADES ("GOTCHAS") POR MARCA

> **RESOLUCION DE FALLAS (TROUBLESHOOTING DE SWITCHES)**


---


Cada fabricante posee particularidades unicas de diseño en su CLI que con frecuencia
confunden incluso a ingenieros experimentados. Esta guia recopila los "gotchas"
y errores mas frustrantes de cada marca y como resolverlos de inmediato.


## 1. CISCO (IOS / IOS-XE)

Gotcha 1: "Command rejected: An interface whose trunk encapsulation is Auto cannot be configured to trunk mode"
  - Causa: En switches tradicionales (Catalyst 3560/3750), el switch rechaza el
    comando `switchport mode trunk` si no se define la encapsulacion primero.
  - Solucion:
```cisco
    SW(config-if)# switchport trunk encapsulation dot1q
    SW(config-if)# switchport mode trunk

Gotcha 2: Borrado accidental de VLANs en troncales por olvidar 'add'
  - Error: `switchport trunk allowed vlan 40` (Borra todas las demas VLANs).
  - Solucion correcta:
    SW(config-if)# switchport trunk allowed vlan add 40

Gotcha 3: Los puertos y las interfaces SVI vienen apagados por defecto
  - A diferencia de otros fabricantes, en Cisco siempre se debe ejecutar `no shutdown`
    en cada interfaz SVI (`interface vlan 1`) para que comience a operar.

Gotcha 4: El comando 'ip routing' ausente en switches L3
  - En switches multicapa de Cisco, el enrutamiento inter-VLAN no funciona hasta
    escribir `ip routing` en modo de configuracion global.
```



## 2. HUAWEI (VRP)

Gotcha 1: "Error: Please renew the default configurations to the port first"
  - Causa: En Huawei NO se puede cambiar un puerto de Trunk a Access (o viceversa)
    si el puerto todavia tiene VLANs asignadas distintas a la VLAN 1.
  - Solucion obligatoria: Primero limpiar las VLANs del puerto y luego cambiar el modo:
```text
    [Huawei-GigabitEthernet0/0/24] undo port trunk allow-pass vlan all
    [Huawei-GigabitEthernet0/0/24] undo port trunk pvid vlan
    [Huawei-GigabitEthernet0/0/24] port link-type access

Gotcha 2: Confundir 'quit' con 'return'
  - `quit`: Retrocede unicamente un nivel en la jerarquia de comandos.
  - `return`: Regresa inmediatamente a la vista de usuario inicial `<Huawei>`
    (equivalente a 'end' o Ctrl+Z en Cisco).

Gotcha 3: El comando 'display this'
  - En lugar de revisar todo el `display current-configuration` (que tiene miles de lineas),
    ingrese a la interfaz o protocolo y escriba `display this` para ver unicamente
    los comandos de esa seccion.
```



## 3. 3COM / H3C (COMWARE)

Gotcha 1: No existe 'configure terminal' ni 'enable'
  - En Comware se ingresa a configuracion con: `system-view`.

Gotcha 2: Configuracion de rangos mediante Port-Group Manual
  - En versiones clasicas de Comware, no existe 'interface range'. Se debe crear un
    grupo temporal para configurar multiples puertos a la vez:
```text
    [3Com] port-group manual GRUPO_USUARIOS
    [3Com-port-group-manual-GRUPO_USUARIOS] group-member GigabitEthernet 1/0/1 to GigabitEthernet 1/0/24
    [3Com-port-group-manual-GRUPO_USUARIOS] port link-type access

Gotcha 3: Requiere autenticacion 'scheme' para usar usuarios locales AAA
  - Si en `user-interface vty` pone `authentication-mode password`, el switch
    ignorara los usuarios creados en `local-user` y pedira una sola contrasena plana.
    Debe usar obligatoriamente: `authentication-mode scheme`.
```



## 4. HP (PROCURVE / PROVISION / ARUBAOS-S)

Gotcha 1: Filosofia centrada en la VLAN (VLAN-Centric) y no en el puerto
  - En HP ProCurve NO se entra al puerto para asignarle la VLAN. Se entra a la VLAN
    y se declaran los puertos como Tagged o Untagged:
    ProCurve(config)# vlan 20
    ProCurve(config-vlan-20)# untagged 1-10    (Puertos de acceso a VLAN 20)
    ProCurve(config-vlan-20)# tagged 24        (Puerto troncal para VLAN 20)

Gotcha 2: Bloqueo de modulos SFP de terceros
  - Los switches ProCurve rechazan transceptores no originales HP.
  - Solucion: `allow-unsupported-transceiver` y confirmar con 'y'.

Gotcha 3: Restablecimiento de credenciales sin perder configuracion
  - Presionando los orificios fisicos "Reset" y "Clear" en el panel frontal se borran
    las contrasenas olvidadas sin alterar las VLANs ni el direccionamiento IP.



## 5. ARUBA (ARUBAOS-CX)

Gotcha 1: Los puertos por defecto son de Capa 3 o Capa 2 segun el modelo
  - Para usar un puerto como switchport L2 clasico, ejecute: `no routing`.
  - Para asignarle una IP directamente como interfaz enrutada: `routing`.

Gotcha 2: Aislamiento estricto de la VRF de Gestion (vrf mgmt)
  - El puerto fisico "MGMT" pertenece a la `vrf mgmt`. Si intenta hacer un ping
    o conectar por SSH a traves de ese puerto, DEBE especificar la VRF:
```cisco
    SW# ping 192.168.1.1 vrf mgmt
    SW# ssh server vrf mgmt

Gotcha 3: Uso de Checkpoints en lugar de reiniciar
  - Antes de aplicar un cambio delicado en produccion, cree siempre un punto de
    restauracion instantaneo:
    SW# checkpoint create Antes_De_Cambios
    Si algo falla, regrese en 1 segundo sin reiniciar:
    SW# checkpoint rollback Antes_De_Cambios
```



## 6. TP-LINK (JETSTREAM)

Gotcha 1: Modo Trunk vs Modo General
  - En TP-Link, si un puerto necesita transportar varias VLANs pero ademas tener
    una VLAN sin etiquetar con PVID especifico para un Access Point Wi-Fi, debe
    usarse `switchport mode general` y no `switchport mode trunk`.

Gotcha 2: Olvido de guardar en la memoria de inicio
  - En TP-Link los comandos entran en vigor de inmediato en RAM (running-config).
    Si hay un corte de energia y el administrador no ejecuto:
    `copy running-config startup-config`

todo el trabajo se perdera al reiniciar.
