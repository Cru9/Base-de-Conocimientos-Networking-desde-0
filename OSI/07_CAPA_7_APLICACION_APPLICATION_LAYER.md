# 07. CAPA 7: CAPA DE APLICACION (APPLICATION LAYER) - PROTOCOLOS Y SERVICIOS

> **MODELO OSI (OPEN SYSTEMS INTERCONNECTION) - GUIA MAESTRA PARA CERTIFICACIONES**  
> *Guía de referencia técnica y preparación para certificaciones Cisco CCNA 200-301, CompTIA Network+ y Huawei HCIA.*

---


## 1. FUNCION Y PROPOSITO DE LA CAPA DE APLICACION

La Capa de Aplicacion es la capa superior del modelo OSI y la mas cercana al usuario.
Actua como la interfaz directa entre los programas de software instalados en la
computadora y los servicios de comunicacion de la red.

¡DISTINCION FUNDAMENTAL DE EXAMEN!:
La Capa 7 NO es el software en si mismo (Google Chrome, Microsoft Outlook o Spotify
NO son la Capa 7). La Capa de Aplicacion esta formada por los PROTOCOLOS DE RED
(HTTP, DNS, DHCP, SMTP) que esos programas utilizan para comunicarse con la red.

Su PDU (Unidad de Datos de Protocolo) es: DATOS (Data).


## 2. PROTOCOLOS WEB: HTTP Y HTTPS (RFC 2616 / 7540 / 9114)

- HTTP (Hypertext Transfer Protocol): Puerto TCP 80 (Texto plano sin cifrar).
- HTTPS (HTTP Secure): Puerto TCP 443 (Cifrado extremo a extremo con TLS).

Metodos HTTP Principales (Operaciones REST):
- GET: Solicita y descarga un recurso del servidor (ej. una pagina HTML o imagen).
- POST: Envia datos al servidor para ser procesados o crear un nuevo registro (ej. login).
- PUT: Reemplaza completamente un recurso existente en el servidor.
- PATCH: Aplica modificaciones parciales a un recurso existente.
- DELETE: Elimina un recurso del servidor.

Codigos de Estado HTTP (Respuestas del Servidor):
- 1xx (Informativos): 101 Switching Protocols.
- 2xx (Exito): 200 OK (Solicitud exitosa), 201 Created (Recurso creado).
- 3xx (Redireccion): 301 Moved Permanently (Redireccion permanente a HTTPS), 304 Not Modified.
- 4xx (Errores del Cliente):
  * 400 Bad Request: Peticion mal estructurada.
  * 401 Unauthorized: Requiere credenciales de autenticacion.
  * 403 Forbidden: Autenticado pero sin permisos para acceder al recurso.
  * 404 Not Found: El archivo o recurso solicitado no existe en el servidor.
  * 429 Too Many Requests: Supero el limite de peticiones permitidas (Rate Limit).
- 5xx (Errores del Servidor):
  * 500 Internal Server Error: El codigo o backend colapso.
  * 502 Bad Gateway: Servidor proxy inverso no recibio respuesta del backend.
  * 503 Service Unavailable: Servidor sobrecargado o en mantenimiento.
  * 504 Gateway Timeout: El servidor proxy agoto el tiempo de espera.

Evolucion de HTTP:
- HTTP/1.1: Basado en conexiones TCP persistentes (Keep-Alive), pero sufre de
  bloqueo de cabeza de linea (Head-of-Line Blocking).
- HTTP/2: Multiplexacion de multiples peticiones sobre una unica conexion TCP binaria.
- HTTP/3: Implementado sobre el protocolo QUIC (basado en UDP), eliminando por
  completo las demoras de conexion de TCP y recuperandose instantaneamente ante perdida de paquetes.


## 3. SISTEMA DE NOMBRES DE DOMINIO: DNS (DOMAIN NAME SYSTEM)

DNS es la "guia telefonica" de Internet. Traduce nombres de dominio legibles
(`www.google.com`) en direcciones IP numericas (`142.250.190.46`).

Puertos utilizados:
- UDP 53: Para consultas y resoluciones normales de nombres (rapidez y bajo consumo).
- TCP 53: Para transferencias de zona (Zone Transfers) entre servidores DNS y respuestas > 512 bytes.

Estructura Jerarquica de Nombres:
Raiz (.) -> TLD (.com, .org, .gob, .mx) -> Dominio Secundario (empresa.com) -> Subdominio (mail.empresa.com)

