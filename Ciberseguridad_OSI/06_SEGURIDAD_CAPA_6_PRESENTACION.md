# 06. SEGURIDAD EN LA CAPA 6 (PRESENTACION) - AMENAZAS, DEFENSAS Y CASO REAL

> **CIBERSEGURIDAD EN EL MODELO OSI - GUIA PRACTICA Y CASOS DE LA VIDA REAL**


---



## 1. PANORAMA DE SEGURIDAD EN LA CAPA DE PRESENTACION

La Capa de Presentacion trata sobre como se representan, codifican, serializan
y cifran los datos antes de ser entregados a las aplicaciones de software.

Durante decadas se considero una capa puramente tecnica de formateo, pero en la
ciberseguridad moderna es el epicentro de vulnerabilidades criticas de ejecucion
remota de codigo (RCE) y ataques contra la criptografia.

Objetivo de la Seguridad en Capa 6:
Garantizar la confidencialidad absoluta mediante estandares criptograficos modernos,
evitar la degradacion de canales cifrados (Downgrade Attacks) y asegurar que los
motores de interpretacion de datos (JSON, XML, objetos serializados) no ejecuten
codigo malicioso oculto.



## 2. VECTORES DE ATAQUE EN CAPA 6


### a) Ataques de Despojo y Degradacion Criptografica (SSL Stripping y POODLE):

   - SSL Stripping (Moxie Marlinspike): El atacante se interpone en la conexion.
     Cuando el usuario intenta conectarse a `http://banco.com`, el atacante intercepta
     la redireccion hacia `https://banco.com`. El atacante habla HTTPS seguro con
     el banco, pero le entrega al usuario una version HTTP desprotegida en texto plano,
     capturando contrasenas y tokens en vivo.
   - Ataques de Degradacion (Downgrade): Fuerzan al servidor a negociar versiones
     obsoletas e inseguras de cifrado (SSLv3, TLS 1.0, o suites con claves de 512 bits)
     para descifrar el trafico en tiempo real.


### b) Deserializacion Insegura de Objetos (Insecure Deserialization - RCE):

   - Muchas aplicaciones convierten objetos en memoria en cadenas de bytes para
     enviarlos por la red (Serializacion en Java, Python pickle, PHP serialize, .NET).
   - Si la aplicacion deserializa datos recibidos de un usuario sin validacion estricta,
     un atacante inyecta una estructura de bytes manipulada (Gadget Chain).
   - Al reconstruir el objeto en el servidor, el procesador ejecuta los comandos
     inyectados con permisos de administrador (Ejecucion Remota de Codigo - RCE).


### c) Inyeccion de Entidades Externas XML (XXE - XML External Entity):

   - Vulnerabilidad en parsers de datos XML que interpretan referencias a entidades externas.
   - Un atacante envia un archivo XML con una definicion DTD que apunta al sistema de
     archivos local: `<!ENTITY xxe SYSTEM "file:///etc/passwd">`.
   - El parser procesa el formato y devuelve el contenido de archivos confidenciales
     o credenciales del servidor.


### d) Ataques por Canal Lateral de Compresion (CRIME y BREACH):

   - Explotan el algoritmo de compresion DEFLATE en TLS y HTTP.
   - Como la compresion reduce el tamano cuando hay texto repetido, un atacante
     puede adivinar cookies secretas y tokens CSRF caracter por caracter midiendo
     las pequenas variaciones en el tamano en bytes de las respuestas cifradas.



## 3. CONTROLES Y SOLUCIONES DE SEGURIDAD EN CAPA 6

1. Implementacion Estricta de TLS 1.3 con Perfect Forward Secrecy (PFS):
   - Desactivar completamente SSLv2, SSLv3, TLS 1.0 y TLS 1.1 en todos los servidores web.
   - Configurar suites de cifrado modernas basadas en curvas elipticas (ECDHE):
     * Cifrado: AES-256-GCM o ChaCha20-Poly1305.
     * Intercambio de claves: ECDHE-RSA o ECDHE-ECDSA.
   - Con Perfect Forward Secrecy, si la clave privada del servidor llegara a ser robada
     en el futuro, los atacantes NO PODRAN descifrar las grabaciones de trafico del pasado.

2. Politica de Seguridad HSTS (HTTP Strict Transport Security) con Preload:
   - Encabezado HTTP que ordena al navegador jamas comunicarse en texto plano:
     `Strict-Transport-Security: max-age=31536000; includeSubDomains; preload`
   - Bloquea al 100% los ataques de SSL Stripping, ya que el navegador rechaza
     cualquier conexion que no sea HTTPS nativo directo.

3. Abandono de Serializadores Nativos Inseguros:
   - Prohibir el uso de `pickle` en Python, `ObjectInputStream` en Java y `unserialize()` en PHP
     para datos provenientes de clientes de red.
   - Reemplazar por formatos de serializacion puramente declarativos como JSON con
     validacion rigurosa de esquema (JSON Schema) o Protocol Buffers (Protobuf).

4. Desactivacion de Entidades DTD en Parsers XML:
   - Configurar todos los motores de procesamiento XML con la propiedad:
     `disallow-doctype-decl = true` y desactivar la resolucion de entidades externas.



## 4. CASO DE LA VIDA REAL: LA BRECHA HISTORICA DE EQUIFAX (APACHE STRUTS)

Escenario:
En 2017, la agencia de informes crediticios Equifax sufrio una de las mayores brechas
de la historia: el robo de datos financieros y personales de mas de 147 millones de personas,
con un costo acumulado en multas, acuerdos y remediacion de mas de 1,400 millones de dolares.

El Ataque (Modus Operandi):
1. El vector de entrada fue la vulnerabilidad CVE-2017-5638 en el framework Apache Struts.
2. La falla residia en el componente de la Capa de Presentacion encargado de interpretar
   el formato de encabezados de subida de archivos (el parser `Jakarta Multipart`).
3. Los atacantes enviaron una peticion HTTP con un valor malformado en el encabezado
   `Content-Type` que contenia una expresion de codigo OGNL (Object-Graph Navigation Language).
4. El parser de la Capa de Presentacion intento procesar la sintaxis del encabezado
   para clasificar el tipo de archivo y ejecuto el codigo malicioso directamente en el
   servidor con privilegios de root.
5. Los atacantes obtuvieron una consola de comandos remota (web shell), descubrieron
   bases de datos no cifradas y exfiltraron datos durante 76 dias sin ser detectados.

La Solucion y Remediacion Implementada:
1. Parcheo Inmediato y Reemplazo del Parser de Contenido:
   - Actualizacion de frameworks y deshabilitacion de interpretes de lenguaje dinamico
     (OGNL) en capas de entrada de datos.
2. Despliegue de WAF (Web Application Firewall) con Inspeccion Profunda de Sintaxis:
   - Se crearon reglas de filtrado que analizan el formato y sintaxis de todos los
     encabezados de Capa 6 (`Content-Type`, `Accept`, `Encoding`), bloqueando cualquier
     solicitud que contenga caracteres o comandos no estandar.
3. Cifrado de Bases de Datos en Reposo (At-Rest) y en Transito con TLS 1.3:
   - Si los datos hubieran estado cifrados internamente, los atacantes habrian robado

cadenas de texto ininteligibles en lugar de expedientes de credito legibles.
