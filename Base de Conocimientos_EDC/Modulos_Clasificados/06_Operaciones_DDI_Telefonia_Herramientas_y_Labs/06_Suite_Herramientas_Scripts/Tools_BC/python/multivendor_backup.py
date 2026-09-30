#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Herramienta de Respaldo y Diff de Configuraciones Multi-Vendor (Netmiko)
Network Engineering & Cybersecurity Master Compendium - BC
Modulo: SW (Switching Multi-Vendor) / Troubleshooting
Soporte: Cisco IOS/XE, Huawei VRP, Aruba OS-CX, MikroTik RouterOS
"""

import os
import sys
import datetime
import difflib
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.syntax import Syntax

try:
    from netmiko import ConnectHandler
    from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException
except ImportError:
    pass

console = Console()

COMANDOS_RESPALDO = {
    "cisco_ios": "show running-config",
    "cisco_xe": "show running-config",
    "huawei": "display current-configuration",
    "aruba_os": "show running-config",
    "mikrotik_routeros": "/export verbose"
}

def crear_directorio_backups():
    directorio = os.path.join(os.path.dirname(__file__), "backups")
    os.makedirs(directorio, exist_ok=True)
    return directorio

def respaldar_equipo(ip: str, vendor: str, usuario: str, password: str, puerto: int = 22, enable_secret: str = None) -> str:
    """
    Se conecta al equipo de red usando Netmiko y extrae la configuracion activa.
    """
    comando = COMANDOS_RESPALDO.get(vendor, "show running-config")
    device_params = {
        "device_type": vendor,
        "host": ip,
        "username": usuario,
        "password": password,
        "port": puerto,
        "fast_cli": False,
        "timeout": 15
    }
    if enable_secret:
        device_params["secret"] = enable_secret

    console.print(f"[bold cyan][*][/bold cyan] Conectando a [bold white]{ip}[/bold white] ({vendor}) via SSH...")
    try:
        net_connect = ConnectHandler(**device_params)
        if enable_secret and vendor.startswith("cisco"):
            net_connect.enable()

        console.print(f"[bold cyan][*][/bold cyan] Extrayendo configuracion mediante '{comando}'...")
        configuracion = net_connect.send_command(comando)
        net_connect.disconnect()

        # Guardar en archivo
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        dir_backups = crear_directorio_backups()
        nombre_archivo = f"{vendor}_{ip}_{timestamp}.cfg"
        ruta_completa = os.path.join(dir_backups, nombre_archivo)

        with open(ruta_completa, "w", encoding="utf-8") as f:
            f.write(configuracion)

        console.print(f"[bold green][OK] Respaldo guardado exitosamente en:[/bold green] {ruta_completa}")
        return ruta_completa

    except Exception as e:
        console.print(f"[bold red][ERROR DE CONEXION][/bold red] {e}")
        return ""

def comparar_configuraciones(archivo_anterior: str, archivo_nuevo: str):
    """
    Compara dos archivos de configuracion e imprime las diferencias (Diff) con codigo de colores.
    """
    if not os.path.exists(archivo_anterior) or not os.path.exists(archivo_nuevo):
        console.print("[bold red][ERROR][/bold red] Uno o ambos archivos de configuracion no existen.")
        return

    with open(archivo_anterior, "r", encoding="utf-8", errors="ignore") as f:
        lineas_ant = f.readlines()
    with open(archivo_nuevo, "r", encoding="utf-8", errors="ignore") as f:
        lineas_nue = f.readlines()

    diff = list(difflib.unified_diff(
        lineas_ant, lineas_nue,
        fromfile=os.path.basename(archivo_anterior),
        tofile=os.path.basename(archivo_nuevo),
        lineterm=""
    ))

    if not diff:
        console.print("[bold green][SIN CAMBIOS][/bold green] Las dos configuraciones son 100% identicas.")
        return

    console.print(f"\n[bold yellow]=== REPORTE DE DIFERENCIAS (DIFF AUDIT) ===[/bold yellow]\n")
    for linea in diff:
        if linea.startswith("+") and not linea.startswith("+++"):
            console.print(f"[green]{linea}[/green]")
        elif linea.startswith("-") and not linea.startswith("---"):
            console.print(f"[red]{linea}[/red]")
        elif linea.startswith("@@"):
            console.print(f"[cyan]{linea}[/cyan]")
        else:
            console.print(f"[gray]{linea}[/gray]")

def demo_simulacion():
    """Genera dos configuraciones de ejemplo y ejecuta un Diff real para demostracion."""
    dir_backups = crear_directorio_backups()
    cfg1 = os.path.join(dir_backups, "demo_cisco_v1.cfg")
    cfg2 = os.path.join(dir_backups, "demo_cisco_v2.cfg")

    contenido_v1 = (
        "hostname SW-CORE-01\n"
        "!\n"
        "interface GigabitEthernet0/1\n"
        " description Enlace WAN Primario\n"
        " ip address 10.10.10.1 255.255.255.252\n"
        "!\n"
        "router ospf 1\n"
        " network 10.10.10.0 0.0.0.3 area 0\n"
    )
    contenido_v2 = (
        "hostname SW-CORE-01\n"
        "!\n"
        "interface GigabitEthernet0/1\n"
        " description Enlace WAN Primario (Actualizado 10G)\n"
        " ip address 10.10.10.1 255.255.255.252\n"
        "!\n"
        "interface GigabitEthernet0/2\n"
        " description Enlace Backup FortiGate\n"
        " ip address 10.20.20.1 255.255.255.252\n"
        "!\n"
        "router ospf 1\n"
        " router-id 1.1.1.1\n"
        " network 10.10.10.0 0.0.0.3 area 0\n"
        " network 10.20.20.0 0.0.0.3 area 0\n"
    )

    with open(cfg1, "w", encoding="utf-8") as f:
        f.write(contenido_v1)
    with open(cfg2, "w", encoding="utf-8") as f:
        f.write(contenido_v2)

    console.print("[bold green][MODO DEMO][/bold green] Archivos de prueba creados. Ejecutando comparativa Diff:")
    comparar_configuraciones(cfg1, cfg2)

def main():
    console.print(Panel.fit(
        "[bold cyan]BC NETWORK - MULTI-VENDOR CONFIG BACKUP & AUDIT DIFF[/bold cyan]\n"
        "[white]Soporte SSH: Cisco IOS/XE, Huawei VRP, ArubaOS-CX, MikroTik RouterOS[/white]",
        border_style="cyan"
    ))

    console.print("[1] Respaldar equipo remoto via SSH (Netmiko)")
    console.print("[2] Comparar dos archivos de configuracion existentes (Audit Diff)")
    console.print("[3] Ejecutar Demostracion / Prueba con archivos simulados")
    console.print("[0] Salir")

    opcion = console.input("\n[bold yellow]Seleccione una opcion [0-3]: [/bold yellow]").strip()

    if opcion == "1":
        console.print("\n[bold]Fabricantes soportados:[/bold] cisco_ios, huawei, aruba_os, mikrotik_routeros")
        vendor = console.input("Tipo de dispositivo (vendor) [cisco_ios]: ").strip() or "cisco_ios"
        ip = console.input("Direccion IP del equipo: ").strip()
        usuario = console.input("Usuario SSH: ").strip()
        password = console.input("Contrasena SSH: ").strip()
        enable = console.input("Enable secret (Cisco - Opcional): ").strip() or None
        if ip and usuario and password:
            respaldar_equipo(ip, vendor, usuario, password, enable_secret=enable)
        else:
            console.print("[red]Datos incompletos.[/red]")
    elif opcion == "2":
        f1 = console.input("Ruta del archivo de configuracion base/anterior: ").strip()
        f2 = console.input("Ruta del archivo de configuracion nuevo: ").strip()
        comparar_configuraciones(f1, f2)
    elif opcion == "3":
        demo_simulacion()
    else:
        console.print("Saliendo.")

if __name__ == "__main__":
    main()
