# GUIA CISCO IOS - PARTE 10: MANTENIMIENTO, COPIAS DE SEGURIDAD Y RESOLUCION DE FALLAS


---



## 1. RESPALDOS (BACKUPS) Y RESTAURACION DE CONFIGURACION

Esencial antes de cualquier cambio importante en la red:

-- Ver archivos en la memoria interna (Flash):
```cisco
Switch# dir flash:

-- Enviar una copia de la configuracion actual hacia un servidor TFTP (ej. 192.168.1.50):
Switch# copy running-config tftp:
  -> Preguntara: Address or name of remote host? [192.168.1.50]
  -> Destination filename? [SW-ACCESO-PISO1-backup-2026.cfg]

-- Restaurar una configuracion desde un servidor TFTP hacia el switch:
Switch# copy tftp: running-config
```


## 2. ACTUALIZACION DE SISTEMA OPERATIVO (CISCO IOS .BIN)

Paso 1: Descargar la imagen IOS (.bin) desde el servidor TFTP a la memoria Flash:
```cisco
Switch# copy tftp: flash:
  -> Remote host: 192.168.1.50
  -> Source filename: c2960x-universalk9-mz.152-7.E8.bin
  -> Destination filename: c2960x-universalk9-mz.152-7.E8.bin

Paso 2: Indicar al switch que cargue la nueva imagen en el proximo arranque:
Switch(config)# boot system flash:c2960x-universalk9-mz.152-7.E8.bin
Switch(config)# exit
Switch# write memory

Paso 3: Verificar que la ruta de arranque este correcta:
Switch# show boot
  -> "BOOT path-list: flash:c2960x-universalk9-mz.152-7.E8.bin"

Paso 4: Reiniciar el switch:
Switch# reload
```


## 3. PROCEDIMIENTO DE RECUPERACION DE CONTRASENA (PASSWORD RECOVERY)

Si perdiste la contrasena de un switch Cisco y no puedes entrar:
Paso 1: Conecta el cable de consola a tu computadora.
Paso 2: Desconecta el cable de corriente del switch.
Paso 3: Manten presionado el boton fisico "MODE" en el frente del switch y vuelve
        a conectar la corriente sin soltar el boton.
Paso 4: Suelta el boton "MODE" cuando la luz SYST deje de parpadear y quede ambar fija.
Paso 5: En tu pantalla de consola aparecera el prompt de arranque: switch:
Paso 6: Escribe los siguientes comandos de recuperacion:
   switch: flash_init
   switch: rename flash:config.text flash:config.old   (Oculta la contrasena vieja)
   switch: boot                                        (Inicia el switch sin pedir clave)
Paso 7: Al iniciar el switch, entra en enable:
```cisco
   Switch> enable
   Switch# rename flash:config.old flash:config.text
   Switch# copy flash:config.text system:running-config (Recupera tu configuracion)
   Switch# configure terminal
   Switch(config)# enable secret MiNuevaClaveSegura2026!
   Switch(config)# exit
   Switch# write memory
```


## 4. DIAGNOSTICO DE SALUD DE HARDWARE (CPU, RAM Y FUENTES)

- Ver que procesos estan consumiendo la CPU (ordenados de mayor a menor):
```cisco
    Switch# show processes cpu sorted | exclude 0.00%

- Ver uso de memoria RAM:
    Switch# show processes memory sorted

- Ver estado de ventiladores, temperatura y fuentes de alimentacion:
    Switch# show env all
    Switch# show power inline    <- Ver consumo electrico PoE entregado a telefonos/camaras
```


## 5. DIAGNOSTICO DE FIBRA OPTICA EN TRANSCEIVERS SFP (DOM / DDM)

¡Comando de oro para diagnosticar cortes o atenuacion en cables de fibra optica!:

```cisco
Switch# show interfaces GigabitEthernet 0/25 transceiver detail
  -> Parametros clave:
     * Optical Tx Power: Potencia con la que el switch esta emitiendo luz (dBm).
     * Optical Rx Power: Potencia con la que esta recibiendo luz del otro extremo.
       (Valores tipicos normales: entre -3 dBm y -18 dBm. Si marca -40 dBm, la fibra esta rota).
```


## 6. DESCUBRIMIENTO DE VECINOS Y TOPOLOGIA (CDP / LLDP)

Permite saber a que switch, router o telefono IP esta conectado cada puerto fisico:

- Ver vecinos mediante protocolo de Cisco (CDP):
```cisco
    Switch# show cdp neighbors
    Switch# show cdp neighbors detail   <- Muestra IP de administracion del vecino

- Ver vecinos con el estandar multi-marca (LLDP):
    Switch# show lldp neighbors
```


## 7. HISTORIAL DE ERRORES Y REGISTROS DEL SISTEMA (LOGS)

- Ver el historial de eventos recientes del switch:
```cisco
    Switch# show logging

- Monitorear registros en vivo cuando estas conectado por SSH (no por consola):
    Switch# terminal monitor
    (Para apagarlo: "terminal no monitor")
```


## 8. DEPURACION EN TIEMPO REAL (DEBUGGING)

Para ver paquetes pasando en vivo por la consola:
```cisco
Switch# debug ip packet detail

-- ¡COMANDO SALVAVIDAS! Apagar inmediatamente todas las depuraciones:
Switch# undebug all   (o la abreviatura: un all)
```
