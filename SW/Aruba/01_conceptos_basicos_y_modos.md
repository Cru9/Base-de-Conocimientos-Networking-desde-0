# 01. CONCEPTOS BASICOS, MODOS DE OPERACION Y COMANDOS INICIALES

> **ARUBA NETWORKS (ARUBAOS-CX) - GUIA DE COMANDOS Y CONFIGURACION**


---



## 1. ARQUITECTURA DE ARUBAOS-CX (AOS-CX)

ArubaOS-CX es el sistema operativo moderno de HPE Aruba para conmutadores
empresariales de campus y centros de datos (CX 6000, 6100, 6200, 6300, 6400,
8320, 8325, 8360, 8400, 10000).

Diferencias clave con sistemas legados (ProCurve / Comware):
- Basado en microservicios y kernel Linux moderno.
- Base de datos de estado OVSDB (Open vSwitch Database) para consistencia total.
- Sintaxis intuitiva tipo industria (similar a Cisco IOS en puertos y comandos).
- Soporte nativo de Checkpoints (puntos de restauración instantáneos con rollback).
- Motor de analítica de red integrado (Network Analytics Engine - NAE).
- Programabilidad REST API y Python nativo en el propio conmutador.



## 2. JERARQUIA DE MODOS EN EL CLI


| Modo | Prompt | Descripcion |
| :--- | :--- | :--- |
| Modo Usuario (No privilegiado) switch> | Consultas basicas de solo lectura. |  |
| Modo Privilegiado (Enable) | switch# | Verificacion completa, pruebas y guardado. |
| Modo Configuracion Global | switch(config)# | Modificacion de parametros globales. |
| Sub-modo de Interfaz | switch(config-if)# | Configuracion de puertos fisicos. |

Sub-modo de Rango de Interfaces switch(config-if<1/1/1..>) Configuracion simultanea de puertos.
Sub-modo de VLAN               switch(config-vlan-<id>)#   Configuracion de nombres y estado de VLAN.
Sub-modo de SVI (VLAN L3)      switch(config-if-vlan)#     Direccionamiento IP de VLAN virtual.
Sub-modo LAG (EtherChannel)    switch(config-lag-if)#      Agregacion de enlaces LACP.
Sub-modo Enrutador             switch(config-router-ospf)# Protocolos de enrutamiento dinamico.
Modo Shell de Linux            switch:~$                   Bash shell directo (diagnostico avanzado).



## 3. TRANSICION ENTRE MODOS

De Usuario a Privilegiado:
  switch> enable
  switch#

De Privilegiado a Configuracion Global:
  switch# configure terminal
  switch(config)#

Ingresar a una interfaz fisica:
  switch(config)# interface 1/1/1
  switch(config-if)#

Retroceder un nivel:
  switch(config-if)# exit
  switch(config)#

Volver directamente al modo privilegiado (#):
  switch(config-if)# end
  (o presionar Ctrl + Z)

Cerrar sesion (Logout):
  switch# exit



## 4. NOMENCLATURA DE PUERTOS EN ARUBAOS-CX (Miembro / Slot / Puerto)

AOS-CX utiliza la nomenclatura de 3 niveles:  [Miembro] / [Ranura] / [Puerto]

Ejemplos:
  1/1/1     -> Switch 1 (independiente o miembro 1 de VSF), Ranura 1, Puerto 1.
  1/1/24    -> Switch 1, Ranura 1, Puerto 24.
  1/1/49    -> Switch 1, Ranura 1, Puerto 49 (usualmente uplink SFP+/SFP28).
  2/1/1     -> Miembro 2 de un stack VSF, Ranura 1, Puerto 1.

Configurar rangos de puertos simultaneos:
  switch(config)# interface 1/1/1-1/1/24
  switch(config-if<1/1/1-1/1/24>)# description Puertos_Usuarios_Piso1
  switch(config-if<1/1/1-1/1/24>)# no shutdown



## 5. HABILITACION Y ESTADO DE PUERTOS

En AOS-CX, los puertos de datos suelen estar habilitados por defecto, pero es
fundamental conocer los comandos de administracion:

Apagar administrativamente un puerto:
  switch(config)# interface 1/1/5
  switch(config-if)# shutdown

Encender el puerto:
  switch(config-if)# no shutdown

Configurar descripcion y velocidad:
  switch(config-if)# description Conexión_AP_Piso_2
  switch(config-if)# speed-duplex 1000-full   (o 'auto' para autonegociacion)



## 6. COMANDOS DE DIAGNOSTICO Y VISUALIZACION (SHOW)

Visualizar la configuracion activa:
  switch# show running-config

Visualizar resumen de todas las interfaces (estado, VLAN, duplex, velocidad):
  switch# show interface brief

Visualizar detalles de un puerto especifico:
  switch# show interface 1/1/1

Visualizar informacion de version de software y hardware:
  switch# show version

Visualizar estado del chasis, temperatura, fuentes de poder y ventiladores:
  switch# show system
  switch# show environment
  switch# show environment power-supply
  switch# show environment fan

Visualizar tabla de direcciones MAC aprendidas:
  switch# show mac-address

Visualizar vecinos conectados por LLDP / CDP:
  switch# show lldp info remote-device
  switch# show cdp neighbor detail



## 7. GUARDADO Y PUNTOS DE RESTAURACION (CHECKPOINTS)

A diferencia de otros sistemas donde solo existe running y startup, ArubaOS-CX
cuenta con un motor de "Checkpoints" (snapshots de configuracion):

Guardado clasico (guarda running-config en startup-config):
  switch# write memory
  (tambien valido: copy running-config startup-config)

Crear un Checkpoint manual antes de un cambio critico:
  switch# checkpoint create Antes_De_Cambio_VLANs

Ver lista de checkpoints guardados:
  switch# checkpoint list

Comparar cambios entre la configuracion activa y el checkpoint:
  switch# checkpoint diff Antes_De_Cambio_VLANs

Restaurar la configuracion a un checkpoint previo (Rollback instantaneo sin reiniciar):
  switch# checkpoint rollback Antes_De_Cambio_VLANs



## 8. REINICIO Y RESTABLECIMIENTO DE FABRICA

Reiniciar el switch de inmediato:
  switch# boot system

Reiniciar seleccionando particion de firmware (primaria o secundaria):
  switch# boot system primary
  switch# boot system secondary

Borrar configuracion de inicio (al reiniciar volvera a valores de fabrica):
  switch# erase startup-config

Restablecimiento completo seguro y borrado de certificados (Zeroize):
  switch# zeroize

## (Confirma con 'y'; el switch borrara claves criptograficas, logs y configuracion).
