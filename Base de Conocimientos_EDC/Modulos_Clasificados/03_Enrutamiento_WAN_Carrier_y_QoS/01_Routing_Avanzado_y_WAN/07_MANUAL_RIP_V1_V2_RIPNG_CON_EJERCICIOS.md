# 07. MANUAL COMPLETO DE RIP (v1, v2 Y RIPng) - TEORIA, MECANISMOS Y LABORATORIO

> **ENRUTAMIENTO AVANZADO Y TECNOLOGIAS WAN (ROUTING & WAN ARCHITECTURE)**


---



## 1. ¿QUE ES RIP Y COMO FUNCIONA EL ALGORITMO BELLMAN-FORD?

RIP (Routing Information Protocol) es uno de los primeros protocolos de enrutamiento
dinamico de la historia de Internet, estandarizado originalmente en 1988 (RFC 1058).

Pertenece a la familia de VECTOR DISTANCIA (Distance Vector):
- "Vector": Indica la direccion (el proximo router o interfaz de salida).
- "Distancia": Indica que tan lejos esta el destino (medido exclusivamente en saltos).

El Principio de "Enrutamiento por Rumor" (Routing by Rumor):
A diferencia de los protocolos de estado de enlace (como OSPF) que conocen el mapa
completo y exacto de toda la red, un router RIP solo conoce lo que sus vecinos directos
le "cuentan". Si el vecino R2 le dice a R1: "Puedo llegar a la red 10.0.0.0 en 2 saltos",
R1 le cree ciegamente, suma 1 salto y anuncia a sus propios vecinos que el puede llegar en 3.

Metrica de RIP: Conteo de Saltos (Hop Count)
- Cada router que un paquete atraviesa cuenta como 1 salto.
- Metrica minima = 1 (red conectada al vecino inmediato).
- Metrica maxima permitida = 15 saltos.
- 16 saltos = INFINITO / INALCANZABLE (Metrica de envenenamiento).
- Consecuencia critica: RIP NO puede utilizarse en redes que tengan mas de 15 routers en serie.



## 2. COMPARATIVA TECNICA: RIPv1 vs RIPv2 vs RIPng


| Caracteristica | RIPv1 (RFC 1058) | RIPv2 (RFC 2453) | RIPng (RFC 2080) |
| :--- | :--- | :--- | :--- |
| Protocolo IP soportado | IPv4 | IPv4 | IPv6 |
| Tipo de Enrutamiento | Classful (Con clase) Classless (Sin clase)Classless |  |  |
| Soporte de VLSM / CIDR | NO | SI | SI |
| Mascara enviada en update NO | SI | SI (Longitud prefijo) |  |
| Direccion de Envio | Broadcast | Multicast | Multicast |
| (255.255.255.255) | (224.0.0.9) | (FF02::9) |  |
| Puerto UDP | 520 | 520 | 521 |
| Autenticacion | Ninguna | Texto plano y MD5 | IPsec (Nativo Capa 3) |
| Sumarizacion Automatica | Obligatoria | Opcional (Desactivable) N/A |  |
| Campo Next-Hop explicito | NO | SI | SI |
| Distancia Administrativa | 120 | 120 | 120 |




## 3. EL PROBLEMA DEL CONTEO AL INFINITO Y MECANISMOS DE PREVENCION DE BUCLES

En redes de vector distancia primitivas, la falla de un enlace generaba el clasico
bucle de enrutamiento "Conteo al Infinito" (Count to Infinity):
Si la red de R3 cae, R2 (que aun no lo sabe) le anuncia a R3 que puede llegar a esa red
a traves de R2 en 2 saltos. R3 le cree, actualiza a 3 saltos y se lo anuncia a R2.
R2 actualiza a 4 saltos, y asi sucesivamente rebotando el paquete hasta saturar el enlace.

Para solucionar esto, RIP implementa 5 mecanismos vitales:


