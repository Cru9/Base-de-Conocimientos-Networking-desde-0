# 02. DIAGNOSTICO Y RESOLUCION DE FALLAS TCP (TCP EXPERT Y FLUJO)

> **ANALISIS FORENSE DE PAQUETES CON WIRESHARK (WIRESHARK_ANALYSIS)**


---



## 1. EL MOTOR DE ANALISIS INTELIGENTE DE WIRESHARK (TCP EXPERT INFO)

TCP es un protocolo orientado a conexion, con control de congestion y entrega
confiable. Wireshark analiza el flujo de numeros de secuencia (Sequence Numbers)
y confirmaciones de recepcion (Acknowledgement Numbers), alertando con colores
y etiquetas especiales cuando detecta anomalías.

Opciones de Visualizacion Clave en Wireshark:
- Ir a: `Analyze -> Expert Information`.
- Colores por severidad:
  * Rojo (Chatter/Error): Conexiones cortadas (RST), Zero Window.
  * Azul claro (Note): Retransmisiones clasicas, ACKs duplicados.
  * Amarillo (Warning): Retransmisiones rapidas, segmentos perdidos.



## 2. ANOMALIAS DE PERDIDA Y RETRANSMISION DE PAQUETES


### a) [TCP Retransmission]:

   - Filtro: `tcp.analysis.retransmission`
   - ¿Que ocurrio? El emisor envio un paquete de datos, inicio un temporizador
     RTO (Retransmission Timeout) y dicho temporizador expiro antes de recibir el ACK.
     Por tanto, el emisor vuelve a transmitir el mismo bloque de datos.
   - Diagnostico:
     * Enlaces WAN o Wi-Fi con interferencia o saturacion de ancho de banda.
     * Descarte por politicas de policer/shaper o buffers saturados en switches.
     * Un firewall intermedio descarto el paquete silenciosamente (Drop).


### b) [TCP Fast Retransmission] y [TCP Dup ACK]:

   - Filtros: `tcp.analysis.fast_retransmission` y `tcp.analysis.duplicate_ack`
   - ¿Que ocurrio? El algoritmo Fast Retransmit (RFC 5681) entra en accion cuando
     se pierden paquetes intermedios:
     * Si el servidor envio los paquetes 1, 2, 3, 4 y el paquete 2 se perdio:
     * El cliente recibe el 1 (ACK 2), pero luego recibe el 3 y el 4.
     * Como el cliente NO puede confirmar el 3 ni el 4 sin haber recibido el 2,
       repite inmediatamente la confirmacion del ultimo byte contiguo recibido
       ("Dup ACK: sigo esperando el paquete 2").
     * Al recibir el tercer Dup ACK consecutivo, el emisor NO espera al temporizador
       lento RTO y retransmite inmediatamente el paquete 2 (Fast Retransmission).
   - Diagnostico: Perdida aislada de paquetes en transito sin congelar la conexion.


### c) [TCP Out-of-Order]:

   - Filtro: `tcp.analysis.out_of_order`
   - ¿Que ocurrio? Un paquete llego con un numero de secuencia menor al esperado,
     pero dentro de la ventana valida.
   - Diagnostico:
     * Enrutamiento asimetrico o balanceo multipath (ECMP) defectuoso donde los
       paquetes de una misma sesion tomaron caminos fisicos de diferente velocidad.



## 3. CONTROL DE FLUJO Y CRISIS DE VENTANA (WINDOW SIZE ISSUES)

El campo Window Size en la cabecera TCP le indica al emisor: "¿Cuantos bytes puede
almacenar mi buffer de memoria RAM antes de que me satures?".


### a) Factor de Escala de Ventana (Window Scale - RFC 7323):

   - El campo original en la cabecera TCP es de solo 16 bits (maximo 65,535 bytes).
   - Para conexiones gigabit modernas, durante el 3-way handshake (SYN / SYN-ACK)
     ambos extremos negocian la opcion `Window Scale (wscale)` para multiplicar
     el valor y permitir ventanas de hasta 1 Gigabyte.
   - ¡CUIDADO!: Para que Wireshark calcule correctamente el tamano de ventana real,
     DEBE haber capturado el inicio de la conexion (SYN). Si se inicio la captura
     con la sesion ya en curso, Wireshark marcara [TCP window size unknown].


