# 07. SEGURIDAD EN LA CAPA 7 (APLICACION) - AMENAZAS, DEFENSAS Y CASO REAL

> **CIBERSEGURIDAD EN EL MODELO OSI - GUIA PRACTICA Y CASOS DE LA VIDA REAL**


---



## 1. PANORAMA DE SEGURIDAD EN LA CAPA DE APLICACION

La Capa de Aplicacion es donde interactuan directamente el usuario final y la
logica del negocio. Segun los informes globales de ciberseguridad, mas del 75%
de todos los ciberataques actuales se dirigen contra la Capa 7.

¿Por que los atacantes prefieren la Capa 7?
Porque los puertos de Capa 4 correspondientes (ej. TCP 443 para HTTPS y UDP 53 para DNS)
DEBEN estar abiertos en el firewall para que el negocio funcione. Un firewall
tradicional de red solo ve "trafico permitido en el puerto 443", pero es ciego
al contenido del mensaje malicioso que viaja adentro.

Objetivo de la Seguridad en Capa 7:
Inspeccionar y sanitizar las entradas de los usuarios, validar la logica de negocio,
proteger las APIs REST, blindar la resolucion de nombres DNS y frustrar el abuso
de protocolos de aplicacion (OWASP Top 10).



## 2. VECTORES DE ATAQUE EN CAPA 7


### a) Inyeccion SQL (SQL Injection - SQLi):

   - El atacante introduce comandos de base de datos dentro de campos de entrada
     (formularios de login, parametros de URL: `' OR 1=1 --`).
   - La aplicacion concatena la entrada directamente en la consulta a la base de datos.
   - Consecuencia: El atacante elude la autenticacion, extrae la base de datos
     completa (Dump), modifica saldos bancarios o ejecuta comandos en el sistema operativo.


### b) Cross-Site Scripting (XSS - Reflejado, Almacenado y Basado en DOM):

   - El atacante inyecta codigo JavaScript malicioso en un sitio web vulnerable.
   - Cuando otros usuarios legitimos visitan la pagina, el navegador ejecuta el script.
   - Consecuencia: Robo de cookies de sesion activas, captura de pulsaciones de
     teclado (keylogger en el navegador) o redireccion a sitios web con malware.


### c) Server-Side Request Forgery (SSRF - El vector moderno en la Nube):

   - El atacante engaña al servidor web para que realice peticiones HTTP internas
     hacia recursos de su propia red que no estan expuestos a Internet.
   - Critico en entornos Cloud (AWS, Azure, GCP): El atacante fuerza al servidor
     a consultar el servicio de metadatos interno (`http://169.254.169.254`) y
     roba las credenciales secretas del rol IAM de administracion de la nube.


### d) Ataques al Protocolo DNS:

   - DNS Cache Poisoning: Inyectar registros falsos en servidores DNS recursivos
     para redirigir a millones de usuarios hacia sitios fraudulentos.
   - DNS Tunneling: Exfiltrar archivos confidenciales codificados en peticiones DNS
     (ej. `base64_archivo_secreto.servidor-atacante.com`). Los firewalls dejan salir
     el trafico creyendo que son consultas normales de nombres.


### e) Denegacion de Servicio en Capa 7 (HTTP Flood / Slowloris):

   - A diferencia de los DDoS volumetricos en Capa 4, un HTTP Flood requiere muy poco
     ancho de banda. Envia peticiones GET o busquedas complejas que obligan a la base
     de datos a procesar millones de calculos intensivos hasta agotar la CPU del servidor.



## 3. CONTROLES Y SOLUCIONES DE SEGURIDAD EN CAPA 7

1. Consultas Parametrizadas y Sentencias Preparadas (Mitigacion Total de SQLi):
   - NUNCA concatenar cadenas de texto para formar consultas SQL.
   - Al usar Prepared Statements, el motor de base de datos trata la entrada del usuario
     estrictamente como un DATO literal y NUNCA como codigo ejecutable, neutralizando
     cualquier intento de inyeccion.

2. Web Application Firewall (WAF - Cloudflare / AWS WAF / ModSecurity / F5 ASM):
   - Inspecciona el trafico HTTP/HTTPS descifrado en tiempo real.
   - Detecta y bloquea firmas de SQLi, XSS, patrones de ataque a APIs y solicitudes
     automatizadas de bots maliciosos (Scraping y Credential Stuffing).

3. Content Security Policy (CSP) y Sanitizacion de Salida:
   - Encabezado HTTP que define estrictamente que dominios tienen permitido ejecutar
     scripts en la pagina web:
     `Content-Security-Policy: default-src 'self'; script-src 'self' https://scripts.confiables.com`
   - Bloquea la ejecucion de scripts XSS inyectados por atacantes.

4. Extensiones de Seguridad de DNS (DNSSEC):
   - Firma criptograficamente con claves publicas y privadas cada zona DNS.
   - Si un atacante intenta envenenar la cache con una IP falsa, el validador DNSSEC
     detecta que la firma no coincide y descarta la respuesta fraudulenta.

5. Autenticacion Multifactor Fuerte (MFA / FIDO2 WebAuthn):
   - Implementar llaves de seguridad fisicas (YubiKey) o biometricas. Aunque un
     atacante robe la contrasena del usuario mediante phishing, no podra acceder
     sin la llave fisica.



## 4. CASO DE LA VIDA REAL: LA MEGABRECHA DE CAPITAL ONE (SSRF EN LA NUBE)

Escenario:
En 2019, la institucion financiera Capital One sufrio el robo de datos personales y
financieros de mas de 106 millones de clientes en Estados Unidos y Canada, resultando
en una multa regulatoria de 80 millones de dolares y acuerdos por mas de 190 millones.

El Ataque (Modus Operandi):
1. El vector de entrada fue un servidor proxy / WAF mal configurado montado sobre
   una instancia virtual EC2 en Amazon Web Services (AWS).
2. La atacante descubrio una vulnerabilidad de Server-Side Request Forgery (SSRF)
   en la aplicacion web.
3. Mediante la peticion manipulada, forzo al servidor de Capital One a hacer una
   consulta interna hacia la direccion de enlace local del servicio de metadatos de AWS:
   `http://169.254.169.254/latest/meta-data/iam/security-credentials/`
4. El servicio de metadatos (IMDSv1) respondio con las credenciales temporales del
   Rol de IAM asociado al servidor, el cual tenia asignados permisos excesivos de administrador.
5. Con esas credenciales robadas, la atacante se conecto directamente al API de AWS
   y descargo mas de 700 carpetas (S3 Buckets) con solicitudes de tarjetas de credito,
   numeros de seguridad social y cuentas bancarias.

La Solucion y Remediacion Implementada:
Este incidente transformo los estandares de seguridad en la nube y Capa 7 a nivel mundial:
1. Migracion Obligatoria a AWS IMDSv2 (Metadatos de Instancia Version 2):
   - IMDSv2 requiere obligatoriamente una peticion `PUT` previa con un token de sesion
     para entregar credenciales. Los ataques SSRF simples en Capa 7 no pueden completar
     este flujo, anulando el ataque por diseno.
2. Principio de Minimo Privilegio en Roles de IAM:
   - Ningun servidor web debe tener permisos de lectura sobre todos los buckets de almacenamiento.
     Los permisos se restringieron de forma granular por aplicacion.
3. Inspeccion Estricta de Salida en WAF y Micro-segmentacion de Red (VPC Endpoints):
   - Se crearon reglas que impiden que los servidores de cara al publico puedan

iniciar conexiones arbitrarias hacia destinos internos no autorizados.
