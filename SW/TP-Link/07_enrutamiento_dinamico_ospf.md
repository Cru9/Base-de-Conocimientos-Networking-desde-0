# 07. ENRUTAMIENTO DINAMICO AVANZADO (OSPFv2)

> **TP-LINK (JETSTREAM SWITCHES) - GUIA DE COMANDOS Y CONFIGURACION**


---



## 1. INTRODUCCION A OSPF EN CONMUTADORES TP-LINK CAPA 3

Los modelos empresariales JetStream de Capa 3 (series SG3428X, SG3452X, SX3008F,
SX3016F, etc.) implementan el protocolo OSPFv2 (Open Shortest Path First).

OSPF es un protocolo de enrutamiento dinamico por estado de enlace (Link-State)
estandar, de rapida convergencia y soporte de topologias jerarquicas basadas
en areas.



## 2. CONFIGURACION DEL PROCESO OSPF Y ROUTER-ID

Paso 1: Habilitar enrutamiento global e iniciar el proceso OSPF
```cisco
  SW-CORE-TPLINK(config)# ip routing
  SW-CORE-TPLINK(config)# router ospf 1

Paso 2: Asignar un identificador unico de enrutador (Router-ID)
  SW-CORE-TPLINK(config-router)# router-id 1.1.1.1
```


## 3. DECLARACION DE REDES Y ASIGNACION DE AREAS (AREA 0 BACKBONE)

En TP-Link JetStream, las redes se anuncian utilizando el comando 'network' con
mascara comodin (wildcard):

```cisco
  SW-CORE-TPLINK(config-router)# network 192.168.10.0 0.0.0.255 area 0
  SW-CORE-TPLINK(config-router)# network 192.168.20.0 0.0.0.255 area 0
  SW-CORE-TPLINK(config-router)# network 10.100.1.0 0.0.0.3 area 0
```


## 4. INTERFACES PASIVAS (PASSIVE-INTERFACE)

Las interfaces pasivas anuncian su red a los vecinos OSPF pero NO transmiten
ni reciben paquetes Hello (indispensable en VLANs de usuarios para evitar ataques):

```cisco
  SW-CORE-TPLINK(config-router)# passive-interface vlan 10
  SW-CORE-TPLINK(config-router)# passive-interface vlan 20
```


## 5. AUTENTICACION CRIPTOGRAFICA OSPF (MD5)

Asegura que unicamente conmutadores autorizados establezcan relaciones de vecindad:

```cisco
  SW-CORE-TPLINK(config)# interface vlan 100
  SW-CORE-TPLINK(config-if)# ip ospf authentication message-digest
  SW-CORE-TPLINK(config-if)# ip ospf message-digest-key 1 md5 ClaveSeguraOspf2026!
  SW-CORE-TPLINK(config-if)# exit
```


## 6. INYECCION DE RUTA POR DEFECTO Y REDISTRIBUCION


### a) Propagar la salida hacia Internet (Default Route) al resto de la red OSPF:

```cisco
  SW-CORE-TPLINK(config-router)# default-information originate
  (O forzar propagacion continua: default-information originate always)

b) Redistribuir rutas estaticas locales dentro de OSPF:
  SW-CORE-TPLINK(config-router)# redistribute static
  SW-CORE-TPLINK(config-router)# redistribute connected
```


## 7. AJUSTE DE METRICAS Y COSTO DE ENLACE

Para forzar al algoritmo SPF a preferir un enlace sobre otro:

```cisco
  SW-CORE-TPLINK(config)# interface vlan 100
  SW-CORE-TPLINK(config-if)# ip ospf cost 10
  SW-CORE-TPLINK(config-if)# exit
```


## 8. VERIFICACION Y COMANDOS DE DIAGNOSTICO

Visualizar vecinos OSPF detectados y su estado (debe mostrar estado 'FULL'):
```cisco
  SW-CORE-TPLINK# show ip ospf neighbor

Visualizar resumen de las interfaces participando en OSPF:
  SW-CORE-TPLINK# show ip ospf interface

Visualizar la base de datos de estado de enlace (OSPF LSDB):
  SW-CORE-TPLINK# show ip ospf database

Visualizar unicamente las rutas dinamicas aprendidas por OSPF:
  SW-CORE-TPLINK# show ip route ospf

Visualizar estadisticas generales del proceso OSPF:
```


## SW-CORE-TPLINK# show ip ospf
