# GUIA 3COM COMWARE - PARTE 3: CREACION DE VLANS, PUERTOS Y GESTION IP


---



## 1. ¿QUE ES UNA VLAN Y PARA QUE SE USA?

Una VLAN divide logicamente un switch fisico en varias redes independientes.
Permite segmentar departamentos, servidores, camaras y telefonos para mejorar
la seguridad y evitar tormentas de broadcast.



## 2. CREACION DE VLANS EN 3COM

-- Crear una sola VLAN con descripcion:
```text
[3Com] vlan 10
[3Com-vlan10] description VENTAS_DATOS
[3Com-vlan10] quit

-- Crear un rango de VLANs (muy util para configuracion masiva):
[3Com] vlan 20 to 30
```


## 3. TIPOS DE PUERTOS EN 3COM COMWARE


### A) ACCESS: Para computadoras, impresoras o camaras (trafico sin etiqueta / untagged).


### B) TRUNK: Para enlaces entre switches o hacia routers (pasa multiples VLANs con etiqueta 802.1Q).


### C) HYBRID: Permite enviar tramas con o sin etiqueta para diferentes VLANs simultaneamente.




## 4. CONFIGURACION DE PUERTOS DE ACCESO (CLIENTES FINALES)

Metodo A: Configurar entrando al puerto especifico
```text
[3Com] interface GigabitEthernet 1/0/1
[3Com-GigabitEthernet1/0/1] description PC_USUARIO_VENTAS
[3Com-GigabitEthernet1/0/1] port link-type access
[3Com-GigabitEthernet1/0/1] port access vlan 10
[3Com-GigabitEthernet1/0/1] quit

Metodo B: ¡EL TRUCO MAS RAPIDO DE 3COM! (Asignar puertos desde la propia VLAN)
En lugar de entrar a cada puerto, entras a la VLAN y le agregas los puertos directamente:
[3Com] vlan 10
[3Com-vlan10] port GigabitEthernet 1/0/2 to GigabitEthernet 1/0/12
[3Com-vlan10] quit
  -> ¡Listo! Los 11 puertos pasan a la VLAN 10 en un solo comando.
```


## 5. CONFIGURACION DE PUERTOS TRONCALES (TRUNK)

Ejemplo: Configurar el puerto GigabitEthernet 1/0/24 como enlace hacia el Switch Core:

```text
[3Com] interface GigabitEthernet 1/0/24
[3Com-GigabitEthernet1/0/24] description UPLINK_HACIA_CORE
[3Com-GigabitEthernet1/0/24] port link-type trunk
-- Permitir el paso de las VLANs autorizadas (en 3Com se usa la palabra "permit"):
[3Com-GigabitEthernet1/0/24] port trunk permit vlan 10 20 30 100
  -> O permitir todas: "port trunk permit vlan all"
[3Com-GigabitEthernet1/0/24] quit
```


## 6. ASIGNAR DIRECCION IP DE GESTION AL SWITCH (VLAN-INTERFACE)

En switches 3Com, la interfaz logica virtual para administrar el switch se llama
"Vlan-interface" (equivalente a SVI en Cisco o Vlanif en Huawei):

```text
[3Com] interface Vlan-interface 100
[3Com-Vlan-interface100] description IP_ADMINISTRACION
[3Com-Vlan-interface100] ip address 192.168.100.10 255.255.255.0
[3Com-Vlan-interface100] quit

-- Configurar la Puerta de Enlace Predeterminada (Default Gateway):
[3Com] ip route-static 0.0.0.0 0.0.0.0 192.168.100.1
```


## 7. COMANDOS DE VERIFICACION

- Ver detalles de una VLAN y que puertos tiene asignados:
```text
    <3Com> display vlan 10

- Ver todas las VLANs configuradas en el switch:
    <3Com> display vlan all

- Ver como esta configurado cada puerto fisico a nivel de VLAN:
    <3Com> display port vlan

- Ver tabla de direcciones MAC aprendidas en los puertos:
    <3Com> display mac-address
```
