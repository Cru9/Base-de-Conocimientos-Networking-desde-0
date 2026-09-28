# GUIA CISCO IOS - PARTE 2: CONFIGURACION INICIAL Y ACCESO SEGURO (SSH / CONSOLA)


---



## 1. CAMBIAR EL NOMBRE DEL SWITCH (HOSTNAME)

```cisco
Switch# configure terminal
Switch(config)# hostname SW-ACCESO-PISO1
SW-ACCESO-PISO1(config)#
```


## 2. AJUSTE DE HORA, ZONA HORARIA Y SERVIDOR NTP

Para que los registros de auditoria (logs) tengan fecha y hora exacta:

-- Ajustar Zona Horaria (Ejemplo: UTC-6 Mexico/Centroamerica):
```cisco
SW-ACCESO-PISO1(config)# clock timezone CDMX -6 0

-- Sincronizacion automatica con servidor NTP de la empresa:
SW-ACCESO-PISO1(config)# ntp server 192.168.1.100

-- Ajuste manual de hora (solo desde modo privilegiado #):
SW-ACCESO-PISO1# clock set 11:30:00 25 September 2026
```


## 3. MENSAJE DE ADVERTENCIA LEGAL (BANNER MOTD)

El delimitador (en este ejemplo el caracter #) indica donde empieza y termina el texto:


## SW-ACCESO-PISO1(config)# banner motd #

 ACCESO EXCLUSIVO PARA PERSONAL AUTORIZADO DE REDES.

## TODO ACCESO NO AUTORIZADO SERA REGISTRADO Y SANCIONADO.

#



## 4. PROTECCION DEL MODO PRIVILEGIADO (ENABLE SECRET)

Evita que cualquier persona entre al modo privilegiado (Switch#) sin password.
¡REGLA DE ORO!: Usa siempre "enable secret" (encriptado con hash fuerte) y NUNCA
"enable password" (que es texto plano o hash debil).

```cisco
SW-ACCESO-PISO1(config)# enable secret MiClavePrivilegiada2026!

-- Encriptar todas las contrasenas visibles en el archivo de texto:
SW-ACCESO-PISO1(config)# service password-encryption
```


## 5. SEGURIDAD EN EL PUERTO DE CONSOLA FISICA (LINE CONSOLE 0)

```cisco
SW-ACCESO-PISO1(config)# line console 0
SW-ACCESO-PISO1(config-line)# password ClaveConsolaFisica!
SW-ACCESO-PISO1(config-line)# login
SW-ACCESO-PISO1(config-line)# exec-timeout 10 0        <- Cierra sesion tras 10 min de inactividad
SW-ACCESO-PISO1(config-line)# logging synchronous       <- ¡TRUCO DE ORO! Evita que los mensajes 
                                                          del sistema te interrumpan mientras escribes.
SW-ACCESO-PISO1(config-line)# exit
```


## 6. CONFIGURACION COMPLETA DE ACCESO REMOTO SEGURO POR SSH

Telnet envia contrasenas en texto claro. En cualquier red corporativa se debe usar SSHv2.

Paso 1: Asignar un nombre de dominio (Requisito obligatorio para generar llaves RSA):
```cisco
SW-ACCESO-PISO1(config)# ip domain-name empresa.com

Paso 2: Generar las llaves criptograficas RSA (Minimo 2048 bits):
SW-ACCESO-PISO1(config)# crypto key generate rsa modulus 2048
  -> Informara: "The name for the keys will be: SW-ACCESO-PISO1.empresa.com"
  -> "Key generation process complete."

Paso 3: Forzar el uso de SSH Version 2 (Mas segura que la version 1):
SW-ACCESO-PISO1(config)# ip ssh version 2

Paso 4: Crear el usuario administrador local:
SW-ACCESO-PISO1(config)# username admin privilege 15 secret AdminClaveSSH2026!
  -> "privilege 15" otorga control total inmediato sin necesidad de volver a pedir enable.

Paso 5: Configurar las lineas virtuales de acceso remoto (VTY 0 a 15):
SW-ACCESO-PISO1(config)# line vty 0 15
SW-ACCESO-PISO1(config-line)# transport input ssh      <- Bloquea Telnet, solo acepta SSH
SW-ACCESO-PISO1(config-line)# login local              <- Valida con los usuarios creados en el switch
SW-ACCESO-PISO1(config-line)# exec-timeout 15 0        <- Desconexion tras 15 min inactivo
SW-ACCESO-PISO1(config-line)# logging synchronous
SW-ACCESO-PISO1(config-line)# exit

Paso 6: Deshabilitar el servidor HTTP plano no seguro:
SW-ACCESO-PISO1(config)# no ip http server
```


## 7. VERIFICACION

- Comprobar que SSH v2 esta corriendo correctamente:
```cisco
    SW-ACCESO-PISO1# show ip ssh

- Ver usuarios conectados remotamente en este momento:
    SW-ACCESO-PISO1# show users
```
