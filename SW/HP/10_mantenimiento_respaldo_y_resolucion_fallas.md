# GUIA HP PROCURVE / ARUBA - PARTE 10: MANTENIMIENTO, COPIAS DE SEGURIDAD Y RESOLUCION DE FALLAS


---



## 1. ARQUITECTURA DE FLASH DUAL (PRIMARY Y SECONDARY FLASH)

Los switches HP ProCurve y Aruba tienen DOS PARTICIONES de sistema operativo:
- Primary Flash (Imagen principal).
- Secondary Flash (Imagen de respaldo).

-- Ver que version de firmware tiene cada particion:
```cisco
SW-HP# show flash
  -> Informara:
     "Primary Image   : 5024220 bytes, Version WC.16.10.0016"
     "Secondary Image : 4899120 bytes, Version WC.16.08.0003"
     "Default Boot    : Primary"
```


## 2. ACTUALIZACION SEGURA DE FIRMWARE (.SWI)

El sistema operativo de HP tiene extension .swi (ej. WC_16_10_0016.swi).

¡REGLA DE ORO DE INGENIERIA EN HP!:
Siempre instala la nueva version en la particion "Secondary", manteniendo tu version
estable en la "Primary". Si la nueva falla, puedes regresar de inmediato sin riesgo.

Paso 1: Descargar el firmware desde el servidor TFTP hacia la Flash secundaria:
```cisco
SW-HP# copy tftp flash 192.168.1.50 WC_16_10_0016.swi secondary

Paso 2: Confirmar la instalacion:
SW-HP# show flash
  -> Comprueba que la particion Secondary tenga la nueva version.

Paso 3: Reiniciar arrancando desde la particion secundaria:
SW-HP# boot system flash secondary
  -> El switch reiniciara cargando el nuevo sistema operativo.
```


## 3. RESPALDOS (BACKUPS) Y RESTAURACION DE CONFIGURACION

-- Enviar copia de la configuracion hacia un servidor TFTP (ej. 192.168.1.50):
```cisco
SW-HP# copy startup-config tftp 192.168.1.50 SW-HP-PISO1-backup-2026.cfg

-- Restaurar una configuracion desde un servidor TFTP:
SW-HP# copy tftp startup-config 192.168.1.50 SW-HP-PISO1-backup-2026.cfg
SW-HP# reload
```


## 4. PROCEDIMIENTO FISICO DE RECUPERACION DE CONTRASENA

Si perdiste la contrasena de administrador en un switch HP ProCurve:
1. En el panel frontal del switch veras dos pequenos orificios: "Clear" y "Reset".
2. Con dos clips de papel, presiona ambos botones al mismo tiempo.
3. Suelta el boton "Reset" mientras continuas presionando "Clear".
4. Cuando la luz de "Test" empiece a parpadear, suelta el boton "Clear".
5. ¡Listo! El switch iniciara sin contrasena, conservando intactas todas tus VLANs
   e interfaces configuradas.



## 5. DIAGNOSTICO DE SALUD DE HARDWARE (CPU, RAM Y POE)

- Ver consumo actual de procesador CPU:
```cisco
    SW-HP# show cpu

- Ver uso de memoria RAM:
    SW-HP# show memory

- Ver consumo electrico PoE entregado a telefonos y camaras IP:
    SW-HP# show power-over-ethernet
```


## 6. DIAGNOSTICO DE FIBRA OPTICA EN TRANSCEIVERS SFP (DOM)

¡Comando indispensable para comprobar la salud de cables de fibra optica!:

```cisco
SW-HP# show interfaces transceiver 25 detail
  -> Parametros clave:
     * Rx Power (Potencia optica recibida en dBm): Valores normales tipicos: -3 dBm a -18 dBm.
       Si marca -30 o -40 dBm, la fibra esta rota, doblada o sucia.
     * Tx Power (Potencia transmitida).
     * Temperature: Temperatura interna del laser.
```


## 7. DESCUBRIMIENTO DE VECINOS Y TOPOLOGIA (LLDP / CDP)

Para saber que dispositivo esta conectado en cada puerto fisico:

- Ver dispositivos vecinos conectados mediante LLDP:
```cisco
    SW-HP# show lldp info remote-device

- Ver dispositivos Cisco o compatibles mediante CDP:
    SW-HP# show cdp neighbors detail
```


## 8. HISTORIAL DE ERRORES Y REGISTROS DEL SISTEMA (LOGS)

- Ver el historial de eventos en orden inverso (los mas recientes primero):
```cisco
    SW-HP# show log -r

- Generar un reporte completo del switch para enviar a soporte tecnico:
    SW-HP# show tech
```
