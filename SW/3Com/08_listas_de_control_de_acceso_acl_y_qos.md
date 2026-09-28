# GUIA 3COM COMWARE - PARTE 8: LISTAS DE ACCESO (ACL), FILTRADO DE TRAFICO Y QOS


---



## 1. ¿QUE SON LAS ACL (ACCESS CONTROL LISTS) EN 3COM?

Son listas de reglas que examinan los paquetes que cruzan el switch y deciden si
se permiten o se descartan:


### A) ACL Basicas (Numeros 2000 al 2999):

   - Solo pueden filtrar segun la DIRECCION IP DE ORIGEN.

### B) ACL Avanzadas (Numeros 3000 al 3999):

   - Filtran por IP de Origen, IP de Destino, Protocolo (TCP, UDP, ICMP) y Puertos
     especificos (HTTP 80, HTTPS 443, SSH 22, SQL 1433, etc.).



## 2. CASO PRACTICO: ACL AVANZADA DE SEGURIDAD

Objetivo de red:
- Los usuarios de Ventas (192.168.10.0/24) NO deben tener acceso al Servidor
  de Base de Datos Financiera (192.168.50.100).
- El resto del trafico si debe permitirse normalmente.

Paso 1: Crear la ACL Avanzada (Numero 3001)
```text
[3Com] acl number 3001

-- Regla 5: Denegar trafico IP desde la red de ventas hacia la IP del servidor
[3Com-acl-adv-3001] rule 5 deny ip source 192.168.10.0 0.0.0.255 destination 192.168.50.100 0

-- Regla 10: Permitir todo el demas trafico
[3Com-acl-adv-3001] rule 10 permit ip
[3Com-acl-adv-3001] quit

Paso 2: Aplicar la ACL mediante Traffic-Filter o Packet-Filter
Se aplica en la direccion INBOUND (entrando al switch) en la interfaz Gateway:

[3Com] interface Vlan-interface 10
[3Com-Vlan-interface10] packet-filter 3001 inbound
[3Com-Vlan-interface10] quit
```


## 3. CONTROL DE ANCHO DE BANDA POR PUERTO (LINE RATE / QOS)

Si necesitas limitar la velocidad maxima de un puerto para que un usuario no sature
la conexion a Internet con descargas excesivas:

Ejemplo: Limitar el puerto GigabitEthernet 1/0/5 a maximo 20 Megas (20,480 Kbps):
```text
[3Com] interface GigabitEthernet 1/0/5
-- Limitar trafico entrante (Inbound):
[3Com-GigabitEthernet1/0/5] line-rate inbound 20480
-- Limitar trafico saliente (Outbound):
[3Com-GigabitEthernet1/0/5] line-rate outbound 20480
[3Com-GigabitEthernet1/0/5] quit
```


## 4. PUERTO ESPEJO PARA ANALISIS CON WIRESHARK (MIRRORING-GROUP)

¿Para que sirve?
Copia en tiempo real todo el trafico de un puerto sospechoso hacia el puerto donde
el administrador tiene conectada su laptop con Wireshark:

Paso 1: Crear el grupo de monitoreo local 1:
```text
[3Com] mirroring-group 1 local

Paso 2: Indicar el puerto que queremos espiar/clonar (puerto origen):
[3Com] mirroring-group 1 mirroring-port GigabitEthernet 1/0/1 both
  -> "both" captura paquetes entrantes y salientes.

Paso 3: Indicar el puerto donde esta conectada la laptop de captura (puerto destino):
[3Com] mirroring-group 1 monitor-port GigabitEthernet 1/0/20
```


## 5. VERIFICACION

- Ver reglas de la ACL y estadisticas de coincidencia:
```text
    <3Com> display acl 3001

- Ver configuracion del puerto espejo (Mirroring):
    <3Com> display mirroring-group 1
```
