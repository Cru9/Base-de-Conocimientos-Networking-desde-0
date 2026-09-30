# 02. BGP (BORDER GATEWAY PROTOCOL) - ARQUITECTURA, ATRIBUTOS Y SELECCION DE RUTA

> **ENRUTAMIENTO AVANZADO Y TECNOLOGIAS WAN (ROUTING & WAN ARCHITECTURE)**


---



## 1. ¿QUE ES BGP Y POR QUE ES EL PROTOCOLO DE INTERNET?

BGP (Border Gateway Protocol Version 4 - RFC 4271) es el unico protocolo de
enrutamiento exterior (EGP) que interconecta a todos los Proveedores de Servicios
de Internet (ISPs), empresas globales, bancos y nubes publicas del planeta.

Diferencias Fundamentales con OSPF / EIGRP:
- OSPF busca siempre "el camino mas rapido / menor costo en milisegundos".
- BGP busca "el camino que cumpla las POLITICAS COMERCIALES y de costo financiero".
  (Por ejemplo: Una empresa puede preferir enviar su trafico por un enlace de 100 Mbps
  porque el ISP es mas barato, antes que por un enlace de 1 Gbps con costo por consumo).
- BGP opera sobre TCP en el puerto 179 (sesiones confiables punto a punto).
- La tabla de enrutamiento BGP global de Internet contiene actualmente mas de 950,000 rutas.



## 2. SISTEMAS AUTONOMOS (AS - AUTONOMOUS SYSTEMS)

Un Sistema Autonomo es una coleccion de redes IP bajo una administracion tecnica
comun y con politicas de enrutamiento uniformes (ej. Google AS15169, Microsoft AS8075).

Rangos de Numeros de Sistema Autonomo (ASN):
- Formato 16 bits (Clasico): 1 a 65,535.
  * Publicos (asignados por RIRs): 1 a 64,495.
  * Privados (uso interno RFC 6996): 64,512 a 65,534.
- Formato 32 bits (Moderno de 4 bytes): Hasta 4,294,967,295 (ej. AS13335 Cloudflare).



## 3. COMPARATIVA: eBGP (BGP EXTERNO) vs iBGP (BGP INTERNO)


| Caracteristica | eBGP (External BGP) | iBGP (Internal BGP) |
| :--- | :--- | :--- |
| Ubicacion | Entre diferentes ASNs | Dentro del mismo ASN |
| Distancia Administrativa (AD) 20 (en Cisco) | 200 (en Cisco) |  |
| TTL del paquete TCP | TTL = 1 (enlace fisico directo) | TTL = 255 (a traves de la red) |
| Atributo Next-Hop | Cambia a la IP del router local | NO CAMBIA (requiere next-hop-self) |
| Regla de Reenvio | Libre | Regla de Split-Horizon iBGP |


La Regla de Split-Horizon de iBGP y Soluciones de Escalabilidad:
- Regla: "Un router iBGP NO propagara a otro vecino iBGP una ruta aprendida de un tercer vecino iBGP".
  (Disenado para prevenir bucles de enrutamiento dentro del AS).
- Problema: Para que todos los routers conozcan las rutas, se requeria una malla
  completa (Full Mesh) de sesiones iBGP: N*(N-1)/2 sesiones (imposible a gran escala).
- Solucion Moderna: Despliegue de BGP Route Reflectors (RR).
  El Route Reflector actua como concentrador central y tiene permiso para retransmitir
  rutas aprendidas de clientes iBGP a otros clientes sin requerir malla completa.



## 4. ATRIBUTOS BGP Y EL ALGORITMO DE SELECCION DE MEJOR RUTA (BEST PATH)

BGP no usa una simple metrica numerica; utiliza ATRIBUTOS que evalua en un orden
estricto paso a paso.

El Algoritmo de Seleccion de Mejor Ruta (Memorizar para Certificaciones):
Cuando BGP recibe multiples rutas hacia el mismo destino, aplica esta cascada eliminatoria:

1. WEIGHT (Peso):
   - Mayor Weight Gana. (Cisco propietario, local al router; no se anuncia a nadie).
2. LOCAL PREFERENCE (Preferencia Local):
   - Mayor Local Preference Gana. (Estandar, propagado dentro de todo el AS local. Default = 100).
   - Se usa para decidir por cual ISP SALIR de la empresa (Control de Trafico Saliente).
3. ORIGEN LOCAL:
   - Prefiere rutas originadas localmente en este router (`network` o `redistribute`).
4. AS-PATH MAS CORTO:
   - Menor cantidad de saltos de Sistemas Autonomos gana.
   - Tecnica de Ingenieria de Trafico: "AS-Path Prepending" (repetir artificialmente
     el propio ASN para hacer que un enlace parezca mas largo y los demas no lo usen).
5. CODIGO DE ORIGEN (Origin Code):
   - Prefiere IGP (i) sobre EGP (e), y este sobre Incomplete (?).
6. MENOR MED (Multi-Exit Discriminator):
   - Menor valor de MED gana. Se anuncia a un AS vecino para sugerirle por cual
     de sus enlaces debe ENTRAR el trafico a nuestra empresa (Control de Trafico Entrante).
7. eBGP SOBRE iBGP:
   - Prefiere rutas aprendidas por eBGP sobre las aprendidas por iBGP.
8. MENOR METRICA IGP HACIA EL NEXT-HOP:
   - Prefiere el camino con menor costo interno (OSPF) hacia el router de salida.
9. MENOR BGP ROUTER-ID:
   - Desempate final: la direccion IP mas baja del identificador del router.



## 5. INGENIERIA DE TRAFICO CON PREFIX-LISTS Y ROUTE-MAPS

BGP permite manipular atributos de forma granular mediante Route-Maps:

Ejemplo: Forzar que el trafico hacia Internet salga por el ISP-A (Mayor Local-Pref):
  route-map PREFERIR_ISP_A permit 10
   set local-preference 200
  exit

  router bgp 65001
   neighbor 203.0.113.1 route-map PREFERIR_ISP_A in



## 6. COMANDOS DE DIAGNOSTICO DE BGP (CISCO / HUAWEI)

CISCO:
```cisco
  SW# show ip bgp summary           (Verificar estado de adyacencias; debe mostrar prefijos recibidos)
  SW# show ip bgp                   (Ver tabla BGP completa con simbolos '>' para mejor ruta)
  SW# show ip bgp 8.8.8.8           (Ver todos los atributos detallados de una ruta)
  SW# show ip bgp neighbors 203.0.113.1 advertised-routes (Ver que rutas estamos enviando al ISP)
  SW# show ip bgp neighbors 203.0.113.1 received-routes   (Ver que rutas nos envia el ISP)
```

HUAWEI:
```cisco
  SW> display bgp peer
  SW> display bgp routing-table
```


## SW> display bgp routing-table 8.8.8.8
