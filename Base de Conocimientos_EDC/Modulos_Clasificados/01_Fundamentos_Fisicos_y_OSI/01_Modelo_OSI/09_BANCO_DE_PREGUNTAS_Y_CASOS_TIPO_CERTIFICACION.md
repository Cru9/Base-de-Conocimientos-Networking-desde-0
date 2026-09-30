# 09. SIMULADOR Y BANCO DE 30 PREGUNTAS TIPO CERTIFICACION (CCNA / NETWORK+ / HCIA)

> **MODELO OSI (OPEN SYSTEMS INTERCONNECTION) - GUIA MAESTRA PARA CERTIFICACIONES**  
> *Guía de referencia técnica y preparación para certificaciones Cisco CCNA 200-301, CompTIA Network+ y Huawei HCIA.*

---


Este banco de preguntas reune los reactivos y casos practicos mas frecuentes en
examenes de certificacion internacional (Cisco CCNA 200-301, CompTIA Network+
y Huawei HCIA-Datacom). Estudie las explicaciones detalladas para consolidar
su dominio teorico y practico.

---

## 📌 BLOQUE 1: FUNDAMENTOS Y ENCAPSULAMIENTO

### ❓ Pregunta 1

¿Cual es el orden correcto de encapsulamiento de datos conforme descienden desde
la Capa de Transporte hasta la Capa Fisica en el modelo OSI?
A) Paquete -> Segmento -> Trama -> Bits
B) Segmento -> Trama -> Paquete -> Bits
C) Segmento -> Paquete -> Trama -> Bits
D) Trama -> Paquete -> Segmento -> Bits
<details>
<summary><b>🔍 Ver Respuesta Correcta y Explicación</b></summary>

> **Respuesta Correcta:** `C`  
> **Explicación:** En la Capa 4 los datos se convierten en Segmentos (TCP) o Datagramas (UDP).
> En la Capa 3 se agrega el encabezado IP formando un Paquete. En la Capa 2 se agregan
> direcciones MAC y el pie FCS formando una Trama. En la Capa 1 la trama se convierte
> en Bits fisicos.
</details>


### ❓ Pregunta 2

¿Cual de las siguientes capas del modelo OSI NO tiene un encabezado equivalente
en el modelo TCP/IP, siendo sus funciones absorbidas directamente por la aplicacion?
A) Capa de Transporte
B) Capas de Sesion y Presentacion
C) Capa de Red
D) Capa de Enlace de Datos
<details>
<summary><b>🔍 Ver Respuesta Correcta y Explicación</b></summary>

> **Respuesta Correcta:** `B`  
> **Explicación:** El modelo TCP/IP fusiona las Capas 5 (Sesion), 6 (Presentacion) y 7 (Aplicacion)
> del modelo OSI en una unica capa llamada "Capa de Aplicacion".
</details>


### ❓ Pregunta 3

Cuando un router reenvia un paquete IPv4 hacia el siguiente salto en Internet,
¿cuales campos sufren modificaciones obligatorias?
A) La IP Origen y la IP Destino
B) El puerto TCP origen y el puerto TCP destino
C) Las direcciones MAC de Capa 2 y el campo TTL de Capa 3
D) Unicamente el campo FCS de la trama
<details>
<summary><b>🔍 Ver Respuesta Correcta y Explicación</b></summary>

> **Respuesta Correcta:** `C`  
> **Explicación:** Las direcciones IP de origen y destino se mantienen constantes de extremo
> a extremo. Sin embargo, el router reescribe las direcciones MAC de Capa 2 para el
> siguiente salto fisico y decrementa el campo TTL (Time-to-Live) en 1 para evitar bucles.
</details>


### ❓ Pregunta 4

¿Que termino describe la cantidad de datos utiles que recibe una aplicacion despues
de descontar la sobrecarga de todos los encabezados de red y retransmisiones?
A) Throughput
B) Bandwidth
C) Goodput
D) Latency
<details>
<summary><b>🔍 Ver Respuesta Correcta y Explicación</b></summary>

