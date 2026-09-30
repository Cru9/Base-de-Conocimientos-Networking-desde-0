#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auditor y Escaner de Protocolos de Redes Industriales OT / SCADA
Network Engineering & Cybersecurity Master Compendium - BC
Modulo: Redes_Industriales_OT (Modelo Purdue & ISA/IEC 62443)
"""

import socket
import sys
import time
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

PUERTOS_OT = {
    502:   ("Modbus TCP", "Capa 1/2 Purdue - Control de PLCs y RTUs (Sin autenticacion nativa)"),
    102:   ("Siemens S7 Comm", "Capa 1/2 Purdue - Comunicacion propietaria con PLCs S7-300/400/1200/1500"),
    44818: ("EtherNet/IP (CIP)", "Capa 1/2 Purdue - Rockwell Automation / Allen-Bradley"),
    20000: ("DNP3", "Capa 1/2 Purdue - Telemetria en subestaciones electricas y agua"),
    2404:  ("IEC 60870-5-104", "Capa 1/2 Purdue - Telecontrol de energia electrica"),
    4840:  ("OPC UA", "Capa 2/3 Purdue - Intercambio seguro de datos HMI/SCADA"),
    47808: ("BACnet/IP", "Capa 1/2 Purdue - Automatizacion y control de edificios (BMS/HVAC)"),
    1883:  ("MQTT (IIoT)", "Capa 3/4 Purdue - Telemetria IoT industrial (Texto claro)"),
    8883:  ("MQTT sobre TLS", "Capa 3/4 Purdue - Telemetria IoT industrial cifrada"),
    23:    ("Telnet Inseguro", "Capa 1/2/3 - Gestion insegura en dispositivos embebidos obsoletos"),
    80:    ("HTTP HMI", "Capa 2/3 - Interfaz web de monitoreo sin cifrar")
}

def sondear_puerto_ot(ip: str, puerto: int, timeout: float = 1.5) -> tuple:
    """Intenta establecer handshake TCP en el puerto industrial y mide latencia en ms."""
    inicio = time.perf_counter()
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            res = s.connect_ex((ip, puerto))
            latencia = (time.perf_counter() - inicio) * 1000
            if res == 0:
                return True, round(latencia, 2)
            else:
                return False, 0
    except Exception:
        return False, 0

def escanear_dispositivo_ot(ip_destino: str):
    console.print(f"\n[bold cyan][*] Auditando protocolos industriales OT en [white]{ip_destino}[/white]...[/bold cyan]\n")

    table = Table(title=f"Auditoria OT / SCADA (Purdue Model) - Host: {ip_destino}", header_style="bold magenta")
    table.add_column("Puerto", justify="center", style="yellow")
    table.add_column("Protocolo Industrial", style="bold white")
    table.add_column("Nivel Purdue / Riesgo", style="gray")
    table.add_column("Estado", style="bold")
    table.add_column("Latencia ms", justify="right")

    abiertos = 0

    for puerto, (proto, descripcion) in PUERTOS_OT.items():
        abierto, latencia = sondear_puerto_ot(ip_destino, puerto)
        if abierto:
            abiertos += 1
            estado_txt = "[bold red]ABIERTO / EXPUESTO[/bold red]"
            lat_txt = f"[green]{latencia} ms[/green]"
        else:
            estado_txt = "[gray]Cerrado / Filtrado[/gray]"
            lat_txt = "-"

        table.add_row(str(puerto), proto, descripcion, estado_txt, lat_txt)

    console.print(table)

    # Diagnostico de seguridad industrial
    console.print("\n[bold yellow]=== EVALUACION DE POSTURA DE SEGURIDAD (ISA/IEC 62443) ===[/bold yellow]")
    if abiertos == 0:
        console.print("[bold green][AISLAMIENTO OPTIMO][/bold green] Ningun puerto OT critico respondio. Cumple con segmentacion de zona.")
    else:
        console.print(f"[bold red][ALERTA DE SEGURIDAD INDUSTRIAL][/bold red] Se detectaron {abiertos} servicios industriales escuchando.")
        console.print("[yellow]Recomendacion:[/yellow] Verificar que este equipo pertenezca exclusivamente a la Zona Celda/Area (Nivel 1/2) y que exista un Firewall Industrial (Conduit) impidiendo el acceso directo desde la red corporativa IT (Nivel 4/5).")

def main():
    console.print(Panel.fit(
        "[bold cyan]BC OT SECURITY - AUDITOR DE PUERTOS Y PROTOCOLOS INDUSTRIALES[/bold cyan]\n"
        "[white]Sondeo de Modbus, Siemens S7, EtherNet/IP, DNP3, BACnet y OPC UA[/white]",
        border_style="cyan"
    ))

    ip = console.input("[bold yellow]Ingrese la direccion IP del PLC, RTU, HMI o Gateway OT (ej. 127.0.0.1 o IP local): [/bold yellow]").strip()
    if not ip:
        ip = "127.0.0.1"
        console.print(f"[gray]Usando loopback local: {ip}[/gray]")

    escanear_dispositivo_ot(ip)

if __name__ == "__main__":
    main()
