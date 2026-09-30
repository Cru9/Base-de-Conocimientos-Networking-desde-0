# 05. FALLAS DE ENRUTAMIENTO INTER-VLAN, INTERFACES SVI Y GATEWAYS

> **RESOLUCION DE FALLAS (TROUBLESHOOTING DE SWITCHES)**


---



## 1. DESCRIPCION DEL PROBLEMA Y SINTOMAS

- Se creo la interfaz de VLAN (SVI) y se le asigno IP, pero aparece en estado:
  `Vlan10 is up, line protocol is down` o `Down/Down`.
- Los usuarios de la VLAN 10 no pueden hacer Ping a su propia puerta de enlace (Gateway).
- Los usuarios de la VLAN 10 hacen Ping a su Gateway, pero NO pueden comunicarse
  con la VLAN 20 (falla total de enrutamiento inter-VLAN).
- El switch no puede ser administrado remotamente desde otra sucursal o no alcanza
  el servidor Syslog `11.39.41.200`.



## 2. PRINCIPALES CAUSAS RAIZ


### a) La regla del Autostate en interfaces SVI (Causa #1 de SVI en Down):

   - Una interfaz virtual de VLAN (SVI) SOLO levantara a estado `Up/Up` si existe
     al menos UN puerto fisico (o troncal) que pertenezca a esa VLAN, este con
     cable conectado (`Up`) y en estado STP `Forwarding`.
   - Si no hay ningun equipo encendido en los puertos de la VLAN 10, la interfaz
     `Vlan10` se mantendra en `Line protocol down` por diseño para ahorrar recursos.


### b) El comando 'ip routing' esta ausente (Causa clasica en conmutadores L3):

   - En muchos switches multicapa (Cisco Catalyst 3560/3750/3850/9300, TP-Link
     JetStream, etc.), el motor de enrutamiento IPv4 viene APAGADO de fabrica.
   - Consecuencia: El switch opera como un simple conmutador Capa 2; cada VLAN
     esta aislada y el switch descarta cualquier paquete destinado a otra VLAN.


### c) Ausencia de Ruta por Defecto (Default Route) en el Switch L3:

   - Las VLANs locales se comunican entre si, pero nadie tiene salida a Internet
     o a otras sedes porque el switch no sabe a que firewall reenviar el trafico.


### d) Error en Switches Capa 2: Falta de 'ip default-gateway':

   - En switches puramente L2, si no se configura `ip default-gateway`, el switch
     solo responde a Pings o conexiones SSH provenientes de su misma subred local.


### e) Agente DHCP Relay (ip helper-address) ausente o mal direccionado:

   - Los clientes no reciben direccion IP automatica porque las solicitudes DHCP
     (broadcasts) no pueden cruzar el limite de Capa 3 del router/SVI sin un relay.



## 3. COMANDOS DE DIAGNOSTICO POR MARCA

CISCO:
```cisco
  SW# show ip interface brief
  (Verificar columnas 'Status' y 'Protocol' de las interfaces Vlan)
  SW# show ip route
  (Si la tabla esta vacia o no muestra rutas conectadas, falta 'ip routing')
  SW# show ip interface Vlan10 | include Helper
```

HUAWEI:
```cisco
  SW> display ip interface brief
  SW> display ip routing-table
```

3COM / H3C:
```cisco
  SW> display ip interface brief
  SW> display ip routing-table
```

HP PROCURVE:
```cisco
  SW# show ip
  SW# show ip route

ARUBA (AOS-CX):
  SW# show ip interface brief
  SW# show ip route
```

TP-LINK JETSTREAM:
```cisco
  SW# show ip interface
  SW# show ip route
```


## 4. SOLUCION PASO A PASO

Caso 1: Habilitar el motor de enrutamiento global en el switch L3
  En Cisco:
```cisco
    SW(config)# ip routing

  En TP-Link JetStream:
    SW(config)# ip routing

  En Huawei / 3Com / Aruba CX:
    El enrutamiento L3 esta activo por defecto en modelos de nucleo/distribucion.

Caso 2: Levantar una interfaz SVI caida por Autostate
Asegurese de que al menos un puerto este conectado y asignado a esa VLAN:
  SW(config)# interface GigabitEthernet 0/5
  SW(config-if)# switchport mode access
  SW(config-if)# switchport access vlan 10
  SW(config-if)# no shutdown
(Conecte una PC o servidor encendido; la interfaz SVI pasara de inmediato a Up/Up).

Caso 3: Configurar la ruta por defecto (Hacia el Firewall o Router de Internet)
En Switches de Capa 3:
  (Cisco)       SW(config)# ip route 0.0.0.0 0.0.0.0 10.100.1.1
  (Huawei)      SW(config)# ip route-static 0.0.0.0 0.0.0.0 10.100.1.1
  (HP/Aruba)    SW(config)# ip route 0.0.0.0/0 10.100.1.1
  (TP-Link)     SW(config)# ip route 0.0.0.0 0.0.0.0 10.100.1.1

En Switches de Capa 2 (Solo para que el switch responda a gestion remota):
  (Cisco/TP-Link) SW(config)# ip default-gateway 192.168.1.254
  (HP ProCurve)   SW(config)# ip default-gateway 192.168.1.254

Caso 4: Configurar DHCP Relay para que las PCs reciban IP de un servidor externo
  (Cisco)       SW(config-if)# interface vlan 10
                SW(config-if)# ip helper-address 192.168.1.100

  (Huawei)      SW(config-if)# interface Vlanif 10
                SW(config-if)# dhcp select relay
                SW(config-if)# dhcp relay server-ip 192.168.1.100

  (Aruba CX)    SW(config-if)# interface vlan 10
                SW(config-if)# ip helper-address 192.168.1.100

  (TP-Link)     SW(config)# service dhcp-relay
                SW(config-if)# interface vlan 10
```


## SW(config-if)# ip dhcp-relay server-address 192.168.1.100
