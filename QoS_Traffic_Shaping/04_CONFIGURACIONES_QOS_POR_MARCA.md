# 04. GUIA DE CONFIGURACION PRACTICA DE QOS MULTI-MARCA (CISCO, HUAWEI, ARUBA)

> **CALIDAD DE SERVICIO Y CONFORMACION DE TRAFICO (QOS & TRAFFIC SHAPING)**


---


Escenario Empresarial de Referencia:
- Enlace WAN contratado: 100 Mbps (sobre puerto fisico GigabitEthernet).
- Requerimientos de Trafico:
  1. Voz en Tiempo Real (DSCP EF / 46): Cola de Prioridad Estricta (LLQ) asignando 15 Mbps.
  2. Videoconferencia (DSCP AF41 / 34): Cola garantizada de 20 Mbps (CBWFQ).
  3. Datos Criticos / ERP (DSCP AF21 / 18): Cola garantizada de 30 Mbps con WRED.
  4. Resto del Trafico (Best Effort): 35 Mbps restantes con cola justa (Fair Queuing).
  5. Shaping Global en la salida WAN: Limitado a 100 Mbps exactos.



## 1. CONFIGURACION EN CISCO IOS-XE (MODULAR QOS CLI - MQC)



## PASO 1: Creacion de Clases de Trafico (Class-Maps):

class-map match-any CLASE-VOZ
  match ip dscp ef

class-map match-any CLASE-VIDEO
  match ip dscp af41

class-map match-any CLASE-DATOS-CRITICOS
  match ip dscp af21 af22


## PASO 2: Creacion de Politica de Encolamiento Hijo (Child Queuing Policy):

policy-map POLITICA-COLAS-HIJO
  class CLASE-VOZ
    priority 15000               ! Cola de Prioridad Estricta LLQ de 15 Mbps con policer
  class CLASE-VIDEO
    bandwidth 20000              ! Cola garantizada CBWFQ de 20 Mbps
  class CLASE-DATOS-CRITICOS
    bandwidth 30000              ! Cola garantizada de 30 Mbps
    random-detect dscp-based     ! Habilitacion de WRED para evitar congestion TCP
  class class-default
    fair-queue                   ! Cola justa para el trafico general de datos


## PASO 3: Jerarquia de Politica con Shaping Padre (Hierarchical QoS - HQoS):

policy-map POLITICA-SHAPING-PADRE
  class class-default
    shape average 100000000      ! Conformacion a 100 Mbps (ancho de banda del ISP)
    service-policy POLITICA-COLAS-HIJO  ! Inyeccion de las colas dentro del Shaper


## PASO 4: Aplicacion a la Interfaz WAN de Salida:

```text
interface GigabitEthernet0/0/1
  description ENLACE-WAN-HACIA-ISP
  service-policy output POLITICA-SHAPING-PADRE
```



## 2. CONFIGURACION EN HUAWEI VRP (TRAFFIC POLICY)



## PASO 1: Definicion de Clasificadores de Trafico:

traffic classifier CLASIF_VOZ operator or
  if-match dscp ef

traffic classifier CLASIF_VIDEO operator or
  if-match dscp af41

traffic classifier CLASIF_DATOS operator or
  if-match dscp af21


## PASO 2: Definicion de Comportamientos de Trafico (Behaviors):

traffic behavior BEHAV_VOZ
  queue ef bandwidth 15000 cbs 375000   ! LLQ para voz (15 Mbps)

traffic behavior BEHAV_VIDEO
  queue af bandwidth 20000             ! CBWFQ para video (20 Mbps)

traffic behavior BEHAV_DATOS
  queue af bandwidth 30000             ! CBWFQ para datos (30 Mbps)
  wred dscp                            ! WRED basado en DSCP


## PASO 3: Integracion en Politica y Aplicacion:

traffic policy POLITICA_QOS_WAN
  classifier CLASIF_VOZ behavior BEHAV_VOZ
  classifier CLASIF_VIDEO behavior BEHAV_VIDEO
  classifier CLASIF_DATOS behavior BEHAV_DATOS

```text
interface GigabitEthernet0/0/1
  description UPLINK-WAN-ISP
  qos lr outbound cir 100000 cbs 2500000  ! Line Rate / Shaping a 100 Mbps
  traffic-policy POLITICA_QOS_WAN outbound
```



## 3. CONFIGURACION EN ARUBAOS-CX (AOS-CX)


En conmutadores ArubaOS-CX, la planificacion de colas se realiza asociando perfiles
de colas de hardware (Hardware Queues 0 a 7):
- Cola 7: Prioridad Estricta (Strict Priority - Voz).
- Colas 0-6: DWRR (Deficit Weighted Round Robin).

qos queue-profile PERFIL-COLAS-CORP
  queue 7 name VOZ
  queue 6 name VIDEO
  queue 5 name DATOS-CRITICOS
  queue 0 name BEST-EFFORT

qos schedule-profile PERFIL-PLANIFICACION-CORP
  strict priority queue 7
  dwrr queue 6 weight 25
  dwrr queue 5 weight 35
  dwrr queue 0 weight 40

! Aplicar globalmente al hardware
apply qos queue-profile PERFIL-COLAS-CORP
apply qos schedule-profile PERFIL-PLANIFICACION-CORP



## 4. COMANDOS DE VERIFICACION Y MONITOREO EN VIVO


En Cisco IOS-XE:
- `show policy-map interface GigabitEthernet0/0/1`
  -> Muestra paquetes transmitidos, paquetes descartados por la cola LLQ y caidas por WRED.
- `show queueing interface GigabitEthernet0/0/1`
  -> Estado de ocupacion de los buffers de memoria en tiempo real.

En Huawei VRP:
- `display traffic-policy applied-record`
  -> Verifica en que interfaces se encuentra activa la politica de QoS.
- `display qos queue statistics interface GigabitEthernet0/0/1`

## -> Estadisticas de bytes enviados y descartados por cada una de las 8 colas.
