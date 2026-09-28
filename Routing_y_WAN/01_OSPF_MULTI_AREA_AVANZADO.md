# 01. OSPF MULTI-AREA AVANZADO, TIPOS DE LSAs, AREAS ESPECIALES Y BFD

> **ENRUTAMIENTO AVANZADO Y TECNOLOGIAS WAN (ROUTING & WAN ARCHITECTURE)**


---



## 1. ¿POR QUE UTILIZAR OSPF MULTI-AREA EN GRANDES REDES?

Cuando una red OSPF crece mas alla de 50 o 100 routers en una sola area (Single-Area):
- El algoritmo Dijkstra (Shortest Path First - SPF) consume demasiada memoria y CPU.
- Cada vez que una interfaz fluctua (aleteo de enlace / flapping) en cualquier sucursal,
  TODOS los routers de la empresa deben recalcular el arbol SPF completo.
- La tabla de enrutamiento se vuelve gigantesca y saturada.

Solucion: OSPF Multi-Area
- Divide la red jerarquicamente: La topologia detallada se confina dentro de cada area.
- Un cambio de enlace en el Area 10 NO fuerza el recalculo SPF en el Area 20.
- Permite la SUMARIZACION de rutas en los limites de las areas.

Regla Estructural Inviolable de OSPF:
El Area 0 (Area de Backbone o `0.0.0.0`) es el nucleo central. TODAS las demas
areas regulares deben conectarse fisicamente (o logicamente) al Area 0.



## 2. ROLES DE ROUTERS EN OSPF MULTI-AREA

- Router Interno (Internal Router): Todas sus interfaces pertenecen a una misma area.
- Router de Backbone (Backbone Router): Tiene al menos una interfaz en el Area 0.
- ABR (Area Border Router): Conecta una o mas areas al Area 0. Mantiene una base
  de datos (LSDB) independiente para cada area a la que pertenece.
- ASBR (Autonomous System Boundary Router): Router que redistribuye rutas externas
  hacia OSPF (rutas estaticas, rutas BGP o rutas de otro protocolo).



## 3. LOS 6 TIPOS DE LSAs (LINK STATE ADVERTISEMENTS) CRITICOS


| Tipo | Nombre Oficial | Generado Por | Alcance de Inundacion | Contenido |
| :--- | :--- | :--- | :--- | :--- |
| LSA 1 | Router LSA | Cada Router | Solo dentro de su area | Lista de enlaces y costos del router. |
| LSA 2 | Network LSA | El DR (Design.)Solo dentro de su area | Routers conectados en redes multiacceso. |  |
| LSA 3 | Summary LSA (Network) | El ABR | Se propaga a otras areas Anuncia redes de otra area (Inter-Area). |  |
| LSA 4 | ASBR Summary LSA | El ABR | Se propaga a otras areas Informa como llegar a la IP del ASBR. |  |
| LSA 5 | AS External LSA | El ASBR | Todo el dominio OSPF | Rutas externas redistribuidas a OSPF. |
| LSA 7 | NSSA External LSA | ASBR en NSSA | Solo dentro del NSSA | Rutas externas en areas NSSA especiales. |




## 4. TIPOS DE AREAS ESPECIALES DE OSPF (STUB, TOTALLY STUBBY, NSSA)

Diseñadas para reducir drasticamente el tamaño de la tabla de enrutamiento en
sucursales remotas con routers de menor capacidad de hardware:


### a) Area Regular (Standard Area):

   - Acepta todos los tipos de LSAs: internas (LSA 1, 2), inter-area (LSA 3, 4)
     y externas de Internet (LSA 5).


### b) Area Stub (Area Muerta):

   - Bloquea los LSAs de rutas externas (LSA 4 y LSA 5).
   - El ABR inyecta automaticamente una ruta por defecto `0.0.0.0/0` mediante un LSA 3.
   - Reduce memoria y trafico WAN.


### c) Area Totally Stubby (Exclusiva de Cisco / Estandarizada):

   - Bloquea LSAs externas (4 y 5) Y TAMBIEN bloquea las rutas de otras areas (LSA 3).
   - Los routers de la sucursal SOLO ven sus redes locales y UNA SOLA ruta por defecto:
     `0.0.0.0/0 via ABR`.


### d) Area NSSA (Not-So-Stubby Area - RFC 3101):

   - Un area Stub NO permite tener un ASBR. Si una sucursal tiene un enlace local
     a Internet o a un socio y necesita redistribuir esa ruta hacia la empresa,
     un area Stub tradicional fallaria.
   - NSSA soluciona esto: Permite tener un ASBR que inyecta la ruta externa como LSA 7.
   - El ABR de la frontera traduce el LSA 7 a LSA 5 estandar para que el Area 0 lo conozca.



## 5. SUMARIZACION DE RUTAS (ROUTE SUMMARIZATION)

La sumarizacion condensa cientos de subredes en un unico supernet, ahorrando memoria:
- Sumarizacion Inter-Area: Se ejecuta EXCLUSIVAMENTE en los ABRs:
  `area 10 range 192.168.0.0 255.255.248.0`
- Sumarizacion Externa: Se ejecuta EXCLUSIVAMENTE en los ASBRs:
  `summary-address 10.0.0.0 255.0.0.0`



## 6. ENLACES VIRTUALES (VIRTUAL LINKS)

Si por una adquisicion de empresa o un diseno temporal un area (ej. Area 20) queda
conectada al Area 10 pero NO al Area 0, OSPF no enrutara su trafico.
Un Virtual Link crea un tunel logico OSPF no cifrado a traves del Area 10 para
conectar el Area 20 directamente con el Backbone Area 0.



## 7. CONVERGENCIA ULTRARRAPIDA CON BFD (BIDIRECTIONAL FORWARDING DETECTION)

- Problema del OSPF tradicional: El temporizador Dead Timer tarda 40 segundos
  en detectar que un enlace se corto si no hay perdida de portadora fisica.
- Solucion: BFD (Bidirectional Forwarding Detection - RFC 5880).
- BFD envia micro-sondeos de hardware cada 50 o 100 milisegundos.
- Si un cable de fibra se desconecta, BFD avisa a OSPF en MENOS DE 150 MILISEGUNDOS,

conmutando el trafico a la ruta de respaldo de forma imperceptible para llamadas de voz.
