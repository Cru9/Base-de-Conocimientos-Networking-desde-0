# 08. MATRIZ INTEGRAL DE AMENAZAS Y ARQUITECTURA ZERO TRUST (NIST SP 800-207)

> **CIBERSEGURIDAD EN EL MODELO OSI - GUIA PRACTICA Y CASOS DE LA VIDA REAL**


---



## 1. MATRIZ MAESTRA DE AMENAZAS, HERRAMIENTAS Y DEFENSAS EN LAS 7 CAPAS


| Capa OSI | Amenaza Principal | Herramienta Común | Control / Tecnologia | Comando / Solucion Clave |
| :--- | :--- | :--- | :--- | :--- |
| Capa 7 | Inyeccion SQL (SQLi) SQLmap, Burp Suite Prepared Statements, | `$stmt = $pdo->prepare(...);` |  |  |
| (Aplicacion) | Cross-Site Scripting BeEF, XSSer | WAF, Content Security | `Content-Security-Policy: ...` |  |
| DNS Cache Poisoning | Kamus, Scapy | DNSSEC, DoH | `dnssec-validation auto;` |  |


Capa 6         SSL Stripping        SSLstrip           HSTS con Preload       `Strict-Transport-Security: ...`
(Presentacion) Deserializacion RCE  Ysoserial, ysoserial.net JSON Schema, No Pickle `$schema = json_decode(...);`
               Cifrados Debiles     SSLScan, Testssl   TLS 1.3 estricto, PFS  `ssl_protocols TLSv1.3;`

Capa 5         Session Hijacking    Wireshark, Dsniff  Cookies HttpOnly/Secure `Set-Cookie: ...; Secure; HttpOnly`
(Sesion)       SIP Toll Fraud       SIPVicious, Svwar  SBC, SIPS (TLS 5061)   `transport=tls`
               Ataques SMB/RPC      EternalBlue, Mimikatz Desactivar SMBv1     `Set-SmbServerConfiguration -EnableSMB1Protocol $false`

Capa 4         TCP SYN Flood        Hping3, LOIC       TCP SYN Cookies        `sysctl -w net.ipv4.tcp_syncookies=1`
(Transporte)   Port Scanning        Nmap (-sS, -sX)    Stateful Firewalls     `iptables -A INPUT -m conntrack --ctstate INVALID -j DROP`
               UDP Amplification    NTPmon, Memcrashed Rate Limiting L4       `iptables -m limit --limit 50/s`

Capa 3         IP Spoofing          Scapy, PackETH     uRPF (Strict Mode)     `ip verify unicast source reachable-via rx`
(Red)          BGP Hijacking        BGP Inquirer       RPKI / ROA Validation  `bgp rpki enable`
               Smurf Ping Flood     Hping3 -1          No Directed-Broadcast  `no ip directed-broadcast`

Capa 2         ARP Poisoning        Ettercap, Bettercap Dynamic ARP Inspection `ip arp inspection vlan 1`
(Enlace Datos) CAM Table Flooding   Macof, Dsniff      Port Security (Max 2)  `switchport port-security maximum 2`
               Rogue DHCP Server    Yersinia           DHCP Snooping          `ip dhcp snooping vlan 1`
               VLAN Hopping         Yersinia (DTP)     Desactivar DTP         `switchport nonegotiate`

Capa 1         Wiretapping / Tapping Coupler optico, Clamps Blindaje, OTDR    Cifrado Line-Rate Capa 1 (DWDM)
(Fisica)       Hardware Implants    LAN Turtle, Ducky  Control Biometrico     Esclusas, Racks con llave
               Puertos Expuestos    Conexion fisica    Bloqueadores RJ45      Cerraduras fisicas en rosetas



## 2. EL MODELO ZERO TRUST (NIST SP 800-207) EN EL MODELO OSI

El paradigma tradicional de seguridad perimetral ("castillo y foso") confiaba
ciegamente en cualquier dispositivo dentro de la red LAN corporativa.

El modelo Zero Trust ("Confianza Cero") destruye este concepto basandose en el axioma:
"NUNCA CONFIES, SIEMPRE VERIFICA" (Never Trust, Always Verify).

¿Como se implementa Zero Trust a lo largo de las 7 Capas del Modelo OSI?

