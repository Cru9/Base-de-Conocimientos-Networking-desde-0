# 03. CONTROL DE TASA: TRAFFIC POLICING vs TRAFFIC SHAPING

> **CALIDAD DE SERVICIO Y CONFORMACION DE TRAFICO (QOS & TRAFFIC SHAPING)**


---



## 1. CUADRO COMPARATIVO FUNDAMENTAL

Cuando se necesita limitar el consumo de ancho de banda de un cliente, subred o enlace,
existen dos filosofias tecnicas radicalmente distintas:


| Caracteristica | Traffic Policing (Regulacion) | Traffic Shaping (Conformacion) |
| :--- | :--- | :--- |
| Accion ante exceso | Descarta o remarca paquetes | Almacena en buffer y suaviza |
| Uso de memoria buffer | NO utiliza buffers de retencion | SI utiliza colas de memoria RAM |
| Efecto en la latencia | CERO latencia o jitter anadido | Introduce retardo y jitter |
| Direccion aplicable | Entrada (Ingress) y Salida (Egress) SOLO Salida (Egress) |  |
| Perfil de trafico | Corte abrupto ("dientes de sierra") Flujo constante y redondeado |  |
| Quien lo suele usar | Proveedores de Internet (ISPs) | Routers de borde del cliente (CPE) |




## 2. EL ALGORITMO "TOKEN BUCKET" (EL CUBO DE FICHAS)

Tanto Policing como Shaping utilizan el modelo matematico del Token Bucket:
- Imagina un cubo con una capacidad fija de fichas (Tokens).
- El sistema arroja fichas al cubo a una velocidad constante predefinida (CIR).
- Cada ficha representa el derecho a transmitir un numero determinado de bits o bytes.
- Cuando un paquete de datos llega a la interfaz:
  * Si hay suficientes fichas en el cubo, el paquete consume las fichas y se transmite.
  * Si el cubo esta vacio:
    - En Policing: El paquete es DESCARTADO de inmediato (o remarcado a un DSCP menor).
    - En Shaping: El paquete se guarda en un buffer de memoria RAM hasta que el cubo
      reciba nuevas fichas en el siguiente ciclo de reloj.

PARAMETROS MATEMATICOS DEL TOKEN BUCKET:
- CIR (Committed Information Rate): Tasa contratada o garantizada en bits por segundo.
- Bc (Committed Burst): Cantidad maxima de bits que pueden acumularse en el cubo en un instante.
- Be (Excess Burst): Capacidad de un segundo cubo para permitir rafagas temporales de exceso.
- Tc (Time Interval - Intervalo de Tiempo): Frecuencia con la que el sistema recarga fichas.
  Formula fundamental: Tc = Bc / CIR
  Ejemplo: Si CIR = 10,000,000 bps (10 Mbps) y Bc = 125,000 bits:
  Tc = 125,000 / 10,000,000 = 0.0125 segundos = 12.5 milisegundos.



## 3. MARCADORES DE DOS TASAS Y TRES COLORES (TWO-RATE THREE-COLOR MARKER / RFC 2698)

Utilizado comunmente en firewalls e ISPs para clasificar el trafico en 3 colores:

- Verde (Conforming / En conformidad):
  El flujo esta dentro del ancho de banda contratado (CIR). Se transmite sin tocar.

- Amarillo (Exceeding / En exceso):
  El flujo supera el CIR pero esta dentro del limite de rafaga maxima permitida (PIR).
  Accion: Se transmite pero se REMARCA hacia abajo (ej. de AF21 a AF23), lo que indica
  que los conmutadores siguientes podran descartarlo si se produce congestion.

- Rojo (Violating / En infraccion):
  El flujo supera tanto el CIR como el PIR.
  Accion: Se descarta inmediatamente (Drop).



## 4. EL CASO TIPICO DE DISENO: ACCESO WAN DE TASA INFERIOR (SUB-RATE ACCESS)

Escenario Real de Produccion:
- Una empresa contrata un enlace de fibra con un proveedor de Internet (ISP).
- El puerto fisico de fibra es de 1 Gbps (1000 Mbps).
- Sin embargo, la empresa solo paga por un plan de 100 Mbps (Sub-rate).
- En el extremo del proveedor, el switch del ISP tiene configurado un POLICER a 100 Mbps.

¿Que ocurre si el router del cliente no tiene QoS configurado?
- Si un servidor interno envia datos a 1 Gbps, las rafagas chocaran contra el
  POLICER del ISP.
- El ISP descartara abruptamente el 90% de los paquetes excedentes.
- Consecuencia: Las sesiones TCP entraran en retransmisiones masivas, el rendimiento
  caera a 5 Mbps y los usuarios sentiran que la red "se congela".

LA SOLUCION ARQUITECTONICA: SHAPING EN EL ROUTER DEL CLIENTE:
- El ingeniero de red de la empresa DEBE configurar TRAFFIC SHAPING a 100 Mbps
  en la interfaz WAN de salida de su propio router.
- El router del cliente retiene las rafagas en sus propios buffers de memoria RAM
  y dosifica la salida de paquetes a un flujo perfectamente constante de 100 Mbps.
- Como el trafico nunca supera los 100 Mbps en el cable, el POLICER del ISP NUNCA

se activa y no se pierde ni un solo paquete.
