# GUIA CISCO IOS - PARTE 4: ENRUTAMIENTO INTER-VLAN Y SERVIDOR DHCP LOCAL


---



## 1. ENRUTAMIENTO EN SWITCHES DE CAPA 3 (MULTICAPA)

En un switch de Capa 3 (ej. Catalyst 3560, 3650, 3850, 9300), el propio switch 
enruta paquetes a velocidad de hardware entre diferentes VLANs.

¡COMANDO CRUCIAL OBLIGATORIO!:
Por defecto, los switches Cisco vienen con el enrutamiento desactivado. Debes encenderlo:
```cisco
Switch(config)# ip routing
```


## 2. CONFIGURACION DE INTERFACES SVI COMO GATEWAYS

Escenario:
- VLAN 10 (Ventas): Red 192.168.10.0/24 -> Gateway: 192.168.10.1
- VLAN 20 (Sistemas): Red 192.168.20.0/24 -> Gateway: 192.168.20.1

Paso 1: Crear las VLANs
```cisco
Switch(config)# vlan 10,20

Paso 2: Configurar Gateway de la VLAN 10
Switch(config)# interface vlan 10
Switch(config-if)# description GATEWAY_VENTAS
Switch(config-if)# ip address 192.168.10.1 255.255.255.0
Switch(config-if)# no shutdown
Switch(config-if)# exit

Paso 3: Configurar Gateway de la VLAN 20
Switch(config)# interface vlan 20
Switch(config-if)# description GATEWAY_SISTEMAS
Switch(config-if)# ip address 192.168.20.1 255.255.255.0
Switch(config-if)# no shutdown
Switch(config-if)# exit
```


## 3. PUERTOS ENRUTADOS (ROUTED PORTS - "NO SWITCHPORT")

¿Que es un Routed Port?
Es un puerto fisico del switch que se convierte en un puerto de Router puro.
No pertenece a ninguna VLAN y se le asigna una direccion IP directamente.
Ideal para enlaces punto a punto hacia Routers o Firewalls:

```cisco
Switch(config)# interface GigabitEthernet 0/24
Switch(config-if)# description ENLACE_PUNTO_A_PUNTO_HACIA_FIREWALL
Switch(config-if)# no switchport                    <- Desactiva Capa 2 y activa Capa 3
Switch(config-if)# ip address 10.0.0.1 255.255.255.252
Switch(config-if)# no shutdown
Switch(config-if)# exit
```


## 4. CONFIGURACION DE SERVIDOR DHCP LOCAL EN EL SWITCH

Para entregar direcciones IP automaticamente a los clientes de la VLAN 10:

Paso 1: Excluir direcciones IP fijas (Gateways, impresoras, servidores):
```cisco
Switch(config)# ip dhcp excluded-address 192.168.10.1 192.168.10.20

Paso 2: Crear el Pool DHCP y sus opciones:
Switch(config)# ip dhcp pool POOL_VENTAS
Switch(dhcp-config)# network 192.168.10.0 255.255.255.0
Switch(dhcp-config)# default-router 192.168.10.1
Switch(dhcp-config)# dns-server 8.8.8.8 1.1.1.1
Switch(dhcp-config)# lease 3                        <- Concesion por 3 dias
Switch(dhcp-config)# exit
```


## 5. AGENTE DE RETRANSMISION DHCP (IP HELPER-ADDRESS)

Si en lugar de usar el switch tienes un Servidor DHCP central dedicado
(ejemplo: Windows Server en 192.168.100.50), las solicitudes DHCP (broadcast)
no pasan entre VLANs por si solas.

Debes activar el "helper-address" en la interfaz SVI de la VLAN:
```cisco
Switch(config)# interface vlan 10
Switch(config-if)# ip helper-address 192.168.100.50
Switch(config-if)# exit
```


## 6. RUTA ESTATICA PREDETERMINADA HACIA INTERNET

Para que todo el trafico que no sea local se envie hacia el Firewall (ej. 10.0.0.2):
```cisco
Switch(config)# ip route 0.0.0.0 0.0.0.0 10.0.0.2
```


## 7. COMANDOS DE VERIFICACION

- Ver la tabla de enrutamiento del switch:
```cisco
    Switch# show ip route

- Ver que clientes y direcciones MAC tienen una IP asignada por el DHCP del switch:
    Switch# show ip dhcp binding

- Ver si hay direcciones duplicadas o conflictos en el DHCP:
    Switch# show ip dhcp conflict
```
