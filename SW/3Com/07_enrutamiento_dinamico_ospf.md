# GUIA 3COM COMWARE - PARTE 7: ENRUTAMIENTO DINAMICO AVANZADO CON OSPF


---



## 1. ¿POR QUE UTILIZAR OSPF EN SWITCHES MULTICAPA 3COM?

OSPF (Open Shortest Path First) permite que switches Core y de distribucion aprendan
todas las subredes de la empresa de forma automatica:
- Si un enlace o switch se corta, OSPF recalcula la mejor ruta alternativa en milisegundos.
- Soporta balanceo de carga en rutas de igual costo (ECMP).
- Evita el mantenimiento manual de decenas de rutas estaticas.



## 2. CONFIGURACION DE OSPF EN SWITCH CORE 1

Escenario:
- VLAN 10 (Red Usuarios): 192.168.10.0/24
- VLAN 100 (Enlace hacia Core 2): 10.0.0.0/30 (IP local: 10.0.0.1)

Paso 1: Iniciar el proceso OSPF y fijar el Router-ID (Identificador unico)
```text
[SW-CORE-1] ospf 1 router-id 1.1.1.1

Paso 2: Entrar al Area 0 (Backbone principal de OSPF)
[SW-CORE-1-ospf-1] area 0

Paso 3: Publicar las redes usando la MASCARA WILDCARD (Inversa a la mascara de red)
* Mascara 255.255.255.0   -> Wildcard: 0.0.0.255
* Mascara 255.255.255.252 -> Wildcard: 0.0.0.3

-- Publicar el enlace hacia Core 2:
[SW-CORE-1-ospf-1-area-0.0.0.0] network 10.0.0.0 0.0.0.3

-- Publicar la red de usuarios de ventas:
[SW-CORE-1-ospf-1-area-0.0.0.0] network 192.168.10.0 0.0.0.255
[SW-CORE-1-ospf-1-area-0.0.0.0] quit

Paso 4: SEGURIDAD Y RENDIMIENTO (Silent-Interface)
No queremos enviar paquetes "Hello" de OSPF hacia las computadoras de los usuarios
(evita gasto inutil de ancho de banda y que alguien conecte un router falso):
[SW-CORE-1-ospf-1] silent-interface Vlan-interface 10
[SW-CORE-1-ospf-1] quit
```


## 3. CONFIGURACION DE OSPF EN SWITCH CORE 2 (VECINO)

```text
[SW-CORE-2] ospf 1 router-id 2.2.2.2
[SW-CORE-2-ospf-1] area 0
[SW-CORE-2-ospf-1-area-0.0.0.0] network 10.0.0.0 0.0.0.3
[SW-CORE-2-ospf-1-area-0.0.0.0] network 192.168.20.0 0.0.0.255
[SW-CORE-2-ospf-1-area-0.0.0.0] quit
[SW-CORE-2-ospf-1] silent-interface Vlan-interface 20
[SW-CORE-2-ospf-1] quit
```


## 4. AUTENTICACION ENCRIPTADA MD5 ENTRE SWITCHES

Para asegurar que solo los switches autenticados puedan compartir informacion de rutas:

```text
[SW-CORE-1] interface Vlan-interface 100
[SW-CORE-1-Vlan-interface100] ospf authentication-mode md5 1 cipher ClaveOspf3Com2026!
[SW-CORE-1-Vlan-interface100] quit

(Configurar exactamente la misma clave en el otro extremo en Core 2).
```


## 5. COMANDOS DE VERIFICACION

- Comprobar que los switches son vecinos OSPF (El estado DEBE ser "Full"):
```text
    <SW-CORE-1> display ospf peer brief

- Ver todas las rutas aprendidas por OSPF:
    <SW-CORE-1> display ospf routing

- Ver la tabla de enrutamiento general filtrando solo OSPF:
    <SW-CORE-1> display ip routing-table protocol ospf
```
