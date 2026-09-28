# 08. LISTAS DE CONTROL DE ACCESO (ACL), CALIDAD DE SERVICIO (QoS) Y MIRRORING

> **TP-LINK (JETSTREAM SWITCHES) - GUIA DE COMANDOS Y CONFIGURACION**


---



## 1. LISTAS DE CONTROL DE ACCESO (ACLs)

Las ACLs inspeccionan y filtran paquetes para controlar que trafico tiene permitido
cruzar el switch y cual debe ser bloqueado.

Tipos de ACL en TP-Link:
- MAC ACL: Filtra por direccion MAC origen/destino y tipo Ethernet (Capa 2).
- Standard IP ACL: Filtra unicamente por direccion IP origen.
- Extended IP ACL: Filtra por IP origen, IP destino, protocolo (TCP, UDP, ICMP) y puertos.



## 2. CONFIGURACION DE UNA ACL IP EXTENDIDA (PASO A PASO)

Escenario: Permitir acceso web (HTTP/HTTPS) y DNS a la red de servidores (10.0.0.0/24),
pero bloquear cualquier otro trafico desde la red de Empleados (192.168.20.0/24).

Paso 1: Crear la ACL extendida (rango 100-199 o con nombre)
```cisco
  SW-CORE-TPLINK(config)# access-list create 105 extended-ip
  SW-CORE-TPLINK(config)# access-list ip 105 rule 10 permit tcp sip 192.168.20.0 0.0.0.255 dip 10.0.0.10 0.0.0.0 d-port 443
  SW-CORE-TPLINK(config)# access-list ip 105 rule 20 permit udp sip 192.168.20.0 0.0.0.255 dip 10.0.0.5 0.0.0.0 d-port 53
  SW-CORE-TPLINK(config)# access-list ip 105 rule 30 deny ip sip 192.168.20.0 0.0.0.255 dip 10.0.0.0 0.0.0.255
  SW-CORE-TPLINK(config)# access-list ip 105 rule 40 permit ip any any

Paso 2: Vincular (Bind) la ACL a un puerto fisico o a una VLAN
  - Aplicar a un puerto especifico:
    SW-CORE-TPLINK(config)# access-list bind 105 interface gigabitEthernet 1/0/5

  - Aplicar a una VLAN completa:
    SW-CORE-TPLINK(config)# access-list bind 105 vlan 20
```


## 3. CALIDAD DE SERVICIO (QoS) Y PRIORIZACION DE TRAFICO

QoS asegura que aplicaciones criticas como voz (VoIP) y streaming de video reciban
tratamiento preferencial frente a transferencias pesadas o descargas.


### a) Modo de programacion de colas (Queue Scheduling):

  - SP (Strict Priority): Las colas de alta prioridad siempre se vacian primero.
  - WRR (Weighted Round Robin): Distribuye el ancho de banda proporcionalmente.

```cisco
  SW-CORE-TPLINK(config)# qos queue schedule wrr weight 1 2 4 8

b) Limitacion de tasa de transferencia (Port Rate Limiting):
  Limitar el trafico de entrada y salida en un puerto de usuario a 20 Mbps (20000 Kbps):
  SW-CORE-TPLINK(config)# interface gigabitEthernet 1/0/1
  SW-CORE-TPLINK(config-if)# rate-limit ingress 20000
  SW-CORE-TPLINK(config-if)# rate-limit egress 20000
  SW-CORE-TPLINK(config-if)# exit
```


## 4. MONITOREO Y DUPLICACION DE PUERTOS (PORT MIRRORING)

Permite clonar los paquetes que entran o salen de uno o varios puertos (origen)
y enviarlos a un puerto de destino donde se conecta un analizador de red (Wireshark).

Escenario: Monitorear el trafico entrante y saliente del servidor en 1/0/10
hacia la estacion de monitoreo conectada en el puerto 1/0/24.

```cisco
  SW-CORE-TPLINK(config)# monitor session 1 source interface gigabitEthernet 1/0/10 both
  SW-CORE-TPLINK(config)# monitor session 1 destination interface gigabitEthernet 1/0/24
  SW-CORE-TPLINK(config)# monitor session 1 state enable

Para detener o eliminar la sesion de duplicacion:
  SW-CORE-TPLINK(config)# no monitor session 1
```


## 5. VERIFICACION Y COMANDOS DE DIAGNOSTICO

Visualizar todas las reglas ACL configuradas:
```cisco
  SW-CORE-TPLINK# show access-list
  SW-CORE-TPLINK# show access-list 105

Visualizar donde estan vinculadas las ACLs (puertos o VLANs):
  SW-CORE-TPLINK# show access-list bind

Visualizar el estado de la sesion de Port Mirroring:
  SW-CORE-TPLINK# show monitor session 1

Visualizar estadisticas y mapeos de QoS:
  SW-CORE-TPLINK# show qos
```


## SW-CORE-TPLINK# show interface gigabitEthernet 1/0/1 rate-limit
