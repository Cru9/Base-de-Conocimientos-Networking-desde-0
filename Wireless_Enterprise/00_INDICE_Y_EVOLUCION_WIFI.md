# 00. INDICE GENERAL Y EVOLUCION DE LOS ESTANDARES IEEE 802.11

> **REDES INALAMBRICAS EMPRESARIALES (WIRELESS ENTERPRISE NETWORKING)**


---



## 1. EVOLUCION DE LA TECNOLOGIA WI-FI: DE LA CONECTIVIDAD BASICA A LA HIPERDENSIDAD

Las redes inalambricas empresariales han dejado de ser un mecanismo de acceso
secundario de conveniencia para convertirse en el medio principal de conexion
de las organizaciones modernas.


## TABLA EVOLUTIVA DE ESTANDARES IEEE 802.11:


| Estandar | Nombre Comercial | Banda(s) | Ancho Canal | Modulacion | Velocidad Maxima |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 802.11b | Wi-Fi 1 | 2.4 GHz | 20 MHz | DSSS/CCK | 11 Mbps |
| 802.11a | Wi-Fi 2 | 5 GHz | 20 MHz | 64-QAM | 54 Mbps |
| 802.11g | Wi-Fi 3 | 2.4 GHz | 20 MHz | 64-QAM | 54 Mbps |
| 802.11n | Wi-Fi 4 | 2.4 / 5 GHz | 20 / 40 MHz | 64-QAM | 600 Mbps (4x4) |
| 802.11ac | Wi-Fi 5 | Solo 5 GHz | Hasta 160MHz 256-QAM | 6.9 Gbps (8x8) |  |
| 802.11ax | Wi-Fi 6 / 6E | 2.4 / 5 / 6 GHz Hasta 160MHz 1024-QAM | 9.6 Gbps (8x8) |  |  |
| 802.11be | Wi-Fi 7 | 2.4 / 5 / 6 GHz Hasta 320MHz 4096-QAM | 46 Gbps (16x16) |  |  |




## 2. LA REVOLUCION DE WI-FI 6 Y WI-FI 6E (802.11ax)

A diferencia de versiones anteriores enfocadas solo en la "velocidad de pico teorica",
Wi-Fi 6 fue disenado especificamente para "Alta Eficiencia en Entornos Densos" (HEW:
High Efficiency Wireless): estadios, auditorios, campus universitarios y hospitales.


### a) OFDMA (Orthogonal Frequency Division Multiple Access):

   - En Wi-Fi tradicional (OFDM), cuando un dispositivo habla, ocupa el canal completo
     de 20 MHz (como un camion de carga gigante llevando un solo sobre pequeno).
   - Con OFDMA, el canal se divide en subcanales diminutos denominados RU (Resource Units).
   - Un solo punto de acceso (AP) puede comunicarse SIMULTANEAMENTE con hasta 37
     clientes (sensores IoT, celulares, laptops) en una misma transmision de radio.
   - Elimina la congestion y colisiones de contencion de CSMA/CA.


### b) BSS Coloring (Coloracion del Conjunto de Servicios Basicos):

   - Asigna un "color" numerico (de 1 a 64) en la cabecera fisica de las tramas.
   - Si un AP detecta una transmision en su mismo canal pero con un "color" diferente,
     sabe que proviene de un AP vecino lejano y puede transmitir en paralelo sin
     detenerse (mitiga el problema de interferencia co-canal y optimiza la reutilizacion espacial).


### c) Wi-Fi 6E y la Apertura del Espectro de 6 GHz:

   - Tradicionalmente, Wi-Fi operaba en las saturadas bandas de 2.4 GHz y 5 GHz.
   - Wi-Fi 6E abre hasta 1,200 MHz de espectro totalmente nuevo y limpio en la banda de 6 GHz.
   - Aporta 59 nuevos canales de 20 MHz o hasta 7 canales super-anchos de 160 MHz.
   - CERO dispositivos antiguos (legacy): Ningun dispositivo 802.11b/g/n/ac puede
     operar en 6 GHz, garantizando rendimiento puro sin degradacion.



## 3. LA PROXIMA FRONTERA: WI-FI 7 (802.11be - EXTREME HIGH THROUGHPUT)

Disenado para Realidad Virtual/Aumentada (VR/AR), automatizacion industrial y telemedicina:
- Modulacion 4096-QAM (4K-QAM): 20% mas densidad de datos por simbolo que Wi-Fi 6.
- Canales ultra-anchos de 320 MHz.
- MLO (Multi-Link Operation): Permite a un dispositivo enviar y recibir paquetes
  SIMULTANEAMENTE a traves de 2.4 GHz, 5 GHz y 6 GHz usando diferentes antenas en paralelo.
  Reduce la latencia a menos de 5 milisegundos y ofrece tolerancia a fallas instantanea.



## 4. INDICE DE ARCHIVOS DE LA CARPETA WIRELESS_ENTERPRISE

[00_INDICE_Y_EVOLUCION_WIFI.md](./00_INDICE_Y_EVOLUCION_WIFI.md)
    - Resumen evolutivo, diferencias entre generaciones y tecnologias Wi-Fi 6/6E y Wi-Fi 7.

[01_ARQUITECTURA_CENTRALIZADA_WLC_Y_CAPWAP.md](./01_ARQUITECTURA_CENTRALIZADA_WLC_Y_CAPWAP.md)
    - Puntos de acceso autonomos vs ligeros (Lightweight), arquitectura Split-MAC,
      el protocolo CAPWAP (UDP 5246/5247) y modos de operacion (Local vs FlexConnect).

[02_SEGURIDAD_WIFI_WPA3_Y_8021X.md](./02_SEGURIDAD_WIFI_WPA3_Y_8021X.md)
    - Vulnerabilidades de WPA2, el protocolo SAE de WPA3 (Dragonfly), autenticacion
      corporativa 802.1X con RADIUS (EAP-TLS, PEAP) y proteccion de tramas de gestion (802.11w MFP).

[03_PLANIFICACION_RF_ROAMING_Y_ANTENAS.md](./03_PLANIFICACION_RF_ROAMING_Y_ANTENAS.md)
    - Diseno de radiofrecuencia (dBm, RSSI, SNR), planificacion de canales (1, 6, 11 en 2.4 GHz
      y canales DFS en 5 GHz), tipos de antenas y estandares de roaming rapido (802.11k/v/r).

[04_CONFIGURACIONES_WIFI_EMPRESARIAL.md](./04_CONFIGURACIONES_WIFI_EMPRESARIAL.md)
    - Laboratorio real de configuracion: Controladoras Cisco Catalyst 9800 WLC (IOS-XE)

y Aruba Mobility Conductor (ArubaOS), con integracion de servidores RADIUS / ISE.
