# 05. DIAGNOSTICO, TRAZAS DE MONITOR, CONSOLA SERIAL DTE Y RECUPERACION AVAYA

> **TELEFONIA EMPRESARIAL Y VOZ SOBRE IP (VOIP)**


---



## 1. HERRAMIENTAS OFICIALES DE DIAGNOSTICO EN VIVO

Avaya incluye dos herramientas de nivel experto para diagnosticar problemas:


## A) AVAYA IP OFFICE SYSTEM STATUS APPLICATION (SSA):

- Aplicacion grafica que se conecta a la IP del conmutador (puerto TCP 50804).
- Muestra el estado fisico y operativo en tiempo real:
  * Alarmas de Sistema (Alarm Log): Fallas de sincronizacion de reloj, cortes de fibra,
    saturacion de DSPs VCM y licencias expiradas.
  * Estado de Troncales (Trunks):
    - En Troncales SIP: Muestra si el registro con el operador ITSP esta activo o en falla.
    - En E1/PRI: Muestra alarmas de capa 1 (Alarma Roja - Cable desconectado,
      Alarma Amarilla - Perdida de trama remota, Alarma Azul - Senal AIS).
  * Monitoreo de Recursos VCM: Porcentaje de uso de DSPs de compresion. Si llega al
    100%, las siguientes llamadas IP seran rechazadas con tono de ocupado.
  * Llamadas Activas en Curso: Muestra origen, destino, codec utilizado (G.711 / G.729),
    latencia, jitter y paquetes descartados en vivo.


## B) AVAYA IP OFFICE MONITOR (SYSMONITOR) - ANALISIS FORENSE DE TRAZAS:

- Permite capturar las tramas binarias y senalizacion interna del conmutador.
- Filtros Esenciales a Habilitar en Monitor (`Filters -> Trace Options`):
  * `SIP -> SIP Rx / SIP Tx`: Captura todos los paquetes SIP INVITE, 200 OK y BYE.
  * `ISDN -> L3 Calls`: Captura mensajes Q.931 de tramas E1/PRI.
  * `Short Codes`: Muestra que codigo corto emparejo la llamada marcada por el usuario.


## CODIGOS DE CAUSA DE DESCONEXION ISDN/SIP MAS FRECUENTES (CAUSE CODES):


| Codigo Causa | Nombre Estandar | Significado y Diagnostico |
| :--- | :--- | :--- |
| Cause 1 | Unallocated Number | El numero marcado no existe o faltan digitos. |
| Cause 16 | Normal Call Clearing | Llamada finalizada normalmente (alguien colgo). |
| Cause 17 | User Busy | El usuario de destino esta ocupado. |
| Cause 19 | No Answer from User | Timbre prolongado sin respuesta. |
| Cause 34 | No Circuit Available | ¡TODAS LAS LINEAS DE LA TRONCAL ESTAN OCUPADAS! |
| Cause 41 | Temporary Failure | Falla temporal en la central del operador telefonico. |
| Cause 88 | Incompatible Destination Falla de negociacion de codecs de audio. |  |




## 2. PUERTO DE CONSOLA SERIAL DTE Y RECUPERACION DE EMERGENCIA

En situaciones de catastrofe donde el conmutador no responde por red, se olvido la
contrasena del usuario `Administrator` o el equipo se encuentra en bucle de reinicio:


## PARAMETROS DE CONEXION POR TERMINAL SERIAL (PuTTY / TeraTerm):

- Cable: Cable serial RS-232 hembra a hembra (Null-Modem) conectado al puerto DTE.
- Velocidad en Baudios : 38,400 bps
- Bits de Datos        : 8
- Paridad              : Ninguna (None)
- Bits de Parada       : 1
- Control de Flujo     : Ninguno (None)


## PROCEDIMIENTO DE RESCATE PASO A PASO (COMANDOS AT):

1. Conecta el cable serial a tu computadora y abre PuTTY en el puerto COM correspondiente.
2. Desconecta el cable de corriente electrica del conmutador Avaya IP500v2.
3. Conecta la corriente electrica y de inmediato presione la combinacion de teclas
   `Ctrl + C` o escriba la palabra `AT` (en MAYUSCULAS) continuamente varias veces.
4. El sistema detendra el arranque normal y entrara al cargador de rescate:
   Prompt en pantalla:
   `OK` (o `Loader>`)


## COMANDOS DE RECUPERACION A BAJO NIVEL:


| Comando | Efecto Inmediato |
| :--- | :--- |
| AT | Verifica comunicacion serial (Responde "OK"). |
| AT-X | ¡BORRADO TOTAL A VALORES DE FABRICA! |
| Borra toda la configuracion del conmutador y la regresa a estado de fabrica. |  |
| (La IP vuelve a ser 192.168.42.1 y la clave vuelve a ser Administrator). |  |
| AT-X21 | Borra la configuracion principal pero PRESERVA las claves de seguridad. |
| AT-X3 | Borra unicamente las credenciales de seguridad (Permite redefinir |
| el usuario Administrator sin perder la configuracion de las extensiones). |  |
| AT-Z | Reinicia el conmutador normalmente. |




## 3. RESPALDO Y RECREACION DE LA TARJETA SYSTEM SD


### A) Respaldar Configuracion en la Tarjeta SD Opcional:

- Si colocas una segunda tarjeta SD en la ranura "Optional SD":
  En Manager ve a: `File -> Advanced -> Backup System Files`.
- El conmutador clonara la configuracion completa y los audios en la tarjeta secundaria.


### B) Recrear una Tarjeta SD Corrupta (Formateo Oficial de Avaya):

- Si el firmware se dana y el equipo no enciende:
  1. Extrae la tarjeta System SD e insertala en el lector de tarjetas de tu computadora.
  2. Abre Avaya IP Office Manager en Windows.
  3. Ve a: `File -> Advanced -> Recreate IP Office SD Card -> IP500v2`.
  4. Selecciona la unidad de tu lector de tarjetas.
  5. Manager formateara la tarjeta con los sectores de arranque oficiales de Avaya
     y copiara todos los binarios (.bin) de firmware correspondientes a la version instalada.

## 6. Reinserta la tarjeta en el chasis IP500v2 y enciende el equipo.
