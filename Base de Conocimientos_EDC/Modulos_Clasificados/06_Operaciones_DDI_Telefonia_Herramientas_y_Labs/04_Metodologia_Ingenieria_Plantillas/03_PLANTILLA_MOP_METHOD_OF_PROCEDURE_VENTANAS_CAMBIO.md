# 03. PLANTILLA PROFESIONAL: METODO DE PROCEDIMIENTO (MOP - METHOD OF PROCEDURE)

> **METODOLOGIA DE INGENIERIA, PLANTILLAS Y DOCUMENTACION PROFESIONAL**


---


-------------------------------------------------------------------------------
DOCUMENTO DE EJECUCION PARA VENTANA DE MANTENIMIENTO (CHANGE WINDOW)
NUMERO DE TICKET / RFC: [CHG-2026-08421]
TITULO DEL CAMBIO:      [Migracion de Enlace Troncal WAN y Activacion de BGP Dual]
FECHA DE EJECUCION:     [Sabado 2026-10-10 23:00 hrs a Domingo 2026-10-11 04:00 hrs]
IMPACTO ESTIMADO:       [Interrupcion controlada de 2 minutos durante conmutacion]

## NIVEL DE RIESGO:        [ALTO - Requiere aprobacion formal del Comite CAB]



## 1. MATRIZ DE PARTICIPANTES Y ROLES (WAR ROOM / BRIDGE CALL)


| Rol en la Ventana | Nombre del Ingeniero | Cargo / Especialidad | Telefono Movil |
| :--- | :--- | :--- | :--- |
| Change Owner | Ing. Roberto Mendez | Gerente de Redes y TI | +52 55 1234 5678 |
| Ingeniero Ejecutor | Ing. Carlos Ortiz | Sr. Network Engineer | +52 55 8765 4321 |
| Ingeniero Validador Ing. Laura Ramos | QA & Security Auditor | +52 55 4567 8901 |  |
| Soporte de Enlace | Ing. Soporte Carrier | NOC de Proveedor ISP | 01-800-999-0000 |

Puente de Voz / URL: https://teams.microsoft.com/l/meetup-join/bridge-chg-08421



## 2. PRE-REQUISITOS (CHECKLIST T-MINUS 2 HORAS ANTES DE LA VENTANA)

[ ] 1. Validar que la aprobacion del comite CAB este en estado "APPROVED" en ServiceNow/Jira.
[ ] 2. Confirmar que el personal de guardia de aplicaciones y base de datos este conectado.
```text
[ ] 3. Comprobar conectividad Fuera de Banda (OOB - Out-of-Band): Acceso por consola 4G/LTE
       disponible por si se pierde la conexion SSH en la red corporativa.
[ ] 4. RESPALDO OBLIGATORIO DE CONFIGURACIONES:
       Ejecutar en todos los equipos involucrados y guardar en servidor seguro:
       Router-01# copy running-config tftp://10.50.0.80/backup-pre-change-RT01.cfg
[ ] 5. CAPTURA DE LINEA BASE (PRE-CHECKS):
       Guardar la salida de los siguientes comandos en archivos de texto para comparacion posterior:
       - show ip route summary
       - show ip interface brief
       - show ip bgp summary
       - show ip ospf neighbor
       - show standby brief / show vrrp brief
```


## 3. CRONOGRAMA DE EJECUCION PASO A PASO (RUNBOOK MINUTO A MINUTO)


| Hora Estimada | Paso | Responsable | Accion Tecnica y Comandos Exactos |
| :--- | :--- | :--- | :--- |
| 23:00 - 23:15 | 1.0 | Change Owner | Apertura de la llamada de crisis (Bridge). Pasar lista. |

                                   Validar que no haya incidentes P1 activos en produccion.

23:15 - 23:30  2.0   Validador     Tomar Pre-Checks de salud de la red y confirmar estado verde.

23:30 - 00:15  3.0   Ejecutor      PASO 1: Habilitar nueva interfaz física hacia el nuevo ISP:
                                   RT-WAN-01# configure terminal
                                   RT-WAN-01(config)# interface GigabitEthernet0/0/2
                                   RT-WAN-01(config-if)# description ENLACE_FIBRA_NUEVO_ISP
                                   RT-WAN-01(config-if)# ip address 187.140.20.2 255.255.255.252
                                   RT-WAN-01(config-if)# no shutdown
                                   RT-WAN-01(config-if)# end

00:15 - 01:00  4.0   Ejecutor      PASO 2: Levantar sesion BGP con el nuevo proveedor:
                                   RT-WAN-01# configure terminal
                                   RT-WAN-01(config)# router bgp 65001
                                   RT-WAN-01(config-router)# neighbor 187.140.20.1 remote-as 64600
                                   RT-WAN-01(config-router)# neighbor 187.140.20.1 description ISP-2-FIBRA
                                   RT-WAN-01(config-router)# address-family ipv4 unicast
                                   RT-WAN-01(config-router-af)# neighbor 187.140.20.1 activate
                                   RT-WAN-01(config-router-af)# network 10.10.0.0 mask 255.255.0.0
                                   RT-WAN-01(config-router-af)# end

01:00 - 01:45  5.0   Validador     PASO 3: Validar convergencia de rutas:
                                   RT-WAN-01# show ip bgp summary
                                   ! Verificar que el estado pase a 'Established' y reciba rutas.
                                   RT-WAN-01# ping 8.8.8.8 source GigabitEthernet0/0/2

01:45 - 02:15  6.0   Ejecutor      PASO 4: Conmutar trafico preferente hacia el nuevo enlace
                                   ajustando Local-Preference en BGP a 200.



## 4. PUNTO DE NO RETORNO (POINT OF NO RETURN - PoNR)

HORA LIMITE DE NO RETORNO: 02:30 AM.
CRITERIO DE DECISION (GO / NO-GO):
- Si a las 02:30 AM el enrutamiento no es 100% estable, o si la perdida de paquetes
  hacia el Datacenter supera el 1%, o si las pruebas de aplicaciones marcan error:
  SE DECLARA INMEDIATAMENTE "NO-GO" Y SE INICIA EL ROLLBACK.
- Queda terminantemente prohibido improvisar comandos o intentar parches en caliente
  despues de las 02:30 AM, garantizando tiempo suficiente para restaurar la red
  original antes de las 04:00 AM.



## 5. POST-CHECKS Y VALIDACION DE SERVICIO

Hora: 02:30 - 03:15
```text
[ ] 1. Comparar tabla de ruteo contra el archivo de Pre-Checks (show ip route summary).
[ ] 2. Pruebas continuas de latencia (ping con 1000 paquetes sin perdida).
[ ] 3. Validar que las sesiones de usuarios no sufran ruteo asimetrico.
[ ] 4. Confirmacion de las areas de Aplicaciones (SAP, Portal Web, Base de Datos OK).
```


## 6. CIERRE DE LA VENTANA DE CAMBIO

Hora: 03:30
- Guardar la configuracion en memoria persistente: 'write memory' / 'copy run start'.
- Notificar por correo electronico al Comite CAB y Service Desk con el estatus "COMPLETADO EXITOSO".

## - Cerrar el puente de comunicacion.
