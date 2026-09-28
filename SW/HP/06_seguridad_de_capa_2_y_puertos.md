# GUIA HP PROCURVE / ARUBA - PARTE 6: SEGURIDAD DE CAPA 2 (PORT SECURITY, DHCP SNOOPING Y LOOP PROTECT)


---



## 1. SEGURIDAD DE PUERTOS (PORT SECURITY)

¿Que problema resuelve?
Evita que los usuarios desconecten su equipo autorizado para conectar laptops
personales, routers personales o alterar direcciones MAC.

Configuracion en puertos de usuario (ej. puertos del 1 al 10):
```cisco
SW-HP(config)# port-security 1-10 learn-mode static address-limit 1 action close
  -> "learn-mode static": Aprende la primera direccion MAC conectada y la bloquea.
  -> "address-limit 1": Permite unicamente 1 MAC en ese puerto.
  -> "action close": Si conectan otra MAC, apaga el puerto inmediatamente.
     (Si prefieres solo generar una alerta sin apagarlo, usa: "action send-alarm").
```


## 2. DHCP SNOOPING (PROTECCION CONTRA SERVIDORES DHCP PIRATAS)

¿Que problema resuelve?
Si alguien conecta un router WiFi en la oficina, este empezara a entregar IPs
falsas a sus companeros, interrumpiendo la conexion a Internet y recursos compartidos.

Paso 1: Habilitar DHCP Snooping globalmente:
```cisco
SW-HP(config)# dhcp-snooping

Paso 2: Activar DHCP Snooping en las VLANs de usuarios:
SW-HP(config)# dhcp-snooping vlan 10,20,30

Paso 3: Marcar el puerto de subida (Uplink hacia el Router/DHCP legitimo) como CONFIABLE:
SW-HP(config)# dhcp-snooping trust 24
  -> O si es un enlace agregado LACP: "dhcp-snooping trust trk1"

-- CARACTERISTICA EXCLUSIVA DE HP (Servidor autorizado explicito):
Puedes definir la IP exacta del unico servidor DHCP autorizado en la red:
SW-HP(config)# dhcp-snooping authorized-server 192.168.100.50
```


## 3. DYNAMIC ARP PROTECTION (PROTECCION CONTRA SUPLANTACION ARP / MAN-IN-THE-MIDDLE)

¿Que problema resuelve?
Evita que un atacante envie respuestas ARP falsas para envenenar la tabla de los
equipos e interceptar contrasenas o trafico sensible.

Paso 1: Activar ARP Protection globalmente y en las VLANs:
```cisco
SW-HP(config)# arp-protect
SW-HP(config)# arp-protect vlan 10,20

Paso 2: Marcar los enlaces hacia routers o switches de confianza como CONFIABLES:
SW-HP(config)# arp-protect trust 24
```


## 4. DETECCION DE BUCLES EN EL EXTREMO DEL USUARIO (LOOP-PROTECT)

Si un usuario une con un cable dos rosetas de red o conecta un mini-switch en bucle:

Paso 1: Habilitar Loop Protect en los puertos de computadoras:
```cisco
SW-HP(config)# loop-protect 1-20

Paso 2: Auto-recuperacion tras 5 minutos (300 segundos):
SW-HP(config)# loop-protect disable-timer 300
```


## 5. VERIFICACION

- Ver estado de seguridad de puertos y que MACs estan fijadas:
```cisco
    SW-HP# show port-security

- Ver estado de DHCP Snooping y clientes vinculados:
    SW-HP# show dhcp-snooping
    SW-HP# show dhcp-snooping binding

- Ver puertos bloqueados por deteccion de bucles:
    SW-HP# show loop-protect
```
