# 02. SEGURIDAD INALAMBRICA: WPA3, IEEE 802.1X, EAP-TLS Y PMF (802.11w)

> **REDES INALAMBRICAS EMPRESARIALES (WIRELESS ENTERPRISE NETWORKING)**


---



## 1. DEBILIDADES CRITICAS DE WPA2 Y LA NECESIDAD DE WPA3


### a) La Gran Falla de WPA2-Personal (PSK):

   - WPA2 utiliza un protocolo de enlace de 4 vias (4-Way Handshake) para derivar
     las claves de cifrado temporales a partir de la contrasena compartida.
   - Ataque de Diccionario Fuera de Linea (Offline Dictionary Attack):
     * Un atacante envia tramas de desautenticacion falsas para desconectar a una victima.
     * Cuando la victima se reconecta, el atacante captura con Wireshark o Airodump-ng
       los 4 paquetes del 4-Way Handshake.
     * El atacante se retira a su laboratorio y prueba miles de millones de contrasenas
       por segundo utilizando GPUs con herramientas como Hashcat sin enviar un solo
       paquete adicional a la red.
   - Falta de Secreto Hacia Adelante (No Forward Secrecy): Si un atacante descubre
     la clave hoy, puede descifrar todas las comunicaciones capturadas en el pasado.


### b) Ataque KRACK (Key Reinstallation Attack):

   - Vulnerabilidad en el diseno del estandar 802.11i de WPA2 que permite forzar
     la reinstalacion de una clave ya en uso reiniciando los contadores de paquetes (Nonces),
     abriendo la puerta al descifrado y manipulacion de trafico.



## 2. WPA3-PERSONAL Y EL PROTOCOLO SAE (DRAGONFLY HANDSHAKE)

WPA3 reemplazo completamente el mecanismo PSK por SAE (Simultaneous Authentication
of Equals - RFC 7664), basado en el protocolo matematico Dragonfly:

- Intercambio de Cero Conocimiento (Zero-Knowledge Proof):
  Ambos extremos demuestran que conocen la contrasena sin enviarla jamas por el aire.
- Inmunidad Total a Ataques de Diccionario Fuera de Linea:
  Incluso si un atacante captura todo el trafico de asociacion por radio, los valores
  matematicos intercambiados son efimeros. No existe forma computacional de verificar
  si una contrasena de diccionario es correcta sin interactuar directamente con el AP.
- Confidencialidad Directa Perfecta (Forward Secrecy):
  Cada sesion utiliza claves de cifrado temporales independientes generadas con
  curvas elipticas (Diffie-Hellman / ECC). Si alguien obtiene la clave manana, es
  matematicamente imposible descifrar el trafico grabado el dia de hoy.



## 3. WPA2 / WPA3-ENTERPRISE: ARQUITECTURA IEEE 802.1X

En entornos corporativos NUNCA se utiliza una contrasena compartida (PSK).
Cada empleado debe autenticarse individualmente con su usuario, contrasena o certificado
digital contra un servidor centralizado (Cisco ISE, Aruba ClearPass o FreeRADIUS).

LOS TRES ACTORES DE 802.1X:
1. Suplicante (Supplicant): El dispositivo cliente (laptop, tablet o smartphone).
2. Autenticador (Authenticator): El Punto de Acceso (AP) o Controladora (WLC).
3. Servidor de Autenticacion (Authentication Server): El servidor RADIUS corporativo
   conectado al Directorio Activo (Microsoft Active Directory / LDAP).


## METODOS EAP (EXTENSIBLE AUTHENTICATION PROTOCOL):


### a) PEAP-MSCHAPv2 (Protected EAP):

   - Funcionamiento:
     1. El servidor RADIUS envia su certificado digital X.509 al cliente.
     2. Se establece un tunel TLS seguro entre el cliente y el servidor RADIUS.
     3. Dentro del tunel TLS protegido, el cliente envia su usuario y contrasena
        corporativa de Active Directory.
   - Ventaja: Muy facil de implementar; no requiere instalar certificados en los clientes.
   - Riesgo Critico: Si los dispositivos de los usuarios no estan configurados por
     GPO para validar estrictamente la Autoridad Certificadora (CA) del RADIUS, un
     atacante con un falso AP y servidor RADIUS puede enganar al cliente y robar
     sus credenciales de red (Ataque Rogue AP / Evil Twin).


### b) EAP-TLS (RFC 5216) - EL ESTANDAR DE ORO DE SEGURIDAD ABSOLUTA:

   - Autenticacion Mutua Basada en Certificados Digitales X.509:
     * El Servidor RADIUS tiene un certificado digital emitido por la CA corporativa.
     * ¡CADA Laptop, Smartphone o Maquina DEBE tener instalado su propio certificado
       digital individual emitido por la PKI empresarial!
   - NO SE UTILIZAN CONTRASENAS: La autenticacion se realiza validando firmas criptograficas.
   - Inmune al Phishing, inmune a ataques Evil Twin y a robo de contrasenas. Si un
     dispositivo no tiene el certificado emitido por la entidad oficial, jamas entra a la red.



## 4. WPA3-ENTERPRISE MODO 192-BIT (SUITE B / CNSA)

Para agencias gubernamentales, banca central y entornos militares de alta seguridad:
- Algoritmo de cifrado simetrico: GCMP-256 (Galois/Counter Mode Protocol de 256 bits).
- Firma e integridad de mensajes: HMAC-SHA-384.
- Intercambio de claves: Curvas Elipticas ECDH y ECDSA utilizando la curva NIST P-384.



## 5. PROTECCION DE TRAMAS DE GESTION (PMF - IEEE 802.11w)

En las redes Wi-Fi tradicionales, las tramas de gestion que controlan la conexion
(como `Deauthentication` y `Disassociation`) viajan en texto plano y sin firma.
- Ataque Clasico de Desautenticacion: Un atacante emite tramas de desautenticacion
  falsificando la MAC del AP y desconecta instantaneamente a todos los usuarios de la sala.

Solucion con IEEE 802.11w (PMF / MFP):
- Se anade una etiqueta criptografica BIP (Broadcast Integrity Protocol) a cada
  trama de gestion emitida por el AP.
- Si un atacante inyecta tramas de desautenticacion falsas, los clientes las descartan
  automaticamente al fallar la verificacion criptografica.

## - En WPA2, PMF era opcional. ¡EN WPA3, PMF ES ESTRICTAMENTE OBLIGATORIO!
