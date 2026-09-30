# 00. INDICE GENERAL, PRINCIPIOS DE SEGURIDAD Y MATRIZ DE DEFENSA

> **CIBERSEGURIDAD EN EL MODELO OSI - GUIA MAESTRA DE DEFENSA EN PROFUNDIDAD**


---



## 1. EL PARADIGMA DE LA DEFENSA EN PROFUNDIDAD (DEFENSE-IN-DEPTH)

La premisa fundamental de la ciberseguridad moderna es: "No existe ninguna medida
de seguridad 100% infalible".

Si una organizacion concentra toda su inversion y atencion en una sola capa
(por ejemplo, comprando el Firewall perimetral mas costoso de Capa 3/4), pero
descuida la seguridad en la Capa 2 (LAN local) o en la Capa 7 (aplicaciones web),
un atacante solo necesita burlar esa unica barrera para comprometer toda la red.

La Defensa en Profundidad establece multiples barreras y controles de seguridad
escalonados a lo largo de las 7 Capas del Modelo OSI:
- Si el atacante burla el Firewall en Capa 3, es bloqueado por la inspeccion de Capa 4.
- Si el atacante penetra la red local mediante un puerto de red, es contenido por
  las defensas de Capa 2 (Port Security, 802.1X, DHCP Snooping).
- Si el atacante intercepta los cables de fibra en Capa 1, los datos estan protegidos
  por el cifrado robusto de Capa 6 (TLS / AES).



## 2. LA TRIADA CIA (CONFIDENCIALIDAD, INTEGRIDAD Y DISPONIBILIDAD) EN EL MODELO OSI

Cada capa del modelo OSI debe proteger uno o mas pilares de la Triada CIA:


| Pilar | Definicion en el Modelo OSI |
| :--- | :--- |
| Confidencialidad | Garantizar que solo los usuarios y procesos autorizados |
| (Confidentiality) | puedan leer la informacion. |
| - Capa 6: Cifrado TLS/SSL, AES-256. |  |
| - Capa 3: Tuneles IPsec VPN. |  |
| - Capa 2: Segmentacion de VLANs y cifrado MACsec. |  |


Integridad             Asegurar que los datos no hayan sido alterados, interceptados
(Integrity)            o falsificados durante el transito.
                       - Capa 7: Firmas digitales y DNSSEC.
                       - Capa 4: Numeros de secuencia TCP e ISN aleatorios.
                       - Capa 2: Dynamic ARP Inspection (DAI) y sumas FCS (CRC-32).

Disponibilidad         Asegurar que los servicios y la red permanezcan operativos
(Availability)         y accesibles ante fallas o ataques hostiles.
                       - Capa 4: Mitigacion de ataques TCP SYN Flood.
                       - Capa 2: Spanning Tree (previene colapso por bucles) y Storm Control.
                       - Capa 1: Enlaces fisicos redundantes y sistemas electricos UPS.



## 3. MAPA DE ATAQUES Y DEFENSAS POR CADA CAPA DEL MODELO OSI


| Capa OSI | Ataques Mas Frecuentes | Controles de Seguridad y Soluciones |
| :--- | :--- | :--- |
| Capa 7: Aplicacion | SQLi, XSS, CSRF, DNS Poisoning, | WAF, DNSSEC, Consultas Preparadas, |
| HTTP Flood L7, Fuerza Bruta. | MFA, Rate Limiting, Sanitizacion. |  |


Capa 6: Presentacion   SSL Stripping, Heartbleed, POODLE, TLS 1.3 estricto, HSTS Preload,
                       Insecure Deserialization, XXE.     Perfect Forward Secrecy, JSON Schema.

Capa 5: Sesion         Session Hijacking, Session Replay, Tokens JWT firmados, SIPS/SRTP,
                       SIP Toll Fraud, SMB Exploits.      Timeouts estrictos, SBC (Session Border).

Capa 4: Transporte     TCP SYN Flood, Port Scanning,      SYN Cookies, Stateful Firewalls,
                       TCP Reset Attack, UDP Amplification. Inspeccion de estado, Connection Limits.

Capa 3: Red            IP Spoofing, Smurf Attack, BGP     uRPF, ACLs de red, Autenticacion OSPF,
                       Hijacking, ICMP Floods, Ping Death. RPKI BGP, IPsec, Filtrado de Prefijos.

