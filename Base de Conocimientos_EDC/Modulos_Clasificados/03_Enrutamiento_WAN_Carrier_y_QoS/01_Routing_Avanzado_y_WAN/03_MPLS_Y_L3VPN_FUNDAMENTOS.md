# 03. FUNDAMENTOS DE MPLS (MULTIPROTOCOL LABEL SWITCHING) Y MPLS L3VPN

> **ENRUTAMIENTO AVANZADO Y TECNOLOGIAS WAN (ROUTING & WAN ARCHITECTURE)**


---



## 1. ¿QUE ES MPLS Y POR QUE REVOLUCIONO LAS REDES WAN?

En las redes IP tradicionales sin MPLS:
- Cada router intermedio en el camino debe abrir el paquete de Capa 3, leer la
  direccion IP destino de 32 o 128 bits, y realizar una busqueda de coincidencia
  mas larga (Longest Prefix Match) en una tabla de enrutamiento con cientos de miles de rutas.
- Este proceso consumia ciclos intensivos de CPU y memoria.

La Revolucion de MPLS (Multi-Protocol Label Switching - Capa 2.5):
- En lugar de examinar direcciones IP complejas en cada salto, MPLS inserta una
  pequena ETIQUETA numerica de 20 bits en la cabecera del paquete.
- Los routers del nucleo (Core) unicamente leen la etiqueta y la "intercambian"
  (Label Swapping) a velocidad de silicio por hardware en nanosegundos.
- Independencia del protocolo: Puede transportar IPv4, IPv6, Ethernet o Frame Relay.



## 2. ROLES DE ROUTERS EN UNA RED MPLS


| Termino | Nombre Completo | Ubicacion | Funcion |
| :--- | :--- | :--- | :--- |
| CE | Customer Edge | Red del Cliente | Router normal del cliente; NO sabe que |

                                                     existe MPLS (solo habla IP estandar).
PE / LER   Provider Edge /        Frontera ISP       Router de borde del proveedor. Recibe el
           Label Edge Router                         paquete IP del cliente, le agrega la
                                                     etiqueta (PUSH) o se la retira (POP).
P / LSR    Provider Router /      Nucleo del ISP     Router del core del proveedor. Conmuta
           Label Switching Router (Backbone)         etiquetas a gran velocidad (SWAP) sin
                                                     mirar jamas las direcciones IP de los clientes.



## 3. ESTRUCTURA DEL ENCABEZADO SHIM DE MPLS (32 BITS)

El encabezado MPLS se inserta exactamente entre el encabezado de Capa 2 (Ethernet)
y el encabezado de Capa 3 (IPv4):

```text
+-------------------+----------------+----------------+--------------------+
| Encabezado Capa 2 | Encabezado     | Encabezado     | Carga Util (Datos) |
| (Ethernet)        | SHIM MPLS (32b)| Capa 3 (IPv4)  |                    |
+-------------------+----------------+----------------+--------------------+

Campos del Encabezado MPLS:
```


| Campo | Bits | Descripcion |
| :--- | :--- | :--- |
| Label (Etiqueta) 20 bits | Numero de la etiqueta (Valores de 0 a 1,048,575). |  |

                          (Valores 0 a 15 reservados; ej. Label 3 = Implicit Null).
TC / EXP         3 bits   Traffic Class / Experimental: Mapea la Calidad de Servicio (QoS CoS).
S (Bottom Stack) 1 bit    Fondo de Pila: Vale 1 si es la ultima etiqueta en la pila;
                          vale 0 si hay mas etiquetas apiladas debajo.
TTL              8 bits   Time-to-Live: Copiado del TTL de IP para prevenir bucles.



## 4. OPERACIONES DE ETIQUETAS Y PROTOCOLO LDP

Operaciones Basicas sobre Etiquetas:
- PUSH (Empujar / Imponer): Insertar una etiqueta nueva encima del paquete (se hace en el PE de entrada).
- SWAP (Intercambiar): Cambiar una etiqueta entrante por una saliente (se hace en los routers P).
- POP (Retirar): Remover la etiqueta superior para exponer el paquete IP o la siguiente etiqueta.

Protocolo LDP (Label Distribution Protocol - RFC 5036):
- Protocolo mediante el cual los routers vecinos del proveedor se intercambian y
  aprenden que etiqueta representa a cada red IP (FEC - Forwarding Equivalence Class).
- Utiliza UDP 646 para descubrimiento de vecinos y TCP 646 para la sesion de intercambio.

Penultimate Hop Popping (PHP - Optimizacion de Examen):
- El router P anterior al PE de destino le retira la etiqueta de transporte exterior
  (usando la etiqueta reservada 3 - Implicit Null).
- De esta forma, el PE de salida solo tiene que procesar una busqueda y no dos,
  ahorrando CPU en el router de borde.



## 5. ARQUITECTURA MPLS L3VPN (RFC 4364 - MULTI-TENANCY)

Permite que un solo proveedor de telecomunicaciones conecte las sucursales de miles
de empresas clientes diferentes de forma totalmente aislada y privada:

Los 3 Componentes Fundamentales de una L3VPN:


### a) VRF (Virtual Routing and Forwarding):

   - Es una "tabla de enrutamiento virtual e independiente" dentro del router PE.
   - Permite que el Cliente "Banco X" y el Cliente "Hospital Y" usen ambos las mismas
     direcciones IP privadas (ej. `10.0.0.0/24`) sin que su tráfico se cruce jamas.


### b) RD (Route Distinguisher - 64 bits):

   - Hace que la IP del cliente sea globalmente unica en la red del ISP.
   - Si dos clientes usan la IP `10.1.1.0/24`, el PE les agrega el RD:
     * Banco X: `65000:100:10.1.1.0/24` (Ruta VPNv4 unica).
     * Hospital Y: `65000:200:10.1.1.0/24` (Ruta VPNv4 unica).


### c) RT (Route Target - Extended BGP Community):

   - Define las politicas de importacion y exportacion: que sucursales tienen derecho
     a comunicarse con que otras sucursales (Topologia en Malla o Hub-and-Spoke).

El Funcionamiento con Doble Etiqueta (MP-BGP):
Los paquetes en una MPLS L3VPN llevan DOS etiquetas apiladas:
1. Etiqueta Exterior (Transport Label - LDP): Lleva el paquete a traves del nucleo
   hasta el PE correcto.
2. Etiqueta Interior (VPN Label - MP-BGP): Al llegar al PE de destino, le indica
   a que cliente y a que interfaz VRF especifica debe entregarse el paquete.



## 6. COMANDOS DE DIAGNOSTICO EN CISCO Y HUAWEI

CISCO:
```cisco
  SW# show mpls interfaces
  SW# show mpls ldp neighbor
  SW# show mpls forwarding-table      (Ver la tabla LFIB de conmutacion de etiquetas)
  SW# show ip vrf                    (Ver las VRFs creadas y sus interfaces asignadas)
  SW# show ip route vrf CLIENTE_BANCO (Ver la tabla de rutas de un cliente especifico)
```

HUAWEI:
```cisco
  SW> display mpls ldp session
  SW> display mpls lsp
```


## SW> display ip vpn-instance
