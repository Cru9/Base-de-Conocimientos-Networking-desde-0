#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analizador Forense Automatizado de Capturas PCAP / PCAPNG
Network Engineering & Cybersecurity Master Compendium - BC
Modulo: Wireshark_Analysis / Troubleshooting / Ciberseguridad_OSI
"""

import os
import sys
from collections import Counter
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

try:
    from scapy.all import rdpcap, wrpcap, Ether, IP, TCP, UDP, ICMP, DNS, DNSQR, Raw
except ImportError:
    console.print("[bold red][ERROR][/bold red] La libreria Scapy no esta instalada. Ejecute 'pip install scapy'.")
    sys.exit(1)

def analizar_pcap(ruta_pcap: str):
    if not os.path.exists(ruta_pcap):
        console.print(f"[bold red][ERROR][/bold red] No se encontro el archivo: {ruta_pcap}")
        return

    console.print(f"\n[bold cyan][*] Cargando y procesando paquetes de '{os.path.basename(ruta_pcap)}'...[/bold cyan]")
    try:
        paquetes = rdpcap(ruta_pcap)
    except Exception as e:
        console.print(f"[bold red][ERROR AL LEER PCAP][/bold red] {e}")
        return

    total_paquetes = len(paquetes)
    if total_paquetes == 0:
        console.print("[yellow]La captura esta vacia.[/yellow]")
        return

    protocolos = Counter()
    ips_origen = Counter()
    ips_destino = Counter()
    conversaciones = Counter()
    consultas_dns = Counter()

    # Metricas TCP
    tcp_syn_count = 0
    tcp_rst_count = 0
    tcp_fin_count = 0
    tcp_retrans_count = 0
    seen_tcp_seqs = {}  # (src_ip, dst_ip, src_port, dst_port) -> set(seq)

    for pkt in paquetes:
        if IP in pkt:
            src = pkt[IP].src
            dst = pkt[IP].dst
            ips_origen[src] += 1
            ips_destino[dst] += 1
            conversaciones[tuple(sorted([src, dst]))] += 1

            if TCP in pkt:
                protocolos["TCP"] += 1
                flags = pkt[TCP].flags
                flujo = (src, dst, pkt[TCP].sport, pkt[TCP].dport)
                seq = pkt[TCP].seq
                payload_len = len(pkt[TCP].payload)

                # Deteccion de flags
                if flags & 0x02:  # SYN
                    tcp_syn_count += 1
                if flags & 0x04:  # RST
                    tcp_rst_count += 1
                if flags & 0x01:  # FIN
                    tcp_fin_count += 1

                # Deteccion de retransmision básica
                if payload_len > 0:
                    if flujo not in seen_tcp_seqs:
                        seen_tcp_seqs[flujo] = set()
                    if seq in seen_tcp_seqs[flujo]:
                        tcp_retrans_count += 1
                    else:
                        seen_tcp_seqs[flujo].add(seq)

            elif UDP in pkt:
                protocolos["UDP"] += 1
                if DNS in pkt and pkt.haslayer(DNSQR):
                    try:
                        qname = pkt[DNSQR].qname.decode('utf-8', errors='ignore')
                        consultas_dns[qname] += 1
                    except Exception:
                        pass
            elif ICMP in pkt:
                protocolos["ICMP"] += 1
            else:
                protocolos[f"IP_Proto_{pkt[IP].proto}"] += 1
        elif Ether in pkt:
            protocolos[f"EtherType_{hex(pkt[Ether].type)}"] += 1

    # Renderizar Resumen en Panel
    resumen_txt = (
        f"[bold white]Total de Paquetes:[/bold white] {total_paquetes}\n"
        f"[bold white]Paquetes TCP SYN:[/bold white] {tcp_syn_count}\n"
        f"[bold red]Conexiones Reseteadas (TCP RST):[/bold red] {tcp_rst_count}\n"
        f"[bold yellow]Retransmisiones TCP Detectadas:[/bold yellow] {tcp_retrans_count}\n"
        f"[bold cyan]Consultas DNS Unicas:[/bold cyan] {len(consultas_dns)}"
    )
    console.print(Panel(resumen_txt, title="Resumen Ejecutivo de Captura", border_style="cyan"))

    # Tabla de Protocolos
    t_proto = Table(title="Distribucion de Protocolos L4/L3", header_style="bold green")
    t_proto.add_column("Protocolo", style="cyan")
    t_proto.add_column("Paquetes", justify="right")
    t_proto.add_column("Porcentaje", justify="right")
    for proto, cant in protocolos.most_common():
        pct = (cant / total_paquetes) * 100
        t_proto.add_row(proto, str(cant), f"{pct:.1f}%")
    console.print(t_proto)

    # Tabla de Top Talkers
    t_top = Table(title="Top 5 Direcciones IP Mas Activas (Origen)", header_style="bold yellow")
    t_top.add_column("Direccion IP", style="bold white")
    t_top.add_column("Paquetes Enviados", justify="right", style="green")
    for ip, cant in ips_origen.most_common(5):
        t_top.add_row(ip, str(cant))
    console.print(t_top)

    # Tabla de Consultas DNS
    if consultas_dns:
        t_dns = Table(title="Top Consultas DNS Observadas", header_style="bold magenta")
        t_dns.add_column("Dominio Consultado", style="white")
        t_dns.add_column("Peticiones", justify="right", style="cyan")
        for dom, cant in consultas_dns.most_common(5):
            t_dns.add_row(dom, str(cant))
        console.print(t_dns)

    # Evaluacion de Salud de Red
    if tcp_retrans_count > (total_paquetes * 0.05):
        console.print("[bold red][ALERTA DE RENDIMIENTO][/bold red] Alta tasa de retransmisiones TCP (>5%). Posible saturacion de enlace o perdida de paquetes.")
    else:
        console.print("[bold green][SALUD TCP][/bold green] Tasa de retransmisiones dentro de parametros normales (<5%).")

def generar_pcap_demo():
    """Genera un archivo PCAP sintetico de prueba con trafico mixto y anomalias."""
    ruta_demo = os.path.join(os.path.dirname(__file__), "captura_demo.pcap")
    console.print(f"[bold cyan][*] Sintetizando trafico con Scapy en '{ruta_demo}'...[/bold cyan]")

    pkts = []
    # 1. Trafico DNS
    p_dns = Ether()/IP(src="192.168.1.50", dst="8.8.8.8")/UDP(sport=53421, dport=53)/DNS(rd=1, qd=DNSQR(qname="portal.empresa.local"))
    pkts.append(p_dns)

    # 2. Handshake TCP Normal
    syn = Ether()/IP(src="192.168.1.50", dst="10.0.0.10")/TCP(sport=49152, dport=443, flags="S", seq=1000)
    syn_ack = Ether()/IP(src="10.0.0.10", dst="192.168.1.50")/TCP(sport=443, dport=49152, flags="SA", seq=5000, ack=1001)
    ack = Ether()/IP(src="192.168.1.50", dst="10.0.0.10")/TCP(sport=49152, dport=443, flags="A", seq=1001, ack=5001)
    pkts.extend([syn, syn_ack, ack])

    # 3. Datos HTTP y una Retransmision
    data1 = Ether()/IP(src="192.168.1.50", dst="10.0.0.10")/TCP(sport=49152, dport=443, flags="PA", seq=1001, ack=5001)/Raw(load="GET /login HTTP/1.1\r\n")
    data1_retrans = data1.copy() # Retransmision
    pkts.extend([data1, data1_retrans])

    # 4. TCP Reset (RST)
    rst = Ether()/IP(src="10.0.0.10", dst="192.168.1.50")/TCP(sport=443, dport=49152, flags="R", seq=5001)
    pkts.append(rst)

    # 5. ICMP Echo Ping
    ping = Ether()/IP(src="192.168.1.50", dst="1.1.1.1")/ICMP()
    pkts.append(ping)

    wrpcap(ruta_demo, pkts)
    console.print("[bold green][OK] Archivo demo generado con exito.[/bold green]")
    return ruta_demo

def main():
    console.print(Panel.fit(
        "[bold cyan]BC NETWORK - ANALIZADOR FORENSE DE CAPTURAS PCAP (SCAPY)[/bold cyan]\n"
        "[white]Deteccion de Retransmisiones TCP, Resets, Top Talkers y Consultas DNS[/white]",
        border_style="cyan"
    ))

    console.print("[1] Analizar un archivo PCAP / PCAPNG existente")
    console.print("[2] Generar captura sintetica de prueba (Demo) y analizarla")
    console.print("[0] Salir")

    opt = console.input("\n[bold yellow]Seleccione una opcion [0-2]: [/bold yellow]").strip()
    if opt == "1":
        ruta = console.input("Ingrese la ruta absoluta o relativa al archivo .pcap: ").strip('"').strip()
        analizar_pcap(ruta)
    elif opt == "2":
        demo_file = generar_pcap_demo()
        analizar_pcap(demo_file)
    else:
        console.print("Saliendo.")

if __name__ == "__main__":
    main()