### a) Split Horizon (Horizonte Dividido):

   - REGLA: "Un router NUNCA debe anunciar una ruta por la misma interfaz fisica
     por la cual la aprendio".
   - Si R2 aprendio la red 10.0.0.0 por su interfaz Gi0/1 (conectada a R3), R2 tiene
     prohibido enviar actualizaciones sobre esa red de regreso por Gi0/1.


### b) Poison Reverse (Envenenamiento Inverso):

   - Modificacion estricta de Split Horizon: En lugar de omitir la ruta, el router
     la devuelve explicitamente anunciando una metrica de 16 (inalcanzable).
   - Confirma de inmediato al vecino que no debe intentar usarlo como ruta alternativa.


### c) Route Poisoning (Envenenamiento de Rutas):

   - En cuanto un router detecta que una red directamente conectada se apaga, envia
     inmediatamente un paquete RIP fijando la metrica de esa red en 16 a todos sus vecinos.


### d) Holddown Timers (Temporizadores de Retencion):

   - Cuando un router recibe la noticia de que una red cayo (metrica 16), congela esa ruta
     durante 180 segundos. Durante ese tiempo, rechaza cualquier actualizacion que afirme
     tener una ruta con metrica igual o peor, permitiendo que la mala noticia se propague
     a toda la red antes de aceptar nuevos calculos.


### e) Triggered Updates (Actualizaciones Disparadas por Eventos):

   - RIP normalmente envia su tabla completa cada 30 segundos. Sin embargo, si un enlace
     cae, NO espera los 30 segundos: envia un paquete de actualizacion de inmediato (Flash Update).



## 4. LOS 4 TEMPORIZADORES DE RIP (TIMERS)

1. Update Timer (30 seg):
   - Intervalo regular con el que el router transmite su base de datos completa.
   - En Cisco se aplica un "jitter" aleatorio (25 a 35 seg) para evitar colisiones.
2. Invalid Timer (180 seg):
   - Si no se reciben noticias de una ruta durante 180 seg, se marca como sospechosa
     y su metrica se fija en 16.
3. Holddown Timer (180 seg):
   - Periodo de bloqueo preventivo contra actualizaciones inconsistentes.
4. Flush Timer (240 seg):
   - Si tras 240 segundos la ruta no ha revivido, se ELIMINA DEFINITIVAMENTE de la tabla RIB.



## 5. ¿DONDE SE UTILIZA RIP EN LA VIDA REAL HOY EN DIA?

Aunque OSPF y BGP dominan las redes corporativas modernas, RIPv2 y RIPng aun se encuentran en:
- Redes Industriales y SCADA / Subestaciones Electricas: Equipos RTU o PLCs antiguos con
  microprocesadores de muy baja capacidad donde el algoritmo SPF de OSPF consumiria toda la RAM.
- Redes Satelitales Maritimas Simples: Enlaces con ancho de banda extremadamente limitado
  donde solo se necesita una difusion periodica sencilla sin estado de enlace complejo.
- Equipos SOHO / Gateways VPN: Enrutamiento simple entre dos firewalls pequenos.
- Entornos de Ensenanza y Certificaciones Internacionales (CompTIA, Cisco).



## 6. ESCENARIO PRACTICO DE LA VIDA REAL: RED DE DISTRIBUCION CON RIPv2 Y MD5



#### 🎯 OBJETIVO DEL ESCENARIO:

Una empresa distribuidora de alimentos conecta su Sede Central con dos Centros de
Distribucion (CEDIS Norte y CEDIS Sur) mediante routers Cisco.
Se requiere configurar RIPv2 con:
- Desactivacion de sumarizacion automatica (`no auto-summary`) para admitir VLSM.
- Interfaces pasivas en las redes de usuario para evitar fugas de informacion.
- Inyeccion de ruta por defecto hacia Internet desde la Sede Central.
- Autenticacion criptografica MD5 en los enlaces WAN para evitar que routers piratas inyecten rutas falsas.


