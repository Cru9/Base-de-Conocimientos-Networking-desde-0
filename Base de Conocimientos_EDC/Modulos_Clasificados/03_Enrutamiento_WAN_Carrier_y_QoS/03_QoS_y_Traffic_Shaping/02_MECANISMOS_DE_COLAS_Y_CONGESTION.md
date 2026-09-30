# 02. MECANISMOS DE PLANIFICACION DE COLAS Y CONTROL DE CONGESTION

> **CALIDAD DE SERVICIO Y CONFORMACION DE TRAFICO (QOS & TRAFFIC SHAPING)**


---



## 1. ¿DONDE OCURRE LA CONGESTION EN UN ROUTER O SWITCH?

La congestion ocurre fisicamente en los buffers de las interfaces de salida (Egress).
Ejemplo clasico: El router recibe trafico desde una interfaz LAN a 10 Gbps pero
debe reenviarlo a traves de un enlace WAN o Internet de solo 100 Mbps.
Los paquetes que no pueden transmitirse instantaneamente deben almacenarse en la
memoria RAM de la interfaz (Colas de salida / Output Queues).

El mecanismo de planificacion (Queue Scheduling) determina que paquete en cola
tiene derecho a salir primero al cable.



## 2. ALGORITMOS DE PLANIFICACION DE COLAS (SCHEDULING)


### a) FIFO (First-In, First-Out):

   - Una sola cola compartida.
   - El primer paquete que entra es el primero que sale, sin importar su tipo.
   - Peligro: Una descarga masiva de Windows Update llena la cola e introduce
     cientos de milisegundos de latencia en una llamada telefonica contigua.


### b) PQ (Priority Queuing - Prioridad Estricta):

   - Cuatro colas jerarquicas: High, Medium, Normal, Low.
   - La cola High siempre se vacia antes de permitir que la cola Medium envie
     un solo paquete.
   - Peligro de Inanicion (Starvation): Si la cola High recibe trafico continuo,
     las demas colas NUNCA transmiten y los usuarios experimentan desconexiones totales.


### c) CBWFQ (Class-Based Weighted Fair Queuing):

   - El administrador define clases de trafico personalizadas (ej. Bases de datos,
     Trafico Web, Correo).
   - A cada clase se le garantiza un porcentaje minimo de ancho de banda
     (ej. 30% para SAP, 20% para Web, 10% para Correo).
   - Si una clase no esta utilizando su ancho de banda asignado, las demas clases
     pueden aprovecharlo dinamicamente.


### d) LLQ (LOW LATENCY QUEUING) - EL ESTANDAR ABSOLUTO DE LA INDUSTRIA:

   - Resuelve el problema historico de combinar Voz con Datos.
   - LLQ es la union perfecta entre:
     * Una cola de Prioridad Estricta (PQ) para trafico en tiempo real (Voz / DSCP EF).
     * Multiples colas CBWFQ para el resto del trafico corporativo.

```text
                    +--------------------------------------------+
                    | Cola de Prioridad Estricta (Voz / DSCP EF) | ---> [Salida Inmediata]
                    +--------------------------------------------+            ^
                                                                              |
                    +--------------------------------------------+            |
                    | Cola CBWFQ 1 (Datos Criticos / ERP 30%)    | -----------+
                    +--------------------------------------------+            |
                                                                              |
                    +--------------------------------------------+            |
                    | Cola CBWFQ 2 (Trafico General / Web 20%)   | -----------+
                    +--------------------------------------------+            |
                                                                              |
                    +--------------------------------------------+            |
                    | Cola Best Effort (Por defecto / Resto)     | -----------+
                    +--------------------------------------------+

   - PROTECCION CONTRA INANICION EN LLQ (Built-in Policer):
     Para evitar que un flujo de voz defectuoso o un ataque ahogue al resto de la red,
     la cola prioritaria de LLQ tiene un limitador estricto (ej. `priority 512` Kbps).
     Si el trafico de voz excede ese ancho de banda, el excedente se descarta
     sin afectar jamas a las colas CBWFQ de datos.
```


## 3. EVITACION DE CONGESTION: TAIL DROP vs WRED


### a) Tail Drop (Descarte de Cola - El Problema por Defecto):

   - Cuando el buffer de la interfaz se llena al 100%, todos los paquetes nuevos que
     llegan son descartados en la cola ("Tail Drop").
   - FENOMENO DEVASTADOR: SINCRONIZACION GLOBAL DE TCP (TCP Global Synchronization):
     1. El buffer se llena al 100% y descarta paquetes de cientos de sesiones TCP al mismo tiempo.
     2. Cientos de servidores y clientes experimentan perdida de paquetes simultanea.
     3. Todos los emisores TCP reducen su ventana de transmision a la mitad exactamente
        en el mismo segundo.
     4. El enlace WAN cae abruptamente del 100% de saturacion al 10% de uso (queda vacio).
     5. Todos los emisores vuelven a incrementar su velocidad simultaneamente hasta
        volver a llenar el buffer al 100%.
     6. Se genera un ciclo vicioso de oscilacion violenta ("ola marina") que destruye el Throughput.


### b) WRED (Weighted Random Early Detection - Deteccion Temprana Ponderada):

   - Evita la sincronizacion global descartando paquetes de forma aleatoria ANTES
     de que el buffer se llene al 100%.
   - Al descartar paquetes aislados de unas pocas sesiones TCP, solo esos clientes
     reducen su velocidad temporalmente, manteniendo el enlace al 95% de uso constante.
   - Ponderacion por Prioridad (Weighted):
     * WRED examina el campo DSCP / IP Precedence del paquete.
     * Paquetes de baja prioridad (ej. DSCP 0 o AF13) tienen umbrales de descarte muy bajos
       (empiezan a descartarse al 40% de llenado del buffer).
     * Paquetes de alta prioridad (ej. AF11 o AF21) solo se descartan si el buffer
       supera el 85% de llenado.
   - REGLA DE ORO: ¡WRED NUNCA se aplica a la cola de voz (LLQ)! La voz no utiliza TCP,

por lo que no responde reduciendo ventanas; descartar paquetes de voz solo destruye el audio.
