# GUIA HUAWEI VRP - PARTE 7: ENRUTAMIENTO DINAMICO AVANZADO CON OSPF


---



## 1. ¿POR QUE UTILIZAR OSPF EN SWITCHES MULTICAPA?

Cuando una red corporativa crece y tiene multiples switches Core, switches de
distribucion y routers, las rutas estaticas se vuelven inmanejables.
OSPF (Open Shortest Path First) es el protocolo estandar de la industria que:
- Descubre rutas automaticamente.
- Si un enlace se corta, recalcula la mejor ruta alternativa en milisegundos.
- Distribuye la carga entre multiples enlaces (ECMP).



## 2. TOPOLOGIA DE EJEMPLO

- Switch Core 1 (Router ID: 1.1.1.1):
  * Vlanif 10 (Red Usuarios 1): 192.168.10.0/24
  * Vlanif 100 (Enlace hacia Core 2): 10.0.0.0/30 (IP local: 10.0.0.1)

- Switch Core 2 (Router ID: 2.2.2.2):
  * Vlanif 20 (Red Usuarios 2): 192.168.20.0/24
  * Vlanif 100 (Enlace hacia Core 1): 10.0.0.0/30 (IP local: 10.0.0.2)



## 3. CONFIGURACION DE OSPF EN SWITCH CORE 1

Paso 1: Iniciar el proceso OSPF asignando un Router ID unico
```text
[SW-CORE-1] ospf 1 router-id 1.1.1.1

Paso 2: Entrar al Area 0 (Area Backbone principal de OSPF)
[SW-CORE-1-ospf-1] area 0

Paso 3: Publicar las redes usando la MASCARA WILDCARD (Inversa a la mascara de red)
* Nota: Para una mascara 255.255.255.0, la wildcard es 0.0.0.255.
* Para una mascara 255.255.255.252 (/30), la wildcard es 0.0.0.3.

-- Publicar la red de enlace entre switches:
[SW-CORE-1-ospf-1-area-0.0.0.0] network 10.0.0.0 0.0.0.3

-- Publicar la red de usuarios de ventas:
[SW-CORE-1-ospf-1-area-0.0.0.0] network 192.168.10.0 0.0.0.255
[SW-CORE-1-ospf-1-area-0.0.0.0] quit

Paso 4: SEGURIDAD Y OPTIMIZACION (Silent-Interface)
No queremos enviar paquetes "Hello" de OSPF hacia las computadoras de los usuarios
(es un gasto inutil de ancho de banda y un riesgo de seguridad):
[SW-CORE-1-ospf-1] silent-interface Vlanif 10
[SW-CORE-1-ospf-1] quit
```


## 4. CONFIGURACION DE OSPF EN SWITCH CORE 2

```text
[SW-CORE-2] ospf 1 router-id 2.2.2.2
[SW-CORE-2-ospf-1] area 0
[SW-CORE-2-ospf-1-area-0.0.0.0] network 10.0.0.0 0.0.0.3
[SW-CORE-2-ospf-1-area-0.0.0.0] network 192.168.20.0 0.0.0.255
[SW-CORE-2-ospf-1-area-0.0.0.0] quit
[SW-CORE-2-ospf-1] silent-interface Vlanif 20
[SW-CORE-2-ospf-1] quit
```


## 5. AUTENTICACION OSPF ENTRE SWITCHES (PRODUCCION)

Para evitar que un dispositivo extrano se una al proceso OSPF e inyecte rutas falsas,
se encripta la comunicacion entre switches en la interfaz de enlace:

```text
[SW-CORE-1] interface Vlanif 100
[SW-CORE-1-Vlanif100] ospf authentication-mode md5 1 cipher ClaveOspfSegura2026!
[SW-CORE-1-Vlanif100] quit

(Se debe configurar exactamente la misma clave en el otro extremo en Core 2).
```


## 6. VERIFICACION Y MONITOREO

- Ver si los switches se reconocen como vecinos OSPF (Debe decir "Full"):
```text
    <SW-CORE-1> display ospf peer brief

- Ver todas las rutas aprendidas dinamicamente mediante OSPF:
    <SW-CORE-1> display ospf routing

- Ver la tabla de enrutamiento general (las rutas OSPF apareceran marcadas como "OSPF"):
    <SW-CORE-1> display ip routing-table protocol ospf
```
