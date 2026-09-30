# 10. MANTENIMIENTO, RESPALDO, ACTUALIZACION Y RESOLUCION DE FALLAS (TROUBLESHOOTING)

> **TP-LINK (JETSTREAM SWITCHES) - GUIA DE COMANDOS Y CONFIGURACION**


---



## 1. RESPALDO Y RESTAURACION DE LA CONFIGURACION

Permite guardar copias de seguridad de la configuracion en un servidor TFTP
externo para su recuperacion inmediata ante cualquier eventualidad.


### a) Exportar la configuracion activa hacia el servidor TFTP:

```cisco
  SW-CORE-TPLINK# copy running-config tftp:
  Address of remote host: 192.168.1.50
  Destination filename: SW_CORE_TPLINK_BACKUP.cfg

b) Exportar la configuracion de inicio:
  SW-CORE-TPLINK# copy startup-config tftp:
  Address of remote host: 192.168.1.50
  Destination filename: SW_CORE_STARTUP.cfg

c) Restaurar configuracion desde el servidor TFTP:
  SW-CORE-TPLINK# copy tftp: startup-config
  Address of remote host: 192.168.1.50
  Source filename: SW_CORE_TPLINK_BACKUP.cfg
```


## 2. ACTUALIZACION DE FIRMWARE MEDIANTE TFTP

Muchos modelos TP-Link JetStream disponen de dos bancos de memoria de firmware
(Image 1 e Image 2) para realizar actualizaciones seguras.

Paso 1: Verificar la version actual y la imagen activa
```cisco
  SW-CORE-TPLINK# show firmware

Paso 2: Descargar el nuevo firmware (.bin) en el banco inactivo (ej. Image 2)
  SW-CORE-TPLINK# firmware upgrade tftp: 192.168.1.50 TL-SG3428X_v1.0.bin image-2

Paso 3: Definir la imagen recien cargada como la de inicio
  SW-CORE-TPLINK(config)# boot image-2
  SW-CORE-TPLINK(config)# exit

Paso 4: Reiniciar el switch para aplicar el nuevo sistema operativo
  SW-CORE-TPLINK# reboot
```


## 3. DIAGNOSTICO DE CABLES DE COBRE (VCT - VIRTUAL CABLE TEST)

La funcion VCT permite medir la longitud exacta del cable UTP y detectar fallas
como pares abiertos (cortados) o en cortocircuito sin necesidad de un tester fisico:

Ejecutar prueba de cable en el puerto 1/0/5:
```cisco
  SW-CORE-TPLINK# test cable-diagnostics gigabitEthernet 1/0/5

Visualizar los resultados de la prueba:
  SW-CORE-TPLINK# show cable-diagnostics gigabitEthernet 1/0/5

Posibles estados de los 4 pares:
- Normal: Cable en optimas condiciones.
- Open: Par roto, desconectado o roseta mal ponchada (muestra la distancia en metros al corte).
- Short: Cortocircuito entre hilos (muestra la distancia exacta al corto).
```


## 4. DIAGNOSTICO DE MODULOS OPTICOS SFP / SFP+ (DDM)

Supervisa los parametros fisicos y niveles de senal de los transceptores de fibra:

Visualizar informacion general del modulo insertado:
```cisco
  SW-CORE-TPLINK# show interface transceiver gigabitEthernet 1/0/25

Visualizar telemetria digital detallada (potencia optica en dBm):
  SW-CORE-TPLINK# show interface transceiver detail gigabitEthernet 1/0/25

Parametros criticos a revisar:
- Tx Power (Potencia emitida): Potencia con la que el laser esta transmitiendo.
- Rx Power (Potencia recibida): Si el valor es excesivamente bajo (ej. -26 dBm o peor),
  indica fibra sucia, curva muy pronunciada o atenuacion grave en la tirada de fibra.
```


## 5. REGISTROS DEL SISTEMA (LOGS Y SERVIDOR SYSLOG)


### a) Visualizar el buffer de eventos recientes en consola:

```cisco
  SW-CORE-TPLINK# show logging

b) Configurar el envio automatico de registros a un servidor Syslog central:
  SW-CORE-TPLINK(config)# logging host 192.168.1.70
  SW-CORE-TPLINK(config)# logging buffer severity informational
```


## 6. MONITOREO DE RECURSOS Y COMANDOS DE DIAGNOSTICO

Visualizar consumo de CPU en tiempo real y promedios:
```cisco
  SW-CORE-TPLINK# show cpu-utilization

Visualizar utilizacion de memoria RAM:
  SW-CORE-TPLINK# show memory-utilization

Generar volcado completo de estado y diagnostico para soporte tecnico:
  SW-CORE-TPLINK# show tech-support

Herramientas basicas de prueba de conectividad:
  SW-CORE-TPLINK# ping 192.168.10.1
```


## SW-CORE-TPLINK# traceroute 8.8.8.8
