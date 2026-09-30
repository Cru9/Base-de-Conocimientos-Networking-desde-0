# 02. FALLAS DE VLANS, PUERTOS TRONCALES Y DISCREPANCIA DE VLAN NATIVA

> **RESOLUCION DE FALLAS (TROUBLESHOOTING DE SWITCHES)**


---



## 1. DESCRIPCION DEL PROBLEMA Y SINTOMAS

- Los equipos en una VLAN especifica (ej. VLAN 10) no se comunican con el servidor
  o gateway ubicado en otro switch, pero los de la VLAN 1 si tienen conexion.
- En la consola aparecen mensajes de error continuos como:
  "%CDP-4-NATIVE_VLAN_MISMATCH: Native VLAN mismatch discovered on GigabitEthernet0/24 (10), with SwitchB GigabitEthernet0/24 (1)"
  "%SPANTREE-2-INCONSISTENT_PORT: Inconsistent port type on GigabitEthernet0/24"
- Fuga de paquetes entre VLANs distintas (VLAN Leaking / Tráfico cruzado).



## 2. PRINCIPALES CAUSAS RAIZ


### a) Discrepancia de VLAN Nativa (Native VLAN Mismatch):

   - El Switch A tiene configurada la VLAN Nativa 1 en el troncal (las tramas de
     la VLAN 1 viajan sin etiquetar / untagged).
   - El Switch B tiene la VLAN Nativa 99 en el mismo troncal.
   - Consecuencia: El Switch B recibe tramas de la VLAN 1 y se las entrega
     equivocadamente a los usuarios de la VLAN 99. Spanning Tree detecta esta
     inconsistencia y bloquea el enlace para prevenir bucles.


### b) El clasico error al agregar VLANs a un troncal (Sobrescritura accidental):

   - El troncal tenia permitido: `10,20,30`.
   - El administrador quiso agregar la VLAN 40 y ejecuto en Cisco/TP-Link:
     `switchport trunk allowed vlan 40`  (¡SIN la palabra 'add'!).
   - Consecuencia Catastrofica: Se borraron las VLANs 10, 20 y 30 del enlace,
     dejando desconectada a toda la empresa y dejando unicamente la VLAN 40.


### c) Un extremo configurado como Troncal y el otro como Acceso:

   - Switch A tiene el puerto en modo Trunk, pero en Switch B olvidaron configurarlo
     y se quedo en modo Access (VLAN 1).


### d) La VLAN no existe en la base de datos global del switch:

   - Se asigno un puerto a la VLAN 50 (`switchport access vlan 50`), pero nunca se
     creo la VLAN de forma global (`vlan 50`). En varios conmutadores, el puerto
     permanece inactivo o no reenvia tráfico.



## 3. COMANDOS DE DIAGNOSTICO POR MARCA

CISCO:
```cisco
  SW# show interfaces trunk
  (Verificar columnas 'Native vlan', 'Vlans allowed on trunk' y 'Vlans in spanning tree forwarding')
  SW# show interfaces GigabitEthernet 0/24 switchport
  SW# show vlan brief
```

HUAWEI:
```cisco
  SW> display port vlan GigabitEthernet 0/0/24
  SW> display port link-type
  SW> display vlan
```

3COM / H3C:
```cisco
  SW> display port link-type
  SW> display vlan all
```

HP PROCURVE:
```cisco
  SW# show vlans
  SW# show vlans ports 24 detail
  (Verificar si el puerto 24 esta como 'Tagged' o 'Untagged' en cada VLAN)

ARUBA (AOS-CX):
  SW# show vlan port 1/1/24
  SW# show vlan
```

TP-LINK JETSTREAM:
```cisco
  SW# show interface switchport gigabitEthernet 1/0/24
  SW# show vlan
```


## 4. SOLUCION PASO A PASO

Caso 1: Corregir discrepancia de VLAN Nativa
Asegurese de que AMBOS conmutadores tengan exactamente el mismo valor de nativa:
En Switch A y Switch B:
  (Cisco)       SW(config-if)# switchport trunk native vlan 99
  (Huawei)      SW(config-if)# port trunk pvid vlan 99
  (HP ProCurve) SW(config)# vlan 99 untagged 24
  (Aruba CX)    SW(config-if)# vlan trunk native 99
  (TP-Link)     SW(config-if)# switchport trunk native vlan 99

Caso 2: Agregar una VLAN a un troncal existente de forma segura
SIEMPRE use la palabra reservada 'add' (o similar) para no sobrescribir:
  (Cisco)       SW(config-if)# switchport trunk allowed vlan add 40
  (Huawei)      SW(config-if)# port trunk allow-pass vlan 40
  (HP ProCurve) SW(config)# vlan 40 tagged 24
  (Aruba CX)    SW(config-if)# vlan trunk allowed 10,20,30,40
  (TP-Link)     SW(config-if)# switchport trunk allowed vlan 10,20,30,40

Caso 3: Verificar que la VLAN este creada globalmente y activa
  (Cisco/TP-Link) SW(config)# vlan 50
```cisco
                  SW(config-vlan)# name Contabilidad
                  SW(config-vlan)# no shutdown

  (Huawei/3Com)   SW(config)# vlan 50
                  SW(config-vlan)# description Contabilidad

  (HP/Aruba)      SW(config)# vlan 50
                  SW(config-vlan)# name Contabilidad
                  SW(config-vlan)# no shutdown
```


## 5. MEJORES PRACTICAS PARA ENLACES TRONCALES

1. Nunca use la VLAN 1 como nativa en enlaces troncales hacia otros edificios
   o routers; etiquetela o use una VLAN sin IP para evitar ataques de VLAN Hopping.
2. Defina explicitamente la lista de VLANs autorizadas en cada troncal en lugar
   de `allowed all` para evitar desperdicio de difusion de broadcast no requerido.
3. Utilice protocolos de descubrimiento de vecinos (LLDP o CDP) para verificar

que el puerto remoto conectado realmente es el puerto troncal del switch par.
