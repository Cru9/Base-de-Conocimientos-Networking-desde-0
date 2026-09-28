# GUIA HUAWEI VRP - PARTE 6: SEGURIDAD DE CAPA 2 (PORT SECURITY, DHCP SNOOPING Y CONTROL DE TORMENTAS)


---



## 1. SEGURIDAD DE PUERTOS (PORT SECURITY / MAC FILTERING)

¿Que problema resuelve?
Evita que un usuario desconecte su PC autorizada y conecte un router personal,
otro switch, o cambie de equipo sin autorizacion.

Configuracion en un puerto de acceso:
```text
[HUAWEI] interface GigabitEthernet 0/0/2
[HUAWEI-GigabitEthernet0/0/2] port-security enable
[HUAWEI-GigabitEthernet0/0/2] port-security max-mac-num 1
  -> Solo permite 1 direccion MAC en este puerto.

-- Modo STICKY (Aprende y fija la MAC actual automaticamente):
[HUAWEI-GigabitEthernet0/0/2] port-security mac-address sticky

-- Accion ante violacion (Si conectan otra MAC no autorizada):
[HUAWEI-GigabitEthernet0/0/2] port-security protect-action shutdown
  -> Opciones:
     * shutdown: Apaga el puerto por completo hasta que el admin lo reabra.
     * restrict: Descarta los paquetes de la MAC invasora y envia una alerta/trap.
     * protect:  Descarta los paquetes silenciosamente sin mandar alertas.
[HUAWEI-GigabitEthernet0/0/2] quit
```


## 2. DHCP SNOOPING (PROTECCION CONTRA SERVIDORES DHCP PIRATAS / ROGUE)

¿Que problema resuelve?
Si un usuario conecta un router casero a la red, ese router empezara a entregar
direcciones IP incorrectas a sus companeros, tumbando la navegacion de la oficina.

DHCP Snooping divide los puertos en dos clases:
- Puertos Confiables (Trusted): Donde esta el router/servidor DHCP legitimo.
- Puertos No Confiables (Untrusted): Todos los puertos de usuarios normales (bloquea
  cualquier oferta DHCP que venga de ellos).

Paso 1: Activar el servicio globalmente
```text
[HUAWEI] dhcp enable
[HUAWEI] dhcp snooping enable

Paso 2: Activar en las VLANs deseadas
[HUAWEI] vlan 10
[HUAWEI-vlan10] dhcp snooping enable
[HUAWEI-vlan10] quit

Paso 3: Marcar el puerto Uplink (hacia el servidor o router real) como CONFIABLE
[HUAWEI] interface GigabitEthernet 0/0/24
[HUAWEI-GigabitEthernet0/0/24] dhcp snooping trusted
[HUAWEI-GigabitEthernet0/0/24] quit
```


## 3. CONTROL DE TORMENTAS (STORM CONTROL / SUPPRESSION)

¿Que problema resuelve?
Una tarjeta de red danada o un bucle local puede inundar el switch con millones
de paquetes de broadcast o multicast, ralentizando a toda la empresa.

Configuracion recomendada en puertos de usuarios:
```text
[HUAWEI] interface GigabitEthernet 0/0/2
[HUAWEI-GigabitEthernet0/0/2] broadcast-suppression 5
  -> Limita el trafico de broadcast a maximo el 5% del ancho de banda del puerto.
[HUAWEI-GigabitEthernet0/0/2] multicast-suppression 5
[HUAWEI-GigabitEthernet0/0/2] unicast-suppression 5
[HUAWEI-GigabitEthernet0/0/2] quit
```


## 4. DETECCION DE BUCLES EN EL EXTREMO DEL CLIENTE (LOOP DETECTION)

Si un usuario une con un cable dos rosetas de pared o crea un bucle en un mini-switch:
```text
[HUAWEI] loopback-detect enable
[HUAWEI] interface GigabitEthernet 0/0/2
[HUAWEI-GigabitEthernet0/0/2] loopback-detect enable
[HUAWEI-GigabitEthernet0/0/2] loopback-detect action shutdown
[HUAWEI-GigabitEthernet0/0/2] quit
```


## 5. VERIFICACION

- Ver estado de seguridad de puertos y MACs aprendidas:
```text
    <HUAWEI> display mac-address security
    <HUAWEI> display mac-address sticky

- Ver tabla de clientes identificados por DHCP Snooping (IP + MAC + Puerto):
    <HUAWEI> display dhcp snooping user-bind all
```
