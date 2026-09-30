# 03. HARDENING, TOPOLOGIAS DE ALTA DISPONIBILIDAD Y FIREWALLS INDUSTRIALES

> **REDES INDUSTRIALES Y CIBERSEGURIDAD OT / SCADA (OPERATIONAL TECHNOLOGY)**


---



## 1. ENDURECIMIENTO DE HARDWARE (CONMUTADORES RUGERIZADOS PARA PLANTA)

Un switch corporativo de oficina colocado en una planta de produccion fallara
en cuestion de semanas debido al calor, polvo metalico, humedad y vibraciones.

Caracteristicas de Conmutadores Industriales (Cisco Catalyst IE, Siemens SCALANCE, Moxa):

### a) Montaje en Carril DIN (DIN-Rail):

   - Formato vertical compacto disenado para instalarse dentro de gabinetes de control
     electrico junto a los PLCs.


### b) Diseno Sin Ventiladores (Fanless):

   - Los ventiladores fallan al aspirar polvo abrasivo, fibras o vapores de aceite.
   - La disipacion termica se realiza por conveccion pasiva a traves de aletas de aluminio macizo.


### c) Barniz de Proteccion Conformada (Conformal Coating):

   - Capa polimerica protectora aplicada sobre la placa de circuito impreso (PCB).
   - Aísla las pistas electronicas de la humedad, hongos y gases corrosivos
     (como acido sulfhidrico H2S en plantas de tratamiento de agua y refinerias).


### d) Rango Extendido de Temperatura:

   - Operacion garantizada entre -40 °C y +75 °C.


### e) Alimentacion Redundante de Corriente Continua (DC):

   - Entradas duales de 12V, 24V o 48V DC para conectarse a bancos de baterias industriales.
   - Contacto de relevador de alarma fisica (Dry Contact) que se cierra ante caidas de energia.



## 2. TOPOLOGIAS DE REDUNDANCIA INDUSTRIAL: CONVERGENCIA EN CERO MILISEGUNDOS

En una linea de ensamblaje robotico, Spanning Tree (RSTP con reconvergencia de 1 a 2 segundos)
es inaceptable: si la red se corta por 1 segundo, los PLCs entran en falla de comunicacion
(Timeout) y disparan un paro de emergencia de la planta.


### a) MRP (Media Redundancy Protocol - Estandar IEC 62439-2):

   - Topologia en anillo de hasta 50 switches conmutados.
   - Un switch maestro (MRM - Media Redundancy Manager) bloquea un extremo del anillo.
   - Tiempo de reconvergencia determinista: < 200 ms (o modo rapido de < 20 ms).


### b) PRP (Parallel Redundancy Protocol - IEC 62439-3 Clausula 4):

   - EL ESTANDAR DE DISPONIBILIDAD MAXIMA PARA SUBESTACIONES ELECTRICAS Y QUIMICAS.
   - Se construyen DOS redes Ethernet fisicamente independientes en paralelo (LAN A y LAN B).
   - Cada sensor o PLC avanzado (DANP - Double Attached Node) envia cada paquete
     duplicado por AMBAS redes al mismo tiempo.
   - El receptor acepta el primer paquete que llega y descarta la copia duplicada.
   - SI UN TRACTOR O INCENDIO CORTA TODOS LOS CABLES DE LA LAN A:
     ¡EL TIEMPO DE RECUPERACION ES EXACTAMENTE DE CERO MILISEGUNDOS (0 ms)!
     No se pierde ni un solo paquete de datos.



## 3. FIREWALLS INDUSTRIALES CON INSPECCION PROFUNDA (DPI - DEEP PACKET INSPECTION)

Un firewall tradicional solo evalua Capa 3 y 4 (IP y Puerto):
  `permit tcp 192.168.1.10 (HMI) to 192.168.1.50 (PLC) port 502 (Modbus)`
PROBLEMA:
Cualquier paquete que vaya al puerto 502 cruzara el firewall, incluyendo comandos
maliciosos para reescribir la memoria del PLC.

EL PODER DE UN FIREWALL INDUSTRIAL CON DPI (FortiGate / Cisco ISA / Palo Alto):
El firewall decodifica la carga util de Modbus, EtherNet/IP o Profinet en tiempo real
y filtra por CODIGOS DE FUNCION y DIRECCIONES DE REGISTRO.


## POLITICA DE PRODUCCION EN FORTIGATE (FORTIOS CON OT SECURITY):

Paso 1: Crear perfil de Inspeccion Industrial para Modbus:
config ips custom
  edit "MODBUS_BLOQUEAR_ESCRITURA"
```text
    set signature "F-SBID( --name \"Modbus.Write.Functions.Block\"; --protocol tcp; --service MODBUS; --flow bi_direction; --pattern \"|05|\"; --context payload; --pattern \"|06|\"; --context payload; --pattern \"|0f|\"; --context payload; --pattern \"|10|\"; --context payload; )"
    set action block
  next
end

Paso 2: Aplicar la politica en el conducto entre la Zona HMI y la Zona PLCs:
config firewall policy
  edit 101
    set name "CONDUCTO-HMI-HACIA-PLCS"
    set srcintf "VLAN_HMI_NIVEL2"
    set dstintf "VLAN_PLCS_NIVEL1"
    set srcaddr "ESTACION_OPERADOR_HMI"
    set dstaddr "GRUPO_PLCS_CALDERA"
    set service "MODBUS"
    set action accept
    set schedule "always"
    ! Habilitar perfil de seguridad industrial
    set utm-status enable
    set ips-sensor "MODBUS_SOLO_LECTURA_PERMITIDA"
  next
end
```

RESULTADO DE SEGURIDAD EN PRODUCCION:
- El operador del HMI puede monitorear temperaturas y presiones (Funciones 03 y 04 de Lectura).
- Si una maquina infectada o un atacante intenta enviar un comando de Escritura (Funciones 05 o 06)
  para apagar una bomba, ¡el firewall industrial descarta el paquete en milisegundos y genera

una alerta de alta prioridad en el SIEM!
