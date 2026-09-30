# 02. SEGURIDAD EN LA CAPA 2 (ENLACE DE DATOS) - AMENAZAS, DEFENSAS Y CASO REAL

> **CIBERSEGURIDAD EN EL MODELO OSI - GUIA PRACTICA Y CASOS DE LA VIDA REAL**


---



## 1. PANORAMA DE SEGURIDAD EN LA CAPA DE ENLACE DE DATOS

La Capa 2 representa el "perimetro blando" de las redes corporativas. Por decadas,
las organizaciones asumieron que "quien esta conectado al cable de red dentro del
edificio es de confianza".

La realidad es que un atacante conectado a un puerto de red en una sala de juntas,
o una maquina infectada con malware dentro de la oficina, puede comprometer a toda
la empresa en cuestion de minutos si los switches carecen de blindaje en Capa 2.

Vulnerabilidad inherente de Capa 2:
Los protocolos tradicionales de Capa 2 (Ethernet, ARP, DHCP, STP) fueron creados
sin ningun mecanismo de autenticacion ni validacion de identidad: confian ciegamente
en cualquier trama que reciben.



## 2. VECTORES DE ATAQUE EN CAPA 2


### a) Envenenamiento de Tablas ARP (ARP Spoofing / ARP Poisoning - Man-in-the-Middle):

   - El atacante envia paquetes ARP falsos (Gratuitous ARP) a la victima y al Gateway:
     * A la victima le dice: "Yo soy la IP 192.168.1.1 (Gateway), mi MAC es la mía".
     * Al Gateway le dice: "Yo soy la IP 192.168.1.50 (Victima), mi MAC es la mía".
   - Consecuencia: Todo el trafico entre la victima e Internet pasa primero por la
     computadora del atacante, quien puede espiar credenciales, inyectar malware
     o modificar datos en tiempo real (Ataque Man-in-the-Middle).


### b) Desbordamiento de la Tabla CAM (CAM Table Flooding):

   - Un atacante ejecuta herramientas como `macof` generando hasta 150,000 direcciones
     MAC falsas por segundo hacia el puerto del switch.
   - La memoria de la tabla CAM del switch se llena hasta agotarse.
   - Consecuencia (Fail-Open): Al no poder aprender mas MACs, el switch entra en
     modo de falla abierta y comienza a INUNDAR (broadcast) todo el trafico de todos
     los puertos como si fuera un Hub. El atacante solo abre Wireshark y captura
     el trafico confidencial de toda la empresa.


### c) Agotamiento DHCP y Servidor DHCP Pirata (DHCP Starvation & Rogue DHCP):

   - Starvation: El atacante solicita miles de direcciones IP con MACs falsas hasta
     agotar el pool del servidor DHCP legitimo (Denegacion de Servicio).
   - Rogue DHCP: El atacante levanta su propio servidor DHCP pirata en su laptop
     y entrega a los clientes su propia IP como Gateway y servidor DNS, interceptando
     todo el trafico saliente.


### d) Salto de VLAN (VLAN Hopping):

   - Switch Spoofing: Aprovecha la autonegociacion DTP (Dynamic Trunking Protocol)
     para fingir ser otro switch y convertir el puerto de acceso en troncal,
     obteniendo acceso a todas las VLANs corporativas.
   - Double Tagging 802.1Q: Inserta dos etiquetas VLAN en la trama para que el switch
     retire la primera (VLAN nativa) y entregue el paquete a una VLAN restringida.


### e) Manipulacion de Spanning Tree (STP Root Takeover):

   - El atacante inyecta BPDUs con prioridad 0 para proclamarse como Switch Raiz (Root Bridge),
     forzando a que todo el trafico de conmutacion pase por su equipo.



## 3. CONTROLES Y SOLUCIONES DE SEGURIDAD EN CAPA 2


| Tecnologia | Funcion y Comando de Mitigacion |
| :--- | :--- |
| Port Security | Limita la cantidad de direcciones MAC permitidas por puerto |
| y apaga la interfaz si se conecta un dispositivo no autorizado: |  |
| `switchport port-security maximum 2` |  |
| `switchport port-security violation shutdown` |  |


DHCP Snooping            Crea una base de datos de confianza y bloquea servidores
                         DHCP no autorizados en puertos de clientes:
                         `ip dhcp snooping vlan 1`
                         (Solo los puertos hacia switches/servidores llevan `trust`).

Dynamic ARP              Valida cada paquete ARP contra la base de datos de DHCP Snooping.
Inspection (DAI)         Si una respuesta ARP es falsa o no coincide, la DESCARTA:
                         `ip arp inspection vlan 1`

IP Source Guard (IPSG)   Impide que un cliente falsifique su direccion IP de origen
                         (IP Spoofing) en la red local:
                         `ip verify source`

BPDU Guard & Root Guard  Protege Spanning Tree contra conmutadores falsos o bucles:
                         `spanning-tree bpduguard enable`
                         `spanning-tree root-guard`

Desactivar DTP           Evita el ataque de Switch Spoofing forzando modo acceso estricto:
                         `switchport mode access`
                         `switchport nonegotiate`

IEEE 802.1X (EAP-TLS)    Autenticacion basada en puerto con certificados digitales y
                         servidores RADIUS (Cisco ISE / Aruba ClearPass). El puerto
                         permanece sellado hasta que la PC demuestre su identidad.

IEEE 802.1AE (MACsec)    Cifrado de Capa 2 a velocidad de cable (Line-Rate) que cifra
                         las tramas Ethernet completas entre switches con AES-GCM-256.



## 4. CASO DE LA VIDA REAL: ROBO DE CREDENCIALES VIA ARP POISONING EN ASEGURADORA

Escenario:
Una empresa multinacional de seguros sufrio el compromiso de cuentas de administradores
y exfiltracion de polizas confidenciales. La auditoria determino que ningun servidor
externo habia sido vulnerado desde Internet; el ataque provino desde adentro.

El Ataque (Modus Operandi):
1. Un consultor externo conecto su laptop en la sala de juntas de la empresa.
2. Ejecuto un script de ARP Poisoning enviando respuestas Gratuitous ARP masivas
   hacia el segmento de servidores y la red de empleados.
3. El atacante se convirtio exitosamente en el intermediario (Man-in-the-Middle)
   entre 45 computadoras del departamento de Recursos Humanos y el servidor de base de datos.
4. Como las conexiones internas a ciertas aplicaciones heredadas viajaban en HTTP plano
   y Telnet, el atacante capturo nombres de usuario, contraseñas y registros medicos
   sin disparar ninguna alerta en el Firewall perimetral (el trafico nunca salio a Internet).

La Solucion y Remediacion Implementada:
El equipo de respuesta a incidentes de ciberseguridad desplego de inmediato las siguientes
defensas de Capa 2 en todos los switches de acceso de la empresa:
1. Habilitacion global de DHCP Snooping:
   - Se aislo la entrega de IPs exclusivamente al servidor DHCP oficial.
2. Habilitacion de Dynamic ARP Inspection (DAI):
   - El switch comenzo a cotejar cada peticion y respuesta ARP. Cuando la laptop del
     consultor intento enviar un paquete ARP diciendo ser el Gateway, el switch
     detecto la discrepancia y DESCARTÓ LOS PAQUETES en menos de 1 milisegundo,
     bloqueando el ataque de Man-in-the-Middle al instante.
3. Configuracion de Port Security con maximo 1 direccion MAC por puerto de roseta.
4. Despliegue de 802.1X con certificados corporativos: Si una laptop no tiene el
   certificado digital de la aseguradora, el puerto la manda a una VLAN de invitados

aislada con salida unicamente a Internet.
