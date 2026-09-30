# GUIA HP PROCURVE / ARUBA - PARTE 1: MODOS DE ACCESO, NAVEGACION Y PRIMEROS COMANDOS


---



## 1. ¿QUE ES EL SISTEMA OPERATIVO PROCURVE / ARUBAOS-S?

Los switches HP ProCurve y ArubaOS-S (series 2530, 2920, 2930F, 5400R, etc.)
ejecutan un sistema operativo conocido como Provision / ArubaOS-S.
Es muy valorado por los administradores de red por su sencillez: la configuracion
esta centralizada y organizada directamente por VLANs.



## 2. JERARQUIA DE MODOS EN HP


### A) Modo Operador (Operator Mode):

   - Prompt: HP-Switch>
   - Solo permite comandos basicos de visualizacion y pruebas de conectividad (ping).
   - Para avanzar, escribe: enable


### B) Modo Administrador (Manager Mode):

   - Prompt: HP-Switch#
   - Permite ver la configuracion completa, guardar cambios y diagnosticos avanzados.
   - Para entrar a configurar, escribe: configure terminal  (o simplemente: config)


### C) Modo de Configuracion Global:

   - Prompt: HP-Switch(config)#
   - Desde aqui se cambian parametros generales (nombre, VLANs, seguridad, STP, etc.).


### D) Modo de Contexto de VLAN:

   - Prompt: HP-Switch(vlan-10)#
   - Desde aqui se gestionan los puertos ("tagged" / "untagged") y la direccion IP de la red.


### E) MODO EXCLUSIVO DE HP: INTERFAZ DE MENU TEXTUAL (MENU)

   - Si no quieres usar la linea de comandos, escribe en el prompt:
       HP-Switch# menu
   - Se abrira un menu interactivo en pantalla con el que puedes configurar IPs,
     puertos y ver estados usando las flechas del teclado y Enter.



## 3. NOMENCLATURA DE PUERTOS EN SWITCHES HP

En HP, los puertos no se llaman "FastEthernet" ni "GigabitEthernet" en los comandos.
Se identifican de forma muy sencilla:
- En switches fijos de 24 o 48 puertos: Simplemente el numero: 1, 2, 3 ... 24, 25, 48.
- En switches modulares (chasis como 5400zl): Letra de ranura + Puerto: A1, A2, B1, B2.
- En apilamientos VSF: Miembro/Puerto: 1/1, 1/2 ... 2/1, 2/2.



## 4. ATAJOS DE TECLADO Y NAVEGACION

- ?: Ayuda contextual inmediata.
- TAB: Autocompleta comandos.
- exit: Retrocede un nivel hacia atras.
- end (o Ctrl + Z): Vuelve directamente al modo Manager (HP-Switch#).
- no [comando]: Deshace o elimina cualquier configuracion (equivalente a "undo" o "no" de Cisco).



## 5. COMANDOS ESENCIALES DE VISUALIZACION (SHOW)

HP-Switch# show system-information
  -> Muestra el modelo exacto (ej. HP J9773A 2530-24G), version de firmware, numero de serie y uptime.

HP-Switch# show running-config  (o show run)
  -> Muestra la configuracion activa que esta ejecutandose en memoria RAM.

HP-Switch# show config
  -> Muestra la configuracion guardada en la memoria permanente flash.

HP-Switch# show interfaces brief
  -> Tabla visual de todos los puertos: estado (Up/Down), velocidad (100M/1000M) y duplex.

HP-Switch# show mac-address
  -> Tabla de direcciones MAC aprendidas en cada puerto del switch.



## 6. GUARDAR Y REINICIAR (WRITE MEMORY & RELOAD)

Todo cambio realizado queda solo en la memoria volatil. Para que no se borre al apagarse:

- Guardar cambios en la memoria permanente Flash:
    HP-Switch# write memory   (o la abreviatura: wr mem)

- Reiniciar el switch:
    HP-Switch# reload
    -> Te preguntara: "Do you want to save current configuration [y/n]?"

- Restaurar configuracion de fabrica (Reset total):
    HP-Switch# erase startup-config
    -> Te preguntara si deseas reiniciar de fabrica. Presiona 'y'.