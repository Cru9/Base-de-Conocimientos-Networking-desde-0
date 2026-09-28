# 01. AWS NETWORKING: VPCs, SUBREDES, NAT GATEWAY, SECURITY GROUPS Y TRANSIT GATEWAY

> **REDES EN LA NUBE Y ARQUITECTURAS HIBRIDAS (CLOUD NETWORKING & MULTI-CLOUD)**


---



## 1. ARQUITECTURA FUNDAMENTAL DE UNA VPC (AMAZON WEB SERVICES)

Una VPC (Virtual Private Cloud) es una red virtual aislada logicamente dentro de la
nube de Amazon AWS. Cada VPC se crea dentro de una Region especifica (ej. `us-east-1` N. Virginia)
y se le asigna un bloque CIDR privado primario (ej. `10.100.0.0/16` = 65,536 direcciones IP).

Regla Inviolable de Direccionamiento IP en AWS:
En cada subred que se crea en AWS, Amazon reserva automaticamente CINCO (5) direcciones IP:
Ejemplo en una subred `10.100.1.0/24`:
- `10.100.1.0`: Direccion de red.
- `10.100.1.1`: Router virtual de la VPC (Gateway predeterminado de la subred).
- `10.100.1.2`: Servidor DNS administrado por Amazon (AmazonProvidedDNS).
- `10.100.1.3`: Reservada por AWS para uso futuro.
- `10.100.1.255`: Direccion de broadcast de red (aunque AWS no soporta broadcast).
- IPs utiles reales para maquinas EC2 = 251 direcciones.



## 2. SUBREDES PUBLICAS vs SUBREDES PRIVADAS Y COMPONENTES GATEWAY


### A) Subred Publica (Public Subnet):

   - Aloja recursos accesibles directamente desde Internet (Balanceadores ALB, Bastion Hosts).
   - Su Tabla de Enrutamiento tiene una ruta explicita `0.0.0.0/0` apuntando hacia un
     Internet Gateway (`igw-xxxx`).
   - Las instancias EC2 reciben una IP publica IPv4 elastica (Elastic IP).


### B) Subred Privada (Private Subnet):

   - Aloja recursos criticos (Bases de datos RDS, servidores de aplicaciones de backend).
   - NO tiene ruta directa al Internet Gateway.
   - Para descargar parches de seguridad de Internet sin ser visibles desde el exterior,
     su tabla de rutas envia `0.0.0.0/0` hacia un NAT Gateway administrado (`nat-xxxx`)
     alojado en la Subred Publica.

DIAGRAMA DE ARQUITECTURA DE UNA VPC DE PRODUCCION:
```text
+-------------------------------------------------------------------------------+
|                            AMAZON AWS VPC (10.100.0.0/16)                     |
|                                                                               |
|   +------------------------------------+                                      |
|   |         INTERNET GATEWAY (IGW)     | <======== INTERNET GLOBAL            |
|   +-----------------+------------------+                                      |
|                     |                                                         |
|   +-----------------v------------------+                                      |
|   | SUBRED PUBLICA (10.100.1.0/24)     |                                      |
|   |  - Balanceador de Carga (ALB)      |                                      |
|   |  - NAT Gateway (IP Elastica Pub.)  |                                      |
|   +-----------------+------------------+                                      |
|                     |                                                         |
|   +-----------------v------------------+                                      |
|   | SUBRED PRIVADA (10.100.2.0/24)     |                                      |
|   |  - Servidores Backend (EC2)        |                                      |
|   |  - Ruta 0.0.0.0/0 -> NAT Gateway   |                                      |
|   +-----------------+------------------+                                      |
|                     |                                                         |
|   +-----------------v------------------+                                      |
|   | SUBRED BASE DE DATOS (10.100.3.0)  |                                      |
|   |  - Cluster RDS PostgreSQL / MySQL  | (Aislada: Cero acceso a Internet)    |
|   +------------------------------------+                                      |
+-------------------------------------------------------------------------------+
```


## 3. SEGURIDAD: SECURITY GROUPS (STATEFUL) vs NACLs (STATELESS)


