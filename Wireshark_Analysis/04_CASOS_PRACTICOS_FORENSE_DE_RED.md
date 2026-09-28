# 04. CASOS PRACTICOS DE INVESTIGACION FORENSE DE RED

> **ANALISIS FORENSE DE PAQUETES CON WIRESHARK (WIRESHARK_ANALYSIS)**


---



## CASO 1: DETECCION Y RECONSTRUCCION DE UN ESCANEO DE PUERTOS Y SYN FLOOD

Escenario:
El centro de operaciones de seguridad (SOC) reporta que un servidor web critico
esta experimentando lentitud extrema y rechazos esporadicos de conexion.
Se obtiene una captura en el puerto del firewall (`captura_ataque.pcap`).

Metodologia de Analisis en Wireshark:
1. Estadisticas Globales:
   - Ir a: `Statistics -> Conversations -> Pestana IPv4`.
   - Hallazgo: Una sola IP de origen externa (ej. 203.0.113.88) ha generado mas de
     45,000 conexiones hacia el servidor en menos de 30 segundos.
2. Analisis de Flags TCP:
   - Aplicar el Display Filter:
     `ip.src == 203.0.113.88 && tcp.flags.syn == 1 && tcp.flags.ack == 0`
   - Hallazgo: Rafaga masiva de paquetes SYN dirigidos secuencialmente a los puertos
     21, 22, 23, 25, 80, 443, 3389, 8080...
   - El tamano de ventana TCP (`Window Size`) anunciado por el atacante es fijo
     (ej. 1024 bytes), tipico de herramientas automatizadas como Nmap (SYN Stealth Scan `-sS`).
3. Diagnostico Forense:
   - El atacante nunca completa el 3-way handshake (no envia el ACK final).
   - Deja las conexiones del servidor en estado `SYN_RCVD`, agotando la tabla de
     conexiones semi-abiertas (SYN Backlog Queue).
4. Accion de Mitigacion:
   - Bloquear la IP 203.0.113.88 en el firewall perimetral y habilitar `SYN Cookies`
     y `TCP Intercept` en el balanceador de carga.



## CASO 2: EXFILTRACION DE INFORMACION MEDIANTE TUNEL DNS (DNS TUNNELING)

Escenario:
Un endpoint infectado por un troyano avanzado se encuentra en una red aislada sin
acceso directo a Internet, pero con permiso para resolver nombres a traves del
servidor DNS interno de la empresa.

Metodologia de Analisis en Wireshark:
1. Inspeccion de Consultas DNS Inusuales:
   - Aplicar el Display Filter: `dns && !icmp`
   - Hallazgo: Miles de consultas DNS por segundo dirigidas a subdominios de un
     dominio extrano (`tunnel-c2.xyz`).
2. Analisis Estructural del Nombre del Dominio:
   - Nombres de consulta observados en Wireshark:
     * `bXlwYXNzd29yZDEyMw==.tunnel-c2.xyz`
     * `Y29uZmlkZW50aWFsX2RvYy5wZGY=.tunnel-c2.xyz`
   - Los subdominios estan codificados en Base64 o Hexadecimal.
3. Caracteristicas de Exfiltracion por DNS:
   - Tipo de consulta: Predominan peticiones `TXT` o `NULL` (`dns.qry.type == 16`)
     para maximizar la cantidad de datos que pueden transmitirse en la respuesta.
   - Longitud excesiva de la consulta:
     Filtro: `dns.qry.name.len > 50`
   - TTL = 0 segundos para forzar a que cada paquete llegue directamente al servidor
     del atacante sin almacenarse en la memoria cache de los servidores DNS intermedios.
4. Mitigacion:
   - Implementar un firewall de DNS con filtrado de reputacion de dominios (Cisco
     Umbrella / Palo Alto DNS Security) e inspeccion de entropia de consultas.



## CASO 3: DESCIFRADO LEGAL DE TRAFICO SSL/TLS PARA AUDITORIA DE SEGURIDAD

Problema Tradicional:
Al capturar una sesion HTTPS moderna en Wireshark, todo el trafico util se muestra
como bloques binarios ilegibles: `Application Data: Encrypted Application Data`.
Debido a los algoritmos Diffie-Hellman Efimeros (ECDHE) en TLS 1.2 y TLS 1.3, ya
no es posible descifrar el trafico simplemente subiendo la clave privada del servidor.

Solucion Estandar de la Industria: Registro de Claves Pre-Master (SSLKEYLOGFILE):
Este metodo permite a los navegadores (Chrome, Firefox, Edge) o aplicaciones exportar
las claves simetricas de sesion para que Wireshark descifre los paquetes en vivo.

Procedimiento Paso a Paso:
1. En la estacion de pruebas / analisis forense:
   - En Windows (PowerShell):
     `$env:SSLKEYLOGFILE="C:\Users\Analista\Desktop\sslkeys.log"`
     `Start-Process "chrome.exe"`
   - En Linux:
     `export SSLKEYLOGFILE=/tmp/sslkeys.log`
     `google-chrome &`
2. Configuracion en Wireshark:
   - Ir al menu superior: `Edit -> Preferences`.
   - Desplegar la seccion `Protocols` y seleccionar `TLS`.
   - En el campo `(Pre)-Master-Secret log filename`, hacer clic en `Browse` y
     seleccionar el archivo `sslkeys.log`.
   - Hacer clic en `OK`.
3. Resultado Inmediato:
   - Wireshark descifra automaticamente el trafico HTTPS en segundo plano.
   - Ahora aparece una nueva pestana `Decrypted TLS` en el panel inferior.
   - Es posible ver las solicitudes completas HTTP/1.1 y HTTP/2:
     Encabezados HTTP, Tokens de autenticacion JWT, Cookies de sesion y cargas JSON.



## CASO 4: INVESTIGACION DE SUPLANTACION DE IDENTIDAD ARP (ARP SPOOFING / MITM)

Sintoma: Usuarios reportan advertencias de certificados invalidos y conexiones caidas.

Metodologia en Wireshark:
1. Filtro Forense: `arp.duplicate-address-detected`
2. Analisis de Tramas Gratuitous ARP:
   - La IP del Gateway (192.168.1.1) tenia historicamente la MAC `00:1c:73:aa:bb:cc`.
   - De pronto, se observan tramas ARP Reply espontaneas anunciando:
     "La IP 192.168.1.1 ahora le pertenece a la MAC `b4:2e:99:11:22:33`".
   - Al buscar el fabricante de la MAC `b4:2e:99:11:22:33` en Wireshark, corresponde
     a una tarjeta de red de una estacion de trabajo no autorizada ejecutando herramientas
     como `Ettercap` o `Bettercap` para realizar un ataque Man-in-the-Middle.
3. Resolucion:
   - Desconectar el puerto del switch del atacante y habilitar Dynamic ARP Inspection

## (DAI) con DHCP Snooping en la capa de acceso.
