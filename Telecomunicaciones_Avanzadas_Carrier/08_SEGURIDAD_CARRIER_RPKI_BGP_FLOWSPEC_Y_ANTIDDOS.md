# 08. SEGURIDAD DE INFRAESTRUCTURA CARRIER, RPKI, BGP FLOWSPEC Y ANTI-DDOS

> **TELECOMUNICACIONES AVANZADAS, REDES DE CARRIER E INFRAESTRUCTURA GLOBAL**


---



## 1. EL "PECADO ORIGINAL" DE BGP Y LA VULNERABILIDAD GLOBAL DE INTERNET

El protocolo BGP v4 se diseno en 1989 bajo una premisa ingenua: "Confianza implicita
entre operadores". Cuando un router BGP recibe un anuncio de ruta, asume que es verdad.

AMENAZAS CRITICAS EN EL ENRUTAMIENTO GLOBAL:
1. BGP Hijacking (Secuestro de Prefijos):
   - Un operador malicioso o router mal configurado anuncia en Internet un bloque IP
     que pertenece a un banco, red social o servicio critico (ej. 200.50.0.0/24).
   - Debido a la regla BGP de la mascara mas especifica (Longest Prefix Match), el trafico
     de millones de usuarios de todo el planeta se desvia hacia el atacante para espiar,
     robar credenciales o interceptar certificados SSL mediante tecnicas Man-in-the-Middle.
2. Route Leaks (Fugas de Rutas):
   - Un proveedor local anuncia accidentalmente a su upstream Tier-1 rutas que aprendio
     de otro proveedor, convirtiendose en un cuello de botella no deseado que colapsa
     el trafico de paises enteros.



## 2. RPKI (RESOURCE PUBLIC KEY INFRASTRUCTURE - RFC 6480)

RPKI es el sistema criptografico que vincula formalmente la titularidad de un bloque
de direcciones IP con el Sistema Autonomo (ASN) autorizado para originarlo.

CADENA DE CONFIANZA CRIPTOGRAFICA:
- Anclada en los 5 Registros Regionales de Internet (RIRs): LACNIC, ARIN, RIPE NCC, APNIC y AFRINIC.
- Objeto ROA (Route Origin Authorization):
  Es un certificado digital firmado criptograficamente por el propietario legitimo
  del direccionamiento que declara formalmente:
  "El prefijo 200.50.0.0/20 SOLO puede ser anunciado en Internet por el ASN 65001,
   con una longitud de mascara maxima de hasta /24 (MaxLength: 24)".



## 3. VALIDACION DE ORIGEN BGP (ROV - ROUTE ORIGIN VALIDATION / RFC 6811)

Cuando un router de borde recibe una ruta BGP de un peering o proveedor de transito,
compara el anuncio contra la base de datos de ROAs y asigna uno de tres estados:

1. Valid (Valido):
   - El ASN emisor coincide con el ROA y la mascara no supera el MaxLength.
   - El router acepta la ruta normalmente.

2. Invalid (Invalido):
   - El prefijo esta siendo anunciado por un ASN NO autorizado en el ROA, O
     la mascara es mas especifica que el MaxLength permitido (ej. anuncian /25 cuando el ROA decia /24).
   - REGLA DE ORO DE MANRS: DESCARTAR INMEDIATAMENTE LA RUTA (DROP INVALID).
   - El descarte de rutas Invalidas erradica el 99% de los ataques de BGP Hijacking en el mundo.

3. NotFound / Unknown (No Encontrado):
   - No existe ningun ROA firmado en los RIRs para este bloque.
   - Se acepta provisionalmente para no romper la conectividad de sitios antiguos.



## 4. ARQUITECTURA DEL VALIDADOR RPKI LOCAL (ROUTINATOR)

Un router de produccion no tiene potencia de CPU para validar firmas criptograficas
en tiempo real. Por ello, se despliega un servidor Validador intermedio (Routinator / StayRTR):

   [ Servidores RPKI de los 5 RIRs ] (LACNIC, RIPE, ARIN, etc.)
                   |
     (Sincronizacion RRDP / HTTPS cada 10 min)
                   v
```text
   +-----------------------------------------------------+
   |      SERVIDOR VALIDADOR LOCAL (ROUTINATOR)          |
   | - Descarga y valida criptograficamente los ROAs     |
   | - Mantiene la tabla limpia de validacion en memoria |
   +-----------------------------------------------------+
                   |
      (Protocolo RTR - RPKI to Router / RFC 8210 / TCP 3323)
                   v
   +-----------------------------------------------------+
   |         ROUTERS BGP EDGE DE PRODUCCION              |
   | - Aplican politicas de enrutamiento: DROP INVALID   |
   +-----------------------------------------------------+
```


## 5. MITIGACION DE ATAQUES DDOS A NIVEL CARRIER: RTBH VS BGP FLOWSPEC

