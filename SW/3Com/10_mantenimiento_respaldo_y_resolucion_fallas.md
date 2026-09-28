# GUIA 3COM COMWARE - PARTE 10: MANTENIMIENTO, COPIAS DE SEGURIDAD Y RESOLUCION DE FALLAS


---



## 1. RESPALDOS (BACKUPS) Y RESTAURACION DE CONFIGURACION

La configuracion del switch se almacena en un archivo con extension .cfg en la memoria Flash.

-- Ver los archivos presentes en el almacenamiento interno del switch:
```text
<3Com> dir

-- Enviar una copia de seguridad hacia un servidor TFTP (ej. 192.168.1.50):
<3Com> tftp 192.168.1.50 put config.cfg backup_SW3COM_2026.cfg

-- Descargar y restaurar una configuracion desde un servidor TFTP:
<3Com> tftp 192.168.1.50 get nueva_config.cfg config.cfg
<3Com> startup saved-configuration config.cfg
<3Com> reboot
```


## 2. ACTUALIZACION DE SISTEMA OPERATIVO (FIRMWARE .BIN)

Los sistemas operativos de 3Com Comware tienen extension .bin o .app:

Paso 1: Descargar el nuevo firmware desde tu servidor TFTP a la memoria Flash:
```text
<3Com> tftp 192.168.1.50 get 3com4500g-cmw520-r2208.bin

Paso 2: Indicar al switch que cargue la nueva imagen como sistema principal (main):
<3Com> boot-loader file 3com4500g-cmw520-r2208.bin main

Paso 3: Verificar que el archivo de arranque este asignado correctamente:
<3Com> display boot-loader
  -> "The current software is: ..."
  -> "The main software to boot is: 3com4500g-cmw520-r2208.bin"

Paso 4: Reiniciar el switch para arrancar con el nuevo firmware:
<3Com> reboot
```


## 3. DIAGNOSTICO DE SALUD DE HARDWARE (CPU, RAM Y FUENTES)

Si la red se siente lenta o el switch no responde adecuadamente:

- Ver uso de procesador CPU:
```text
    <3Com> display cpu-usage

- Ver uso de memoria RAM:
    <3Com> display memory-usage

- Ver estado de temperatura, ventiladores y fuentes de alimentacion:
    <3Com> display environment
    <3Com> display power
```


## 4. DIAGNOSTICO DE FIBRA OPTICA EN TRANSCEIVERS SFP (DDM)

¡Herramienta fundamental para detectar fallas en enlaces de fibra optica!:

```text
<3Com> display transceiver verbose interface GigabitEthernet 1/0/25
  -> Parametros clave:
     * Rx Power (Potencia optica recibida en dBm): Si esta en -30 o peor, la fibra
       esta doblada, sucia o rota. Lo normal suele oscilar entre -3 dBm y -18 dBm.
     * Tx Power (Potencia optica transmitida).
     * Temperature: Temperatura interna del modulo laser.
```


## 5. HISTORIAL DE ERRORES Y REGISTROS DEL SISTEMA (LOGS)

- Ver los ultimos eventos y caidas de puertos registrados por el switch:
```text
    <3Com> display logbuffer

- Filtrar logs de puertos que cambiaron de estado (UP/DOWN):
    <3Com> display logbuffer | include IFNET
```


## 6. HERRAMIENTAS DE PRUEBA DE RED (PING Y TRACEROUTE)

- Prueba basica de conectividad:
```text
    <3Com> ping 192.168.10.50

- Prueba de ping especificando la IP de origen (VLAN origen):
    <3Com> ping -a 192.168.10.1 8.8.8.8

- Traza de ruta salto a salto:
    <3Com> tracert 8.8.8.8
```


## 7. COMANDOS DE DEPURACION EN VIVO (DEBUGGING)

Para inspeccionar paquetes pasando en tiempo real por la consola:

Paso 1: Habilitar la impresion de depuracion en pantalla:
```text
<3Com> terminal monitor
<3Com> terminal debugging

Paso 2: Activar la depuracion de un protocolo especifico (ej. paquetes OSPF):
<3Com> debugging ospf packet

Paso 3: ¡MUY IMPORTANTE! Desactivar toda la depuracion al terminar:
<3Com> undo debugging all
```
