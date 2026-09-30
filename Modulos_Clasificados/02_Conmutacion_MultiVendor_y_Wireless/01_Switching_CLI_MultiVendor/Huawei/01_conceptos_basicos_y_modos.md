# GUIA HUAWEI VRP - PARTE 1: CONCEPTOS BASICOS, MODOS Y PRIMEROS COMANDOS


---



## 1. ¿QUE ES HUAWEI VRP?

VRP (Versatile Routing Platform) es el sistema operativo que ejecutan los switches
y routers de Huawei. Es similar a Cisco IOS, pero con su propia sintaxis y comandos.



## 2. MODOS DE TRABAJO (JERARQUIA DE NAVEGACION)

En Huawei existen 3 niveles principales de comando:


### A) Modo Usuario (User View):

   - Prompt: <HUAWEI>
   - Funcion: Solo permite ver estados basicos, pruebas de ping y comandos de monitoreo.
   - No permite cambiar la configuracion del switch.


### B) Modo Sistema (System View):

   - Prompt: [HUAWEI]
   - Como entrar: 
```text
       <HUAWEI> system-view
   - Funcion: Desde aqui se configuran parametros globales (nombre, usuarios, vlans, etc.).

C) Modos de Interfaz / Protocolo (Interface / Protocol View):
   - Prompt: [HUAWEI-GigabitEthernet0/0/1] o [HUAWEI-vlan10]
   - Como entrar:
       [HUAWEI] interface GigabitEthernet 0/0/1
   - Funcion: Configuracion especifica de un puerto, una VLAN, o un protocolo.
```


## 3. ATAJOS DE TECLADO Y NAVEGACION

- ?: Muestra los comandos disponibles o la ayuda de la palabra actual.
- TAB: Autocompleta el comando.
- quit: Retrocede un nivel atras (de interfaz a system, o de system a user).
- return (o Ctrl + Z): Vuelve directamente al modo usuario <HUAWEI> desde cualquier nivel.
- undo: Es el equivalente al "no" de Cisco. Se usa para borrar, deshabilitar o revertir 
        cualquier comando.
        Ejemplo: "undo shutdown" (enciende el puerto), "undo vlan 10" (borra la vlan 10).



## 4. COMANDOS ESENCIALES DE VISUALIZACION (DISPLAY)

En Huawei, en lugar de "show" se utiliza "display" (o la abreviatura "dis").

```text
<HUAWEI> display version
  -> Muestra el modelo del switch, tiempo encendido (uptime) y version de VRP.

<HUAWEI> display current-configuration
  -> Muestra la configuracion activa que esta corriendo en memoria RAM.

<HUAWEI> display saved-configuration
  -> Muestra la configuracion que esta guardada en la memoria flash (disco).

<HUAWEI> display interface brief
  -> Muestra un resumen de todos los puertos: estado (UP/DOWN), velocidad y duplex.

<HUAWEI> display ip interface brief
  -> Muestra las interfaces que tienen direcciones IP asignadas.

<HUAWEI> display device
  -> Muestra el estado del hardware, tarjetas, fuentes de poder y ventiladores.
```


## 5. GUARDAR Y REINICIAR (SAVE & REBOOT)

Si configuras algo y se apaga el switch, se perdera si no guardas:

- Guardar cambios en la memoria permanente:
```text
    <HUAWEI> save
    (Preguntara: Are you sure to continue? Presiona 'Y' y luego Enter).

- Reiniciar el switch:
    <HUAWEI> reboot
    (Te preguntara si deseas guardar cambios antes de reiniciar).

- Borrar la configuracion de fabrica (Reset total):
    <HUAWEI> reset saved-configuration
    (Presiona 'Y', y luego reinicia con 'reboot' sin guardar).
```
