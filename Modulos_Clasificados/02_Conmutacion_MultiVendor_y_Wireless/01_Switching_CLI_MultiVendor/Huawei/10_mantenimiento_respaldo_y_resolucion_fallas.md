# GUIA HUAWEI VRP - PARTE 10: MANTENIMIENTO, COPIAS DE SEGURIDAD Y RESOLUCION DE FALLAS


---



## 1. RESPALDOS (BACKUPS) Y RESTAURACION DE CONFIGURACION

La configuracion del switch se guarda fisicamente en un archivo zip dentro de la
memoria flash (usualmente llamado vrpcfg.zip).

-- Ver los archivos presentes en el almacenamiento interno del switch:
```text
<HUAWEI> dir

-- Enviar una copia de seguridad hacia un servidor TFTP (ej. 192.168.1.50):
<HUAWEI> tftp 192.168.1.50 put vrpcfg.zip backup_SW_PISO1_2026.zip

-- Descargar y restaurar una configuracion desde un servidor TFTP:
<HUAWEI> tftp 192.168.1.50 get nueva_config.zip vrpcfg.zip
<HUAWEI> startup saved-configuration vrpcfg.zip
<HUAWEI> reboot
```


## 2. ACTUALIZACION DE FIRMWARE (SISTEMA OPERATIVO VRP)

El sistema operativo de Huawei tiene extension .cc (ej. S5700-V200R019.cc).

Paso 1: Descargar el archivo .cc desde tu servidor TFTP/FTP a la memoria flash:
```text
<HUAWEI> tftp 192.168.1.50 get S5700-V200R019C00SPC500.cc

Paso 2: Indicar al switch que use la nueva version en el proximo reinicio:
<HUAWEI> startup system-software S5700-V200R019C00SPC500.cc

Paso 3: Verificar los parametros de arranque:
<HUAWEI> display startup
  -> Comprueba que en "Next startup system software" aparezca el archivo nuevo.

Paso 4: Reiniciar para aplicar la actualizacion:
<HUAWEI> reboot
```


## 3. DIAGNOSTICO DE SALUD DEL HARDWARE (CPU, MEMORIA Y FUENTES)

Si la red se siente lenta o el switch no responde:

- Ver uso de procesador (Normal: < 40%):
```text
    <HUAWEI> display cpu-usage

- Ver uso de memoria RAM:
    <HUAWEI> display memory-usage

- Ver estado de temperatura, ventiladores y fuentes de poder:
    <HUAWEI> display environment
    <HUAWEI> display power
```


## 4. DIAGNOSTICO DE FIBRA OPTICA (MODULOS SFP / TRANSCEIVERS)

¡Comando de oro para ingenieros de soporte!
Permite ver la potencia optica (RX/TX en dBm) del laser para detectar si la fibra
esta rota, sucia, atenuada o si el modulo SFP se dano:

```text
<HUAWEI> display transceiver verbose interface GigabitEthernet 0/0/25
  -> Revisar los parametros:
     * Rx Power (Potencia recibida): Si esta en -30 o -40 dBm, la fibra esta rota o sucia.
     * Tx Power (Potencia emitida): Debe estar dentro de los limites del fabricante.
     * Temperature: Temperatura de operacion del modulo SFP.
```


## 5. HISTORIAL DE ERRORES Y EVENTOS (LOGS)

Para saber que paso cuando un puerto se cayo a las 3:00 AM:

- Ver los ultimos registros del sistema:
```text
    <HUAWEI> display logbuffer

- Filtrar logs de puertos que cambiaron de estado (UP/DOWN):
    <HUAWEI> display logbuffer | include IFNET
```


## 6. HERRAMIENTAS DE PRUEBA DE RED (PING Y TRACEROUTE)

- Ping estandar:
```text
    <HUAWEI> ping 192.168.10.50

- Ping especificando la IP de origen (muy util para probar VLANs especificas):
    <HUAWEI> ping -a 192.168.10.1 8.8.8.8

- Ping continuo o con tamano de paquete grande (para medir MTU):
    <HUAWEI> ping -c 100 -s 1472 192.168.10.50

- Traza de ruta salto a salto:
    <HUAWEI> tracert 8.8.8.8
```


## 7. COMANDOS DE DEPURACION EN VIVO (DEBUGGING)

Para ver paquetes pasando en tiempo real por la consola (usar con precaucion):

Paso 1: Habilitar la salida de terminal:
```text
<HUAWEI> terminal monitor
<HUAWEI> terminal debugging

Paso 2: Activar depuracion de un protocolo (ejemplo: mensajes OSPF):
<HUAWEI> debugging ospf packet

Paso 3: APAGAR la depuracion (Siempre hacerlo al terminar para no sobrecargar el CPU):
<HUAWEI> undo debugging all
```
