# GUIA CISCO IOS - PARTE 6: SEGURIDAD DE CAPA 2 (PORT SECURITY, DHCP SNOOPING, DAI Y STORM CONTROL)


---



## 1. SEGURIDAD DE PUERTOS (PORT SECURITY)

¿Que problema resuelve?
Impide que usuarios desconecten su equipo asignado para conectar laptops personales,
switches clandestinos o realizar ataques de suplantacion de MAC (MAC Flooding).

Configuracion en un puerto de usuario:
```cisco
Switch(config)# interface GigabitEthernet 0/1
Switch(config-if)# switchport mode access
Switch(config-if)# switchport port-security
Switch(config-if)# switchport port-security maximum 1
Switch(config-if)# switchport port-security mac-address sticky
  -> "sticky": El switch aprende la MAC de la computadora conectada y la guarda
     automaticamente en el running-config.

Switch(config-if)# switchport port-security violation shutdown
  -> Modos de violacion:
     * shutdown: (Recomendado) Apaga el puerto inmediatamente (estado err-disable).
     * restrict: Descarta paquetes no autorizados, genera log y envia alertas SNMP.
     * protect:  Descarta paquetes silenciosamente.
Switch(config-if)# exit

-- RECUPERACION AUTOMATICA DE PUERTOS APAGADOS (ERRDISABLE RECOVERY)
Para que un puerto apagado por violacion de seguridad intente reactivarse solo
despues de 5 minutos (300 seg) sin requerir intervencion manual del admin:
Switch(config)# errdisable recovery cause psecure-violation
Switch(config)# errdisable recovery interval 300
```


## 2. DHCP SNOOPING (PROTECCION CONTRA SERVIDORES DHCP FALSOS)

¿Que problema resuelve?
Si alguien conecta un router WiFi casero en su cubículo, este empezara a entregar
direcciones IP y gateways falsos a otros usuarios, interrumpiendo la navegacion.

Paso 1: Habilitar DHCP Snooping globalmente y en las VLANs deseadas:
```cisco
Switch(config)# ip dhcp snooping
Switch(config)# ip dhcp snooping vlan 10,20,30

Paso 2: ¡TRUCO CISCO FUNDAMENTAL!
Por defecto, Cisco inserta la "Opcion 82" en las peticiones DHCP. Si tu servidor
DHCP no es Cisco, descartara las solicitudes. Desactiva esta insercion si tienes problemas:
Switch(config)# no ip dhcp snooping information option

Paso 3: Marcar el puerto de enlace (Uplink hacia el Router/DHCP real) como CONFIABLE:
Switch(config)# interface GigabitEthernet 0/24
Switch(config-if)# ip dhcp snooping trust
Switch(config-if)# exit
  -> Todos los demas puertos seran "Untrusted" (bloquearan respuestas DHCP ofrecidas por usuarios).
```


## 3. DYNAMIC ARP INSPECTION (DAI - MITIGACION DE ARP POISONING / MAN-IN-THE-MIDDLE)

¿Que problema resuelve?
Evita que un atacante envie paquetes ARP falsos para desviar el trafico de la red
hacia su computadora para espiar contrasenas (Ataques Man-in-the-Middle).
Requiere que DHCP Snooping este habilitado.

Paso 1: Activar DAI en las VLANs:
```cisco
Switch(config)# ip arp inspection vlan 10,20

Paso 2: Marcar los enlaces troncales y uplinks como confiables:
Switch(config)# interface GigabitEthernet 0/24
Switch(config-if)# ip arp inspection trust
Switch(config-if)# exit
```


## 4. CONTROL DE TORMENTAS (STORM CONTROL)

Si una tarjeta de red danada o software malicioso inunda la red con broadcast:

```cisco
Switch(config)# interface range GigabitEthernet 0/1 - 20
Switch(config-if-range)# storm-control broadcast level 5.0
  -> Si el broadcast supera el 5% de la capacidad del puerto, descarta el exceso.
Switch(config-if-range)# storm-control multicast level 10.0
Switch(config-if-range)# storm-control action trap
  -> Envia una alarma de monitoreo cuando se activa el bloqueo.
Switch(config-if-range)# exit
```


## 5. DESACTIVAR PROTOCOLOS DE DESCUBRIMIENTO EN PUERTOS PUBLICOS (CDP)

CDP (Cisco Discovery Protocol) revela el modelo exacto, version de IOS y nombre
del switch a cualquiera conectado a la pared:
```cisco
Switch(config)# interface range GigabitEthernet 0/1 - 20
Switch(config-if-range)# no cdp enable
Switch(config-if-range)# exit
```


## 6. VERIFICACION

- Ver estado de seguridad de puertos y puertos en err-disabled:
```cisco
    Switch# show port-security
    Switch# show port-security interface GigabitEthernet 0/1

- Ver tabla de enlaces de DHCP Snooping (IP asignada a cada MAC y puerto):
    Switch# show ip dhcp snooping binding

- Ver puertos bloqueados por caida de seguridad:
    Switch# show interfaces status err-disabled
```
