#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auditor de Certificados SSL/TLS y Cifrado
Network Engineering & Cybersecurity Master Compendium - BC
Modulo: Ciberseguridad_OSI (Capa 6 Presentacion / Capa 7 Aplicacion)
"""

import socket
import ssl
import sys
import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

def auditar_certificado_tls(host: str, puerto: int = 443, timeout: int = 5) -> dict:
    """
    Se conecta mediante socket TLS con SNI, descarga el certificado X.509
    y evalua la vigencia, emisor, version del protocolo y suite de cifrado.
    """
    contexto = ssl.create_default_context()
    contexto.check_hostname = False
    contexto.verify_mode = ssl.CERT_NONE  # Permite inspeccionar certificados autofirmados de equipos de red

    resultado = {
        "host": host,
        "puerto": puerto,
        "estado": "ERROR",
        "protocolo_tls": "Desconocido",
        "cipher_suite": "Desconocido",
        "emisor": "Desconocido",
        "sujeto": "Desconocido",
        "dias_restantes": 0,
        "expiracion": "Desconocida",
        "alerta_seguridad": ""
    }

    try:
        with socket.create_connection((host, puerto), timeout=timeout) as sock:
            with contexto.wrap_socket(sock, server_hostname=host) as ssock:
                cert = ssock.getpeercert(binary_form=False)
                # En CERT_NONE getpeercert() devuelve vacio, usamos cert binario o modo cert_optional
                version_tls = ssock.version()
                cipher = ssock.cipher()

                resultado["protocolo_tls"] = version_tls
                resultado["cipher_suite"] = f"{cipher[0]} ({cipher[2]} bits)"

        # Segunda pasada con validacion de fecha decodificando cert binario
        contexto_peercert = ssl.create_default_context()
        contexto_peercert.check_hostname = False
        contexto_peercert.verify_mode = ssl.CERT_OPTIONAL
        
        with socket.create_connection((host, puerto), timeout=timeout) as sock:
            with contexto_peercert.wrap_socket(sock, server_hostname=host) as ssock:
                cert = ssock.getpeercert()

        if cert:
            # Fechas de validez
            formato_fecha = "%b %d %H:%M:%S %Y %Z"
            fecha_exp_str = cert.get("notAfter", "")
            fecha_exp = datetime.datetime.strptime(fecha_exp_str, formato_fecha)
            ahora = datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
            dias_restantes = (fecha_exp - ahora).days

            resultado["expiracion"] = fecha_exp.strftime("%Y-%m-%d %H:%M:%S")
            resultado["dias_restantes"] = dias_restantes

            # Emisor y Sujeto
            sujeto_dict = dict(x[0] for x in cert.get("subject", []))
            emisor_dict = dict(x[0] for x in cert.get("issuer", []))

            resultado["sujeto"] = sujeto_dict.get("commonName", host)
            resultado["emisor"] = emisor_dict.get("organizationName", emisor_dict.get("commonName", "Desconocido"))
            resultado["estado"] = "OK"

            # Evaluacion de seguridad
            alertas = []
            if dias_restantes < 0:
                alertas.append("[bold red]CERTIFICADO VENCIDO[/bold red]")
            elif dias_restantes <= 15:
                alertas.append(f"[bold red]EXPIRA PRONTO ({dias_restantes} dias)[/bold red]")
            elif dias_restantes <= 30:
                alertas.append(f"[bold yellow]Atencion: Expira en {dias_restantes} dias[/bold yellow]")

            if version_tls in ["TLSv1", "TLSv1.1", "SSLv2", "SSLv3"]:
                alertas.append("[bold red]Version TLS Obsoleta e Insegura[/bold red]")

            resultado["alerta_seguridad"] = " | ".join(alertas) if alertas else "[green]Valido y Seguro[/green]"

    except Exception as e:
        resultado["alerta_seguridad"] = f"[red]{str(e)}[/red]"

    return resultado

def mostrar_reporte_tls(hosts: list):
    table = Table(title="Auditoria de Certificados SSL/TLS e Infraestructura Criptografica", header_style="bold cyan")
    table.add_column("Host / Endpoint", style="white")
    table.add_column("Puerto", justify="center")
    table.add_column("TLS Version", style="yellow")
    table.add_column("Dias Rest.", justify="right")
    table.add_column("Expiracion", style="gray")
    table.add_column("Emisor (CA)", style="cyan")
    table.add_column("Estado de Seguridad", style="bold")

    for h in hosts:
        res = auditar_certificado_tls(h)
        dias_str = str(res["dias_restantes"])
        if res["dias_restantes"] < 0:
            dias_style = f"[red]{dias_str}[/red]"
        elif res["dias_restantes"] <= 30:
            dias_style = f"[yellow]{dias_str}[/yellow]"
        else:
            dias_style = f"[green]{dias_str}[/green]"

        table.add_row(
            res["host"],
            str(res["puerto"]),
            res["protocolo_tls"],
            dias_style,
            res["expiracion"],
            res["emisor"],
            res["alerta_seguridad"]
        )

    console.print(table)

def main():
    console.print(Panel.fit(
        "[bold cyan]BC CYBERSECURITY - AUDITOR DE CERTIFICADOS SSL/TLS Y CIPHER SUITES[/bold cyan]\n"
        "[white]Inspeccion de Protocolos Criptograficos, Fechas de Expiracion y Autoridades Emisoras[/white]",
        border_style="cyan"
    ))

    console.print("[1] Auditar un host o firewall especifico (ej. gateway, switch web o dominio)")
    console.print("[2] Auditar lista de servicios criticos predefinidos (Google, Cloudflare, GitHub, Microsoft)")
    console.print("[0] Salir")

    opt = console.input("\n[bold yellow]Seleccione una opcion [0-2]: [/bold yellow]").strip()

    if opt == "1":
        host = console.input("Ingrese el nombre de dominio o IP (ej. portal.empresa.com): ").strip()
        puerto_str = console.input("Puerto [443]: ").strip()
        puerto = int(puerto_str) if puerto_str else 443
        if host:
            mostrar_reporte_tls([host])
    elif opt == "2":
        hosts_demo = ["cloudflare.com", "google.com", "github.com", "microsoft.com"]
        mostrar_reporte_tls(hosts_demo)
    else:
        console.print("Saliendo.")

if __name__ == "__main__":
    main()
