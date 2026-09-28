# 08. FALLAS DE DHCP SNOOPING, DYNAMIC ARP INSPECTION (DAI) Y TABLAS ARP

> **RESOLUCION DE FALLAS (TROUBLESHOOTING DE SWITCHES)**


---



## 1. DESCRIPCION DEL PROBLEMA Y SINTOMAS

- Inmediatamente despues de que el administrador habilita la seguridad de DHCP Snooping,
  TODAS las computadoras de la empresa pierden su direccion IP y reciben la IP
  automatica de Windows (APIPA 169.254.x.x).
- Los servidores o impresoras con direccion IP estatica fija no pueden comunicarse
  con nadie despues de activar Dynamic ARP Inspection (DAI).
- En el log del switch aparecen alertas de paquetes DHCP o ARP descartados:
  "%DHCP_SNOOPING-5-DHCP_SNOOPING_UNTRUSTED_PORT: DHCP packet received on untrusted port"
  "%SW_DAI-4-DHCP_SNOOPING_DENY: 1 Invalid ARPs (Req) on Gi0/5, vlan 1"



## 2. PRINCIPALES CAUSAS RAIZ


### a) Se olvido configurar el puerto Troncal / Uplink como Confiable (TRUST):

   - Al activar DHCP Snooping, TODOS los puertos del switch se convierten en
     "No Confiables" (Untrusted) por defecto.
   - Cuando el servidor DHCP legitimo responde con un paquete `DHCPOFFER` o `DHCPACK`
     a traves del troncal (puerto 24), el switch cree que se trata de un atacante
     pirata y DESCARTA SILENCIOSAMENTE LA RESPUESTA.
   - Consecuencia: Ningun cliente puede renovar u obtener direccion IP.


### b) El problema de la Opcion 82 de DHCP (Option 82 / GIADDR):

   - Por estandar, muchos conmutadores insertan la "Option 82" (informacion del puerto
     y circuito) en las solicitudes DHCP que van hacia el servidor.
   - Si el router o el siguiente switch de la cadena recibe un paquete con Option 82
     en un puerto que considera no confiable, lo descarta con el mensaje:
     "%DHCP_SNOOPING-5-DHCP_SNOOPING_NONZERO_GIADDR".


### c) Bloqueo de dispositivos con IP estatica fija por DAI:

   - Dynamic ARP Inspection (DAI) valida cada peticion ARP comparandola con la
     tabla aprendida por DHCP Snooping (Binding Database).
   - Como los servidores, camaras e impresoras tienen IP fija configurada a mano,
     NUNCA solicitaron una concesion DHCP y NO estan en la tabla de DHCP Snooping.
   - Consecuencia: DAI asume que son atacantes envenenando la tabla ARP (ARP Spoofing)
     y bloquea todo su tráfico de red.



## 3. COMANDOS DE DIAGNOSTICO POR MARCA

CISCO:
```cisco
  SW# show ip dhcp snooping
  (Verificar si el puerto 24 esta en la lista de 'Trusted')
  SW# show ip dhcp snooping binding
  SW# show ip arp inspection statistics
```

HUAWEI:
```cisco
  SW> display dhcp snooping configuration
  SW> display dhcp snooping user-bind all
  SW> display arp anti-attack configuration
```

HP PROCURVE:
```cisco
  SW# show dhcp-snooping
  SW# show dhcp-snooping stats

ARUBA (AOS-CX):
  SW# show dhcp-snooping
  SW# show dhcp-snooping binding
  SW# show arp-inspection statistics
```

TP-LINK JETSTREAM:
```cisco
  SW# show ip dhcp snooping
  SW# show ip dhcp snooping binding
  SW# show ip arp inspection
```


## 4. SOLUCION PASO A PASO

Paso 1: Marcar SIEMPRE los puertos troncales y puertos del servidor DHCP como TRUST:
  (Cisco)       SW(config-if)# interface GigabitEthernet 0/24
```cisco
                SW(config-if)# ip dhcp snooping trust

  (Huawei)      SW(config-if)# interface GigabitEthernet 0/0/24
                SW(config-if)# dhcp snooping trusted

  (HP ProCurve) SW(config)# dhcp-snooping trust 24

  (Aruba CX)    SW(config-if)# interface 1/1/24
                SW(config-if)# dhcp-snooping trust

  (TP-Link)     SW(config-if)# interface gigabitEthernet 1/0/24
                SW(config-if)# ip dhcp snooping trust

Paso 2: Desactivar insercion de Option 82 si los clientes se quedan sin IP:
  En Cisco:
    SW(config)# no ip dhcp snooping information option
    (O en switch Core: ip dhcp snooping information option allow-untrusted)

  En TP-Link:
    SW(config)# no ip dhcp snooping information option

Paso 3: Crear listas de excepcion (ARP Access-List) para servidores e impresoras con IP fija:
Para que DAI no bloquee equipos con IP estatica:
  En Cisco:
    SW(config)# arp access-list DISPOSITIVOS_ESTATICOS
    SW(config-arp-nacl)# permit ip host 192.168.1.10 mac host 0015.5d01.a2b4
    SW(config-arp-nacl)# permit ip host 192.168.1.20 mac host 0011.2233.4455
    SW(config-arp-nacl)# exit
    SW(config)# ip arp inspection filter DISPOSITIVOS_ESTATICOS vlan 1

  O marcar directamente el puerto del servidor como confiable para DAI:
    SW(config-if)# interface GigabitEthernet 0/10
```


## SW(config-if)# ip arp inspection trust
