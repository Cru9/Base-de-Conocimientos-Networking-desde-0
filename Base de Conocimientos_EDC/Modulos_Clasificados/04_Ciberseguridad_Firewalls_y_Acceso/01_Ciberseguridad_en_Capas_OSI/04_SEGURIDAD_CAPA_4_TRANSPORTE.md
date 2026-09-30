# 04. SEGURIDAD EN LA CAPA 4 (TRANSPORTE) - AMENAZAS, DEFENSAS Y CASO REAL

> **CIBERSEGURIDAD EN EL MODELO OSI - GUIA PRACTICA Y CASOS DE LA VIDA REAL**


---



## 1. PANORAMA DE SEGURIDAD EN LA CAPA DE TRANSPORTE

La Capa 4 es el campo de batalla donde se libran los mayores ataques de Denegacion
de Servicio Distribuido (DDoS) del mundo y donde operan los Firewalls con Estado
(Stateful Firewalls).

A diferencia de la Capa 3 (que solo ve direcciones IP), la Capa 4 entiende el
concepto de ESTADO DE CONEXION: sabe cuando una sesion esta naciendo (SYN), cuando
esta activa y autenticada (ESTABLISHED) y cuando ha terminado (FIN/RST).

Objetivo de la Seguridad en Capa 4:
Evitar la saturacion de las colas de conexion de los servidores, mitigar ataques
de denegacion de servicio (TCP SYN Flood / UDP Amplification) y controlar con
precision quirurgica que puertos y servicios tienen permitido comunicarse.



## 2. VECTORES DE ATAQUE EN CAPA 4


### a) Inundacion TCP SYN Flood (DDoS de Agotamiento de Memoria):

   - El atacante abusa del saludo de tres vias (3-Way Handshake) de TCP.
   - Envia millones de paquetes con la bandera `[SYN]` por segundo con IPs falsas.
   - Para cada peticion, el servidor reserva un bloque de memoria RAM (TCB - Transmission
     Control Block) y queda esperando la respuesta `[ACK]` en estado `SYN_RCVD`.
   - Como la IP es falsa, el `ACK` nunca llega. En pocos segundos, la cola de
     conexiones pendientes (Backlog Queue) del servidor se llena al 100%.
   - Consecuencia: El servidor colapsa y rechaza las conexiones de clientes legitimos.


### b) Ataque de Reinicio Forzado de Sesion (TCP Reset Attack):

   - Si un atacante intercepta o adivina el numero de puerto y el numero de secuencia
     de una conexion TCP activa importante (ej. una sesion BGP o un tunel VPN),
     inyecta un paquete falso con la bandera `[RST]` (Reset).
   - El servidor cree que el cliente se desconecto de emergencia y CIERRA LA SESION
     inmediatamente, derribando enlaces criticos de telecomunicaciones.


### c) Escaneos Sigilosos de Puertos (Port Scanning / Reconocimiento):

   - TCP SYN Stealth Scan (`nmap -sS`): Envia un SYN; si el servidor responde SYN-ACK,
     el atacante sabe que el puerto esta abierto y de inmediato envia un RST para
     no completar la conexion y evitar ser registrado en los logs de la aplicacion.
   - Escaneos anomalos: Xmas Scan (banderas FIN, URG y PSH encendidas al mismo tiempo),
     Null Scan (cero banderas activas).


### d) Ataques de Amplificacion y Reflexion UDP:

   - Dado que UDP no valida el origen (no tiene handshake), el atacante envia
     pequenas peticiones a servidores publicos con la IP de la victima suplantada:
     * NTP Monlist (UDP 123): Factor de amplificacion de 556 veces.
     * DNS Any Query (UDP 53): Factor de amplificacion de 50 veces.
     * Memcached (UDP 11211): Factor de amplificacion de ¡hasta 51,000 veces!
       (Un paquete de 1 KB del atacante genera 51 MB de datos directos a la victima).



## 3. CONTROLES Y SOLUCIONES DE SEGURIDAD EN CAPA 4

