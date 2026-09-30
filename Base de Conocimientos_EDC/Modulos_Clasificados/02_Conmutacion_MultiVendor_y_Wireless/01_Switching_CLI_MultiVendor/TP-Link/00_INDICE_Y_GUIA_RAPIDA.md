# TP-LINK (JETSTREAM SWITCHES) - BASE DE CONOCIMIENTOS Y GUIA DE CONFIGURACION


---

Bienvenido a la guia de referencia y configuracion de conmutadores TP-Link para
redes empresariales (linea JetStream gestionada L2/L2+/L3, series TL-SG, TL-SX
y conmutadores compatibles con modo independiente y Omada SDN CLI).


## INDICE GENERAL DE ARCHIVOS DE LA BASE DE CONOCIMIENTOS:

[00_INDICE_Y_GUIA_RAPIDA.md](./00_INDICE_Y_GUIA_RAPIDA.md)
    - Resumen maestro, mapa de archivos, filosofia del CLI de TP-Link JetStream
      y tabla de equivalencias con Cisco y otros fabricantes.

[01_conceptos_basicos_y_modos.md](./01_conceptos_basicos_y_modos.md)
    - Jerarquia de modos en el CLI (User, Enable, Config, Interface, VLAN).
    - Nomenclatura de puertos (gigabitEthernet 1/0/1, ten-gigabitEthernet).
    - Comandos de visualizacion (show), guardado y reinicio.

[02_configuracion_inicial_y_seguridad.md](./02_configuracion_inicial_y_seguridad.md)
    - Asignacion de Hostname y Banner legal.
    - Configuracion de reloj, zona horaria y sincronizacion NTP.
    - Creacion de cuentas locales con privilegios y seguridad SSH / Web GUI.

[03_gestion_ip_y_vlans_basicas.md](./03_gestion_ip_y_vlans_basicas.md)
    - Creacion y nombrado de VLANs 802.1Q.
    - Modos de puerto: Access, Trunk y General (hibrido).
    - Asignacion de PVID y tagged/untagged.
    - Configuracion de interfaz de gestion SVI (interface vlan).

[04_enrutamiento_intervlan_y_servidor_dhcp.md](./04_enrutamiento_intervlan_y_servidor_dhcp.md)
    - Habilitacion de enrutamiento IPv4 en modelos L2+/L3.
    - Configuracion de SVIs como Gateways de VLAN.
    - Servidor DHCP local y Agente de Retransmision (DHCP Relay).
    - Rutas estaticas y ruta por defecto (Default Route).

[05_redundancia_y_agregacion_lag_lacp_stp.md](./05_redundancia_y_agregacion_lag_lacp_stp.md)
    - Agregacion de enlaces (Port-Channel / LAG) estatico y dinamico LACP.
    - Configuracion de Spanning Tree (STP / RSTP / MSTP).
    - Proteccion de topologia: PortFast, BPDU Guard y Root Guard.

[06_seguridad_de_capa_2_y_puertos.md](./06_seguridad_de_capa_2_y_puertos.md)
    - Port Security (limite de direcciones MAC y acciones de violacion).
    - DHCP Snooping y prevencion de servidores DHCP no autorizados.
    - Dynamic ARP Inspection (DAI) y enlace con base de datos de DHCP Snooping.
    - Storm Control (control de tormentas de broadcast y multicast).

[07_enrutamiento_dinamico_ospf.md](./07_enrutamiento_dinamico_ospf.md)
    - OSPFv2 en conmutadores TP-Link Capa 3 (JetStream L3).
    - Router-ID, asignacion de redes por comando network o interfaz, areas y costos.
    - Interfaces pasivas y autenticacion OSPF.

[08_listas_de_control_de_acceso_acl_y_qos.md](./08_listas_de_control_de_acceso_acl_y_qos.md)
    - Creacion de ACLs basadas en MAC (L2) e IP (L3/L4).
    - Aplicacion de ACLs a puertos y VLANs.
    - Calidad de Servicio (QoS 802.1p y DSCP), limitacion de velocidad (Rate-Limit).
    - Port Mirroring (duplicacion de trafico para Wireshark).

[09_alta_disponibilidad_vrrp_y_apilamiento.md](./09_alta_disponibilidad_vrrp_y_apilamiento.md)
    - Protocolo de Redundancia de Enrutador Virtual (VRRP) en switches Core L3.
    - Apilamiento fisico (Stacking) en series JetStream compatibles.
    - Enlaces agregados distribuidos a traves del stack (Multi-Switch LAG).

[10_mantenimiento_respaldo_y_resolucion_fallas.md](./10_mantenimiento_respaldo_y_resolucion_fallas.md)
    - Respaldo y restauracion de configuraciones mediante TFTP.
    - Actualizacion de firmware en memoria flash.
    - Diagnostico de cable de cobre (Virtual Cable Test - VCT).
    - Transceptores SFP (DDM), logs de sistema y comandos de prueba.


## TABLA RAPIDA DE EQUIVALENCIAS: TP-LINK JETSTREAM vs OTROS FABRICANTES


| Accion | TP-Link JetStream | Cisco IOS | Huawei VRP |
| :--- | :--- | :--- | :--- |
| Modo privilegiado | enable | enable | system-view |
| Modo configuracion global configure | configure terminal system-view |  |  |
| Salir de modo | exit | exit | quit |
| Guardar configuracion | copy running startup | write memory / wr | save |
| Crear VLAN | vlan 10 | vlan 10 | vlan 10 |
| Puerto a VLAN acceso | switchport mode access | switchport mode... port link-type access |  |

```text
                          switchport access vlan 10 switchport acc... port default vlan 10
Puerto Troncal            switchport mode trunk    switchport mode... port link-type trunk
                          switchport trunk allowed... switchport trunk port trunk allow-pass...
Agregacion de puertos     interface port-channel 1 interface port-ch.. interface eth-trunk 1
                          channel-group 1 mode act channel-group 1... mode lacp-static
```


## Ruta estatica             ip route 0.0.0.0 0.0.0.0 ip route 0.0.0.0.. ip route-static 0.0.0.0...

