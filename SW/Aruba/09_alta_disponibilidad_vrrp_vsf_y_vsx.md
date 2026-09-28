# 09. ALTA DISPONIBILIDAD (VRRP, APILAMIENTO VSF Y ARQUITECTURA VSX)

> **ARUBA NETWORKS (ARUBAOS-CX) - GUIA DE COMANDOS Y CONFIGURACION**


---



## 1. PANORAMA DE ALTA DISPONIBILIDAD EN ARUBAOS-CX

ArubaOS-CX ofrece tres tecnologias principales de alta disponibilidad segun el
rol y modelo de conmutador:

1. VRRP (Virtual Router Redundancy Protocol): Redundancia de gateway de Capa 3
   estandar entre dos o mas switches independientes (Activo / En espera).
2. VSF (Virtual Switching Framework): Apilamiento de Capa 2/3 con un solo plano
   de control y gestion centralizada (ideal para switches de acceso CX 6200 y 6300).
3. VSX (Virtual Switching Extension): Arquitectura de chasis dual para centros
   de datos y nucleos (Core/Agregacion CX 6400, 8320, 8325, 8360, 8400) con
   planos de control independientes, sincronizacion de estado y cero tiempo de caida.



## 2. CONFIGURACION DE VRRPv2 / VRRPv3

Permite que dos switches compartan una direccion IP virtual que sirve de Default
Gateway para los clientes. Si el Master falla, el Backup asume instantaneamente.


### a) Switch Primario (Master - Prioridad 110):

```cisco
  SW-01(config)# interface vlan 10
  SW-01(config-if-vlan)# ip address 192.168.10.2/24
  SW-01(config-if-vlan)# vrrp 1 address-family ipv4
  SW-01(config-if-vlan-vrrp-ipv4-1)# address 192.168.10.1 primary
  SW-01(config-if-vlan-vrrp-ipv4-1)# priority 110
  SW-01(config-if-vlan-vrrp-ipv4-1)# preempt
  SW-01(config-if-vlan-vrrp-ipv4-1)# no shutdown
  SW-01(config-if-vlan-vrrp-ipv4-1)# exit

b) Switch Secundario (Backup - Prioridad 100 por defecto):
  SW-02(config)# interface vlan 10
  SW-02(config-if-vlan)# ip address 192.168.10.3/24
  SW-02(config-if-vlan)# vrrp 1 address-family ipv4
  SW-02(config-if-vlan-vrrp-ipv4-1)# address 192.168.10.1 primary
  SW-02(config-if-vlan-vrrp-ipv4-1)# priority 100
  SW-02(config-if-vlan-vrrp-ipv4-1)# preempt
  SW-02(config-if-vlan-vrrp-ipv4-1)# no shutdown
  SW-02(config-if-vlan-vrrp-ipv4-1)# exit
```


## 3. APILAMIENTO VSF (VIRTUAL SWITCHING FRAMEWORK - CX 6200 / 6300)

Permite interconectar hasta 8 o 10 switches mediante puertos de enlace ascendente
SFP+ (10G/25G/50G) para que operen como una unica entidad logica administrable.

Paso 1: En el Switch 1 (Conductor / Primario)
```cisco
  SW-01(config)# vsf member 1
  SW-01(config-vsf-member-1)# type jl660a      (o el modelo correspondiente)
  SW-01(config-vsf-member-1)# link 1 1/1/49,1/1/50
  SW-01(config-vsf-member-1)# exit
  SW-01(config)# vsf secondary-member 2        (designa el backup del stack)

Paso 2: Conectar fisicamente los cables DAC o fibra entre los puertos VSF.
Al encender el segundo switch, este detectara los enlaces VSF, se unira al stack
y se reiniciara adoptando la numeracion '2/1/x'.

Paso 3: Proteccion contra cerebro dividido (Split-Brain Detection):
  SW-01(config)# vsf split-detect mgmt         (usa el puerto de gestion para validar quorum)
```


## 4. ARQUITECTURA VSX (VIRTUAL SWITCHING EXTENSION - CX 6400 / 83XX)

La tecnologia lider de Aruba para Core y Data Center. Proporciona:
- Planos de control independientes (si un switch crashea, el otro sigue operando).
- Sincronizacion de tablas OVSDB mediante el Inter-Switch Link (ISL).
- Active-Active L3 Default Gateway sin sobrecarga de VRRP.
- Agregacion Multi-Chassis (VSX-LAG).

Estructura de configuracion basica en Switch VSX-A:
```cisco
  SW-A(config)# vsx
  SW-A(config-vsx)# system-mac 02:00:00:00:00:01
  SW-A(config-vsx)# inter-switch-link lag 256
  SW-A(config-vsx)# keepalive peer 192.168.254.2 source 192.168.254.1 vrf keepalive_vrf
  SW-A(config-vsx)# role primary

Active-Gateway en interfaz de VLAN (Ambos switches responden con la misma IP y MAC virtual):
  SW-A(config)# interface vlan 10
  SW-A(config-if-vlan)# ip address 192.168.10.2/24
  SW-A(config-if-vlan)# active-gateway ip 192.168.10.1 mac 00:00:5e:00:01:01
```


## 5. COMANDOS DE VERIFICACION Y MONITOREO

Verificar estado de VRRP:
```cisco
  SW-01# show vrrp
  SW-01# show vrrp brief

Verificar estado y topologia del stack VSF:
  SW-01# show vsf
  SW-01# show vsf detail
  SW-01# show vsf topology

Verificar estado completo de la extension VSX:
  SW-A# show vsx status
  SW-A# show vsx status keepalive
  SW-A# show vsx status inter-switch-link
```


## SW-A# show vsx configuration-split
