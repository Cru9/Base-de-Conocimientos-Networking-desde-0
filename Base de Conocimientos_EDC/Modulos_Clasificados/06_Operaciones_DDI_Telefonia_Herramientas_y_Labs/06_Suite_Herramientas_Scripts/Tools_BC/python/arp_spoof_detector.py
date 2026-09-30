#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Detector de Envenenamiento ARP (ARP Spoofing / MITM Detector)
Network Engineering & Cybersecurity Master Compendium - BC
Modulo: Ciberseguridad_OSI (Seguridad de Capa 2) / Troubleshooting
"""

import sys
import time
import subprocess
import re
import warnings
warnings.filterwarnings("ignore")

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

try:
    from scapy.all import sniff, ARP, Ether
except ImportError:
    console.print("[bold red][ERROR][/bold red] Scapy es necesario para esta herramienta. Ejecute 'pip install scapy'.")
    sys.exit(1)

def obtener_gateway_y_mac():
    """Obtiene la IP y MAC del Default Gateway en Windows."""
    gw_ip = None
    gw_mac = None

    # Obtener IP del gateway
    try:
        salida_route = subprocess.check_output("route print 0.0.0.0", shell=True).decode('utf-8', errors='ignore')
        match = re.search(r"0\.0\.0\.0\s+0\.0\.0\.0\s+([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)", salida_route)
        if match:
            gw_ip = match.group(1)
    except Exception:
        pass

    # Obtener MAC del gateway desde la tabla ARP
    if gw_ip:
        try:
            salida_arp = subprocess.check_output(f"arp -a {gw_ip}", shell=True).decode('utf-8', errors='ignore')
            match_mac = re.search(r"([0-9a-fA-F]{2}[:-][0-9a-fA-F]{2}[:-][0-9a-fA-F]{2}[:-][0-9a-fA-F]{2}[:-][0-9a-fA-F]{2}[:-][0-9a-fA-F]{2})", salida_arp)
            if match_mac:
                gw_mac = match_mac.group(1).replace("-", ":").lower()
        except Exception:
            pass

    return gw_ip, gw_mac

class DetectorARPSpoof:
    def __init__(self, gw_ip, gw_mac):
        self.gw_ip = gw_ip
        self.gw_mac = gw_mac.lower() if gw_mac else None
        self.ip_mac_table = {}
        if self.gw_ip and self.gw_mac:
            self.ip_mac_table[self.gw_ip] = self.gw_mac
        self.alertas = 0

    def procesar_paquete(self, pkt):
        if ARP in pkt and pkt[ARP].op in [1, 2]: # 1=who-has, 2=is-at
            ip_origen = pkt[ARP].psrc
            mac_origen = pkt[ARP].hwsrc.lower()

            # Caso 1: Ataque al Gateway predeterminado (Escenario MITM clasico)
            if self.gw_ip and ip_origen == self.gw_ip:
                if self.gw_mac and mac_origen != self.gw_mac:
                    self.alertas += 1
                    console.print(Panel(
                        f"[bold red]¡ATAQUE MITM / ARP SPOOFING DETECTADO EN TIEMPO REAL![/bold red]\n"
                        f"[white]Direccion IP Suplantada:[/white] {self.gw_ip} (Default Gateway)\n"
                        f"[green]MAC Legítima Registrada:[/green]  {self.gw_mac}\n"
                        f"[bold red]MAC Falsa del Atacante:[/bold red]   {mac_origen}\n"
                        f"[yellow]Accion preventiva:[/yellow] Activar Dynamic ARP Inspection (DAI) y DHCP Snooping en switches.",
                        title="[bold red]ALERTA CRITICA DE CAPA 2[/bold red]",
                        border_style="red"
                    ))
                    return

            # Caso 2: Conflicto o cambio repentino de MAC para otra IP
            if ip_origen in self.ip_mac_table:
                if self.ip_mac_table[ip_origen] != mac_origen:
                    self.alertas += 1
                    console.print(f"[bold yellow][CAMBIO ARP SOSPECHOSO][/bold yellow] IP {ip_origen} cambio de {self.ip_mac_table[ip_origen]} a {mac_origen}")
                    self.ip_mac_table[ip_origen] = mac_origen
            else:
                self.ip_mac_table[ip_origen] = mac_origen
                console.print(f"[gray][ARP Visto] IP {ip_origen} asociada a {mac_origen}[/gray]")

def simular_ataque_prueba(detector: DetectorARPSpoof):
    """Simula paquetes ARP para verificar que el motor de deteccion reacciona de inmediato."""
    console.print("\n[bold yellow][*] Generando paquete ARP sintetico de prueba simulando suplantacion...[/bold yellow]")
    pkt_falso = Ether()/ARP(op=2, psrc=detector.gw_ip or "192.168.1.1", hwsrc="aa:bb:cc:dd:ee:ff")
    detector.procesar_paquete(pkt_falso)

def main():
    console.print(Panel.fit(
        "[bold cyan]BC CYBERSECURITY - DETECTOR EN TIEMPO REAL DE ARP SPOOFING (MITM)[/bold cyan]\n"
        "[white]Inspeccion defensiva de Capa 2 (Modelo OSI) y Dynamic ARP Inspection[/white]",
        border_style="cyan"
    ))

    gw_ip, gw_mac = obtener_gateway_y_mac()
    console.print(f"[*] Default Gateway detectado: [bold green]{gw_ip}[/bold green]")
    console.print(f"[*] MAC del Gateway detectada:  [bold green]{gw_mac or 'No registrada en cache (se aprendera dinamicamente)'}[/bold green]\n")

    detector = DetectorARPSpoof(gw_ip, gw_mac)

    console.print("[1] Iniciar escucha pasiva de paquetes ARP en vivo en la interfaz de red")
    console.print("[2] Ejecutar prueba de simulacion inmediata (Test de deteccion)")
    console.print("[0] Salir")

    opt = console.input("\n[bold yellow]Seleccione una opcion [0-2]: [/bold yellow]").strip()

    if opt == "1":
        console.print("\n[bold cyan][*] Monitoreando trafico ARP... Presione [Ctrl+C] para detener.[/bold cyan]")
        try:
            sniff(filter="arp", store=0, prn=detector.procesar_paquete)
        except KeyboardInterrupt:
            console.print(f"\n[green]Monitoreo finalizado. Total de incidentes registrados: {detector.alertas}[/green]")
        except Exception as e:
            console.print(f"[bold red][ERROR][/bold red] {e}")
    elif opt == "2":
        if not detector.gw_mac:
            detector.gw_mac = "00:11:22:33:44:55"
            detector.gw_ip = "192.168.1.1"
        simular_ataque_prueba(detector)
    else:
        console.print("Saliendo.")

if __name__ == "__main__":
    main()
