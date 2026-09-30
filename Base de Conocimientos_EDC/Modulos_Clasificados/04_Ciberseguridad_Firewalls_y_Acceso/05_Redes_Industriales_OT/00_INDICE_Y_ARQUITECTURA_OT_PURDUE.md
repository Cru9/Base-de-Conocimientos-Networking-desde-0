# 00. INDICE GENERAL, EL CHOQUE IT vs OT Y EL MODELO PURDUE (ISA-95)

> **REDES INDUSTRIALES Y CIBERSEGURIDAD OT / SCADA (OPERATIONAL TECHNOLOGY)**


---



## 1. EL CHOQUE CULTURAL ENTRE IT (OFICINA) Y OT (INDUSTRIA)

Las redes corporativas de oficina (IT - Information Technology) y las redes de
plantas de fabricacion, centrales electricas, oleoductos y refinerias (OT - Operational
Technology) operan bajo filosofias radicalmente opuestas:


| Caracteristica | Redes IT (Corporativas) | Redes OT (Industriales / SCADA) |
| :--- | :--- | :--- |
| Triada Primaria | C - I - A | A - I - C |
| (Confidencialidad > Integridad | (DISPONIBILIDAD > Integridad |  |
| > Disponibilidad) | > Confidencialidad) |  |
| Impacto de Falla | Perdida financiera o de datos | DAÑO FISICO, EXPLOSION, IMPACTO |

                                                      AMBIENTAL O PERDIDA DE VIDAS HUMANAS
Tolerancia a Paros   Reinicio en ventanas nocturnas   OPERACION CONTINUA 24/7/365 (Un paro
                                                      no planificado cuesta millones)
Ciclo de Vida        Equipos renovados cada 3-5 anos  Maquinaria y PLCs con vida de 15 a 30 anos
Sistemas Operativos  Windows 11, Linux, parches al dia Windows XP/7/10 embebido, VxWorks, QNX
Protocolos           TCP/IP, HTTPS, SSH, DNS, TLS     Modbus, Profinet, EtherNet/IP, DNP3
                                                      (Historicamente sin cifrado ni clave)

## Determinismo         "Best Effort" (milisegundos)     TIEMPO REAL ESTRICTO (< 1 a 10 ms)




## 2. EL MODELO PURDUE (PERA / ISA-95): LA ARQUITECTURA DE SEGURIDAD

Para evitar que una infeccion de ransomware en la red corporativa de oficina apague
los hornos o bombas de una refineria, la industria utiliza la arquitectura jerarquica
del Modelo Purdue (dividido en 6 niveles estrictos):

   [NIVEL 5: NUBE PUBLICA / INTERNET]
                     |
```text
   +=======================================================================+
   | NIVEL 4: RED CORPORATIVA DE LA EMPRESA (IT ENTERPRISE)                |
   | - Servidores ERP (SAP), Correo Office 365, PCs de Oficina, Wi-Fi Corp.|
   +=======================================================================+
                     |
   +-----------------------------------------------------------------------+
   | NIVEL 3.5: DMZ INDUSTRIAL (iDMZ) - AISLAMIENTO TOTAL                  |
   | - Servidores Jump Host (Bastion RDP con MFA), Proxies, Servidor       |
   |   Historian Replicado, Antivirus WSUS/Patching exclusivo para planta. |
   | * REGLA DE ORO: ¡NINGUN TRAFICO PUEDE CRUZAR DIRECTAMENTE DE IT A OT! |
   +-----------------------------------------------------------------------+
                     |
   +=======================================================================+
   | NIVEL 3: OPERACIONES DE MANUFACTURA Y SITIO (SITE MANUFACTURING)      |
   | - Servidor Historian Primario (base de datos de series de tiempo).    |
   | - Sistemas MES (Manufacturing Execution Systems).                     |
   | - Dominio Active Directory exclusivo de la Planta OT.                 |
   +=======================================================================+
                     |
   +=======================================================================+
   | NIVEL 2: CONTROL SUPERVISORIO DE AREA (SUPERVISORY CONTROL)           |
   | - Estaciones de Trabajo HMI (Human-Machine Interface).                |
   | - Servidores SCADA locales y Estaciones de Ingenieria (EWS).          |
   +=======================================================================+
                     |
   +=======================================================================+
   | NIVEL 1: CONTROL BASICO Y AUTOMATISMOS (BASIC CONTROL)                |
   | - PLCs (Programmable Logic Controllers - Siemens S7, Rockwell AB).   |
   | - PACs, RTUs (Remote Terminal Units) y Relevadores de Proteccion IED. |
   | - Lazos de control PID en tiempo real (milisegundos).                 |
   +=======================================================================+
                     |
   +=======================================================================+
   | NIVEL 0: PROCESO FISICO DE CAMPO (FIELD PROCESS)                      |
   | - Sensores de temperatura, presion, flujo, actuadores, bombas,        |
   |   valvulas neumaticas, brazos roboticos y motores electricos.         |
   +=======================================================================+
```


## 3. REGLAS FUNDAMENTALES DE LA DMZ INDUSTRIAL (iDMZ NIVEL 3.5)

1. Ninguna comunicacion de Capa 2 (VLANs) puede extenderse entre la red IT y la red OT.
2. Todo acceso de soporte remoto desde la red corporativa o Internet DEBE terminar
   en un servidor Jump Host (Bastion) dentro de la iDMZ con autenticacion multifactor (MFA).
3. Las bases de datos Historian se configuran en espejo unidireccional: el Historian
   del Nivel 3 envia datos hacia el Historian de la iDMZ; los usuarios de IT consultan
   unicamente la copia de la iDMZ sin tocar jamas la planta de produccion.



## 4. INDICE DE ARCHIVOS DE LA CARPETA REDES_INDUSTRIALES_OT

[00_INDICE_Y_ARQUITECTURA_OT_PURDUE.md](./00_INDICE_Y_ARQUITECTURA_OT_PURDUE.md)
    - El choque cultural IT vs OT, triada AIC, el Modelo Purdue (Niveles 0 al 5) y la iDMZ.

[01_PROTOCOLOS_INDUSTRIALES_SCADA_Y_PLC.md](./01_PROTOCOLOS_INDUSTRIALES_SCADA_Y_PLC.md)
    - Analisis profundo de protocolos: Modbus RTU vs TCP (puerto 502), Profinet RT/IRT,
      EtherNet/IP (CIP puerto 44818), DNP3 y protocolos modernos MQTT y OPC UA.

[02_CIBERSEGURIDAD_INDUSTRIAL_ISA_IEC_62443.md](./02_CIBERSEGURIDAD_INDUSTRIAL_ISA_IEC_62443.md)
    - Estandar ISA/IEC 62443, niveles de seguridad (SL 1 a 4), zonas y conductos,
      y lecciones forenses de ciberataques historicos (Stuxnet, Industroyer, Triton).

[03_HARDENING_Y_CONFIGURACION_REDES_OT.md](./03_HARDENING_Y_CONFIGURACION_REDES_OT.md)
    - Switches rugerizados para carril DIN, protocolos de redundancia en anillo

## (MRP, PRP, HSR con cero ms de convergencia) y reglas de firewall industrial con DPI.
