# 01. FRROUTING (FRR) EN LINUX: ARQUITECTURA, VTYSH, BGP, OSPF Y BFD

> **SISTEMAS OPERATIVOS DE RED ABIERTOS (OPEN NETWORKING & WHITE-BOX)**


---



## 1. ¿QUE ES FRROUTING (FRR) Y POR QUE DOMINA LA INFRAESTRUCTURA MODERNA?

FRRouting (FRR) es la suite de enrutamiento IP de codigo abierto mas rapida y robusta
para sistemas operativos Linux y Unix. Es un proyecto oficial de la Linux Foundation
mantenido por ingenieros de Cumulus, Nvidia, Red Hat, Orange y 6WIND.

FRR se utiliza hoy en dia como motor de ruteo dentro de:
- SONiC (Microsoft Azure datacenter OS)
- Cumulus Linux (Nvidia)
- Kubernetes CNI plugins (Cilium BGP Control Plane, Calico BGP)
- Routers de borde e hipervisores Proxmox / KVM

ARQUITECTURA DE DAEMONS DE FRR:

```text
               +--------------------------------------+
               |     VTYSH (Cisco-like Unified CLI)   |
               +--------------------------------------+
                                   |
         +-------------+-----------+-----------+-------------+
         |             |           |           |             |
         v             v           v           v             v
     [ bgpd ]      [ ospfd ]   [ isisd ]   [ bfdd ]      [ staticd ]
     (BGP/EVPN)    (OSPFv2)    (IS-IS)     (BFD Subseg)  (Rutas Estaticas)
         |             |           |           |             |
         +-------------+-----------+-----------+-------------+
                                   |
                                   v
                      +--------------------------+
                      |          ZEBRA           | <--- Daemon Central de Enrutamiento
                      +--------------------------+
                                   | (Netlink Sockets)
                                   v
                      +--------------------------+
                      |   LINUX KERNEL (FIB)     | <--- Reenvio de paquetes de datos
                      +--------------------------+
```


## 2. INSTALACION Y HABILITACION DE DAEMONS EN UBUNTU LINUX

A. Instalar paquetes oficiales de FRR:
   sudo apt-get update
   sudo apt-get install -y frr frr-pythontools

B. Habilitar el reenvio de paquetes en el Kernel (/etc/sysctl.conf):
   net.ipv4.ip_forward = 1
   net.ipv6.conf.all.forwarding = 1
   sudo sysctl -p

C. Activar los daemons requeridos en /etc/frr/daemons:
   zebra=yes
   bgpd=yes
   ospfd=yes
   ospf6d=no
   ripd=no
   isisd=no
   bfdd=yes
   staticd=yes

D. Reiniciar el servicio de FRR:
   sudo systemctl restart frr
   sudo systemctl enable frr



## 3. CONFIGURACION MEDIANTE LA CONSOLA UNIFICADA VTYSH

Para configurar FRR, se ingresa con el comando 'vtysh'. La sintaxis es 99% identica
a Cisco IOS:

sudo vtysh
Router-FRR# configure terminal

! 1. Definir nombre y contrasena
hostname Linux-Core-FRR
log syslog informational

! 2. Configurar Interfaces Fisicas y Direccionamiento
interface eth1
 description ENLACE_LAN_CAMPUS
```text
 ip address 10.10.10.1/24
 ip ospf area 0
 exit

interface eth2
 description ENLACE_WAN_ISP
 ip address 200.50.10.2/30
 exit

! 3. Configurar OSPFv2 para la red interna
router ospf
 ospf router-id 10.10.10.1
 redistribute connected metric-type 1
 exit

! 4. Configurar Deteccion de Fallas Subsegundo (BFD)
bfd
 peer 200.50.10.1 interface eth2
  detect-multiplier 3
  receive-interval 300
  transmit-interval 300
 exit
exit

! 5. Configurar BGP Dinamico hacia el ISP con soporte BFD
router bgp 65001
 bgp router-id 10.10.10.1
 bgp log-neighbor-changes
 no bgp default ipv4-unicast

 neighbor 200.50.10.1 remote-as 64500
 neighbor 200.50.10.1 description PEER_ISP_PRINCIPAL
 neighbor 200.50.10.1 bfd

 address-family ipv4 unicast
  network 10.10.0.0/16
  neighbor 200.50.10.1 activate
  neighbor 200.50.10.1 soft-reconfiguration inbound
 exit-address-family
exit

! 6. Guardar la configuracion en el disco (/etc/frr/frr.conf)
Router-FRR# write memory
[OK] Configuration saved to /etc/frr/frr.conf
```


## 4. VINCULACION ENTRE FRR Y EL KERNEL DE LINUX

Cuando FRR aprende una ruta mediante BGP u OSPF, Zebra la inyecta inmediatamente
en la tabla de enrutamiento del Kernel de Linux.

Comparacion de comandos:
- Para ver la tabla de enrutamiento en la consola de red (vtysh):
  vtysh -c "show ip route"
  O>* 10.10.20.0/24 [110/20] via 10.10.10.2, eth1, weight 1, 00:15:32
  B>* 0.0.0.0/0 [20/0] via 200.50.10.1, eth2, weight 1, 01:40:11

- Para ver como el Kernel de Linux aplica la ruta en el sistema operativo:
  ip route show
  default via 200.50.10.1 dev eth2 proto bgp metric 20
  10.10.20.0/24 via 10.10.10.2 dev eth1 proto ospf metric 20



## 5. COMANDOS DE MONITOREO Y VERIFICACION EN VTYSH

1. Verificar estado de la sesion BGP:
```text
   show ip bgp summary
   ! Neighbor: 200.50.10.1  V: 4  AS: 64500  Up/Down: 01:40:11  State/PfxRcd: 15

2. Verificar vecinos OSPF:
   show ip ospf neighbor
   ! Neighbor ID: 10.10.10.2  Pri: 1  State: Full/DR  Address: 10.10.10.2  Interface: eth1

3. Verificar que BFD este monitoreando el enlace en 300 milisegundos:
   show bfd peers
```


## ! Session up: Yes  Local: 200.50.10.2  Remote: 200.50.10.1  Status: Up  Uptime: 01:40:11
