# 04. PLAN DE PRUEBAS DE ACEPTACION (TESTING) Y ROLLBACK DE EMERGENCIA

> **METODOLOGIA DE INGENIERIA, PLANTILLAS Y DOCUMENTACION PROFESIONAL**


---


-------------------------------------------------------------------------------
GUIA DE VALIDACION, MATRIZ DE PRUEBAS Y PROCEDIMIENTO DE REVERSION (BACKOUT)
ASOCIADO A RFC:      [CHG-2026-08421]
OBJETIVO:            Garantizar que ningun cambio degrade el desempeno de la red

y definir el protocolo matematico de retorno al estado seguro.



## 1. MATRIZ FORMAL DE PRUEBAS DE ACEPTACION (TESTING MATRIX)

La validacion posterior a la ventana de cambio debe ejecutarse sistematicamente:


| Prueba ID | Capa OSI | Descripcion de la Prueba | Criterio de Exito | Resultado |
| :--- | :--- | :--- | :--- | :--- |
| TST-01 | Capa 1/2 | Verificar errores fisicos en puerto | Contadores CRC = 0 | [ PASO / FALLO ] |
| Comando: show interfaces TenGig1/0/1 | Errores Input/Output = 0 |  |  |  |
| TST-02 | Capa 2 | Verificar estado del arbol Spanning | Switches Root sin flaps; | [ PASO / FALLO ] |
| Comando: show spanning-tree detail | 0 TCNs tras 10 minutos |  |  |  |
| TST-03 | Capa 3 | Verificar Adyacencia OSPF Interna | Estado: FULL en todos | [ PASO / FALLO ] |
| Comando: show ip ospf neighbor | los vecinos del Backbone |  |  |  |
| TST-04 | Capa 3 | Verificar Sesion BGP con Proveedor | Estado: ESTABLISHED | [ PASO / FALLO ] |
| Comando: show ip bgp summary | Rutas recibidas > 0 |  |  |  |
| TST-05 | Capa 3 | Comprobar Tamano de MTU sin fragmentar 100% exito con 1500 bytes | [ PASO / FALLO ] |  |
| Comando: ping 10.10.10.1 size 1500 df | (o 1400 bytes en tuneles) |  |  |  |
| TST-06 | Capa 4 | Medicion de Throughput y Jitter iPerf3 Throughput > 950 Mbps | [ PASO / FALLO ] |  |
| iperf3 -c 10.10.10.50 -t 30 -P 4 | Jitter < 2 ms, 0% perdida |  |  |  |
| TST-07 | Capa 7 | Resolucion de Nombres DNS Corporativos dig erp.corp.local | [ PASO / FALLO ] |  |
| dig @10.50.0.10 portal.corp.local | Responde IP en < 5 ms |  |  |  |
| TST-08 | Capa 7 | Autenticacion de Usuarios en Dominio | Login exitoso en Windows | [ PASO / FALLO ] |
| Inicio de sesion en Active Directory | Sin demoras de Kerberos |  |  |  |




## 2. PRUEBA DE CONMUTACION FORZADA (FAILOVER DRILL)

Antes de dar por concluida una ventana de mantenimiento que involucre alta disponibilidad,
es OBLIGATORIO simular la falla del enlace principal:

Procedimiento de Simulacion:
1. Dejar corriendo un ping continuo en una estacion de monitoreo:
```text
   ping -t 10.10.10.50
2. Apagar administrativamente la interfaz del enlace principal:
   RT-WAN-01(config)# interface GigabitEthernet0/0/1
   RT-WAN-01(config-if)# shutdown
3. Cronometrar la perdida de paquetes:
   - Con BFD subsegundo + BGP/HSRP, la conmutacion al enlace secundario NO debe
     perder mas de 1 o 2 paquetes ping (< 1 segundo).
4. Restaurar el enlace principal:
   RT-WAN-01(config-if)# no shutdown
5. Verificar el retorno estable (Failback) sin generar tormentas de paquetes (Route Flapping).
```


## 3. PROTOCOLO DE ROLLBACK DE EMERGENCIA (BACKOUT PLAN)

Si la ventana de cambio falla y se declara "NO-GO", se debe revertir el cambio
de inmediato siguiendo este procedimiento:

A. EL METODO MODERNO EN CISCO IOS-XE: REEMPLAZO ATOMICO DE CONFIGURACION
   En lugar de intentar borrar comandos manualmente con 'no ...' (lo que casi siempre
   deja configuraciones residuales huerfanas o bloquea el acceso), Cisco IOS-XE
   permite sustituir la configuracion activa por el respaldo previo en un solo paso:

   ! Comando magico de recuperacion atomica (sin necesidad de reiniciar el router):
   Router-01# configure replace flash:backup-pre-change.cfg force

   Este comando analiza las diferencias entre la memoria actual y el archivo previo,
   remueve unicamente lo que se anadio y restaura lo que se habia borrado, entregando
   el equipo exactamente como estaba antes de iniciar la ventana.

B. EN DISPOSITIVOS VYOS / JUNIPER JUNOS:
   vyos@vyos# rollback 1
   vyos@vyos# commit

C. EN HUAWEI VRP:
```text
   <Huawei> rollback configuration to file backup-pre-change.cfg
```


## 4. SCRIPT MANUAL DE ROLLBACK LINEA POR LINEA (EN CASO DE CONTINGENCIA)

Si por alguna razon el reemplazo atomico fallara, aplicar este bloque de comandos
para desmantelar el cambio realizado:

! 1. Desactivar la sesion BGP con el nuevo ISP
```text
configure terminal
router bgp 65001
 no neighbor 187.140.20.1
exit

! 2. Apagar la interfaz del nuevo proveedor para que no interfiera en la red
interface GigabitEthernet0/0/2
 shutdown
 description ENLACE_CANCELADO_POR_ROLLBACK
 no ip address 187.140.20.2 255.255.255.252
exit

! 3. Forzar el retorno de la ruta por defecto hacia el ISP antiguo
ip route 0.0.0.0 0.0.0.0 200.50.10.1
end
write memory
```


## 5. REPORTE DE CAUSA RAIZ (RCA - ROOT CAUSE ANALYSIS)

Tras un evento de Rollback, el equipo tecnico debe emitir un informe RCA formal en
un plazo maximo de 48 horas detallando:
1. ¿Que fallo exactamente? (Analisis de logs, capturas de Wireshark).
2. ¿Por que no se detecto en el laboratorio de pruebas antes de ir a produccion?

## 3. Acciones correctivas necesarias antes de volver a solicitar la ventana en el CAB.
