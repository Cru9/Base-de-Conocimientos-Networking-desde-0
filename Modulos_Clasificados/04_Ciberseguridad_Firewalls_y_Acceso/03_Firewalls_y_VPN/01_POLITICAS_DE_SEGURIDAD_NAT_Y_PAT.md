# 01. POLITICAS DE SEGURIDAD, TIPOS DE NAT/PAT Y DESCIFRADO SSL/TLS

> **FIREWALLS DE PROXIMA GENERACION (NGFW) Y VPNs EMPRESARIALES**


---



## 1. FUNDAMENTOS DE TRADUCCION DE DIRECCIONES DE RED (NAT)

NAT (Network Address Translation - RFC 1631 / 3022) resolvio el agotamiento de
direcciones IPv4 permitiendo que millones de computadoras con direcciones privadas
(RFC 1918) naveguen en Internet utilizando una cantidad minima de IPs publicas.

Ademas de ahorrar direcciones, NAT aporta una barrera de seguridad natural:
Oculta la topologia y direccionamiento interno de la empresa al mundo exterior.



## 2. TIPOS DE NAT EXPLICADOS CON EJEMPLOS


### a) NAT Estatico (Static NAT - Uno a Uno):

   - Mapea de forma permanente una unica IP privada a una unica IP publica.
   - Es bidireccional (permite conexiones salientes y entrantes).
   - Uso: Servidores publicos en la DMZ (Servidores Web, Correo SMTP, VPNs).
   - Ejemplo: `192.168.50.10` (DMZ) <====> `203.0.113.15` (IP Publica).


### b) NAT Dinamico (Pool de Direcciones):

   - Asigna dinamicamente una IP publica de un pool a una IP privada mientras
     la sesion este activa, segun el orden de llegada (First-Come, First-Served).
   - Desventaja: Si el pool tiene 5 IPs publicas y un 6to empleado intenta navegar,
     su conexion es rechazada. (Rara vez utilizado hoy en dia).


### c) PAT (Port Address Translation / NAT Overload / Source NAT - SNAT):

   - La tecnologia mas utilizada del mundo.
   - Permite que miles de computadoras de una oficina salgan a Internet compartiendo
     UNA SOLA direccion IP publica.
   - ¿Como funciona la magia de PAT?
     El firewall sustituye la IP privada por su propia IP publica y REEMPLAZA EL
     PUERTO ORIGEN por un numero de puerto efimero unico (ej. 51001, 51002).
     Cuando el servidor web de Internet responde, envia los datos a ese puerto,
     y el firewall consulta su tabla de traduccion para devolver el paquete a la PC correcta.
     *Capacidad: Hasta ~64,000 conexiones concurrentes por IP publica.


### d) Destination NAT (DNAT / Port Forwarding / Virtual IP - VIP):

   - Traduce la IP o puerto de DESTINO de un paquete entrante desde Internet.
   - Permite que usuarios externos consulten `https://203.0.113.5:443` y el firewall
     redirija esa solicitud al servidor interno `192.168.50.20:8080`.


### e) Hairpin NAT (NAT Loopback):

   - Permite que una computadora dentro de la oficina acceda a un servidor interno
     escribiendo su nombre de dominio publico (`https://portal.empresa.com`),
     haciendo que el firewall traduzca la peticion internamente sin enviarla a Internet.



## 3. ORDEN DE EVALUACION DE POLITICAS EN UN NGFW (FLUJO DE PROCESAMIENTO)

Cuando un paquete ingresa a un Firewall de Proxima Generacion, sigue este orden estricto:

1. Ingreso por la Interfaz Fisica y Verificacion de Capa 2.
2. Identificacion de la Zona de Seguridad de Origen (Source Zone).
3. Evaluacion de Destination NAT (DNAT) para saber a que IP real debe dirigirse.
4. Consulta de Ruta de Enrutamiento (Route Lookup) para determinar la Zona de Salida.
5. Evaluacion de Politicas de Seguridad (Security Policies) de ARRIBA HACIA ABAJO:
   - Coincidencia de Primer Acierto (First-Match Rule): En cuanto una regla coincide
     con la Zona Origen, Zona Destino, Usuario, Aplicacion y Horario, se ejecuta
     la accion (Permit o Deny) y SE DETIENE la evaluacion de las demas reglas.
6. Inspeccion de Perfiles de Seguridad (IPS, Antivirus, Filtrado Web, Sandbox).
7. Aplicacion de Source NAT (SNAT / PAT) para enmascarar la IP saliente.
8. Egreso por la interfaz fisica hacia Internet o la LAN.



## 4. EL PUNTO CIEGO DEL 90%: DESCIFRADO SSL/TLS (SSL FORWARD PROXY)

El Problema Critico:
Mas del 90% de todo el trafico de Internet viaja cifrado con HTTPS (TLS 1.3).
Si un empleado descarga un archivo infectado con Ransomware o una fuga de datos
se envia por HTTPS, un firewall tradicional NO PUEDE VER EL ARCHIVO porque el
contenido esta cifrado. El firewall es ciego.

La Solucion: Descifrado SSL Forward Proxy (Inspeccion Profunda TLS):
1. El firewall se interpone como intermediario transparente entre la PC e Internet.
2. Cuando el empleado entra a un sitio web, el firewall establece la conexion HTTPS
   con el servidor web remoto.
3. El firewall descifra el trafico en su propio hardware (ASIC especializado).
4. El motor IPS y Antivirus escanean el archivo descargado en texto plano.
5. Si el archivo esta limpio, el firewall lo vuelve a cifrar al vuelo utilizando
   un certificado digital emitido por la Autoridad Certificadora (CA) de la empresa
   y se lo entrega a la PC del usuario.

Exclusiones de Privacidad Obligatorias (Compliance):
Por normativas legales (GDPR, HIPAA, secreto bancario), las categorias de
Servicios Financieros, Banca en Linea y Salud NUNCA deben descifrarse.



## 5. MEJORES PRACTICAS PARA REGLAS DE CORTAFUEGOS

1. NUNCA use "Any / Any / Allow" en ninguna regla entre zonas distintas.
2. Defina reglas especificas para APLICACIONES (ej. permitir `zoom-base` y `office365`)
   en lugar de solo abrir puertos genericos TCP 80/443.
3. Siempre deje la regla final de "Bloqueo Implicito con Registro" (Implicit Deny All Log)
   al fondo de la tabla para auditar cualquier intento de conexion no autorizada.

## 4. Active perfiles de IPS en todas las politicas que comuniquen la DMZ hacia la LAN.