Tipos de Registros DNS Criticos en Certificaciones:
| Registro | Tipo | Proposito |
| :--- | :--- | :--- |
| A | IPv4 | Mapea un nombre de host a una direccion IPv4 (ej. server -> 192.168.1.10). |
| AAAA | IPv6 | Mapea un nombre a una direccion IPv6 de 128 bits. |
| CNAME | Alias | Nombre Canonico: Redirige un alias a otro dominio (ej. www -> host.com). |
| MX | Correo | Mail Exchange: Especifica los servidores de correo y su prioridad. |
| PTR | Inverso | Pointer: Mapea una direccion IP a un nombre (Resolucion DNS Inversa). |
| NS | Servidor | Name Server: Delega la autoridad de una zona DNS a un servidor especifico. |
| TXT | Texto | Contiene cadenas de texto. Clave para seguridad de correo (SPF, DKIM, DMARC) |
| y validacion de propiedad de dominios. |  |  |
| SOA | Autoridad | Start of Authority: Informacion tecnica de la zona (serial, timers de refresco). |



## 4. ASIGNACION DINAMICA DE DIRECCIONES IP: DHCP (RFC 2131)

Permite que computadoras, telefonos e impresoras obtengan configuracion de red
automatica sin intervencion manual.

Puertos: Servidor DHCP escucha en UDP 67; Cliente DHCP escucha en UDP 68.

## El Proceso DORA (Pregunta Clasica e Indispensable de Examen):

| Fase | Origen | Destino | Tipo de Mensaje | Descripcion |
| :--- | :--- | :--- | :--- | :--- |

1. DISCOVER    Cliente    255.255.255.255  Broadcast         Cliente: "¿Hay algun servidor DHCP disponible?"
2. OFFER       Servidor   255.255.255.255  Unicast/Broadcast Servidor: "Te ofrezco la IP 192.168.1.50 con GW y DNS".
3. REQUEST     Cliente    255.255.255.255  Broadcast         Cliente: "Acepto formalmente la IP 192.168.1.50".
4. ACK         Servidor   255.255.255.255  Unicast/Broadcast Servidor: "Confirmado. La IP es tuya por 24 horas".

Renovacion de la Concesion (Lease Renewal):
- Al llegar al 50% del tiempo de concesion (T1): El cliente envia un unicast al servidor renovando la IP.
- Si no contesta, al 87.5% del tiempo (T2): El cliente envia un broadcast buscando cualquier servidor DHCP.


## 5. PROTOCOLOS DE CORREO ELECTRONICO

- SMTP (Simple Mail Transfer Protocol): Puerto TCP 25 (texto plano), TCP 587 (Envio con STARTTLS cifrado).
  *Proposito: Se utiliza EXCLUSIVAMENTE para ENVIAR correos (de cliente a servidor y entre servidores).
- POP3 (Post Office Protocol v3): Puerto TCP 110 (TCP 995 con SSL).
  *Proposito: Descarga los correos del servidor a la computadora local y los BORRA del servidor.
- IMAP (Internet Message Access Protocol): Puerto TCP 143 (TCP 993 con SSL).
  *Proposito: Mantiene los correos sincronizados en el servidor en tiempo real; accesible desde
   multiples dispositivos (celular, laptop, webmail) simultaneamente.


## 6. OTROS PROTOCOLOS FUNDAMENTALES DE CAPA 7

- FTP (File Transfer Protocol): Puerto TCP 21 (control) y TCP 20 (datos). Transferencia de archivos.
- TFTP (Trivial File Transfer Protocol): Puerto UDP 69. Sin autenticacion; usado para backup de switches y PXE boot.
- SSH (Secure Shell): Puerto TCP 22. Acceso a terminal remota seguro y cifrado.
- Telnet: Puerto TCP 23. Terminal remota en texto plano vulnerable (obsoleto).
- NTP (Network Time Protocol): Puerto UDP 123. Sincronizacion de reloj con jerarquia de Stratum (0 a 16).
- SNMP (Simple Network Management Protocol): Puerto UDP 161 (consultas) y UDP 162 (Trap alertas).


## 7. BANCO DE PREGUNTAS DE EXAMEN (TIPO CCNA / NETWORK+)

### ❓ Pregunta 1
> **Un cliente nuevo se conecta a la red cableada. ¿Cual es el orden exacto**

de los 4 mensajes intercambiados para obtener direccionamiento IP automatico?
Respuesta: DORA (Discover, Offer, Request, Acknowledge).

### ❓ Pregunta 2
> **¿Cual protocolo y numero de puerto utiliza un agente SNMP para enviar**

una notificacion de alarma no solicitada (Trap) al servidor de gestion central?
## Respuesta: Protocolo UDP, puerto 162. (Las consultas GET/SET usan el puerto UDP 161).

