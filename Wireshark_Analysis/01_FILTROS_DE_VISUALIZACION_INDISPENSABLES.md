# 01. GUIA MAESTRA DE FILTROS DE VISUALIZACION (DISPLAY FILTERS CHEAT SHEET)

> **ANALISIS FORENSE DE PAQUETES CON WIRESHARK (WIRESHARK_ANALYSIS)**


---



## 1. OPERADORES LOGICOS Y DE COMPARACION EN WIRESHARK


| Sintaxis | Equivalente | Descripcion |
| :--- | :--- | :--- |
| == | eq | Igual a |
| != | ne | Diferente de |
| > | gt | Mayor que |
| < | lt | Menor que |
| >= | ge | Mayor o igual que |
| <= | le | Menor o igual que |
| && | and | Y logico (Ambas condiciones obligatorias) |
| \|\| | or | O logico (Cualquiera de las dos) |
| ! | not | Negacion logica (Excluir lo que coincida) |
| contains | - | Busqueda de subcadena de texto o byte |
| matches | - | Expresion regular (Regex PCRE) |
| in {} | - | Pertenencia a un conjunto de valores |




## 2. FILTROS DE CAPA 2 (ENLACE) Y CAPA 3 (RED)


### a) Direccionamiento MAC y Ethernet:

   - `eth.addr == 00:50:56:c0:00:08`        -> Filtra por MAC origen o destino.
   - `eth.dst[0] & 1`                        -> Muestra unicamente trafico Broadcast y Multicast.
   - `eth.type == 0x0806`                    -> Filtra exclusivamente tramas ARP.


### b) Deteccion de Fallas ARP:

   - `arp.duplicate-address-detected`        -> ¡CRITICO! Alerta de conflicto de IP (IP Duplicada).
   - `arp.opcode == 1`                       -> Peticiones ARP Request ("¿Quien tiene la IP X?").
   - `arp.opcode == 2`                       -> Respuestas ARP Reply ("La IP X tiene mi MAC Y").


### c) Direccionamiento IPv4 e IPv6:

   - `ip.addr == 192.168.1.100`              -> Paquetes donde la IP sea origen o destino.
   - `ip.src == 10.0.0.1 && ip.dst == 10.0.0.2` -> Comunicacion punto a punto especifica.
   - `ip.addr == 172.16.0.0/16`              -> Filtra subred completa en notacion CIDR.
   - `ipv6.addr == 2001:db8::1`              -> Trafico IPv6 especifico.


### d) Fragmentacion y Problemas de MTU:

   - `ip.flags.df == 1`                      -> Paquetes con bandera "Don't Fragment" activa.
   - `ip.flags.mf == 1`                      -> Paquetes fragmentados (fragmentos intermedios).
   - `ip.ttl < 5`                            -> Paquetes a punto de morir (bucles de enrutamiento).


### e) Analisis de Mensajes de Control ICMP:

   - `icmp.type == 8`                        -> Ping Request (Echo Request).
   - `icmp.type == 0`                        -> Ping Reply (Echo Reply).
   - `icmp.type == 3`                        -> Destination Unreachable (Destino Inalcanzable).
     * `icmp.code == 0`                      -> Red inalcanzable.
     * `icmp.code == 1`                      -> Host inalcanzable.
     * `icmp.code == 3`                      -> Puerto inalcanzable (Servicio apagado o cerrado).
     * `icmp.code == 4`                      -> Fragmentacion requerida pero DF activo (Falla de MTU).
   - `icmp.type == 11`                       -> Time-to-Live Exceeded (Respuesta de un router en Traceroute).



## 3. SERVICIOS ESENCIALES DE INFRAESTRUCTURA (DHCP Y DNS)


### a) Diagnostico de DHCP:

   - `dhcp` (o `bootp`)                     -> Todo el trafico de asignacion de direccionamiento.
   - `bootp.option.dhcp == 1`                -> DHCP Discover (Cliente buscando servidor).
   - `bootp.option.dhcp == 2`                -> DHCP Offer (Oferta de IP del servidor).
   - `bootp.option.dhcp == 3`                -> DHCP Request (Aceptacion formal del cliente).
   - `bootp.option.dhcp == 5`                -> DHCP ACK (Confirmacion final de IP concedida).
   - `bootp.option.dhcp == 6`                -> DHCP NAK (¡Rechazo de asignacion de IP!).


### b) Diagnostico y Auditoria de DNS:

   - `dns.flags.response == 0`               -> Peticiones DNS (Consultas enviadas por clientes).
   - `dns.flags.response == 1`               -> Respuestas de servidores DNS.
   - `dns.time > 0.05`                       -> Consultas DNS lentas (tardaron mas de 50 milisegundos).
   - `dns.flags.rcode != 0`                  -> Consultas DNS fallidas.
     * `dns.flags.rcode == 3`                -> NXDOMAIN (El dominio no existe).
     * `dns.flags.rcode == 2`                -> Server Failure (Servidor DNS caido o saturado).
   - `dns.qry.name contains "malicioso"`     -> Rastreo de peticiones a un dominio sospechoso.



## 4. FILTROS DE PROTOCOLO TCP (CONTROL, CONECTIVIDAD Y ESTADOS)

- `tcp.flags.syn == 1 && tcp.flags.ack == 0` -> Inicios de conexion TCP (SYN iniciales).
- `tcp.flags.reset == 1`                    -> Paquetes TCP RST (Conexion cortada o puerto cerrado).
- `tcp.flags.fin == 1`                      -> Cierre ordenado de conexiones TCP.
- `tcp.port in {80, 443, 8080, 8443}`       -> Trafico web en cualquiera de esos puertos.
- `tcp.time_delta > 0.5`                    -> Muestra pausas o retrasos de mas de 500 ms en la sesion.
- `tcp.stream eq 4`                         -> Aísla la conversacion TCP numero 4 completa.



## 5. PROTOCOLOS WEB Y DE APLICACION (HTTP Y TLS/HTTPS)


### a) Analisis HTTP:

   - `http.request.method == "POST"`         -> Envio de formularios, credenciales o cargas utiles.
   - `http.response.code >= 400`             -> Errores de cliente (404 Not Found, 403 Forbidden).
   - `http.response.code >= 500`             -> Errores internos de servidor web (500, 502 Bad Gateway).
   - `http.time > 1`                         -> Peticiones HTTP donde el backend tardo mas de 1 segundo.


### b) Analisis de Cifrado TLS / SSL (Inspeccion de Metadatos sin descifrar):

   - `tls.handshake.type == 1`               -> TLS Client Hello (Inicio de negociacion criptografica).
   - `tls.handshake.extensions_server_name`  -> SNI (Server Name Indication). Revela a que sitio
                                                web especifico se dirige el usuario (ej. "banco.com"),
                                                incluso si el trafico posterior esta cifrado.
   - `tls.handshake.type == 11`              -> TLS Certificate (Certificado digital enviado por servidor).

## - `tls.record.content_type == 21`         -> TLS Alert (Alertas o fallas de negociacion SSL/TLS).
