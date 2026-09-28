# 00. INDICE MAESTRO, METODOLOGIA DE DIAGNOSTICO Y PROTOCOLO DE TRIAGE

> **BASE DE CONOCIMIENTOS DE RESOLUCION DE FALLAS (TROUBLESHOOTING DE SWITCHES)**


---



## 1. OBJETIVO DE ESTA GUIA

Esta base de conocimientos recopila los errores, fallas y comportamientos anomalos
mas frecuentes que experimentan los ingenieros y administradores de red al
configurar y operar conmutadores (switches) de multiples marcas:
- Cisco (IOS / IOS-XE)
- Huawei (VRP)
- 3Com / H3C (Comware)
- HP (ProCurve / Provision / AOS-S)
- Aruba (ArubaOS-CX)
- TP-Link (JetStream L2/L3)

Cada documento ofrece la explicacion tecnica de la falla, sintomas visibles,
comandos de diagnostico (show / display), pasos exactos de solucion y las
mejores practicas de la industria para evitar su reaparicion.



## 2. INDICE DE ARCHIVOS DE LA CARPETA TROUBLESHOOTING

[00_INDICE_Y_METODOLOGIA_DE_DIAGNOSTICO.md](./00_INDICE_Y_METODOLOGIA_DE_DIAGNOSTICO.md)
    - Metodologia de resolucion segun modelo OSI, triage de incidentes y
      protocolo de aislamiento de problemas de red.

[01_fallas_puertos_bloqueados_errdisable_y_seguridad.md](./01_fallas_puertos_bloqueados_errdisable_y_seguridad.md)
    - Puertos en estado 'err-disabled' / 'shutdown' por violacion de Port Security,
      BPDU Guard o Storm Control. Diagnostico, reactivacion y autorrecuperacion.

[02_fallas_vlans_troncales_y_vlan_nativa.md](./02_fallas_vlans_troncales_y_vlan_nativa.md)
    - Discrepancia de VLAN Nativa (Native VLAN Mismatch), VLANs omitidas en troncal,
      puertos en modo Access en vez de Trunk y aislamiento de tráfico.

[03_fallas_spanning_tree_bucles_y_tormentas.md](./03_fallas_spanning_tree_bucles_y_tormentas.md)
    - Bucles de Capa 2 (Broadcast Storms), CPU al 100%, parpadeo masivo de LEDs,
      seleccion erronea del Root Bridge y aleteo de direcciones MAC (MAC Flapping).

[04_fallas_enlace_agregado_lag_lacp_port_channel.md](./04_fallas_enlace_agregado_lag_lacp_port_channel.md)
    - Caida de enlaces agregados (Port-Channel / LACP / Eth-Trunk), desajuste de
      velocidad/duplex entre miembros, puertos suspendidos o no agrupados.

[05_fallas_enrutamiento_intervlan_svi_y_gateway.md](./05_fallas_enrutamiento_intervlan_svi_y_gateway.md)
    - SVIs en estado 'Down/Down' por falta de puertos activos (Autostate), olvido
      del comando 'ip routing', mascaras de subred incorrectas y DHCP Relay caido.

[06_fallas_capa_1_fisica_sfp_fibra_y_cable_utp.md](./06_fallas_capa_1_fisica_sfp_fibra_y_cable_utp.md)
    - Errores de colision tardia (Late Collisions), tramas CRC/Runt, polaridad
      invertida en fibra optica (Tx a Tx), diagnostico optico DDM/DOM y cables UTP (TDR).

[07_fallas_acceso_remoto_ssh_telnet_y_autenticacion.md](./07_fallas_acceso_remoto_ssh_telnet_y_autenticacion.md)
    - Bloqueo de sesiones SSH ("Connection refused"), falta de llaves RSA criptograficas,
      bloqueo involuntario por ACL de gestion y procedimientos de recuperacion de contrasena.

[08_fallas_dhcp_snooping_dai_y_arp.md](./08_fallas_dhcp_snooping_dai_y_arp.md)
    - Clientes sin IP tras habilitar DHCP Snooping (falta del comando 'trust' en troncal),
      descarte de paquetes por Option 82 e interferencia de Dynamic ARP Inspection (DAI).

[09_guia_errores_frecuentes_y_gotchas_por_marca.md](./09_guia_errores_frecuentes_y_gotchas_por_marca.md)
    - "Trampas" sintacticas y peculiaridades unicas de cada fabricante (Cisco, Huawei,
      3Com, HP, Aruba y TP-Link) que causan frustracion en el despliegue.



## 3. METODOLOGIA CIENTIFICA DE RESOLUCION DE PROBLEMAS (TROUBLESHOOTING)

Nunca intente resolver una falla cambiando configuraciones a ciegas ("trial and error").
Siga el enfoque estructurado basado en el modelo OSI:


### a) Enfoque de Abajo hacia Arriba (Bottom-Up - Recomendado para problemas fisicos):

   1. Capa 1 (Fisica): ¿El LED de enlace esta encendido? ¿El cable esta bien conectado?
      ¿La fibra tiene potencia de recepcion adecuada (dBm)?
   2. Capa 2 (Enlace): ¿El puerto negocia duplex y velocidad? ¿Esta en la VLAN correcta?
      ¿El puerto fue bloqueado por STP, Port Security o BPDU Guard?
   3. Capa 3 (Red): ¿El SVI tiene IP y mascara correcta? ¿Hay respuesta de Ping al Gateway?
      ¿Existe una ruta por defecto configurada?
   4. Capa 4 a 7 (Transporte / Aplicacion): ¿El firewall o la ACL bloquea el puerto TCP/UDP?
      ¿El servicio SSH, DNS o DHCP esta activo y respondiendo?


### b) Enfoque de Arriba hacia Abajo (Top-Down - Recomendado cuando el hardware esta bien):

   - Probar conexion por aplicacion (SSH / Ping) y descender hacia el origen de la falla.


### c) Enfoque "Divide y Venceras" (Divide-and-Conquer):

   - Hacer un Ping desde el centro de la topologia para aislar si el problema esta hacia
     el cliente o hacia el nucleo / servidor.



## 4. PROTOCOLO DE TRIAGE INMEDIATO ANTE UNA CRISIS

Cuando la red se caiga o haya lentitud extrema:
1. NO REINICIE EL SWITCH DE INMEDIATO: El reinicio borra los logs de memoria volatil,
   las tablas MAC dinámicas y la evidencia forense de la causa raíz.
2. RECOPILE INFORMACION:
   - Verifique el consumo de CPU y memoria (`show processes cpu` / `display cpu-usage`).
   - Verifique si hay puertos aleteando (`show log` / `display logbuffer`).
   - Verifique si el Spanning Tree esta cambiando constantemente (`show spanning-tree detail`).

## 3. ASISLE LA ZONA AFECTADA antes de aplicar cambios globales.
