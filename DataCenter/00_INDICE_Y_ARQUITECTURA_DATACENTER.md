# 00. INDICE GENERAL, EVOLUCION ARQUITECTONICA Y EL CAMBIO DE PARADIGMA

> **REDES DE CENTROS DE DATOS (DATA CENTER & CLOUD NETWORKING)**


---



## 1. LA TRANSFORMACION DEL CENTRO DE DATOS: NORTE-SUR vs ESTE-OESTE

Historicamente, los centros de datos utilizaban el diseno jerarquico de 3 capas
(Core -> Agregacion / Distribucion -> Acceso).

El cambio radical en los patrones de trafico:

### a) Trafico Norte-Sur (Tradicional):

   - Trafico que entra o sale del centro de datos (de un cliente en Internet hacia
     un servidor web).
   - En la decada de los 2000, el 80% del trafico era Norte-Sur.


### b) Trafico Este-Oeste (Moderno):

   - Trafico que fluye INTERNAMENTE entre servidores dentro del centro de datos
     (consultas de microservicios, sincronizacion de bases de datos, movimiento de
     maquinas virtuales con VMware vMotion, contenedores Kubernetes y clusters de Big Data / IA).
   - En la actualidad, ¡MAS DEL 80% DEL TRAFICO DE UN CENTRO DE DATOS ES ESTE-OESTE!

¿Por que fallo la arquitectura tradicional de 3 capas?
- El modelo tradicional dependia de Spanning Tree Protocol (STP) para evitar bucles.
- Para evitar bucles, STP BLOQUEABA la mitad de los enlaces redundantes (50% de la
  red permanecia apagada y desperdiciada).
- Si un servidor en el Rack 1 queria hablar con un servidor en el Rack 40, el tráfico
  tenia que subir hasta el switch Core y volver a bajar, generando latencias altas
  e impredecibles y cuellos de botella masivos.



## 2. TOPOLOGIA DE CABLEADO EN RACKS: ToR vs EoR


### a) ToR (Top-of-Rack - Estandar de la Industria):

   - Se instalan 1 o 2 switches de acceso dedicados en la parte superior de CADA rack.
   - Los servidores del rack se conectan con cables de cobre cortos (DAC) de 1 metro
     hacia los switches ToR.
   - Del switch ToR salen unicamente enlaces de fibra de alta velocidad hacia el Spine.
   - Ventaja: Cableado ultra-limpio, aislamiento de fallas por rack y escalabilidad.


### b) EoR (End-of-Row / MoR):

   - Los servidores de varios racks envian cientos de cables de cobre a traves de
     canaletas hasta un switch chasis masivo ubicado al final de la fila.
   - Desventaja: Pesadillas de cableado denso y dificil mantenimiento.



## 3. INDICE DE ARCHIVOS DE LA CARPETA DATACENTER

[00_INDICE_Y_ARQUITECTURA_DATACENTER.md](./00_INDICE_Y_ARQUITECTURA_DATACENTER.md)
    - El cambio de trafico Norte-Sur a Este-Oeste, limitaciones de STP y diseno de racks.

[01_ARQUITECTURA_SPINE_AND_LEAF.md](./01_ARQUITECTURA_SPINE_AND_LEAF.md)
    - La topologia Clos Spine-and-Leaf: Latencia determinista de 1 salto, eliminacion
      de Spanning Tree y balanceo masivo por hardware mediante ECMP (Equal-Cost Multi-Path).

[02_VXLAN_Y_EVPN_DATA_CENTER_FABRIC.md](./02_VXLAN_Y_EVPN_DATA_CENTER_FABRIC.md)
    - Redes superpuestas modernas: De las 4094 VLANs a los 16 millones de VNIs con VXLAN
      (encapsulado MAC-in-UDP), plano de control MP-BGP EVPN y Anycast Gateway distribuido.

[03_REDES_DE_ALMACENAMIENTO_SAN_NAS_FIBRE_CHANNEL.md](./03_REDES_DE_ALMACENAMIENTO_SAN_NAS_FIBRE_CHANNEL.md)
    - Redes de almacenamiento de alta velocidad: Fibre Channel (FC 32G/64G, Zoning, WWPN),
      FCoE sobre Ethernet sin perdida (PFC), iSCSI y la revolucion de baja latencia con RoCE.

[04_CONFIGURACION_DATACENTER_FABRIC.md](./04_CONFIGURACION_DATACENTER_FABRIC.md)
    - Laboratorio real de configuracion de una matriz Spine-Leaf con VXLAN y EVPN

para conmutadores Cisco Nexus (NX-OS) y Arista EOS.