#### 🌐 DIAGRAMA DE LA TOPOLOGIA:

```text
             +-----------------------------------------+
             |         SEDE CENTRAL (R_CENTRAL)        |
             |       LAN: 192.168.100.0/24 (Gi0/0)     |
             |       Internet: Salida WAN (Loopback0)  |
             +-------------+-------------+-------------+
                           |             |
           WAN_NORTE       |             | WAN_SUR
      10.1.1.0/30 (Gi0/1)  |             | 10.1.2.0/30 (Gi0/2)
                           |             |
             +-------------+             +-------------+
             |                                         |
             v                                         v
   +--------------------+                    +--------------------+
   |   CEDIS NORTE      |                    |   CEDIS SUR        |
   |   (R_NORTE)        |                    |   (R_SUR)          |
   | LAN:               |                    | LAN:               |
   | 192.168.10.0/24    |                    | 192.168.20.0/24    |
   +--------------------+                    +--------------------+
```


#### 📋 TABLA DE DIRECCIONAMIENTO:


| Dispositivo | Interfaz | Direccion IP | Mascara | Descripcion |
| :--- | :--- | :--- | :--- | :--- |
| R_CENTRAL | Gi0/0 | 192.168.100.1 | 255.255.255.0 | LAN Servidores Central |
| R_CENTRAL | Gi0/1 | 10.1.1.1 | 255.255.255.252 | Enlace WAN hacia Norte |
| R_CENTRAL | Gi0/2 | 10.1.2.1 | 255.255.255.252 | Enlace WAN hacia Sur |
| R_CENTRAL | Lo0 | 200.10.10.1 | 255.255.255.255 | Simulacion de Internet |
| R_NORTE | Gi0/0 | 192.168.10.1 | 255.255.255.0 | LAN Usuarios Norte |
| R_NORTE | Gi0/1 | 10.1.1.2 | 255.255.255.252 | Enlace WAN hacia Central |
| R_SUR | Gi0/0 | 192.168.20.1 | 255.255.255.0 | LAN Usuarios Sur |
| R_SUR | Gi0/2 | 10.1.2.2 | 255.255.255.252 | Enlace WAN hacia Central |




## CONFIGURACION PASO A PASO EN CISCO IOS



## 1. CONFIGURACION EN ROUTER CENTRAL (R_CENTRAL):

! Configuracion de Llave de Autenticacion MD5
key chain RIP_KEY
 key 1
  key-string ClaveSeguraRIP2026
!
```text
interface GigabitEthernet0/0
 description LAN_CENTRAL_SERVIDORES
 ip address 192.168.100.1 255.255.255.0
 no shutdown
!
interface GigabitEthernet0/1
 description WAN_HACIA_CEDIS_NORTE
 ip address 10.1.1.1 255.255.255.252
 ip rip authentication mode md5
 ip rip authentication key-chain RIP_KEY
 no shutdown
!
interface GigabitEthernet0/2
 description WAN_HACIA_CEDIS_SUR
 ip address 10.1.2.1 255.255.255.252
 ip rip authentication mode md5
 ip rip authentication key-chain RIP_KEY
 no shutdown
!
interface Loopback0
 description SALIDA_A_INTERNET_SIMULADA
 ip address 200.10.10.1 255.255.255.255
!
ip route 0.0.0.0 0.0.0.0 Loopback0
!
! Configuracion del Proceso RIPv2
router rip
 version 2
 no auto-summary
 ! Desactivar el envio de updates en la LAN de usuarios (Seguridad y ahorro de trafico)
 passive-interface GigabitEthernet0/0
 network 10.0.0.0
 network 192.168.100.0
 ! Inyectar la ruta por defecto hacia los CEDIS remotos
 default-information originate
exit
```


## 2. CONFIGURACION EN CEDIS NORTE (R_NORTE):

key chain RIP_KEY
 key 1
  key-string ClaveSeguraRIP2026