Los ataques volumétricos modernos superan cientos de Gigabits y Terabits por segundo
(amplificacion DNS, NTP, SSDP, Memcached). Ningun firewall perimetral puede resistir
semejante avalancha. Se debe mitigar en el plano de enrutamiento del Carrier:

A. REMOTELY TRIGGERED BLACKHOLE (RTBH - RFC 3882 / RFC 7999):
   - Tecnica de contingencia: Sacrificar a la maquina atacada para salvar el enlace de la empresa.
   - Cuando una IP interna (ej. 200.50.10.85/32) es atacada con 200 Gbps:
     1. El NOC inyecta un anuncio BGP interno para 200.50.10.85/32 con la comunidad BGP
        universal 65535:666 (BLACKHOLE).
     2. Todos los routers de borde del carrier fuerzan el siguiente salto de esa IP hacia 'Null0'.
     3. El trafico de ataque se descarta en el silicio de los routers de borde, liberando
        el enlace del cliente para que el resto de sus servidores sigan operando.

B. BGP FLOWSPEC (BGP FLOW SPECIFICATION - RFC 5575 / RFC 8955):
   - LA SOLUCION DEFINITIVA. En lugar de apagar la IP completa de la victima, Flowspec
     inyecta dinamicamente reglas de firewall Capa 3 y Capa 4 a traves de BGP.
   - Permite definir filtros hiper-granulares:
     * "Descartar paquetes UDP dirigidos a 200.50.10.85 con puerto origen 53 y tamano > 1200 bytes".
   - Acciones de Control en Hardware:
     * traffic-rate 0: Descarte puro del flujo de ataque sin tocar el trafico legitimo.
     * traffic-rate <bps>: Estrangulamiento de velocidad (Rate-Limiting).
     * redirect-to-vrf: Desviar el flujo sospechoso hacia un Centro de Limpieza (Scrubbing Center)
       para inspeccion profunda y reinyectar el trafico limpio mediante un tunel GRE.



## 6. CONFIGURACION PRACTICA DE RPKI EN CISCO IOS-XR

! 1. Apuntar a los servidores validadores locales de RPKI (Routinator)
router bfd
!
router bgp 65001
 rpki server 10.50.0.60
  transport tcp port 3323
  refresh time 300
 !
 rpki server 10.50.0.61
  transport tcp port 3323
  refresh time 300
 !

! 2. Crear Route-Policy para descartar rutas BGP invalidas
route-policy RPKI-VALIDATION-POLICY
  if rpki state is invalid then
    drop
  elseif rpki state is valid then
    set local-preference 200
    pass
  else
    ! Rutas NotFound / Unknown se aceptan con prioridad estandar
    set local-preference 100
    pass
  endif
end-policy

! 3. Aplicar la validacion a los peers de transito de Internet
router bgp 65001
 neighbor 195.20.1.1
  remote-as 64500
  description PEER_UPSTREAM_TIER1_INTERNET
  address-family ipv4 unicast
   route-policy RPKI-VALIDATION-POLICY in
  !
!
commit



## 7. CONFIGURACION DE BGP FLOWSPEC EN CISCO IOS-XR

! 1. Habilitar la familia de direcciones Flowspec en BGP
router bgp 65001
 address-family ipv4 flowspec
 !
 neighbor 10.50.0.100
  remote-as 65001
  description CONTROLADOR_ANTI_DDOS_FLOWSPEC
  address-family ipv4 flowspec
   activate
  !
!

! 2. Ejemplo de regla Flowspec inyectada automaticamente ante un ataque NTP Amplification:
! Filtro: Trafico UDP hacia la victima 200.50.10.85 proveniente del puerto 123 (NTP)
flowspec
 local-install interface all
 address-family ipv4
  class-map type traffic match-all CM-MITIGACION-NTP-DDOS
   match destination-address 200.50.10.85/32
   match protocol udp
   match source-port 123
  !
  policy-map type pbr PM-MITIGACION-DDOS
   class type traffic CM-MITIGACION-NTP-DDOS
    drop                       ! Descartar en hardware a velocidad de linea
   !
  !
!
commit



## 8. COMANDOS DE MONITOREO Y VERIFICACION EN EL CARRIER EDGE

1. Verificar estado de la sesion con el servidor Validador RPKI:
```text
   show bgp rpki server summary
   ! Muestra: Server IP, Status: Established, Records: 450,000 ROAs sincronizados.

2. Consultar el estado de validacion RPKI de un prefijo en la tabla BGP:
   show bgp 8.8.8.0/24
   ! Muestra: "RPKI validation status: valid (Announced by AS15169, matches ROA)"

3. Ver si hay prefijos maliciosos o secuestrados detectados:
   show bgp rpki state invalid
   ! Despliega todas las rutas descartadas automaticamente por no coincidir con el ROA.

4. Ver las reglas y estadisticas de paquetes descartados por BGP Flowspec:
   show flowspec ipv4
```


`cisco
show flowspec statistics
`