Capa 2: Enlace Datos   ARP Poisoning (MitM), CAM Flooding, DHCP Snooping, DAI, Port Security,
                       Rogue DHCP, VLAN Hopping, STP Loop. 802.1X, BPDU Guard, IP Source Guard.

Capa 1: Fisica         Wiretapping (pinchado de cables),  Control biometrico, Encriptacion fisica,
                       Hardware Implants (Rubber Ducky),  Bloqueadores RJ45, OTDR, Cable blindado,
                       Cortes de fibra, Rogue APs.        Deteccion de Rogue APs, CCTV.



## 4. INDICE DE ARCHIVOS DE LA CARPETA CIBERSEGURIDAD OSI

[00_INDICE_Y_DEFENSA_EN_PROFUNDIDAD.md](./00_INDICE_Y_DEFENSA_EN_PROFUNDIDAD.md)
    - Metodologia de Defensa en Profundidad, Triada CIA y mapa maestro de ataques.

[01_SEGURIDAD_CAPA_1_FISICA.md](./01_SEGURIDAD_CAPA_1_FISICA.md)
    - Pinchado de cable/fibra (Tapping), implantes de hardware fisicos (LAN Turtle,
      Rubber Ducky), esclusas y control perimetral.
    - Caso Real: Infiltracion fisica con Drop-Box en una sucursal bancaria.

[02_SEGURIDAD_CAPA_2_ENLACE_DE_DATOS.md](./02_SEGURIDAD_CAPA_2_ENLACE_DE_DATOS.md)
    - Envenenamiento ARP (Man-in-the-Middle), desbordamiento CAM, servidores DHCP piratas,
      VLAN Hopping y secuestro de Spanning Tree.
    - Caso Real: Robo masivo de credenciales en empresa de seguros via ARP Poisoning.

[03_SEGURIDAD_CAPA_3_RED.md](./03_SEGURIDAD_CAPA_3_RED.md)
    - Suplantacion IP (IP Spoofing), secuestro de rutas BGP (BGP Hijacking), ataques Smurf
      y tuneles clandestinos.
    - Caso Real: Secuestro BGP a escala global que desvio trafico de servidores DNS y criptomonedas.

[04_SEGURIDAD_CAPA_4_TRANSPORTE.md](./04_SEGURIDAD_CAPA_4_TRANSPORTE.md)
    - Inundacion TCP SYN Flood (DDoS de agotamiento de memoria), escaneos sigilosos nmap,
      ataques de reinicio RST y amplificacion UDP.
    - Caso Real: Caida critica de plataforma de comercio electronico por SYN Flood en Black Friday.

[05_SEGURIDAD_CAPA_5_SESION.md](./05_SEGURIDAD_CAPA_5_SESION.md)
    - Secuestro y fijacion de sesiones, ataques a protocolos RPC y SMB (EternalBlue),
      fraude telefonico internacional por protocolo SIP (VoIP Toll Fraud).
    - Caso Real: Fraude millonario de llamadas internacionales via PBX corporativo sin autenticar.

[06_SEGURIDAD_CAPA_6_PRESENTACION.md](./06_SEGURIDAD_CAPA_6_PRESENTACION.md)
    - Degradacion criptografica (SSL Strip, POODLE), deserializacion insegura de objetos
      (RCE), fallas de formato XML/JSON y Heartbleed.
    - Caso Real: Ejecucion Remota de Codigo (RCE) en portal corporativo via Java Deserialization.

[07_SEGURIDAD_CAPA_7_APLICACION.md](./07_SEGURIDAD_CAPA_7_APLICACION.md)
    - Vulnerabilidades OWASP Top 10: Inyeccion SQL (SQLi), Cross-Site Scripting (XSS),
      exfiltracion por DNS Tunneling y ataques de denegacion HTTP.
    - Caso Real: Fuga masiva de millones de historiales medicos via Blind SQLi y tunel DNS.

[08_MATRIZ_INTEGRAL_DE_AMENAZAS_Y_ARQUITECTURA_ZERO_TRUST.md](./08_MATRIZ_INTEGRAL_DE_AMENAZAS_Y_ARQUITECTURA_ZERO_TRUST.md)
    - Matriz de referencia rapida de 7 capas y aplicacion practica del modelo Zero Trust

## ("Nunca confies, siempre verifica").
