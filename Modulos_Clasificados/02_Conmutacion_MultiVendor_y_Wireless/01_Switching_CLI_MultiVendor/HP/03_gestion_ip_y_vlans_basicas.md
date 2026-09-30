# GUIA HP PROCURVE / ARUBA - PARTE 3: CREACION DE VLANS, PUERTOS Y GESTION IP


---



## 1. LA ARQUITECTURA DE VLANS EN HP (LA DIFERENCIA CON CISCO Y HUAWEI)

¡IMPORTANTE!: En Cisco y Huawei, vas al puerto y le dices que VLAN tiene.
En HP ProCurve es al reves: ENTRAS A LA VLAN y le indicas que puertos le pertenecen:

- Puerto UNTAGGED (Sin etiqueta) = Equivalente al puerto ACCESS (para computadoras).
  Un puerto solo puede ser "untagged" en UNA sola VLAN a la vez.

- Puerto TAGGED (Con etiqueta 802.1Q) = Equivalente al puerto TRUNK (para enlaces
  entre switches o hacia un router). Un puerto puede ser "tagged" en muchas VLANs.



## 2. CREACION DE VLANS Y ASIGNACION DE PUERTOS ACCESS (UNTAGGED)

Escenario: Crear la VLAN 10 para Ventas y asignarle los puertos del 1 al 12:

```cisco
SW-HP(config)# vlan 10
SW-HP(vlan-10)# name "VENTAS_DATOS"
-- Indicar que puertos van a pertenecer a esta VLAN sin etiqueta:
SW-HP(vlan-10)# untagged 1-12
SW-HP(vlan-10)# exit

* Explicacion: Al poner "untagged 1-12" en la VLAN 10, el switch los saca automaticamente
  de la VLAN 1 (VLAN por defecto) y los mete a la VLAN 10. ¡Rapido y sin rodeos!
```


## 3. CONFIGURACION DE ENLACES TRONCALES ENTRE SWITCHES (TAGGED)

Escenario: El puerto 24 es el cable que conecta con el Switch Core o Router.
Queremos que por el puerto 24 pasen las VLANs 10, 20 y 30 con etiqueta (Trunk):

```cisco
SW-HP(config)# vlan 10
SW-HP(vlan-10)# tagged 24
SW-HP(vlan-10)# exit

SW-HP(config)# vlan 20
SW-HP(vlan-20)# tagged 24
SW-HP(vlan-20)# exit

SW-HP(config)# vlan 30
SW-HP(vlan-30)# tagged 24
SW-HP(vlan-30)# exit
```


## 4. VLAN DE VOZ PARA TELEFONOS IP (VOICE VLAN)

Para que los telefonos IP envien su trafico con prioridad sobre el cable de red
donde tambien se conecta la PC:

```cisco
SW-HP(config)# vlan 20
SW-HP(vlan-20)# name "VOZ_TELEFONIA"
SW-HP(vlan-20)# voice                  <- Le indica al switch que es trafico de Voz IP
SW-HP(vlan-20)# tagged 1-12            <- El telefono enviara paquetes con etiqueta
SW-HP(vlan-20)# exit
```


## 5. ASIGNAR DIRECCION IP DE GESTION AL SWITCH

En HP ProCurve, la direccion IP se asigna DIRECTAMENTE dentro del contexto de la VLAN,
sin necesidad de crear interfaces virtuales separadas:

```cisco
SW-HP(config)# vlan 100
SW-HP(vlan-100)# name "GESTION_ADMIN"
SW-HP(vlan-100)# untagged 23
SW-HP(vlan-100)# ip address 192.168.100.10 255.255.255.0
SW-HP(vlan-100)# exit

-- Configurar la Puerta de Enlace Predeterminada (Default Gateway):
SW-HP(config)# ip default-gateway 192.168.100.1
```


## 6. COMANDOS DE DIAGNOSTICO Y VERIFICACION

- Ver resumen de todas las VLANs y su estado:
```cisco
    SW-HP# show vlans

- Ver detalle de que puertos tiene una VLAN especifica (Tagged / Untagged):
    SW-HP# show vlans 10

- Ver que VLANs estan pasando por un puerto especifico (ej. puerto 1):
    SW-HP# show vlans ports 1

- Ver configuracion IP del switch:
    SW-HP# show ip
```
