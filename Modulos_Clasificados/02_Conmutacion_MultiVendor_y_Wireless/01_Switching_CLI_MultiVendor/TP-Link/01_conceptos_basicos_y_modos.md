# 01. CONCEPTOS BASICOS, MODOS DE OPERACION Y COMANDOS INICIALES

> **TP-LINK (JETSTREAM SWITCHES) - GUIA DE COMANDOS Y CONFIGURACION**


---



## 1. ARQUITECTURA DE CONMUTADORES TP-LINK JETSTREAM

La linea JetStream comprende conmutadores gestionables empresariales de Capa 2,
Capa 2+ y Capa 3 (series TL-SG, TL-SX y conmutadores Omada Smart/Managed).

Pueden operar en dos modalidades:

### a) Modo Independiente (Standalone CLI / Web): Gestion directa puerto por puerto

   mediante consola serie, SSH, Telnet o interfaz web local.

### b) Modo Controlador SDN (Omada SDN): Administracion centralizada por software o

   controlador en la nube (la mayoria de los comandos CLI son adoptados por el
   controlador).

Esta guia se enfoca en el potente CLI de TP-Link (muy similar al estandar Cisco).



## 2. JERARQUIA DE MODOS DEL CLI


| Modo | Prompt | Descripcion |
| :--- | :--- | :--- |
| Modo Usuario (User EXEC) | TP-LINK> | Consultas basicas de solo lectura. |
| Modo Privilegiado (Enable) | TP-LINK# | Diagnostico, pruebas, guardado y reinicio. |
| Modo Configuracion Global | TP-LINK(config)# | Cambios de parametros globales del switch. |
| Modo Interfaz Fisica | TP-LINK(config-if)# | Configuracion de un puerto especifico. |
| Modo Rango de Interfaces | TP-LINK(config-if-range)# | Configuracion simultanea de puertos. |
| Modo VLAN | TP-LINK(config-vlan)# | Nombrado y estado de VLANs. |
| Modo Port-Channel (LAG) | TP-LINK(config-port-cha..)# Enlaces agregados LACP. |  |
| Modo Interfaz VLAN (SVI) | TP-LINK(config-if)# | Direccion IP y Gateway de VLAN. |




## 3. TRANSICION ENTRE MODOS

De Usuario a Privilegiado:
  TP-LINK> enable
  TP-LINK#

De Privilegiado a Configuracion Global:
  TP-LINK# configure
  TP-LINK(config)#

Ingresar a una interfaz fisica:
  TP-LINK(config)# interface gigabitEthernet 1/0/1
  TP-LINK(config-if)#

Configurar un rango de interfaces a la vez:
  TP-LINK(config)# interface range gigabitEthernet 1/0/1-24
  TP-LINK(config-if-range)#

Retroceder un nivel:
  TP-LINK(config-if)# exit
  TP-LINK(config)#

Volver directamente al modo privilegiado (#):
  TP-LINK(config-if)# end
  (o presionar Ctrl + Z)

Cerrar sesion (Logout):
  TP-LINK# exit



## 4. NOMENCLATURA DE PUERTOS EN TP-LINK JETSTREAM

TP-Link utiliza la sintaxis de 3 coordenadas: [Unidad] / [Ranura] / [Puerto]

Tipos comunes de puertos:
  fastEthernet 1/0/1       -> Puerto 10/100 Mbps (modelos antiguos o FE).
  gigabitEthernet 1/0/1    -> Puerto 10/100/1000 Mbps de cobre (RJ45).
  gigabitEthernet 1/0/24   -> Puerto 24 de cobre.
  gigabitEthernet 1/0/25   -> Ranura SFP 1G (uplink).
  ten-gigabitEthernet 1/0/1-> Ranura SFP+ 10G (modelos TL-SX o switches con uplink 10G).

Ejemplo de configuracion basica de puerto:
  TP-LINK(config)# interface gigabitEthernet 1/0/5
  TP-LINK(config-if)# description Enlace_Hacia_Impresora_Piso1
  TP-LINK(config-if)# speed auto
  TP-LINK(config-if)# duplex auto
  TP-LINK(config-if)# no shutdown



## 5. HABILITACION Y ESTADO DE PUERTOS

Apagar administrativamente un puerto:
  TP-LINK(config)# interface gigabitEthernet 1/0/10
  TP-LINK(config-if)# shutdown

Encender el puerto:
  TP-LINK(config-if)# no shutdown



## 6. COMANDOS DE DIAGNOSTICO Y VISUALIZACION (SHOW)

Visualizar la configuracion activa en memoria RAM:
  TP-LINK# show running-config

Visualizar la configuracion guardada en memoria Flash:
  TP-LINK# show startup-config

Visualizar estado de los puertos (enlace, velocidad, duplex, VLAN):
  TP-LINK# show interface status
  TP-LINK# show interface gigabitEthernet 1/0/1

Visualizar informacion general del sistema (modelo, version de firmware, MAC base):
  TP-LINK# show system-info

Visualizar la tabla de direcciones MAC aprendidas:
  TP-LINK# show mac address-table

Visualizar vecinos conectados por LLDP:
  TP-LINK# show lldp neighbor-information



## 7. GUARDADO Y PERSISTENCIA DE LA CONFIGURACION

En TP-Link, los cambios realizados en modo de configuracion se aplican de inmediato
en la memoria volatil (running-config). Para evitar perderlos al reiniciar:

Guardar la configuracion activa en la memoria de inicio:
  TP-LINK# copy running-config startup-config
  (Presionar Enter para confirmar cuando el sistema pregunte).



## 8. REINICIO Y RESTABLECIMIENTO DE FABRICA

Reiniciar el switch:
  TP-LINK# reboot
  (El sistema preguntara si desea guardar los cambios no guardados).

Restablecer el conmutador a sus valores predeterminados de fabrica:
  TP-LINK# reset
  (Confirma con 'y'; el switch borrara la configuracion y se reiniciara con la

## IP por defecto, habitualmente 192.168.0.1).
