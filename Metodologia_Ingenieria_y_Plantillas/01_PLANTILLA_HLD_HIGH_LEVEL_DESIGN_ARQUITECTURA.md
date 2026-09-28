# 01. PLANTILLA PROFESIONAL: DISENO DE ALTO NIVEL (HLD - HIGH-LEVEL DESIGN)

> **METODOLOGIA DE INGENIERIA, PLANTILLAS Y DOCUMENTACION PROFESIONAL**


---


-------------------------------------------------------------------------------
DOCUMENTO DE ARQUITECTURA DE RED Y TELECOMUNICACIONES
TITULO DEL PROYECTO: [Nombre del Proyecto, ej. Modernizacion Core WAN y Datacenter]
EMPRESA / CLIENTE:   [Nombre de la Corporacion]
FECHA DE EMISION:    [AAAA-MM-DD]
AUTOR PRINCIPAL:     [Nombre y Titulo del Arquitecto / Ingeniero Senior]

## ESTADO:              [Borrador / En Revision / Aprobado]


CONTROL DE VERSIONES:

## Version   Fecha        Autor               Descripcion del Cambio

1.0       2026-09-26   Ing. Principal      Version inicial para revision del comite

## 1.1       2026-10-02   Arquitecto Cloud    Incorporacion de conectividad Multi-Cloud




## 1. RESUMEN EJECUTIVO (EXECUTIVE SUMMARY)

[Describir en 2 o 3 parrafos dirigidos a la direccion de TI:
 - ¿Cual es el proposito fundamental del proyecto?
 - ¿Que problemas tecnicos o de negocio actuales resuelve? (ej. lentitud de la red,
   falta de redundancia ante caidas de fibra, obsolescencia tecnologica, soporte a nueva nube).
 - ¿Cual es el beneficio tangible para la organizacion?]

Ejemplo:
"El presente proyecto define la modernizacion integral de la red de comunicaciones
de la corporacion, sustituyendo el antiguo enlace MPLS monoproveedor por una
arquitectura híbrida de Alta Disponibilidad con doble salida a Internet, balanceo BGP
y tuneles IPsec IKEv2 cifrados hacia las nubes de AWS y Microsoft Azure. Esta solucion
reduce los costos operativos en un 40% y garantiza una disponibilidad del 99.999%."



## 2. REQUERIMIENTOS Y LIMITACIONES DEL NEGOCIO (BUSINESS REQUIREMENTS)


| Requerimiento | Descripcion Tecnica | Prioridad |
| :--- | :--- | :--- |
| Disponibilidad (SLA) | Disponibilidad minima de red anual del 99.99% | Critica (Alta) |
| Tiempo de Convergencia | Conmutacion automatica ante fallas en < 1 seg | Critica |
| Seguridad de Datos | Cifrado AES-256 en todo enlace que cruce la WAN | Obligatoria |
| Presupuesto (CAPEX) | No exceder el presupuesto asignado de $150K USD | Restriccion |
| Ventana de Caida | Cero impacto en horario laboral (08:00 a 20:00) | Mandatoria |




## 3. ESTADO ACTUAL (CURRENT STATE) VS ESTADO FUTURO (TARGET ARCHITECTURE)

Estado Actual (As-Is):
- Router WAN unico (punto unico de falla - SPoF).
- Enlace MPLS simple de 50 Mbps con saturacion recurrente en horas pico.
- Enrutamiento estatico sin balanceo dinamico ni deteccion automatica de fallas.

Estado Objetivo (To-Be):
- Arquitectura Dual-CPE en cada sede principal con routers redundantes.
- Doble proveedor de Internet (ISP A Fibra Optica + ISP B Radioenlace/5G).
- Enrutamiento dinamico BGP con politicas de retorno asimetrico mitigadas y BFD subsegundo.
- Extension de la red hacia Amazon AWS y Microsoft Azure mediante Transit VPCs y C8000v.



## 4. DIAGRAMA DE ARQUITECTURA LOGICA (TARGET STATE TOPOLOGY)


```text
                        +-----------------------+
                        |      INTERNET /       |
                        |      NUBE PUBLICA     |
                        +-----------------------+
                           /                 \
                  ISP A   /                   \   ISP B
               (Primario)/                     \(Secundario)
                        v                       v
               +-----------------+     +-----------------+
               |   ROUTER WAN 1  | === |   ROUTER WAN 2  |
               | (Cisco C8300-1) | BFD | (Cisco C8300-2) |
               +-----------------+     +-----------------+
                        \                       /
                         \                     /
                     HSRP / VRRP Virtual IP: 10.10.1.1
                                   |
                                   v
                        +-----------------------+
                        |   SWITCH CORE / LAN   |
                        |  (Cisco Catalyst 9500)|
                        +-----------------------+
                                   |
                 +-----------------+-----------------+
                 |                                   |
                 v                                   v
        [ VLAN 10 - SERVIDORES ]            [ VLAN 20 - USUARIOS ]
```


## 5. SELECCION DE TECNOLOGIA Y MATRIZ DE DECISION

Se evaluaron las siguientes opciones para la conectividad de la red:
- Opcion 1: MPLS Tradicional Gestionado por Carrier.
  * Ventajas: SLA de latencia garantizado por el proveedor.
  * Desventajas: Costos excesivos por Mbps, tiempos de aprovisionamiento lentos (60-90 dias).
- Opcion 2 (SELECCIONADA): Dual-ISP Directo con IPsec BGP y Routers Propios.
  * Ventajas: Control total de la empresa sobre el enrutamiento, cifrado de extremo a extremo,
    reduccion sustancial de costos mensuales y flexibilidad multi-cloud.



## 6. ARQUITECTURA DE ENRUTAMIENTO Y DIRECCIONAMIENTO IP

- Protocolo de Enrutamiento Interno (IGP):
  OSPFv2 Multi-Area. El Backbone (Area 0) residira en el Datacenter principal;
  las sucursales remotas operaran como Areas Totally Stubby para minimizar consumo de memoria.
- Protocolo de Borde Exterior (EGP):
  BGP con Sistema Autonomo (ASN) privado 65001. Se implementara BFD (Bidirectional Forwarding
  Detection) con intervalos de 300 ms para conmutacion instantanea.
- Plan de Direccionamiento IP:
  Bloque corporativo privado RFC 1918: 10.0.0.0/8 segmentado en jerarquia /16 por sede regional.



## 7. POSTURA DE CIBERSEGURIDAD Y CONTROL DE ACCESO

- Seguridad Perimetral: Firewalls NGFW FortiGate / Palo Alto en modo cluster Activo-Pasivo.
- Inspeccion Capa 7: Activacion de antivirus de gateway, prevencion de intrusiones (IPS)
  y descifrado SSL profundo con bypass de banca y salud.
- Control de Acceso (NAC): Autenticacion 802.1X con EAP-TLS en puertos de switch mediante Cisco ISE.



## 8. MATRIZ DE RIESGOS Y ESTRATEGIA DE MITIGACION


| Riesgo Identificado | Probabilidad | Impacto | Estrategia de Mitigacion |
| :--- | :--- | :--- | :--- |
| Retraso en entrega de enlaces | Media | Alto | Contratar ISP de respaldo con despliegue 5G rapido |
| Incompatibilidad MTU en tuneles Baja | Medio | Clamping obligatorio con 'ip tcp adjust-mss 1360' |  |
| Falla humana durante migracion | Media | Critico | Obligatoriedad de aprobacion de MOP y Rollback Plan |
