# 03. SEGURIDAD EN LA CAPA 3 (RED) - AMENAZAS, DEFENSAS Y CASO REAL

> **CIBERSEGURIDAD EN EL MODELO OSI - GUIA PRACTICA Y CASOS DE LA VIDA REAL**


---



## 1. PANORAMA DE SEGURIDAD EN LA CAPA DE RED

La Capa de Red es el pilar de interconexion global. Gobierna como los paquetes
cruzan fronteras entre diferentes proveedores de servicios de Internet (ISPs) y
como se enruta la informacion entre sucursales y centros de datos.

Objetivo de la Seguridad en Capa 3:
Garantizar la autenticidad del origen de los paquetes, proteger la integridad de
las tablas de enrutamiento global y aislar segmentos de red mediante politicas
de filtrado y tuneles criptograficos.



## 2. VECTORES DE ATAQUE EN CAPA 3


### a) Falsificacion de Direccion IP (IP Address Spoofing):

   - El protocolo IPv4 original no verifica si la IP que aparece en el campo
     'Source IP Address' realmente pertenece al emisor.
   - Un atacante altera los paquetes enviando una IP falsa para:
     * Saltar listas de control de acceso (ACLs) basadas en IP de confianza.
     * Lanzar ataques de reflexion / amplificacion (DDoS) donde las respuestas
       masivas de los servidores saturan a una victima inocente.


### b) Secuestro de Rutas BGP (BGP Route Hijacking):

   - El protocolo BGP (Border Gateway Protocol) que conecta los sistemas autonomos
     (AS) del mundo confia historicamente en los prefijos que cada operador anuncia.
   - Si un atacante o un ISP malicioso anuncia falsamente poseer un prefijo IP mas
     especifico (ej. anuncia una subred `/24` de un banco cuando el banco anuncia una `/22`),
     la regla de coincidencia mas larga (Longest Prefix Match) hara que todos los
     routers del planeta desvien el trafico hacia el atacante.


### c) Ataque Smurf (Amplificacion por Broadcast ICMP):

   - El atacante envia paquetes ICMP Echo Request (Ping) a la direccion de broadcast
     de una subred (`192.168.1.255`), falsificando la IP origen con la IP de la victima.
   - Cientos de computadoras responden al mismo tiempo con un Echo Reply hacia la victima,
     colapsando su enlace de telecomunicaciones.


### d) Inyeccion de Rutas Falsas en Protocolos Internos (OSPF / EIGRP / RIP):

   - Un atacante conectado a la red local levanta un proceso OSPF falso y anuncia
     una ruta por defecto con costo 1.
   - Todos los conmutadores y routers de la empresa redirigen su trafico hacia la
     laptop del atacante (agujero negro o espionaje).


### e) Fragmentacion Maliciosa (Ataques Teardrop y Tiny Fragments):

   - Manipulacion de los campos 'Fragment Offset' y 'Total Length' en el encabezado
     IPv4 con fragmentos solapados que provocan fallos de buffer y pantallas azules
     (Kernel Panic) en los routers receptores.



## 3. CONTROLES Y SOLUCIONES DE SEGURIDAD EN CAPA 3

1. Unicast Reverse Path Forwarding (uRPF - Mitigacion Definitiva de IP Spoofing):
   - El router verifica la IP origen de cada paquete entrante contra su tabla FIB:
     * uRPF Estricto (Strict Mode): El paquete solo se acepta si el router usaria
       exactamente la misma interfaz para responder hacia esa IP. Si la IP origen
       no tiene sentido que llegue por ese puerto, el router la DESCARTA de inmediato.
     * Comando Cisco: `ip verify unicast source reachable-via rx`

2. Validacion Criptografica de Rutas BGP (RPKI y ROA):
   - Resource Public Key Infrastructure (RPKI) permite firmar criptograficamente
     con certificados digitales que Sistema Autonomo (ASN) esta autorizado por los
     RIRs (ARIN, LACNIC, RIPE) para originar determinados prefijos IP (Route Origin Authorization - ROA).
   - Los routers de Internet descartan los anuncios BGP marcados como "Invalid".

3. Autenticacion Criptografica en Protocolos de Enrutamiento (OSPF / BGP):
   - Forzar que cada paquete OSPF lleve un hash HMAC-SHA256 o MD5:
     `ip ospf authentication message-digest`
     `ip ospf message-digest-key 1 md5 ClaveSegura2026`
   - BGP TTL Security Mechanism (GTSM - RFC 5082): Verifica que los paquetes BGP
     eBGP directos tengan TTL=255, bloqueando ataques lanzados desde routers remotos.

4. Desactivar Broadcasts Dirigidos (Anti-Smurf):
   - Impide que se utilicen las subredes como amplificadores de ping:
     `no ip directed-broadcast`

5. Tuneles Cifrados IPsec (Network-to-Network Encryption):
   - Cifra el paquete IP completo dentro de un encabezado ESP (Encapsulating Security
     Payload) con AES-256-GCM y autenticacion IKEv2 entre sucursales y nube.



## 4. CASO DE LA VIDA REAL: EL SECUESTRO BGP DE AMAZON DNS (MYETHERWALLET)

Escenario:
En abril de 2018, atacantes ciberneticos ejecutaron uno de los secuestros de rutas
BGP mas sonados de la historia contra el servicio DNS de Amazon (Route 53) para
robar millones de dolares a usuarios del servicio de criptomonedas MyEtherWallet.

El Ataque (Modus Operandi):
1. Los atacantes comprometieron un ISP en Europa (eNet) y comenzaron a anunciar
   por BGP los prefijos `84.16.227.0/24` y los rangos de servidores DNS de Amazon
   Route 53 (`205.251.192.0/24`), que Amazon anunciaba normalmente en bloques mas
   grandes (`/22`).
2. Grandes proveedores de transito global (como Hurricane Electric) propagaron
   el anuncio falso a traves del planeta en menos de 2 minutos.
3. Debido a la regla fundamental de enrutamiento IP (Longest Prefix Match), el
   trafico destinado a los servidores DNS de Amazon en todo el mundo fue desviado
   hacia los servidores falsos de los atacantes en Rusia.
4. Cuando los usuarios intentaban entrar a `myetherwallet.com`, el DNS falso respondio
   con la IP de un servidor clon de phishing con un certificado digital falso.
5. Los usuarios introdujeron sus claves privadas creyendo que estaban en el sitio
   oficial, y los atacantes sustrajeron mas de 17 millones de dolares en Ethereum en 2 horas.

La Solucion y Remediacion Global:
Este incidente marco un antes y un despues en la seguridad de la Capa de Red mundial:
1. Implementacion masiva de RPKI (Resource Public Key Infrastructure):
   - Los principales operadores de telecomunicaciones (Cloudflare, Tier 1 Telcos)
     activaron la validacion de origen de rutas (ROA). Con RPKI activo, los routers
     del mundo habrian catalogado el anuncio falso de eNet como "RPKI INVALID"
     y habrian rechazado la ruta de forma automatica en 0 segundos.
2. Filtrado Estricto de Prefijos en Clientes BGP (Prefix-Lists y Max-Prefix):
   - Los ISPs de transito impusieron limites estrictos para que ningun cliente pueda
     anunciar prefijos IP que no le hayan sido formalmente delegados por el registro regional.
3. Despliegue de DNSSEC (DNS Security Extensions) en la Capa 7 para que los navegadores

puedan verificar con firmas digitales si la IP devuelta por el DNS fue alterada.
