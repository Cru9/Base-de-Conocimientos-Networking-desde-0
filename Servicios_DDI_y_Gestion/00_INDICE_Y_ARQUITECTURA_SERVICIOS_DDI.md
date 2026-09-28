# 00. INDICE GENERAL, ARQUITECTURA DDI Y OBSERVABILIDAD DE RED

> **SERVICIOS DE RED CORE (DDI: DNS, DHCP, IPAM) Y GESTION EMPRESARIAL**


---



## 1. ¿QUE ES DDI Y POR QUE ES EL CORAZON DE CUALQUIER INFRAESTRUCTURA IP?

El acronimo DDI agrupa los tres servicios basicos e indispensables que permiten
que cualquier dispositivo se comunique en una red IP moderna:

1. DNS (Domain Name System):
   - Traduce nombres legibles por humanos (ej. erp.corporativo.com) en direcciones IP.
   - Si el DNS falla o sufre latencia, la empresa se paraliza: Active Directory deja
     de autenticar, los correos electronicos no se enrutan y las aplicaciones web
     marcan error aunque los enlaces fisicos esten al 100% de operatividad.

2. DHCP (Dynamic Host Configuration Protocol):
   - Asigna dinamicamente direcciones IP, mascaras de subred, puertas de enlace (Gateways),
     servidores DNS y opciones avanzadas (como Option 150 para telefonos IP Cisco o
     Option 43 para ubicar controladores Wireless WLC).
   - Sin DHCP, miles de estaciones de trabajo, laptops y telefonos quedan sin conectividad.

3. IPAM (IP Address Management):
   - Es el registro centralizado y "Fuente Unica de Verdad" (Single Source of Truth)
     del espacio de direccionamiento IPv4 e IPv6 de la corporacion.
   - Elimina las hojas de calculo Excel desactualizadas, previene conflictos de IPs
     duplicadas y automatiza la asignacion de subredes para nuevas sucursales o nubes.



## 2. INTEGRACION DE SERVICIOS CORE Y OBSERVABILIDAD

Alrededor de DDI operan los servicios de gestion, sincronizacion y telemetria:
- NTP / PTP (Sincronizacion de Tiempo):
  * La correlacion de incidentes de seguridad en un SIEM es imposible si el firewall
    marca las 10:00 y el switch core marca las 10:15.
  * Transacciones bancarias y trading de alta frecuencia exigen precision en
    microsegundos (PTP IEEE 1588v2).
- Telemetria y Monitoreo:
  * SNMPv3 seguro con autenticacion y cifrado (authPriv).
  * Syslog centralizado bajo estandar RFC 5424.
  * Analisis de flujos NetFlow v9 e IPFIX para identificar saturacion de enlaces ("Top Talkers").



## 3. INDICE DE ARCHIVOS DE LA CARPETA SERVICIOS_DDI_Y_GESTION

[00_INDICE_Y_ARQUITECTURA_SERVICIOS_DDI.md](./00_INDICE_Y_ARQUITECTURA_SERVICIOS_DDI.md)
    - Indice general, explicacion del ecosistema DDI y servicios criticos de gestion.

[01_DNS_EMPRESARIAL_ANYCAST_BGP_DNSSEC_Y_SPLIT_HORIZON.md](./01_DNS_EMPRESARIAL_ANYCAST_BGP_DNSSEC_Y_SPLIT_HORIZON.md)
    - Servidores DNS recursivos y autoritativos (BIND9 y Windows Server DNS).
    - Despliegue de Anycast DNS mediante BGP para alta disponibilidad y baja latencia.
    - Split-Horizon DNS (vistas internas vs externas) y validacion DNSSEC.

[02_DHCP_ALTA_DISPONIBILIDAD_FAILOVER_Y_SNOOPING.md](./02_DHCP_ALTA_DISPONIBILIDAD_FAILOVER_Y_SNOOPING.md)
    - Servidores DHCP empresariales en Failover (Active-Active 50/50 y Hot-Standby).
    - Agente Relay DHCP (ip helper-address) y uso de Opciones DHCP (Option 43, 60, 82, 150).
    - Seguridad de capa 2: DHCP Snooping, Dynamic ARP Inspection (DAI) e IP Source Guard.

[03_IPAM_NETBOX_SINGLE_SOURCE_OF_TRUTH.md](./03_IPAM_NETBOX_SINGLE_SOURCE_OF_TRUTH.md)
    - NetBox como plataforma lider de IPAM y modelado de infraestructura de red.
    - Estructura de datos: Sitios, Racks, Dispositivos, Prefijos, Direcciones IP y VLANs.
    - Automatizacion y sincronizacion mediante API REST y libreria Python 'pynetbox'.

[04_NTP_ESTRATOS_AUTENTICACION_Y_PTP_IEEE_1588.md](./04_NTP_ESTRATOS_AUTENTICACION_Y_PTP_IEEE_1588.md)
    - Jerarquia de estratos NTP (Stratum 0, 1, 2). Servidores Chrony y NTPd en Linux.
    - Configuracion de clientes y servidores NTP con llaves de autenticacion en Cisco y Huawei.
    - PTP (Precision Time Protocol - IEEE 1588v2) para redes de ultra baja latencia y telecomunicaciones.

[05_SNMPV3_AUTHPRIV_SYSLOG_RFC5424_Y_NETFLOW_IPFIX.md](./05_SNMPV3_AUTHPRIV_SYSLOG_RFC5424_Y_NETFLOW_IPFIX.md)
    - Monitoreo seguro con SNMPv3 (Autenticacion SHA + Cifrado AES con vistas MIB/OID).
    - Registro centralizado Syslog estructurado (RFC 5424) con Rsyslog y Graylog.

## - Exportacion de telemetria de trafico NetFlow v9 / IPFIX en Cisco IOS-XE y Huawei VRP.
