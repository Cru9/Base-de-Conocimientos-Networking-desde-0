# 03. GUIA PASO A PASO: CONFIGURACION DE AVAYA IP OFFICE CON MANAGER

> **TELEFONIA EMPRESARIAL Y VOZ SOBRE IP (VOIP)**


---



## 1. CONEXION INICIAL CON AVAYA IP OFFICE MANAGER

Avaya IP Office Manager es la aplicacion oficial de administracion sobre Windows.

PASO 1: Direccionamiento de la Computadora:
- Conecta un cable de red de tu laptop al puerto LAN 1 del chasis IP500v2.
- Configura en tu adaptador de red de Windows una IP fija en el mismo segmento:
  * Direccion IP : 192.168.42.50
  * Mascara      : 255.255.255.0
  * Gateway      : 192.168.42.1

PASO 2: Descubrimiento y Apertura de la Configuracion:
- Abre el programa IP Office Manager en Windows.
- Ve a: `File -> Open Configuration`.
- Manager emitira un broadcast UDP 5080 y detectara el equipo (Nombre, IP 192.168.42.1,
  Version de Firmware y Tipo de Unidad IP500v2).
- Selecciona el sistema y haz clic en OK.
- Credenciales de Fabrica por defecto:
  * Usuario : `Administrator`
  * Password: `Administrator` (o la contrasena asignada en el primer arranque).

PASO 3: Los Modos de Guardado (Save Configuration):
- Al realizar cualquier cambio, se guarda mediante `File -> Save Configuration`:
  * Modo Merge (En Caliente): Aplica los cambios inmediatamente a la memoria RAM
    SIN reiniciar el conmutador y SIN CORTAR llamadas en curso.
  * Modo Immediate (Reinicio Inmediato): Reinicia el hardware. Obligatorio si cambias
    la IP de la LAN o cambias tarjetas base fisicas.



## 2. CREACION DE USUARIOS Y EXTENSIONES

En Avaya existe una distincion crucial:
- Extension: Representa el dispositivo fisico o puerto de hardware.
- User (Usuario): Representa la persona, sus permisos, clave de buzon y reglas.


### A) Creacion del Usuario (User):

1. En el arbol izquierdo, haz clic derecho sobre `User` -> `New`.
2. Pestana "User":
   - Name: `Juan_Perez`
   - Extension: `201`
   - Password / Phone Password: `1234` (PIN utilizado por el telefono IP para autenticarse).
3. Pestana "Voicemail":
   - Voicemail On: Marcado (Habilita buzon personal).
   - Voicemail Code: `1234` (PIN de seguridad para escuchar mensajes).
   - Voicemail Email: `juan.perez@empresa.com` (Activa Voicemail-to-Email).


### B) Creacion de la Extension (Extension):

1. Haz clic derecho sobre `Extension` -> `New`.
2. Elegir el tipo de telefono:
   - `H.323 Extension`: Para telefonos Avaya series 9600 (9608, 9611G) y 1600.
   - `SIP Extension`: Para telefonos modernos Avaya J100 (J129, J139, J179) o genericos.
   - `Digital Station`: Para telefonos cableados a 2 hilos serie 1400 / 9500.
3. En Base Extension, escribe `201`.
4. ¡IP Office enlazara automaticamente la Extension 201 con el Usuario 201!



## 3. CONFIGURACION DE TRONCAL SIP (SIP TRUNK)

Para habilitar llamadas externas con un proveedor de telefonia IP (ITSP):

PASO 1: Habilitar SIP en el Sistema:
- Ve a: `System -> LAN1 -> Pestana VoIP`.
- Asegurate de marcar la casilla: `[X] SIP Trunks Enable`.

PASO 2: Crear la Linea SIP (SIP Line):
- Haz clic derecho sobre `Line` -> `New` -> `SIP Line`.
- Pestana "SIP Line":
  * Line Number: `17` (Numero de linea interno).
  * ITSP Domain Name: `sip.proveedor.com` (o IP publica del carrier).
  * Outgoing Group ID: `1` (ID de grupo para llamadas de salida).
  * Incoming Group ID: `1` (ID de grupo para llamadas de entrada).