!
```text
interface GigabitEthernet0/0
 description LAN_USUARIOS_CEDIS_NORTE
 ip address 192.168.10.1 255.255.255.0
 no shutdown
!
interface GigabitEthernet0/1
 description WAN_HACIA_CENTRAL
 ip address 10.1.1.2 255.255.255.252
 ip rip authentication mode md5
 ip rip authentication key-chain RIP_KEY
 no shutdown
!
router rip
 version 2
 no auto-summary
 passive-interface GigabitEthernet0/0
 network 10.0.0.0
 network 192.168.10.0
exit
```


## 3. CONFIGURACION EN CEDIS SUR (R_SUR):

key chain RIP_KEY
 key 1
  key-string ClaveSeguraRIP2026
!
```text
interface GigabitEthernet0/0
 description LAN_USUARIOS_CEDIS_SUR
 ip address 192.168.20.1 255.255.255.0
 no shutdown
!
interface GigabitEthernet0/2
 description WAN_HACIA_CENTRAL
 ip address 10.1.2.2 255.255.255.252
 ip rip authentication mode md5
 ip rip authentication key-chain RIP_KEY
 no shutdown
!
router rip
 version 2
 no auto-summary
 passive-interface GigabitEthernet0/0
 network 10.0.0.0
 network 192.168.20.0
exit
```


## COMANDOS DE VALIDACION Y VERIFICACION

1. Verificar que RIPv2 esta corriendo sin sumarizacion automatica:
   R_NORTE# show ip protocols
   Routing Protocol is "rip"
     Sending updates every 30 seconds, next due in 18 secs
     Invalid after 180 seconds, hold down 180, flushed after 240
     Outgoing update filter list for all interfaces is not set
     Incoming update filter list for all interfaces is not set
     Default redistribution metric is 1
     Redistributing: rip
     Default version control: send version 2, receive version 2
       Interface             Send  Recv  Triggered RIP  Key-chain
       GigabitEthernet0/1    2     2                    RIP_KEY
     Automatic network summarization is not in effect
     Routing for Networks:
       10.0.0.0
       192.168.10.0
     Passive Interface(s):
       GigabitEthernet0/0
     Routing Information Sources:
       Gateway         Distance      Last Update
       10.1.1.1             120      00:00:14

2. Comprobar la tabla de rutas aprendida en CEDIS Norte:
   R_NORTE# show ip route rip
   Gateway of last resort is 10.1.1.1 to network 0.0.0.0

   R*    0.0.0.0/0 [120/1] via 10.1.1.1, 00:00:08, GigabitEthernet0/1  (Ruta por defecto)
   R     10.1.2.0/30 [120/1] via 10.1.1.1, 00:00:08, GigabitEthernet0/1 (Enlace WAN Sur)
   R     192.168.20.0/24 [120/2] via 10.1.1.1, 00:00:08, GigabitEthernet0/1 (LAN Sur, 2 saltos!)
   R     192.168.100.0/24 [120/1] via 10.1.1.1, 00:00:08, GigabitEthernet0/1 (LAN Central)

   Notese: Para llegar a CEDIS Sur (192.168.20.0/24), la metrica es [120/2]:
   - 120 = Distancia Administrativa de RIP.
   - 2 = Cantidad de saltos (R_CENTRAL -> R_SUR).

3. Verificacion de la Base de Datos RIP:
   R_NORTE# show ip rip database
   192.168.20.0/24    auto-summary
   192.168.20.0/24    [2] via 10.1.1.1, 00:00:12, GigabitEthernet0/1

4. Diagnostico en tiempo real de actualizaciones y llaves MD5:
   R_NORTE# debug ip rip
   RIP: received packet with MD5 authentication
   RIP: received v2 update from 10.1.1.1 on GigabitEthernet0/1
        192.168.20.0/24 via 0.0.0.0 in 2 hops

## 0.0.0.0/0 via 0.0.0.0 in 1 hops