> **Respuesta Correcta:** `C`  
> **Explicación:** Goodput es el rendimiento real a nivel de aplicacion (datos netos sin
> encabezados ni paquetes retransmitidos). Bandwidth es la capacidad teorica y Throughput
> es la tasa de transferencia bruta total en el medio.

</details>


---

## 📌 BLOQUE 2: CAPA 1 (FISICA) Y CAPA 2 (ENLACE DE DATOS)

### ❓ Pregunta 5

Un ingeniero debe conectar dos switches de distribucion separados por una distancia
de 8 kilometros a traves del campus. ¿Que tipo de fibra y transceptor debe seleccionar?
A) Fibra Multimodo OM4 con transceptor 10GBASE-SR (850 nm)
B) Fibra Monomodo (SMF) con transceptor 10GBASE-LR (1310 nm)
C) Cable UTP Categoria 6a
D) Cable DAC de cobre pasivo
<details>
<summary><b>🔍 Ver Respuesta Correcta y Explicación</b></summary>

> **Respuesta Correcta:** `B`  
> **Explicación:** La fibra multimodo solo alcanza hasta 400-550 metros. Para distancias
> mayores a 2 kilometros es obligatorio usar Fibra Monomodo (SMF) con transceptores
> LR (Long Reach - hasta 10 km) o ER (Extended Reach - hasta 40 km).
</details>


### ❓ Pregunta 6

¿Cual es el estandar de cableado TIA/EIA para los pines 1 y 2 en la norma 568A?
A) Blanco/Naranja y Naranja
B) Blanco/Verde y Verde
C) Blanco/Azul y Azul
D) Blanco/Marron y Marron
<details>
<summary><b>🔍 Ver Respuesta Correcta y Explicación</b></summary>

> **Respuesta Correcta:** `B`  
> **Explicación:** En la norma T568A, el par verde ocupa los pines 1 (Blanco/Verde) y 2 (Verde).
> En la norma T568B, el par naranja ocupa los pines 1 y 2.
</details>


### ❓ Pregunta 7

Un switch recibe una trama unicast cuya direccion MAC destino NO se encuentra en
su tabla CAM de direcciones MAC. ¿Que accion tomara el conmutador?
A) Descarta la trama de inmediato y envia un mensaje ICMP al emisor
B) Envia la trama unicamente por el puerto que tenga la prioridad mas alta
C) Inunda la trama por todos los puertos activos de esa misma VLAN, excepto por el puerto donde ingreso
D) Envia un broadcast ARP para descubrir la MAC del host
<details>
<summary><b>🔍 Ver Respuesta Correcta y Explicación</b></summary>

> **Respuesta Correcta:** `C`  
> **Explicación:** Este proceso se conoce como "Unknown Unicast Flooding". El switch reenvia
> la trama por todos los puertos de esa VLAN (salvo el puerto origen) esperando que el
> dispositivo legitimo responda para aprender su ubicacion. Los switches no generan ARP.
</details>


### ❓ Pregunta 8

¿Cuantos bytes agrega a la trama Ethernet original el estandar IEEE 802.1Q para
identificar la VLAN?
A) 2 Bytes
B) 4 Bytes
C) 8 Bytes
D) 32 Bytes
<details>
<summary><b>🔍 Ver Respuesta Correcta y Explicación</b></summary>

> **Respuesta Correcta:** `B`  
> **Explicación:** La etiqueta 802.1Q agrega exactamente 4 bytes (32 bits) entre la MAC Origen
> y el EtherType, conteniendo el TPID (0x8100), la prioridad PCP (3 bits), DEI (1 bit)
> y el VLAN ID (12 bits, permitiendo hasta 4094 VLANs).
</details>


### ❓ Pregunta 9

¿Cual de las siguientes afirmaciones describe con precision la relacion entre
un switch y los dominios de colision y difusion?
A) Cada puerto de un switch es un dominio de difusion y colision separado.
B) Todos los puertos de un switch forman un solo dominio de colision y un solo dominio de difusion.
C) Cada puerto de un switch es un dominio de colision independiente; todos los puertos en la misma VLAN comparten un dominio de difusion.
D) Los switches no manejan dominios de colision.
<details>
<summary><b>🔍 Ver Respuesta Correcta y Explicación</b></summary>

