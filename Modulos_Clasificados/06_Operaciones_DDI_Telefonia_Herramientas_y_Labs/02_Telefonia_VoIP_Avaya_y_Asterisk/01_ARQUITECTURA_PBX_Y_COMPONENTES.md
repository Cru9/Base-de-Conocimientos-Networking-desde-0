# 01. ARQUITECTURA DEL PBX, TRONCALES, EXTENSIONES Y PLANES DE MARCACION

> **TELEFONIA EMPRESARIAL Y VOZ SOBRE IP (VOIP)**


---



## 1. ¿QUE ES UN PBX (PRIVATE BRANCH EXCHANGE) Y UN IP-PBX?

Un PBX (comunmente llamado "Conmutador Telefonico") es una central telefonica
privada propiedad de la empresa. Cumple tres funciones fundamentales:
1. Conmutar llamadas internas entre empleados de forma 100% gratuita sin usar lineas publicas.
2. Compartir un numero reducido de lineas telefonicas externas (Troncales) entre
   cientos de extensiones de la oficina.
3. Brindar servicios avanzados de gestion de llamadas (Operadora automatica IVR,
   buzones de voz, grabacion, transferencias, conferencias y reportes de tarificacion).



## 2. BLOQUES FUNDAMENTALES DE UN SISTEMA TELEFONICO



## A) EXTENSIONES / ANEXOS (LOS PUNTOS FINALES):

Es el numero interno asignado a un usuario o telefono (ej. Extension 201).
- Extensiones IP (H.323 o SIP): Telefonos que se conectan al switch mediante cable
  Ethernet y utilizan direcciones IP.
- Extensiones Digitales: Telefonos propietarios de dos hilos (como Avaya serie 1400/9500)
  que viajan sobre cobre convencional hasta tarjetas digitales del conmutador.
- Extensiones Analogicas: Telefonos convencionales (POTS) o maquinas de Fax.


## B) TRONCALES (TRUNKS - LAS VIAS DE ENTRADA Y SALIDA A LA CALLE):

1. Troncal SIP (SIP Trunk - La Tecnologia Dominante):
   - Enlace logico de voz contratado con un operador ITSP (Internet Telephony Service Provider).
   - Viaja sobre la conexion de fibra o Internet mediante paquetes IP.
   - Ventajas: Escalabilidad instantanea (puedes contratar de 5 a 500 canales concurrentes
     sin tender un solo cable fisico nuevo), costo muy reducido y asignacion de cientos
     de numeros publicos directos (DID / DDI).

2. Troncal Digital E1 / PRI (Primary Rate Interface):
   - Enlace fisico digital clasico sobre cable coaxial o par trenzado blindado de 120 ohms.
   - Estructura: 32 ranuras de tiempo (Timeslots) a 2.048 Mbps:
     * 30 Canales B (Bearer Channels): transportan 30 llamadas simultaneas a 64 Kbps (G.711).
     * 1 Canal D (Data Channel / Canal 16): transporta la senalizacion de llamada (ISDN Q.931).
     * 1 Canal de sincronizacion y tramas (Canal 0).

3. Troncales Analogicas (Lineas de Cobre de la Calle / FXO):
   - Cada linea de cobre fisica solo permite UNA llamada a la vez.



## 3. LA DIFERENCIA DE ORO EN TELEFONIA: FXS vs FXO

CONFUSION FRECUENTE: ¿Cual es la diferencia entre un puerto FXS y uno FXO?

Puerto FXS (Foreign eXchange Station):
- ES EL PUERTO QUE ENTREGA LA LINEA.
- Genera el tono de invitacion a marcar, suministra voltaje de corriente continua
  (-48V DC en reposo) y envia el voltaje alterno de campanilla (90V AC a 20 Hz) para
  hacer timbrar el telefono.
- ¿Que se conecta a un puerto FXS?: Telefonos analogicos convencionales, aparatos
  de Fax y terminales de tarjeta bancaria (POS).

Puerto FXO (Foreign eXchange Office):
- ES EL PUERTO QUE RECIBE LA LINEA.
- Se comporta como un telefono: detecta el tono de marcado y simula el descolgado
  cerrando el circuito de corriente.
- ¿Que se conecta a un puerto FXO?: La linea de cobre fisica que viene del poste
  de la compania telefonica publica.

REGLA MNEMOTECNICA UNIVERSAL:
"FXS Suministra (Supplies) el tono | FXO Obtiene (Obtains) el tono".
Siempre se debe conectar un puerto FXS con un puerto FXO.



## 4. GRUPOS DE BUSQUEDA Y TIMBRADO (HUNT GROUPS)

Permiten distribuir llamadas entrantes dirigidas a un solo numero publico
(ej. 55-1234-5678 para el departamento de "Ventas") entre un grupo de operadores.

Metodos de Distribucion de Llamadas:
- Colectivo (Collective / Ring-All): Todos los telefonos del grupo timbran al
  mismo tiempo; el primer operador que descuelga se queda con la llamada.
- Secuencial (Sequential / Linear): Timbra primero la Extension A; si no contesta
  en 15 segundos, salta a la Extension B, y luego a la C.
- Rotativo (Rotary / Circular): Distribuye en circulo; si la ultima llamada la tomo
  la Extension B, la siguiente llamada empezara timbrando en la Extension C.
- Mas Tiempo Inactivo (Longest Waiting / Longest Idle): La llamada se entrega
  automaticamente al operador que lleva mas minutos desocupado sin atender llamadas.



## 5. OPERADORA AUTOMATICA (IVR / AUTO-ATTENDANT)

Sistema de respuesta de voz interactiva que guia al cliente externo mediante tonos DTMF:
- "Bienvenido a Empresa ABC. Si conoce el numero de extension marquelo ahora.
   Para Ventas marque 1. Para Soporte marque 2. Para hablar con recepcion marque 0."
- Permite programar horarios laborales (Horario Diurno) y desviar llamadas a un
  mensaje de fuera de oficina o guardia tecnica durante las noches y fines de semana (Horario Nocturno).



## 6. BUZON DE VOZ Y MENSAJERIA UNIFICADA (VOICEMAIL TO EMAIL)

- Cada extension posee su propio buzon digital protegido por PIN numerico.
- Mensajeria Unificada (Unified Messaging): En cuanto un cliente deja un mensaje
  de voz, el PBX convierte el audio en un archivo `.wav` adjunto y lo envia
  automaticamente al correo electronico corporativo del empleado (Outlook/Gmail).



## 7. CDR (CALL DETAIL RECORDS) Y TARIFICACION

Flujo de datos en tiempo real que emite el PBX por red o puerto serial (SMDR):
- Registra: Fecha, hora exacta, extension origen, numero marcado, duracion de
  la llamada, linea troncal utilizada y codigo de cuenta.

## - Esencial para facturacion departamental, auditoria de costos y deteccion de fraude telefonico.
