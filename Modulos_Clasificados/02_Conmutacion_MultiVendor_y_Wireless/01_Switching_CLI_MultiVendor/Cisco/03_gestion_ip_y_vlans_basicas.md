# GUIA CISCO IOS - PARTE 3: CREACION DE VLANS, PUERTOS Y GESTION IP


---



## 1. ¿QUE ES UNA VLAN Y PARA QUE SE USA?

Una VLAN (Virtual Local Area Network) divide un switch fisico en multiples redes
virtuales aisladas. Por ejemplo, permite separar las computadoras de Ventas, los
telefonos de Voz IP y las Camaras de seguridad para que no interfieran entre si.



## 2. CREACION DE VLANS EN CISCO

```cisco
SW(config)# vlan 10
SW(config-vlan)# name VENTAS_DATOS
SW(config-vlan)# exit

SW(config)# vlan 20
SW(config-vlan)# name VOZ_IP
SW(config-vlan)# exit

-- Crear varias VLANs en una sola linea:
SW(config)# vlan 30,40,50,100
```


## 3. CONFIGURACION DE PUERTOS DE ACCESO (ACCESS)

Los puertos Access se usan para conectar equipos finales (Computadoras, Laptops,
Impresoras). El trafico se envia sin etiqueta 802.1Q.

-- Configurar un puerto individual:
```cisco
SW(config)# interface GigabitEthernet 0/1
SW(config-if)# description PC_USUARIO_VENTAS
SW(config-if)# switchport mode access
SW(config-if)# switchport access vlan 10
SW(config-if)# no shutdown
SW(config-if)# exit
```

-- TRUCO: Configurar un rango completo de puertos (interface range):
```cisco
SW(config)# interface range GigabitEthernet 0/2 - 12
SW(config-if-range)# switchport mode access
SW(config-if-range)# switchport access vlan 10
SW(config-if-range)# no shutdown
SW(config-if-range)# exit
```


## 4. PUERTO PARA TELEFONO IP + COMPUTADORA (VOICE VLAN)

En Cisco es muy comun conectar la computadora detras del Telefono IP usando
un solo cable de red hacia el switch:

```cisco
SW(config)# interface GigabitEthernet 0/5
SW(config-if)# description TELEFONO_IP_Y_PC
SW(config-if)# switchport mode access
SW(config-if)# switchport access vlan 10     <- Trafico de datos de la PC (Sin etiqueta)
SW(config-if)# switchport voice vlan 20      <- Trafico de voz del telefono (Con etiqueta 802.1Q)
SW(config-if)# exit
```


## 5. CONFIGURACION DE PUERTOS TRONCALES (TRUNK)

Los puertos Trunk transportan trafico de multiples VLANs entre switches o hacia un Router/Firewall.

```cisco
SW(config)# interface GigabitEthernet 0/24
SW(config-if)# description UPLINK_HACIA_SWITCH_CORE
-- En switches Catalyst serie 3560/3750 se debe indicar primero la encapsulacion:
SW(config-if)# switchport trunk encapsulation dot1q  (en series 2960/9200 ya viene por defecto)
SW(config-if)# switchport mode trunk

-- Buenas practicas de seguridad en Troncales:
SW(config-if)# switchport trunk allowed vlan 10,20,30,100  <- Solo permite pasar las VLANs autorizadas
SW(config-if)# switchport trunk native vlan 99             <- Cambia la VLAN nativa fuera de la vlan 1
SW(config-if)# switchport nonegotiate                      <- Apaga DTP (negociacion dinamica no segura)
SW(config-if)# exit
```


## 6. ASIGNAR DIRECCION IP DE GESTION AL SWITCH (SVI)

Para conectarte por SSH al switch en un switch de Capa 2, debes asignarle una IP
a una interfaz virtual SVI (Switch Virtual Interface), comunmente en la VLAN de gestion:

```cisco
SW(config)# interface vlan 100
SW(config-if)# description IP_ADMINISTRACION
SW(config-if)# ip address 192.168.100.10 255.255.255.0
SW(config-if)# no shutdown
SW(config-if)# exit

-- Configurar la Puerta de Enlace Predeterminada (Default Gateway):
SW(config)# ip default-gateway 192.168.100.1
```


## 7. COMANDOS DE VERIFICACION

- Ver todas las VLANs y puertos asignados:
```cisco
    SW# show vlan brief

- Ver el estado de todos los enlaces troncales activos:
    SW# show interfaces trunk

- Ver configuracion de Capa 2 de un puerto especifico:
    SW# show interfaces GigabitEthernet 0/1 switchport
```