> **Respuesta Correcta:** `C`  
> **Explicación:** Al operar en conmutacion dedicada (Full-Duplex), cada puerto es su propio
> dominio de colision. Sin embargo, el trafico broadcast enviado por cualquier puerto
> inunda a todos los demas puertos de esa VLAN (mismo dominio de difusion).
</details>


### ❓ Pregunta 10

¿Que subcapa de la Capa de Enlace de Datos interactua directamente con la Capa de
Red y permite que multiples protocolos como IPv4 e IPv6 coexistan en la misma NIC?
A) Subcapa MAC (Media Access Control)
B) Subcapa FCS
C) Subcapa LLC (Logical Link Control - IEEE 802.2)
D) Subcapa PHY
<details>
<summary><b>🔍 Ver Respuesta Correcta y Explicación</b></summary>

> **Respuesta Correcta:** `C`  
> **Explicación:** La subcapa LLC (802.2) proporciona la interfaz logica independiente del
> hardware para comunicarse con la Capa 3 mediante puntos de acceso al servicio (SAP).

</details>


---

## 📌 BLOQUE 3: CAPA 3 (RED) Y SUBNETTING

### ❓ Pregunta 11

Se requiere disenar un enlace punto a punto WAN entre dos routers utilizando la
menor cantidad posible de direcciones IP utiles. ¿Que mascara de subred debe usar?
A) 255.255.255.248 (/29)
B) 255.255.255.252 (/30)
C) 255.255.255.240 (/28)
D) 255.255.255.0 (/24)
<details>
<summary><b>🔍 Ver Respuesta Correcta y Explicación</b></summary>

> **Respuesta Correcta:** `B`  
> **Explicación:** Una mascara /30 (255.255.255.252) tiene 2 bits de host: 2^2 - 2 = 2 direcciones
> IP utiles exactas, perfectas para un enlace punto a punto sin desperdiciar direcciones.
</details>


### ❓ Pregunta 12

¿Cual de las siguientes direcciones IPv4 pertenece a un rango publico enrutable en Internet?
A) 10.150.20.1
B) 172.25.100.50
C) 192.168.1.254
D) 172.33.1.1
<details>
<summary><b>🔍 Ver Respuesta Correcta y Explicación</b></summary>

> **Respuesta Correcta:** `D`  
> **Explicación:** Los rangos privados RFC 1918 son: 10.0.0.0/8, 172.16.0.0/12 (hasta 172.31.255.255)
> y 192.168.0.0/16. La direccion 172.33.1.1 queda fuera del rango privado y es publica.
</details>


### ❓ Pregunta 13

Al comprimir la direccion IPv6 `2001:0db8:0000:0000:0000:0000:1428:57ab`, ¿cual es
la forma correcta y mas compacta permitida por el RFC?
A) 2001:db8::1428:57ab
B) 2001:db8::::1428:57ab
C) 2001:0db8::1428:57ab
D) 2001:db8:0:0:0:0:1428:57ab
<details>
<summary><b>🔍 Ver Respuesta Correcta y Explicación</b></summary>

> **Respuesta Correcta:** `A`  
> **Explicación:** Se eliminan los ceros a la izquierda (`0db8` -> `db8`) y los grupos
> consecutivos de cuatro ceros se reemplazan por `::` una sola vez.
</details>


### ❓ Pregunta 14

¿Cual es el valor del campo 'Protocol' en el encabezado IPv4 cuando el paquete
transporta un segmento TCP?
A) 1
B) 6
C) 17
D) 89
<details>
<summary><b>🔍 Ver Respuesta Correcta y Explicación</b></summary>

> **Respuesta Correcta:** `B`  
> **Explicación:** Protocol 1 = ICMP, Protocol 6 = TCP, Protocol 17 = UDP, Protocol 89 = OSPF.
</details>