Capa 1 (Fisica):
- Ningun puerto físico esta activo por defecto. Los puertos de pared en areas
  comunes estan apagados administrativamente hasta que se apruebe una solicitud formal.

Capa 2 (Enlace de Datos):
- Control de Acceso Basado en Red (IEEE 802.1X): Todo dispositivo (laptop, telefono,
  camara) debe autenticarse con certificado corporativo o identidad de usuario.
  Si la autenticacion falla, el puerto no envia una sola trama Ethernet.
- Segmentacion dinamica: El switch asigna la VLAN dinamicamente segun el rol del usuario.

Capa 3 (Red):
- Micro-segmentacion: Se abandona el concepto de "una gran red plana".
- Cada servidor o carga de trabajo (Workload) esta rodeado por un firewall logico
  (Micro-perimetro) que bloquea el movimiento lateral de un atacante (Trafico Este-Oeste).

Capa 4 (Transporte):
- Transporte Mutuamente Autenticado y Cifrado (mTLS): El cliente autentica al servidor
  y el servidor autentica al cliente mediante certificados en cada conexion TCP individual.

Capa 5 (Sesion):
- Sesiones de Corta Duracion y Evaluacion Continua: Los tokens expiran en minutos.
  Si el dispositivo cambia de red o presenta un comportamiento anomalo, la sesion
  se revoca en tiempo real forzando una nueva validacion.

Capa 6 (Presentacion):
- Cifrado Universal en Reposo y en Transito: Todo dato, base de datos y mensaje
  se almacena y transmite cifrado con algoritmos modernos (AES-256 / ChaCha20).
- Deserializacion con esquemas estrictos: Ningun dato externo se deserializa como objeto nativo.

Capa 7 (Aplicacion):
- Acceso Basado en el Contexto y Menor Privilegio (RBAC / ABAC):
  El usuario solo puede ver y ejecutar las funciones estrictamente necesarias para
  su puesto laboral, validando la postura del dispositivo (si tiene antivirus activo y parches al dia).
- Autenticacion Multifactor Obligatoria (MFA) con llaves FIDO2 resistentes al phishing.



## 3. CHECKLIST DE AUDITORIA DE SEGURIDAD INTEGRAL (7 CAPAS)

[ ] Capa 1: ¿Estan todos los armarios de telecomunicaciones (IDFs/MDFs) cerrados con llave y monitoreados por camaras?
[ ] Capa 1: ¿Estan apagados o bloqueados con tapones fisicos los puertos RJ45 de salas de juntas y pasillos?
[ ] Capa 2: ¿Tienen todos los switches habilitados DHCP Snooping, Dynamic ARP Inspection (DAI) y BPDU Guard?
[ ] Capa 2: ¿Esta desactivada la autonegociacion de troncales DTP (`nonegotiate`) en todos los puertos de acceso?
[ ] Capa 3: ¿Esta configurado uRPF (Unicast Reverse Path Forwarding) en los routers de frontera para mitigar IP Spoofing?
[ ] Capa 3: ¿Estan firmadas las rutas BGP con RPKI (ROA) y autenticados los procesos OSPF con MD5/SHA?
[ ] Capa 4: ¿Tienen todos los servidores Linux y appliances de red habilitado TCP SYN Cookies?
[ ] Capa 4: ¿Bloquean los firewalls perimetrales los paquetes TCP con combinaciones invalidas de banderas (Xmas/Null)?
```text
[ ] Capa 5: ¿Tienen todas las cookies de sesion web los atributos `HttpOnly`, `Secure` y `SameSite=Strict`?
[ ] Capa 5: ¿Estan cifradas las llamadas de telefonia IP corporativas mediante SIPS (TLS) y SRTP?
[ ] Capa 6: ¿Tienen los servidores web configurado HSTS con la opcion `preload` y desactivados los protocolos TLS 1.0 y 1.1?
[ ] Capa 6: ¿Se validan todas las entradas de datos JSON y XML contra esquemas rigurosos evitando deserializadores nativos?
[ ] Capa 7: ¿Se utilizan consultas parametrizadas (Prepared Statements) en el 100% de las consultas a bases de datos?
[ ] Capa 7: ¿Esta protegido el portal web y las APIs corporativas detras de un Web Application Firewall (WAF)?
```


## [ ] Capa 7: ¿Tienen todas las cuentas administrativas y accesos remotos VPN autenticacion multifactor (MFA)?
