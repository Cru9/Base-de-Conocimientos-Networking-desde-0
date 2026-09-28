# 06. CAPA 6: CAPA DE PRESENTACION (PRESENTATION LAYER) - FORMATO Y CIFRADO

> **MODELO OSI (OPEN SYSTEMS INTERCONNECTION) - GUIA MAESTRA PARA CERTIFICACIONES**  
> *Guía de referencia técnica y preparación para certificaciones Cisco CCNA 200-301, CompTIA Network+ y Huawei HCIA.*

---


## 1. FUNCION Y PROPOSITO DE LA CAPA DE PRESENTACION

La Capa de Presentacion es la responsable de la sintaxis y la semantica de la
informacion transmitida entre dos sistemas.

Actua como el "traductor oficial" de la red. Su mision es garantizar que los
datos enviados por la Capa de Aplicacion de una computadora emisor puedan ser
leidos e interpretados correctamente por la Capa de Aplicacion de una computadora
receptora, sin importar que tengan diferentes sistemas operativos, procesadores
o conjuntos de caracteres.

Su PDU (Unidad de Datos de Protocolo) es: DATOS (Data).

Las Tres Grandes Funciones de la Capa 6 (Regla de Examen):
1. TRADUCCION de formatos y codificacion de caracteres.
2. CIFRADO y DESCIFRADO de datos (Seguridad y Privacidad).
3. COMPRESION y DESCOMPRESION de datos (Eficiencia de ancho de banda).


## 2. TRADUCCION Y CODIFICACION DE CARACTERES

Diferentes arquitecturas informaticas representan letras, numeros y simbolos
con distintas combinaciones binarias:

### a) EBCDIC (Extended Binary Coded Decimal Interchange Code):

   - Sistema de codificacion de 8 bits utilizado historicamente por los Mainframes
     de IBM.

### b) ASCII (American Standard Code for Information Interchange):

   - Codigo de 7 u 8 bits comun en computadoras personales y terminales antiguas.

### c) UNICODE (UTF-8 / UTF-16):

   - El estandar universal moderno. UTF-8 es compatible con ASCII y codifica mas de
     140,000 caracteres de todos los idiomas del mundo, alfabetos cientificos y emojis.
   - La Capa 6 convierte un archivo de EBCDIC (Mainframe) a UTF-8 (PC) en vuelo
     para que sea legible.


## 3. FORMATOS DE SERIALIZACION Y MULTIMEDIA EN CAPA 6

La Capa de Presentacion define el formato con el que las aplicaciones serializan
estructuras de datos complejas para enviarlas por la red:

Formatos de Intercambio de Datos Estructurados:
- JSON (JavaScript Object Notation): Texto ligero clave-valor (estandar de APIs REST).
- XML (Extensible Markup Language): Formato basado en etiquetas jerarquicas.
- YAML: Formato legible para humanos utilizado en configuracion y automatizacion.
- ASN.1 (Abstract Syntax Notation One): Estandar formal de telecomunicaciones.

Formatos Multimedia y Graficos estandarizados en Capa 6:
- Imagenes: JPEG, PNG, GIF, BMP, TIFF, SVG.
- Audio: MP3, AAC, WAV, Opus, FLAC.
- Video: MP4, MPEG-2, H.264, H.265 (HEVC), AV1.
- Documentos: PostScript, PDF.


## 4. CIFRADO Y SEGURIDAD CRIPTOGRAFICA (ENCRYPTION)

Para evitar que un atacante que capture los paquetes en la red pueda leer informacion
sensible (claves bancarias, mensajes privados), la Capa de Presentacion transforma
el texto claro (Plaintext) en texto cifrado ininteligible (Ciphertext):

### a) Cifrado Simetrico (Misma clave para cifrar y descifrar):

   - Rapido y eficiente para grandes volumenes de datos.
   - Estandares: AES (Advanced Encryption Standard - 128 / 256 bits), ChaCha20, 3DES.

### b) Cifrado Asimetrico (Clave Publica y Clave Privada):

   - La clave publica cifra y unicamente la clave privada correspondiente puede descifrar.
   - Estandares: RSA, Criptografia de Curva Eliptica (ECC / ECDSA).
   - Se utiliza para autenticar servidores e intercambiar la clave simetrica de sesion.

### c) TLS / SSL (Transport Layer Security):

   - Aunque lleva la palabra "Transport" en su nombre, la capa de registro de TLS
     (TLS Record Protocol) opera a nivel de presentacion, encapsulando y descifrando
     los datos de la aplicacion (HTTPS) antes de entregarlos al navegador web.


## 5. COMPRESION DE DATOS (DATA COMPRESSION)

Reduce la cantidad de bytes que deben transmitirse fisicamente, acelerando la
carga de paginas web y ahorrando costos de transferencia:

- Compresion Sin Perdida (Lossless): Permite reconstruir el archivo original
  bit por bit de forma identica. Utilizado en textos, bases de datos y codigo:
  GZIP, Deflate, Brotli, ZIP.
- Compresion Con Perdida (Lossy): Descarta detalles imperceptibles para el ojo
  o el oido humano para reducir drásticamente el tamaño del archivo:
  JPEG (imagenes), MP3 (audio), H.264 (video streaming).


## 6. BANCO DE PREGUNTAS DE EXAMEN (TIPO CERTIFICACION)

### ❓ Pregunta 1
> **¿Cual capa del modelo OSI es responsable de asegurar que los datos**

cifrados con AES-256 sean descifrados correctamente para que la aplicacion web
pueda procesarlos?
Respuesta: Capa 6 (Presentacion).

### ❓ Pregunta 2
> **¿En que capa del modelo OSI se realiza la traduccion de formatos de**

archivos graficos como JPEG y PNG?
## Respuesta: Capa 6 (Presentacion).

