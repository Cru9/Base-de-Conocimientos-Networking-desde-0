# 00. INDICE GENERAL, CICLO DE VIDA DE REDES (PPDIOO/ITIL) Y PIRAMIDE DOCUMENTAL

> **METODOLOGIA DE INGENIERIA, PLANTILLAS Y DOCUMENTACION PROFESIONAL**


---



## 1. LA DIFERENCIA ENTRE UN "CONFIGURADOR" Y UN INGENIERO DE REDES SENIOR

Cualquier persona puede memorizar comandos de consola o seguir un tutorial de internet.
Sin embargo, en el mundo corporativo de mision critica (banca, telecomunicaciones,
retail masivo, salud y gobierno), la excelencia de un Ingeniero Principal de Redes
se mide por su rigor metodologico:
- Capacidad de traducir necesidades de negocio en arquitecturas de red resilientes.
- Documentacion impecable que permita a cualquier miembro del equipo operar el sistema.
- Gestion estricta del riesgo: CERO caidas de servicio no planificadas.
- Cada cambio en produccion debe contar con un procedimiento cronometrado (MOP)
  y un plan de rollback probado antes de tocar el primer equipo.



## 2. EL CICLO DE VIDA DE LA RED: METODOLOGIA PPDIOO Y MARCO ITIL

El estandar internacional de diseno de infraestructura de telecomunicaciones sigue
el modelo PPDIOO de Cisco y las mejores practicas de ITIL v4:

1. Prepare (Preparar):
   - Definicion de objetivos comerciales, requerimientos de ancho de banda y presupuesto.
2. Plan (Planificar):
   - Auditoria de la red actual, analisis de brechas y evaluacion de riesgos.
3. Design (Disenar - Fase Documental HLD y LLD):
   - Elaboracion de la arquitectura de alto nivel (HLD) y especificaciones detalladas (LLD).
4. Implement (Implementar - Fase MOP):
   - Despliegue en ventana de mantenimiento siguiendo el Method of Procedure (MOP).
5. Operate (Operar):
   - Monitoreo NOC 24/7, soporte a incidencias y mantenimiento preventivo.
6. Optimize (Optimizar):
   - Ajustes de desempeno, analisis de trafico y planificacion de capacidad (Capacity Planning).



## 3. LA PIRAMIDE DOCUMENTAL DE INGENIERIA DE REDES

Para que un proyecto sea considerado profesional, debe contar con 4 documentos clave:

```text
                    +------------------------------------+
                    |       HLD (High-Level Design)      | <--- Para Directores y Arquitectos
                    +------------------------------------+
                                      |
                    +------------------------------------+
                    |        LLD (Low-Level Design)      | <--- Para Ingenieros y Soporte
                    +------------------------------------+
                                      |
                    +------------------------------------+
                    |     MOP (Method of Procedure)      | <--- Para la Ventana de Cambio
                    +------------------------------------+
                                      |
                    +------------------------------------+
                    |    TESTING & ROLLBACK RUNBOOK      | <--- Para Gestion del Riesgo
                    +------------------------------------+
```


## 4. INDICE DE ARCHIVOS DE LA CARPETA METODOLOGIA_INGENIERIA_Y_PLANTILLAS

[00_INDICE_Y_ESTANDARES_DE_DOCUMENTACION_IT.md](./00_INDICE_Y_ESTANDARES_DE_DOCUMENTACION_IT.md)
    - Indice general, metodologia PPDIOO, gestion de cambios ITIL y piramide documental.

[01_PLANTILLA_HLD_HIGH_LEVEL_DESIGN_ARQUITECTURA.md](./01_PLANTILLA_HLD_HIGH_LEVEL_DESIGN_ARQUITECTURA.md)
    - Plantilla lista para rellenar de Diseno de Alto Nivel (HLD): Resumen ejecutivo,
      drivers de negocio, matriz de seleccion tecnologica, diagrama logico y seguridad.

[02_PLANTILLA_LLD_LOW_LEVEL_DESIGN_INGENIERIA_DETALLE.md](./02_PLANTILLA_LLD_LOW_LEVEL_DESIGN_INGENIERIA_DETALLE.md)
    - Plantilla lista para rellenar de Diseno de Bajo Nivel (LLD): Elevacion de racks,
      mapeo puerto a puerto (Port Mapping), esquema de direccionamiento IP, matriz de VLANs/VRFs,
      Bill of Materials (BOM) y snippets de configuracion.

[03_PLANTILLA_MOP_METHOD_OF_PROCEDURE_VENTANAS_CAMBIO.md](./03_PLANTILLA_MOP_METHOD_OF_PROCEDURE_VENTANAS_CAMBIO.md)
    - Plantilla lista para rellenar de Metodo de Procedimiento (MOP): Cronograma minuto
      a minuto de la ventana (T-minus, T0, post-check), matriz de roles y autorizaciones CAB.

[04_PLAN_DE_PRUEBAS_TESTING_Y_ROLLBACK_DE_EMERGENCIA.md](./04_PLAN_DE_PRUEBAS_TESTING_Y_ROLLBACK_DE_EMERGENCIA.md)
    - Protocolo de pruebas de aceptacion (Sanity checks, failover drills, verificacion BGP)

y Procedimiento de Rollback Inmediato con scripts de reversa ante contingencias.
