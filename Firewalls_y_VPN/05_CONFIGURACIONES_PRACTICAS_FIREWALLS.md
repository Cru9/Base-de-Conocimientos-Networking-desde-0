# 05. CONFIGURACIONES REALES EN CORTAFUEGOS: FORTINET FORTIGATE Y PALO ALTO

> **FIREWALLS DE PROXIMA GENERACION (NGFW) Y VPNs EMPRESARIALES**


---


Este laboratorio contiene la sintaxis real utilizada por ingenieros de seguridad
para configurar:
1. Zonas de seguridad y direccionamiento IP.
2. Politicas de navegacion a Internet con Source NAT (PAT).
3. Publicacion de un servidor DMZ mediante Destination NAT (Virtual IP / Port Forwarding).
4. Tunel VPN IPsec Site-to-Site basado en rutas (Route-Based VPN).


## 1. CONFIGURACION EN FORTINET FORTIGATE (FORTIOS CLI)

# --- PASO 1: CREACION DE ZONAS E INTERFACES ---
config system zone
    edit "ZONA_TRUST"
        set interface "port2"
    next
    edit "ZONA_UNTRUST"
        set interface "port1"
    next
    edit "ZONA_DMZ"
        set interface "port3"
    next
end

# --- PASO 2: PUBLICACION DE SERVIDOR WEB (DESTINATION NAT / VIP) ---
config firewall vip
    edit "VIP_SERVIDOR_WEB"
        set extip 203.0.113.10
        set extintf "port1"
        set mappedip "192.168.50.10"
        set portforward enable
        set protocol tcp
        set extport 443
        set mappedport 443
    next
end

# --- PASO 3: POLITICA DE NAVEGACION DE EMPLEADOS A INTERNET (PAT) ---
config firewall policy
    edit 10
        set name "LAN_HACIA_INTERNET_PAT"
        set srcintf "ZONA_TRUST"
        set dstintf "ZONA_UNTRUST"
        set srcaddr "all"
        set dstaddr "all"
        set action accept
        set schedule "always"
        set service "ALL"
        set utm-status enable
        set ssl-ssh-profile "certificate-inspection"
        set av-profile "default"
        set webfilter-profile "default"
        set ips-sensor "default"
        set nat enable                  ! (Activa PAT / SNAT con la IP publica del port1)
    next
    edit 20
        set name "ACCESO_INTERNET_A_DMZ"
        set srcintf "ZONA_UNTRUST"
        set dstintf "ZONA_DMZ"
        set srcaddr "all"
        set dstaddr "VIP_SERVIDOR_WEB"
        set action accept
        set schedule "always"
        set service "HTTPS"
    next
end

# --- PASO 4: TUNEL VPN IPSEC SITE-TO-SITE (ROUTE-BASED) ---
config vpn ipsec phase1-interface
    edit "VPN_A_SUCURSAL"
        set interface "port1"
        set ike-version 2
        set peertype any
        set net-device disable
        set proposal aes256-sha256
        set dhgrp 14
        set remote-gw 198.51.100.1
        set psksecret "ClaveSecretaForti2026!"
        set dpd-retryinterval 20
    next
end

config vpn ipsec phase2-interface
    edit "VPN_A_SUCURSAL_P2"
        set phase1name "VPN_A_SUCURSAL"
        set proposal aes256gcm
        set pfs enable
        set dhgrp 14
        set auto-negotiate enable
    next
end

# Enrutar la subred de la sucursal por la interfaz del tunel:
config router static
    edit 5
        set dst 192.168.20.0 255.255.255.0
        set device "VPN_A_SUCURSAL"
    next
end



## 2. CONFIGURACION EN PALO ALTO NETWORKS (PAN-OS CLI)

# --- PASO 1: ZONAS DE SEGURIDAD ---
set zone trust network layer3 ethernet1/2
set zone untrust network layer3 ethernet1/1
set zone dmz network layer3 ethernet1/3

# --- PASO 2: POLITICA DE NAT DE SALIDA (PAT / DYNAMIC IP AND PORT - DIPP) ---
set nat rule LAN_A_INTERNET_PAT from trust to untrust source any destination any translation source dynamic-ip-and-port interface-address interface ethernet1/1

# --- PASO 3: REGLA DE SEGURIDAD CON APP-ID Y PERFILES DE AMENAZAS ---
set rulebase security rules NAVEGACION_EMPLEADOS from trust to untrust source any destination any application [ web-browsing ssl dns ms-office365-base ] service application-default action allow
set rulebase security rules NAVEGACION_EMPLEADOS profile-setting group default

# --- PASO 4: TUNEL VPN IPSEC BASADO EN RUTAS (VTI) ---
# Crear la interfaz de tunel logica:
set network interface tunnel units tunnel.10 ip 172.16.100.1/30
set zone trust network layer3 tunnel.10

# Perfil IKE (Fase 1) con IKEv2:
set network ike crypto-profiles ike-crypto-profiles PERFIL_IKE_P1 hash sha256 dh-group group14 encryption aes-256-cbc lifetime seconds 86400
set network ike gateway GW_SUCURSAL version ikev2 local-address interface ethernet1/1 peer-address ip 198.51.100.1 authentication pre-shared-key key ClaveSecretaPalo2026! protocol-common nat-traversal enable
set network ike gateway GW_SUCURSAL protocol ikev2 ike-crypto-profile PERFIL_IKE_P1

# Perfil IPsec (Fase 2) con PFS:
set network ipsec crypto-profiles ipsec-crypto-profiles PERFIL_IPSEC_P2 esp encryption aes-256-gcm authentication none dh-group group14 lifetime seconds 28800

# Vincular la interfaz de tunel con el gateway y crypto profile:
set network ipsec tunnel VPN_SUCURSAL_TUNNEL tunnel-interface tunnel.10 ike-gateway GW_SUCURSAL ipsec-crypto-profile PERFIL_IPSEC_P2

# Enrutamiento hacia la red remota:
set network virtual-router default routing-table ip static-route RUTA_A_SUCURSAL destination 192.168.20.0/24 interface tunnel.10

# Confirmar y aplicar los cambios en memoria persistente:

`cisco
commit
`
