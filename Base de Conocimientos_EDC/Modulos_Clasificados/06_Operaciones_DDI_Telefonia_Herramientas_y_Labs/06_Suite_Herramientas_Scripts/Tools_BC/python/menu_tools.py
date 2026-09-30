#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Menu Principal Interactivo de Herramientas Python (Tools_BC)
Network Engineering & Cybersecurity Master Compendium - BC
"""

import sys
import os
import subprocess
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

HERRAMIENTAS = [
    {
        "num": "1",
        "script": "vlsm_calculator.py",
        "nombre": "Calculadora VLSM y Planes de Direccionamiento IP",
        "modulo": "OSI / Routing_y_WAN",
        "desc": "Subnetting optimizado con cálculo de desperdicio y plantillas CLI (Cisco/Huawei)"
    },
    {
        "num": "2",
        "script": "multivendor_backup.py",
        "nombre": "Respaldo y Auditoria Diff Multi-Vendor (Netmiko)",
        "modulo": "SW / Troubleshooting",
        "desc": "Extraccion SSH de configuraciones y comparativa visual entre versiones"
    },
    {
        "num": "3",
        "script": "pcap_analyzer.py",
        "nombre": "Analizador Forense de Capturas PCAP (Scapy)",
        "modulo": "Wireshark_Analysis",
        "desc": "Deteccion de retransmisiones TCP, resets, top talkers y consultas DNS"
    },
    {
        "num": "4",
        "script": "arp_spoof_detector.py",
        "nombre": "Detector de Ataques ARP Spoofing / MITM (Capa 2)",
        "modulo": "Ciberseguridad_OSI",
        "desc": "Monitoreo pasivo en vivo para deteccion de suplantacion de Gateway"
    },
    {
        "num": "5",
        "script": "tls_cert_inspector.py",
        "nombre": "Auditor de Certificados SSL/TLS y Cifrado",
        "modulo": "Ciberseguridad_OSI",
        "desc": "Inspeccion de vigencia de certificados X.509, suites criptograficas y versiones TLS"
    },
    {
        "num": "6",
        "script": "syslog_collector.py",
        "nombre": "Servidor Colector Syslog UDP en Vivo (RFC 5424)",
        "modulo": "Servicios_DDI / SOC",
        "desc": "Captura en tiempo real de eventos de switches y routers clasificados por severidad"
    },
    {
        "num": "7",
        "script": "ot_industrial_scanner.py",
        "nombre": "Auditor de Redes Industriales OT / SCADA (Purdue)",
        "modulo": "Redes_Industriales_OT",
        "desc": "Sondeo de puertos Modbus, Siemens S7, EtherNet/IP, DNP3 y evaluacion IEC 62443"
    },
    {
        "num": "8",
        "script": "port_banner_grabber.py",
        "nombre": "Escaner Multihilo TCP con Banner Grabbing",
        "modulo": "Troubleshooting / Firewalls",
        "desc": "Identificacion rapida de servicios y versiones en equipos de infraestructura"
    }
]

def mostrar_menu():
    while True:
        console.clear()
        console.print(Panel.fit(
            "[bold cyan]BC NETWORK TOOLKIT - SUITE AVANZADA DE HERRAMIENTAS PYTHON[/bold cyan]\n"
            "[white]Network Engineering & Cybersecurity Master Compendium | Cru9[/white]",
            border_style="cyan"
        ))

        table = Table(title="Catalogo de Modulos Python Disponibles", header_style="bold magenta")
        table.add_column("#", justify="center", style="bold yellow")
        table.add_column("Herramienta", style="bold white")
        table.add_column("Dominio / Modulo", style="cyan")
        table.add_column("Descripcion", style="gray")

        for h in HERRAMIENTAS:
            table.add_row(h["num"], h["nombre"], h["modulo"], h["desc"])

        console.print(table)
        console.print("\n[bold yellow]Seleccione el numero de la herramienta a ejecutar o '0' para salir:[/bold yellow]")

        opcion = console.input("[bold cyan]> [/bold cyan]").strip()

        if opcion == "0":
            console.print("[green]Hasta pronto.[/green]")
            break

        seleccionada = next((h for h in HERRAMIENTAS if h["num"] == opcion), None)
        if seleccionada:
            script_path = os.path.join(os.path.dirname(__file__), seleccionada["script"])
            console.clear()
            console.print(f"[bold green][*] Iniciando {seleccionada['nombre']}...[/bold green]\n")
            subprocess.run([sys.executable, script_path])
            console.input("\n[bold gray]Presione Enter para regresar al menu...[/bold gray]")
        else:
            console.print("[red]Opcion no valida.[/red]")
            input("Presione Enter para continuar...")

if __name__ == "__main__":
    mostrar_menu()
