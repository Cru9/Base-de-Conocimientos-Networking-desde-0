# MANUAL MAESTRO DE CONFIGURACION DE SWITCHES HP / ARUBA (PROCURVE / ARUBAOS-S)


---


Bienvenido a tu coleccion de guias de configuracion para switches HP ProCurve,
HPE y ArubaOS-S (series clasicas y modernas como ProCurve 2510, 2530, 2810, 2910, 
2920, 3500yl, 3800, 5400zl, y Aruba 2530, 2540, 2930F/M).


## ¿PROCURVE (ARUBAOS-S) O HPE COMWARE?

En el ecosistema de HP existen dos lineas historicas:
1. HP ProCurve / Provision (ArubaOS-S): La arquitectura mas famosa y extendida 
   en switches de acceso y distribucion de HP. Tiene una sintaxis unica y muy
   facil de entender centrada en VLANs ("tagged" / "untagged"). Este manual
   esta dedicado 100% a esta arquitectura.
2. HPE Comware (A-Series / H3C): Se utiliza en switches de Data Center y Core de 
   alta gama. Para esta serie, consulta directamente la carpeta "3Com", ya que 
   comparten exactamente el mismo sistema operativo Comware.


## INDICE DE ARCHIVOS:


[01_conceptos_basicos_y_modos.md](./01_conceptos_basicos_y_modos.md)
   -> Modos de acceso (>, #, (config)#), atajos de teclado, menu visual (menu),
      comandos "show", guardar cambios (write memory) y reinicio seguro (reload).

[02_configuracion_inicial_y_seguridad.md](./02_configuracion_inicial_y_seguridad.md)
   -> Nombre del switch (hostname), fecha/hora (SNTP), banners MOTD, cuentas de
      administrador (manager/operator), seguridad web SSL y configuracion completa de SSH.

[03_gestion_ip_y_vlans_basicas.md](./03_gestion_ip_y_vlans_basicas.md)
   -> La arquitectura VLAN de HP: puertos "untagged" (Access), "tagged" (Trunk),
      VLAN de voz para telefonos IP y asignacion de IP de gestion en la propia VLAN.

[04_enrutamiento_intervlan_y_servidor_dhcp.md](./04_enrutamiento_intervlan_y_servidor_dhcp.md)
   -> Enrutamiento de Capa 3 entre VLANs (ip routing), gateways en VLANs, agente
      de retransmision DHCP (ip helper-address) y rutas estaticas a Internet.

[05_redudancia_y_agregacion_trunk_lacp_stp.md](./05_redudancia_y_agregacion_trunk_lacp_stp.md)
   -> Agregacion de enlaces (Trunks LACP en terminologia HP) para duplicar velocidad,
      mas Spanning Tree (RSTP / MSTP, Root Bridge, Admin-Edge-Port y BPDU Protection).

[06_seguridad_de_capa_2_y_puertos.md](./06_seguridad_de_capa_2_y_puertos.md)
   -> Port Security (bloqueo por direccion MAC), DHCP Snooping (bloqueo de routers
      piratas), ARP Protection (contra ataques Man-in-the-Middle) y Loop Protection.

[07_enrutamiento_dinamico_ospf.md](./07_enrutamiento_dinamico_ospf.md)
   -> Configuracion de OSPFv2 en switches Capa 3: Router-ID, asociacion de VLANs
      al Area 0, interfaces pasivas y autenticacion MD5 entre switches.

[08_listas_de_control_de_acceso_acl_y_qos.md](./08_listas_de_control_de_acceso_acl_y_qos.md)
   -> Filtros de paquetes con ACL estandar y extendidas, control de ancho de banda
      por puerto (Rate Limiting) y puerto espejo (Port Monitor / Wireshark).

[09_alta_disponibilidad_vrrp_y_apilamiento_vsf.md](./09_alta_disponibilidad_vrrp_y_apilamiento_vsf.md)
   -> Alta disponibilidad con VRRP (Gateway virtual compartido entre switches Core)
      y apilamiento moderno HP/Aruba VSF (Virtual Switching Framework).

[10_mantenimiento_respaldo_y_resolucion_fallas.md](./10_mantenimiento_respaldo_y_resolucion_fallas.md)
   -> Gestion de memoria Flash dual (Primary / Secondary), respaldos por TFTP,
      actualizacion de firmware (.swi), diagnostico optico SFP (DOM) y logs del sistema.


## TABLA DE EQUIVALENCIAS (HP PROCURVE vs CISCO IOS vs HUAWEI VRP):

Accion                         HP ProCurve / Aruba   Cisco IOS              Huawei VRP
-----------------------------  --------------------  ---------------------  ---------------------
Entrar a modo config           enable / config       enable / config t      system-view
Retroceder nivel               exit                  exit                   quit
Volver al inicio               end / Ctrl+Z          end / Ctrl+Z           return / Ctrl+Z
Borrar / Negar comando         no [comando]          no [comando]           undo [comando]
Ver configuracion actual       show run              show run               display current-conf
Ver interfaces resumen         show int brief        show ip int brief      display ip int brief
Guardar cambios                write memory / wr mem write memory / wr      save
Reiniciar equipo               reload                reload                 reboot
Crear VLANs                    vlan 10               vlan 10                vlan 10
Puerto de acceso (Untagged)    vlan 10 untagged 1    switchport access vlan port default vlan 10
Puerto troncal (Tagged)        vlan 10 tagged 24     switchport mode trunk  port link-type trunk
Canal de agregacion (LACP)     trunk 23-24 trk1 lacp channel-group 1 mode   eth-trunk 1

## Interfaz logica de VLAN        vlan 10 (ip address)  interface Vlan 10      interface Vlanif 10
