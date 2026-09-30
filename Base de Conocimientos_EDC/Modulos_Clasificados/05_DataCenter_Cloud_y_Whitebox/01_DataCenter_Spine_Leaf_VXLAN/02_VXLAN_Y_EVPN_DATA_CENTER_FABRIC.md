# 02. VXLAN Y MP-BGP EVPN (DATA CENTER FABRIC Y OVERLAY)

> **REDES DE CENTROS DE DATOS (DATA CENTER & CLOUD NETWORKING)**


---



## 1. LA CRISIS DE LAS VLANS TRADICIONALES

El estandar IEEE 802.1Q utiliza una cabecera de etiqueta de 12 bits para identificar
las VLANs. Esto limita el numero maximo a 4,094 VLANs.
En centros de datos modernos de computacion en la nube (AWS, Azure, Google Cloud o
nubes privadas empresariales basadas en VMware / OpenStack / Kubernetes):
- Cada cliente o "Tenant" requiere multiples segmentos de red aislados.
- 4,094 VLANs resultan completamente insuficientes para miles de clientes.
- Requerir extender VLANs de Capa 2 a traves de cables fisicos por todo el datacenter
  genera bucles catastroficos de STP e inestabilidad de tablas MAC.



## 2. VXLAN (VIRTUAL EXTENSIBLE LAN - RFC 7348)

VXLAN es una tecnologia de "Overlay" (red superpuesta) que encapsula tramas completas
de Capa 2 (Ethernet) dentro de paquetes de Capa 4 (UDP/IP).

Caracteristicas Principales:

### a) VNI (VXLAN Network Identifier):

   - Posee un campo identificador de 24 bits.
   - Permite crear ¡16,777,216 redes virtuales aisladas! (frente a las 4,094 de 802.1Q).


### b) Encapsulado MAC-in-UDP:

   El switch de acceso encapsula la trama del servidor en un paquete UDP estandar
   y lo enruta a traves de la red fisica IP (Underlay) hacia el switch destino.

```text
   +--------------------------------------------------------------------------+
   | Cabecera Ethernet Externa (MAC Outer)                                    | 14 bytes
   +--------------------------------------------------------------------------+
   | Cabecera IP Externa (IP Origen VTEP-A, IP Destino VTEP-B)                | 20 bytes
   +--------------------------------------------------------------------------+
   | Cabecera UDP Externa (Dst Port: 4789, Src Port: HASH L2/L3/L4 Servidor)  | 8 bytes
   +--------------------------------------------------------------------------+
   | Cabecera VXLAN (Flags + 24-bit VNI)                                      | 8 bytes
   +--------------------------------------------------------------------------+
   | TRAMA ETHERNET ORIGINAL DEL SERVIDOR                                     |
   | (MAC Dst Servidor, MAC Src Servidor, Payload Original IP/TCP...)        | 1500 bytes
   +--------------------------------------------------------------------------+
   | FCS / CRC Externo                                                        | 4 bytes
   +--------------------------------------------------------------------------+
   SOBRECARGA TOTAL (OVERHEAD) DE VXLAN: 50 a 54 Bytes adicionales.

c) Requisito Obligatorio de MTU (JUMBO FRAMES):
   Dado que VXLAN anade 50 bytes sobre el paquete original de 1500 bytes, el paquete
   resultante mide 1550 bytes. Si los conmutadores intermedios (Spines) tienen una
   MTU estandar de 1500 bytes, el paquete se fragmentara o descartara.
   -> REGLA DE ORO: La red fisica Underlay debe configurarse con Jumbo Frames:
      MTU = 9000 o 9216 bytes en todas las interfaces de los Spines y Leaves.

d) Puerto Origen Dinamico para ECMP:
   El puerto de destino UDP es siempre 4789 (estandar IANA para VXLAN).
   Sin embargo, el puerto de ORIGEN UDP se calcula mediante un Hash de la trama
   interna del servidor.
   ¿Por que? Porque los conmutadores Spines solo ven la cabecera IP/UDP externa. Al
   ver diferentes puertos UDP de origen para diferentes flujos, el balanceo ECMP
   por hardware distribuye el trafico VXLAN perfectamente a traves de todos los Spines.
```


## 3. VTEP (VXLAN TUNNEL ENDPOINT)

Un VTEP es el nodo que realiza el encapsulado y desencapsulado de las tramas VXLAN.
- Hardware VTEP: Realizado en silicio (ASIC) por el propio Leaf Switch ToR a velocidad
  de linea (Cisco Nexus CloudScale, Arista StrataXGS/Jericho, Broadcom Trident/Tomahawk).
- Software VTEP: Realizado por el hipervisor (VMware NSX-T, Open vSwitch en KVM).



## 4. EL PLANO DE CONTROL: MP-BGP EVPN (RFC 7432 / RFC 8365)

En los primeros despliegues de VXLAN no existia un plano de control inteligente. Para
descubrir direcciones MAC se utilizaba "Flood-and-Learn" apoyado en Multicast IP,
lo cual inundaba la red con peticiones ARP.

La solucion definitiva de la industria es MP-BGP EVPN (Multi-Protocol BGP Ethernet VPN):
- Sustituye el "chismorreo" de broadcast por anuncios de rutas BGP estructurados.
- Cada vez que un servidor o maquina virtual se enciende o se mueve a un Leaf, el
  Leaf aprende su MAC e IP y genera un anuncio BGP EVPN hacia los Spines (Route Reflectors).
- Todos los demas Leaves aprenden la ubicacion exacta de la maquina virtual mediante BGP.


## TIPOS DE RUTAS BGP EVPN FUNDAMENTALES:

1. Route Type 2 (MAC/IP Advertisement Route):
   - La mas importante. Publica la direccion MAC y la direccion IP de un host,
     asociandolas a un VNI y a la IP del VTEP que aloja a dicho host.
   - Habilita la "Supresion de ARP" (ARP Suppression): Cuando un host pregunta por
     una IP, el Leaf local responde directamente el ARP en hardware sin inundar la red.

2. Route Type 3 (Inclusive Multicast Ethernet Tag Route):
   - Establece la lista de VTEPs participantes para la replicacion de trafico BUM
     (Broadcast, Unknown Unicast, Multicast) usando replicacion en cascada (Ingress Replication).

3. Route Type 5 (IP Prefix Route):
   - Utilizada para enrutamiento puro inter-VRF o para anunciar subredes completas
     y rutas por defecto hacia el exterior (hacia Firewalls, WAN o Internet).



## 5. DISTRIBUTED ANYCAST GATEWAY

En redes tradicionales, el Gateway por defecto era una interfaz compartida con HSRP o
VRRP ubicada en un par de switches de agregacion. Si una VM en el Rack 50 se comunicaba
con otra subred, el trafico viajaba fisicamente hasta el Gateway activo.

Con EVPN Distributed Anycast Gateway:
- CADA Leaf Switch en todo el Datacenter tiene configurada la EXACTA MISMA direccion
  IP de Gateway y la EXACTA MISMA direccion MAC virtual (ej. 10.1.1.254, MAC 0000.5e00.0101).
- Cuando una Maquina Virtual envia un paquete a su Gateway, el paquete es enrutado
  LOCALMENTE en el switch ToR de su propio rack en el primer salto.
- Si la VM se migra en caliente (VMware vMotion) a otro rack a 100 metros de distancia:
  - Mantiene su misma direccion IP y Gateway.
  - El nuevo Leaf detecta la VM y emite un BGP EVPN Type 2 con un numero de secuencia
    superior (Mobility Sequence Number).

## - La red se actualiza en menos de 1 segundo sin interrumpir conexiones TCP activas.
