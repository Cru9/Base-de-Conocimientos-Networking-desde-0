# 06. SEGURIDAD DE CAPA 2 (PORT SECURITY, DHCP SNOOPING, DAI, STORM CONTROL)

> **ARUBA NETWORKS (ARUBAOS-CX) - GUIA DE COMANDOS Y CONFIGURACION**


---



## 1. SEGURIDAD DE PUERTO (PORT SECURITY / PORT-ACCESS)

Permite limitar la cantidad de direcciones MAC que pueden transmitir a traves de
un puerto fisico. Si un usuario conecta un switch no autorizado o clona una MAC,
el switch actua protegiendo la red.


### a) Habilitar seguridad de puerto limitando a 2 MACs:

```cisco
  SW-CORE-ARUBA-01(config)# interface 1/1/5
  SW-CORE-ARUBA-01(config-if)# port-access security
  SW-CORE-ARUBA-01(config-if)# port-access security client-limit 2
  SW-CORE-ARUBA-01(config-if)# port-access security violation action shutdown
  SW-CORE-ARUBA-01(config-if)# port-access security violation recovery-timer 300

Opciones de accion de violacion:
- shutdown: Deshabilita el puerto completamente al detectar una MAC no autorizada.
- notify: Permite el trafico pero genera una trampa SNMP y un log de alerta.
```


## 2. DHCP SNOOPING (PREVENCION DE SERVIDORES DHCP PÍRATAS O ROGUE)

Evita que atacantes o routers caseros mal configurados entreguen IPs incorrectas
y puertas de enlace falsas a los clientes de la red.
- Puertos Untrusted (No confiables): Todos los puertos de acceso de usuarios.
- Puertos Trusted (Confiables): Puertos hacia switches de distribucion o servidores DHCP.


### a) Habilitar DHCP Snooping globalmente y en las VLANs requeridas:

```cisco
  SW-CORE-ARUBA-01(config)# dhcp-snooping
  SW-CORE-ARUBA-01(config)# dhcp-snooping vlan 10,20,30

b) Configurar el puerto de uplink / servidor como CONFIABLE (Trust):
  SW-CORE-ARUBA-01(config)# interface 1/1/49
  SW-CORE-ARUBA-01(config-if)# dhcp-snooping trust
  (o en la interfaz LAG si el uplink es un agregado: interface lag 1 -> dhcp-snooping trust)
```


## 3. DYNAMIC ARP INSPECTION (DAI - INSPECCION DINAMICA DE ARP)

Previene ataques de intermediario (Man-in-the-Middle) y envenenamiento de tablas
ARP (ARP Spoofing / Poisoning). DAI valida cada solicitud y respuesta ARP contra
la base de datos de DHCP Snooping.


### a) Habilitar DAI en las VLANs correspondientes:

```cisco
  SW-CORE-ARUBA-01(config)# arp-inspection vlan 10,20,30

b) Definir puertos troncales o uplinks como confiables:
  SW-CORE-ARUBA-01(config)# interface 1/1/49
  SW-CORE-ARUBA-01(config-if)# arp-inspection trust
```


## 4. PROTECCION CONTRA TORMENTAS DE TRAFICO (STORM CONTROL)

Evita la saturacion del ancho de banda y degradacion del switch ante tormentas
de Broadcast, Multicast o Unicast Desconocido (Unknown Unicast).

Configuracion en rango de puertos de acceso (ejemplo limitando a 1% o en kbps):
```cisco
  SW-CORE-ARUBA-01(config)# interface 1/1/1-1/1/24
  SW-CORE-ARUBA-01(config-if<1/1/1-1/1/24>)# storm-control broadcast 1.0%
  SW-CORE-ARUBA-01(config-if<1/1/1-1/1/24>)# storm-control multicast 2.0%
  SW-CORE-ARUBA-01(config-if<1/1/1-1/1/24>)# storm-control unknown-unicast 1.0%
  SW-CORE-ARUBA-01(config-if<1/1/1-1/1/24>)# storm-control action notify
```


## 5. PROTECCION CONTRA BUCLES EN ACCESO (LOOP PROTECT)

Ideal para detectar bucles locales causados por usuarios que interconectan dos
rosetas o usan hubs sin soporte STP:


### a) Habilitar globalmente y en puertos:

```cisco
  SW-CORE-ARUBA-01(config)# loop-protect
  SW-CORE-ARUBA-01(config)# loop-protect vlan 10,20
  SW-CORE-ARUBA-01(config)# interface 1/1/1-1/1/24
  SW-CORE-ARUBA-01(config-if<1/1/1-1/1/24>)# loop-protect
  SW-CORE-ARUBA-01(config-if<1/1/1-1/1/24>)# loop-protect action tx-disable
  SW-CORE-ARUBA-01(config)# loop-protect re-enable-timer 180 (segundos para rehabilitar)
```


## 6. VERIFICACION Y COMANDOS DE DIAGNOSTICO

Visualizar estado de la seguridad de puertos y clientes detectados:
```cisco
  SW-CORE-ARUBA-01# show port-access security
  SW-CORE-ARUBA-01# show port-access security violation

Visualizar estado de DHCP Snooping y puertos confiables:
  SW-CORE-ARUBA-01# show dhcp-snooping

Visualizar la tabla de vinculaciones IP-MAC de DHCP Snooping (Binding Database):
  SW-CORE-ARUBA-01# show dhcp-snooping binding

Visualizar estadisticas y paquetes bloqueados por DAI:
  SW-CORE-ARUBA-01# show arp-inspection
  SW-CORE-ARUBA-01# show arp-inspection statistics

Visualizar estado y parametros de Storm Control por interfaz:
```


## SW-CORE-ARUBA-01# show storm-control
