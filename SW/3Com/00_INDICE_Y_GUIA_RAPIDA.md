# MANUAL MAESTRO DE CONFIGURACION DE SWITCHES 3COM (COMWARE OS)


---


Bienvenido a tu coleccion de guias de configuracion para switches 3Com (series
SuperStack 4, 4200G, 4500, 4800G, 5500G, 7700 y modelos H3C/HPE Comware).

NOTA HISTORICA IMPORTANTE:
3Com creo junto con Huawei la alianza H3C, y sus switches empresariales mas populares
utilizan el sistema operativo "Comware". Por esta razon, la sintaxis de 3Com es
extremadamente similar a la de Huawei, con pequeñas variaciones en nombres de 
interfaces (ej. "Vlan-interface" en 3Com vs "Vlanif" en Huawei).


## INDICE DE ARCHIVOS:


[01_conceptos_basicos_y_modos.md](./01_conceptos_basicos_y_modos.md)
   -> Modos de acceso (<3Com>, [3Com]), atajos de teclado esenciales,
      comandos "display", guardar configuracion (save) y reinicio (reboot).

[02_configuracion_inicial_y_seguridad.md](./02_configuracion_inicial_y_seguridad.md)
   -> Nombre del switch (sysname), fecha/hora, banners de bienvenida, contrasena
      de consola y configuracion completa de acceso remoto SSH / Telnet con usuarios AAA.

[03_gestion_ip_y_vlans_basicas.md](./03_gestion_ip_y_vlans_basicas.md)
   -> Creacion de VLANs, modos de puerto (Access, Trunk, Hybrid), asignacion de
      puertos y configuracion de IP de administracion (Vlan-interface).

[04_enrutamiento_intervlan_y_servidor_dhcp.md](./04_enrutamiento_intervlan_y_servidor_dhcp.md)
   -> Enrutamiento de Capa 3 entre VLANs (Gateways), configuracion de servidor
      DHCP local en el switch (Pools, exclusiones, DNS) y rutas estaticas.

[05_redudancia_y_agregacion_link_aggregation_stp.md](./05_redudancia_y_agregacion_link_aggregation_stp.md)
   -> Agregacion de enlaces (Link-Aggregation / LACP 802.3ad) para duplicar velocidad
      y redundancia, mas Spanning Tree (RSTP, Root Bridge, Edge-Port y proteccion BPDU).

[06_seguridad_de_capa_2_y_puertos.md](./06_seguridad_de_capa_2_y_puertos.md)
   -> Port Security (bloqueo por direccion MAC), DHCP Snooping (bloqueo de 
      routers falsos) y control de tormentas de broadcast (storm-constrain).

[07_enrutamiento_dinamico_ospf.md](./07_enrutamiento_dinamico_ospf.md)
   -> Configuracion de OSPFv2 en switches multicapa 3Com: Router-ID, Area 0,
      mascaras wildcard, silent-interfaces y autenticacion MD5 entre switches.

[08_listas_de_control_de_acceso_acl_y_qos.md](./08_listas_de_control_de_acceso_acl_y_qos.md)
   -> Filtros de paquetes con ACL basicas y avanzadas (3000), control de ancho de
      banda por puerto (Line Rate QoS) y puerto espejo (Port Mirroring / Wireshark).

[09_alta_disponibilidad_vrrp_y_xrn_irf.md](./09_alta_disponibilidad_vrrp_y_xrn_irf.md)
   -> Alta disponibilidad con VRRP (IP virtual compartida entre dos switches Core)
      y tecnologia de apilamiento 3Com XRN / IRF (unir multiples switches en uno).

[10_mantenimiento_respaldo_y_resolucion_fallas.md](./10_mantenimiento_respaldo_y_resolucion_fallas.md)
   -> Respaldos de configuracion (.cfg) por TFTP, actualizacion de firmware (.bin),
      diagnostico de fibra optica SFP, monitoreo de CPU/RAM y debugging en vivo.


## TABLA DE EQUIVALENCIAS (3COM COMWARE vs CISCO IOS vs HUAWEI VRP):

Accion                         3Com Comware           Cisco IOS              Huawei VRP
-----------------------------  ---------------------  ---------------------  ---------------------
Entrar a modo config           system-view            enable / config t      system-view
Retroceder nivel               quit                   exit                   quit
Volver al inicio               return / Ctrl+Z        end / Ctrl+Z           return / Ctrl+Z
Borrar / Negar comando         undo [comando]         no [comando]           undo [comando]
Ver configuracion actual       display current-conf   show run               display current-conf
Ver interfaces resumen         display ip int brief   show ip int brief      display ip int brief
Guardar cambios                save                   write memory / wr      save
Reiniciar equipo               reboot                 reload                 reboot
Crear VLANs                    vlan 10                vlan 10                vlan 10
Tipo de puerto de acceso       port link-type access  switchport mode access port link-type access
Asignar VLAN a puerto          port access vlan 10    switchport access vlan port default vlan 10
Tipo de puerto troncal         port link-type trunk   switchport mode trunk  port link-type trunk
Permitir VLANs en troncal      port trunk permit vlan switchport trunk allow port trunk allow-pass
Canal de agregacion            link-aggregation group channel-group 1 mode   eth-trunk 1

## Interfaz logica de VLAN        interface Vlan-int 10  interface Vlan 10      interface Vlanif 10
