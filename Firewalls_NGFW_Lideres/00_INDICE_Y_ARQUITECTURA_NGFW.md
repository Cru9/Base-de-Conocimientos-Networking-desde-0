# 00. INDICE GENERAL, ARQUITECTURA DE INSPECCION CAPA 7 Y ZONAS DE SEGURIDAD

> **FIREWALLS DE PROXIMA GENERACION (NGFW) POR MARCA LIDER**


---



## 1. EVOLUCION HISTORICA: DE FILTRO DE PAQUETES A NGFW

La seguridad perimetral de redes ha atravesado tres grandes eras:

1. Primera Generacion: Filtros de Paquetes sin Estado (Stateless Packet Filters)
   - Evaluaban cada paquete de forma aislada basandose unicamente en IP origen/destino
     y puerto TCP/UDP (Listas de Control de Acceso - ACLs).
   - Vulnerables a suplantacion de identidad (IP spoofing) y ataques de fragmentacion.

2. Segunda Generacion: Inspeccion con Estado (Stateful Inspection)
   - Popularizada por Cisco ASA y Check Point clasico en los anos 90 y 2000.
   - Mantenian una tabla de estados de conexion (State Table): si el cliente interno
     iniciaba una conexion TCP SYN al puerto 80, el firewall permitia el SYN-ACK de vuelta.
   - PROBLEMA CRITICO: Hoy en dia, mas del 95% del trafico transita por los puertos 80 (HTTP)
     y 443 (HTTPS). Un firewall stateful ve pasar trafico en el puerto 443 y asume que es
     "web segura", cuando en realidad puede ser malware, comando y control (C2),
     aplicaciones peer-to-peer (BitTorrent) o exfiltracion de bases de datos.

3. Tercera Generacion: Firewalls de Proxima Generacion (NGFW - Capa 7)
   - No confian en el numero de puerto. Identifican la APLICACION real (App-ID)
     independientemente del puerto o protocolo utilizado.
   - Integran proteccion contra amenazas en una sola pasada:
     * Prevencion de Intrusiones (IPS / IDS con firmas Snort/Suricata).
     * Antivirus de pasarela y proteccion Anti-Spyware.
     * Desempaquetado y analisis en Sandboxing en la nube (Palo Alto WildFire, FortiSandbox).
     * Descifrado e inspeccion profunda SSL/TLS (Deep Packet Inspection).
     * Integracion con Identidad (User-ID): aplican politicas a "jperez del grupo Contabilidad",
       no a una simple IP anonima.



## 2. ARQUITECTURA DE PROCESAMIENTO: SINGLE-PASS VS MULTI-PASS

A. Arquitectura Multi-Pass (Legada):
   El paquete entra al firewall, es inspeccionado por el motor de enrutamiento,
   luego pasa por el motor NAT, se copia en memoria para el proxy web, pasa por el
   motor IPS, luego por el motor antivirus... Cada motor introduce latencia, copia
   de buferes y caidas severas de throughput.

B. Arquitectura Single-Pass (Palo Alto SP3 / ASICs de Fortinet FortiGate):
   El paquete se decodifica y clasifica UNA SOLA VEZ. Una unica pasada de hardware
   especializado (ASICs NP7/CP9 de red y contenido en Fortinet, o procesadores Single-Pass
   en Palo Alto) evalua App-ID, firmas de amenazas, antivirus y politicas de seguridad
   simultaneamente, manteniendo latencias en microsegundos aun con todas las funciones activas.



## 3. MODELO DE ZONAS DE SEGURIDAD (SECURITY ZONES)

Los NGFW modernos abandonan el concepto de "puertos o interfaces fisicas" para sus
politicas de seguridad. En su lugar, agrupan interfaces en Zonas Logicas de Seguridad:

           [ ZONA OUTSIDE / INTERNET ]
                      ^
                      | (Politica: Permitir SSL, Bloquear amenazas)
                      v
```text
             +-----------------+
             |   NGFW CLUSTER  | <======> [ ZONA DMZ (Servidores Publicos) ]
             +-----------------+
                      ^
                      | (Politica: Denegar acceso directo DMZ -> INSIDE)
                      v
            [ ZONA INSIDE / LAN ]
            [ ZONA USUARIOS VPN ]
            [ ZONA GUEST WIFI   ]
```

REGLAS FUNDAMENTALES DE ZONAS:
- Trafico Intra-Zona (de INSIDE a INSIDE): Permitido por defecto en la mayoria de plataformas.
- Trafico Inter-Zona (de INSIDE a OUTSIDE, o de OUTSIDE a INSIDE): DENEGADO IMPLICITAMENTE
  salvo que exista una politica explicita que lo autorice.



## 4. INDICE DE ARCHIVOS DE LA CARPETA FIREWALLS_NGFW_LIDERES

[00_INDICE_Y_ARQUITECTURA_NGFW.md](./00_INDICE_Y_ARQUITECTURA_NGFW.md)
    - Fundamentos de NGFW, evolucion, Single-Pass, conceptos de Zonas de Seguridad y App-ID.

[01_FORTINET_FORTIGATE_FORTIOS_POLICIES_VDOMS_Y_HA.md](./01_FORTINET_FORTIGATE_FORTIOS_POLICIES_VDOMS_Y_HA.md)
    - Fortinet FortiOS 7.x: Virtual Domains (VDOMs), Politicas de seguridad de proxima generacion,
      VIPs (Virtual IPs), Central NAT, Cluster FGCP (Active-Passive / Active-Active) y SD-WAN.

[02_PALO_ALTO_NETWORKS_PANOS_APPID_USERID_Y_CONTENTID.md](./02_PALO_ALTO_NETWORKS_PANOS_APPID_USERID_Y_CONTENTID.md)
    - Palo Alto Networks PAN-OS: Arquitectura SP3, Security Profiles (Antivirus, Anti-Spyware,
      Vulnerability, WildFire), User-ID con Active Directory y High Availability (HA1/HA2).

[03_SSL_DEEP_INSPECTION_Y_CERTIFICADOS_NGFW.md](./03_SSL_DEEP_INSPECTION_Y_CERTIFICADOS_NGFW.md)
    - Descifrado e inspeccion profunda SSL/TLS: Inbound SSL (servidores internos) vs
      Outbound SSL Forward Proxy (navegacion de usuarios), despliegue de Autoridad Certificadora
      intermedia (CA) corporativa por GPO, manejo de Certificate Pinning y listas de exclusion.

[04_CISCO_SECURE_FIREWALL_FTD_FMC_Y_SNORT3.md](./04_CISCO_SECURE_FIREWALL_FTD_FMC_Y_SNORT3.md)
    - Cisco Secure Firewall (FTD) gestionado por FMC (Firepower Management Center):

## Motor dual (LINA + Snort 3), Access Control Policies (ACP), Prefilter Policies y Site-to-Site VPN.
