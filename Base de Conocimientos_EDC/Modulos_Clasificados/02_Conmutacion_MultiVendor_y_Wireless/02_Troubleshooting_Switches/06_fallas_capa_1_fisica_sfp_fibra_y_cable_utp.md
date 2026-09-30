# 06. FALLAS DE CAPA 1 FISICA: SFP, FIBRA OPTICA, DUPLEX Y CABLE DE COBRE

> **RESOLUCION DE FALLAS (TROUBLESHOOTING DE SWITCHES)**


---



## 1. SINTOMAS DE FALLAS EN LA CAPA FISICA

La Capa 1 es responsable de mas del 60% de los problemas aparentemente "inexplicables":
- Lentitud extrema en transferencias de archivos grandes mientras que el Ping funciona.
- Llamadas de VoIP entrecortadas, roboticas o con perdida constante de paquetes.
- El LED de enlace de un puerto de fibra optica no enciende jamas al conectar el cable.
- El switch bloquea el puerto SFP con el mensaje:
  "%GBIC_FTM-4-UNSUPPORTED_SFP: SFP inserted in GigabitEthernet0/24 is not supported"
- Los contadores de errores en la interfaz no paran de aumentar:
  CRC errors, Input errors, Late collisions, Runts, Giants.



## 2. DISCREPANCIA DE DUPLEX (DUPLEX MISMATCH)

Ocurre cuando un extremo esta forzado en Full-Duplex y el otro extremo esta en Auto.
Por regla IEEE, si un extremo esta forzado, el que esta en Auto NO puede detectar
el duplex y cae obligatoriamente a Half-Duplex.

Consecuencia:
- El equipo en Half-Duplex cree que hay una colision cada vez que ambos transmiten
  al mismo tiempo, aborta la transmision y genera 'Late Collisions'.
- La velocidad efectiva se reduce a menos del 1% del ancho de banda contratado.

Como diagnosticar:
```cisco
  SW# show interfaces GigabitEthernet 0/5
  Verifique la linea: `Half-duplex, 100Mb/s` y el contador `late collision > 0`.

Solucion:
  Configure AMBOS extremos en autonegociacion (lo recomendado en Gigabit):
  SW(config-if)# speed auto
  SW(config-if)# duplex auto
  O fuerce ambos extremos exactamente iguales: `speed 100` y `duplex full`.
```


## 3. FALLAS EN ENLACES DE FIBRA OPTICA Y MODULOS SFP / SFP+

Falla A: Polaridad invertida (Tx a Tx / Rx a Rx)
  - La fibra optica requiere que el transmisor (Tx) de un switch conecte con el
    receptor (Rx) del otro switch (cruzado).
  - Si el enlace no enciende, presione el seguro del clip LC duplex, intercambie
    los dos hilos de fibra (cruce Tx y Rx) y vuelva a insertar.

Falla B: Mezcla de Fibra Monomodo (SMF) y Multimodo (MMF)
  - Monomodo (SMF): Cubierta amarilla, nucleo de 9 µm, laser de 1310/1550 nm (largas distancias).
  - Multimodo (MMF): Cubierta naranja o aqua (OM3/OM4), nucleo de 50/62.5 µm, 850 nm (cortas distancias).
  - ¡NUNCA use un transceptor SX (multimodo) con un cable o transceptor LX (monomodo)!



## 4. DIAGNOSTICO DIGITAL DE POTENCIA OPTICA (DDM / DOM)

Permite conocer exactamente la potencia con la que emite el laser (Tx) y la potencia
con la que recibe la senal de luz (Rx) en dBm:

CISCO:
```cisco
  SW# show interfaces GigabitEthernet 0/24 transceiver detail
```

HUAWEI:
```cisco
  SW> display transceiver interface GigabitEthernet 0/0/24 verbose
```

HP PROCURVE:
```cisco
  SW# show interfaces transceiver detail 24

ARUBA (AOS-CX):
  SW# show interface 1/1/24 transceiver detail
```

TP-LINK JETSTREAM:
```cisco
  SW# show interface transceiver detail gigabitEthernet 1/0/25

INTERPRETACION DE LOS VALORES EN dBm (Rx Power):
- Entre -2 dBm y -15 dBm: EXCELENTE. Potencia de senal optica optima.
- Entre -16 dBm y -22 dBm: REGULAR / ACEPTABLE. El enlace funciona pero hay perdida.
- Menor a -25 dBm (ej. -30 dBm, -40 dBm): FALLA CRITICA. Atenuacion severa;
  causada por conectores LC sucios, curvas de fibra muy cerradas o empalme danado.
```


## 5. DESBLOQUEO DE TRANSCEPTORES SFP DE TERCEROS (NO ORIGINALES)

Varios fabricantes (como Cisco y HP) bloquean por firmware modulos SFP genericos
o compatibles (FS.com, Finisar, etc.) poniendolos en 'err-disable'.

Desbloqueo en CISCO:
```cisco
  SW(config)# service unsupported-transceiver
  SW(config)# no errdisable detect cause gbic-invalid

Desbloqueo en HP PROCURVE:
  SW(config)# allow-unsupported-transceiver
  (Confirmar con 'y' la advertencia de garantia).
```


## 6. PRUEBA DE CABLES DE COBRE INTEGRADA EN EL SWITCH (TDR / VCT)

Permite medir con precision de metros donde esta roto o dañado un cable UTP:

En Cisco:
```cisco
  SW# test cable-diagnostics tdr interface GigabitEthernet 0/5
  (Esperar 5 segundos)
  SW# show cable-diagnostics tdr interface GigabitEthernet 0/5

En Huawei:
  SW> virtual-cable-test GigabitEthernet 0/0/5

En HP ProCurve:
  SW# test cable-diagnostics 5
  SW# show cable-diagnostics 5

En TP-Link JetStream:
  SW# test cable-diagnostics gigabitEthernet 1/0/5
  SW# show cable-diagnostics gigabitEthernet 1/0/5

Significado de los resultados:
- Normal / Pair OK: El cable de 4 pares esta en perfecto estado.
- Open: Par cortado o roseta desconectada (indica los metros exactos hasta el corte).
```


## - Short: Dos hilos tocandose (cortocircuito) por cable pisado o ponchado aplastado.
