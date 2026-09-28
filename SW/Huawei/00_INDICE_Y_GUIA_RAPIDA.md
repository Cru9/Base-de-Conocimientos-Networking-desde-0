# MANUAL MAESTRO DE CONFIGURACION DE SWITCHES HUAWEI (VRP)


---


Bienvenido a tu coleccion de guias de configuracion para switches Huawei VRP.
Cada archivo de texto (.txt) aborda un nivel de complejidad progresivo, explicado 
paso a paso de forma directa y practica.


## INDICE DE ARCHIVOS:


[01_conceptos_basicos_y_modos.md](./01_conceptos_basicos_y_modos.md)
   -> Modos de acceso (<HUAWEI>, [HUAWEI]), atajos de teclado esenciales,
      comandos "display" basicos, guardar configuracion (save) y reinicio (reboot).

[02_configuracion_inicial_y_seguridad.md](./02_configuracion_inicial_y_seguridad.md)
   -> Nombre del switch (sysname), ajuste de hora/reloj, banners de bienvenida,
      contrasenas de consola y configuracion completa de acceso remoto SSH (STelnet)
      con llaves RSA y usuarios AAA.

[03_gestion_ip_y_vlans_basicas.md](./03_gestion_ip_y_vlans_basicas.md)
   -> Creacion de VLANs individuales y en lote (batch), modos de puerto (Access, 
      Trunk, Hybrid), asignacion de puertos y configuracion de IP de gestion (Vlanif).

[04_enrutamiento_intervlan_y_servidor_dhcp.md](./04_enrutamiento_intervlan_y_servidor_dhcp.md)
   -> Enrutamiento de Capa 3 entre VLANs, asignacion de gateways, configuracion 
      de servidor DHCP local en el switch (Pools, rangos, DNS) y rutas estaticas.

[05_redudancia_y_agregacion_eth_trunk.md](./05_redudancia_y_agregacion_eth_trunk.md)
   -> Agregacion de enlaces (Eth-Trunk / LACP 802.3ad) para duplicar velocidad y 
      tolerancia a fallas, mas protocolo Spanning Tree (RSTP, Root Bridge, Edged-Port
      y proteccion BPDU contra bucles).

[06_seguridad_de_capa_2_y_puertos.md](./06_seguridad_de_capa_2_y_puertos.md)
   -> Port Security (bloqueo por direccion MAC), DHCP Snooping (bloqueo de 
      routers/servidores DHCP piratas) y control de tormentas de broadcast.

[07_enrutamiento_dinamico_ospf.md](./07_enrutamiento_dinamico_ospf.md)
   -> Configuracion de OSPFv2 en switches multicapa: Router-ID, Area 0, mascaras
      wildcard, silent-interfaces y encriptacion MD5 entre switches.

[08_listas_de_control_de_acceso_acl_y_qos.md](./08_listas_de_control_de_acceso_acl_y_qos.md)
   -> Filtros de paquetes con ACLs basicas y avanzadas (3000), limitacion de ancho 
      de banda por puerto (QoS Rate Limiting) y puerto espejo (Mirroring) para Wireshark.

[09_alta_disponibilidad_vrrp_y_apilamiento_istack.md](./09_alta_disponibilidad_vrrp_y_apilamiento_istack.md)
   -> Alta disponibilidad con VRRP (IP virtual compartida entre dos switches Core 
      con seguimiento de enlaces) y apilamiento iStack (unir fisicamente varios 
      switches en uno solo logico).

[10_mantenimiento_respaldo_y_resolucion_fallas.md](./10_mantenimiento_respaldo_y_resolucion_fallas.md)
   -> Respaldos de configuracion (vrpcfg.zip) por TFTP, actualizacion de firmware VRP (.cc),
      monitoreo de CPU/RAM, diagnostico de potencia optica en fibras SFP y debugging en vivo.


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
