# GUIA HUAWEI VRP - PARTE 4: ENRUTAMIENTO INTER-VLAN Y SERVIDOR DHCP LOCAL


---



## 1. ¿QUE ES EL ENRUTAMIENTO INTER-VLAN EN CAPA 3?

Por defecto, los dispositivos de la VLAN 10 NO pueden comunicarse con los de la 
VLAN 20. En un switch de Capa 3 (Switch Multicapa), el propio switch actua como
router interno utilizando sus interfaces logicas (Vlanif) como puertas de enlace
(gateways).



## 2. CONFIGURACION DE INTERFACES VLANIF COMO GATEWAYS

Escenario:
- VLAN 10 (Ventas): Red 192.168.10.0/24 -> Gateway: 192.168.10.1
- VLAN 20 (TI):     Red 192.168.20.0/24 -> Gateway: 192.168.20.1

Paso 1: Crear las VLANs
```text
[HUAWEI] vlan batch 10 20

Paso 2: Asignar IP a la interfaz de la VLAN 10
[HUAWEI] interface Vlanif 10
[HUAWEI-Vlanif10] description GATEWAY_VENTAS
[HUAWEI-Vlanif10] ip address 192.168.10.1 255.255.255.0
[HUAWEI-Vlanif10] quit

Paso 3: Asignar IP a la interfaz de la VLAN 20
[HUAWEI] interface Vlanif 20
[HUAWEI-Vlanif20] description GATEWAY_TI
[HUAWEI-Vlanif20] ip address 192.168.20.1 255.255.255.0
[HUAWEI-Vlanif20] quit

¡Listo! En este punto, cualquier paquete que viaje entre la VLAN 10 y la VLAN 20
sera enrutado directamente por el hardware del switch a velocidad de cable (wire-speed).
```


## 3. CONFIGURACION DE SERVIDOR DHCP LOCAL EN EL SWITCH

Para que los equipos conectados reciban direccion IP, mascara, gateway y DNS
automaticamente, el switch puede actuar como servidor DHCP.

Paso 1: Activar el servicio DHCP globalmente
```text
[HUAWEI] dhcp enable

Paso 2: Crear el Pool Global de Direcciones IP (Ejemplo para VLAN 10)
[HUAWEI] ip pool POOL_VENTAS
[HUAWEI-ip-pool-POOL_VENTAS] network 192.168.10.0 mask 255.255.255.0
[HUAWEI-ip-pool-POOL_VENTAS] gateway-list 192.168.10.1
[HUAWEI-ip-pool-POOL_VENTAS] dns-list 8.8.8.8 1.1.1.1
[HUAWEI-ip-pool-POOL_VENTAS] lease day 3 hour 0 minute 0     <- Tiempo de concesion: 3 dias
[HUAWEI-ip-pool-POOL_VENTAS] excluded-ip-address 192.168.10.2 192.168.10.20 <- IPs reservadas (impresoras/servidores)
[HUAWEI-ip-pool-POOL_VENTAS] quit

Paso 3: Asociar el Pool con la Interfaz VLANIF
[HUAWEI] interface Vlanif 10
[HUAWEI-Vlanif10] dhcp select global
[HUAWEI-Vlanif10] quit

-- METODO ALTERNATIVO RAPIDO (DHCP directo por Interfaz):
Si no quieres crear un pool separado, puedes activarlo directo en la Vlanif:
[HUAWEI] interface Vlanif 20
[HUAWEI-Vlanif20] dhcp select interface
[HUAWEI-Vlanif20] dhcp server dns-list 8.8.8.8 8.8.4.4
[HUAWEI-Vlanif20] quit
```


## 4. RUTAS ESTATICAS (SALIDA A INTERNET / FIREWALL)

Para que las VLANs naveguen a Internet o alcancen otras redes corporativas,
se define una ruta por defecto hacia el Router o Firewall (ejemplo: 10.0.0.1):

```text
[HUAWEI] ip route-static 0.0.0.0 0.0.0.0 10.0.0.1
```


## 5. VERIFICACION Y MONITOREO

- Ver tabla de enrutamiento del switch:
```text
    <HUAWEI> display ip routing-table

- Ver el estado y uso de las direcciones del Pool DHCP:
    <HUAWEI> display ip pool name POOL_VENTAS used

- Ver que clientes tienen una IP asignada por DHCP:
    <HUAWEI> display ip pool name POOL_VENTAS conflict
```
