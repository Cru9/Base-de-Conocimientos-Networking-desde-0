# GUIA 3COM COMWARE - PARTE 1: MODOS DE ACCESO, NAVEGACION Y PRIMEROS COMANDOS


---



## 1. ¿QUE ES EL SISTEMA OPERATIVO COMWARE EN 3COM?

Los switches administrables de 3Com (como las series SuperStack 4200G, 4500, 4800G,
5500G y 7700) utilizan el sistema operativo Comware. Su interfaz de linea de comandos
es robusta, orientada a vistas jerarquicas.



## 2. MODOS DE TRABAJO (JERARQUIA DE NAVEGACION)


### A) Modo Usuario (User View):

   - Prompt: <3Com>
   - Solo permite tareas de consulta basica, pruebas de ping y visualizacion elemental.


### B) Modo Sistema (System View):

   - Prompt: [3Com]
   - Como entrar:
```text
       <3Com> system-view
   - Permite configurar parametros globales del switch (nombre, VLANs, enrutamiento, etc.).

C) Modos de Interfaz / Protocolo (Interface View):
   - Prompt: [3Com-GigabitEthernet1/0/1] o [3Com-Vlan-interface10]
   - Como entrar:
       [3Com] interface GigabitEthernet 1/0/1
   - Nomenclatura de puertos en 3Com:
     Unidad / Ranura / Puerto (ej. 1/0/1 = Switch 1, tarjeta 0, puerto 1).
```


## 3. ATAJOS DE TECLADO Y REGLAS DE NAVEGACION

- ?: Muestra ayuda contextual y lista de comandos disponibles.
- TAB: Autocompleta comandos incompletos.
- quit: Retrocede un nivel hacia atras en la jerarquia.
- return (o Ctrl + Z): Regresa directamente al modo usuario <3Com>.
- undo [comando]: Deshace, borra o desactiva cualquier configuracion.
  Ejemplos: "undo shutdown" (enciende el puerto), "undo vlan 10" (elimina la VLAN).



## 4. COMANDOS ESENCIALES DE VISUALIZACION (DISPLAY)

En 3Com se utiliza el comando "display" (o su abreviatura "dis"):

```text
<3Com> display version
  -> Muestra el modelo exacto (ej. 3Com Switch 4500G 24-Port), version de Comware y uptime.

<3Com> display current-configuration  (o dis cur)
  -> Muestra la configuracion activa que esta ejecutandose en memoria RAM.

<3Com> display saved-configuration
  -> Muestra la configuracion que se cargara al reiniciar (guardada en flash).

<3Com> display interface brief
  -> Tabla resumen de puertos fisicos: estado (UP/DOWN), velocidad y duplex.

<3Com> display ip interface brief
  -> Muestra las interfaces logicas con sus direcciones IP asignadas.

<3Com> display mac-address
  -> Tabla de direcciones MAC aprendidas por el switch.
```


## 5. GUARDAR Y REINICIAR (SAVE & REBOOT)

- Guardar los cambios permanentemente en la memoria Flash:
```text
    <3Com> save
    -> Preguntara: "The current configuration will be written to the device. Are you sure? [Y/N]:"
    -> Presiona 'y' y luego Enter.

- Reiniciar el switch:
    <3Com> reboot
    -> Te preguntara si deseas guardar los cambios pendientes antes del reinicio.

- Restaurar configuracion de fabrica (Reset total):
    <3Com> reset saved-configuration
    -> Presiona 'y' para confirmar, y luego reinicia con:
    <3Com> reboot
    -> Cuando pregunte si deseas guardar cambios antes de reiniciar, responde: 'n' (No).
```
