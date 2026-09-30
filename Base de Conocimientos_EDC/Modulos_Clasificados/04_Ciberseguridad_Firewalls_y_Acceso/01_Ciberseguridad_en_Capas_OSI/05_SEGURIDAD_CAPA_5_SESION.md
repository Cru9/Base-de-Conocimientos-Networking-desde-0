# 05. SEGURIDAD EN LA CAPA 5 (SESION) - AMENAZAS, DEFENSAS Y CASO REAL

> **CIBERSEGURIDAD EN EL MODELO OSI - GUIA PRACTICA Y CASOS DE LA VIDA REAL**


---



## 1. PANORAMA DE SEGURIDAD EN LA CAPA DE SESION

La Capa de Sesion gobierna el ciclo de vida de la comunicacion entre usuarios y
servidores: el inicio de sesion (login), la persistencia del estado autenticado
y el cierre formal de sesion (logout).

Objetivo de la Seguridad en Capa 5:
Garantizar que una vez que un usuario demuestra su identidad legitima, ningun
tercero pueda robar su sesion activa, falsificar tokens de autorizacion, interceptar
llamadas de telefonia IP o abusar de protocolos de llamada a procedimiento remoto (RPC/SMB).



## 2. VECTORES DE ATAQUE EN CAPA 5


### a) Secuestro de Sesion (Session Hijacking):

   - El atacante no necesita adivinar la contrasena del usuario. Espera a que la
     victima inicie sesion exitosamente y roba su identificador de sesion activo
     (Session ID / Token).
   - El atacante inserta el Session ID en su propio navegador o cliente y toma el
     control total de la cuenta con los mismos privilegios del usuario.


### b) Fijacion de Sesion (Session Fixation):

   - El atacante obtiene un ID de sesion valido no autenticado y se lo envia a la
     victima a traves de un enlace trampa (`https://banco.com?sessionid=CLAVE_TRAMPA`).
   - Cuando la victima hace clic e inicia sesion con su usuario y clave, el servidor
     comete el error de mantener el mismo ID de sesion prefijado.
   - El atacante, que ya conocia ese ID, accede a la cuenta ya autenticada.


### c) Explotacion de Sesiones SMB y RPC (El vector de WannaCry y NotPetya):

   - Protocolos como Microsoft RPC (Remote Procedure Call) y SMB (Server Message Block -
     puerto TCP 445) permiten interactuar con sesiones remotas a nivel de sistema operativo.
   - Vulnerabilidades catastroficas como MS17-010 (EternalBlue) permitieron que
     el ransomware WannaCry infectara mas de 300,000 computadoras en 150 paises
     mediante la inyeccion de paquetes SMBv1 que ejecutaban codigo con maximos privilegios
     de SYSTEM sin requerir ninguna autenticacion de usuario.


### d) Fraude Telefonico y Ataques de Sesion VoIP / SIP (Toll Fraud):

   - El protocolo SIP (Session Initiation Protocol) senaliza las llamadas de voz IP.
   - Si un conmutador IP-PBX (ej. Asterisk, FreePBX, Cisco CallManager) expone su
     puerto de senalizacion sin autenticacion estricta, los atacantes inyectan
     mensajes `SIP INVITE` para realizar llamadas masivas automatizadas hacia
     numeros internacionales con tarifa especial (premium rate) controlados por ellos,
     generando facturas de decenas de miles de dolares en un solo fin de semana.



## 3. CONTROLES Y SOLUCIONES DE SEGURIDAD EN CAPA 5

1. Regeneracion Obligatoria de ID de Sesion tras Autenticacion:
   - Principio anti-fijacion: NUNCA reutilice el identificador de sesion anonimo.
   - En el instante exacto en que un usuario ingresa sus credenciales validas, el
     servidor debe DESTRUIR la sesion anterior y generar un nuevo Session ID criptografico.

