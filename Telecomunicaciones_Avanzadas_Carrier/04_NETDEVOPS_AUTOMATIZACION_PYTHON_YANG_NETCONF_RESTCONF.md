# 04. NETDEVOPS, AUTOMATIZACION CARRIER, PYTHON, YANG, NETCONF Y RESTCONF

> **TELECOMUNICACIONES AVANZADAS, REDES DE CARRIER E INFRAESTRUCTURA GLOBAL**


---



## 1. DE LA GESTION POR PANTALLA (SCREEN SCRAPING) A NETDEVOPS

Durante decadas, los ingenieros de red operaron mediante conexiones manuales SSH
y scripts basicos con expresiones regulares (Regex) para parsear texto plano.
Este enfoque fracasa en redes de Carrier debido a:
- Fragilidad: Si el fabricante cambia una coma o un espacio en la salida de 'show ip route',
  el script de Python se rompe.
- Falta de Atomicidad: Si un script de 50 lineas falla en la linea 32, el router queda
  en un estado huerfano inconsistente.
- Ausencia de Validacion de Tipos: La CLI acepta texto plano y los errores se detectan
  demasiado tarde en produccion.

EL PARADIGMA NETDEVOPS:
- Red como Codigo (Infrastructure as Code - IaC).
- Modelos de datos estructurados e independientes del fabricante (YANG).
- APIs programables atómicas con confirmacion o descarte total (NETCONF / RESTCONF).
- Telemetria por transmision continua en microsegundos (Streaming Telemetry gNMI/gRPC).
- Pipelines de Integracion y Entrega Continua (CI/CD) con GitOps.



## 2. MODELADO DE DATOS CON YANG (RFC 6020 / RFC 7950)

YANG (Yet Another Next Generation) es el lenguaje estandarizado por el IETF para
modelar la configuracion y el estado operativo de los dispositivos de red.
No es un lenguaje de programacion, sino un esquema de definicion de datos:

Ecosistemas de Modelos YANG:
1. OpenConfig: Modelos estandares desarrollados por un consorcio de operadores globales
   (Google, Microsoft, AT&T, Comcast) para configurar switches de Cisco, Arista, Juniper
   y Nokia usando exactamente el mismo modelo JSON o XML.
2. Modelos Nativos del Fabricante: Modelos propietarios (ej. Cisco-IOS-XE-native.yang)
   que exponen funciones especificas de hardware no incluidas en OpenConfig.

Ejemplo de Fragmento de Modelo YANG (openconfig-interfaces.yang):
container interfaces {
  list interface {
    key "name";
    leaf name {
      type string;
      description "Nombre del puerto fisico, ej. GigabitEthernet0/0/1";
    }
    leaf enabled {
      type boolean;
      default "true";
      description "Estado administrativo up/down";
    }
    container ipv4 {
      list address {
        key "ip";
        leaf ip {
          type inet:ipv4-address;
        }
        leaf prefix-length {
          type uint8 {
            range "0..32";
          }
        }
      }
    }
  }
}



## 3. PROTOCOLOS DE GESTION: NETCONF VS RESTCONF


| Caracteristica | NETCONF (RFC 6241) | RESTCONF (RFC 8040) |
| :--- | :--- | :--- |
| Protocolo de Transporte SSH (Puerto 830) / TLS | HTTPS (Puerto 443 / 80) |  |
| Formato de Mensajes | XML estructurado en sobres RPC | JSON o XML (application/yang-data+json) |
| Filosofia de Diseno | Orientado a Operaciones RPC remotas | Orientado a Recursos REST Web estandar |
| Bases de Datos | <running/>, <candidate/>, <startup/> | Directo sobre el Datastore unificado |

Capacidad Transaccional Soporta transacciones complejas (commit) Operaciones HTTP atomicas por peticion
Ideal para              Orquestadores Core y Backbone masivo    Aplicaciones Web, Portales y Scripts ligeros

OPERACIONES ESTANDAR DE NETCONF (RPCs):
- <get-config>: Consulta la configuracion de un datastore especifico.
- <edit-config>: Modifica o anade bloques de configuracion.
- <copy-config>: Copia configuraciones completas entre datastores.
- <commit>: Aplica los cambios del datastore candidate al running.
- <lock> / <unlock>: Bloquea el router para evitar que dos scripts escriban al mismo tiempo.



## 4. STREAMING TELEMETRY CON GNMI Y GRPC

