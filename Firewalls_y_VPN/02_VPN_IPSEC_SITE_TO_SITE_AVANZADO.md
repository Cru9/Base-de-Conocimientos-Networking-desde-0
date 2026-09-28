# 02. VPN IPSEC SITE-TO-SITE AVANZADO (IKEv1 vs IKEv2, FASES Y TUNEL VTI)

> **FIREWALLS DE PROXIMA GENERACION (NGFW) Y VPNs EMPRESARIALES**


---



## 1. ¿QUE ES UNA VPN IPSEC SITE-TO-SITE?

Una Red Privada Virtual Sitio a Sitio (Site-to-Site VPN) conecta dos sedes fisicas
(ej. Corporativo y Planta Fabril) a traves de una red publica insegura (Internet),
creando un tunel cifrado que hace que ambas sedes se comuniquen como si estuvieran
conectadas por un cable de red privado.

IPsec (Internet Protocol Security - Conjunto de RFCs del IETF) opera en la Capa 3
del modelo OSI y provee:
1. Confidencialidad: Cifrado robusto para que nadie pueda espiar el contenido.
2. Integridad: Verificacion de que ningun bit fue alterado en transito.
3. Autenticacion: Certeza matematica de la identidad de ambos cortafuegos.
4. Proteccion Antirreproduccion (Anti-Replay): Evita que un atacante capture un
   paquete valido y lo retransmita para duplicar una transaccion.



## 2. LOS PROTOCOLOS DEL CORAZON DE IPSEC


| Protocolo | Numero IP / Puerto | Funcion |
| :--- | :--- | :--- |
| ESP | Protocolo IP 50 | Encapsulating Security Payload: Cifra los datos |

                                     con algoritmos simetricos (AES-256), autentica
                                     el origen y provee proteccion antirreproduccion.
                                     (Utilizado en el 99% de las VPNs modernas).

AH              Protocolo IP 51      Authentication Header: Autentica el paquete y el
                                     encabezado IP, pero ¡NO CIFRA NADA! (Incompatible
                                     con NAT; casi extinto en la industria).

IKE             Puerto UDP 500       Internet Key Exchange: Negocia las claves secretas,
                                     autenticacion y politicas entre los firewalls.

NAT-T           Puerto UDP 4500      NAT-Traversal (RFC 3948): Si uno de los firewalls
                                     esta detras de un router con NAT, encapsula los
                                     paquetes ESP dentro de UDP 4500 para cruzar el NAT.



## 3. LAS DOS FASES DE IPSEC EXPLICADAS AL DETALLE

El establecimiento de un tunel IPsec se divide en dos fases obligatorias:

FASE 1: IKE SA (EL CANAL DE CONTROL SEGURO)
- Proposito: Los dos firewalls se autentican mutuamente y establecen un canal cifrado
  seguro UNICAMENTE para hablar entre ellos y negociar las claves del tunel.
- Parametros a coincidir exactamente (Mnemotecnia HAGLE):
  * H - Hash: SHA-256 o SHA-512 (integridad de la negociacion).
  * A - Authentication: Clave Precompartida (Pre-Shared Key - PSK) o Certificados X.509.
  * G - Diffie-Hellman Group: Intercambio seguro de claves (Grupo 14 de 2048b, o
        Grupo 19/20 de Curvas Elipticas - ECDH).
  * L - Lifetime: Tiempo de vida del canal de control (ej. 86400 segundos / 24 horas).
  * E - Encryption: AES-CBC-256 o AES-GCM-256.

IKEv1 vs IKEv2 (Pregunta de Examen):
- IKEv1: Obsoleto. Requiere 6 paquetes en Main Mode o 3 en Aggressive Mode.
- IKEv2 (RFC 7296): Estandar moderno obligatorio. Negocia en solo 4 paquetes,
  soporta recuperacion automatica de fallas (MOBIKE), NAT-T nativo integrado
  y menor consumo de CPU.

FASE 2: IPsec SA (EL TUNEL DE DATOS REAL DEL USUARIO)
- Proposito: Negociar los parametros con los que se cifrara el trafico de las PCs y servidores.
- Genera dos Asociaciones de Seguridad (SAs) unidireccionales (una para subida y una para bajada).
- Parametros negociados:
  * Protocolo: ESP.
  * Algoritmo de Cifrado y Hash: AES-256-GCM.
  * Perfect Forward Secrecy (PFS): Fuerza a ejecutar un nuevo intercambio Diffie-Hellman
    cada vez que la Fase 2 expira (ej. cada 8 horas), asegurando que si una clave es
    descubierta, jamas pueda descifrar el trafico futuro ni pasado.
  * Selectores de Trafico (Proxy-ID): Subred Local (192.168.10.0/24) y Subred Remota (192.168.20.0/24).



## 4. PARADIGMAS DE DISENO: POLICY-BASED vs ROUTE-BASED (VTI)


### a) VPN Basada en Politicas (Policy-Based / Crypto Maps - Modelo Antiguo):

   - Una Lista de Control de Acceso (ACL) define que trafico se cifra.
   - Si el paquete coincide con la ACL, se envia al tunel; si no, sale a Internet.
   - Desventaja Critica: NO soporta enrutamiento dinamico (OSPF / BGP) ni interfaces logicas.


### b) VPN Basada en Rutas (Route-Based / VTI - Virtual Tunnel Interface - Estandar Actual):

   - El firewall crea una interfaz de red virtual (ej. `tunnel.1` o `vti1`).
   - El trafico entra al tunel simplemente enrutandolo hacia la interfaz `tunnel.1`
     (mediante una ruta estatica o un protocolo dinamico como OSPF/BGP).
   - Ventaja: Maxima simplicidad de gestion, soporta multicast, SD-WAN y failover automatico.



## 5. MECANISMO DE SUPERVIVENCIA: DEAD PEER DETECTION (DPD - RFC 3706)

- Problema: Si el firewall de la sucursal sufre un corte de energia repentino, no
  tiene tiempo de avisarle al corporativo que se apago.
- El corporativo seguiria enviando paquetes al tunel muerto durante horas.
- DPD envia micro-mensajes "Are You There?" cada 10 o 20 segundos por UDP 500.
- Si no recibe respuesta tras 3 intentos, declara la sesion como muerta (Dead),

destruye las SAs en memoria y commuta el enrutamiento al enlace de respaldo.
