# 08. LISTAS DE CONTROL DE ACCESO (ACL), CALIDAD DE SERVICIO (QoS) Y MIRRORING

> **ARUBA NETWORKS (ARUBAOS-CX) - GUIA DE COMANDOS Y CONFIGURACION**


---



## 1. LISTAS DE CONTROL DE ACCESO (ACLs IPv4)

Las ACLs filtran el flujo de trafico entrante o saliente basandose en criterios
como direccion IP origen, destino, protocolo (TCP/UDP/ICMP) y puertos de servicio.

En ArubaOS-CX, las reglas utilizan numeros de secuencia (10, 20, 30...) lo que
permite insertar o eliminar reglas intermedias con total facilidad.


### a) Crear una ACL IPv4 con nombre:

```cisco
  SW-CORE-ARUBA-01(config)# access-list ip FILTRO_USUARIOS
  SW-CORE-ARUBA-01(config-acl-ip)# 10 comment Permitir acceso web seguro a servidores
  SW-CORE-ARUBA-01(config-acl-ip)# 10 permit tcp 192.168.10.0/24 10.0.0.10/32 eq 443
  SW-CORE-ARUBA-01(config-acl-ip)# 20 comment Permitir consultas DNS hacia servidor interno
  SW-CORE-ARUBA-01(config-acl-ip)# 20 permit udp 192.168.10.0/24 10.0.0.5/32 eq 53
  SW-CORE-ARUBA-01(config-acl-ip)# 30 comment Bloquear acceso a la red de Servidores Criticos
  SW-CORE-ARUBA-01(config-acl-ip)# 30 deny ip 192.168.10.0/24 10.0.0.0/24 count
  SW-CORE-ARUBA-01(config-acl-ip)# 40 comment Permitir todo el resto del trafico (ej. Internet)
  SW-CORE-ARUBA-01(config-acl-ip)# 40 permit ip any any
  SW-CORE-ARUBA-01(config-acl-ip)# exit

Nota: Por defecto, al final de toda ACL existe un 'deny ip any any' implicito.

b) Aplicar la ACL a una interfaz de VLAN (SVI):
  SW-CORE-ARUBA-01(config)# interface vlan 10
  SW-CORE-ARUBA-01(config-if-vlan)# apply access-list ip FILTRO_USUARIOS in

c) Aplicar la ACL a un puerto fisico de acceso:
  SW-CORE-ARUBA-01(config)# interface 1/1/5
  SW-CORE-ARUBA-01(config-if)# apply access-list ip FILTRO_USUARIOS in
```


## 2. CONTROL DE ACCESO AL PLANO DE CONTROL (PROTEGER EL SWITCH)

Permite que unicamente IPs autorizadas de gestion puedan conectarse por SSH/HTTPS:

```cisco
  SW-CORE-ARUBA-01(config)# access-list ip ACL_ADMIN_ONLY
  SW-CORE-ARUBA-01(config-acl-ip)# 10 permit tcp 192.168.99.50/32 any eq 22
  SW-CORE-ARUBA-01(config-acl-ip)# 20 permit tcp 192.168.99.50/32 any eq 443
  SW-CORE-ARUBA-01(config-acl-ip)# 30 deny ip any any
  SW-CORE-ARUBA-01(config-acl-ip)# exit

Aplicar al plano de gestion (Control Plane):
  SW-CORE-ARUBA-01(config)# apply access-list ip ACL_ADMIN_ONLY control-plane vrf default
```


## 3. CALIDAD DE SERVICIO (QoS) Y PRIORIZACION DE TRAFICO

Garantiza que el trafico sensible a la latencia (VoIP y Videoconferencias) tenga
prioridad sobre descargas masivas o navegacion web.


### a) Confiar en etiquetas de calidad existentes (DSCP o CoS 802.1p):

```cisco
  SW-CORE-ARUBA-01(config)# qos trust dscp
  (o: qos trust cos)

b) Limitar la velocidad de egreso en un puerto de usuario (Traffic Shaping / Rate Limit):
  Limitar a 50 Mbps de salida en el puerto 1/1/1:
  SW-CORE-ARUBA-01(config)# interface 1/1/1
  SW-CORE-ARUBA-01(config-if)# qos rate-limit egress 50000 kbps
```


## 4. MONITOREO DE PUERTOS (PORT MIRRORING / SPAN)

Copia y duplica paquetes de uno o varios puertos hacia una sonda de red o analizador
de protocolos (ej. Wireshark, IDS/IPS Snort/Suricata).

Escenario: Monitorear el trafico entrante y saliente del servidor en 1/1/10
enviando la copia a la PC con Wireshark conectada en 1/1/24.

```cisco
  SW-CORE-ARUBA-01(config)# mirror session 1
  SW-CORE-ARUBA-01(config-mirror-1)# description Monitoreo_Sonda_Wireshark
  SW-CORE-ARUBA-01(config-mirror-1)# source interface 1/1/10 both
  SW-CORE-ARUBA-01(config-mirror-1)# destination interface 1/1/24
  SW-CORE-ARUBA-01(config-mirror-1)# enable
  SW-CORE-ARUBA-01(config-mirror-1)# exit

Para pausar o deshabilitar la sesion de duplicacion:
  SW-CORE-ARUBA-01(config)# mirror session 1
  SW-CORE-ARUBA-01(config-mirror-1)# no enable
```


## 5. VERIFICACION Y COMANDOS DE DIAGNOSTICO

Visualizar todas las ACLs configuradas:
```cisco
  SW-CORE-ARUBA-01# show access-list

Visualizar una ACL especifica y el conteo de paquetes coincidentes (Hit counts):
  SW-CORE-ARUBA-01# show access-list ip FILTRO_USUARIOS
  SW-CORE-ARUBA-01# show access-list hitcounts ip FILTRO_USUARIOS

Visualizar donde esta aplicada una ACL:
  SW-CORE-ARUBA-01# show access-list summary

Visualizar el estado de la sesion de Port Mirroring:
  SW-CORE-ARUBA-01# show mirror 1

Visualizar confianza y colas de QoS:
  SW-CORE-ARUBA-01# show qos trust
```


## SW-CORE-ARUBA-01# show qos queue-statistics interface 1/1/49
