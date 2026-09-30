# 02. CIBERSEGURIDAD INDUSTRIAL: NORMA ISA/IEC 62443 Y CASOS HISTORICOS

> **REDES INDUSTRIALES Y CIBERSEGURIDAD OT / SCADA (OPERATIONAL TECHNOLOGY)**


---



## 1. LA NORMA INTERNACIONAL ISA/IEC 62443

La norma ISA/IEC 62443 es el marco global de ciberseguridad obligatorio para Sistemas
de Control y Automatizacion Industrial (IACS - Industrial Automation and Control Systems).

Estructura de la Familia de Normas:
- Nivel 1 (General - 62443-1-x): Conceptos, modelos y terminologia basica.
- Nivel 2 (Politicas y Personas - 62443-2-x): Gestion de parches OT y respuesta a incidentes.
- Nivel 3 (Sistema - 62443-3-x): Requisitos tecnicos de seguridad y diseno de zonas.
  * IEC 62443-3-2: Evaluacion de riesgos y definicion de "Zonas y Conductos".
  * IEC 62443-3-3: Requisitos de seguridad del sistema y Niveles de Seguridad (SL).
- Nivel 4 (Componentes - 62443-4-x): Requisitos para fabricantes de PLCs y switches
  (desarrollo seguro del firmware y silicio).



## 2. NIVELES DE SEGURIDAD (SECURITY LEVELS - SL)

La norma define 4 niveles de capacidad defensiva segun el perfil del atacante:


| Nivel (SL) | Perfil del Atacante | Capacidad y Recursos del Adversario |
| :--- | :--- | :--- |
| SL 1 | Errores Casuales / Accidentales | Sin motivacion. Empleado que comete un error, |

                                               conecta un cable equivocado o introduce virus comun.
SL 2         Atacante Oportunista              Motivacion simple. Recursos bajos y conocimientos
                                               genericos de hacking comercial.
SL 3         Cibercriminal Especializado / Hacktivista Recursos moderados y conocimientos
                                               profundos de PLCs, SCADA y redes industriales.
SL 4         Ciberterrorismo / Estado-Nacion   Recursos financieros ilimitados, agencias de

## (Nation-State Actors)             inteligencia militar y exploits Zero-Day fisicos.




## 3. METODOLOGIA DE ZONAS Y CONDUCTOS (ZONES & CONDUITS)

En lugar de una red plana donde cualquier dispositivo puede hablar con cualquier PLC,
la norma IEC 62443-3-2 exige compartimentar la planta industrial:

```text
  +-----------------------+                         +-----------------------+
  |    ZONA 1: CALDERAS   |                         |  ZONA 2: EMBOTELLADO  |
  | (PLCs, Sensores, HMIs)|                         | (PLCs, Sensores, HMIs)|
  +-----------+-----------+                         +-----------+-----------+
              |                                                 |
              |             =======================             |
              +-----------> # CONDUCTO DE SEGURIDAD # <---------+
```


## # (Firewall Industrial) #

                                       |
                                       v
```text
                            +-----------------------+
                            |    ZONA 3: SCADA/MES  |
                            | (Servidores Nivel 3)  |
                            +-----------------------+

a) Zona (Zone):
   - Una agrupacion logica o fisica de activos industriales que comparten el mismo
     nivel de criticidad y los mismos requisitos de seguridad (Security Level).
   - Ejemplo: La Zona de Turbinas de Vapor (SL 3) se separa de la Zona de Empaque (SL 1).

b) Conducto (Conduit):
   - El canal de comunicacion fisico o logico que interconecta dos o mas zonas.
```

   - REGLA DE ORO: ¡TODO trafico entre zonas debe pasar obligatoriamente a traves
     de un conducto!
   - El conducto debe implementar controles estrictos: Firewall industrial con
     Inspeccion Profunda de Paquetes (DPI), Diodos de Datos Unidireccionales o VPNs cifradas.



## 4. LECCIONES FORENSES DE CIBERATAQUES INDUSTRIALES REALES


## CASO 1: STUXNET (2010 - PLANTA NUCLEAR DE NATANZ, IRAN)

- El primer ciberarma fisica militar de la historia.
- Vector de Entrada: Memoria USB infectada que salto el aislamiento fisico (Air-Gap)
  aprovechando vulnerabilidades Zero-Day de Windows (CVE-2010-2568 LNK).
- Mecanismo de Ataque:
  * Infeccion del software de ingenieria Siemens SIMATIC Step 7.
  * Sustitucion de la libreria `s7otbxdx.dll` (Ataque Man-in-the-Middle en el PLC).
  * Modificacion silenciosa del codigo en el PLC Siemens S7-300 / S7-400 para alterar
    la frecuencia de giro de las centrifugadoras de enriquecimiento de uranio
    (acelerandolas a 1410 Hz y frenandolas a 2 Hz), destruyendolas fisicamente por fatiga mecanica.
- Camuflaje Forense:
  * Mientras rompia los rotores, Stuxnet grababa telemetria de sensores de presion
    normales y la reproducia en bucle en las pantallas HMI de los operadores humanos.


## CASO 2: INDUSTROYER / CRASHOVERRIDE (2016 - RED ELECTRICA DE UCRANIA)

- Primer malware disenado especificamente para hablar protocolos electricos nativos
  (IEC 60870-5-104, IEC 61850 y OPC DA).
- Impacto:
  * Tomo el control directo de las Unidades Terminales Remotas (RTU).
  * Emitio secuencias legitimate de comandos para abrir interruptores de potencia
    de alta tension, dejando a mas de 225,000 ciudadanos sin electricidad en pleno invierno.
- Leccion: El malware no requirio explotar fallas de software; utilizo la falta de
  autenticacion y cifrado inherente del protocolo IEC 104.


## CASO 3: TRITON / TRISIS (2017 - REFINERIA PETROQUIMICA DE ARABIA SAUDITA)

- Objetivo: El Sistema Instrumentado de Seguridad (SIS - Schneider Electric Triconex).
- Los sistemas SIS son la ultima linea de defensa fisica: si la presion o calor
  se descontrolan, el SIS apaga la planta de emergencia para evitar una explosion.
- Impacto del Ataque:
  * Los atacantes reprogramaron la memoria del controlador SIS para deshabilitar
    los disparadores de seguridad.
  * Intencion: El objetivo no era espiar ni pedir rescate (Ransomware); el objetivo
    era provocar un desastre catastrófico con perdida de vidas humanas.
  * La planta se salvo debido a que un error de programacion en el codigo del malware

disparo una falla de memoria en el PLC, forzando un apagado seguro no previsto.