### ❓ Pregunta 15

Un router tiene en su tabla de enrutamiento las siguientes rutas hacia la red 10.1.1.0/24:
- OSPF (Distancia Administrativa 110, Metrica 20)
- EIGRP (Distancia Administrativa 90, Metrica 2000)
- Ruta Estatica (Distancia Administrativa 1, Metrica 0)
¿Cual ruta instalara el router en la tabla de reenvio activa?
A) OSPF porque tiene menor metrica
B) EIGRP porque es propietario de Cisco
C) La Ruta Estatica porque tiene la menor Distancia Administrativa (AD = 1)
D) Realizara balanceo de carga entre las tres rutas
<details>
<summary><b>🔍 Ver Respuesta Correcta y Explicación</b></summary>

> **Respuesta Correcta:** `C`  
> **Explicación:** Cuando un router aprende la misma red por diferentes origenes, SIEMPRE
> elige la ruta con la menor Distancia Administrativa (AD). 1 (Estatica) vence a 90 y a 110.

</details>


---

## 📌 BLOQUE 4: CAPA 4 (TRANSPORTE)

### ❓ Pregunta 16

Durante el saludo de tres vias (3-Way Handshake) de TCP, ¿que bandera(s) lleva
activadas el segundo paquete enviado por el servidor hacia el cliente?
A) Solo SYN
B) SYN y ACK
C) PSH y ACK
D) FIN y ACK
<details>
<summary><b>🔍 Ver Respuesta Correcta y Explicación</b></summary>

> **Respuesta Correcta:** `B`  
> **Explicación:** El flujo es: 1. Cliente envia [SYN] -> 2. Servidor responde [SYN, ACK] ->
> 3. Cliente envia [ACK].
</details>


### ❓ Pregunta 17

¿Que mecanismo utiliza el protocolo TCP para evitar que un servidor que transmite
a 10 Gbps desborde la memoria del buffer de una computadora cliente lenta?
A) Congestion Avoidance
B) Sliding Window (Ventana Deslizante / Control de Flujo)
C) Three-Way Handshake
D) Slow Start
<details>
<summary><b>🔍 Ver Respuesta Correcta y Explicación</b></summary>

> **Respuesta Correcta:** `B`  
> **Explicación:** El receptor anuncia en el campo 'Window Size' de sus paquetes TCP la
> cantidad de bytes que su buffer puede recibir antes de colapsar.
</details>


### ❓ Pregunta 18

¿Cual de las siguientes aplicaciones se beneficia mas utilizando el protocolo UDP
en lugar de TCP?
A) Descarga de archivos ejecutables (HTTP)
B) Transmision de llamadas de Voz sobre IP (VoIP)
C) Transferencia de estados de cuenta bancarios (HTTPS)
D) Envio de correos electronicos (SMTP)
<details>
<summary><b>🔍 Ver Respuesta Correcta y Explicación</b></summary>

> **Respuesta Correcta:** `B`  
> **Explicación:** En VoIP y transmisiones en vivo, la latencia y la fluidez son criticas.
> Si un paquete de voz se pierde, no tiene sentido retransmitirlo porque causaria
> eco y tartamudeo en la llamada. UDP no tiene retransmisiones y ofrece minima latencia.
</details>


### ❓ Pregunta 19

¿Cual es el rango de numeros de puerto conocidos como "Puertos Bien Conocidos" (Well-Known Ports)?
A) 0 a 1023
B) 1024 a 49151
C) 49152 a 65535
D) 1 a 255
<details>
<summary><b>🔍 Ver Respuesta Correcta y Explicación</b></summary>

> **Respuesta Correcta:** `A`  
> **Explicación:** 0 a 1023 son Puertos Bien Conocidos (IANA), 1024 a 49151 son Registrados
> y 49152 a 65535 son Dinamicos o Efimeros.

</details>


---

## 📌 BLOQUE 5: CAPAS 5, 6 Y 7 (SESION, PRESENTACION, APLICACION)

