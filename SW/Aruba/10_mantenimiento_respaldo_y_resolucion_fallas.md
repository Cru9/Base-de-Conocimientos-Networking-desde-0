# 10. MANTENIMIENTO, RESPALDO, ACTUALIZACION Y RESOLUCION DE FALLAS (TROUBLESHOOTING)

> **ARUBA NETWORKS (ARUBAOS-CX) - GUIA DE COMANDOS Y CONFIGURACION**


---



## 1. RESPALDO Y RESTAURACION DE CONFIGURACIONES

ArubaOS-CX permite transferir archivos de configuracion facilmente mediante TFTP,
SFTP, SCP o unidades USB.


### a) Exportar la configuracion activa hacia un servidor TFTP o SFTP:

```cisco
  SW-CORE-ARUBA-01# copy running-config tftp://192.168.1.50/SW_CORE_ARUBA_RUNNING.cfg vrf default
  SW-CORE-ARUBA-01# copy startup-config sftp://admin@192.168.1.60/backups/SW_CORE.cfg vrf default

b) Respaldo directo en memoria USB conectada al frontal del switch:
  SW-CORE-ARUBA-01# copy running-config usb:/backup_sw_core_2026.cfg

c) Restaurar configuracion desde TFTP hacia la memoria de inicio:
  SW-CORE-ARUBA-01# copy tftp://192.168.1.50/SW_CORE_ARUBA_RUNNING.cfg startup-config vrf default
```


## 2. ACTUALIZACION DE FIRMWARE (AOS-CX DUAL FLASH IMAGES)

Los switches ArubaOS-CX cuentan con dos bancos de memoria flash para el sistema
operativo: banco 'primary' y banco 'secondary'. Esto garantiza que una actualizacion
nunca deje el equipo inoperativo.

Paso 1: Verificar que banco esta activo y que versiones estan instaladas
```cisco
  SW-CORE-ARUBA-01# show images

Paso 2: Descargar el nuevo firmware (.swi) en el banco inactivo (ej. primary)
  SW-CORE-ARUBA-01# copy tftp://192.168.1.50/FL_10_13_0010.swi primary vrf default

Paso 3: Validar que la transferencia concluyo sin corrupcion
  SW-CORE-ARUBA-01# show images

Paso 4: Reiniciar el switch indicando el banco recien actualizado
  SW-CORE-ARUBA-01# boot system primary
```


## 3. DIAGNOSTICO DE TRANSCEPTORES OPTICOS SFP / SFP+ / QSFP (DOM / DDM)

Permite verificar la potencia de recepcion y emision optica (Rx y Tx en dBm),
temperatura y corriente para detectar fibras atenuadas, sucias o rotas:

Visualizar resumen de transceptores insertados y modelos:
```cisco
  SW-CORE-ARUBA-01# show interface transceiver

Visualizar diagnostico digital completo (potencia optica dBm en tiempo real):
  SW-CORE-ARUBA-01# show interface 1/1/49 transceiver detail

Interpretacion rapida de potencia:
- Tx Power (Potencia transmitida): Debe estar dentro del rango normal del modulo.
- Rx Power (Potencia recibida): Valores muy bajos (ej. -25 dBm o menores) indican
  fibra atenuada, curva excesiva o conectores LC sucios.
```


## 4. DIAGNOSTICO DE CABLE DE COBRE (TDR / CABLE DIAGNOSTIC)

Mide la longitud del cable UTP y detecta pares abiertos o en cortocircuito sin
necesidad de un probador externo:

```cisco
  SW-CORE-ARUBA-01# test cable-diagnostics 1/1/5
  SW-CORE-ARUBA-01# show cable-diagnostics 1/1/5
```


## 5. GESTION DE REGISTROS (EVENT LOGS Y SERVIDOR SYSLOG)


### a) Visualizar los eventos mas recientes del sistema:

```cisco
  SW-CORE-ARUBA-01# show events

b) Visualizar en orden cronologico inverso (lo mas reciente primero):
  SW-CORE-ARUBA-01# show events -r

c) Filtrar eventos por nivel de severidad (emergency, alert, critical, error, warning):
  SW-CORE-ARUBA-01# show events severity error

d) Configurar envio de logs hacia un servidor Syslog centralizado:
  SW-CORE-ARUBA-01(config)# logging 192.168.1.70 severity informational vrf default
```


## 6. MOTOR DE ANALITICA DE RED (NETWORK ANALYTICS ENGINE - NAE)

NAE es un framework exclusivo de ArubaOS-CX que ejecuta scripts en Python dentro
del conmutador para monitorear anomalías (ej. picos de CPU, fluctuaciones de
enlaces o violaciones de trafico) y capturar evidencias automaticamente.

Visualizar agentes NAE activos y su estado:
```cisco
  SW-CORE-ARUBA-01# show nae-agent
  SW-CORE-ARUBA-01# show nae-agent summary
```


## 7. ACCESO AL BASH SHELL Y HERRAMIENTAS AVANZADAS DE LINUX

Al estar construido sobre un kernel Linux moderno, los ingenieros pueden acceder
directamente a la shell para pruebas avanzadas:

Iniciar la shell de Linux:
```cisco
  SW-CORE-ARUBA-01# start-shell
  switch:~$

Ejemplos de comandos dentro del shell:
- Captura de paquetes en vivo en la interfaz de gestion:
  switch:~$ sudo tcpdump -i mgmt -nn
- Ver procesos y memoria en tiempo real:
  switch:~$ top
- Salir del shell de Linux y volver al CLI de Aruba:
  switch:~$ exit
  SW-CORE-ARUBA-01#
```


## 8. GENERACION DE ARCHIVO PARA SOPORTE TECNICO (ARUBA TAC)

Genera un volcado completo de configuracion, estados, colas, buffers y logs para
analisis de fallas:


## SW-CORE-ARUBA-01# copy support-dump tftp://192.168.1.50/support_dump.tar.gz vrf default
