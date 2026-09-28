# 07. ENRUTAMIENTO DINAMICO AVANZADO (OSPFv2)

> **ARUBA NETWORKS (ARUBAOS-CX) - GUIA DE COMANDOS Y CONFIGURACION**


---



## 1. INTRODUCCION A OSPF EN ARUBAOS-CX

OSPF (Open Shortest Path First) es un protocolo de enrutamiento por estado de
enlace (Link-State) estandar y altamente escalable.

Caracteristica clave de ArubaOS-CX:
A diferencia de sistemas antiguos que usan comandos 'network' con mascaras wildcard,
en AOS-CX OSPF se habilita directamente dentro de cada interfaz (SVI o puerto
enrutado), brindando un control preciso y reduciendo errores humanos.



## 2. CONFIGURACION DEL PROCESO OSPF GLOBAL

Paso 1: Iniciar el proceso OSPF y fijar el Router-ID (Identificador unico)
```cisco
  SW-CORE-ARUBA-01(config)# router ospf 1
  SW-CORE-ARUBA-01(config-router-ospf)# router-id 1.1.1.1
  SW-CORE-ARUBA-01(config-router-ospf)# exit
```


## 3. ASIGNACION DE INTERFACES AL AREA DE BACKBONE (AREA 0)

Escenario: Anunciar las VLANs de usuarios como pasivas y el enlace punto a punto
hacia el router perimetral.


### a) Configurar interfaz punto a punto hacia router/firewall (Puerto L3):

```cisco
  SW-CORE-ARUBA-01(config)# interface 1/1/48
  SW-CORE-ARUBA-01(config-if)# routing
  SW-CORE-ARUBA-01(config-if)# ip address 10.100.1.2/30
  SW-CORE-ARUBA-01(config-if)# ip ospf 1 area 0.0.0.0
  SW-CORE-ARUBA-01(config-if)# ip ospf network point-to-point   (optimiza tiempos de convergencia)
  SW-CORE-ARUBA-01(config-if)# no shutdown

b) Habilitar OSPF en la VLAN 10 y configurar como interfaz pasiva:
  Una interfaz pasiva anuncia su prefijo de red a los vecinos OSPF, pero NO envia
  ni acepta paquetes Hello (evita que usuarios inyecten rutas falsas).
  SW-CORE-ARUBA-01(config)# interface vlan 10
  SW-CORE-ARUBA-01(config-if-vlan)# ip ospf 1 area 0.0.0.0
  SW-CORE-ARUBA-01(config-if-vlan)# ip ospf passive

c) Habilitar OSPF en la VLAN 20 (pasiva):
  SW-CORE-ARUBA-01(config)# interface vlan 20
  SW-CORE-ARUBA-01(config-if-vlan)# ip ospf 1 area 0.0.0.0
  SW-CORE-ARUBA-01(config-if-vlan)# ip ospf passive
```


## 4. AUTENTICACION CRIPTOGRAFICA OSPF (MD5 / SHA)

Asegura que solo dispositivos autorizados puedan establecer adyacencias OSPF:

```cisco
  SW-CORE-ARUBA-01(config)# interface 1/1/48
  SW-CORE-ARUBA-01(config-if)# ip ospf authentication message-digest
  SW-CORE-ARUBA-01(config-if)# ip ospf message-digest-key 1 md5 ClaveOspfSegura2026
```


## 5. INYECCION DE RUTA POR DEFECTO Y REDISTRIBUCION


### a) Propagar la salida hacia Internet (Default Route) hacia todos los routers OSPF:

```cisco
  SW-CORE-ARUBA-01(config)# router ospf 1
  SW-CORE-ARUBA-01(config-router-ospf)# default-information originate
  (Agregar 'always' si se desea propagar aun sin tener la ruta por defecto en tabla).

b) Redistribuir rutas estaticas o directamente conectadas a OSPF:
  SW-CORE-ARUBA-01(config-router-ospf)# redistribute static
  SW-CORE-ARUBA-01(config-router-ospf)# redistribute connected
```


## 6. AJUSTE DE METRICA Y TEMPORIZADORES (TIMERS)


### a) Modificar el costo de una ruta para preferir un enlace sobre otro:

```cisco
  SW-CORE-ARUBA-01(config)# interface 1/1/48
  SW-CORE-ARUBA-01(config-if)# ip ospf cost 10

b) Ajustar temporizadores Hello y Dead (deben coincidir en ambos extremos):
  SW-CORE-ARUBA-01(config-if)# ip ospf hello-interval 5
  SW-CORE-ARUBA-01(config-if)# ip ospf dead-interval 20
```


## 7. VERIFICACION Y COMANDOS DE DIAGNOSTICO

Visualizar vecinos OSPF y su estado de adyacencia (debe estar en 'Full'):
```cisco
  SW-CORE-ARUBA-01# show ip ospf neighbor
  SW-CORE-ARUBA-01# show ip ospf neighbor detail

Visualizar resumen de interfaces participantes en OSPF:
  SW-CORE-ARUBA-01# show ip ospf interface brief

Visualizar la base de datos de estado de enlace (OSPF LSDB):
  SW-CORE-ARUBA-01# show ip ospf database

Visualizar unicamente las rutas aprendidas via OSPF en la tabla de enrutamiento:
  SW-CORE-ARUBA-01# show ip route ospf

Visualizar contadores de trafico y estadisticas de proceso:
```


## SW-CORE-ARUBA-01# show ip ospf
