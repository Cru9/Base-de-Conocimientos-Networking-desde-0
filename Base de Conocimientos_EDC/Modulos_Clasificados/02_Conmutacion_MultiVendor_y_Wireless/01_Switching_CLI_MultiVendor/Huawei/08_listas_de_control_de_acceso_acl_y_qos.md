# GUIA HUAWEI VRP - PARTE 8: LISTAS DE ACCESO (ACL), FILTRADO DE TRAFICO Y QOS


---



## 1. ¿QUE SON LAS ACL (ACCESS CONTROL LISTS)?

Son reglas ordenadas que permiten o deniegan paquetes que pasan por el switch.
En Huawei existen 2 categorias principales:


### A) ACL Basicas (Numeros 2000 al 2999):

   - Solo pueden filtrar basandose en la DIRECCION IP DE ORIGEN.

### B) ACL Avanzadas (Numeros 3000 al 3999):

   - Pueden filtrar por IP de Origen, IP de Destino, Protocolo (TCP, UDP, ICMP)
     y Puertos de servicio (HTTP 80, HTTPS 443, SSH 22, etc.).



## 2. CASO PRACTICO: ACL AVANZADA DE SEGURIDAD

Objetivo de negocio:
- Los usuarios de Ventas (192.168.10.0/24) NO deben tener acceso al Servidor
  de Base de Datos Financiera (192.168.50.100).
- El resto del trafico si debe permitirse normalmente.

Paso 1: Crear la ACL Avanzada (Numero 3001)
```text
[HUAWEI] acl number 3001
[HUAWEI-acl-adv-3001] description BLOQUEO_ACCESO_BASE_DATOS

-- Regla 5: Denegar trafico IP desde la red de ventas hacia la IP del servidor
[HUAWEI-acl-adv-3001] rule 5 deny ip source 192.168.10.0 0.0.0.255 destination 192.168.50.100 0

-- Regla 10: Permitir todo el demas trafico
[HUAWEI-acl-adv-3001] rule 10 permit ip
[HUAWEI-acl-adv-3001] quit

Paso 2: Aplicar la ACL mediante Traffic-Filter
Las ACLs se aplican en la direccion INBOUND (entrando al switch) o OUTBOUND (saliendo).
Se recomienda aplicar lo mas cerca posible del origen (en la Vlanif 10):

[HUAWEI] interface Vlanif 10
[HUAWEI-Vlanif10] traffic-filter inbound acl 3001
[HUAWEI-Vlanif10] quit
```


## 3. CONTROL DE ANCHO DE BANDA (RATE LIMITING / QOS)

Si tienes un usuario o departamento que satura la conexion con descargas masivas,
puedes limitar la velocidad fisica de su puerto:

Ejemplo: Limitar el puerto GigabitEthernet 0/0/5 a un maximo de 20 Megas (20,480 Kbps):
```text
[HUAWEI] interface GigabitEthernet 0/0/5
-- Limitar trafico de subida (Inbound):
[HUAWEI-GigabitEthernet0/0/5] qos lr inbound cir 20480 cbs 2560000

-- Limitar trafico de bajada (Outbound):
[HUAWEI-GigabitEthernet0/0/5] qos lr outbound cir 20480 cbs 2560000
[HUAWEI-GigabitEthernet0/0/5] quit

* Explicacion de terminos:
  - CIR (Committed Information Rate): Velocidad en Kbps garantizada/maxima.
  - CBS (Committed Burst Size): Rafaga de paquetes permitida en bytes.
```


## 4. PUERTO ESPEJO PARA ANALISIS DE TRAFICO (PORT MIRRORING / WIRESHARK)

¿Para que sirve?
Copia todo el trafico de uno o varios puertos sospechosos hacia el puerto donde
el ingeniero tiene conectada su laptop con Wireshark para analizar la red.

Paso 1: Definir el puerto donde esta conectada la laptop de monitoreo (puerto observador)
```text
[HUAWEI] observe-port 1 interface GigabitEthernet 0/0/20

Paso 2: Indicar que puerto queremos espiar / clonar (ej. el puerto del servidor 0/0/1)
[HUAWEI] interface GigabitEthernet 0/0/1
[HUAWEI-GigabitEthernet0/0/1] port-mirroring to observe-port 1 both
  -> "both" clona tanto el trafico entrante (inbound) como saliente (outbound).
[HUAWEI-GigabitEthernet0/0/1] quit
```


## 5. VERIFICACION

- Ver configuracion y reglas de una ACL especifica:
```text
    <HUAWEI> display acl 3001

- Ver estadisticas de cuantos paquetes han coincidido con la regla de bloqueo:
    <HUAWEI> display traffic-filter statistics interface Vlanif 10 inbound

- Ver configuracion del puerto de monitoreo (Mirroring):
    <HUAWEI> display observe-port
```
