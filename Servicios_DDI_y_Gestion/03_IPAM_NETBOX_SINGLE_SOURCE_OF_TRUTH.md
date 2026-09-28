# 03. IPAM CON NETBOX: FUENTE UNICA DE VERDAD (SINGLE SOURCE OF TRUTH)

> **SERVICIOS DE RED CORE (DDI: DNS, DHCP, IPAM) Y GESTION EMPRESARIAL**


---



## 1. LA MUERTE DE LAS HOJAS DE EXCEL: POR QUE NECESITAS UN IPAM MODERNO

Durante decadas, los administradores de red gestionaron direccionamientos IP en
archivos de Microsoft Excel compartidos. Este enfoque provoca:
- Conflictos constantes de IPs duplicadas al conectar nuevos servidores.
- Falta de visibilidad sobre que subredes estan saturadas o desperdiciadas.
- Imposibilidad de automatizar con Ansible, Terraform o Python, ya que un script
  no puede consultar de forma confiable un documento de Excel manual.

NETBOX COMO "SINGLE SOURCE OF TRUTH" (SSoT):
Creado originalmente por DigitalOcean y mantenido por NetBox Labs, NetBox no es
un simple visor de IPs; es el modelo digital de toda la infraestructura fisica
y logica de telecomunicaciones de la empresa.



## 2. MODELO DE DATOS Y JERARQUIA DE NETBOX

NetBox organiza la infraestructura en modulos fuertemente vinculados entre si:

1. Modulo de Organizacion:
   - Tenants: Clientes o unidades de negocio (ej. 'Finanzas', 'Sucursal-Norte').
   - Sites: Ubicaciones geograficas fisicas (ej. 'DC-Queretaro', 'Campus-Guadalajara').

2. Modulo DCIM (Data Center Infrastructure Management):
   - Racks: Racks fisicos de 42U con representacion grafica de elevacion.
   - Device Types: Fabricante, modelo y especificaciones (ej. 'Cisco Catalyst 9300-48P').
   - Devices: Equipos reales con su numero de serie, MAC de gestion y posicion de rack.
   - Interfaces: Puertos fisicos (1G, 10G, 100G), subinterfaces, SVI y Port-Channels.
   - Cables: Conexiones de cableado estructurado punto a punto (puerto switch a patch panel).

3. Modulo IPAM (IP Address Management):
   - Aggregates: Grandes bloques asignados por RIR (ej. LACNIC / ARIN) o RFC 1918 (10.0.0.0/8).
   - Prefixes: Subredes asignadas (ej. 10.10.20.0/24 para VLAN 20 de Finanzas).
   - IP Ranges: Rangos de distribucion (ej. para pools DHCP).
   - IP Addresses: Direcciones IP individuales (/32) vinculadas a una Interfaz fisica o virtual.
   - VRFs: Dominios de enrutamiento independientes para aislamiento multi-tenant.
   - VLANs: Identificadores 802.1Q (VID 1 al 4094) organizados en VLAN Groups.



## 3. AUTOMATIZACION CON PYTHON Y LA LIBRERIA PYNETBOX

NetBox expone una API REST completa bajo OpenAPI / Swagger. La libreria oficial
de Python es 'pynetbox'.


## Script de Python para obtener la siguiente IP libre y aprovisionarla automaticamente:

import pynetbox

# 1. Conexion al servidor NetBox mediante Token de API seguro
NETBOX_URL = "https://netbox.corporativo.com"
API_TOKEN = "0123456789abcdef0123456789abcdef01234567"

nb = pynetbox.api(NETBOX_URL, token=API_TOKEN)

# 2. Buscar el prefijo de la VLAN de Servidores en el Datacenter
prefix = nb.ipam.prefixes.get(prefix="10.10.50.0/24")
print(f"Prefijo encontrado: {prefix.prefix} - Sitio: {prefix.site.name}")

# 3. Consultar y reservar la siguiente IP disponible en la subred
# NetBox calcula automaticamente que IP no esta asignada
available_ips = prefix.available_ips.list()

if available_ips:
    next_ip = prefix.available_ips.create({
        "description": "Servidor Base de Datos Oracle PROD-DB-02",
        "status": "active",
        "dns_name": "db02.corp.local"
    })
    print(f"[EXITO] Direccion IP reservada: {next_ip.address}")
else:
    print("[ERROR] No hay direcciones IP disponibles en esta subred.")

# 4. Vincular la IP creada a la interfaz de red del dispositivo en el rack
device = nb.dcim.devices.get(name="SRV-ORACLE-02")
interface = nb.dcim.interfaces.get(device_id=device.id, name="eth0")

# Asignar la IP a la interfaz fisica
next_ip.assigned_object_type = "dcim.interface"
next_ip.assigned_object_id = interface.id
next_ip.save()
print(f"IP {next_ip.address} asignada a la interfaz {interface.name} de {device.name}")



## 4. WEBHOOKS Y AUTOMATIZACION DIRIGIDA POR EVENTOS (EVENT-DRIVEN)

NetBox puede emitir Webhooks HTTP POST en tiempo real cada vez que un ingeniero
crea, edita o elimina un recurso:

Flujo de Trabajo Automatizado:
1. El ingeniero crea un nuevo Prefijo (10.200.1.0/24) en NetBox para una nueva tienda.
2. NetBox dispara un Webhook POST con el payload en formato JSON hacia AWX/Ansible Tower.
3. El playbook de Ansible se ejecuta de inmediato:
   - Se conecta al Switch Core por SSH / NETCONF.
   - Crea la VLAN en la base de datos de switching.
   - Configura la interfaz SVI con la IP gateway documentada en NetBox.
   - Notifica por canal de Microsoft Teams o Slack con el resultado de la ventana.



## 5. MEJORES PRACTICAS DE GOBERNANZA EN IPAM

- Estados de Prefijos:
  * 'Container': Superred que engloba otras subredes hijas (no asignar a interfaces).
  * 'Active': Subred operativa en produccion.
  * 'Reserved': Bloque apartado para proyectos futuros.
  * 'Deprecated': Subred en proceso de migracion o retiro.
- Prohibir cambios manuales en switches sin documentar previamente en NetBox:

## La red debe ser el REFLEJO de NetBox, nunca al reves.
