# MANUAL MAESTRO DE CONFIGURACION DE SWITCHES CISCO (IOS / IOS-XE)


---


Bienvenido a tu coleccion de guias de configuracion para switches Cisco Catalyst 
y switches basados en Cisco IOS / IOS-XE.

Cada archivo de texto (.txt) aborda un nivel de complejidad progresivo, explicado 
paso a paso de forma directa, practica y con sintaxis real de produccion.


## INDICE DE ARCHIVOS:


[01_conceptos_basicos_y_modos.md](./01_conceptos_basicos_y_modos.md)
   -> Modos de acceso (User >, Privileged #, Global Config (config)#, Interface),
      atajos de teclado esenciales, comandos "show" basicos, guardar configuracion
      (write memory / copy run start) y reinicio seguro (reload).

[02_configuracion_inicial_y_seguridad.md](./02_configuracion_inicial_y_seguridad.md)
   -> Nombre del switch (hostname), ajuste de hora/reloj, banners legales (MOTD),
      contrasena de enable encriptada (secret), seguridad de consola y configuracion
      completa de acceso remoto seguro SSH con llaves RSA y lineas VTY.

[03_gestion_ip_y_vlans_basicas.md](./03_gestion_ip_y_vlans_basicas.md)
   -> Creacion de VLANs, modos de puerto (Access y Trunk), configuracion de rangos
      de puertos (interface range), VLAN de voz para telefonos IP y configuracion
      de la IP de administracion (SVI / Interface Vlan).

[04_enrutamiento_intervlan_y_servidor_dhcp.md](./04_enrutamiento_intervlan_y_servidor_dhcp.md)
   -> Enrutamiento de Capa 3 entre VLANs (ip routing), puertos enrutados (no switchport),
      configuracion de servidor DHCP local en el switch (Pools, exclusiones, DNS),
      agente de retransmision (ip helper-address) y rutas estaticas.

[05_redundancia_y_agregacion_etherchannel_stp.md](./05_redundancia_y_agregacion_etherchannel_stp.md)
   -> Agregacion de enlaces EtherChannel (LACP 802.3ad / PAgP) para tolerancia a fallas
      y doble ancho de banda, mas Spanning Tree (Rapid-PVST+, Root Bridge, PortFast
      y BPDU Guard contra bucles accidentales).

[06_seguridad_de_capa_2_y_puertos.md](./06_seguridad_de_capa_2_y_puertos.md)
   -> Port Security (bloqueo por direccion MAC y modo Sticky), DHCP Snooping
      (bloqueo de routers/servidores DHCP piratas), Dynamic ARP Inspection (DAI)
      y control de tormentas de broadcast (Storm Control).

[07_enrutamiento_dinamico_ospf.md](./07_enrutamiento_dinamico_ospf.md)
   -> Configuracion de OSPFv2 en switches multicapa: Router-ID, Area 0, mascaras
      wildcard, interfaces pasivas (passive-interface) y autenticacion MD5.

[08_listas_de_control_de_acceso_acl_y_qos.md](./08_listas_de_control_de_acceso_acl_y_qos.md)
   -> Listas de control de acceso estandar y extendidas (ACL 100+), aplicacion en
      interfaces, limitacion de ancho de banda (QoS MQC) y puerto espejo (SPAN /
      Port Mirroring) para analisis con Wireshark.

[09_alta_disponibilidad_hsrp_y_stackwise.md](./09_alta_disponibilidad_hsrp_y_stackwise.md)
   -> Alta disponibilidad de primer salto con HSRP (Gateway virtual redundante entre
      dos switches Core con seguimiento de enlaces) y apilamiento fisico Cisco
      StackWise / FlexStack (operar multiples switches como uno solo).

[10_mantenimiento_respaldo_y_resolucion_fallas.md](./10_mantenimiento_respaldo_y_resolucion_fallas.md)
   -> Copias de seguridad por TFTP de la configuracion (running-config) e imagen IOS (.bin),
      procedimiento de recuperacion de contrasena, monitoreo de CPU/RAM, diagnostico
      optico SFP (DOM) y descubrimiento con CDP / LLDP.


## TABLA DE EQUIVALENCIAS RAPIDAS (CISCO IOS vs HUAWEI VRP):

Accion                         Cisco IOS                 Huawei VRP
-----------------------------  ------------------------  -----------------------
Entrar a modo de config        enable / config t         system-view
Retroceder / Salir             exit                      quit
Volver al inicio               end / Ctrl+Z              return / Ctrl+Z
Borrar / Negar comando         no [comando]              undo [comando]
Ver configuracion actual       show run                  display current-configuration
Ver interfaces resumen         show ip int brief         display ip interface brief
Guardar cambios                write memory / copy run   save
Reiniciar equipo               reload                    reboot
Crear VLANs                    vlan 10,20                vlan batch 10 20
Tipo de puerto de acceso       switchport mode access    port link-type access
Asignar VLAN a puerto          switchport access vlan 10 port default vlan 10
Tipo de puerto troncal         switchport mode trunk     port link-type trunk
Permitir VLANs en troncal      switchport trunk allowed  port trunk allow-pass vlan
Canal de agregacion            channel-group 1 mode ...  eth-trunk 1

## Interfaz logica de VLAN        interface Vlan 10         interface Vlanif 10