1. Mecanismo de TCP SYN Cookies (RFC 4987 - Solucion Definitiva al SYN Flood):
   - Cuando la cola de conexiones del servidor se satura, el sistema operativo
     DEJA DE RESERVAR MEMORIA para las conexiones en estado semi-abierto.
   - En su lugar, codifica los parametros de la conexion dentro del numero de secuencia
     inicial (ISN) que envia en el `[SYN, ACK]`.
   - Consumo de memoria = 0 bytes. Si el cliente es legitimo y devuelve el `[ACK]`,
     el servidor decodifica el numero y crea la sesion en ese momento.
   - Habilitacion en Linux: `sysctl -w net.ipv4.tcp_syncookies=1`

2. Inspeccion de Estado (Stateful Firewalls - iptables / Cisco ASA / Palo Alto / Fortinet):
   - El cortafuegos mantiene una tabla de estados dinamica en memoria RAM:
     * Si llega un paquete `[ACK]` o `[RST]` que no corresponde a una conexion que
       haya iniciado previamente con un `[SYN]`, el firewall lo DESCARTA de inmediato.
   - Bloquea escaneos anomalos de nmap (Xmas, Null scans) catalogandolos como paquetes
     de estado 'INVALID'.

3. TCP Intercept y Rate Limiting de Conexiones:
   - El Firewall o balanceador de carga se interpone entre Internet y el servidor:
     responde el 3-way handshake en nombre del servidor y solo si el cliente completa
     la conexion, transfiere el socket al servidor real.

4. Aleatorizacion Criptografica de Numeros de Secuencia (ISN Randomization - RFC 6528):
   - Los sistemas operativos modernos utilizan generadores de numeros pseudoaleatorios
     criptograficamente seguros (CSPRNG) para que sea matematicamente imposible
     predecir el Sequence Number y ejecutar un TCP Session Hijacking.



## 4. CASO DE LA VIDA REAL: COLAPSO DE TIENDA EN LINEA POR SYN FLOOD EN BLACK FRIDAY

Escenario:
Uno de los mayores portales de comercio electronico de latinoamerica sufrio una caida
total durante las primeras dos horas del evento de ofertas "Black Friday", con pérdidas
estimadas en mas de 350,000 dolares por hora.

El Ataque (Modus Operandi):
1. A las 00:01 AM, una botnet de dispositivos IoT infectados (camaras de seguridad
   y routers comprometidos) comenzo a emitir un ataque de inundacion TCP SYN Flood
   dirigido al puerto TCP 443 (HTTPS) de los servidores de pasarela de pago.
2. La botnet genero mas de 12 millones de paquetes SYN por segundo con IPs origen falsificadas.
3. La cola de memoria de conexiones pendientes (TCP Backlog Queue) de los balanceadores
   se lleno en 3 segundos.
4. Cuando los clientes reales intentaban hacer clic en "Finalizar Compra", su navegador
   se quedaba cargando indefinidamente hasta mostrar el error "Connection Timed Out".

La Solucion y Remediacion Implementada:
El equipo de ingenieria de infraestructura y ciberseguridad ejecuto las siguientes acciones:
1. Activacion de Centros de Mitigacion y Limpieza de Trafico (Anti-DDoS Scrubbing):
   - Se modifico el anuncio de rutas BGP para canalizar todo el trafico a traves de
     redes de mitigacion distribuidas (Cloudflare / Akamai).
2. Despliegue de TCP SYN Cookies a nivel de hardware en balanceadores:
   - El centro de mitigacion comenzo a responder el saludo TCP mediante SYN Cookies.
     Como los bots de la botnet solo enviaban SYNs y nunca esperaban la respuesta para
     enviar el ACK final, el 100% del trafico malicioso fue filtrado antes de tocar
     los servidores de comercio electronico.
3. Restriccion de conexiones TCP simultaneas por IP origen (Rate Limiting de Capa 4):
   - Se impuso un limite maximo de 50 conexiones nuevas por segundo por direccion IP.
4. El servicio se restablecio por completo a las 02:20 AM y la pasarela de pagos

proceso las compras con total normalidad durante el resto del evento.
