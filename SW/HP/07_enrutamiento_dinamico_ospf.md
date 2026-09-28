# GUIA HP PROCURVE / ARUBA - PARTE 7: ENRUTAMIENTO DINAMICO AVANZADO CON OSPF


---



## 1. ¿POR QUE UTILIZAR OSPF EN SWITCHES MULTICAPA HP?

OSPF (Open Shortest Path First) permite que los switches de distribucion y Core
aprendan todas las rutas corporativas de forma dinamica y automatica:
- Si un enlace o switch se corta, OSPF recalcula el camino alternativo en menos de 1 segundo.
- Soporta balanceo de carga (ECMP).
- Escala facilmente a decenas de switches sin configurar rutas estaticas a mano.



## 2. CONFIGURACION DE OSPF EN SWITCH CORE 1

Escenario:
- VLAN 10 (Red Usuarios): 192.168.10.0/24 (IP switch: 192.168.10.1)
- VLAN 100 (Enlace hacia Core 2): 10.0.0.0/30 (IP switch: 10.0.0.1)

Paso 1: Habilitar enrutamiento IP global:
```cisco
SW-HP-Core1(config)# ip routing

Paso 2: Iniciar OSPF y definir el Router-ID (Identificador unico del switch):
SW-HP-Core1(config)# router ospf
SW-HP-Core1(ospf)# router-id 1.1.1.1
SW-HP-Core1(ospf)# area 0
SW-HP-Core1(ospf)# enable
SW-HP-Core1(ospf)# exit

Paso 3: ¡EL METODO UNICO DE HP PARA PUBLICAR REDES EN OSPF!
En Cisco y Huawei se usa el comando "network con wildcard".
En HP ProCurve se asocia la VLAN directamente al proceso OSPF:

-- Publicar la VLAN 100 (Enlace hacia Core 2) en el Area 0:
SW-HP-Core1(config)# vlan 100
SW-HP-Core1(vlan-100)# ip ospf 1 area 0
SW-HP-Core1(vlan-100)# exit

-- Publicar la VLAN 10 (Usuarios) en el Area 0:
SW-HP-Core1(config)# vlan 10
SW-HP-Core1(vlan-10)# ip ospf 1 area 0

Paso 4: SEGURIDAD Y RENDIMIENTO (Passive Interface)
Evitar que el switch envie paquetes "Hello" de OSPF hacia las computadoras de los usuarios:
SW-HP-Core1(vlan-10)# ip ospf passive
SW-HP-Core1(vlan-10)# exit
```


## 3. AUTENTICACION ENCRIPTADA MD5 ENTRE SWITCHES

Para garantizar que solo los switches autorizados de la empresa puedan hablar OSPF:

```cisco
SW-HP-Core1(config)# vlan 100
SW-HP-Core1(vlan-100)# ip ospf md5-auth-key-chain 1
SW-HP-Core1(vlan-100)# exit

(Se debe configurar exactamente la misma clave en la VLAN 100 del switch Core 2).
```


## 4. CONFIGURACION EN SWITCH CORE 2 (VECINO)

```cisco
SW-HP-Core2(config)# ip routing
SW-HP-Core2(config)# router ospf
SW-HP-Core2(ospf)# router-id 2.2.2.2
SW-HP-Core2(ospf)# area 0
SW-HP-Core2(ospf)# enable
SW-HP-Core2(ospf)# exit

SW-HP-Core2(config)# vlan 100
SW-HP-Core2(vlan-100)# ip ospf 1 area 0
SW-HP-Core2(vlan-100)# exit

SW-HP-Core2(config)# vlan 20
SW-HP-Core2(vlan-20)# ip ospf 1 area 0
SW-HP-Core2(vlan-20)# ip ospf passive
SW-HP-Core2(vlan-20)# exit
```


## 5. COMANDOS DE DIAGNOSTICO Y VERIFICACION

- Comprobar que los switches son vecinos OSPF (Estado "FULL"):
```cisco
    SW-HP# show ip ospf neighbor

- Ver estado general del proceso OSPF:
    SW-HP# show ip ospf general-info

- Ver solo las rutas aprendidas dinamicamente mediante OSPF:
    SW-HP# show ip route ospf
```
