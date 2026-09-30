# 04. GUIA DE CONFIGURACION: CONTROLADORAS CISCO CATALYST 9800 Y ARUBA MOBILITY

> **REDES INALAMBRICAS EMPRESARIALES (WIRELESS ENTERPRISE NETWORKING)**


---


Escenario Corporativo de Referencia:
- SSID Empresarial: "EMPRESA_SEGURA"
- Seguridad: WPA3-Enterprise con IEEE 802.1X (EAP-TLS / PEAP).
- Servidor RADIUS Centralizado (Cisco ISE / Aruba ClearPass): 10.100.1.50
- Roaming Rapido: Habilitado con 802.11r (FT), 802.11k y 802.11v.
- Proteccion de Tramas de Gestion: PMF (802.11w) Obligatorio.
- Segmento de Red de Empleados: VLAN 20 (Subred 10.20.0.0/24).



## 1. CONFIGURACION EN CISCO CATALYST 9800 WLC (IOS-XE WIRELESS)



## A) Definicion del Servidor RADIUS y Grupo AAA:

radius server RADIUS-ISE-01
  address ipv4 10.100.1.50 auth-port 1812 acct-port 1813
  key 7 ClaveSuperSeguraRadius2026!
  automate-tester username test-probe idle-time 5

aaa group server radius GRUPO-RADIUS-CORP
  server name RADIUS-ISE-01

aaa authentication dot1x METODO-DOT1X-CORP group GRUPO-RADIUS-CORP
aaa authorization network METODO-AUTHZ-CORP group GRUPO-RADIUS-CORP
aaa accounting identity METODO-ACCT-CORP start-stop group GRUPO-RADIUS-CORP


## B) Creacion del Perfil WLAN (SSID y Seguridad WPA3):

wlan EMPRESA_SEGURA 1 EMPRESA_SEGURA
  security dot1x authentication-list METODO-DOT1X-CORP
  security wpa
  security wpa version wpa3
  security wpa mode 802.1x
  security wpa wpa3-sae-pmk-timeout 43200
  security pmf mandatory
  security ft over-the-air
  security ft
  mobility-domain 0x1234
  assisted-roaming neighbor-list
  assisted-roaming prediction-list
  bss-transition
```text
  no shutdown
```


## C) Creacion del Perfil de Politica (Policy Profile - Mapeo de VLAN):

wireless profile policy POLITICA-CORP-VLAN20
```text
  vlan 20
  central switching
  central dhcp
  central association
  session-timeout 28800
  no shutdown
```


## D) Asociacion en Policy Tag y Despliegue en APs:

wireless tag policy TAG-POLITICA-SEDE-CENTRAL
  wlan EMPRESA_SEGURA policy POLITICA-CORP-VLAN20

! Asignar la etiqueta a los puntos de acceso del edificio
ap 00:a3:8e:11:22:33
  policy-tag TAG-POLITICA-SEDE-CENTRAL



## 2. CONFIGURACION EN ARUBA MOBILITY CONDUCTOR / CONTROLLER (ARUBAOS 8.X)



## A) Definicion del Servidor RADIUS (ClearPass):

aaa authentication-server radius "CLEARPASS-CORP"
  host "10.100.1.50"
  key "ClaveSuperSeguraRadius2026!"
  auth-port 1812
  acct-port 1813

aaa server-group "GRUPO-RADIUS-CLEARPASS"
  auth-server "CLEARPASS-CORP"


## B) Creacion del Perfil de Autenticacion 802.1X y Perfil AAA:

aaa authentication dot1x "PERFIL-DOT1X-CORP"
  wpa3-enterprise-ccmp-128
  pmf-mandatory
  fast-bss-transition
  ft-over-air

aaa profile "PERFIL-AAA-CORP"
  authentication-dot1x "PERFIL-DOT1X-CORP"
  dot1x-server-group "GRUPO-RADIUS-CLEARPASS"
  initial-role "logon"
  default-role "authenticated-employee"


## C) Creacion del Perfil SSID (WLAN):

wlan ssid-profile "SSID-EMPRESA-SEGURA"
  essid "EMPRESA_SEGURA"
  opmode wpa3-enterprise-aes
  mfp-mandatory
  advertise-ap-name
```text
  enable-11k
  enable-11v
```


## D) Creacion del Virtual AP (VAP Profile) y Asignacion de VLAN:

wlan virtual-ap "VAP-EMPRESA-SEGURA"
  aaa-profile "PERFIL-AAA-CORP"
  ssid-profile "SSID-EMPRESA-SEGURA"
```text
  vlan 20

! Asignar el VAP al grupo de APs corporativos
ap-group "GRUPO-APS-EDIFICIO-CENTRAL"
  virtual-ap "VAP-EMPRESA-SEGURA"
```



## 3. COMANDOS DE MONITOREO Y VERIFICACION EN PRODUCCION


En Cisco Catalyst 9800 WLC:
- `show wireless summary`                -> Resumen de APs registrados y clientes conectados.
- `show wlan summary`                    -> Estado operativo de los SSIDs configurados.
- `show wireless client summary`         -> Lista de laptops y telefonos conectados actualmente.
- `show wireless client mac <MAC_CLIENTE> detail`
                                         -> Muestra si el cliente negocio 802.11r, RSSI y SNR.
- `show ap auto-rf dot11 5ghz`           -> Muestra la asignacion automatica de canales y potencia.

En Aruba Mobility Controller:
- `show ap active`                       -> Lista de APs encendidos y su canal de operacion.
- `show user-table`                      -> Usuarios autenticados, su IP, VLAN y rol asignado.
- `show ap bss-table`                    -> Mapeo de SSIDs transmitidos por cada AP.
- `show aaa authentication-server operational`

## -> Diagnostico de disponibilidad del servidor RADIUS.
