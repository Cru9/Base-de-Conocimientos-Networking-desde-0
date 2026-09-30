# GUIA 3COM COMWARE - PARTE 6: SEGURIDAD DE CAPA 2 (PORT SECURITY, DHCP SNOOPING Y CONTROL DE TORMENTAS)


---



## 1. SEGURIDAD DE PUERTOS (PORT SECURITY)

¿Que problema resuelve?
Evita que un empleado desconecte su computadora de trabajo para conectar laptops
personales, routers WiFi o dispositivos no autorizados en la oficina.

Paso 1: Habilitar Port Security globalmente:
```text
[3Com] port-security enable

Paso 2: Configurar en el puerto de usuario (ej. GigabitEthernet 1/0/2):
[3Com] interface GigabitEthernet 1/0/2
[3Com-GigabitEthernet1/0/2] port-security max-mac-count 1
  -> Solo permite 1 direccion MAC en este puerto.

-- Modo AUTOLEARN (Aprende la MAC actual de la PC y la recuerda):
[3Com-GigabitEthernet1/0/2] port-security port-mode autolearn

-- Accion ante violacion (Si conectan otra MAC):
[3Com-GigabitEthernet1/0/2] port-security intrusion-mode disableport
  -> Opciones de intrusion:
     * disableport: Apaga el puerto por completo (apagado de seguridad).
     * blockmac: Bloquea unicamente a la MAC invasora sin tirar el puerto.
[3Com-GigabitEthernet1/0/2] quit
```


## 2. DHCP SNOOPING (PROTECCION CONTRA SERVIDORES DHCP PIRATAS)

¿Que problema resuelve?
Si alguien conecta un router WiFi casero en su oficina, este empezara a entregar
direcciones IP y gateways falsos a otros usuarios, cortando la navegacion.

Paso 1: Activar DHCP Snooping globalmente:
```text
[3Com] dhcp-snooping

Paso 2: Activar DHCP Snooping en las VLANs deseadas:
[3Com] vlan 10
[3Com-vlan10] dhcp-snooping enable
[3Com-vlan10] quit

Paso 3: Marcar el puerto de enlace (Uplink hacia el Router/DHCP real) como CONFIABLE:
[3Com] interface GigabitEthernet 1/0/24
[3Com-GigabitEthernet1/0/24] dhcp-snooping trust
[3Com-GigabitEthernet1/0/24] quit
  -> Todos los demas puertos bloquearan de inmediato cualquier oferta DHCP entrante.
```


## 3. CONTROL DE TORMENTAS (STORM-CONSTRAIN / SUPPRESSION)

Si una tarjeta de red rota o un bucle inunda la red con broadcast:

```text
[3Com] interface GigabitEthernet 1/0/2
-- Limitar el trafico de broadcast al 5% de la capacidad del puerto:
[3Com-GigabitEthernet1/0/2] broadcast-suppression 5
[3Com-GigabitEthernet1/0/2] multicast-suppression 5
[3Com-GigabitEthernet1/0/2] quit
```


## 4. DETECCION DE BUCLES EN EL EXTREMO DEL CLIENTE (LOOPBACK-DETECTION)

Si un usuario une con un cable dos rosetas de pared creando un bucle local:
```text
[3Com] loopback-detection enable
[3Com] interface GigabitEthernet 1/0/2
[3Com-GigabitEthernet1/0/2] loopback-detection enable
[3Com-GigabitEthernet1/0/2] loopback-detection control enable
[3Com-GigabitEthernet1/0/2] loopback-detection action shutdown
[3Com-GigabitEthernet1/0/2] quit
```


## 5. VERIFICACION

- Ver estado de seguridad de puertos:
```text
    <3Com> display port-security interface GigabitEthernet 1/0/2

- Ver tabla de asociaciones de DHCP Snooping (IP + MAC + Puerto):
    <3Com> display dhcp-snooping
```