### ❓ Pregunta 20

¿En que capa del modelo OSI opera el protocolo SIP (Session Initiation Protocol)
para senalizar y establecer el inicio y fin de una llamada telefonica?
A) Capa 3 (Red)
B) Capa 4 (Transporte)
C) Capa 5 (Sesion)
D) Capa 2 (Enlace)
<details>
<summary><b>🔍 Ver Respuesta Correcta y Explicación</b></summary>

> **Respuesta Correcta:** `C`  
> **Explicación:** SIP es el protocolo estandar de Capa de Sesion que inicia, coordina y
> finaliza sesiones multimedia entre usuarios.
</details>


### ❓ Pregunta 21

¿Cual de las siguientes funciones corresponde exclusivamente a la Capa de Presentacion (Capa 6)?
A) Determinacion de la mejor ruta a traves de la red
B) Deteccion de colisiones en el cable
C) Cifrado de datos, compresion y traduccion de conjuntos de caracteres (ASCII a Unicode)
D) Resolucion de nombres de dominio
<details>
<summary><b>🔍 Ver Respuesta Correcta y Explicación</b></summary>

> **Respuesta Correcta:** `C`  
> **Explicación:** La Capa 6 se ocupa de la sintaxis y representacion de los datos:
> Cifrado (AES/RSA/TLS), Compresion (GZIP) y Codificacion (UTF-8, ASCII).
</details>


### ❓ Pregunta 22

Un administrador de sistemas detecta que su servidor web devuelve el codigo de
estado "HTTP 403". ¿Que significa este error?
A) El servidor se apago o crasheo
B) El recurso solicitado no existe (Not Found)
C) El cliente esta autenticado pero tiene el acceso estrictamente prohibido (Forbidden)
D) La solicitud fue redirigida a HTTPS
<details>
<summary><b>🔍 Ver Respuesta Correcta y Explicación</b></summary>

> **Respuesta Correcta:** `C`  
> **Explicación:** 403 Forbidden indica que el servidor comprendio la solicitud, pero se niega
> a autorizar el acceso al archivo o directorio. (404 = Not Found, 500 = Server Error).
</details>


### ❓ Pregunta 23

En el proceso de asignacion de direcciones IP por DHCP (DORA), ¿cual mensaje envia
el cliente de forma masiva (Broadcast) para formalizar la aceptacion de la IP ofrecida?
A) DHCP Discover
B) DHCP Offer
C) DHCP Request
D) DHCP Acknowledge
<details>
<summary><b>🔍 Ver Respuesta Correcta y Explicación</b></summary>

> **Respuesta Correcta:** `C`  
> **Explicación:** En la fase 3, el cliente envia un `DHCP Request` por broadcast para que
> todos los servidores DHCP que le hicieron ofertas sepan cual IP acepto y liberen las demas.
</details>


### ❓ Pregunta 24

¿Que registro DNS debe configurarse obligatoriamente para dirigir el trafico de
correo electronico hacia los servidores de correo de la organizacion?
A) Registro A
B) Registro CNAME
C) Registro MX (Mail Exchange)
D) Registro PTR
<details>
<summary><b>🔍 Ver Respuesta Correcta y Explicación</b></summary>

> **Respuesta Correcta:** `C`  
> **Explicación:** Los registros MX especifican los nombres de los servidores de correo
> encargados de recibir emails para ese dominio y su respectiva prioridad numerica.
</details>


### ❓ Pregunta 25

¿Cual es la diferencia operativa fundamental entre los protocolos POP3 e IMAP?
A) POP3 envia correos mientras que IMAP los recibe.
B) POP3 descarga los correos en la computadora y los elimina del servidor; IMAP sincroniza carpetas y correos en tiempo real en el servidor.
C) POP3 es cifrado y seguro, mientras que IMAP es en texto plano.
D) No hay diferencia, ambos son identicos.
<details>
<summary><b>🔍 Ver Respuesta Correcta y Explicación</b></summary>

