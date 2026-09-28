# GUIA CISCO IOS - PARTE 1: MODOS DE CONFIGURACION, NAVEGACION Y PRIMEROS COMANDOS


---



## 1. ¿QUE ES CISCO IOS?

Cisco IOS (Internetwork Operating System) e IOS-XE son los sistemas operativos 
que controlan los switches Cisco Catalyst (como las series 2960, 3560, 3750, 3850,
9200, 9300, etc.).



## 2. JERARQUIA DE MODOS EN CISCO

Para configurar un switch Cisco se navega a traves de diferentes modos:


### A) Modo Usuario (User EXEC Mode):

   - Prompt: Switch>
   - Solo permite tareas basicas de monitoreo y ping. No permite ver configuraciones 
     completas ni modificar parametros.
   - Para pasar al siguiente nivel, escribe: enable


### B) Modo Privilegiado (Privileged EXEC Mode / Enable Mode):

   - Prompt: Switch#
   - Permite ver toda la configuracion activa, estados de interfaces, tablas de enrutamiento
     y reiniciar el equipo.
   - Para entrar a configuracion, escribe: configure terminal (o conf t)


### C) Modo de Configuracion Global (Global Configuration Mode):

   - Prompt: Switch(config)#
   - Modifica parametros generales que afectan a todo el switch (nombre, contrasenas,
     VLANs, enrutamiento, etc.).


### D) Modos Especificos (Interfaces, Lineas, Protocolos):

   - Prompt: Switch(config-if)#  (para un puerto o VLAN)
   - Prompt: Switch(config-line)# (para consola o lineas VTY remotas)
   - Prompt: Switch(config-router)# (para protocolos como OSPF)



## 3. ATAJOS DE TECLADO Y TRUCOS INDISPENSABLES

- ?: Muestra los comandos disponibles o la ayuda de la palabra actual.
- TAB: Autocompleta el comando.
- exit: Retrocede un nivel hacia atras.
- end (o Ctrl + Z): Vuelve directamente al modo privilegiado (Switch#) desde cualquier nivel.
- no [comando]: Niega, deshabilita o elimina cualquier comando (ej. "no shutdown" enciende
  un puerto, "no vlan 10" elimina una VLAN).
- do [comando]: ¡TRUCO DE ORO! Permite ejecutar comandos de visualizacion (show) desde 
  el modo de configuracion sin tener que salirte.
  Ejemplo: Switch(config-if)# do show ip int brief



## 4. COMANDOS ESENCIALES DE VISUALIZACION (SHOW)

Todos se ejecutan desde el modo privilegiado Switch# (o usando "do show" en config):

```cisco
Switch# show version
  -> Muestra el modelo del switch, version de IOS, numero de serie y tiempo encendido (uptime).

Switch# show running-config  (o sh run)
  -> Muestra la configuracion activa que esta corriendo en memoria RAM.

Switch# show startup-config  (o sh start)
  -> Muestra la configuracion que se cargara al reiniciar (guardada en NVRAM).

Switch# show ip interface brief  (o sh ip int br)
  -> Resumen de interfaces con su direccion IP, estado administrativo y protocolo (up/down).

Switch# show interfaces status
  -> Tabla visual de todos los puertos fisicos: nombre, estado (connected/notconnect),
     VLAN a la que pertenecen, velocidad (10/100/1000) y tipo de duplex.

Switch# show mac address-table
  -> Muestra las direcciones MAC aprendidas por el switch y en que puerto fisico estan conectadas.
```


## 5. GUARDAR Y REINICIAR (SAVE & RELOAD)

Todo lo que configures esta solo en memoria RAM (running-config). Si el switch se 
apaga, se perdera si no guardas:

- Guardar cambios en la memoria permanente NVRAM:
```cisco
    Switch# write memory   (o simplemente: wr)
    -- Metodo oficial equivalente:
    Switch# copy running-config startup-config

- Reiniciar el switch:
    Switch# reload
    (Si hay cambios sin guardar, te preguntara: "System configuration has been modified. Save? [yes/no]:")

- Borrar la configuracion de fabrica (Reset total):
    ¡OJO! En switches Cisco no basta con borrar el startup-config, tambien debes borrar
    el archivo de VLANs (vlan.dat):
    Switch# erase startup-config
    Switch# delete flash:vlan.dat   (presiona Enter a cada confirmacion)
    Switch# reload
```