| Caracteristica | Security Group (SG) | Network ACL (NACL) |
| :--- | :--- | :--- |
| Nivel de Operacion | A nivel de Interfaz de Red (ENI) | A nivel de Subred completa |
| Estado (Stateful/Stateless)STATEFUL (Con estado) | STATELESS (Sin estado) |  |
| (Si entra peticion, la respuesta | (Si permites entrada, DEBES |  |
| sale automaticamente) | permitir salida explicitamente) |  |
| Tipos de Reglas | Solo reglas de PERMITIR (Permit) | Reglas de PERMITIR y DENEGAR (Deny) |
| Orden de Evaluacion | Se evaluan TODAS las reglas | Se evaluan en orden numerico estricto |
| en conjunto | (Regla 100, 110, 200, etc.) |  |




## 4. VPC PEERING Y SUS LIMITACIONES DE TRANSITIVIDAD

VPC Peering es una conexion punto a punto directa entre dos VPCs en la red interna de AWS.
- Ventaja: Trafico cifrado en hardware, alta velocidad (hasta 100 Gbps), baja latencia.
- LIMITACION CRITICA: ¡NO TIENE ENRUTAMIENTO TRANSITIVO!
  Si VPC-A se conecta a VPC-B, y VPC-B se conecta a VPC-C:
  VPC-A NO PUEDE hablar con VPC-C a traves de VPC-B.
  Para 20 VPCs conectadas entre si, se requerian 190 enlaces Peering en malla (Inescalable).



## 5. AWS TRANSIT GATEWAY (TGW): EL CONCENTRADOR HUB-AND-SPOKE EMPRESARIAL

AWS Transit Gateway (TGW) es un router virtual administrado a escala masiva (hasta 50 Gbps
por attachment) que resuelve el problema del enrutamiento transitivo.
- Actua como el Hub central que interconecta miles de VPCs, VPNs IPsec de sucursales
  y conexiones dedicadas AWS Direct Connect.
- Soporta multiples Tablas de Enrutamiento TGW (equivalente a VRFs en la nube), permitiendo
  aislar el trafico de Produccion del trafico de Desarrollo.

DIAGRAMA EMPRESARIAL CON TRANSIT GATEWAY:
         [VPC PRODUCCION]                   [VPC DESARROLLO]
          (10.10.0.0/16)                     (10.20.0.0/16)
                 \                                 /
                  \                               /
```text
          +--------v-----------------------------v--------+
          |           AWS TRANSIT GATEWAY (TGW)          |
          |       (Router Central Multi-VPC con BGP)     |
          +-----------------------+----------------------+
                                  |
                   +--------------+--------------+
                   |                             |
                   v (VPN IPsec BGP)             v (Direct Connect 10G)
          [SUCURSAL CORPORATIVA]        [DATACENTER ON-PREMISES]
```



## 6. IMPLEMENTACION PRACTICA: CREACION DE INFRAESTRUCTURA MEDIANTE AWS CLI


! 1. Crear la VPC Corporativa
aws ec2 create-vpc --cidr-block 10.100.0.0/16 --tag-specifications "ResourceType=vpc,Tags=[{Key=Name,Value=VPC_CORPORATIVA}]"

! 2. Crear las Subredes Publica y Privada en la Zona de Disponibilidad us-east-1a
aws ec2 create-subnet --vpc-id vpc-0123456789abcdef0 --cidr-block 10.100.1.0/24 --availability-zone us-east-1a
aws ec2 create-subnet --vpc-id vpc-0123456789abcdef0 --cidr-block 10.100.2.0/24 --availability-zone us-east-1a

! 3. Crear y adjuntar el Internet Gateway (IGW)
aws ec2 create-internet-gateway
aws ec2 attach-internet-gateway --internet-gateway-id igw-0123456789abcdef0 --vpc-id vpc-0123456789abcdef0

! 4. Crear Elastic IP y NAT Gateway para la Subred Privada
aws ec2 allocate-address --domain vpc
aws ec2 create-nat-gateway --subnet-id subnet-publica1 --allocation-id eipalloc-0123456789

! 5. Enrutamiento en las Tablas de la VPC
! Tabla Publica: Salida a Internet via IGW
aws ec2 create-route --route-table-id rtb-publica --destination-cidr-block 0.0.0.0/0 --gateway-id igw-0123456789abcdef0
! Tabla Privada: Salida a Internet via NAT Gateway
aws ec2 create-route --route-table-id rtb-privada --destination-cidr-block 0.0.0.0/0 --nat-gateway-id nat-0123456789abcdef0

! 6. Interconectar la VPC al Transit Gateway (TGW Attachment)
aws ec2 create-transit-gateway-vpc-attachment \
    --transit-gateway-id tgw-0123456789abcdef0 \
    --vpc-id vpc-0123456789abcdef0 \

## --subnet-ids subnet-privada1
