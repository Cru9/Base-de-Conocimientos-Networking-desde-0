# 04. VPN DE ACCESO REMOTO: SSL/TLS VPN vs WIREGUARD Y AUTENTICACION MFA

> **FIREWALLS DE PROXIMA GENERACION (NGFW) Y VPNs EMPRESARIALES**


---



## 1. LA NECESIDAD DE LA VPN DE ACCESO REMOTO

Con el auge del teletrabajo y la movilidad, los empleados necesitan acceder a los
recursos internos de la empresa (sistemas ERP, servidores de archivos, escritorios
remotos RDP e intranets) desde cualquier lugar del mundo de forma segura.

Objetivo:
Crear un tunel cifrado individual temporal desde la laptop o smartphone del usuario
hacia el firewall perimetral corporativo, validando la identidad del usuario y la
seguridad del dispositivo.



## 2. ARQUITECTURA DE SSL / TLS VPN (EL ESTANDAR EMPRESARIAL)

Las VPNs SSL operan sobre el puerto estandar TCP 443 (HTTPS), lo que les permite
atravesar casi cualquier firewall de hotel, cafeteria o aeropuerto sin ser bloqueadas.

Dos Modalidades de Operacion:


### a) Portal Web Sin Cliente (Clientless / Web-Only):

   - El usuario solo necesita un navegador web (Chrome, Edge, Firefox).
   - Ingresa a `https://vpn.empresa.com`, se autentica y accede a un portal HTML5
     con escritorios remotos RDP web, carpetas de archivos compartidos y SSH web.
   - Ventaja: Cero instalacion de software; ideal para contratistas externos.


### b) Tunel Completo con Cliente Ligero (Client-Based - AnyConnect / FortiClient / GlobalProtect):

   - Se instala una aplicacion en la computadora que crea un adaptador virtual de red.
   - El equipo del usuario obtiene una direccion IP privada de la red corporativa.

Diseno de Enrutamiento: Split Tunnel vs Full Tunnel (Pregunta de Examen):
- Tunel Completo (Full Tunnel):
  TODO el trafico de la computadora del usuario (incluso sus busquedas personales
  en Google, videos de YouTube y Spotify) es forzado a viajar por el tunel VPN hacia
  la empresa antes de salir a Internet.
  *Ventaja: Maxima seguridad corporativa (inspeccion DLP y antivirus de todo).
  *Desventaja: Consume masivamente el ancho de banda del firewall central.
- Tunel Dividido (Split Tunnel):
  UNICAMENTE el trafico dirigido a las subredes internas de la empresa (`10.0.0.0/8`,
  `192.168.0.0/16`) viaja por la VPN. El trafico de navegacion personal sale
  directo por el Wi-Fi domestico del empleado.
  *Ventaja: Ahorra ancho de banda corporativo.
  *Riesgo: Si la laptop del usuario se infecta navegando en Internet, puede actuar
   como puente de infeccion hacia la red de la empresa.



## 3. EVALUACION DE POSTURA DEL DISPOSITIVO (HOST CHECK / COMPLIANCE)

Antes de autorizar que una computadora remota se conecte a la red, el software
de VPN (Cisco AnyConnect ISE Posture, FortiClient EMS) inspecciona la maquina:
- ¿Tiene el antivirus corporativo instalado y con firmas del dia?
- ¿Tiene el cortafuegos de Windows encendido?
- ¿El disco duro esta cifrado con BitLocker?
- ¿Pertenece al dominio de Active Directory de la empresa?
Si la computadora no cumple los requisitos de seguridad, el firewall la rechaza
o la envia a una red de cuarentena para que se actualice.



## 4. WIREGUARD: EL PROTOCOLO VPN DE NUEVA GENERACION

WireGuard es un protocolo moderno de codigo abierto diseñado para reemplazar a
IPsec y OpenVPN.

¿Por que esta revolucionando el mercado?
1. Base de Codigo Ultraligera:
   - IPsec y OpenVPN tienen entre 100,000 y 400,000 lineas de codigo (dificiles de
     auditar y propensas a vulnerabilidades).
   - WireGuard tiene MENOS DE 4,000 LINEAS DE CODIGO. Es facil de auditar formalmente.
2. Criptografia Moderna Forzada (Opinionated Crypto):
   - No permite negociar algoritmos obsoletos ni inseguros.
   - Utiliza exclusivamente lo mejor de la criptografia moderna:
     * Cifrado Simetrico: ChaCha20 con autenticacion Poly1305.
     * Intercambio de Claves: Curve25519 (ECDH).
     * Hashing: BLAKE2s.
3. Rendimiento en el Espacio del Kernel:
   - Opera directamente dentro del kernel de Linux/Windows, alcanzando tasas de
     transferencia de velocidad de cable con un consumo de CPU 4 veces menor que OpenVPN.
4. Itinerancia Transparente (Seamless Roaming):
   - Si un usuario cambia de la red Wi-Fi de su casa a la red celular 5G de su telefono,
     la sesion NO SE CORTA. WireGuard no tiene handshake de sesion costoso; reanuda
     el envio de paquetes de inmediato.



## 5. COMPARATIVA DIRECTA: IPSEC vs SSL VPN vs WIREGUARD


| Caracteristica | IPsec (IKEv2) | SSL/TLS VPN | WireGuard |
| :--- | :--- | :--- | :--- |
| Capa OSI | Capa 3 (Red) | Capa 4/5 (Transporte/Ses) Capa 3 (Red) |  |
| Puerto Utilizado | UDP 500 / 4500 / ESP 50 | TCP 443 (HTTPS) | UDP Variable |
| Paso por Firewalls | Puede ser bloqueado | Pasa por cualquier lado | Requiere puerto UDP |
| Velocidad / Rendim. | Muy alta (Hardware ASIC) Moderada | Maxima (Kernel space) |  |
| Complejidad Config. | Alta | Media | Extremadamente simple |
| Uso Predominante | Site-to-Site (Sedes) | Acceso Remoto Empleados Nube y Contenedores |  |




## 6. AUTENTICACION MULTIFACTOR (MFA) CON SAML 2.0 / OIDC

La mejor practica empresarial actual consiste en NO almacenar contraseñas en el
propio firewall, sino delegar la autenticacion a un Proveedor de Identidad (IdP):
- Integracion SAML 2.0 con Microsoft Entra ID (Azure AD), Okta o Google Workspace.
- Cuando el empleado abre la VPN:
  1. El cliente VPN abre una ventana de inicio de sesion corporativa.
  2. El usuario introduce sus credenciales institucionales.
  3. Su telefono celular recibe una notificacion de aprobacion (MFA Push Notification
     de Microsoft Authenticator / Duo Security).

## 4. Una vez aprobado en el celular, el firewall recibe el token SAML y levanta el tunel.
