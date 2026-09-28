# 01. PROTOCOLOS INDUSTRIALES: MODBUS, PROFINET, ETHERNET/IP, DNP3 Y OPC UA

> **REDES INDUSTRIALES Y CIBERSEGURIDAD OT / SCADA (OPERATIONAL TECHNOLOGY)**


---



## 1. EL PROTOCOLO MODBUS (EL LENGUAJE UNIVERSAL DE LA INDUSTRIA)

Disenado por Modicon en 1979, Modbus es el protocolo industrial mas extendido
del mundo debido a su simplicidad. Opera bajo arquitectura Maestro/Esclavo
(Cliente/Servidor).


### a) Modbus RTU (Serial):

   - Se transmite sobre cableado serial RS-485 (par trenzado a 9600 o 19200 baudios).
   - Estructura de la Trama:
```text
     [ Direccion Esclavo (1 byte) | Codigo de Funcion (1 byte) | Datos | CRC-16 (2 bytes) ]

b) Modbus TCP (Ethernet / IP):
   - Encapsula las solicitudes Modbus sobre paquetes TCP/IP en el Puerto TCP 502.
   - Elimina la direccion serial y el CRC, sustituyendolos por la cabecera MBAP
     (Modbus Application Protocol Header de 7 bytes):
     * Transaction ID (2 bytes): Identificador de transaccion.
     * Protocol ID (2 bytes): Siempre 0 para Modbus.
     * Length (2 bytes): Longitud de los bytes siguientes.
     * Unit ID (1 byte): Identificador de la sub-unidad o esclavo remoto.
```


c) Codigos de Funcion Modbus Mas Importantes (Function Codes):


| Codigo Funcion | Hex | Tipo de Accion | Descripcion |
| :--- | :--- | :--- | :--- |
| 01 | 0x01 | Read Coils | Lee el estado de salidas digitales (ON/OFF) |
| 02 | 0x02 | Read Discrete Inputs Lee el estado de entradas digitales fisicas |  |
| 03 | 0x03 | Read Holding Regs | Lee registros analogicos de configuracion |
| 04 | 0x04 | Read Input Regs | Lee mediciones de sensores (Temperatura/Presion) |
| 05 | 0x05 | Write Single Coil | ¡PELIGRO! Fuerza el encendido/apagado de una salida |
| 06 | 0x06 | Write Single Reg | ¡PELIGRO! Modifica el valor de un registro analogico |
| 15 | 0x0F | Write Mult. Coils | Escribe multiples salidas booleanas a la vez |
| 16 | 0x10 | Write Mult. Regs | Escribe multiples registros de parametros |


LA VULNERABILIDAD INTRINSECA DE MODBUS:
- Modbus fue disenado cuando las redes estaban completamente aisladas del mundo exterior.
- ¡NO POSEE AUTENTICACION, NO POSEE CIFRADO Y NO POSEE INTEGRIDAD!
- Cualquier atacante que logre alcanzar la IP de un PLC sobre el puerto TCP 502 puede
  emitir un paquete con Funcion 05 o 06 y abrir una valvula de gas o apagar las
  bombas de refrigeracion instantaneamente sin necesidad de ingresar ninguna clave.



## 2. PROFINET (PROCESS FIELD NET - ESTANDAR SIEMENS / PI)

Profinet es el estandar lider en Europa y en plantas automotrices y de manufactura.

Diferencia entre sus 3 Canales de Comunicacion:

### a) Profinet NRT (Non-Real-Time):

   - Utiliza la pila estandar TCP/IP y UDP (puertos 34962 a 34964).
   - Utilizado para parametrizacion, descarga de programas al PLC y diagnostico (~100 ms).


### b) Profinet RT (Real-Time - Tiempo Real por Software):

   - ¡SALTA LA PILA TCP/IP! Las tramas se inyectan DIRECTAMENTE en la Capa 2 Ethernet
     (EtherType 0x8892 con prioridad VLAN CoS 6).
   - Elimina la sobrecarga de IP y TCP, logrando tiempos de ciclo de 1 a 10 milisegundos.


### c) Profinet IRT (Isochronous Real-Time - Tiempo Real Isocrono por Hardware):

   - Disenado para robotica de alta velocidad y control de movimiento sincrono (Motion Control).
   - Utiliza ASICs dedicados (ERTEC) y sincronizacion de reloj sub-microsegundo
     mediante IEEE 1588 PTP (Precision Time Protocol).
   - El ancho de banda del cable de 100 Mbps se divide en ranuras de tiempo fijas (Time Slots).
   - Jitter determinista: ¡MENOR A 1 MICROSEGUNDO!



## 3. ETHERNET/IP Y CIP (COMMON INDUSTRIAL PROTOCOL - ROCKWELL / ODVA)

Estandar dominante en Estados Unidos y America Latina en plantas con tecnologia Allen-Bradley:
- Utiliza la red Ethernet estandar pero implementa CIP (Common Industrial Protocol)
  en la capa de aplicacion.
- Opera sobre el Puerto TCP/UDP 44818.
- Tipos de Mensajes:
  * Mensajes Explicitos (TCP 44818): Para lectura de etiquetas (Tags), configuracion
    y consulta de diagnosticos bajo demanda.
  * Mensajes Implicitos / E/S (UDP 2222): Flujo continuo de paquetes UDP que transporta
    los estados de entradas y salidas de sensores a alta velocidad en tiempo real.



## 4. DNP3 Y PROTOCOLOS PARA REDES ELECTRICAS (SUBESTACIONES)

En subestaciones de transmision electrica, plantas hidroelectricas y redes de agua:
- DNP3 (Distributed Network Protocol / IEEE 1815): Opera sobre TCP 20000.
- IEC 60870-5-104: Opera sobre TCP 2404.
- IEC 61850: Estandar moderno para automatizacion de subestaciones electricas.
  Introduce tramas GOOSE (Generic Object Oriented Substation Events) que viajan
  directamente en Capa 2 para disparar la apertura de interruptores de alta tension
  en menos de 4 milisegundos ante un cortocircuito.



## 5. PROTOCOLOS MODERNOS DE IIoT E INDUSTRIA 4.0: OPC UA Y MQTT


### a) OPC UA (Open Platform Communications Unified Architecture - IEC 62541):

   - El sustituto seguro y moderno del antiguo OPC basado en Microsoft DCOM.
   - Es completamente multiplataforma (corre en Linux, Windows, RTOS embebidos).
   - Modelo de datos orientado a objetos.
   - SEGURIDAD NATIVA: Cifrado TLS estricto, autenticacion mediante certificados
     digitales X.509 y firmas digitales en cada paquete. Es el puente oficial
     entre la red OT de planta (Nivel 3) y la red IT (Nivel 4).


### b) MQTT (Message Queuing Telemetry Transport - TCP 1883 / 8883 TLS):

   - Arquitectura ligera de Publicacion/Suscripcion (Pub/Sub) con Broker central.
   - Ideal para sensores remotos de baterias o telemetria en oleoductos conectados

mediante enlaces celulares o satelitales estrechos.
