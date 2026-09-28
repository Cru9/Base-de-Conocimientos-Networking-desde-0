# GUIA HP PROCURVE / ARUBA - PARTE 4: ENRUTAMIENTO INTER-VLAN Y SERVIDOR DHCP LOCAL


---



## 1. ENRUTAMIENTO EN SWITCHES HP CAPA 3 (MULTICAPA)

En switches HP y Aruba con soporte de Capa 3 (ej. series 2920, 2930F, 3800, 5400R),
el switch puede comunicarse entre VLANs a maxima velocidad de hardware.

¡COMANDO OBLIGATORIO!:
Por defecto el enrutamiento esta apagado. Debes activarlo con:
```cisco
SW-HP(config)# ip routing
```


## 2. CONFIGURACION DE GATEWAYS EN MULTIPLES VLANS

Escenario:
- VLAN 10 (Ventas): Red 192.168.10.0/24 -> Gateway: 192.168.10.1
- VLAN 20 (TI):     Red 192.168.20.0/24 -> Gateway: 192.168.20.1

Paso 1: Asignar IP al Gateway de la VLAN 10:
```cisco
SW-HP(config)# vlan 10
SW-HP(vlan-10)# ip address 192.168.10.1 255.255.255.0
SW-HP(vlan-10)# exit

Paso 2: Asignar IP al Gateway de la VLAN 20:
SW-HP(config)# vlan 20
SW-HP(vlan-20)# ip address 192.168.20.1 255.255.255.0
SW-HP(vlan-20)# exit

¡Listo! Al tener "ip routing" activo y una IP en cada VLAN, el switch enrutara
el trafico de forma automatica e instantanea entre la red de Ventas y la de TI.
```


## 3. RETRANSMISION DHCP (IP HELPER-ADDRESS)

Si tienes un Servidor DHCP central en tu red (ejemplo: un servidor Windows en 192.168.100.50),
las solicitudes de IP (broadcast) de los usuarios no pasaran entre VLANs por si solas.

Para reenviar las peticiones al servidor DHCP, entra a la VLAN y coloca el helper:
```cisco
SW-HP(config)# vlan 10
SW-HP(vlan-10)# ip helper-address 192.168.100.50
SW-HP(vlan-10)# exit
```


## 4. SERVIDOR DHCP LOCAL EN EL SWITCH (ARUBAOS-S / MODELOS CAPA 3)

En modelos compatibles, el propio switch puede entregar direcciones IP:

Paso 1: Activar el servicio DHCP:
```cisco
SW-HP(config)# dhcp-server enable

Paso 2: Crear el Pool de direcciones para la VLAN 10:
SW-HP(config)# dhcp-server pool POOL_VENTAS
SW-HP(dhcp-server-pool)# network 192.168.10.0 255.255.255.0
SW-HP(dhcp-server-pool)# default-router 192.168.10.1
SW-HP(dhcp-server-pool)# dns-server 8.8.8.8 1.1.1.1
SW-HP(dhcp-server-pool)# lease 03:00:00                 <- 3 dias
SW-HP(dhcp-server-pool)# exit
```


## 5. RUTA ESTATICA PREDETERMINADA (HACIA INTERNET / FIREWALL)

Para que todo el trafico destinado hacia Internet viaje al Firewall (ej. 10.0.0.1):
```cisco
SW-HP(config)# ip route 0.0.0.0 0.0.0.0 10.0.0.1
```


## 6. COMANDOS DE VERIFICACION

- Ver la tabla de enrutamiento del switch:
```cisco
    SW-HP# show ip route

- Ver todas las direcciones IP configuradas en el switch y si el ruteo esta activo:
    SW-HP# show ip
```
