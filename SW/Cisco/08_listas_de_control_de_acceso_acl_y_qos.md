# GUIA CISCO IOS - PARTE 8: LISTAS DE ACCESO (ACL), QOS Y PUERTO ESPEJO (SPAN)


---



## 1. ¿QUE SON LAS ACL (ACCESS CONTROL LISTS) EN CISCO?

Son filtros de seguridad que inspeccionan paquetes y deciden si pasan (permit)
o se descartan (deny).

Tipos de ACL IPv4:

### A) Estandar (Numeradas 1-99 o con nombre):

   - Solo filtran segun la DIRECCION IP DE ORIGEN.

### B) Extendidas (Numeradas 100-199 o con nombre):

   - Filtran por IP de Origen, IP de Destino, Protocolo (TCP, UDP, ICMP) y Puertos
     especificos (HTTP 80, HTTPS 443, SSH 22, RDP 3389, etc.).
¡REGLA DE ORO!: En el fondo de TODA lista de acceso existe un "deny ip any any"
implicito (todo lo que no permitas explicitamente, sera bloqueado).



## 2. CASO PRACTICO: ACL EXTENDIDA CON NOMBRE (BEST PRACTICE)

Objetivo de seguridad:
- Impedir que la red de Ventas (192.168.10.0/24) acceda al Servidor de Base de Datos
  (192.168.50.100) en el puerto SQL (TCP 1433) y SSH (TCP 22).
- Permitir todo el resto del trafico.

Paso 1: Crear la ACL extendida con un nombre descriptivo
```cisco
Switch(config)# ip access-list extended FILTRO_SEGURIDAD_VENTAS

-- Regla 10: Bloquear acceso al puerto SQL 1433
Switch(config-ext-nacl)# 10 deny tcp 192.168.10.0 0.0.0.255 host 192.168.50.100 eq 1433

-- Regla 20: Bloquear acceso SSH (puerto 22)
Switch(config-ext-nacl)# 20 deny tcp 192.168.10.0 0.0.0.255 host 192.168.50.100 eq 22

-- Regla 30: Permitir todo el demas trafico
Switch(config-ext-nacl)# 30 permit ip any any
Switch(config-ext-nacl)# exit

Paso 2: Aplicar la ACL en la interfaz correspondiente (en direccion IN):
Switch(config)# interface vlan 10
Switch(config-if)# ip access-group FILTRO_SEGURIDAD_VENTAS in
Switch(config-if)# exit
```


## 3. CONTROL DE ANCHO DE BANDA CON QOS (POLICING MQC)

Para limitar la velocidad de descarga/subida de un puerto y evitar saturaciones:

Ejemplo: Limitar el puerto GigabitEthernet 0/5 a maximo 20 Megas (20,000,000 bps):

Paso 1: Crear una Class-Map que capture todo el trafico:
```cisco
Switch(config)# class-map MATCH_ALL_TRAFFIC
Switch(config-cmap)# match any
Switch(config-cmap)# exit

Paso 2: Crear la Policy-Map con la accion de limitacion (Policing):
Switch(config)# policy-map LIMITAR_20MEGAS
Switch(config-pmap)# class MATCH_ALL_TRAFFIC
-- police <bits por segundo> <tamano rafaga normal en bytes> conform-action transmit exceed-action drop
Switch(config-pmap-c)# police 20000000 2500000 conform-action transmit exceed-action drop
Switch(config-pmap-c)# exit
Switch(config-pmap)# exit

Paso 3: Aplicar la politica al puerto fisico:
Switch(config)# interface GigabitEthernet 0/5
Switch(config-if)# service-policy input LIMITAR_20MEGAS
Switch(config-if)# exit
```


## 4. PUERTO ESPEJO PARA ANALISIS CON WIRESHARK (CISCO SPAN)

¿Que es SPAN (Switched Port Analyzer)?
Permite clonar todo el trafico de un puerto sospechoso (ej. G0/1) y enviarlo
al puerto donde conectas tu laptop con Wireshark (ej. G0/20) sin afectar el servicio.

```cisco
Switch(config)# monitor session 1 source interface GigabitEthernet 0/1 both
  -> "both": Captura trafico entrante (Rx) y saliente (Tx).

Switch(config)# monitor session 1 destination interface GigabitEthernet 0/20
  -> Puerto donde conectas tu laptop para capturar los paquetes.
```


## 5. COMANDOS DE DIAGNOSTICO Y MONITOREO

- Ver las ACLs configuradas y CUANTOS PAQUETES han coincidido con cada regla (matches):
```cisco
    Switch# show access-lists

- Ver si la politica de limitacion de ancho de banda esta descartando paquetes excedentes:
    Switch# show policy-map interface GigabitEthernet 0/5

- Ver las sesiones de monitoreo (SPAN) activas:
    Switch# show monitor session 1
```
