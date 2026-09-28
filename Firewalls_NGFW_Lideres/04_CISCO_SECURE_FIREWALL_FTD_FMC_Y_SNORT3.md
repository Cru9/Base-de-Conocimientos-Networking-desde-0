# 04. CISCO SECURE FIREWALL (FTD), FMC Y MOTOR SNORT 3

> **FIREWALLS DE PROXIMA GENERACION (NGFW) POR MARCA LIDER**


---



## 1. EVOLUCION Y ARQUITECTURA DE CISCO SECURE FIREWALL (FTD)

La plataforma NGFW de Cisco (Cisco Secure Firewall, anteriormente Firepower Threat
Defense - FTD) unifico el legendario motor de firewalling Cisco ASA con la potencia
del sistema de prevencion de intrusiones Snort.

ARQUITECTURA INTERNA DE PROCESAMIENTO (DUAL-ENGINE):

           [ PAQUETE DE RED ENTRANTE ]
                       |
                       v
```text
     +-----------------------------------+
     |        LINA ENGINE (Capa 3/4)     | <--- Nucleo de enrutamiento y estado ASA
     | - Enrutamiento IP / BGP / OSPF    |
     | - Traduccion NAT / PAT            |
     | - Terminacion de VPNs AnyConnect  |
     | - Prefilter Policy (Fastpath)     |
     +-----------------------------------+
                       |
       (Copia a traves de DAQ / Shared Memory)
                       |
                       v
     +-----------------------------------+
     |        SNORT 3 ENGINE (Capa 7)    | <--- Motor de inspeccion avanzada de amenazas
     | - Arquitectura Multi-Threaded     |
     | - OpenAppID (Clasificacion L7)    |
     | - Reglas IPS / Prevencion Exploits|
     | - Analisis de Archivos y Malware  |
     | - Cisco Talos Intelligence Feeds  |
     +-----------------------------------+
```


## 2. PLATAFORMAS DE GESTION: FMC VS FDM

- FMC (Firepower Management Center):
  Appliance dedicado (FMC 1600, 2600, 4600 o maquina virtual en VMware/KVM/AWS/Azure).
  Es la plataforma corporativa estandar: gestiona cientos de appliances FTD, centraliza
  reportes, distribuye politicas de acceso, coordina actualizaciones de firmas Talos
  y se integra con Cisco ISE a traves de pxGrid.

- FDM (Firepower Device Manager):
  Interfaz web local integrada en la propia caja del firewall. Disenada para sucursales
  aisladas o empresas pequenas que tienen 1 o 2 firewalls y no requieren FMC central.



## 3. ESTRUCTURA JERARQUICA DE POLITICAS EN FMC (ACCESS CONTROL POLICY)

Al evaluar una conexion, el FMC procesa las politicas en este orden estricto:

1. Prefilter Policy:
   - Permite clasificar trafico simple en Capa 3/Capa 4.
   - Accion FASTPATH: Envía directamente el trafico de respaldos de servidores o backups
     de bases de datos sin enviarlo a Snort 3, ahorrando hasta un 70% de consumo de CPU.

2. Security Intelligence (SI):
   - Primera linea de defensa alimentada por Cisco Talos en tiempo real.
   - Descarta paquetes automaticamente si la IP, dominio o URL pertenece a una lista
     negra global de botnets, spam o servidores de ataque, antes de evaluar las reglas ACP.

3. Access Control Policy (Reglas de Acceso Capa 7):
   - Reglas con condiciones: Zonas Origen/Destino, Redes, Usuarios de Active Directory,
     Aplicaciones detectadas por OpenAppID, Puertos.
   - Inspeccion IPS asociada (Snort 3):
     * "Balanced Security and Connectivity" (Perfil recomendado por Cisco).
     * "Security Over Connectivity" (Maxima proteccion para zonas criticas).
   - Politica de Archivos y Malware (AMP - Advanced Malware Protection):
     * Inspecciona hashes SHA-256 de ejecutables descargados y bloquea malware.



## 4. CONFIGURACION DE FTD MEDIANTE CLI DE DIAGNOSTICO

Aunque la configuracion de politicas se realiza desde el FMC, el ingeniero de redes
debe dominar la consola CLI para diagnostico y validacion en vivo:

Acceder al motor Lina (clasico ASA):
> system support diagnostic-cli
Attaching to Diagnostic CLI ...
Firepower-01#

1. Ver interfaces y asignacion de zonas:
```text
   show interface ip brief
   show nameif

2. Ver politicas y traducciones NAT activas:
   show nat
   show xlate count

3. Ver conexiones TCP/UDP activas en la tabla de estados:
   show conn address 10.10.20.105
   show conn count

4. Herramienta de simulacion de paquetes (Packet Tracer):
   La herramienta mas poderosa de diagnostico en Cisco FTD. Simula el paso de un
   paquete por todas las etapas (Lina, Prefilter, SI, ACP, NAT, Snort, Routing)
   y te dice con exactitud si pasa o en que regla se descarta:

   packet-tracer input INSIDE tcp 10.10.20.105 54120 8.8.8.8 443 detailed

   Salida esperada al final del analisis:
   Phase: 12 (ACCESS-LIST)
   Action: ALLOW
   Result:
   input-interface: INSIDE
   input-status: up
   output-interface: OUTSIDE
   output-status: up
   Action: allow
```


## 5. MONITOREO Y DEPURACION EN TIEMPO REAL (SNORT Y TALOS)

1. Monitoreo en vivo de eventos Snort en consola:
   system support firewall-engine-debug
   ! Permite filtrar por IP origen, destino y puerto para ver la clasificacion L7.

2. Verificar estado de la sincronizacion con Cisco Talos:
```text
   show threat-detection
   show version

3. Comprobar la comunicacion entre el sensor FTD y el servidor central FMC:
   ssp sftunnel status
```


## ! Debe mostrar: "Connected to FMC at 10.10.1.100 (Port 8305 Encrypted)"