- Pestana "Transport":
  * ITSP Proxy Address: Direccion IP del Session Border Controller (SBC) del operador.
  * Layer 4 Protocol: `UDP` (Puerto 5060).
- Pestana "SIP Credentials":
  * Haz clic en `Add`:
    - User Name: Numero de cabecera o usuario asignado por el carrier (ej. `5512345600`).
    - Authentication Name: Usuario de autenticacion.
    - Password: Password entregado por el carrier.
- Pestana "SIP URI":
  * Haz clic en `Add` para mapear los canales:
    - Local URI: `*`
    - Contact: `*`
    - Display: `*`
    - Max Sessions: Numero de canales concurrentes contratados (ej. `20`).
- Pestana "VoIP":
  * Codecs: Colocar en orden de preferencia `G.711 ULAW` y `G.729(8K CS-ACELP)`.
  * Fax Transport Support: `T.38` (Habilitado para envio de faxes por IP).



## 4. CODIGOS CORTOS (SHORT CODES) Y PLAN DE MARCACION

Los codigos cortos le indican a Avaya que accion tomar cuando un usuario marca
determinados digitos en el telefono:

SINTAXIS MAESTRA:
```text
[ Codigo Marcado ] -> [ Funcion / Feature ] -> [ Numero Telefonico ] -> [ Line Group ID ]
```


## A) Salida a Lineas Externas Marcando "9":

- Code            : `9N;`
- Feature         : `Dial`
- Telephone Number: `N` (o `N"@sip.proveedor.com"`)
- Line Group ID   : `1` (Apunta a nuestra troncal SIP)
Explicacion:
- El digito `9` se consume para tomar linea exterior.
- La letra `N` representa cualquier cantidad de digitos que marque el usuario.
- El punto y coma `;` es fundamental: indica "espera a que el usuario termine de marcar
  antes de lanzar la llamada por la troncal SIP".


## B) Codigos Cortos Esenciales de Sistema:


| Codigo | Funcion | Descripcion |
| :--- | :--- | :--- |
| 911 | Dial Emergency | Llamada de emergencia prioritaria al 911 |
| *17 | Voicemail Collect | Ingreso directo al buzon de voz personal |
| *30 | Call Pickup Any | Jalar/capturar llamada que timbra en cualquier lugar |
| *31 | Call Pickup Group | Jalar llamada de un companero del mismo departamento |
| *01 | Forwarding All On | Activar desvio incondicional de llamadas |
| *02 | Forwarding All Off | Desactivar desvio de llamadas |
| *08 | Do Not Disturb On | Activar No Molestar (DND) |
| *09 | Do Not Disturb Off | Desactivar No Molestar (DND) |




## 5. ENRUTAMIENTO DE LLAMADAS ENTRANTES (INCOMING CALL ROUTE - ICR)

Controla que ocurre cuando entra una llamada desde la compania telefonica hacia
un numero publico directo (DID / DDI):

1. En el arbol izquierdo, haz clic derecho sobre `Incoming Call Route` -> `New`.
2. Pestana "Standard":
   - Line Group ID: `1` (La troncal SIP por donde entra la llamada).
   - Incoming Number: El numero telefonico publico asignado (ej. `5512345600`).
   - Destination:
     * Si deseas que vaya a un grupo: `200` (Grupo de Recepcion).
     * Si es un DID directo a un director: `201` (Extension directa).
     * Si deseas que conteste la operadora automatica: `AA:MenuPrincipal`.



## 6. GRUPOS DE BUSQUEDA (HUNT GROUPS)

1. Haz clic derecho sobre `Hunt Group` -> `New`.
2. Pestana "Hunt Group":
   - Name: `RECEPCION`
   - Extension: `200`
   - Ring Mode:
     * `Collective`: Timbran todos los telefonos a la vez.
     * `Longest Waiting`: Timbra primero la recepcionista con mas tiempo desocupada.
   - Ring Time: `15` segundos.
3. Pestana "User List":
   - Agrega las extensiones que atenderan las llamadas (ej. 201, 202, 203).
4. Pestana "Fallbacks":

## - Si nadie contesta en 15 segundos: desviar la llamada a `Voicemail` o a un celular de guardia.
