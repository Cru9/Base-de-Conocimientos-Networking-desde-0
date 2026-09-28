# 03. DESCIFRADO SSL/TLS DEEP INSPECTION, PKI Y MANEJO DE CERTIFICADOS

> **FIREWALLS DE PROXIMA GENERACION (NGFW) POR MARCA LIDER**


---



## 1. EL PUNTO CIEGO DE LA CIBERSEGURIDAD: POR QUE DESCIFRAR SSL/TLS

En la actualidad, mas del 95% del trafico de red transita bajo cifrado SSL/TLS (HTTPS).
Si un Firewall NGFW no cuenta con inspeccion profunda SSL (Deep Packet Inspection - DPI):
- El motor de antivirus NO puede escanear ningun archivo descargado por HTTPS.
- El motor de prevencion de intrusiones (IPS) NO puede ver los ataques web ni SQLi.
- El filtrado de contenido solo ve el nombre de dominio SNI (ejemplo: 'drive.google.com'),
  pero NO puede distinguir si el usuario esta leyendo un documento laboral o subiendo
  la base de datos confidencial de clientes a su cuenta personal de Google Drive.

DIAGRAMA DEL FLUJO DE DESCIFRADO FORWARD PROXY (MAN-IN-THE-MIDDLE AUTORIZADO):

   [ Usuario Interno ]           [ NGFW (FortiGate / Palo Alto) ]          [ Servidor Web Remoto ]
   (Laptop Corporativa)                (Sub-CA Empresarial)                 (Ej. www.salesforce.com)
            |                                    |                                     |
            | === 1. Client Hello (HTTPS) =====> |                                     |
            |                                    | ===== 2. Client Hello (HTTPS) ====> |
            |                                    | <==== 3. Server Hello + Cert Leg==- |
            |                                    |   [Valida Cert con CAs Globales]    |
            | <== 4. Emite Cert Al Vuelo ======= |                                     |
            |    (Firmado por Sub-CA Firewall)   |                                     |
            |                                    |                                     |
            |<==== Tunel TLS 1 (Cliente-FW) ====>|<==== Tunel TLS 2 (FW-Internet) ====>|
            |                                    |                                     |
            | === 5. GET /descarga_archivo ====> | [DESCIFRA EN MEMORIA,               |
            |                                    |  APLICA ANTIVIRUS E IPS,            |
            |                                    |  RECIFRA EL PAQUETE]                |
            |                                    | ===== 6. GET /descarga_archivo ===> |



## 2. LOS DOS MODELOS DE INSPECCION SSL

1. Outbound SSL Inspection (SSL Forward Proxy):
   - Protege a los usuarios internos cuando navegan hacia Internet.
   - El firewall genera certificados dinamicos al vuelo para cada sitio web que
     visitan los usuarios.
   - Requiere que todas las computadoras confien en el certificado Raiz o Sub-CA del firewall.

2. Inbound SSL Inspection (SSL Reverse Proxy / Servidores Internos):
   - Protege los servidores web y aplicaciones publicadas en la DMZ de la empresa.
   - El firewall almacena el certificado original y la llave privada del servidor.
   - No requiere instalar nada en los clientes de Internet, ya que el firewall posee
     la identidad autentica del sitio.



## 3. ESTRATEGIA DE DESPLIEGUE DE PKI Y DISTRIBUCION POR GPO

Para que los navegadores (Chrome, Edge, Firefox) no bloqueen el acceso con la alerta
"Su conexion no es privada (NET::ERR_CERT_AUTHORITY_INVALID)":

Paso 1: Generar una Solicitud de Certificado (CSR) en el Firewall como Autoridad Subordinada:
        CN = "Firewall-NGFW-Enterprise-SubCA"
        Key Usage = Certificate Signing, CRL Signing

Paso 2: Firmar el CSR en la Autoridad Certificadora Raiz de la empresa (Microsoft AD CS)
        y exportar el certificado con su cadena de confianza (.CER o .CRT).

Paso 3: Importar el certificado firmado en el Firewall con su llave privada.