2. Atributos de Seguridad en Cookies de Sesion:
   - `HttpOnly`: Impide que scripts maliciosos de JavaScript (ataques XSS) puedan
     leer la cookie de sesion en el navegador.
   - `Secure`: Fuerza a que la cookie solo viaje a traves de canales cifrados HTTPS.
   - `SameSite=Strict`: Evita que la sesion sea enviada en ataques de falsificacion
     de peticiones (CSRF) desde sitios web de terceros.

3. Tokens de Sesion Inmutables y Firmados (JWT - JSON Web Tokens):
   - Uso de tokens cifrados y firmados con algoritmos HMAC-SHA256 o RSA/ECDSA,
     con tiempos de expiracion cortos (ej. 15 minutos) y tokens de refresco (Refresh Tokens).

4. Temporizadores de Inactividad y Cierre de Sesion Seguro:
   - Terminar automaticamente la sesion si el usuario no realiza ninguna accion
     durante 10 o 15 minutos (Session Timeout).
   - Invalidation en el Servidor: Cuando el usuario hace clic en "Cerrar Sesion",
     el servidor debe revocar el token en su base de datos o lista de revocacion,
     no solo borrar la cookie en el navegador del cliente.

5. Cifrado de Sesiones Multimedia: SIPS y SRTP:
   - SIPS (SIP over TLS): Cifra la señalizacion de inicio y fin de llamada en el puerto TCP 5061.
   - SRTP (Secure Real-Time Transport Protocol): Cifra el flujo de audio y video
     de la llamada con AES-128/256 para evitar escuchas telefonicas clandestinas.

6. Despliegue de Controladores de Borde de Sesion (SBC - Session Border Controllers):
   - Actuan como firewalls especializados de Capa 5 que inspeccionan paquetes SIP/H.323,
     aplican listas negras geograficas y limitan la cantidad de sesiones por minuto.



## 4. CASO DE LA VIDA REAL: FRAUDE TELEFONICO MILLONARIO EN EMPRESA LOGISTICA

Escenario:
Una empresa internacional de transporte y logistica llego un lunes por la mañana
y descubrio que su conmutador telefonico IP (IP-PBX) habia originado mas de 45,000
llamadas internacionales durante el sabado y domingo, generando un cargo de
128,000 dolares por parte del operador telefonico.

El Ataque (Modus Operandi):
1. Los atacantes escanearon Internet buscando servidores VoIP en el puerto UDP 5060 (SIP).
2. Localizaron el conmutador de la empresa, el cual tenia extensiones genericas
   configuradas de fabrica con contrasenas debiles (ej. Extension `1001` con clave `1001`).
3. Mediante un script automatizado, los atacantes autenticaron una sesion SIP en la PBX.
4. Una vez establecida la sesion, programaron un marcador automatico que emitio llamadas
   continuas de 10 segundos hacia numeros de tarifa especial en paises de Europa del Este,
   Africa e islas del Caribe propiedad de redes de cibercrimen.
5. Los atacantes cobraron un porcentaje por cada minuto de llamada internacional completada.

La Solucion y Remediacion Implementada:
Para erradicar la vulnerabilidad y blindar la telefonia corporativa en Capa 5:
1. Despliegue de un Session Border Controller (SBC) perimetral:
   - Ningun telefono ni servidor de Internet puede hablar directamente con la PBX interna.
2. Migracion a SIPS (SIP sobre TLS) en el puerto TCP 5061:
   - Todas las sesiones de señalizacion y registro de extensiones se forzaron con
     certificados digitales y autenticacion mutua (mTLS).
3. Bloqueo de Rutas de Marcacion Internacional (Toll Restriction):
   - Se configuro el dial-plan de la PBX para deshabilitar por completo las llamadas
     internacionales salientes en horario no laboral (fines de semana y noches).
   - Se requirio un codigo PIN de autorizacion individual para realizar llamadas al extranjero.
4. Monitoreo y Rate Limiting de Sesiones SIP:
   - Se configuro una regla en el SBC que bloquea y envia una alerta inmediata si

una extension inicia mas de 3 llamadas por minuto.
