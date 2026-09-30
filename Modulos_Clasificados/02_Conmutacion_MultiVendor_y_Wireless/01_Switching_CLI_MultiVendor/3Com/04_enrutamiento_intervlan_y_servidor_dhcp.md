# GUIA 3COM COMWARE - PARTE 4: ENRUTAMIENTO INTER-VLAN Y SERVIDOR DHCP LOCAL


---



## 1. ENRUTAMIENTO INTER-VLAN EN SWITCHES 3COM CAPA 3

En switches multicapa de 3Com (ej. series 4500G, 4800G, 5500G, 7700), el enrutamiento
entre VLANs viene activo por defecto. Cada interfaz Vlan-interface con direccion IP
actua como la puerta de enlace (Gateway) para los usuarios de esa red.



## 2. CONFIGURACION DE INTERFACES GATEWAY

Escenario:
- VLAN 10 (Ventas):     Red 192.168.10.0/24 -> Gateway: 192.168.10.1
- VLAN 20 (Produccion): Red 192.168.20.0/24 -> Gateway: 192.168.20.1

Paso 1: Crear las VLANs
```text
[3Com] vlan 10
[3Com-vlan10] quit
[3Com] vlan 20
[3Com-vlan20] quit

Paso 2: Asignar IP al Gateway de la VLAN 10
[3Com] interface Vlan-interface 10
[3Com-Vlan-interface10] description GATEWAY_VENTAS
[3Com-Vlan-interface10] ip address 192.168.10.1 255.255.255.0
[3Com-Vlan-interface10] quit

Paso 3: Asignar IP al Gateway de la VLAN 20
[3Com] interface Vlan-interface 20
[3Com-Vlan-interface20] description GATEWAY_PRODUCCION
[3Com-Vlan-interface20] ip address 192.168.20.1 255.255.255.0
[3Com-Vlan-interface20] quit

¡Listo! El switch ahora enrutara el trafico entre ambas VLANs sin necesidad de un router externo.
```


## 3. CONFIGURACION DE SERVIDOR DHCP LOCAL EN 3COM

Para que las computadoras conectadas reciban direccion IP y DNS automaticamente:

Paso 1: Habilitar el servicio DHCP globalmente:
```text
[3Com] dhcp enable

Paso 2: Excluir direcciones IP fijas (Gateways, impresoras, servidores):
[3Com] dhcp server forbidden-ip 192.168.10.1 192.168.10.20

Paso 3: Crear el Pool de direcciones IP (Ejemplo para VLAN 10):
[3Com] dhcp server ip-pool POOL_VENTAS
[3Com-dhcp-pool-POOL_VENTAS] network 192.168.10.0 mask 255.255.255.0
[3Com-dhcp-pool-POOL_VENTAS] gateway-list 192.168.10.1
[3Com-dhcp-pool-POOL_VENTAS] dns-list 8.8.8.8 1.1.1.1
[3Com-dhcp-pool-POOL_VENTAS] expired day 3 hour 0           <- Concesion de 3 dias
[3Com-dhcp-pool-POOL_VENTAS] quit
```


## 4. RETRANSMISION DHCP (DHCP RELAY AGENT)

Si ya tienes un servidor DHCP dedicado en tu empresa (ej. Windows Server en 192.168.100.50),
puedes hacer que el switch reenvie las peticiones DHCP hacia ese servidor:

```text
[3Com] dhcp enable
[3Com] interface Vlan-interface 10
[3Com-Vlan-interface10] dhcp select relay
[3Com-Vlan-interface10] ip relay address 192.168.100.50
[3Com-Vlan-interface10] quit
```


## 5. RUTA ESTATICA PREDETERMINADA (HACIA EL FIREWALL / INTERNET)

Para que los usuarios puedan salir a Internet enviando los paquetes al Firewall (ej. 10.0.0.1):
```text
[3Com] ip route-static 0.0.0.0 0.0.0.0 10.0.0.1
```


## 6. COMANDOS DE VERIFICACION

- Ver la tabla de enrutamiento del switch:
```text
    <3Com> display ip routing-table

- Ver el estado y uso de las direcciones del Pool DHCP:
    <3Com> display dhcp server ip-pool POOL_VENTAS

- Ver que clientes y direcciones MAC tienen una IP asignada:
    <3Com> display dhcp server free-ip
```
