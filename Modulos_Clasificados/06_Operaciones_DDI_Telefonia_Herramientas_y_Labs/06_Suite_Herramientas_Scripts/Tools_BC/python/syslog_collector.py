#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Servidor y Colector Syslog en Vivo (RFC 3164 / RFC 5424)
Network Engineering & Cybersecurity Master Compendium - BC
Modulo: Servicios_DDI_y_Gestion / Troubleshooting / SOC
"""

import socket
import re
import datetime
import threading
import time
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

NOMBRES_FACILITY = [
    "kernel", "user", "mail", "system", "auth", "syslog", "lpr", "news",
    "uucp", "clock", "authpriv", "ftp", "ntp", "logaudit", "logalert", "cron",
    "local0", "local1", "local2", "local3", "local4", "local5", "local6", "local7"
]

NOMBRES_SEVERITY = [
    ("EMERGENCY", "bold white on red"),
    ("ALERT", "bold red"),
    ("CRITICAL", "red"),
    ("ERROR", "bold magenta"),
    ("WARNING", "yellow"),
    ("NOTICE", "cyan"),
    ("INFO", "green"),
    ("DEBUG", "gray")
]

def decodificar_syslog(mensaje_crudo: str):
    """
    Decodifica el encabezado PRI de Syslog: <PRI>Mensaje
    PRI = Facility * 8 + Severity
    """
    facility_nombre = "local7"
    severity_nombre = "INFO"
    severity_estilo = "green"
    cuerpo = mensaje_crudo

    match = re.match(r"^<(\d{1,3})>(.*)", mensaje_crudo)
    if match:
        pri = int(match.group(1))
        cuerpo = match.group(2)
        facility_idx = pri // 8
        severity_idx = pri % 8

        if facility_idx < len(NOMBRES_FACILITY):
            facility_nombre = NOMBRES_FACILITY[facility_idx]
        if severity_idx < len(NOMBRES_SEVERITY):
            severity_nombre, severity_estilo = NOMBRES_SEVERITY[severity_idx]

    return facility_nombre, severity_nombre, severity_estilo, cuerpo

def iniciar_servidor_syslog(ip_escucha: str = "0.0.0.0", puerto: int = 514, log_file: str = "syslog_captura.log"):
    """
    Inicia el socket UDP de escucha de eventos Syslog.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.bind((ip_escucha, puerto))
    except PermissionError:
        console.print(f"[bold red][ERROR DE PERMISOS][/bold red] El puerto {puerto} requiere privilegios de Administrador.")
        puerto_alt = 1514
        console.print(f"[yellow]Intentando en puerto alternativo {puerto_alt}...[/yellow]")
        try:
            sock.bind((ip_escucha, puerto_alt))
            puerto = puerto_alt
        except Exception as e:
            console.print(f"[bold red][ERROR FATAL][/bold red] {e}")
            return
    except Exception as e:
        console.print(f"[bold red][ERROR][/bold red] No se pudo vincular el socket: {e}")
        return

    console.print(f"[bold green][OK] Servidor Syslog activo escuchando en UDP {ip_escucha}:{puerto}[/bold green]")
    console.print(f"[gray]Guardando registros en: {log_file}[/gray]")
    console.print("[cyan]Esperando mensajes de routers, switches y firewalls... (Presione Ctrl+C para salir)[/cyan]\n")

    try:
        while True:
            datos, addr = sock.recvfrom(4096)
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            mensaje = datos.decode("utf-8", errors="ignore").strip()

            facility, severity, estilo, cuerpo = decodificar_syslog(mensaje)
            origen_ip = addr[0]

            # Imprimir en consola con formato enriquecido
            console.print(
                f"[gray]{timestamp}[/gray] | [bold white]{origen_ip}[/bold white] | "
                f"[{estilo}][{severity}][/{estilo}] | [cyan]({facility})[/cyan] {cuerpo}"
            )

            # Persistir en archivo
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(f"[{timestamp}] [{origen_ip}] [{severity}] ({facility}) {cuerpo}\n")

    except KeyboardInterrupt:
        console.print("\n[yellow]Servidor Syslog detenido por el usuario.[/yellow]")
    finally:
        sock.close()

def enviar_log_prueba(puerto: int = 514):
    """Envia un mensaje Syslog de prueba simulando la caida de una interfaz de switch."""
    time.sleep(1)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # PRI 187 = local7 (23*8 = 184) + Error (3) -> 187
    msg_cisco = "<187>%LINK-3-UPDOWN: Interface GigabitEthernet0/1, changed state to down"
    sock.sendto(msg_cisco.encode('utf-8'), ("127.0.0.1", puerto))
    sock.close()

def main():
    console.print(Panel.fit(
        "[bold cyan]BC SERVICES - SERVIDOR COLECTOR SYSLOG UDP EN VIVO (RFC 5424)[/bold cyan]\n"
        "[white]Monitoreo en tiempo real de eventos de routers, switches y firewalls[/white]",
        border_style="cyan"
    ))

    console.print("[1] Iniciar Servidor Syslog en puerto estandar UDP 514 (Requiere Admin)")
    console.print("[2] Iniciar Servidor Syslog en puerto alternativo UDP 1514 (Modo Lab)")
    console.print("[3] Probar emision de mensaje Syslog simulado (Test Local)")
    console.print("[0] Salir")

    opt = console.input("\n[bold yellow]Seleccione una opcion [0-3]: [/bold yellow]").strip()
    if opt == "1":
        iniciar_servidor_syslog(puerto=514)
    elif opt == "2":
        iniciar_servidor_syslog(puerto=1514)
    elif opt == "3":
        console.print("[*] Iniciando prueba con hilo emisor...")
        threading.Thread(target=enviar_log_prueba, args=(1514,), daemon=True).start()
        iniciar_servidor_syslog(puerto=1514)
    else:
        console.print("Saliendo.")

if __name__ == "__main__":
    main()
