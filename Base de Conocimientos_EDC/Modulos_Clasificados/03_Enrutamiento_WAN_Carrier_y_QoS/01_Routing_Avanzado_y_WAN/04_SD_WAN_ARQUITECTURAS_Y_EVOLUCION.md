# 04. ARQUITECTURA SD-WAN (SOFTWARE-DEFINED WAN) Y EVOLUCION DIGITAL

> **ENRUTAMIENTO AVANZADO Y TECNOLOGIAS WAN (ROUTING & WAN ARCHITECTURE)**


---



## 1. LAS LIMITACIONES DE LA RED WAN TRADICIONAL

Durante decadas, el estandar corporativo consistio en conectar cada sucursal
mediante dos enlaces: un circuito MPLS primario costoso y un enlace de Internet
de respaldo barato.

Problemas criticos de la WAN tradicional:
1. Desperdicio de Ancho de Banda: El enlace de Internet se mantenia al 0% de uso
   (en espera pasiva) durante meses, pagandose sin ser aprovechado hasta que el
   enlace MPLS se cortaba.
2. Efecto "Trombon" (Tromboning / Backhauling Ineficiente):
   - Con la migracion a aplicaciones en la nube (Microsoft 365, Salesforce, AWS),
     las sucursales enviaban todo el trafico web por el enlace MPLS hasta el centro
     de datos central unicamente para salir a Internet desde ahi.
   - Consecuencia: Saturacion del enlace central y llamadas de Teams/Zoom con eco y congelamiento.
3. Despliegue Lento: Abrir una nueva sucursal tomaba entre 60 y 90 dias esperando
   que la compania telefonica instalara el circuito privado.



## 2. EL PARADIGMA SD-WAN (SOFTWARE-DEFINED WIDE AREA NETWORK)

SD-WAN desacopla el hardware de enrutamiento del software de gestion, permitiendo
agregar multiples conexiones de transporte independientes (Fibra, Coaxial, 5G,
Starlink y MPLS) para que operen simultaneamente como un unico canal virtual inteligente.

Arquitectura de los 4 Planos Desacoplados de SD-WAN:

| Plano | Rol y Funcion en la Arquitectura |
| :--- | :--- |
| Plano de Orquestacion | Aprovisionamiento Cero Contacto (ZTP - Zero-Touch Provisioning). |
| (Orchestration Plane) | Autentica que equipos nuevos tienen permitido unirse a la empresa. |
| Ejemplo: Cisco vBond. |  |


Plano de Gestion       Consola central unica de administracion ("Single Pane of Glass").
(Management Plane)     Permite crear politicas de seguridad y empujarlas a miles de routers
                       en 1 solo clic. Ejemplo: Cisco vManage / FortiManager.

Plano de Control       El cerebro de enrutamiento centralizado. Distribuye las rutas,
(Control Plane)        topologias y claves criptograficas de sesion a los routers.
                       Ejemplo: Cisco vSmart (Protocolo OMP - Overlay Management Protocol).

Plano de Datos         Routers fisicos o virtuales en cada sucursal (Edge Routers).
(Data Plane)           Inspeccionan y conmutan el trafico real a traves de los tuneles IPsec.
                       Ejemplo: Cisco cEdge / Fortinet FortiGate / Aruba EdgeConnect.



## 3. LA DIFERENCIA CLAVE: RED UNDERLAY vs RED OVERLAY

- Red Underlay (Subyacente):
  Es la conexion fisica real suministrada por los ISPs: Los cables de fibra de Telmex/Totalplay,
  el enlace 5G de AT&T y el circuito MPLS. Es heterogenea y no confiable.
- Red Overlay (Superpuesta):
  Es la red logica y privada formada por una malla dinamica de tuneles IPsec cifrados
  con AES-256 que se construyen ENCIMA del Underlay.
  La empresa solo administra el Overlay, abstrayendose por completo de los proveedores fisicos.



## 4. ENRUTAMIENTO BASADO EN APLICACIONES Y SLAs EN TIEMPO REAL

La mayor fortaleza de SD-WAN es su capacidad de monitorear la salud de cada enlace
cada segundo mediante sondas sinteticas BFD.

Metricas monitoreadas:
- Latencia (RTT en ms)
- Jitter (Variacion del retardo)
- Perdida de Paquetes (Packet Loss %)

Ejemplo de Politica de Aplicacion (Application-Aware Routing):
- Politica Corporativa: "El trafico de llamadas de voz IP (VoIP) requiere < 150 ms de
  latencia y menos de 1% de perdida de paquetes".
- Comportamiento Dinamico:
  1. La llamada de voz inicia viajando por el enlace de fibra optica.
  2. Si una excavadora dana un cable y la fibra comienza a experimentar microcortes
     (3% de perdida de paquetes), el router SD-WAN detecta la violacion de SLA en
     milisegundos y MUEVE LA LLAMADA DE VOZ EN TIEMPO REAL hacia el enlace 5G o satelital,
     SIN QUE LA LLAMADA SE CORTE ni los usuarios noten la caida.



## 5. ACCESO DIRECTO A INTERNET (DIA - DIRECT INTERNET ACCESS)

En lugar de enviar todo el trafico web al centro de datos:
- El router SD-WAN de la sucursal identifica la aplicacion mediante inspeccion profunda (DPI):
  * Si es trafico de Office 365, Teams o YouTube: Lo saca DIRECTAMENTE por el enlace
    de Internet local con su propio firewall integrado (Breakout local).
  * Si es trafico del sistema bancario o base de datos central: Lo enruta por el
    tunel IPsec privado hacia el Datacenter.
- Resultado: Se ahorra hasta un 70% del ancho de banda del enlace corporativo central.



## 6. COMPARATIVA DE LAS SOLUCIONES LIDERES DE LA INDUSTRIA (GARTNER MAGIC QUADRANT)


| Fabricante | Producto Principal | Fortalezas Clave |
| :--- | :--- | :--- |
| Fortinet | FortiGate Secure SD-WAN | Seguridad NGFW nativa incluida en el mismo |

                                                   dispositivo (ASIC de aceleracion de hardware).
Cisco                  Catalyst SD-WAN (Viptela)   Escalabilidad masiva para miles de sedes,
                                                   segmentacion compleja y madurez empresarial.
HPE Aruba              Aruba EdgeConnect           Optimizacion WAN avanzada (WAN Optimization),
                       (Anteriormente Silver Peak) deduplicacion de datos y aceleracion de TCP.

## Palo Alto Networks     Prisma SD-WAN (CloudGenix)  Enfoque nativo en nube y seguridad SASE integrada.
