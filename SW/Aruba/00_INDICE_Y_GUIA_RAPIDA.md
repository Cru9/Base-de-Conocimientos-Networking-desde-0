# MANUAL MAESTRO DE CONFIGURACION DE SWITCHES ARUBA (ARUBAOS-CX)


---


Bienvenido a tu coleccion de guias de configuracion para switches Aruba modernos
basados en ArubaOS-CX (AOS-CX), que abarca las series empresariales actuales:
Aruba CX 6000, 6100, 6200, 6300, 6400, 8320, 8325 y 8400.


## ¿QUE ES ARUBAOS-CX Y EN QUE SE DIFERENCIA DE ARUBAOS-S (PROCURVE)?

ArubaOS-CX es la plataforma de conmutacion moderna de ultima generacion de Aruba (HPE):
- Es un sistema operativo cloud-native basado en Linux, con base de datos en tiempo
  real (State Database) y soporte de automatizacion con APIs REST y Python.
- Su sintaxis de consola adopta el estándar de la industria (similar a Cisco IOS),
  abandonando la sintaxis orientada a VLANs de los antiguos ProCurve.
  * Por ejemplo: En AOS-CX entras a la interfaz y configuras "vlan access 10" o
    "vlan trunk allowed 10,20" directamente en el puerto.
- Si buscas la sintaxis clasica de los switches HP ProCurve / ArubaOS-S (2530, 2920, 5400zl),
  consulta la carpeta hermana "HP".


## INDICE DE ARCHIVOS:


[01_conceptos_basicos_y_modos.md](./01_conceptos_basicos_y_modos.md)
   -> Modos de acceso (switch#, switch(config)#, interfaces), nomenclatura 1/1/1,
      comandos "show", guardar (write memory), reinicio y la tecnologia Checkpoint.

[02_configuracion_inicial_y_seguridad.md](./02_configuracion_inicial_y_seguridad.md)
   -> Nombre del switch (hostname), reloj y NTP, banners MOTD, administracion de
      usuarios locales y roles, llaves criptograficas y acceso remoto seguro SSHv2.

[03_gestion_ip_y_vlans_basicas.md](./03_gestion_ip_y_vlans_basicas.md)
   -> Creacion de VLANs, puertos Access ("vlan access"), puertos Trunk ("vlan trunk allowed"),
      VLAN de voz con LLDP-MED e interfaces virtuales SVI ("interface vlan").

[04_enrutamiento_intervlan_y_servidor_dhcp.md](./04_enrutamiento_intervlan_y_servidor_dhcp.md)
   -> Enrutamiento de Capa 3 entre VLANs, puertos enrutados puros ("routing"),
      agente de retransmision DHCP (ip helper-address) y rutas estaticas.

[05_redudancia_y_agregacion_lag_lacp_stp.md](./05_redudancia_y_agregacion_lag_lacp_stp.md)
   -> Agregacion de enlaces LAG / LACP (Port-Channels) para duplicar velocidad y
      redundancia, mas Spanning Tree (RSTP / MSTP, Root Bridge, Admin-Edge y BPDU Guard).

[06_seguridad_de_capa_2_y_puertos.md](./06_seguridad_de_capa_2_y_puertos.md)
   -> Port-Access Security (bloqueo por MAC y limite de clientes), DHCP Snooping,
      Dynamic ARP Inspection (DAI) y Loop Protection en puertos de acceso.

[07_enrutamiento_dinamico_ospf.md](./07_enrutamiento_dinamico_ospf.md)
   -> Configuracion de OSPFv2 en switches Capa 3: Router-ID, asociacion de VLANs
      al Area 0, interfaces pasivas y autenticacion MD5 entre switches.

[08_listas_de_control_de_acceso_acl_y_qos.md](./08_listas_de_control_de_acceso_acl_y_qos.md)
   -> Filtrado de paquetes con ACL de IPv4, limitacion de ancho de banda por puerto
      (Rate Limiting) y puerto espejo (Mirror Session) para Wireshark.

[09_alta_disponibilidad_vrrp_vsf_y_vsx.md](./09_alta_disponibilidad_vrrp_vsf_y_vsx.md)
   -> Alta disponibilidad con VRRP (Gateway virtual compartido), apilamiento VSF
      (en series CX 6200/6300) y arquitectura de redundancia de Data Center VSX.

[10_mantenimiento_respaldo_y_resolucion_fallas.md](./10_mantenimiento_respaldo_y_resolucion_fallas.md)
   -> Sistema revolucionario de Puntos de Restauracion (Checkpoints y Rollback),
      respaldos por TFTP, actualizacion de firmware, diagnostico optico SFP (DOM) y logs.


## TABLA DE EQUIVALENCIAS (ARUBAOS-CX vs CISCO IOS vs HP PROCURVE):

Accion                         ArubaOS-CX               Cisco IOS              HP ProCurve
-----------------------------  -----------------------  ---------------------  ---------------------
Entrar a modo config           configure terminal / con configure terminal     config
Retroceder nivel               exit                     exit                   exit
Volver al inicio               end / Ctrl+Z             end / Ctrl+Z           end / Ctrl+Z
Borrar / Negar comando         no [comando]             no [comando]           no [comando]
Ver configuracion actual       show running-config      show running-config    show run
Ver interfaces resumen         show interface brief     show ip int brief      show int brief
Guardar cambios                write memory             write memory / wr      write memory / wr mem
Reiniciar equipo               boot system              reload                 reload
Crear VLAN                     vlan 10                  vlan 10                vlan 10
Puerto de acceso               vlan access 10           switchport access vlan untagged 1
Puerto troncal                 vlan trunk allowed 10,20 switchport trunk allow tagged 24
Canal de agregacion (LACP)     interface lag 1          interface port-chan 1  trunk 1-2 trk1 lacp

## Interfaz logica de VLAN        interface vlan 10        interface Vlan 10      vlan 10 (ip address)
