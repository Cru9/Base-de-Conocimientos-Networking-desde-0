# 03. GOOGLE CLOUD (GCP): VPC GLOBAL, CLOUD ROUTER CON BGP, CLOUD NAT Y SHARED VPC

> **REDES EN LA NUBE Y ARQUITECTURAS HIBRIDAS (CLOUD NETWORKING & MULTI-CLOUD)**


---



## 1. LA VENTAJA ARQUITECTONICA DE GOOGLE: VPC GLOBAL NATIVA

A diferencia de AWS y Azure (donde las redes virtuales son regionales y requieren
peering o gateways para hablar con otra region), en Google Cloud (GCP) una VPC
es un recurso GLOBAL por naturaleza.

- Una sola VPC en GCP abarca TODOS los continentes y Datacenters del planeta.
- Una maquina virtual en Iowa (`us-central1`) puede comunicarse con una maquina
  virtual en Tokio (`asia-northeast1`) utilizando sus direcciones IP privadas
  internas directas con latencia minima sobre la red privada de fibra optica de Google,
  sin necesidad de VPNs, sin NAT y sin enrutadores de transito intermedios.

Subredes Regionales en GCP:
Dentro de la VPC Global, las subredes son regionales (asociadas a una region geografica,
pero accesibles desde cualquier zona de esa region).
En GCP solo se reservan DOS (2) direcciones IP por subred:
- La primera direccion IP (ej. `10.0.0.0`): Red.
- La segunda direccion IP (ej. `10.0.0.1`): Gateway predeterminado.
- (A diferencia de AWS/Azure, la direccion broadcast y las demas son utilizables).



## 2. CLOUD ROUTER Y ENRUTAMIENTO DINAMICO BGP EN GCP

Google Cloud Router es un servicio de plano de control BGP administrado y escalable.
- No transporta paquetes de datos en su CPU; unicamente ejecuta las sesiones de BGP (TCP 179).
- Modos de Enrutamiento Dinamico en la VPC:
  * Regional Dynamic Routing: El Cloud Router solo anuncia y aprende rutas de la region local.
  * Global Dynamic Routing: El Cloud Router anuncia todas las subredes de todo el planeta
    a traves de una unica sesion BGP con tu router on-premises.


#### 💻 CONFIGURACION GCLOUD CLI:

```bash
gcloud compute routers create CR_DATACENTER \
    --network=VPC_GLOBAL_CORP \
    --region=us-central1 \
    --asn=65001
```


## 3. CLOUD NAT: SALIDA SEGURA A INTERNET SIN IPs PUBLICAS EN INSTANCIAS

Cloud NAT permite que las maquinas Compute Engine y clusters de Kubernetes (GKE)
accedan a Internet de forma segura y altamente disponible sin requerir una IP publica
externa ni desplegar servidores proxy o appliances de NAT individuales.
- Es un servicio completamente definido por software (cero cuellos de botella de hardware).


#### 💻 CONFIGURACION GCLOUD CLI:

```bash
gcloud compute routers nats create NAT_SALIDA_INTERNET \
    --router=CR_DATACENTER \
    --region=us-central1 \
    --auto-allocate-nat-external-ips \
    --nat-all-subnet-ip-ranges
```


## 4. ARQUITECTURA SHARED VPC (VPC COMPARTIDA ENTORNO MULTI-PROYECTO)

En grandes corporativos con cientos de proyectos de desarrollo, crear una VPC por
cada proyecto fragmenta el direccionamiento y la seguridad.
Shared VPC centraliza la gestion de red en un "Proyecto Host" administrado por el
equipo de telecomunicaciones, y delega subredes a "Proyectos de Servicio" (donde
los desarrolladores solo despliegan VMs sin poder tocar el enrutamiento ni los firewalls).


#### 🌐 DIAGRAMA:

```text
  +-----------------------------------------------------------------------------+
  |              PROYECTO HOST (ADMINISTRADO POR TELECOMUNICACIONES)            |
  |                   VPC Global: Red Corporativa (10.0.0.0/16)                 |
  |        [Cloud Router BGP] <====== Cloud Interconnect ======> [ON-PREM]      |
  +-----------------------+-----------------------------+-----------------------+
                          |                             |
                          v                             v
           +-----------------------------+   +-----------------------------+
           |    PROYECTO DE SERVICIO 1   |   |    PROYECTO DE SERVICIO 2   |
           |      (EQUIPO DE DATOS)      |   |       (EQUIPO WEB)          |
           | Subred: 10.0.1.0/24         |   | Subred: 10.0.2.0/24         |
           +-----------------------------+   +-----------------------------+
```


## 5. REGLAS DE FIREWALL EN GCP: ETIQUETAS DE RED (NETWORK TAGS)

En Google Cloud, las reglas de firewall no se aplican a subredes ni a interfaces fijas;
se aplican a nivel de VPC y se filtran mediante "Network Tags" asignados a las instancias.

EJEMPLO EN GCLOUD CLI:
! Permitir trafico HTTPS entrante solo a las VMs que tengan la etiqueta 'servidor-web':
gcloud compute firewall-rules create permitir-https-web \
    --network=VPC_GLOBAL_CORP \
    --allow=tcp:443 \
    --target-tags=servidor-web \

## --source-ranges=0.0.0.0/0
