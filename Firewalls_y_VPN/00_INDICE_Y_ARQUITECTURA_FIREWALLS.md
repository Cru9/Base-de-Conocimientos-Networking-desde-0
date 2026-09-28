# 00. INDICE GENERAL, ARQUITECTURA DE CORTAFUEGOS Y ZONAS DE SEGURIDAD

> **FIREWALLS DE PROXIMA GENERACION (NGFW) Y VPNs EMPRESARIALES**


---



## 1. EVOLUCION DE LOS FIREWALLS: DE CAPA 4 A PROXIMA GENERACION (NGFW)


### a) Firewalls de Filtro de Paquetes (Stateless - Primera Generacion):

   - Inspeccionan cada paquete de forma aislada segun una ACL simple (IP y puerto).
   - No tienen memoria: No saben si un paquete es una respuesta valida o un ataque.


### b) Firewalls de Inspeccion de Estado (Stateful - Segunda Generacion):

   - Mantienen una tabla de sesiones (State Table). Si el cliente inicio la conexion,
     el firewall permite la respuesta automaticamente.
   - Limitacion: Ciegos al trafico de Capa 7. Si un atacante inyecta malware sobre
     el puerto 443 (HTTPS), el firewall lo deja pasar porque "el puerto 443 es legal".


### c) Firewalls de Proxima Generacion (NGFW - Estandar Actual):

   - Trascienden los puertos y direcciones IP. Inspeccionan la APLICACION real
     (App-ID / Deep Packet Inspection - DPI), el USUARIO (User-ID) y el CONTENIDO (Content-ID).
   - Un NGFW sabe distinguir si el trafico que viaja por el puerto 443 es navegacion
     bancaria legitima, transferencia de archivos por BitTorrent o una llamada de Zoom,
     y puede bloquear la aplicacion independientemente del puerto que utilice.
   - Motores integrados: IPS (Intrusion Prevention System), Antivirus en tiempo real,
     Filtrado Web por reputacion, Sandbox antimalware en la nube e Inspeccion SSL/TLS.



## 2. ARQUITECTURA BASADA EN ZONAS DE SEGURIDAD (SECURITY ZONES)

Los NGFWs modernos no aplican politicas a "puertos fisicos", sino a ZONAS LOGICAS.
Una Zona de Seguridad es un contenedor logico que agrupa una o mas interfaces:


## Zonas Tipicas Empresariales:


| Zona | Nivel Confianza | Descripcion y Funcion |
| :--- | :--- | :--- |
| TRUST (LAN) | Alto (100) | Red interna de computadoras de empleados y corporativo. |
| DMZ | Medio (50) | Zona Desmilitarizada: Servidores web, correo y VPNs |

                                  accesibles desde Internet (si un servidor es hackeado,
                                  la DMZ impide que el atacante salte a la zona TRUST).
UNTRUST (WAN)   Cero (0)          Internet publico y redes externas desconocidas.
GUEST (Wi-Fi)   Muy Bajo (10)     Red inalambrica de visitas aislada de los recursos internos.
MGMT            Critico (100)     Red exclusiva para la administracion de los equipos de TI.

La Regla de Oro del Cortafuegos (Default Deny):
- Trafico Intra-Zona (dentro de la misma zona): Permitido por defecto en varios sistemas.
- Trafico Inter-Zona (entre diferentes zonas): BLOQUEADO POR DEFECTO (Implicit Deny).
  Todo trafico entre zonas debe ser explicitamente autorizado por una Politica de Seguridad.



## 3. INDICE DE ARCHIVOS DE LA CARPETA FIREWALLS_Y_VPN

[00_INDICE_Y_ARQUITECTURA_FIREWALLS.md](./00_INDICE_Y_ARQUITECTURA_FIREWALLS.md)
    - Arquitectura NGFW, comparativa generacional y diseno de zonas de seguridad.

[01_POLITICAS_DE_SEGURIDAD_NAT_Y_PAT.md](./01_POLITICAS_DE_SEGURIDAD_NAT_Y_PAT.md)
    - Politicas de seguridad NGFW, tipos de NAT (Estatico, Dinamico, PAT / Overload,
      Destination NAT para servidores DMZ) y Descifrado SSL/TLS (Forward Proxy).

[02_VPN_IPSEC_SITE_TO_SITE_AVANZADO.md](./02_VPN_IPSEC_SITE_TO_SITE_AVANZADO.md)
    - Tuneles IPsec entre corporativos y sucursales: Protocolo IKEv1 vs IKEv2,
      Fase 1 (IKE SA), Fase 2 (IPsec SA), perfiles criptograficos AES-GCM,
      tuneles basados en rutas (VTI) y deteccion DPD.

[03_DMVPN_DYNAMIC_MULTIPOINT_VPN.md](./03_DMVPN_DYNAMIC_MULTIPOINT_VPN.md)
    - Redes privadas virtuales multipunto de Cisco: Protocolos mGRE y NHRP,
      Fases 1, 2 y 3 (comunicacion directa Spoke-to-Spoke sin cruzar el Hub).

[04_VPN_ACCESO_REMOTO_SSL_Y_WIREGUARD.md](./04_VPN_ACCESO_REMOTO_SSL_Y_WIREGUARD.md)
    - VPNs para teletrabajo: SSL VPN de portal vs tunel completo, comparativa con
      el nuevo protocolo ultrarrapido WireGuard, y autenticacion MFA (SAML / Duo).

[05_CONFIGURACIONES_PRACTICAS_FIREWALLS.md](./05_CONFIGURACIONES_PRACTICAS_FIREWALLS.md)
    - Laboratorio practico de configuracion con comandos reales para Fortinet FortiOS,

## Palo Alto Networks (PAN-OS) y Cisco ASA / Firepower.
