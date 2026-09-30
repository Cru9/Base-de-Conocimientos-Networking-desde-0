# 09. ALTA DISPONIBILIDAD (VRRP Y APILAMIENTO FISICO / STACKING)

> **TP-LINK (JETSTREAM SWITCHES) - GUIA DE COMANDOS Y CONFIGURACION**


---



## 1. ALTA DISPONIBILIDAD EN CONMUTADORES TP-LINK

Para evitar que un fallo en un equipo desconecte a toda la organizacion, los
switches TP-Link JetStream de nivel corporativo ofrecen dos mecanismos esenciales:

1. VRRP (Virtual Router Redundancy Protocol): Redundancia de puerta de enlace
   en Capa 3 entre switches independientes (Activo / En espera).
2. Apilamiento Fisico (Physical Stacking): Unificacion de multiples conmutadores
   en un solo equipo logico de gestion mediante enlaces de alta velocidad 10G SFP+.



## 2. CONFIGURACION DE VRRP (GATEWAY REDUNDANTE L3)

Permite que dos switches L3 compartan una IP Virtual. Si el switch Maestro (Master)
sufre una averia de hardware o perdida de energia, el switch de Respaldo (Backup)
asume el trafico de forma transparente sin interrupcion para los usuarios.


### a) Switch Principal (Master - Prioridad 120):

```cisco
  SW-01(config)# interface vlan 10
  SW-01(config-if)# ip address 192.168.10.2 255.255.255.0
  SW-01(config-if)# vrrp 1 ip 192.168.10.1
  SW-01(config-if)# vrrp 1 priority 120
  SW-01(config-if)# vrrp 1 preempt
  SW-01(config-if)# no shutdown
  SW-01(config-if)# exit

b) Switch Secundario (Backup - Prioridad 100 por defecto):
  SW-02(config)# interface vlan 10
  SW-02(config-if)# ip address 192.168.10.3 255.255.255.0
  SW-02(config-if)# vrrp 1 ip 192.168.10.1
  SW-02(config-if)# vrrp 1 priority 100
  SW-02(config-if)# vrrp 1 preempt
  SW-02(config-if)# no shutdown
  SW-02(config-if)# exit

Nota: Los clientes de la red configuran como Default Gateway la direccion virtual
192.168.10.1.
```


## 3. APILAMIENTO FISICO (PHYSICAL STACKING)

Disponible en conmutadores JetStream equipados con puertos 10G SFP+ (ej. series
SG3428X, SG3452X, SX3016F).

Ventajas:
- Gestion mediante una sola direccion IP y una unica consola.
- Tolerancia a fallos: Si un switch se apaga, los demas siguen operando.
- Soporte de Cross-Stack LAG (enlaces agregados repartidos entre diferentes unidades).

Configuracion del Stacking:
Paso 1: Habilitar los puertos dedicados al apilamiento en cada unidad:
```cisco
  SW-01(config)# stack port ten-gigabitEthernet 1/0/25 enable
  SW-01(config)# stack port ten-gigabitEthernet 1/0/26 enable

Paso 2: Asignar la prioridad de la unidad Master (mayor prioridad = Maestro):
  SW-01(config)# stack unit 1 priority 20

Paso 3: Conectar los cables DAC 10G o fibra en topologia de anillo (Ring Topology)
y reiniciar las unidades subordinadas para que se integren al stack.

Al unirse, los puertos se identificaran automaticamente por su numero de unidad:
- Unidad 1: gigabitEthernet 1/0/1 a 1/0/24
- Unidad 2: gigabitEthernet 2/0/1 a 2/0/24
```


## 4. AGREGACION MULTI-CHASIS (CROSS-STACK LAG)

Conecta un servidor o switch de acceso repartiendo los cables fisicos entre dos
unidades del stack para soportar la caida de un switch completo:

```cisco
  SW-STACK(config)# interface gigabitEthernet 1/0/20   (Puerto en el Switch 1)
  SW-STACK(config-if)# channel-group 5 mode active
  SW-STACK(config-if)# exit

  SW-STACK(config)# interface gigabitEthernet 2/0/20   (Puerto en el Switch 2)
  SW-STACK(config-if)# channel-group 5 mode active
  SW-STACK(config-if)# exit

  SW-STACK(config)# interface port-channel 5
  SW-STACK(config-if)# switchport mode trunk
  SW-STACK(config-if)# switchport trunk allowed vlan 10,20,30
```


## 5. VERIFICACION Y COMANDOS DE DIAGNOSTICO

Visualizar estado de los grupos VRRP:
```cisco
  SW-01# show vrrp
  SW-01# show vrrp brief

Visualizar estado del stack fisico y sus unidades miembros:
  SW-STACK# show stack
  SW-STACK# show stack detail

Visualizar el ancho de banda y estado de los enlaces del stack:
```


## SW-STACK# show stack-port