El monitoreo tradicional mediante SNMP Polling cada 5 minutos es ciego ante caidas
y micro-rafagas de trafico que saturan los buferes de los switches en milisegundos.

gNMI (gRPC Network Management Interface):
- Desarrollado por Google y OpenConfig. Opera sobre HTTP/2 y serializacion binaria Protocol Buffers (Protobuf).
- Modo STREAM ON_CHANGE: El router NO espera a que nadie le pregunte; en el instante exacto
  en que una interfaz cae o una ruta BGP cambia de estado, empuja un paquete de telemetria al colector.
- Modo STREAM SAMPLE: Emite contadores de paquetes y temperatura a intervalos de 100 ms
  con un impacto de CPU inferior al 1% gracias a la decodificacion por hardware del silicio.



## 5. SCRIPTS PRACTICOS DE PRODUCCION EN PYTHON



## A. Automatizacion con NETCONF y la libreria 'ncclient' (Cisco IOS-XE / Juniper):

import sys
from ncclient import manager

# Parametros de conexion al Router Core
ROUTER_HOST = "10.10.1.1"
ROUTER_PORT = 830
USERNAME = "admin_netdevops"
PASSWORD = "PasswordUltraSegura2026!"

# Payload XML modelado en YANG para configurar una interfaz Loopback y su IP
XML_PAYLOAD = """
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
```text
    <interface>
      <Loopback>
        <name>100</name>
        <description>LOOPBACK_APROVISIONADA_CON_NETCONF</description>
        <ip>
          <address>
            <primary>
              <address>10.255.100.1</address>
              <mask>255.255.255.255</mask>
            </primary>
          </address>
        </ip>
      </Loopback>
    </interface>
  </native>
</config>
"""

def aplicar_netconf():
    with manager.connect(host=ROUTER_HOST, port=ROUTER_PORT, username=USERNAME,
                         password=PASSWORD, hostkey_verify=False,
                         device_params={'name': 'csr'}) as m:
        print("[+] Conectado exitosamente via NETCONF por puerto 830")
        
        # Bloquear datastore para cambio seguro
        m.lock(target='running')
        print("[+] Datastore bloqueado para transaccion exclusiva")
        
        # Aplicar el cambio
        netconf_reply = m.edit_config(target='running', config=XML_PAYLOAD)
        print(f"[+] Respuesta del Router: {netconf_reply}")
        
        m.unlock(target='running')
        print("[+] Datastore liberado. Cambio aplicado atomicamente.")

if __name__ == "__main__":
    aplicar_netconf()
```


## B. Automatizacion con RESTCONF y la libreria 'requests' (JSON):

import requests
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Endpoint RESTCONF estandar segun RFC 8040
URL = "https://10.10.1.1/restconf/data/ietf-interfaces:interfaces"
HEADERS = {
    "Accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}
AUTH = ("admin_netdevops", "PasswordUltraSegura2026!")

# Consultar todas las interfaces del equipo en formato JSON estructurado
response = requests.get(URL, headers=HEADERS, auth=AUTH, verify=False)

if response.status_code == 200:
    data = response.json()
    print("[+] Datos recibidos en formato JSON estructurado:")
    for iface in data['ietf-interfaces:interfaces']['interface']:
        print(f"Interfaz: {iface['name']} - Habilitada: {iface['enabled']}")
else:
    print(f"[-] Error: Codigo HTTP {response.status_code}")



## 6. VALIDACION AUTOMATIZADA CON CISCO PYATS Y GITOPS

En una organizacion NetDevOps, ningun cambio se aplica a produccion sin pasar
por un pipeline de CI/CD:

1. Validacion de Sintaxis (Pre-Check):
   - El desarrollador hace "git push" de la nueva configuracion a un repositorio GitLab.
   - El pipeline ejecuta pruebas sintacticas (yamllint, yanglint).

2. Simulacion en Laboratorio Virtual:
   - El pipeline despliega automaticamente la topologia en un emulador (Containerlab o EVE-NG).
   - Aplica el cambio y valida que los protocolos BGP y OSPF alcancen estado Established.

3. Validacion Operativa con pyATS / Genie:
   - pyATS captura el estado de la red antes del cambio: "pyats learn bgp"
   - Aplica el cambio.
   - pyATS captura el estado posterior y ejecuta un "diff" matematico:
     "pyats diff pre_change_bgp post_change_bgp"
   - Si se detecta una sola ruta BGP perdida o caida de interfaces, el pipeline aborta

y ejecuta un rollback automatico en menos de 10 segundos.
