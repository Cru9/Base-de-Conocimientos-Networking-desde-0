# GUIA HP PROCURVE / ARUBA - PARTE 8: LISTAS DE ACCESO (ACL), QOS Y PUERTO ESPEJO (MIRRORING)


---



## 1. ¿QUE SON LAS ACL (ACCESS CONTROL LISTS) EN HP?

Son listas ordenadas de reglas de seguridad que inspeccionan los paquetes de red
para decidir si se permiten (permit) o se descartan (deny).

Tipos de ACL:

### A) Standard: Solo filtran segun la DIRECCION IP DE ORIGEN.


### B) Extended: Filtran por IP de Origen, IP de Destino, Protocolo (TCP/UDP/ICMP)

   y Puertos de servicio (HTTP 80, HTTPS 443, SSH 22, SQL 1433, etc.).
¡REGLA FUNDAMENTAL!: Al final de cada lista de acceso existe un "deny implícito"
(todo lo que no se permita explicitamente sera bloqueado).



## 2. CASO PRACTICO: ACL EXTENDIDA DE SEGURIDAD

Objetivo de red:
- Los usuarios de Ventas (192.168.10.0/24) NO deben tener acceso al Servidor
  de Base de Datos Financiera (192.168.50.100) en el puerto SQL (1433) ni SSH (22).
- Permitir todo el resto del trafico.

Paso 1: Crear la ACL extendida con nombre descriptivo:
```cisco
SW-HP(config)# ip access-list extended FILTRO_VENTAS

-- Regla 10: Denegar trafico TCP hacia el puerto SQL 1433 del servidor:
SW-HP(config-ext-nacl)# 10 deny tcp 192.168.10.0 0.0.0.255 192.168.50.100 0.0.0.0 eq 1433

-- Regla 20: Denegar acceso SSH (puerto 22):
SW-HP(config-ext-nacl)# 20 deny tcp 192.168.10.0 0.0.0.255 192.168.50.100 0.0.0.0 eq 22

-- Regla 30: Permitir todo el demas trafico:
SW-HP(config-ext-nacl)# 30 permit ip any any
SW-HP(config-ext-nacl)# exit

Paso 2: Aplicar la ACL a la interfaz de la VLAN (en direccion de entrada IN):
SW-HP(config)# vlan 10
SW-HP(vlan-10)# ip access-group FILTRO_VENTAS in
SW-HP(vlan-10)# exit
```


## 3. CONTROL DE ANCHO DE BANDA POR PUERTO (RATE LIMITING / QOS)

Para evitar que un usuario sature la red con descargas descontroladas:

Ejemplo: Limitar el puerto 5 a una velocidad maxima de 20 Megas (20,000 Kbps):
```cisco
SW-HP(config)# interface 5
-- Limitar trafico entrante (Inbound):
SW-HP(eth-5)# rate-limit in kbps 20000
-- Limitar trafico saliente (Outbound):
SW-HP(eth-5)# rate-limit out kbps 20000
SW-HP(eth-5)# exit
```


## 4. PUERTO ESPEJO PARA ANALISIS CON WIRESHARK (PORT MONITOR / MIRRORING)

¿Para que sirve?
Clona todo el trafico de un puerto bajo sospecha (ej. puerto 1) y lo envia al puerto
donde tienes conectada tu laptop de diagnostico (ej. puerto 24):

Paso 1: Definir el puerto observador donde esta tu laptop con Wireshark:
```cisco
SW-HP(config)# mirror 1 port 24

Paso 2: Indicar que puerto(s) deseas monitorear y clonar hacia el monitor 1:
SW-HP(config)# interface 1
SW-HP(eth-1)# monitor all 1
  -> "all" captura tanto el trafico recibido (Rx) como transmitido (Tx).
SW-HP(eth-1)# exit
```


## 5. COMANDOS DE DIAGNOSTICO Y MONITOREO

- Ver las ACLs configuradas y contadores de coincidencia:
```cisco
    SW-HP# show access-list
    SW-HP# show access-list config

- Ver estado de la sesion de puerto espejo (Mirroring):
    SW-HP# show monitor

- Ver politicas de limitacion de ancho de banda (Rate-limit):
    SW-HP# show rate-limit 5
```
