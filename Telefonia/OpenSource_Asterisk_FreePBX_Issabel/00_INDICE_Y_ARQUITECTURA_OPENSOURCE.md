# ASTERISK, FREEPBX E ISSABEL

> **TELEFONIA DE CODIGO ABIERTO (OPEN SOURCE VOIP)**

> *00. INDICE GENERAL, ARQUITECTURA Y EVOLUCION*


---



## 1. LA REVOLUCION DEL CODIGO ABIERTO EN LAS TELECOMUNICACIONES

Historicamente, instalar un conmutador telefonico empresarial requeria pagar decenas
de miles de dolares a fabricantes propietarios (Avaya, Cisco, Nortel, Siemens).
Cada extension, cada puerto y cada canal requeria la compra de costosas licencias.

En 1999, Mark Spencer creo ASTERISK:
- Un software gratuito y de codigo abierto (GPL) para Linux que convierte cualquier
  computadora o servidor estandar en un conmutador telefonico IP de nivel corporativo.
- Sin costo de licencias por extension ni por troncal.
- Soporta millones de llamadas concurrentes en clusters empresariales.
- Hoy en dia, mas del 80% de las centrales telefonicas en la nube y sistemas de
  atencion al cliente del mundo estan construidos sobre el motor de Asterisk.



## 2. EL ECOSISTEMA: ASTERISK vs FREEPBX vs ISSABEL

Muchas personas confunden estos tres terminos. Su relacion es jerarquica:

```text
       +-----------------------------------------------------------------------+
       |               ISSABEL                                                 |
       |  (Distribucion completa Linux CentOS + PBX + Call Center + Fax + Web) |
       +-----------------------------------------------------------------------+
                                          |
                                          v
       +-----------------------------------------------------------------------+
       |               FREEPBX                                                 |
       |  (Interfaz Grafica Web GUI para administrar el conmutador sin tocar  |
       |   lineas de comandos en Linux)                                        |
       +-----------------------------------------------------------------------+
                                          |
                                          v
       +-----------------------------------------------------------------------+
       |               ASTERISK                                                |
       |  (El MOTOR BINARIO subyacente que procesa y conmuta las llamadas      |
       |   en tiempo real)                                                     |
       +-----------------------------------------------------------------------+

a) Asterisk (El Motor / Back-End):
   - Escrito en lenguaje C.
   - Procesa los paquetes RTP, decodifica los codecs de audio (G.711, G.729, Opus),
     gestiona la senalizacion SIP y ejecuta las reglas del Plan de Marcacion (Dialplan).
   - Se administra historicamente mediante archivos de texto plano en `/etc/asterisk/`.

b) FreePBX (La Interfaz Web / GUI):
   - Desarrollado por Sangoma.
   - Interfaz web amigable en PHP/MySQL que genera automaticamente los archivos
     de configuracion de Asterisk.
   - Permite crear extensiones, troncales, IVR y grupos con clics de raton.

c) Issabel (La Plataforma de Comunicaciones Unificadas Completa):
   - La continuacion y fork oficial comunitario del legendario sistema ELASTIX
     (despues de que 3CX adquiriera la marca comercial en 2016).
   - Sistema operativo completo listo para instalar desde una imagen ISO que incluye:
     * Asterisk + FreePBX integrados.
     * Modulo de Call Center con marcador predictivo (Predictive Dialer).
     * Servidor de Fax por IP (HylaFax y AvantFAX).
     * Servidor de Correo Electronico Postfix y Chat XMPP.
     * Firewall y deteccion de intrusos Fail2Ban preconfigurados.
```


## 3. INDICE DE ARCHIVOS DE ESTA BIBLIOTECA

[00_INDICE_Y_ARQUITECTURA_OPENSOURCE.md](./00_INDICE_Y_ARQUITECTURA_OPENSOURCE.md)
    - Origen del open source en VoIP, ecosistema Asterisk vs FreePBX vs Issabel.

[01_ASTERISK_MOTOR_CORE_Y_DIALPLAN.md](./01_ASTERISK_MOTOR_CORE_Y_DIALPLAN.md)
    - El motor interno de Asterisk: canales chan_sip vs chan_pjsip, la estructura del
      Dialplan (extensions.conf), contextos, prioridades, aplicaciones y CLI.

[02_FREEPBX_E_ISSABEL_GUI_Y_MODULOS.md](./02_FREEPBX_E_ISSABEL_GUI_Y_MODULOS.md)
    - Arquitectura grafica, modulos esenciales: Extensiones, Troncales, Rutas Entrantes,
      Rutas Salientes, IVR, Ring Groups, Queues (Colas de atencion) y Time Conditions.

[03_INSTALACION_Y_LABORATORIO_VIRTUAL.md](./03_INSTALACION_Y_LABORATORIO_VIRTUAL.md)
    - Como desplegar un conmutador gratuito de laboratorio en VMware Workstation,
      VirtualBox o Proxmox paso a paso (particionamiento, red en puente y acceso web).

[04_CONFIGURACION_PRACTICA_PJSIP_TRONCALES_E_IVR.md](./04_CONFIGURACION_PRACTICA_PJSIP_TRONCALES_E_IVR.md)
    - Taller practico: Creacion de extensiones PJSIP, registro de softphones (MicroSIP/Zoiper),
      conexion de troncal SIP de pruebas, construccion de un IVR y desvios dia/noche.

[05_SEGURIDAD_FAIL2BAN_Y_TROUBLESHOOTING.md](./05_SEGURIDAD_FAIL2BAN_Y_TROUBLESHOOTING.md)
    - Hardening de conmutadores de codigo abierto: Bloqueo de ataques de fuerza bruta con

## Fail2Ban, cambio de puertos SIP, desactivacion de llamadas de invitados y comandos CLI.
