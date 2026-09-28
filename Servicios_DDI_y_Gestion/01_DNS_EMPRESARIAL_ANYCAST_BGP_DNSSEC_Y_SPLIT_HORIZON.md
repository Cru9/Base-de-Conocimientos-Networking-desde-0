# 01. DNS EMPRESARIAL, ANYCAST BGP, SPLIT-HORIZON Y DNSSEC

> **SERVICIOS DE RED CORE (DDI: DNS, DHCP, IPAM) Y GESTION EMPRESARIAL**


---



## 1. ARQUITECTURA DE RESOLUCION DNS EMPRESARIAL

El sistema de nombres de dominio (DNS - RFC 1034 / 1035) opera en dos roles clave:

1. DNS Autoritativo:
   - Almacena y administra las zonas originales de la empresa (ej. 'corp.local' o
     'miempresa.com'). Es la fuente oficial de registros A, AAAA, CNAME, MX, TXT y SRV.

2. DNS Recursivo / Resolutor (Resolver):
   - Recibe las peticiones de las PCs y dispositivos de la red.
   - Si no tiene la respuesta en su memoria cache, navega por la jerarquia mundial
     de DNS (Root Servers -> TLD Servers -> Autoritativo) hasta obtener la IP.



## 2. ANYCAST DNS CON BGP: MAXIMA ALTA DISPONIBILIDAD Y BAJA LATENCIA

En grandes corporaciones, configurar una IP primaria y secundaria tradicional
(Unicast) causa problemas: si el DNS primario cae, los clientes tardan entre
3 y 5 segundos de timeout antes de intentar con el secundario.

Solucion de Nivel ISP / Carrier: Anycast DNS
Multiples servidores DNS ubicados en distintos Datacenters comparten EXACTAMENTE
la misma direccion IP virtual (ejemplo: 10.50.0.1/32).

DIAGRAMA ANYCAST DNS CON BGP:

   [ Datacenter Norte ]                               [ Datacenter Sur ]
   Servidor DNS 01                                    Servidor DNS 02
   IP Loopback: 10.50.0.1/32                          IP Loopback: 10.50.0.1/32
         |                                                  |
    (Anuncia 10.50.0.1/32 por BGP)                     (Anuncia 10.50.0.1/32 por BGP)
         |                                                  |
         v                                                  v
    [ Router BGP DC Norte ]                            [ Router BGP DC Sur ]
         \                                                  /
          \============= NUCLEO DE RED WAN IP =============/
                                  ^
                                  | (Enruta por menor distancia AS-Path/IGP)
                          [ Clientes / PCs ]
                          DNS: 10.50.0.1

Ventajas de Anycast:
1. Conmutacion instantanea (Failover Subsegundo): Si el Servidor DNS 01 cae, su daemon
   BGP (BIRD/FRR) retira la ruta 10.50.0.1/32 y la red redirige el trafico al DNS 02.
2. Latencia minima: Los usuarios de Monterrey consultan al DC Norte; los de CDMX
   consultan al DC Sur, usando siempre la misma IP.



## 3. SPLIT-HORIZON DNS (VISTAS INTERNAS VS EXTERNAS)

Permite que un mismo nombre FQDN responda con una IP diferente segun quien pregunte:
- Usuario en Internet: pregunta por 'erp.miempresa.com' -> Responde IP Publica: 200.50.10.80
- Usuario en la LAN: pregunta por 'erp.miempresa.com'   -> Responde IP Privada: 10.10.50.80


## Configuracion en Linux BIND9 (/etc/bind/named.conf.local):

! Definir ACL de redes internas
acl "redes-internas" {
    10.0.0.0/8;
    172.16.0.0/12;
    192.168.0.0/16;
    localhost;
};

! Vista Interna para empleados
view "interna" {
    match-clients { "redes-internas"; };
    recursion yes;

    zone "miempresa.com" {
        type master;
        file "/etc/bind/zones/db.miempresa.com.interna";
    };
};

! Vista Externa para clientes de Internet
view "externa" {
    match-clients { any; };
    recursion no;     ! Prohibir recursion a desconocidos (evita ataques de amplificacion)

    zone "miempresa.com" {
        type master;
        file "/etc/bind/zones/db.miempresa.com.externa";
    };
};



## 4. ARCHIVO DE ZONA DNS ESTANDAR (RFC 1035)

Ejemplo de archivo de zona interna (/etc/bind/zones/db.miempresa.com.interna):
$TTL 86400
@   IN  SOA ns1.miempresa.com. admin.miempresa.com. (
            2026092601 ; Serial (AAAAMMDD + revision)
            3600       ; Refresh (1 hora)
            1800       ; Retry (30 minutos)
            604800     ; Expire (1 semana)
            86400 )    ; Minimum TTL (1 dia)

; Servidores de Nombres autoritativos
@       IN  NS      ns1.miempresa.com.
@       IN  NS      ns2.miempresa.com.

; Registros A (IPv4)
ns1     IN  A       10.50.0.1
ns2     IN  A       10.50.0.2
dc01    IN  A       10.10.10.10
erp     IN  A       10.10.50.80
mail    IN  A       10.10.20.25

; Registros MX (Servidor de Correo)
@       IN  MX  10  mail.miempresa.com.

; Registros CNAME (Alias)
www     IN  CNAME   erp.miempresa.com.
portal  IN  CNAME   erp.miempresa.com.

; Registro TXT (Validacion SPF para evitar spoofing de correo)
@       IN  TXT     "v=spf1 ip4:200.50.10.25 -all"



## 5. DNSSEC: PROTECCION CONTRA ENVENENAMIENTO DE CACHE (CACHE POISONING)

DNSSEC anade criptografia de clave publica a los registros DNS mediante firmas
digitales para certificar que la respuesta proviene del servidor legitimo y no ha
sido alterada en transito:
- RRSIG (Resource Record Signature): Firma criptografica que acompana a cada registro.
- DNSKEY: Clave publica de la zona utilizada para verificar las firmas.
- DS (Delegation Signer): Hash de la clave DNSKEY entregado al registrador del dominio
  para formar la cadena de confianza con la zona superior (.com / .net).



## 6. COMANDOS DE DIAGNOSTICO Y VALIDACION DNS

1. Consulta detallada con tiempos de respuesta en milisegundos:
   dig @10.50.0.1 erp.miempresa.com A

2. Rastrear toda la cadena de resolucion jerarquica desde la raiz:
   dig +trace erp.miempresa.com

3. Verificar registros especificos (MX, TXT, SRV de Active Directory):
   dig _ldap._tcp.corp.local SRV
   dig miempresa.com TXT

4. Probar transferencia de zona completa (auditoria de seguridad):
   dig @ns1.miempresa.com miempresa.com AXFR

## ! Debe devolver "Transfer failed" si el servidor esta correctamente protegido.
