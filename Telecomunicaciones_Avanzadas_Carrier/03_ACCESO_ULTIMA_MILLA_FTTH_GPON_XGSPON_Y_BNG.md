# 03. REDES DE ACCESO DE ULTIMA MILLA FIJA: FTTH, GPON, XGS-PON Y BNG

> **TELECOMUNICACIONES AVANZADAS, REDES DE CARRIER E INFRAESTRUCTURA GLOBAL**


---



## 1. ARQUITECTURAS FTTX Y PRINCIPIOS DE REDES OPTICAS PASIVAS (PON)

Las redes FTTx (Fiber to the x) reemplazaron al cable de cobre coaxial (HFC) y par
trenzado (ADSL/VDSL) llevando la fibra optica hasta el usuario final:
- FTTH (Fiber to the Home): La fibra llega directamente a la roseta interior del hogar.
- FTTB (Fiber to the Building): La fibra llega al sotano del edificio de departamentos.
- FTTO (Fiber to the Office): Enlaces empresariales dedicados con SLA de alta disponibilidad.

¿POR QUE UNA RED OPTICA PASIVA (PON)?
- Topologia Punto a Multipunto (P2MP): Un unico puerto optico en la central telefonica
  (OLT) alimenta a 32, 64 o hasta 128 usuarios simultaneos a traves de un solo hilo.
- CERO electronica en la calle: Entre la central y el cliente NO existen switches,
  ni fuentes de poder, ni baterias de respaldo que puedan fallar ante cortes de luz
  o tormentas. La division de la luz se realiza mediante prismas de vidrio (Splitters).



## 2. COMPARATIVA DE TECNOLOGIAS PON (GPON VS XGS-PON)


| Parametro | GPON (Gigabit PON) | XGS-PON (10G Simetrico) |
| :--- | :--- | :--- |
| Estandar | ITU-T G.984 | ITU-T G.9807.1 |
| Velocidad Downstream | 2.488 Gbps | 9.953 Gbps (~10 Gbps) |
| Velocidad Upstream | 1.244 Gbps | 9.953 Gbps (~10 Gbps Simetricos) |
| Longitud Onda Down (Tx) 1490 nm | 1577 nm |  |
| Longitud Onda Up (Rx) | 1310 nm | 1270 nm |
| Longitud Video RF | 1550 nm (CATV opcional) | 1550 nm (Coexistencia) |
| Tipo de Trafico Up | TDMA (Ranuras de tiempo dinamicas DBA) | TDMA / XGEM |
| Cifrado de Datos | AES-128 en canal descendente | AES-128 / AES-256 bidireccional |
| Ratio de Split Maximo | 1:64 o 1:128 | 1:128 o 1:256 |
| Presupuesto Optico | Clase B+ (28 dB) / Clase C+ (32 dB) | Clase N1 (29 dB) / Clase N2 / E1 (35 dB) |


COEXISTENCIA EN EL MISMO HILO DE FIBRA (COMBO-PON):
Gracias a que GPON y XGS-PON operan en longitudes de onda totalmente distintas,
los operadores utilizan filtros WDM1r para transmitir GPON y XGS-PON simultaneamente
por la misma fibra fisica. El cliente con contrato basico usa una ONT GPON barata,
y el cliente corporativo o gamer recibe una ONT XGS-PON de 10 Gbps sin obras de zanja.



## 3. ARQUITECTURA DE LA RED ODN (OPTICAL DISTRIBUTION NETWORK)

La planta externa pasiva (ODN) se compone de los siguientes elementos en serie:

  [ CENTRAL TELEFONICA / POP ]
  [ OLT (Chasis Huawei/ZTE)  ]
              |
         (Patch Cord)
              v
  [ ODF (Optical Dist. Frame)]
              |
       (Cable Feeder Troncal de 96 o 144 fibras)
              v
```text
  [ FDT / Armario de Distribucion ] ===> Splitter Primario Nivel 1 (ej. 1:8)
              |
       (Cable de Distribucion de 24 fibras)
              v
  [ CTO / Caja Terminal Optica ]   ===> Splitter Secundario Nivel 2 (ej. 1:8)
              |                         (Total de split combinado: 8 x 8 = 1:64)
       (Acometida Drop G.657.A2)
              v
  [ Roseta Optica en Domicilio ] ===> Conector SC/APC (Verde, corte angular 8 grados)
              |
  [ ONT / Modem Residencial    ]
```


## 4. PERDIDAS DE POTENCIA POR SPLITTERS OPTICOS (PLC)

Un divisor pasivo (Splitter PLC) divide la potencia del haz de luz.
La perdida teorica e insercion real se calcula con la formula: Perdida = 10 * log10(N)


