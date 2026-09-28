# 03. DMVPN (DYNAMIC MULTIPOINT VPN) - ARQUITECTURA mGRE, NHRP Y FASES 1, 2 Y 3

> **FIREWALLS DE PROXIMA GENERACION (NGFW) Y VPNs EMPRESARIALES**


---



## 1. EL PROBLEMA DE ESCALABILIDAD DE LAS VPNs TRADICIONALES

Imagine una cadena de farmacias o bancos con 800 sucursales (Spokes) y un Corporativo (Hub):
- Con VPNs IPsec tradicionales punto a punto, el router del Hub requeriria
  800 interfaces de tunel independientes (`interface Tunnel 1` a `Tunnel 800`) y
  miles de lineas de configuracion criptografica.
- Cada vez que se abriera una sucursal nueva, un ingeniero tendria que entrar al
  Hub central a modificar la configuracion.
- Si la Sucursal A queria enviar un archivo a la Sucursal B, el trafico tenia que
  viajar obligatoriamente por el Hub, duplicando la latencia y consumiendo ancho de banda central.

La Solucion Revolucionaria de Cisco: DMVPN (Dynamic Multipoint VPN)
- El router Hub utiliza UNA SOLA interfaz de tunel (`interface Tunnel 0`) para
  atender dinamicamente a las 800 sucursales.
- Despliegue Zero-Touch en el Hub: Se pueden agregar 200 sucursales nuevas y NO
  se toca una sola linea en el router central.
- Comunicacion Directa Spoke-to-Spoke: Las sucursales crean tuneles cifrados
  directos y temporales entre si sin pasar por el Hub.



## 2. LOS 4 PILARES TECNOLOGICOS DE DMVPN


| Tecnologia | Rol en DMVPN |
| :--- | :--- |
| mGRE | Multipoint Generic Routing Encapsulation: A diferencia de GRE normal |
| (Multipoint GRE) | (que exige definir `tunnel destination <IP>`), mGRE no define un |
| destino fijo; permite que una sola interfaz conecte con multiples destinos. |  |


NHRP               Next Hop Resolution Protocol (RFC 2332): El "servidor ARP de la WAN".
                   Mantiene una base de datos que mapea la IP privada del tunel de cada
                   sucursal con su IP publica real de Internet (Next Hop Server - NHS).

IPsec Profile      Aplica cifrado AES-256 a los paquetes mGRE de forma automatica y
                   dinamica a medida que las sucursales se conectan.

Protocolo de       Distribuye las rutas de la empresa por encima del tunel multipunto.
Enrutamiento       (EIGRP o BGP son los mas recomendados; OSPF requiere ajustes de red).



## 3. LAS TRES FASES DE EVOLUCION DE DMVPN

FASE 1: HUB-AND-SPOKE PURO
- Los Spokes usan tuneles GRE punto a punto estandar dirigidos al Hub.
- Solo el Hub utiliza mGRE.
- Todo el trafico entre sucursales DEBE pasar obligatoriamente a traves del Hub.
- No hay tuneles directos entre sucursales.

FASE 2: SPOKE-TO-SPOKE DINAMICO
- Tanto el Hub como todos los Spokes utilizan interfaces mGRE.
- Cuando la Sucursal A quiere enviar trafico a la Sucursal B:
  1. Sucursal A le pregunta al Hub via NHRP: "¿Cual es la IP publica de la Sucursal B?".
  2. El Hub responde con la IP publica de B.
  3. Sucursal A y Sucursal B levantan un tunel IPsec directo "on-demand" entre ellas.
  4. El trafico fluye directo sin saturar el Hub.
  5. Al terminar la transferencia, el tunel dinamico se destruye para ahorrar memoria.

FASE 3: REDIRECCION Y ATAJOS NHRP (EL ESTANDAR EMPRESARIAL MODERNO)
- Resuelve las limitaciones de sumarizacion de rutas de la Fase 2.
- Utiliza dos primitivas avanzadas:
  * `ip nhrp redirect`: El Hub recibe el primer paquete entre sucursales y le dice
    al Spoke A: "No me mandes esto a mi; existe una mejor ruta directa hacia B".
  * `ip nhrp shortcut`: El Spoke A instala dinamicamente la ruta de atajo en su tabla CEF
    y enruta directamente hacia el Spoke B.
- Permite construir arquitecturas jerarquicas con cientos de miles de sucursales.



## 4. LABORATORIO PRACTICO: CONFIGURACION DE DMVPN FASE 3 (CISCO)


#### 💻 CONFIGURACION DEL ROUTER CENTRAL (HUB):

```text
  crypto ikev2 profile IKEV2_DMVPN
   match identity remote any
   authentication remote pre-share key ClaveDmvpnSecreta2026!
   authentication local pre-share key ClaveDmvpnSecreta2026!
  !
  crypto ipsec profile IPSEC_DMVPN
   set ikev2-profile IKEV2_DMVPN
  !
  interface Tunnel 0
   description DMVPN_HUB_CENTRAL
   ip address 172.16.1.1 255.255.255.0
   no ip redirects
   ip nhrp network-id 1
   ip nhrp redirect                  ! (Habilita DMVPN Fase 3)
   tunnel source GigabitEthernet 0/0/0 (Interfaz publica con IP 203.0.113.1)
   tunnel mode gre multipoint
   tunnel protection ipsec profile IPSEC_DMVPN
   no shutdown
```


#### 💻 CONFIGURACION DE LA SUCURSAL REMOTA (SPOKE 1):

```text
  interface Tunnel 0
   description DMVPN_SPOKE_SUCURSAL_1
   ip address 172.16.1.10 255.255.255.0
   ip nhrp network-id 1
   ip nhrp shortcut                  ! (Acepta atajos directos en Fase 3)
   ip nhrp nhs 172.16.1.1 nbma 203.0.113.1 multicast  ! (Registra con el Hub NHS)
   tunnel source GigabitEthernet 0/0/0
   tunnel mode gre multipoint
   tunnel protection ipsec profile IPSEC_DMVPN
   no shutdown
```

COMANDOS DE DIAGNOSTICO:
```cisco
  SW-HUB# show ip nhrp
  (Muestra el mapeo dinamico entre la IP del tunel y la IP publica de cada sucursal)
  SW-HUB# show dmvpn
```


## (Muestra el estado de las sesiones activas, sockets de cifrado y uptime)