Paso 4: Distribuir el Certificado Raiz a todos los endpoints del dominio mediante Active Directory:
        - Abrir la consola de Administracion de Directivas de Grupo (gpmc.msc).
        - Navegar a: Configuracion del equipo -> Directivas -> Configuracion de Windows
          -> Configuracion de seguridad -> Directivas de clave publica
          -> Entidades de certificacion raiz de confianza.
        - Importar el certificado corporativo. Al reiniciar o ejecutar "gpupdate /force",
          todas las PCs de la organizacion confiaran en los certificados del firewall.



## 4. EXCEPCIONES CRITICAS: PRIVACIDAD Y CERTIFICATE PINNING

El descifrado SSL NUNCA debe aplicarse indiscriminadamente a todo el trafico.
Existen dos grandes categorias que DEBEN excluirse de la inspeccion profunda (SSL Bypass):

A. Cumplimiento Legal y Privacidad de los Empleados:
   - Servicios Financieros y Banca por Internet (evitar que el firewall capture
     numeros de tarjetas de credito o contrasenas bancarias de los empleados).
   - Salud y Medicina (regulaciones HIPAA y privacidad de datos sensibles).
   - Portales Gubernamentales y Legales.

B. Certificate Pinning (Anclaje de Certificados):
   - Aplicaciones que llevan incrustada la clave publica legitima directamente en
     su codigo ejecutable (ej. Dropbox, Microsoft Teams, WhatsApp Desktop, Zoom,
     Spotify, Google Drive App).
   - Estas aplicaciones detectan la intervencion del firewall como un ataque y
     bloquean inmediatamente la conexion.
   - Solucion: Crear reglas de "No-Decrypt" o bypass para estas aplicaciones y dominios.



## 5. CONFIGURACION EN FORTINET FORTIGATE (FORTIOS)

! 1. Crear el perfil de inspeccion profunda SSL con bypass de categorias sensibles
config firewall ssl-ssh-profile
    edit "SSL_DEEP_INSPECTION_CORP"
        set comment "Descifrado profundo con excepciones de privacidad"
        config https
            set ports 443
            set status deep-inspection
        end
        config ftps
            set status disable
        end
        config imaps
            set status disable
        end
        ! Seleccionar la Sub-CA corporativa
        set server-cert "SubCA_Corporativa_FortiGate"
        ! Excluir categorias de privacidad
        set ssl-exemption enable
        config ssl-exempt
            edit 1
                set fortiguard-category 30   ! Categoria Finance and Banking
            next
            edit 2
                set fortiguard-category 45   ! Categoria Health and Medicine
            next
            edit 3
                set type wildcard-fqdn
                set wildcard-fqdn "*.zoom.us"
            next
            edit 4
                set type wildcard-fqdn
                set wildcard-fqdn "*.microsoft.com"
            next
        end
    next
end

! 2. Aplicar el perfil de inspeccion profunda a la politica de salida de usuarios
config firewall policy
    edit 10
        set ssl-ssh-profile "SSL_DEEP_INSPECTION_CORP"
    next
end



## 6. CONFIGURACION EN PALO ALTO NETWORKS (PAN-OS)

! 1. Definir la regla de Excepcion de Descifrado (Bypass para Banca y Salud)
set rulebase decryption rules REGLA_BYPASS_BANCA_Y_SALUD from trust
set rulebase decryption rules REGLA_BYPASS_BANCA_Y_SALUD to untrust
set rulebase decryption rules REGLA_BYPASS_BANCA_Y_SALUD source any
set rulebase decryption rules REGLA_BYPASS_BANCA_Y_SALUD destination any
set rulebase decryption rules REGLA_BYPASS_BANCA_Y_SALUD category [ financial-services health-and-medicine ]
set rulebase decryption rules REGLA_BYPASS_BANCA_Y_SALUD action no-decrypt

! 2. Definir la regla de Descifrado Profundo para el resto del trafico web
set rulebase decryption rules REGLA_DESCIFRADO_GENERAL from trust
set rulebase decryption rules REGLA_DESCIFRADO_GENERAL to untrust
set rulebase decryption rules REGLA_DESCIFRADO_GENERAL source any
set rulebase decryption rules REGLA_DESCIFRADO_GENERAL destination any
set rulebase decryption rules REGLA_DESCIFRADO_GENERAL service-type [ any ]
set rulebase decryption rules REGLA_DESCIFRADO_GENERAL action decrypt
set rulebase decryption rules REGLA_DESCIFRADO_GENERAL type ssl-forward-proxy

`cisco
commit
`
