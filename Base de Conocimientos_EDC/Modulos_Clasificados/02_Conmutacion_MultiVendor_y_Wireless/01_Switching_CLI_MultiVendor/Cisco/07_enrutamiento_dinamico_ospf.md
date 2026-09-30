# GUIA CISCO IOS - PARTE 7: ENRUTAMIENTO DINAMICO AVANZADO CON OSPF


---



## 1. ¿POR QUE UTILIZAR OSPF EN SWITCHES MULTICAPA CISCO?

OSPF (Open Shortest Path First) permite que switches Core y de Distribucion aprendan
todas las redes de la empresa de forma automatica y dinamica:
- Si un switch o cable se desconecta, OSPF encuentra un camino alternativo en menos
  de un segundo.
- Soporta balanceo de carga de igual costo (ECMP).
- Escala a cientos de switches y routers sin necesidad de crear rutas estaticas a mano.



## 2. CONFIGURACION COMPLETA DE OSPF EN SWITCH CORE 1

Escenario:
- Red de Usuarios (VLAN 10): 192.168.10.0/24
- Enlace enrutado hacia Core 2 (G0/24): 10.0.0.0/30 (IP local: 10.0.0.1)

Paso 1: Habilitar enrutamiento global (¡Obligatorio en switches Cisco!)
Switch-Core1(config)# ip routing

Paso 2: Iniciar el proceso OSPF y fijar el Router-ID (Identificador unico del equipo)
Switch-Core1(config)# router ospf 1
Switch-Core1(config-router)# router-id 1.1.1.1

Paso 3: Publicar las redes con MASCARA WILDCARD (Inversa a la mascara de subred)
* Mascara 255.255.255.0   -> Wildcard: 0.0.0.255
* Mascara 255.255.255.252 -> Wildcard: 0.0.0.3

-- Publicar el enlace hacia Core 2 en el Area 0:
Switch-Core1(config-router)# network 10.0.0.0 0.0.0.3 area 0

-- Publicar la red de usuarios de ventas en el Area 0:
Switch-Core1(config-router)# network 192.168.10.0 0.0.0.255 area 0

Paso 4: SEGURIDAD Y RENDIMIENTO (Passive-Interface)
No queremos enviar paquetes "Hello" de OSPF hacia las computadoras de los usuarios
(evita saturacion inutil y que alguien monte un router falso para espiar rutas):
Switch-Core1(config-router)# passive-interface vlan 10

Paso 5: AJUSTE DE ANCHO DE BANDA DE REFERENCIA (MODERNO)
Por defecto, Cisco calcula el costo considerando 100 Mbps como maximo. En switches
Gigabit y 10G se debe ajustar la referencia:
Switch-Core1(config-router)# auto-cost reference-bandwidth 10000
Switch-Core1(config-router)# exit



## 3. AUTENTICACION SEGURA MD5 ENTRE SWITCHES

Para garantizar que solo los switches autorizados de la empresa puedan hablar OSPF:

Switch-Core1(config)# interface GigabitEthernet 0/24
Switch-Core1(config-if)# ip ospf authentication message-digest
Switch-Core1(config-if)# ip ospf message-digest-key 1 md5 ClaveOspfCisco2026!
Switch-Core1(config-if)# exit

(Se debe colocar exactamente la misma clave en el puerto del otro switch vecino).



## 4. CONFIGURACION RAPIDA EN SWITCH CORE 2 (VECINO)

Switch-Core2(config)# ip routing
Switch-Core2(config)# router ospf 1
Switch-Core2(config-router)# router-id 2.2.2.2
Switch-Core2(config-router)# network 10.0.0.0 0.0.0.3 area 0
Switch-Core2(config-router)# network 192.168.20.0 0.0.0.255 area 0
Switch-Core2(config-router)# passive-interface vlan 20
Switch-Core2(config-router)# exit
Switch-Core2(config)# interface GigabitEthernet 0/24
Switch-Core2(config-if)# ip ospf authentication message-digest
Switch-Core2(config-if)# ip ospf message-digest-key 1 md5 ClaveOspfCisco2026!
Switch-Core2(config-if)# exit



## 5. COMANDOS DE DIAGNOSTICO Y VERIFICACION

- Comprobar que los switches son vecinos OSPF (El estado DEBE ser "FULL"):
    Switch-Core1# show ip ospf neighbor

- Ver solo las rutas aprendidas por OSPF en la tabla de enrutamiento:
    Switch-Core1# show ip route ospf

- Ver estado de las interfaces participando en OSPF:
    Switch-Core1# show ip ospf interface brief