### b) [TCP Window Full]:

   - Filtro: `tcp.analysis.window_full`
   - ¿Que ocurrio? El emisor transmitio tantos bytes que lleno el 100% de la ventana
     anunciada por el receptor (`Bytes in Flight == Window Size`).
   - Consecuencia: El emisor entra en pausa obligatoria y la transferencia se congela
     hasta que el receptor envia un paquete confirmando que proceso los datos.


### c) [TCP ZeroWindow] - LA ALERTA MAS GRAVE DE SERVIDOR:

   - Filtro: `tcp.analysis.zero_window`
   - ¿Que ocurrio? El receptor anuncia explicitamente: `Window Size = 0`.
   - Diagnostico:
     * ¡NO ES UN PROBLEMA DE RED!
     * Es un problema critico en el host de destino (Servidor o Base de Datos).
     * El sistema operativo del servidor tiene el buffer de sockets de la RAM lleno
       al 100% porque el proceso de la aplicacion (ej. Java Tomcat, MySQL, Python)
       esta congelado, sufriendo un bloqueo (Lock/Deadlock), saturacion de CPU al 100%
       o una pausa de Garbage Collection (GC) y no puede leer datos del socket.


### d) [TCP ZeroWindowProbe] y [TCP ZeroWindowProbeAck]:

   - Filtro: `tcp.analysis.zero_window_probe`
   - El emisor envia periodicamente 1 byte de prueba para preguntar: "¿Ya tienes memoria libre?".
   - El receptor responde con ZeroWindowProbeAck indicando si sigue en cero o si ya abrio ventana.



## 4. METODOLOGIA CIENTIFICA: ¿LA CULPA ES DE LA RED O DE LA APLICACION?

Cuando los usuarios reclaman: "El sistema esta lentisimo, la red no sirve", el analista
de paquetes utiliza las metricas de tiempo de Wireshark para demostrar matematicamente
el origen del cuello de botella.

PASO 1: Medir la Latencia de Red (Network Round-Trip Time - RTT):
- Se inspecciona el 3-way handshake inicial:
  * Paquete 1: Cliente -> Servidor (SYN)         [Tiempo: 0.000000 s]
  * Paquete 2: Servidor -> Cliente (SYN-ACK)     [Tiempo: 0.005120 s]
- Calculo de Latencia de Red:
  RTT = 0.005120 s = 5.1 milisegundos.
- Conclusion: La red fisica, enlaces de fibra, routers y firewalls tardan solo
  5 milisegundos en ir y regresar.

PASO 2: Medir la Latencia de la Aplicacion (Server Processing Time / TTFB):
- Se inspecciona la peticion de la aplicacion y su primera respuesta:
  * Paquete 10: Cliente -> Servidor (HTTP GET /api/facturas) [Tiempo: 1.100000 s]
  * Paquete 11: Servidor -> Cliente (TCP ACK del paquete 10) [Tiempo: 1.105200 s]
    (El switch y la tarjeta de red del servidor confirmaron recepcion en 5 ms).
  * Paquete 12: Servidor -> Cliente (HTTP 200 OK con datos)   [Tiempo: 5.605200 s]
- Calculo del Tiempo de Proceso del Servidor:
  Delta = 5.605200 s - 1.105200 s = 4.500000 segundos.

CONCLUSION FORENSE IRREFUTABLE:
- De los 4.505 segundos que tardo la operacion:
  * La Red consumio: 5.1 milisegundos (0.11% del tiempo total).
  * El Servidor / Base de Datos consumio: 4.5 segundos (99.89% del tiempo total).

## - La falla reside en una consulta SQL no indexada o codigo ineficiente en el servidor.
