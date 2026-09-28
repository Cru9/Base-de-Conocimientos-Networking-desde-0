# 03. REDES DE ALMACENAMIENTO: SAN, NAS, FIBRE CHANNEL Y RoCEv2

> **REDES DE CENTROS DE DATOS (DATA CENTER & CLOUD NETWORKING)**


---



## 1. PARADIGMAS DE ALMACENAMIENTO EMPRESARIAL

En centros de datos modernos, el almacenamiento se clasifica en 3 arquitecturas:


### a) Almacenamiento por Bloques (Block Storage - SAN):

   - El almacenamiento se presenta al servidor como si fuera un disco duro fisico
     local (LUN - Logical Unit Number) sobre el cual el sistema operativo formatea
     su propio sistema de archivos (NTFS, EXT4, VMFS de VMware).
   - Protocolos: Fibre Channel (FC), FCoE, iSCSI, NVMe-oF.
   - Casos de Uso: Bases de Datos de alto rendimiento (Oracle RAC, SQL Server),
     Hipervisores VMware ESXi / Hyper-V / Proxmox.


### b) Almacenamiento por Archivos (File Storage - NAS):

   - El servidor de almacenamiento gestiona el sistema de archivos y expone carpetas
     compartidas a traves de la red.
   - Protocolos: NFS v3 / v4 (Linux/Unix), SMB 3.0 / CIFS (Windows).
   - Casos de Uso: Repositorios de archivos compartidos, copias de seguridad (Backups).


### c) Almacenamiento por Objetos (Object Storage):

   - Almacenamiento no estructurado accesible mediante llamadas API HTTP REST.
   - Protocolos: Amazon S3 API, Ceph, MinIO.
   - Casos de Uso: Big Data, Data Lakes, archivos multimedia y backups inmutables.



## 2. FIBRE CHANNEL (FC): LA RED SAN DEDICADA DE MISION CRITICA

Fibre Channel es una arquitectura de red dedicada, totalmente independiente de Ethernet,
disenada con un solo proposito: transmitir comandos SCSI/NVMe con CERO perdida de
paquetes y latencia ultra-baja.


### a) Componentes de una SAN Fibre Channel:

   - HBA (Host Bus Adapter): Tarjeta PCIe especializada instalada en el servidor (QLogic / Emulex).
   - Conmutadores SAN (Fibre Channel Switches): Brocade (Broadcom) o Cisco MDS 9000.
   - Cabinas de Almacenamiento (Storage Arrays): NetApp, Dell PowerStore, Pure Storage, HPE Primera.


### b) Identificadores y Direccionamiento:

   - WWN (World Wide Name): Direccion global unica de 64 bits (hexadecimal):
     * WWNN (Node Name): Identifica el nodo fisico o cabina.
     * WWPN (Port Name): Identifica el puerto especifico del HBA (ej. 21:00:00:24:ff:45:12:a0).
   - FCID (Fibre Channel ID): Direccion de Capa 3 dinamica de 24 bits asignada por
     el switch durante el inicio de sesion (Fabric Login):
```text
     [ Domain ID (8 bits) | Area ID (8 bits) | Port ID (8 bits) ]

c) Secuencia de Registro en el Fabric:
   1. FLOGI (Fabric Login): El HBA del servidor se autentica contra el switch FC y
      recibe su FCID.
   2. PLOGI (Port Login): El HBA contacta al puerto de la cabina de discos.
   3. PRLI (Process Login): Se negocia el protocolo SCSI a nivel de canal.

d) Zonificacion (Zoning):
   Mecanismo de seguridad fundamental en SAN. Impide que servidores no autorizados
   vean los discos de otros servidores.
   - Hard Zoning: Zonificacion por numero de puerto fisico del switch FC.
   - Soft Zoning (Recomendado por la industria): Zonificacion por WWPN. Permite
     mover el cable de puerto sin romper la conexion de almacenamiento.
   - Regla de Oro: Single-Initiator / Single-Target Zoning (una zona debe contener
     unicamente un puerto de servidor y un puerto de storage para evitar tormentas RSCN).

e) VSAN (Virtual Storage Area Network - Cisco):
   Equivalente exacto a una VLAN de Ethernet pero dentro de la red Fibre Channel.
   Aisla completamente dominios de conmutacion, servidores y tablas de nombres.
```


## 3. FCoE (FIBRE CHANNEL OVER ETHERNET) Y LOSSLESS ETHERNET

Para evitar tener que tender cables dobles (cables Ethernet para datos y cables
Fibre Channel para almacenamiento), la industria desarrollo FCoE (EtherType 0x8906).

El Gran Desafio:
- Fibre Channel exige "Lossless" (CERO PERDIDA DE PAQUETES).
- Ethernet tradicional es "Best Effort" (descarta paquetes cuando hay congestion).

La Solucion: DCB (Data Center Bridging):
1. PFC (Priority-based Flow Control - IEEE 802.1Qbb):
   En Ethernet clasico, la trama PAUSE (802.3x) congela TODO el trafico del enlace.
   Con PFC, la pausa se aplica de forma selectiva a un nivel de prioridad CoS
   especifico (ej. CoS 3 para almacenamiento), permitiendo que el trafico web
   o SSH siga fluyendo sin detenerse.
2. ETS (Enhanced Transmission Selection - IEEE 802.1Qaz):
   Garantiza un ancho de banda minimo reservado para almacenamiento (ej. 50% para SAN,
   50% para trafico de datos del sistema operativo).



## 4. iSCSI (INTERNET SMALL COMPUTER SYSTEMS INTERFACE)

Transporta bloques SCSI estandar encapsulados en paquetes TCP/IP ordinarios sobre
puerto TCP 3260.

- Identificador IQN (iSCSI Qualified Name):
  Formato: iqn.yyyy-mm.reverse-domain:unique-name
  Ejemplo: `iqn.1998-01.com.vmware:esxi-host-rack01-4a2b1c`
- Componentes:
  * Initiator: El cliente (Servidor o Hipervisor ESXi que solicita disco).
  * Target: El servidor de almacenamiento o LUN que expone el disco.
  * Autenticacion CHAP (Challenge Handshake Authentication Protocol) mutua.



## 5. LA REVOLUCION DEL ALMACENAMIENTO DE ALTA VELOCIDAD: NVMe-oF Y RoCEv2

Los discos SSD NVMe modernos alcanzan millones de IOPS y latencias de microsegundos,
superando la capacidad de procesamiento de las capas TCP del sistema operativo.

RDMA (Remote Direct Memory Access):
Tecnologia que permite a la tarjeta de red de un servidor escribir y leer DIRECTAMENTE
en la memoria RAM de otro servidor sin involucrar a la CPU ni al Kernel del Sistema
Operativo.

RoCEv2 (RDMA over Converged Ethernet v2):
- Encapsula RDMA sobre paquetes UDP (Puerto UDP 4791).
- Es el estandar indiscutible en la actualidad para:
  1. Redes de Almacenamiento NVMe-oF (Non-Volatile Memory Express over Fabrics).
  2. Redes de Interconexion de GPUs para Inteligencia Artificial (NVIDIA GPUDirect
     RDMA en servidores de entrenamiento LLM con clusters H100 / Blackwell).
- Requisitos estrictos de red en conmutadores Leaf:
  * PFC (Priority Flow Control) habilitado.
  * ECN (Explicit Congestion Notification - RFC 3168) habilitado con WRED para marcar

paquetes con bits CE antes de que los buffers de los conmutadores se llenen.
