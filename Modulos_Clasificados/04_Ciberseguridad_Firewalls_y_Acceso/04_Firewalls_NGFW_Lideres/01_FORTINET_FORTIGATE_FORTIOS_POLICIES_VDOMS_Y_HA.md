# 01. FORTINET FORTIGATE (FORTIOS 7.X): POLITICAS, VDOMS, FGCP HA Y SD-WAN

> **FIREWALLS DE PROXIMA GENERACION (NGFW) POR MARCA LIDER**


---



## 1. ARQUITECTURA DE HARDWARE Y ASICS EN FORTINET

El secreto del alto rendimiento de Fortinet radica en sus procesadores de silicio
personalizados (ASICs):
- NP7 (Network Processor): Acelera en hardware el reenvio de paquetes IPv4/IPv6,
  tablas de enrutamiento, NAT masivo y cifrado de tuneles VPN IPsec (hasta 100 Gbps).
- CP9 (Content Processor): Acelera la criptografia SSL/TLS, desencapsulado de paquetes
  e inspeccion de firmas antivirus e IPS sin sobrecargar la CPU general.
- SoC4 / SoC5 (System-on-a-Chip): Combina CPU x86/ARM con NP y CP en un solo chip
  para equipos de sucursal compactos (series 40F, 60F, 70F, 80F).



## 2. VIRTUAL DOMAINS (VDOMs): MULTI-TENANCY EN EL MISMO CHASIS

Un VDOM divide un FortiGate fisico en multiples firewalls logicos completamente
aislados. Cada VDOM tiene su propia tabla de enrutamiento, politicas de seguridad,
administradores independientes y servidores de log.

Comandos para habilitar VDOMs en CLI:
config system global
    set vdom-mode multi-vdom
end

Creacion de un VDOM para clientes externos e interconexion por VDOM-Link:
config vdom
    edit VDOM-CLIENTES
next
end

! Crear enlace inter-VDOM virtual (sin cables externos)
config system vdom-link
    edit VLINK-ROOT-CLI
        set type ethernet
    next
end



## 3. CONFIGURACION DE OBJETOS, VIP (DNAT) Y POLITICAS DE SEGURIDAD

! 1. Crear objetos de direccion IP
config firewall address
    edit "NET_LAN_FINANZAS"
        set subnet 10.10.20.0 255.255.255.0
    next
    edit "SRV_WEB_INTERNO"
        set subnet 10.10.50.80 255.255.255.255
    next
end

! 2. Crear un VIP (Virtual IP / Port Forwarding para publicar servidor a Internet)
config firewall vip
    edit "VIP_PUBLICACION_WEB"
        set extip 200.50.10.80
        set mappedip "10.10.50.80"
        set extintf "port1"          ! Interfaz WAN conectada al ISP
        set portforward enable
        set protocol tcp
        set extport 443
        set mappedport 8443
    next
end

! 3. Crear Politica de Seguridad de Salida a Internet (con NAT y Seguridad Capa 7)
config firewall policy
    edit 10
        set name "POL_SALIDA_INTERNET_LAN"
        set srcintf "port2"          ! Interfaz LAN interna
        set dstintf "port1"          ! Interfaz WAN Internet
        set srcaddr "NET_LAN_FINANZAS"
        set dstaddr "all"
        set action accept
        set schedule "always"
        set service "HTTP" "HTTPS" "DNS"
        set utm-status enable        ! Habilitar perfiles de seguridad UTM / NGFW
        set ssl-ssh-profile "certificate-inspection"
        set av-profile "default"
        set ips-sensor "default"
        set application-list "default"
        set nat enable               ! Habilitar Source NAT (masquerade)
    next
    edit 20
        set name "POL_ACCESO_WEB_PUBLICADO"
        set srcintf "port1"
        set dstintf "port3"          ! Interfaz DMZ
        set srcaddr "all"
        set dstaddr "VIP_PUBLICACION_WEB"
        set action accept
        set schedule "always"
        set service "ALL"
        set utm-status enable
        set ips-sensor "protect_http_server"
        set nat disable
    next
end



## 4. ALTA DISPONIBILIDAD: CLUSTER FGCP (ACTIVO-PASIVO)

El protocolo propietario FGCP (FortiGate Clustering Protocol) garantiza redundancia
con conmutacion transparente de sesiones TCP en milisegundos:

Configuracion en FortiGate PRIMARIO (Nodo A):
config system ha
    set group-name "CLUSTER-PROD-HA"
    set mode a-p                       ! Active-Passive
    set password ClaveClusterSecreta2026#
    set priority 200                   ! Mayor prioridad = Nodo Maestro
    set override disable               ! Evita flap recurrente al reiniciar
    set hbdev "port7" 50 "port8" 40    ! Enlaces dedicados de Heartbeat con peso
    set session-pickup enable          ! Sincronizar sesiones TCP activas
    set monitor "port1" "port2"        ! Si cae la WAN o la LAN, conmuta el cluster
end

Configuracion en FortiGate SECUNDARIO (Nodo B):
config system ha
    set group-name "CLUSTER-PROD-HA"
    set mode a-p
    set password ClaveClusterSecreta2026#
    set priority 100                   ! Menor prioridad = Nodo Esclavo
    set override disable
    set hbdev "port7" 50 "port8" 40
    set session-pickup enable
    set monitor "port1" "port2"
end



## 5. SD-WAN INTEGRADO EN FORTIOS

FortiOS incluye controlador SD-WAN nativo sin licencias adicionales:
config system sdwan
    config zone
        edit "ZONA_INTERNET"
        next
    end
    config members
        edit 1
            set interface "port1"      ! ISP 1 Fibra Dedicada
            set zone "ZONA_INTERNET"
            set gateway 200.50.10.1
        next
        edit 2
            set interface "port2"      ! ISP 2 Backup Coaxial / Radioenlace
            set zone "ZONA_INTERNET"
            set gateway 190.20.5.1
        next
    end
    config health-check
        edit "SLA_GOOGLE_DNS"
            set server "8.8.8.8"
            set members 1 2
            config sla
                edit 1
                    set latency-threshold 50
                    set jitter-threshold 10
                    set packetloss-threshold 2
                next
            end
        next
    end
    config service
        edit 1
            set name "REGLA_TRAFICO_CRITICO_VOIP"
            set mode priority
            set dst "NET_SERVIDORES_VOIP"
            set health-check "SLA_GOOGLE_DNS"
            set link-cost-process enable
            set priority-members 1 2
        next
    end
end



## 6. DIAGNOSTICO Y TROUBLESHOOTING EN FORTIOS

1. Verificar estado del cluster de Alta Disponibilidad:
   get system ha status
   ! Comprueba si ambos nodos estan sincronizados (checksum match: yes).

2. Rastrear el flujo de un paquete en tiempo real (Packet Sniffer):
   diagnose sniffer packet any "host 10.10.20.15 and port 443" 4 0 l

3. Seguir el motor de politicas para ver por que se descarta un paquete (Debug Flow):
   diagnose debug reset
   diagnose debug flow filter saddr 10.10.20.15
   diagnose debug flow filter daddr 8.8.8.8
   diagnose debug flow show function-name enable
   diagnose debug flow trace start 20
   diagnose debug enable
   ! Para apagar la depuracion:

`cisco
diagnose debug disable
`
