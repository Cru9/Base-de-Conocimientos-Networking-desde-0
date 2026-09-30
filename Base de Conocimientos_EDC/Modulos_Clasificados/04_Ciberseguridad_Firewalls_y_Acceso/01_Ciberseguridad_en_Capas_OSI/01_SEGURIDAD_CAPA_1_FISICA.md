# 01. SEGURIDAD EN LA CAPA 1 (FISICA) - AMENAZAS, DEFENSAS Y CASO REAL

> **CIBERSEGURIDAD EN EL MODELO OSI - GUIA PRACTICA Y CASOS DE LA VIDA REAL**


---



## 1. PANORAMA DE SEGURIDAD EN LA CAPA FISICA

La Capa 1 es la mas ignorada en las politicas de seguridad digital ("si no esta
en la pantalla, no existe"). Sin embargo, existe una maxima universal en hacking:
"Si un atacante tiene acceso fisico sin restricciones a tu dispositivo o a tu cable,
ya no es tu dispositivo: es del atacante".

Objetivo en Capa 1:
Proteger los medios de transmision (cables de cobre, fibras opticas, ondas de radio),
los puertos de conexion y los equipos de red contra el acceso fisico no autorizado,
intercepcion pasiva, danos ambientales y destruccion o sabotaje.



## 2. VECTORES DE ATAQUE EN CAPA 1


### a) Intercepcion de Senales y Pinchado de Cables (Wiretapping):

   - Pinchado de Cobre: Mediante pinzas inductivas que capturan la radiacion
     electromagnetica emitida por cables UTP sin blindaje sin necesidad de cortar el cable.
   - Pinchado de Fibra Optica (Fiber Bending / Tapping): Al curvar levemente una fibra
     optica (macrobending) con un dispositivo llamado "Optical Clip-On Coupler", una
     fraccion microscopica de luz escapa del nucleo hacia un fotodetector. El atacante
     clona el 100% del trafico que viaja por la fibra sin que el switch detecte un corte de enlace.


### b) Implantes Fisicos Encubiertos (Hardware Implants):

   - Drop-Boxes (ej. LAN Turtle, Raspberry Pi oculta): Dispositivos pequenos que
     se conectan entre el switch y la toma de pared, abriendo un tunel inverso 4G/LTE
     hacia los servidores del atacante (bypass completo del firewall perimetral).
   - Keyloggers de Hardware: Dispositivos intercalados entre el teclado USB y la PC
     de una recepcion o cajero para capturar contraseñas antes de que lleguen al sistema operativo.
   - Rubber Ducky (BadUSB): Memorias USB modificadas que se hacen pasar por teclados
     humanos, inyectando cientos de lineas de codigo malicioso por segundo en cuanto
     se insertan.


### c) Puntos de Acceso Inalambricos Piratas (Rogue APs / Evil Twins):

   - Un empleado o intruso conecta un router Wi-Fi barato a una toma de red libre
     de la oficina para tener "internet rapido", abriendo una puerta trasera sin
     cifrado hacia toda la red corporativa.


### d) Sabotaje y Danos Fisicos:

   - Cortes deliberados de enlaces de fibra troncales, apagado de interruptores
     electricos, desconexion de cables de consola o manipulacion del boton de Reset
     para reiniciar a valores de fabrica.



## 3. CONTROLES Y SOLUCIONES DE SEGURIDAD EN CAPA 1

1. Control de Acceso Fisico Estricto a Centros de Datos y Armarios de Red (MDF/IDF):
   - Acceso con doble factor biometrico (huella dactilar/iris + tarjeta RFID).
   - Esclusas de seguridad (Mantraps) que impiden el paso simultaneo de dos personas (anti-tailgating).
   - Gabinetes (racks) cerrados con llave y sensores de apertura conectados a alarmas.

2. Bloqueadores Fisicos de Puertos RJ45 y USB:
   - Insertar tapones de plastico con cerradura especial (RJ45 Port Blockers) en
     todos los puertos de pared y puertos de switches que no esten en uso, impidiendo
     que cualquiera conecte un cable.

3. Cableado Estructurado Blindado y Protegido:
   - Utilizar cableado STP/FTP y canaletas metalicas selladas o tuberias EMT con
     sellos de inviolabilidad (Tamper-evident seals).
   - Enlace de Fibra Monitorizada mediante OTDR (Optical Time-Domain Reflectometer):
     Monitorea la dispersion y atenuacion del haz de luz en tiempo real; si alguien
     curva la fibra para pincharla, el sistema detecta la caida de dB y activa una alarma.

4. Cifrado a Nivel de Enlace Fisico (Line-Rate Encryption):
   - Implementar cifradores de capa fisica (Capa 1 OTN Encryption o DWDM Encryption)
     entre centros de datos. Si el cable submarino o la fibra es pinchada, el atacante
     solo captura luz cifrada con AES-256 indescifrable.

5. Sistemas de Alimentacion Ininterrumpida (UPS) y Acondicionamiento de Energia:
   - Generadores diesel de respaldo, supresores de picos de voltaje y cableado doble
     a fuentes redundantes (Dual Power Supply).



## 4. CASO DE LA VIDA REAL: INFILTRACION FISICA EN SUCURSAL BANCARIA

Escenario:
Un banco multinacional sufrio una brecha de seguridad grave en una de sus sucursales
principales sin que sus firewalls perimetrales registraran ninguna alerta de intrusión.

El Ataque (Modus Operandi):
1. Un atacante vestido como tecnico de aire acondicionado solicito acceso al area
   de atencion a clientes fuera de horario bancario bajo el pretexto de mantenimiento preventivo.
2. Al estar solo por unos minutos, el atacante desconecto el cable de red de una
   impresora de red de la sucursal e interpuso un pequeno dispositivo oculto dentro
   de un cargador de pared falso (LAN Turtle / Drop-Box con modem 4G integrado).
3. Conecto la impresora a la salida del dispositivo. La impresora siguio funcionando
   con normalidad, por lo que nadie noto nada sospechoso.
4. El dispositivo, alimentado por la corriente, establecio una conexion VPN cifrada
   por red celular 4G hacia el servidor del atacante, saltandose por completo el
   Firewall perimetral y los filtros de salida de Internet del banco.
5. Durante 3 semanas, los atacantes realizaron reconocimiento de la red interna,
   capturaron transacciones y credenciales administrativas no cifradas.

La Solucion y Remediacion Implementada:
Tras el analisis forense, el equipo de ciberseguridad aplico las siguientes medidas
obligatorias de Capa 1 y Capa 2:
1. Retiro de todos los puertos libres y uso de Bloqueadores Fisicos RJ45 en todas
   las tomas de pared de atencion al publico.
2. Despliegue de Control de Acceso Basado en Red (802.1X): Cada dispositivo (incluso
   impresoras) debe autenticarse mediante certificados digitales X.509 antes de
   que el puerto del switch abra el paso de datos. Si se conecta un dispositivo no
   autorizado (como el Drop-Box), el puerto se apaga de inmediato.
3. Protocolo Estricto de Seguridad Fisica: Prohibicion absoluta de acceso a cuartos
   de comunicacion o cableado sin acompañamiento presencial permanente de un oficial
   de seguridad y registro con credenciales de identidad.

## 4. Camaras de videovigilancia CCTV dirigidas exclusivamente a los racks de comunicaciones.
