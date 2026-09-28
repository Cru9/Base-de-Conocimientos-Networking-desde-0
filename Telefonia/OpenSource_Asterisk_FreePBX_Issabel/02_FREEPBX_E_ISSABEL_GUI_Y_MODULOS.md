# ASTERISK, FREEPBX E ISSABEL

> **TELEFONIA DE CODIGO ABIERTO (OPEN SOURCE VOIP)**

> *02. ARQUITECTURA WEB: MODULOS FUNDAMENTALES DE FREEPBX E ISSABEL*


---



## 1. LA INTERFAZ GRAFICA MODULAR (FREEPBX / ISSABEL GUI)

Tanto FreePBX como Issabel eliminan la necesidad de editar archivos `.conf` a mano.
La interfaz web almacena toda la configuracion en una base de datos MariaDB/MySQL
y, al hacer clic en el boton rojo superior "Apply Config" (Aplicar Cambios),
ejecuta scripts que generan los archivos de configuracion oficiales para Asterisk
y recargan el servicio en milisegundos sin interrumpir llamadas activas.



## 2. LOS 10 MODULOS FUNDAMENTALES DE LA CENTRAL TELEFONICA


1. EXTENSIONES (APPLICATIONS -> EXTENSIONS):
   - Creacion de cuentas para usuarios finales.
   - Tipos de extension:
     * `PJSIP Extension` (Recomendada): Soporta multiples dispositivos en paralelo,
       cifrado WebRTC y transporte moderno.
     * `Virtual Extension`: Extension sin telefono fisico, utilizada para desviar
       llamadas a numeros de celular externos o buzones compartidos.

2. TRONCALES (CONNECTIVITY -> TRUNKS):
   - Conexiones hacia los proveedores de telefonia publica (ITSP / Carriers).
   - Tipos principales:
     * `PJSIP Trunk`: Troncal SIP autenticada por usuario/clave o autorizada por IP fija.
     * `IAX2 Trunk` (Inter-Asterisk eXchange): Protocolo super-eficiente exclusivo
       de Asterisk para enlazar dos conmutadores remotos (utiliza un solo puerto UDP 4569
       tanto para senalizacion como para audio RTP, eliminando todo problema de NAT).

3. RUTAS SALIENTES (CONNECTIVITY -> OUTBOUND ROUTES):
   - Gobierna que troncal utilizar cuando un usuario marca hacia el exterior.
   - Secuencia de Troncales (Trunk Sequence):
     * Permite definir redundancia automatica (Failover): Si la Troncal SIP 1 esta
       saturada o caida, el conmutador prueba automaticamente la Troncal SIP 2.
   - Codigos de Marcacion (Dial Patterns):
     * Prefijo (Prefix): Se elimina antes de enviar al carrier (ej. marcar `9` para salir).
     * Coincidencia (Match Pattern): La cantidad de digitos validos (ej. `NXXXXXXXXX`).
     * PIN Sets: Permite exigir una contrasena numerica a los usuarios antes de
       permitir llamadas a celulares o larga distancia internacional.

4. RUTAS ENTRANTES (CONNECTIVITY -> INBOUND ROUTES):
   - Controla que ocurre cuando entra una llamada externa desde el operador.
   - Enrutamiento por DID (Direct Inward Dialing): Si el cliente llamo al `5512345678`,
     se envia a la Operadora Automatica (IVR); si llamo al `5512345679`, se envia
     directamente al escritorio del Director General.
   - Enrutamiento por CallerID: Si llama un cliente VIP especifico, salta la cola
     y timbra en la extension de su ejecutivo de cuenta personal.

5. GRUPOS DE TIMBRADO (APPLICATIONS -> RING GROUPS):
   - Hace sonar un conjunto de telefonos al mismo tiempo para un departamento (ej. Soporte).
   - Estrategias de Timbrado:
     * `ringall`: Todos los telefonos timbran a la vez.
     * `hunt`: Timbra uno por uno secuencialmente.
     * `memoryhunt`: Timbra la extension 1; luego timbran la 1 y la 2 juntas; luego 1, 2 y 3.
   - Destino sin respuesta: Si nadie atiende en 20 segundos, la llamada se transfiere
     al buzon de voz o a una cola de atencion.

6. COLAS DE ATENCION (APPLICATIONS -> QUEUES):
   - El motor de atencion al cliente para Call Centers y Mesas de Ayuda.
   - Retiene a los usuarios en espera con musica, informando su posicion en la fila
     ("Usted es el cliente numero 3 en la cola, tiempo estimado 2 minutos").
   - Agentes Estaticos vs Dinamicos:
     * Un agente dinamico puede llegar a cualquier escritorio y teclear `101*` para
       iniciar turno en la cola, y `101**` para salir a comer.
   - Estrategias de Distribucion:
     * `leastrecent`: Entrega la llamada al agente que hace mas tiempo atendio una llamada.
     * `fewestcalls`: Entrega la llamada al agente que menos llamadas ha recibido en el dia.
     * `random`: Distribucion aleatoria pura.

7. OPERADORA AUTOMATICA (APPLICATIONS -> IVR):
   - Menu de bienvenida interactivo por voz.
   - Permite asociar cada tecla marcada (0 al 9) a un destino diferente:
     * Presione 1 -> Ring Group de Ventas.
     * Presione 2 -> Cola de Soporte Tecnico.
     * Presione 0 -> Recepcion.
   - Permite habilitar "Direct Dial": Si el cliente externo conoce la extension (ej. 105),
     puede marcarla directamente en cualquier momento durante la grabacion.

8. CONDICIONES DE TIEMPO (APPLICATIONS -> TIME CONDITIONS & TIME GROUPS):
   - Define los horarios laborales de la compania:
     * Grupo de Tiempo "Horario de Oficina": Lunes a Viernes de 09:00 a 18:00 hrs.
   - Si la llamada entra dentro del horario: Se envia al IVR Diurno de Recepcion.
   - Si la llamada entra fuera de horario: Se envia al mensaje nocturno de "Cerrado"
     o al buzon de voz de guardia.

9. CONTROL DE FLUJO MANUAL (CALL FLOW CONTROL / DIA-NOCHE):
   - Permite a la recepcionista forzar el modo "Noche" o "Dia" de forma manual
     marcando un codigo rapido en su telefono (ej. `*280`) en caso de una salida
     temprana de oficina o simulacro de emergencia.

10. SIGUEME (APPLICATIONS -> FOLLOW ME / FIND ME):
    - Movilidad inteligente para ejecutivos:
    - Si la extension 105 de la oficina timbra 3 veces y nadie descuelga, el conmutador
      marca en segundo plano al numero de celular personal del empleado y enlaza la llamada.



## 3. VENTAJAS EXCLUSIVAS DE ISSABEL (CALL CENTER Y SERVICIOS INTEGRADOS)

A diferencia de FreePBX estandar, Issabel integra funcionalidades avanzadas de fabrica:

### a) Modulo de Call Center con Marcador Predictivo:

   - Permite cargar bases de datos de campanas (archivos CSV con miles de telefonos).
   - El conmutador realiza las llamadas automaticamente y, en cuanto un humano real
     contesta, entrega la llamada instantaneamente a la pantalla de un agente disponible.

### b) Servidor de Fax Virtual (HylaFax / Fax to Email):

   - Los faxes entrantes se convierten en documentos PDF y llegan al correo electronico.

### c) Telefono WebRTC Embebido:

   - Permite a los empleados contestar llamadas directamente desde Google Chrome

sin necesidad de instalar ningun programa ni softphone en su computadora.