| Ratio de Splitter | Perdida Teorica | Perdida de Insercion Real Tipica |
| :--- | :--- | :--- |
| 1:2 | 3.01 dB | ~3.5 dB a 3.8 dB |
| 1:4 | 6.02 dB | ~7.0 dB a 7.4 dB |
| 1:8 | 9.03 dB | ~10.2 dB a 10.6 dB |
| 1:16 | 12.04 dB | ~13.5 dB a 14.0 dB |
| 1:32 | 15.05 dB | ~16.8 dB a 17.5 dB |
| 1:64 | 18.06 dB | ~20.2 dB a 21.0 dB |


REGLA DE ORO DE INSTALACION FTTH:
- La potencia transmitida por el laser de la OLT (Clase C+) es de +3 a +7 dBm.
- La sensibilidad minima del receptor de la ONT es de -28 dBm (Clase B+) o -32 dBm (Clase C+).
- La potencia que llega a la roseta del cliente debe situarse idealmente entre -18 dBm y -24 dBm.
  Si la potencia cae por debajo de -27 dBm, la ONT sufrira desconexiones y microcortes.



## 5. PROTOCOLO OMCI (ONU MANAGEMENT AND CONTROL INTERFACE)

OMCI (ITU-T G.988) es el protocolo de gestion remota que permite a la OLT aprovisionar
la ONT del cliente de forma completamente desatendida a traves del enlace optico:
- Crea las interfaces VLAN de datos, telefonia VoIP y television IPTV.
- Configura las reglas de calidad de servicio (T-CONTs y GEM Ports).
- Asigna credenciales de Wi-Fi, puertos LAN Gigabit y actualiza el firmware de la ONT.



## 6. EL CONCENTRADOR DE BANDA ANCHA (BNG / BRAS) Y METODOS DE ACCESO

El BNG (Broadband Network Gateway) es el enrutador carrier de alta capacidad que
termina las sesiones de Capa 2 de los abonados y los conecta al nucleo IP:

1. IPoE (Internet Protocol over Ethernet - La eleccion moderna):
   - El router de la casa solicita IP mediante DHCP estandar.
   - El switch o la OLT intercepta el paquete e inserta la Opcion 82 (DHCP Option 82):
     * Circuit-ID: "OLT01-PON 0/1/3:12" (Chasis, tarjeta, puerto PON y numero de ONT).
     * Remote-ID: "CONTRATO_CLIENTE_84920".
   - El servidor DHCP entrega la IP asignada directamente al contrato sin que el usuario
     tenga que configurar un usuario y contrasena.

2. PPPoE (Point-to-Point Protocol over Ethernet - Enfoque clasico):
   - El router cliente levanta un tunel PPP punto a punto sobre Ethernet.
   - Requiere usuario y contrasena autenticados contra servidores RADIUS corporativos.
   - Introduce un overhead de 8 bytes en la cabecera (MTU maxima de 1492 bytes en lugar de 1500).

3. Estrategia Dual-Stack Masiva:
   - IPv4 con CGNAT (Carrier-Grade NAT / RFC 6598): Asigna al abonado una IP del rango
     100.64.0.0/10. Varios clientes comparten una misma IP publica mediante NAT masivo
     con registro riguroso de puertos asignados para auditorias legales.
   - IPv6 Nativo con DHCPv6-PD (Prefix Delegation): El BNG delega a cada hogar un
     bloque /56 (lo que equivale a 256 subredes /64), garantizando direccionamiento
     global publico a cada dispositivo inteligente del hogar sin necesidad de NAT.



## 7. CONFIGURACION PRACTICA EN OLT HUAWEI (SMARTAX MA5608T / MA5800)

! 1. Definir Perfil de Asignacion Dinamica de Ancho de Banda (DBA Profile)
dba-profile add profile-id 20 profile-name "PERFIL_INTERNET_300M" type4 max 307200

! 2. Crear Perfil de Linea (Line Profile) - Mapea T-CONT y GEM Ports
ont-lineprofile gpon profile-id 30 profile-name "LINE_PERFIL_RESIDENCIAL"
  tcont 1 dba-profile-id 20
  gem add 1 eth tcont 1
  gem mapping 1 0 vlan 100
  commit
quit

! 3. Crear Perfil de Servicio (Service Profile) - Configura puertos fisicos de la ONT
ont-srvprofile gpon profile-id 30 profile-name "SRV_PERFIL_4GE_WIFI"
  ont-port eth 4 pots 2
  port vlan eth 1 translation 100 user-vlan 100
  commit
quit

! 4. Registrar y autorizar una nueva ONT en el puerto PON 0/1/2
interface gpon 0/1
  ont add 2 15 sn-auth "48575443ABC12345" omci ont-lineprofile-id 30 ont-srvprofile-id 30 desc "CLIENTE_C_GOMEZ"
quit

! 5. Crear el puerto de servicio (Service Port) que conecta la ONT con el BNG

`cisco
service-port vlan 100 gpon 0/1/2 ont 15 gemport 1 multi-service user-vlan 100 tag-transform translate
`
