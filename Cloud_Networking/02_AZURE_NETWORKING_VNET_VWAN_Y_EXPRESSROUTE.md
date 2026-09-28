# 02. AZURE NETWORKING: VNets, SUBREDES, NSGs, UDR, VIRTUAL WAN Y EXPRESSROUTE

> **REDES EN LA NUBE Y ARQUITECTURAS HIBRIDAS (CLOUD NETWORKING & MULTI-CLOUD)**


---



## 1. ARQUITECTURA DE UNA RED VIRTUAL EN AZURE (VNet)

En Microsoft Azure, una VNet (Virtual Network) representa una red aislada por suscripcion
y grupo de recursos dentro de una region geografica (ej. `East US`).
A diferencia de AWS (donde las subredes estan atadas a una Zona de Disponibilidad especifica),
en Azure las subredes abarcan toda la region por defecto.

Direcciones IP Reservadas en cada Subred de Azure:
En cualquier subred creada en Azure (ej. `172.16.1.0/24`), Microsoft reserva 5 IPs:
- `172.16.1.0`: Direccion de red.
- `172.16.1.1`: Gateway predeterminado administrado de la subred.
- `172.16.1.2` y `172.16.1.3`: Asignadas para DNS de Azure e infraestructura interna.
- `172.16.1.255`: Direccion de broadcast de red.



## 2. SEGURIDAD: NETWORK SECURITY GROUPS (NSGs) Y APPLICATION SECURITY GROUPS (ASGs)


### A) NSG (Network Security Group):

   - Es un firewall con estado (Stateful) de Capa 3 y 4.
   - Se puede asociar a:
     * Una Subred completa (protege a todas las VMs que residen en esa subred).
     * Una Tarjeta de Red Virtual (NIC) individual de una maquina virtual.
   - Las reglas se procesan en orden de prioridad numerica (100 a 4096; menor numero = mayor prioridad).
   - Incluye reglas por defecto inmutables (Prioridades 65000 a 65500) como `AllowVnetInBound`
     y `DenyAllInBound`.


### B) ASG (Application Security Group):

   - Permite agrupar maquinas virtuales bajo una etiqueta logica (ej. `ASG_SERVIDORES_WEB`).
   - En las reglas del NSG, en lugar de escribir IPs fijas, se usa el nombre del ASG:
     `Allow TCP 443 from Any to ASG_SERVIDORES_WEB`.



## 3. ENRUTAMIENTO PERSONALIZADO CON UDR (USER DEFINED ROUTES)

Por defecto, Azure enruta automaticamente el trafico entre todas las subredes de una VNet.
Si la empresa instala un Firewall NGFW virtual (Fortinet / Palo Alto / Azure Firewall)
para inspeccionar el trafico interno, se debe sobreescribir el enrutamiento del sistema
mediante una Tabla de Rutas UDR (User-Defined Route) con el siguiente salto tipo "Virtual Appliance".


#### 🌐 DIAGRAMA:

```text
  [SUBRED USUARIOS: 172.16.1.0/24]
        |
        v
  [UDR: 172.16.2.0/24 -> Next Hop Virtual Appliance 172.16.10.4]
        |
        v
  [FIREWALL NGFW VIRTUAL (172.16.10.4) - Inspeccion Antivirus / IPS]
        |
        v
  [SUBRED SERVIDORES: 172.16.2.0/24]
```


## 4. VNet PEERING Y AZURE VIRTUAL WAN (vWAN)


### A) VNet Peering:

   - Interconecta dos VNets con ancho de banda sin limites y latencia minima de fibra.
   - Puede ser local (en la misma region) o Global VNet Peering (cruzando continentes).
   - Permite "Gateway Transit" para que una VNet Spoke comparta la VPN de la VNet Hub.


### B) Azure Virtual WAN (vWAN):

   - Es la solucion empresarial unificada de Microsoft para arquitecturas de gran escala.
   - Proporciona un Virtual Hub en cada region con servicios integrados:
     * VPN Gateway de alta velocidad (IKEv2).
     * ExpressRoute Gateway.
     * Azure Firewall administrado integrado.
     * Enrutamiento de transito automatico entre sucursales y la nube.



## 5. AZURE EXPRESSROUTE Y PEERING PRIVADO

ExpressRoute es una conexion privada dedicada entre el Datacenter de la empresa y
los centros de computo de Microsoft a traves de un proveedor de conectividad (Lumen, Equinix).
- NO viaja por la red publica de Internet (cero jitter, latencia fija garantizada).
- Tipos de Peering:
  * Private Peering: Conecta hacia tus propias maquinas virtuales (VNets) con BGP privado.
  * Microsoft Peering: Conecta directamente hacia servicios PaaS y SaaS publicos
    (Microsoft 365, Teams, Azure Storage, Azure SQL) sin salir por Internet.



## 6. IMPLEMENTACION PRACTICA MEDIANTE AZURE CLI (POWERSHELL / BASH)


! 1. Crear el Grupo de Recursos y la Red Virtual (VNet)
az group create --name RG_CORPORATIVO --location eastus
az network vnet create \
    --name VNET_CORP \
    --resource-group RG_CORPORATIVO \
    --address-prefix 172.16.0.0/16 \
    --subnet-name Subnet_Frontend \
    --subnet-prefix 172.16.1.0/24

! 2. Crear una segunda Subred para el Backend
az network vnet subnet create \
    --name Subnet_Backend \
    --vnet-name VNET_CORP \
    --resource-group RG_CORPORATIVO \
    --address-prefix 172.16.2.0/24

! 3. Crear un Network Security Group (NSG) y permitir HTTPS entrante
az network nsg create --name NSG_WEB --resource-group RG_CORPORATIVO
az network nsg rule create \
    --name Permitir_HTTPS \
    --nsg-name NSG_WEB \
    --resource-group RG_CORPORATIVO \
    --priority 100 \
    --direction Inbound \
    --access Allow \
    --protocol Tcp \
    --destination-port-ranges 443

! 4. Asociar el NSG a la Subred Frontend
az network vnet subnet update \
    --name Subnet_Frontend \
    --vnet-name VNET_CORP \
    --resource-group RG_CORPORATIVO \
    --network-security-group NSG_WEB

! 5. Crear una Tabla de Rutas UDR para forzar el trafico por un Firewall Virtual
az network route-table create --name UDR_FORZAR_FW --resource-group RG_CORPORATIVO
az network route-table route create \
    --name Ruta_Hacia_Backend_via_FW \
    --route-table-name UDR_FORZAR_FW \
    --resource-group RG_CORPORATIVO \
    --address-prefix 172.16.2.0/24 \
    --next-hop-type VirtualAppliance \

## --next-hop-ip-address 172.16.10.4