> **Respuesta Correcta:** `B`  
> **Explicación:** IMAP permite sincronizacion multidispositivo centralizada en el servidor;
> POP3 es un protocolo unidireccional heredado que almacena los correos localmente.
</details>


### ❓ Pregunta 26

¿Cual protocolo y numero de puerto utiliza Secure Shell (SSH) para proveer acceso
a la linea de comandos de forma cifrada?
A) UDP 23
B) TCP 23
C) TCP 22
D) TCP 443
<details>
<summary><b>🔍 Ver Respuesta Correcta y Explicación</b></summary>

> **Respuesta Correcta:** `C`  
> **Explicación:** SSH opera sobre el puerto TCP 22 de forma cifrada. (Telnet utiliza el puerto TCP 23 en texto plano).

</details>


---

## 📌 BLOQUE 6: CASOS INTEGRALES Y ESCENARIOS DE CERTIFICACION

### ❓ Pregunta 27

Un usuario no puede cargar una pagina web escribiendo `https://142.250.190.46` en su
navegador, pero la prueba `ping 142.250.190.46` responde con 0% de perdida.
¿En que capas del modelo OSI se encuentra localizada la falla con mayor probabilidad?
A) Capa 1 y Capa 2
B) Capa 3 (Red)
C) Capas 4 a 7 (El puerto TCP 443 esta bloqueado por un firewall o el servidor web esta caido)
D) El cable de red esta danado
<details>
<summary><b>🔍 Ver Respuesta Correcta y Explicación</b></summary>

> **Respuesta Correcta:** `C`  
> **Explicación:** Si el Ping responde exitosamente, las Capas 1, 2 y 3 (Fisica, Enlace y Red)
> estan operando perfectamente. El problema reside en las capas superiores (Capa 4 puerto
> cerrado, o Capa 7 servicio web detenido).
</details>


### ❓ Pregunta 28

¿Que valor de MTU (Maximum Transmission Unit) estandar se utiliza en redes Ethernet
en la Capa de Enlace de Datos para el campo de carga util (Payload)?
A) 64 Bytes
B) 1500 Bytes
C) 1518 Bytes
D) 9000 Bytes
<details>
<summary><b>🔍 Ver Respuesta Correcta y Explicación</b></summary>

> **Respuesta Correcta:** `B`  
> **Explicación:** El MTU estandar de la carga util de Capa 3 dentro de una trama Ethernet es
> de 1500 bytes. 1518 bytes es el tamano maximo de la trama completa incluyendo encabezados.
</details>


### ❓ Pregunta 29

Cuando una computadora envia una solicitud ARP para averiguar la direccion MAC
de su Gateway predeterminado, ¿que direccion MAC destino lleva la trama ARP en Capa 2?
A) La direccion MAC del servidor DNS
B) 00:00:00:00:00:00
C) FF:FF:FF:FF:FF:FF (Broadcast)
D) La direccion IP del Gateway
<details>
<summary><b>🔍 Ver Respuesta Correcta y Explicación</b></summary>

> **Respuesta Correcta:** `C`  
> **Explicación:** Como la PC desconoce que tarjeta de red posee esa direccion IP, debe enviar
> una peticion de difusion (Broadcast) con MAC destino `FF:FF:FF:FF:FF:FF` para que
> todos los equipos de la LAN la procesen y el dueno legitimo responda.
</details>


### ❓ Pregunta 30

¿Que mecanismo de seguridad en switches inspecciona las tramas de Capa 2 contra
la tabla de la Capa 3 de DHCP para prevenir ataques de envenenamiento de tablas ARP?
A) BPDU Guard
B) Port Security
C) Dynamic ARP Inspection (DAI)
D) Spanning Tree
<details>
<summary><b>🔍 Ver Respuesta Correcta y Explicación</b></summary>

> **Respuesta Correcta:** `C`  
> **Explicación:** DAI (Dynamic ARP Inspection) valida los paquetes ARP entrantes en puertos
> no confiables contrastandolos contra la base de datos de enlaces IP-MAC generada por
</details>

## DHCP Snooping.

