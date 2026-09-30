#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Escáner Multihilo TCP y Banner Grabbing para Infraestructura de Red
Network Engineering & Cybersecurity Master Compendium - BC
Modulo: Ciberseguridad_OSI / Troubleshooting / Firewalls_y_VPN
"""

import socket
import sys
import concurrent.futures
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import track

console = Console()

PUERTOS_RED_INFRA = {
    21: "FTP",
    22: "SSH (Gestion Segura)",
    23: "Telnet (Gestion Insegura)",
    25: "SMTP",
    49: "TACACS+ (AAA)",
    53: "DNS",
    80: "HTTP",
    88: "Kerberos",
    110: "POP3",
    123: "NTP",
    135: "MS-RPC",
    139: "NetBIOS",
    143: "IMAP",
    161: "SNMP",
    179: "BGP (Border Gateway Protocol)",
    389: "LDAP",
    443: "HTTPS",
    445: "SMB",
    500: "ISAKMP / IPsec IKE",
    514: "Syslog",
    636: "LDAPS",
    646: "LDP (MPLS)",
    873: "Rsync",
    1433: "MSSQL",
    1521: "Oracle DB",
    1723: "PPTP VPN",
    1812: "RADIUS Auth",
    1813: "RADIUS Acct",
    3306: "MySQL",
    3389: "RDP (Escritorio Remoto)",
    5060: "SIP (VoIP)",
    5432: "PostgreSQL",
    5900: "VNC",
    8080: "HTTP-Proxy/Alt",
    8443: "HTTPS-Alt"
}

def capturar_banner(ip: str, puerto: int, timeout: float = 1.0) -> tuple:
    """Intenta conectarse y capturar el mensaje de bienvenida (Banner) del servicio."""
    banner = ""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            if s.connect_ex((ip, puerto)) == 0:
                # Intentar leer banner
                try:
                    s.sendall(b"HEAD / HTTP/1.0\r\n\r\n" if puerto in [80, 8080, 443, 8443] else b"\r\n")
                    raw_data = s.recv(1024)
                    banner = raw_data.decode("utf-8", errors="ignore").strip().splitlines()[0][:60]
                except Exception:
                    banner = "(Conexion aceptada sin banner)"
                return puerto, True, banner
            else:
                return puerto, False, ""
    except Exception:
        return puerto, False, ""

def escanear_servicios(ip: str, lista_puertos: list, hilos: int = 50):
    console.print(f"\n[bold cyan][*] Iniciando escaneo multihilo sobre [white]{ip}[/white] ({len(lista_puertos)} puertos)...[/bold cyan]\n")

    puertos_abiertos = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=hilos) as executor:
        futuros = {executor.submit(capturar_banner, ip, p): p for p in lista_puertos}
        for future in concurrent.futures.as_completed(futuros):
            puerto, abierto, banner = future.result()
            if abierto:
                servicio = PUERTOS_RED_INFRA.get(puerto, "Servicio Personalizado")
                puertos_abiertos.append({
                    "puerto": puerto,
                    "servicio": servicio,
                    "banner": banner
                })

    # Mostrar resultados
    if not puertos_abiertos:
        console.print(f"[yellow][i] No se detectaron puertos TCP abiertos en {ip} dentro de la seleccion solicitada.[/yellow]")
        return

    # Ordenar por numero de puerto
    puertos_abiertos.sort(key=lambda x: x["puerto"])

    table = Table(title=f"Servicios Activos Detectados - Host: {ip}", header_style="bold green")
    table.add_column("Puerto TCP", justify="center", style="yellow")
    table.add_column("Servicio de Red", style="bold cyan")
    table.add_column("Banner / Firma Detectada", style="white")

    for item in puertos_abiertos:
        table.add_row(str(item["puerto"]), item["servicio"], item["banner"])

    console.print(table)
    console.print(f"\n[bold green][OK] Total de puertos abiertos encontrados: {len(puertos_abiertos)}[/bold green]")

def main():
    console.print(Panel.fit(
        "[bold cyan]BC NETWORK - ESCANER MULTIHILO TCP CON BANNER GRABBING[/bold cyan]\n"
        "[white]Identificacion de Puertos de Gestion (SSH, Telnet), Routing (BGP), DDI y Bases de Datos[/white]",
        border_style="cyan"
    ))

    ip = console.input("[bold yellow]Direccion IP o Hostname destino: [/bold yellow]").strip()
    if not ip:
        ip = "127.0.0.1"
        console.print(f"[gray]Usando loopback: {ip}[/gray]")

    console.print("\n[1] Escanear puertos clave de Infraestructura de Red (35 puertos estandar)")
    console.print("[2] Escanear rango personalizado (ej. 1 a 1024)")
    console.print("[3] Escanear lista especifica de puertos separados por coma")

    opt = console.input("\nSeleccione modo de escaneo [1-3] [1]: ").strip() or "1"

    if opt == "1":
        puertos = list(PUERTOS_RED_INFRA.keys())
    elif opt == "2":
        inicio = int(console.input("Puerto inicial: ").strip() or 1)
        fin = int(console.input("Puerto final: ").strip() or 1024)
        puertos = list(range(inicio, fin + 1))
    elif opt == "3":
        puertos_str = console.input("Ingrese puertos separados por coma (ej. 22,80,443,3389): ").strip()
        puertos = [int(p.strip()) for p in puertos_str.split(",") if p.strip().isdigit()]
    else:
        puertos = list(PUERTOS_RED_INFRA.keys())

    escanear_servicios(ip, puertos)

if __name__ == "__main__":
    main()
