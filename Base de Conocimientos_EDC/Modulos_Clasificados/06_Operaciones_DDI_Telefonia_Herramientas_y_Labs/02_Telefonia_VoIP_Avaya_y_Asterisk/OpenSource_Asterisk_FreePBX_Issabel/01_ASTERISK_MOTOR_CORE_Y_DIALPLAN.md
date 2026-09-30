# ASTERISK, FREEPBX E ISSABEL

> **TELEFONIA DE CODIGO ABIERTO (OPEN SOURCE VOIP)**

> *01. EL MOTOR CORE DE ASTERISK Y LA LOGICA DEL DIALPLAN*


---



## 1. ARQUITECTURA INTERNA DE CANALES DE ASTERISK

Asterisk procesa diferentes tipos de conexiones fisicas o de red a traves de
controladores de canal (Channel Drivers):


### a) chan_sip (OBSOLETO / DEPRECADO):

   - El controlador SIP original de Asterisk (archivo `sip.conf`).
   - Limitaciones: Monolitico, monohilo (bloqueaba procesos en servidores con miles
     de llamadas) y dificil de mantener. Ha sido descontinuado en Asterisk 21+.


### b) chan_pjsip (EL ESTANDAR MODERNO INDISCUTIBLE):

   - Basado en la pila de codigo abierto PJSIP (archivo `pjsip.conf`).
   - Multihilo asincrono, arquitectura modular orientada a objetos y cumplimiento
     estricto de los ultimos RFCs de la IETF.
   - Soporta nativamente Multi-Contact: Un mismo usuario puede tener su extension
     registrada al mismo tiempo en su telefono de escritorio, su laptop y su celular.


### c) chan_dahdi (Digium Asterisk Hardware Device Interface):

   - Controlador para tarjetas fisicas PCIe (tarjetas Digium o Sangoma con puertos
     E1/PRI o modulos analogicos FXS/FXO).



## 2. LOS 5 OBJETOS FUNDAMENTALES DE PJSIP (pjsip.conf)

Para crear una extension o troncal en el archivo `pjsip.conf`, se configuran 5 objetos:

1. [transport] : Define el protocolo y puerto de escucha (ej. UDP 5060 o TLS 5061).
2. [endpoint]  : Configura los codecs de audio, DTMF, timers RTP y caller ID.
3. [aor]       : (Address of Record) Almacena dinamicamente la IP y puerto del telefono.
4. [auth]      : Credenciales de autenticacion (Usuario y Contrasena).
5. [identify]  : Mapea llamadas entrantes por IP origen (util para troncales SIP fijas).


## EJEMPLO REAL DE EXTENSION PJSIP EN /etc/asterisk/pjsip.conf:

```text
[transport-udp]
type=transport
protocol=udp
bind=0.0.0.0:5060

[101]
type=endpoint
context=from-internal
disallow=all
allow=ulaw,alaw,g729
auth=101-auth
aors=101-aor

[101-auth]
type=auth
auth_type=userpass
username=101
password=ClaveSuperSegura101!

[101-aor]
type=aor
max_contacts=2     ; Permite registrar la extension en laptop y telefono a la vez
```


## 3. LA LOGICA DEL DIALPLAN (EL PLAN DE MARCACION: extensions.conf)

El Dialplan es el cerebro de Asterisk. Define con precision quirurgica que debe
suceder cuando un usuario levanta la bocina y marca cualquier numero.

SINTAXIS MAESTRA:
`exten => [Numero_o_Patron], [Prioridad], [Aplicacion(Argumentos)]`


### A) Patrones de Marcacion (Pattern Matching):

   Los patrones siempre inician con un guion bajo `_`:
   - `_X` : Coincide con cualquier digito del 0 al 9.
   - `_Z` : Coincide con cualquier digito del 1 al 9.
   - `_N` : Coincide con cualquier digito del 2 al 9.
   - `_.` : Comodin universal (coincide con uno o mas caracteres cualesquiera).
   - Ejemplo: `_9NXXXXXX` coincide con una marcacion de 7 digitos que inicie con 9.


### B) Prioridades:

   - `1` : Primer paso obligatorio.
   - `n` : (Next) Ejecuta el siguiente paso secuencialmente.


### C) Aplicaciones Core de Asterisk:

   - `Answer()`           : Descuelga formalmente la llamada (envia un SIP 200 OK).
   - `Playback(archivo)`  : Reproduce un audio sin permitir interrupcion por teclado.
   - `Background(archivo)`: Reproduce un audio mientras escucha digitos DTMF (para IVRs).
   - `WaitExten(segundos)`: Espera que el usuario presione una tecla.
   - `Dial(destino,tiempo)`: Envia la llamada al telefono objetivo.
   - `VoiceMail(ext@context)`: Envia la llamada al buzon de voz.
   - `Hangup()`           : Cuelga y corta la llamada (envia un SIP BYE).


## EJEMPLO COMPLETO DE DIALPLAN EN /etc/asterisk/extensions.conf:

```text
[from-internal]
; Llamadas internas entre extensiones de 3 digitos (100 a 199)
exten => _1XX,1,NoOp(Llamada interna hacia extension ${EXTEN})
 same => n,Dial(PJSIP/${EXTEN},20,m)   ; Timbra por 20 seg con musica de espera
 same => n,GotoIf($["${DIALSTATUS}" = "BUSY"]?ocupado:nobusy)
 same => n(ocupado),Playback(im-sorry)
 same => n,VoiceMail(${EXTEN}@default,b) ; Buzon de ocupado
 same => n,Hangup()
 same => n(nobusy),VoiceMail(${EXTEN}@default,u) ; Buzon de no contesta
 same => n,Hangup()

; Menu de Operadora Automatica (IVR) al marcar el 500
exten => 500,1,Answer()
 same => n,Wait(1)
 same => n,Background(menu-bienvenida) ; "Para Ventas marque 1, Soporte marque 2"
 same => n,WaitExten(5)

exten => 1,1,Dial(PJSIP/101,15)        ; Opcion 1: Ventas
exten => 2,1,Dial(PJSIP/102,15)        ; Opcion 2: Soporte
exten => t,1,Playback(vm-goodbye)      ; Opcion t (Timeout si no marca nada)
 same => n,Hangup()
```


## 4. CONSOLA DE COMANDOS DE ASTERISK (ASTERISK CLI)

Para entrar a la consola en vivo desde la terminal de Linux:
`asterisk -rvvv`
(-r = reconectar al proceso en ejecucion; -vvv = nivel 3 de verbosidad).


## COMANDOS INDISPENSABLES EN EL CLI DE ASTERISK:


| Comando | Descripcion |
| :--- | :--- |
| core show version | Muestra la version instalada de Asterisk |
| core show channels | Muestra todas las llamadas activas en este segundo |
| pjsip show endpoints | Lista todas las extensiones PJSIP y su estado (Online/Offline) |
| pjsip show registrations | Verifica el estado de registro de las troncales SIP con el ISP |
| pjsip set logger on | ¡DEPURACION EN VIVO! Muestra los paquetes SIP crudos en pantalla |
| pjsip set logger off | Desactiva el log de paquetes SIP |
| dialplan reload | Recarga el archivo extensions.conf sin reiniciar Asterisk |
| module reload chan_pjsip.so | Recarga la configuracion de extensiones y troncales PJSIP |
| core stop now | Detiene inmediatamente el servicio de Asterisk |
