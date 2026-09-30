#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Calculadora Profesional VLSM (Variable Length Subnet Masking)
Network Engineering & Cybersecurity Master Compendium - BC
Modulo: OSI / Routing_y_WAN / Servicios_DDI_y_Gestion
"""

import ipaddress
import math
import sys
import json
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

def calcular_vlsm(red_base_str: str, subredes_pedidas: list) -> list:
    """
    Calcula la asignacion de subredes VLSM optimizada ordenando por tamano de hosts.
    """
    try:
        red_base = ipaddress.ip_network(red_base_str, strict=False)
    except ValueError as e:
        console.print(f"[bold red][ERROR][/bold red] Red principal invalida: {e}")
        return []

    # Ordenar subredes solicitadas de mayor a menor numero de hosts requeridos
    subredes_ordenadas = sorted(subredes_pedidas, key=lambda x: x['hosts'], reverse=True)

    ip_actual = int(red_base.network_address)
    ip_limite = int(red_base.broadcast_address)

    resultados = []

    for item in subredes_ordenadas:
        nombre = item['nombre']
        hosts_necesarios = item['hosts']

        # Se requieren hosts + 2 (red y broadcast)
        total_ips_necesarias = hosts_necesarios + 2
        bits_host = math.ceil(math.log2(total_ips_necesarias))
        prefijo = 32 - bits_host
        tamano_bloque = 2 ** bits_host

        # Alinear a limite de bloque
        if ip_actual % tamano_bloque != 0:
            ip_actual = ((ip_actual // tamano_bloque) + 1) * tamano_bloque

        ip_red = ipaddress.IPv4Address(ip_actual)
        ip_broadcast = ipaddress.IPv4Address(ip_actual + tamano_bloque - 1)

        if int(ip_broadcast) > ip_limite:
            console.print(f"[bold red][DESBORDAMIENTO][/bold red] La subred '{nombre}' ({hosts_necesarios} hosts) supera el espacio de la red principal {red_base_str}!")
            break

        ip_primera_util = ipaddress.IPv4Address(ip_actual + 1)
        ip_ultima_util = ipaddress.IPv4Address(ip_actual + tamano_bloque - 2)
        mascara = ipaddress.IPv4Network(f"{ip_red}/{prefijo}").netmask

        hosts_asignables = tamano_bloque - 2
        desperdicio = hosts_asignables - hosts_necesarios

        resultados.append({
            "nombre": nombre,
            "hosts_requeridos": hosts_necesarios,
            "hosts_asignables": hosts_asignables,
            "prefijo": f"/{prefijo}",
            "mascara": str(mascara),
            "red": str(ip_red),
            "rango_util": f"{ip_primera_util} - {ip_ultima_util}",
            "broadcast": str(ip_broadcast),
            "desperdicio": desperdicio,
            "cisco_cfg": f"ip address {ip_primera_util} {mascara}",
            "huawei_cfg": f"ip address {ip_primera_util} {prefijo}"
        })

        # Avanzar puntero para la siguiente subred
        ip_actual += tamano_bloque

    return resultados

def mostrar_tabla_vlsm(resultados: list, red_base: str):
    table = Table(title=f"Plan de Direccionamiento VLSM - Red Base: {red_base}", header_style="bold magenta")
    table.add_column("Subred", style="cyan", no_wrap=True)
    table.add_column("Requeridos", justify="right")
    table.add_column("Asignables", justify="right")
    table.add_column("Prefijo", style="green")
    table.add_column("Mascara", style="yellow")
    table.add_column("Red", style="bold white")
    table.add_column("Rango Util", style="white")
    table.add_column("Broadcast", style="red")

    for r in resultados:
        table.add_row(
            r["nombre"],
            str(r["hosts_requeridos"]),
            str(r["hosts_asignables"]),
            r["prefijo"],
            r["mascara"],
            r["red"],
            r["rango_util"],
            r["broadcast"]
        )

    console.print(table)

def main():
    console.print(Panel.fit(
        "[bold cyan]BC NETWORK TOOLKIT - CALCULADORA VLSM AVANZADA[/bold cyan]\n"
        "[white]Generador de Planes de Direccionamiento IP y Comandos CLI (Cisco/Huawei)[/white]",
        border_style="cyan"
    ))

    red_input = console.input("[bold yellow]Ingrese la Red Mayor Base con prefijo (ej. 192.168.1.0/24 o 10.0.0.0/16): [/bold yellow]").strip()
    if not red_input:
        red_input = "192.168.10.0/24"
        console.print(f"[gray]Usando valor por defecto: {red_input}[/gray]")

    subredes = []
    console.print("\n[bold green]Defina las subredes requeridas (Deje el nombre vacio para finalizar):[/bold green]")
    
    # Modo rapido o manual
    modo = console.input("[bold white]¿Desea cargar un perfil de ejemplo rapido? (S/N) [N]: [/bold white]").strip().upper()
    if modo == "S":
        subredes = [
            {"nombre": "VLAN_10_Servidores", "hosts": 50},
            {"nombre": "VLAN_20_Usuarios", "hosts": 100},
            {"nombre": "VLAN_30_WiFi_Invitados", "hosts": 25},
            {"nombre": "WAN_Punto_a_Punto", "hosts": 2}
        ]
    else:
        while True:
            nombre = console.input("  Nombre de la subred / VLAN: ").strip()
            if not nombre:
                if len(subredes) == 0:
                    console.print("[red]Debe ingresar al menos una subred.[/red]")
                    continue
                break
            try:
                hosts = int(console.input(f"  Numero de hosts necesarios para '{nombre}': ").strip())
                subredes.append({"nombre": nombre, "hosts": hosts})
            except ValueError:
                console.print("[red]Numero invalido, intente de nuevo.[/red]")

    console.print("\n[bold cyan][*] Calculando asignacion optima VLSM...[/bold cyan]\n")
    resultados = calcular_vlsm(red_input, subredes)

    if resultados:
        mostrar_tabla_vlsm(resultados, red_input)

        # Plantillas de comandos
        console.print("\n[bold yellow]Comandos de Configuracion Listos para Switches/Routers:[/bold yellow]")
        for r in resultados:
            console.print(f"[cyan]• {r['nombre']}:[/cyan]")
            console.print(f"   [green]Cisco IOS (SVI/Interface):[/green]   {r['cisco_cfg']}")
            console.print(f"   [magenta]Huawei VRP (Vlanif):[/magenta]          {r['huawei_cfg']}")

        # Opcion de exportar
        guardar = console.input("\n[bold white]¿Desea guardar el plan en formato JSON? (S/N) [N]: [/bold white]").strip().upper()
        if guardar == "S":
            archivo_salida = "plan_vlsm_export.json"
            with open(archivo_salida, "w", encoding="utf-8") as f:
                json.dump({"red_base": red_input, "plan": resultados}, f, indent=4)
            console.print(f"[bold green][OK] Plan guardado con exito en '{archivo_salida}'[/bold green]")

if __name__ == "__main__":
    main()
