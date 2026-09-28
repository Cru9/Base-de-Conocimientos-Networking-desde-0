# GUIA HUAWEI VRP - PARTE 3: CREACION DE VLANS, PUERTOS Y GESTION IP


---



## 1. ¿QUE ES UNA VLAN Y POR QUE SE UTILIZA?

Una VLAN (Virtual LAN) divide un switch fisico en multiples redes logicas aisladas.
Permite separar el trafico de diferentes departamentos (ej. Datos, Voz IP, Camaras,
Servidores) por motivos de seguridad y reduccion de tormentas de difusion (broadcast).



## 2. CREACION DE VLANS

En Huawei puedes crear una VLAN individual o en lote (batch):

-- Crear una sola VLAN con descripcion:
```text
[HUAWEI] vlan 10
[HUAWEI-vlan10] description VENTAS_DATOS
[HUAWEI-vlan10] quit

-- Crear multiples VLANs de un solo golpe (Comando muy util):
[HUAWEI] vlan batch 20 30 40 100 to 105
  -> Crea las VLANs 20, 30, 40 y el rango del 100 al 105 de forma instantanea.
```


## 3. TIPOS DE PUERTOS EN SWITCHES HUAWEI

Huawei tiene 3 modos de enlace principales en sus interfaces:


### A) ACCESS:

   - Para conectar dispositivos finales (Computadoras, Impresoras, Servidores comunes).
   - El trafico entra y sale sin etiqueta 802.1Q (Untagged). Solo pertenece a 1 VLAN.


### B) TRUNK:

   - Para conectar Switches entre si o un Switch con un Router / Firewall.
   - Pasan multiples VLANs con etiqueta 802.1Q (Tagged) a traves de un solo cable.


### C) HYBRID (Modo nativo y unico de Huawei):

   - Puede enviar tramas con o sin etiqueta para diferentes VLANs simultaneamente.
   - Es el modo por defecto de fábrica en los puertos Huawei.



## 4. CONFIGURACION DE PUERTOS ACCESS (CLIENTES FINALES)

Ejemplo: Conectar la PC de ventas al puerto GigabitEthernet 0/0/1 en la VLAN 10.

```text
[HUAWEI] interface GigabitEthernet 0/0/1
[HUAWEI-GigabitEthernet0/0/1] description PC_USUARIO_VENTAS
[HUAWEI-GigabitEthernet0/0/1] port link-type access
[HUAWEI-GigabitEthernet0/0/1] port default vlan 10
[HUAWEI-GigabitEthernet0/0/1] quit
```

-- TIP PRO: Configurar un rango de puertos a la vez usando port-group:
```text
[HUAWEI] port-group group-member GigabitEthernet 0/0/2 to GigabitEthernet 0/0/10
[HUAWEI-port-group] port link-type access
[HUAWEI-port-group] port default vlan 10
[HUAWEI-port-group] quit
```


## 5. CONFIGURACION DE PUERTOS TRUNK (ENLACES UPLINK ENTRE SWITCHES)

Ejemplo: Conectar el puerto GigabitEthernet 0/0/24 hacia el Switch Core o Router.

```text
[HUAWEI] interface GigabitEthernet 0/0/24
[HUAWEI-GigabitEthernet0/0/24] description UPLINK_HACIA_CORE
[HUAWEI-GigabitEthernet0/0/24] port link-type trunk
[HUAWEI-GigabitEthernet0/0/24] port trunk allow-pass vlan 10 20 30
  -> Solo permite el paso de las VLANs especificadas.
  -> Si quieres permitir todas: "port trunk allow-pass vlan all"
[HUAWEI-GigabitEthernet0/0/24] quit
```


## 6. ASIGNAR DIRECCION IP DE GESTION AL SWITCH (VLANIF)

Para administrar el switch remotamente por SSH/Web, se le asigna una IP a una 
interfaz logica llamada VLANIF (equivalente a SVI en Cisco):

```text
[HUAWEI] interface Vlanif 100
[HUAWEI-Vlanif100] description GESTION_ADMINISTRATIVA
[HUAWEI-Vlanif100] ip address 192.168.100.10 255.255.255.0
[HUAWEI-Vlanif100] quit

-- Configurar la Puerta de Enlace Predeterminada (Default Gateway):
[HUAWEI] ip route-static 0.0.0.0 0.0.0.0 192.168.100.1
```


## 7. COMANDOS DE DIAGNOSTICO Y VERIFICACION

- Ver todas las VLANs creadas y a que puertos estan asignadas:
```text
    <HUAWEI> display vlan

- Ver como esta configurado cada puerto a nivel de VLAN:
    <HUAWEI> display port vlan

- Ver la tabla de direcciones MAC aprendidas por el switch:
    <HUAWEI> display mac-address
```
