"""
CLI Maestro interactivo de PyEDC - Enterprise Data & Connectivity Suite.
"""

import sys
import argparse
from typing import List

# Configurar codificación UTF-8 en Windows para compatibilidad de emojis y caracteres especiales
if sys.platform.startswith("win"):
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")
        if hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm

console = Console()


from pyedc import __version__
from pyedc.config import SUPPORTED_VENDORS, VENDOR_DISPLAY_NAMES

# Modulos
from pyedc.modules.calculator.subnetting import calculate_subnet_info, calculate_vlsm
from pyedc.modules.calculator.mtu_mss import calculate_mtu_mss, ENCAPSULATION_OVERHEADS
from pyedc.modules.calculator.optics import calculate_optical_budget, OPTICAL_TRANSCEIVERS, FIBER_STANDARDS
from pyedc.modules.calculator.fabric_design import calculate_spine_leaf

from pyedc.modules.automator.transpiler import translate_command, find_equivalent_task, get_supported_vendors
from pyedc.modules.automator.generator import generate_device_config
from pyedc.modules.automator.matrix_parser import parse_iana_ports

from pyedc.modules.examiner.parser import load_all_question_banks
from pyedc.modules.examiner.engine import ExamSession, ExamMode

from pyedc.modules.copilot.indexer import KnowledgeIndexer
from pyedc.modules.copilot.retriever import KnowledgeRetriever
from pyedc.modules.copilot.chat import CopilotAssistant

from pyedc.modules.glossary.glossary_engine import GlossaryEngine, GlossaryTerm
from pyedc.modules.troubleshooter.troubleshooter import TroubleshooterEngine, DiagnosticCase
from pyedc.modules.standards.rfc_catalog import RFCCatalog, RFCItem
from pyedc.modules.labs.lab_catalog import LabCatalog, LabBlock

console = Console()


def show_banner():
    """Muestra el banner de bienvenida con diseño premium."""
    banner_text = (
        "[bold cyan]🏛️ PyEDC - Enterprise Data & Connectivity Suite[/bold cyan]\n"
        f"[dim]Versión {__version__} | Framework Modular de Automatización, Cálculo, Certificación y RAG[/dim]\n"
        "[dim]Alineado con Cisco CCNA/CCNP, Huawei HCIA/HCIP, CompTIA, Fortinet y Estándares IETF/IEEE[/dim]"
    )
    console.print(Panel(banner_text, border_style="cyan", padding=(0, 2)))


# ============================================================================
# CONTROLADORES DEL MÓDULO CALCULADORA
# ============================================================================

def handle_calc_subnet(cidr: str) -> bool:
    try:
        info = calculate_subnet_info(cidr.strip())
    except Exception as e:
        console.print(Panel(
            f"[bold red]❌ Formato o dirección de red inválida:[/bold red] {e}\n\n"
            f"[yellow]Ejemplos válidos:[/yellow] [green]192.168.10.0/24[/green], [green]10.0.0.0/8[/green], [green]172.16.50.0/26[/green], [green]11.1.35.0/24[/green]\n"
            f"[dim]Nota: Asegúrate de completar los 4 octetos antes de la barra '/' (evita puntos sueltos como './/' o '..').[/dim]",
            title="⚠️ Error de Entrada",
            border_style="red"
        ))
        return False

    table = Table(title=f"📊 Análisis de Red: {info['cidr']}", border_style="cyan")
    table.add_column("Propiedad Técnica", style="bold white", width=25)
    table.add_column("Valor Calculado", style="cyan")

    table.add_row("Dirección de Red", info["network"])
    table.add_row("Prefijo / Longitud", f"/{info['prefix']}")
    table.add_row("Máscara Decimal", info["netmask"])
    table.add_row("Máscara Wildcard", info["wildcard"])
    table.add_row("Máscara Binaria", info["binary_mask"])
    table.add_row("Primer Host Válido", info["first_host"])
    table.add_row("Último Host Válido", info["last_host"])
    table.add_row("Dirección de Broadcast", info["broadcast"])
    table.add_row("Total de Direcciones", str(info["total_hosts"]))
    table.add_row("Capacidad Hosts Usables", f"[bold green]{info['usable_hosts']}[/bold green]")
    table.add_row("Clasificación de Alcance", info["tipo"])

    console.print(table)
    return True


def handle_calc_vlsm(parent_network: str, hosts_str: str) -> bool:
    # hosts_str puede ser "Ventas:50,Sistemas:20,DMZ:10,WAN:2" o "50,20,10,2"
    try:
        requirements = []
        tokens = [t.strip() for t in hosts_str.split(",") if t.strip()]
        if not tokens:
            raise ValueError("Debes ingresar al menos un requerimiento de hosts (ej: 50 o Ventas:50).")

        for idx, token in enumerate(tokens, start=1):
            if ":" in token:
                name, count_str = token.split(":", 1)
                name = name.strip() or f"Subred_{idx}"
                try:
                    count = int(count_str.strip())
                except ValueError:
                    raise ValueError(f"La cantidad de hosts para '{name}' debe ser un número entero (recibido: '{count_str}').")
            else:
                name = f"Subred_{idx}"
                try:
                    count = int(token.strip())
                except ValueError:
                    raise ValueError(f"La cantidad de hosts debe ser un número entero (recibido: '{token}').")

            if count <= 0:
                raise ValueError(f"El número de hosts para '{name}' debe ser mayor a 0 (recibido: {count}).")
            requirements.append((name, count))

        res = calculate_vlsm(parent_network.strip(), requirements)
    except Exception as e:
        console.print(Panel(
            f"[bold red]❌ Error en cálculo VLSM:[/bold red] {e}\n\n"
            f"[yellow]Sugerencia:[/yellow] Verifica que la red raíz tenga formato CIDR válido (ej: [green]192.168.1.0/24[/green]) y que los requerimientos sean números enteros separados por comas (ej: [green]50,20,10,2[/green] o [green]Ventas:50,DMZ:10[/green]).",
            title="⚠️ Error de Entrada",
            border_style="red"
        ))
        return False

    console.print(f"\n[bold green]✅ Asignación VLSM para Red Raíz: {res['parent_network']}[/bold green]")
    console.print(f"[dim]Capacidad total: {res['parent_total_addresses']} IPs | Hosts pedidos: {res['total_requested_hosts']} | Eficiencia: {res['efficiency_percent']}%[/dim]\n")

    table = Table(title="Detalle de Asignación por Subred", border_style="cyan")
    table.add_column("Subred / Nombre", style="bold white")
    table.add_column("Hosts Pedidos", justify="center")
    table.add_column("Prefijo CIDR", style="cyan")
    table.add_column("Rango Útil (Primer - Último)", style="green")
    table.add_column("Broadcast", style="yellow")
    table.add_column("Máscara", style="dim")
    table.add_column("Desperdicio", justify="center", style="dim")

    for sub in res["subnets"]:
        table.add_row(
            sub["name"],
            str(sub["requested_hosts"]),
            sub["cidr"],
            f"{sub['first_host']} - {sub['last_host']}",
            sub["broadcast"],
            sub["netmask"],
            str(sub["waste"]),
        )

    console.print(table)
    console.print(f"[bold cyan]Direcciones libres restantes en el bloque:[/bold cyan] {res['free_addresses_remaining']}")
    return True


def handle_calc_mss(base_mtu: int, encapsulations: List[str], is_ipv6: bool = False) -> bool:
    try:
        res = calculate_mtu_mss(base_mtu=base_mtu, is_ipv6=is_ipv6, active_encapsulations=encapsulations)
    except Exception as e:
        console.print(Panel(f"[bold red]❌ Error en cálculo de MTU/MSS:[/bold red] {e}", title="⚠️ Error", border_style="red"))
        return False

    table = Table(title=f"🧮 Cálculo de MTU / TCP MSS (Base: {base_mtu} Bytes)", border_style="cyan")
    table.add_column("Capa / Protocolo", style="white")
    table.add_column("Overhead", justify="right", style="cyan")

    table.add_row(f"Encabezado Red {res['ip_version']}", f"{res['ip_header_bytes']} B")
    table.add_row("Encabezado Capa 4 (TCP)", f"{res['tcp_header_bytes']} B")

    for item in res["breakdown"]:
        table.add_row(f"{item['nombre']} ({item['capa']})", f"+{item['overhead_bytes']} B")

    table.add_row("[bold]Total Overhead de Encapsulamiento[/bold]", f"[bold yellow]{res['total_tunnel_overhead_bytes']} B[/bold yellow]")
    table.add_row("[bold]MTU IP Efectivo[/bold]", f"[bold]{res['effective_ip_mtu']} B[/bold]")
    table.add_row("[bold green]MSS TCP Óptimo Recomendado[/bold green]", f"[bold green]{res['recommended_tcp_mss']} Bytes[/bold green]")

    console.print(table)

    if res["warning"]:
        console.print(f"\n[bold red]⚠️ {res['warning']}[/bold red]")

    console.print("\n[bold cyan]🔧 Comandos de Remediación CLI:[/bold cyan]")
    for vendor, cmd in res["cli_remediation"].items():
        console.print(Panel(cmd, title=f"Fabricante: {vendor.upper()}", border_style="dim"))
    return True


def handle_calc_optics(distance_km: float, fiber: str, transceiver: str) -> bool:
    try:
        res = calculate_optical_budget(distance_km=distance_km, fiber_type=fiber, transceiver_model=transceiver)
    except Exception as e:
        console.print(Panel(f"[bold red]❌ Error en presupuesto óptico:[/bold red] {e}", title="⚠️ Error", border_style="red"))
        return False

    status_color = "green" if "EXCELENTE" in res["status"] else ("yellow" if "VIABLE" in res["status"] else "red")

    table = Table(title=f"💡 Presupuesto Óptico ({res['transceiver']} - {res['distance_km']} km)", border_style="cyan")
    table.add_column("Parámetro Óptico", style="white")
    table.add_column("Valor Calculado", style="cyan")

    table.add_row("Norma de Fibra", res["fiber_type"])
    table.add_row("Atenuación del Cable", f"{res['cable_loss_db']} dB")
    table.add_row("Pérdida en Conectores", f"{res['connectors_loss_db']} dB")
    table.add_row("Pérdida en Empalmes", f"{res['splices_loss_db']} dB")
    table.add_row("Margen de Seguridad (Envejecimiento)", f"{res['safety_margin_db']} dB")
    table.add_row("[bold]Pérdida Total del Enlace[/bold]", f"[bold yellow]{res['total_link_attenuation_db']} dB[/bold yellow]")
    table.add_row("Presupuesto Disponible del Transceptor", f"{res['power_budget_db']} dB")
    table.add_row("[bold]Margen de Operación Final[/bold]", f"[bold {status_color}]{res['operating_margin_db']} dB[/bold {status_color}]")
    table.add_row("[bold]Diagnóstico[/bold]", f"[bold {status_color}]{res['status']}[/bold {status_color}]")

    console.print(table)
    console.print(f"\n[dim]{res['recommendation']}[/dim]")
    return True


def handle_calc_fabric(leafs: int, downlinks: int, uplinks: int) -> bool:
    try:
        res = calculate_spine_leaf(num_leafs=leafs, downlinks_per_leaf=downlinks, uplinks_per_leaf=uplinks)
    except Exception as e:
        console.print(Panel(f"[bold red]❌ Error en dimensionamiento Fabric:[/bold red] {e}", title="⚠️ Error", border_style="red"))
        return False

    table = Table(title=f"🏢 Dimensionamiento Spine-Leaf Clos (Leafs: {leafs})", border_style="cyan")
    table.add_column("Métrica Arquitectónica", style="white")
    table.add_column("Valor", style="cyan")

    table.add_row("Spines Requeridos (Full-Mesh)", str(res["required_spines"]))
    table.add_row("Total de Puertos para Servidores", str(res["total_server_ports"]))
    table.add_row("Throughput Agregado Servidores", f"{res['total_server_throughput_tbps']} Tbps")
    table.add_row("Ancho de Banda Biseccional Fabric", f"{res['bisectional_bandwidth_tbps']} Tbps")
    table.add_row("[bold]Relación de Sobresuscripción[/bold]", f"[bold yellow]{res['health']}[/bold yellow]")
    table.add_row("Uso de Puertos en Spine", res["spine_port_usage"])
    table.add_row("Capacidad de Crecimiento en Leafs", f"+{res['fabric_expandability_leafs']} switches adicionales")

    console.print(table)
    console.print(f"\n[dim]{res['assessment']}[/dim]")
    return True


# ============================================================================
# CONTROLADORES DEL MÓDULO AUTOMATIZACIÓN
# ============================================================================

def handle_transpile(command: str, from_vendor: str, to_vendor: str) -> bool:
    try:
        res = translate_command(command, from_vendor, to_vendor)
    except Exception as e:
        console.print(Panel(f"[bold red]❌ Error de transpilación:[/bold red] {e}", title="⚠️ Error", border_style="red"))
        return False

    console.print(Panel(
        f"[bold white]Comando Origen ({res['from_vendor']}):[/bold white]\n"
        f"[yellow]{res['original']}[/yellow]\n\n"
        f"[bold white]Equivalente Traducido ({res['to_vendor']}):[/bold white]\n"
        f"[bold green]{res['translated']}[/bold green]\n\n"
        f"[dim]Tarea: {res['task']} | Confianza: {int(res['confidence'] * 100)}%[/dim]",
        title="⚙️ Transpilador Multi-Vendor EDC",
        border_style="cyan"
    ))
    return True


def handle_matrix_search(query: str) -> bool:
    try:
        matches = find_equivalent_task(query)
    except Exception as e:
        console.print(Panel(f"[bold red]❌ Error en búsqueda:[/bold red] {e}", title="⚠️ Error", border_style="red"))
        return False

    if not matches:
        console.print(f"[yellow]No se encontraron coincidencias para:[/yellow] '{query}'")
        return True

    table = Table(title=f"📊 Matriz Multi-Vendor: Coincidencias para '{query}'", border_style="cyan")
    table.add_column("Tarea Operativa", style="bold white", width=22)
    table.add_column("Cisco IOS-XE", style="cyan")
    table.add_column("Huawei VRP", style="green")
    table.add_column("Aruba CX", style="magenta")
    table.add_column("HP ProCurve", style="yellow")
    table.add_column("Comware", style="blue")
    table.add_column("TP-Link", style="white")

    for m in matches:
        table.add_row(
            m["task"],
            m["cisco"],
            m["huawei"],
            m["aruba"],
            m["hp_procurve"],
            m["comware"],
            m["tplink"],
        )

    console.print(table)
    return True


def handle_generate_config(task_type: str, vendor: str, **kwargs) -> bool:
    try:
        cfg = generate_device_config(task_type, vendor, kwargs)
    except Exception as e:
        console.print(Panel(f"[bold red]❌ Error generando configuración:[/bold red] {e}", title="⚠️ Error", border_style="red"))
        return False

    v_name = VENDOR_DISPLAY_NAMES.get(vendor.lower(), vendor)
    console.print(Panel(
        f"[bold green]{cfg}[/bold green]",
        title=f"📄 Configuración Generada - {v_name} ({task_type.upper()})",
        border_style="cyan"
    ))
    return True


def handle_iana_ports(query: str) -> bool:
    try:
        ports = parse_iana_ports()
        q = query.strip().lower()
        matches = [p for p in ports if q in p["port"].lower() or q in p["service"].lower() or q in p["threat"].lower()]
    except Exception as e:
        console.print(Panel(f"[bold red]❌ Error consultando catálogo IANA:[/bold red] {e}", title="⚠️ Error", border_style="red"))
        return False

    if not matches:
        console.print(f"[yellow]No se encontraron registros en el catálogo IANA para:[/yellow] '{query}'")
        return True

    table = Table(title=f"🛡️ Catálogo IANA y Mitigación EDC: '{query}'", border_style="red")
    table.add_column("Puerto", style="bold white", width=10)
    table.add_column("Servicio", style="cyan", width=12)
    table.add_column("Riesgo", width=12)
    table.add_column("Vector de Amenaza", style="yellow", width=30)
    table.add_column("Medida de Mitigación Oficial", style="green")

    for p in matches:
        table.add_row(
            f"{p['port']} ({p['protocol']})",
            p["service"],
            p["risk_level"],
            p["threat"],
            p["mitigation"],
        )

    console.print(table)
    return True


# ============================================================================
# CONTROLADORES DE EXÁMENES Y COPILOT
# ============================================================================

def handle_exam(mode_str: str = "practice", count: int = 10) -> bool:
    try:
        all_qs = load_all_question_banks()
        if not all_qs:
            console.print("[red]❌ No se encontraron preguntas disponibles en el repositorio.[/red]")
            return False

        mode = ExamMode.PRACTICE if mode_str.lower() == "practice" else ExamMode.SIMULATION
        session = ExamSession(all_qs, mode=mode, count=count, shuffle=True)
        session.run_interactive()
        return True
    except Exception as e:
        console.print(Panel(f"[bold red]❌ Error en simulador de exámenes:[/bold red] {e}", title="⚠️ Error", border_style="red"))
        return False


def handle_copilot_ask(question: str) -> bool:
    try:
        assistant = CopilotAssistant()
        assistant.query(question)
        return True
    except Exception as e:
        console.print(Panel(f"[bold red]❌ Error en consulta Copilot:[/bold red] {e}", title="⚠️ Error", border_style="red"))
        return False


def handle_copilot_chat() -> bool:
    try:
        assistant = CopilotAssistant()
        assistant.interactive_chat()
        return True
    except Exception as e:
        console.print(Panel(f"[bold red]❌ Error en sesión Copilot:[/bold red] {e}", title="⚠️ Error", border_style="red"))
        return False


# ============================================================================
# CONTROLADORES DE DICCIONARIO, TROUBLESHOOTING, RFCS Y LABS
# ============================================================================

def handle_glossary_search(query: str) -> bool:
    try:
        engine = GlossaryEngine()
        results = engine.search(query)
        if not results:
            console.print(f"[yellow]No se encontraron términos para:[/yellow] '{query}'")
            return True

        console.print(f"\n[bold green]📖 Encontrados {len(results)} términos en el Diccionario EDC:[/bold green]\n")
        for t in results[:5]:
            std_str = f" | [bold cyan]{', '.join(t.standards)}[/bold cyan]" if t.standards else ""
            console.print(Panel(
                f"[bold white]{t.definition}[/bold white]\n\n"
                f"[dim]Dominio/Capa: {t.domain_layer}{std_str}[/dim]",
                title=f"📌 {t.term}",
                border_style="cyan"
            ))
        return True
    except Exception as e:
        console.print(Panel(f"[bold red]❌ Error en consulta de diccionario:[/bold red] {e}", title="⚠️ Error", border_style="red"))
        return False


def handle_glossary_letter(letter: str) -> bool:
    try:
        engine = GlossaryEngine()
        results = engine.get_by_letter(letter)
        if not results:
            console.print(f"[yellow]No hay términos registrados bajo la letra '{letter.upper()}'.[/yellow]")
            return True

        table = Table(title=f"📖 Términos de la Letra '{letter.upper()}' ({len(results)} términos)", border_style="cyan")
        table.add_column("Término / Acrónimo", style="bold white", width=25)
        table.add_column("Dominio / Capa", style="cyan", width=30)
        table.add_column("Estándares", style="green", width=25)

        for t in results:
            table.add_row(t.term, t.domain_layer, ", ".join(t.standards) if t.standards else "-")

        console.print(table)
        return True
    except Exception as e:
        console.print(Panel(f"[bold red]❌ Error al listar letra:[/bold red] {e}", title="⚠️ Error", border_style="red"))
        return False


def handle_glossary_random() -> bool:
    try:
        engine = GlossaryEngine()
        t = engine.get_random_term()
        if not t:
            console.print("[yellow]No hay términos disponibles.[/yellow]")
            return True

        std_str = f"\n[dim]Estándares:[/dim] [bold cyan]{', '.join(t.standards)}[/bold cyan]" if t.standards else ""
        console.print(Panel(
            f"[bold white]{t.definition}[/bold white]\n\n"
            f"[dim]Dominio/Capa:[/dim] [yellow]{t.domain_layer}[/yellow]{std_str}",
            title=f"💡 Flashcard Técnica: {t.term}",
            border_style="magenta",
            padding=(1, 2)
        ))
        return True
    except Exception as e:
        console.print(Panel(f"[bold red]❌ Error en flashcard:[/bold red] {e}", title="⚠️ Error", border_style="red"))
        return False


def handle_troubleshoot_list() -> bool:
    try:
        engine = TroubleshooterEngine()
        cases = engine.get_all_cases()

        table = Table(title="🚨 Casos de Troubleshooting y Diagnóstico Guiado", border_style="red")
        table.add_column("#", style="dim", width=4)
        table.add_column("Patología / Problema de Red", style="bold white", width=42)
        table.add_column("Capa OSI", style="cyan", width=24)
        table.add_column("Estándar / RFC", style="green")

        for idx, c in enumerate(cases, start=1):
            table.add_row(str(idx), c.title, c.layer, c.related_rfc)

        console.print(table)
        return True
    except Exception as e:
        console.print(Panel(f"[bold red]❌ Error listando casos:[/bold red] {e}", title="⚠️ Error", border_style="red"))
        return False


def handle_troubleshoot_detail(case_idx: int) -> bool:
    try:
        engine = TroubleshooterEngine()
        cases = engine.get_all_cases()
        if case_idx < 1 or case_idx > len(cases):
            console.print(f"[yellow]Número de caso inválido (1 a {len(cases)}).[/yellow]")
            return False

        c = cases[case_idx - 1]

        console.print(f"\n[bold red]━━━ 🚨 DIAGNÓSTICO GUIADO: {c.title} ━━━[/bold red]")
        console.print(f"[dim]Capa: {c.layer} | Estándar: {c.related_rfc}[/dim]\n")

        # Síntomas
        symptom_table = Table(title="🔍 Síntomas Detectados", border_style="yellow")
        symptom_table.add_column("Comportamiento Anómalo", style="white")
        for s in c.symptoms:
            symptom_table.add_row(f"• {s}")
        console.print(symptom_table)

        # Causas
        causes_table = Table(title="⚠️ Causas Raíz Comunes", border_style="red")
        causes_table.add_column("Causa Posible", style="white")
        for r in c.root_causes:
            causes_table.add_row(f"• {r}")
        console.print(causes_table)

        # Filtros Wireshark
        console.print(Panel(
            f"[bold cyan]Filtro de Visualización (Display Filter):[/bold cyan]\n"
            f"[bold green]{c.wireshark_display_filter}[/bold green]\n\n"
            f"[bold cyan]Filtro de Captura (BPF Kernel):[/bold cyan]\n"
            f"[bold yellow]{c.wireshark_capture_filter}[/bold yellow]",
            title="🦈 Filtros Forenses Wireshark",
            border_style="cyan"
        ))

        # Comandos CLI
        cli_content = "[bold white]Cisco IOS / IOS-XE:[/bold white]\n" + "\n".join(f"  {cmd}" for cmd in c.cisco_commands)
        cli_content += "\n\n[bold white]Huawei VRP:[/bold white]\n" + "\n".join(f"  {cmd}" for cmd in c.huawei_commands)
        console.print(Panel(cli_content, title="💻 Comandos de Verificación CLI", border_style="dim"))

        # Remediación
        rem_content = "\n".join(f"[bold green]{idx}.[/bold green] {step}" for idx, step in enumerate(c.remediation_steps, 1))
        console.print(Panel(rem_content, title="🛠️ Plan de Remediación Paso a Paso", border_style="green"))

        return True
    except Exception as e:
        console.print(Panel(f"[bold red]❌ Error mostrando caso de troubleshooting:[/bold red] {e}", title="⚠️ Error", border_style="red"))
        return False


def handle_rfc_search(query: str) -> bool:
    try:
        catalog = RFCCatalog()
        results = catalog.search(query)
        if not results:
            console.print(f"[yellow]No se encontraron RFCs para:[/yellow] '{query}'")
            return True

        table = Table(title=f"📜 Catálogo Oficial de RFCs y Estándares: '{query}'", border_style="cyan")
        table.add_column("RFC / ID", style="bold white", width=12)
        table.add_column("Título Oficial", style="cyan", width=35)
        table.add_column("Categoría", style="yellow", width=25)
        table.add_column("Resumen y Propósito", style="dim")

        for rfc in results[:8]:
            table.add_row(rfc.rfc_id, rfc.title, rfc.category, rfc.description)

        console.print(table)
        return True
    except Exception as e:
        console.print(Panel(f"[bold red]❌ Error buscando RFCs:[/bold red] {e}", title="⚠️ Error", border_style="red"))
        return False


def handle_labs_list(query: Optional[str] = None) -> bool:
    try:
        catalog = LabCatalog()
        blocks = catalog.search_labs(query) if query else catalog.get_all_blocks()

        table = Table(title="🧪 Catálogo del Banco de 200 Laboratorios Prácticos EDC", border_style="cyan")
        table.add_column("Bloque", justify="center", style="dim", width=8)
        table.add_column("Rango Labs", justify="center", style="bold cyan", width=12)
        table.add_column("Área Temática", style="bold white", width=35)
        table.add_column("Nivel / Certificación", style="green", width=28)
        table.add_column("Emulador Recomendado", style="yellow")

        for b in blocks:
            table.add_row(
                f"Parte {b.part}",
                b.lab_range,
                b.title,
                f"{b.complexity}\n[dim]{b.certification}[/dim]",
                b.suggested_emulator
            )

        console.print(table)
        return True
    except Exception as e:
        console.print(Panel(f"[bold red]❌ Error consultando banco de labs:[/bold red] {e}", title="⚠️ Error", border_style="red"))
        return False


# ============================================================================
# MENÚ INTERACTIVO PRINCIPAL
# ============================================================================

def interactive_menu():
    """Ejecuta un menú de texto completo cuando no se pasan argumentos por línea de comandos."""
    show_banner()

    while True:
        try:
            console.print("\n[bold cyan]Selecciona el módulo que deseas utilizar:[/bold cyan]")
            console.print("  [bold green]1.[/bold green] 🧮 [bold]Calculadora & Diseñador de Red[/bold] (VLSM, MTU/MSS, Presupuesto Óptico, Spine-Leaf)")
            console.print("  [bold green]2.[/bold green] ⚙️ [bold]Automatización & Transpilador Multi-Vendor[/bold] (Cisco, Huawei, Aruba, TP-Link, IANA)")
            console.print("  [bold green]3.[/bold green] 📖 [bold]Diccionario Enciclopédico (+200 Términos A-Z)[/bold] (Definiciones, Capas, RFCs)")
            console.print("  [bold green]4.[/bold green] 🚨 [bold]Diagnóstico & Troubleshooting Guiado[/bold] (Fallas L2-L7, TCP, OSPF, BGP, Wireshark)")
            console.print("  [bold green]5.[/bold green] 📜 [bold]Catálogo Oficial de RFCs y Estándares IETF[/bold] (Búsqueda de RFCs y normas)")
            console.print("  [bold green]6.[/bold green] 🧪 [bold]Banco de 200 Laboratorios y Emulación[/bold] (EVE-NG, GNS3, CCNA a Experto)")
            console.print("  [bold green]7.[/bold green] 🎓 [bold]Simulador de Certificaciones[/bold] (CCNA, HCIA, Network+, Security+)")
            console.print("  [bold green]8.[/bold green] 🧠 [bold]Asistente Técnico & Copilot EDC[/bold] (Búsqueda semántica en toda la base)")
            console.print("  [bold green]0.[/bold green] ❌ [bold red]Salir[/bold red]")

            opt = Prompt.ask("\n[bold yellow]Ingresa una opción[/bold yellow]", choices=["0", "1", "2", "3", "4", "5", "6", "7", "8"], default="1")

            if opt == "0":
                console.print("\n[cyan]¡Hasta luego! Gracias por usar PyEDC.[/cyan]")
                break
            elif opt == "1":
                menu_calculator()
            elif opt == "2":
                menu_automator()
            elif opt == "3":
                menu_glossary()
            elif opt == "4":
                menu_troubleshooter()
            elif opt == "5":
                menu_standards()
            elif opt == "6":
                menu_labs()
            elif opt == "7":
                menu_examiner()
            elif opt == "8":
                menu_copilot()
        except (KeyboardInterrupt, EOFError):
            console.print("\n\n[yellow]Presionaste Ctrl+C. Saliendo de forma segura... ¡Hasta luego![/yellow]")
            break
        except Exception as e:
            console.print(Panel(f"[bold red]Ocurrió un error inesperado:[/bold red] {e}\n[yellow]El sistema se ha recuperado para que puedas continuar.[/yellow]", title="⚠️ Advertencia", border_style="yellow"))


def menu_calculator():
    while True:
        try:
            console.print("\n[bold cyan]━━━ 🧮 MÓDULO DE CÁLCULO Y DISEÑO DE RED ━━━[/bold cyan]")
            console.print("1. Análisis Técnico de Subred (CIDR)")
            console.print("2. Calculadora VLSM con Requerimientos por Departamento")
            console.print("3. Calculadora de MTU de Ruta y TCP MSS (Overhead IPsec/GRE/VXLAN)")
            console.print("4. Presupuesto Óptico y Atenuación de Fibra (TIA-568-D)")
            console.print("5. Dimensionamiento Spine-Leaf Clos para Datacenter")
            console.print("0. Regresar al Menú Principal")

            sub_opt = Prompt.ask("\nOpción", choices=["0", "1", "2", "3", "4", "5"])

            if sub_opt == "0":
                break

            elif sub_opt == "1":
                while True:
                    cidr = Prompt.ask("\nIngresa la red en formato CIDR (ej: 192.168.10.0/24 o 10.0.0.0/16, o '0' para regresar)", default="192.168.10.0/24").strip()
                    if cidr in ["0", "q", "cancelar", "salir", "regresar"]:
                        break
                    if handle_calc_subnet(cidr):
                        Prompt.ask("\n[dim]Presiona Enter para continuar...[/dim]")
                        break

            elif sub_opt == "2":
                while True:
                    root = Prompt.ask("\nIngresa la red raíz (ej: 192.168.1.0/24, o '0' para regresar)", default="192.168.1.0/24").strip()
                    if root in ["0", "q", "cancelar", "salir", "regresar"]:
                        break
                    reqs = Prompt.ask("Ingresa requerimientos (ej: Ventas:50,Sistemas:20,DMZ:10,WAN:2)", default="Ventas:50,Sistemas:20,DMZ:10,WAN:2").strip()
                    if reqs in ["0", "q", "cancelar", "salir", "regresar"]:
                        break
                    if handle_calc_vlsm(root, reqs):
                        Prompt.ask("\n[dim]Presiona Enter para continuar...[/dim]")
                        break

            elif sub_opt == "3":
                mtu_raw = Prompt.ask("\nMTU Base de Interfaz (o '0' para regresar)", default="1500").strip()
                if mtu_raw in ["0", "q", "regresar"]:
                    continue
                try:
                    mtu = int(mtu_raw)
                except ValueError:
                    console.print("[yellow]Valor inválido. Se utilizará 1500 por defecto.[/yellow]")
                    mtu = 1500
                encs = []
                if Confirm.ask("¿Atraviesa Túnel IPsec ESP?", default=True):
                    encs.append("ipsec_esp")
                if Confirm.ask("¿Atraviesa Túnel GRE?", default=False):
                    encs.append("gre")
                if Confirm.ask("¿Atraviesa Túnel VXLAN?", default=False):
                    encs.append("vxlan")
                if Confirm.ask("¿Tiene Etiquetado VLAN 802.1Q?", default=True):
                    encs.append("vlan_8021q")
                handle_calc_mss(base_mtu=mtu, encapsulations=encs)
                Prompt.ask("\n[dim]Presiona Enter para continuar...[/dim]")

            elif sub_opt == "4":
                dist_raw = Prompt.ask("\nDistancia del enlace en Kilómetros (o '0' para regresar)", default="10.0").strip()
                if dist_raw in ["0", "q", "regresar"]:
                    continue
                try:
                    dist = float(dist_raw)
                except ValueError:
                    console.print("[yellow]Distancia no numérica. Se usará 10.0 km por defecto.[/yellow]")
                    dist = 10.0
                console.print("[dim]Modelos: 10GBASE-LR, 10GBASE-SR, 10GBASE-ER, 25GBASE-LR, 100GBASE-LR4[/dim]")
                xcvr = Prompt.ask("Modelo de Transceptor", default="10GBASE-LR").strip()
                fib = Prompt.ask("Tipo de Fibra (OS2_1310, OS2_1550, OM3_850, OM4_850)", default="OS2_1310").strip()
                handle_calc_optics(dist, fib, xcvr)
                Prompt.ask("\n[dim]Presiona Enter para continuar...[/dim]")

            elif sub_opt == "5":
                try:
                    leafs = int(Prompt.ask("\nCantidad de Switches Leaf", default="4"))
                    down = int(Prompt.ask("Puertos de Acceso por Leaf (Servidores)", default="48"))
                    up = int(Prompt.ask("Puertos de Uplink por Leaf (Hacia Spines)", default="4"))
                except ValueError:
                    console.print("[yellow]Entradas no numéricas. Se usarán valores recomendados (4 Leafs, 48 Down, 4 Up).[/yellow]")
                    leafs, down, up = 4, 48, 4
                handle_calc_fabric(leafs, down, up)
                Prompt.ask("\n[dim]Presiona Enter para continuar...[/dim]")

        except (KeyboardInterrupt, EOFError):
            break
        except Exception as e:
            console.print(Panel(f"[bold red]Error en módulo de cálculo:[/bold red] {e}", title="⚠️ Advertencia", border_style="yellow"))


def menu_automator():
    while True:
        try:
            console.print("\n[bold cyan]━━━ ⚙️ MÓDULO DE AUTOMATIZACIÓN MULTI-VENDOR ━━━[/bold cyan]")
            console.print("1. Traducir Comando Directo entre 2 Fabricantes")
            console.print("2. Buscar Tarea en la Matriz Comparativa Completa")
            console.print("3. Generador de Plantilla de Configuración (VLAN, Acceso, Troncal)")
            console.print("4. Consultar Puerto IANA, Riesgo y Medida de Mitigación")
            console.print("0. Regresar al Menú Principal")

            sub_opt = Prompt.ask("\nOpción", choices=["0", "1", "2", "3", "4"])

            if sub_opt == "0":
                break

            elif sub_opt == "1":
                cmd = Prompt.ask("\nComando original (ej: switchport mode trunk, vlan 10, write memory, o '0' para regresar)", default="switchport mode trunk").strip()
                if cmd in ["0", "q", "regresar"]:
                    continue
                from_v = Prompt.ask("Fabricante origen (cisco, huawei, aruba, hp_procurve, comware, tplink)", default="cisco").strip()
                to_v = Prompt.ask("Fabricante destino (cisco, huawei, aruba, hp_procurve, comware, tplink)", default="huawei").strip()
                handle_transpile(cmd, from_v, to_v)
                Prompt.ask("\n[dim]Presiona Enter para continuar...[/dim]")

            elif sub_opt == "2":
                query = Prompt.ask("\nTérmino o comando a buscar (ej: trunk, lacp, rstp, vlan, route, o '0' para regresar)", default="trunk").strip()
                if query in ["0", "q", "regresar"]:
                    continue
                handle_matrix_search(query)
                Prompt.ask("\n[dim]Presiona Enter para continuar...[/dim]")

            elif sub_opt == "3":
                task = Prompt.ask("\nTipo de plantilla (vlan, access_port, trunk_port)", default="vlan").strip()
                vendor = Prompt.ask("Fabricante (cisco, huawei, aruba, hp_procurve, comware, tplink)", default="cisco").strip()
                if task == "vlan":
                    try:
                        v_id = int(Prompt.ask("ID de VLAN", default="10"))
                    except ValueError:
                        v_id = 10
                    v_name = Prompt.ask("Nombre de VLAN", default="VENTAS")
                    handle_generate_config("vlan", vendor, vlan_id=v_id, name=v_name)
                elif task == "access_port":
                    iface = Prompt.ask("Interfaz física", default="Gi0/1")
                    try:
                        v_id = int(Prompt.ask("ID de VLAN", default="10"))
                    except ValueError:
                        v_id = 10
                    handle_generate_config("access_port", vendor, interface=iface, vlan_id=v_id)
                elif task == "trunk_port":
                    iface = Prompt.ask("Interfaz física", default="Gi0/24")
                    vlans = Prompt.ask("VLANs permitidas", default="10,20,30")
                    handle_generate_config("trunk_port", vendor, interface=iface, allowed_vlans=vlans)
                Prompt.ask("\n[dim]Presiona Enter para continuar...[/dim]")

            elif sub_opt == "4":
                q = Prompt.ask("\nNúmero de puerto o servicio (ej: 22, 23, 53, 445, 179, bgp, dhcp, o '0' para regresar)", default="445").strip()
                if q in ["0", "q", "regresar"]:
                    continue
                handle_iana_ports(q)
                Prompt.ask("\n[dim]Presiona Enter para continuar...[/dim]")

        except (KeyboardInterrupt, EOFError):
            break
        except Exception as e:
            console.print(Panel(f"[bold red]Error en módulo de automatización:[/bold red] {e}", title="⚠️ Advertencia", border_style="yellow"))


def menu_glossary():
    engine = GlossaryEngine()
    letters = engine.get_available_letters()

    while True:
        try:
            console.print("\n[bold cyan]━━━ 📖 DICCIONARIO ENCICLOPÉDICO EDC (+200 TÉRMINOS) ━━━[/bold cyan]")
            console.print("1. Buscar Término o Acrónimo (ej: BGP, EVPN, DAI, AAA, Anycast, RSTP)")
            console.print(f"2. Explorar por Letra Alfabética [{', '.join(letters[:10])}...]")
            console.print("3. Flashcard Técnica Aleatoria (Término del Día)")
            console.print("0. Regresar al Menú Principal")

            sub_opt = Prompt.ask("\nOpción", choices=["0", "1", "2", "3"])

            if sub_opt == "0":
                break
            elif sub_opt == "1":
                q = Prompt.ask("\nTérmino o concepto a buscar (o '0' para regresar)", default="BGP").strip()
                if q in ["0", "q", "regresar"]:
                    continue
                handle_glossary_search(q)
                Prompt.ask("\n[dim]Presiona Enter para continuar...[/dim]")
            elif sub_opt == "2":
                let = Prompt.ask(f"\nIngresa la letra a consultar ({', '.join(letters)})", default="A").strip().upper()
                if let in ["0", "Q"]:
                    continue
                handle_glossary_letter(let)
                Prompt.ask("\n[dim]Presiona Enter para continuar...[/dim]")
            elif sub_opt == "3":
                handle_glossary_random()
                Prompt.ask("\n[dim]Presiona Enter para continuar...[/dim]")

        except (KeyboardInterrupt, EOFError):
            break
        except Exception as e:
            console.print(Panel(f"[bold red]Error en módulo de diccionario:[/bold red] {e}", title="⚠️ Advertencia", border_style="yellow"))


def menu_troubleshooter():
    engine = TroubleshooterEngine()
    cases = engine.get_all_cases()

    while True:
        try:
            console.print("\n[bold cyan]━━━ 🚨 DIAGNÓSTICO & TROUBLESHOOTING GUIADO ━━━[/bold cyan]")
            console.print("1. Listar Todas las Patologías de Red Documentadas")
            console.print("2. Abrir Guía de Diagnóstico Paso a Paso por Número de Caso")
            console.print("3. Buscar Caso por Síntoma o Protocolo (ej: TCP, OSPF, BGP, IPsec, VoIP)")
            console.print("0. Regresar al Menú Principal")

            sub_opt = Prompt.ask("\nOpción", choices=["0", "1", "2", "3"])

            if sub_opt == "0":
                break
            elif sub_opt == "1":
                handle_troubleshoot_list()
                Prompt.ask("\n[dim]Presiona Enter para continuar...[/dim]")
            elif sub_opt == "2":
                handle_troubleshoot_list()
                idx_raw = Prompt.ask(f"\nSelecciona el número de caso (1 a {len(cases)}, o '0' para regresar)", default="1").strip()
                if idx_raw in ["0", "q", "regresar"]:
                    continue
                try:
                    c_idx = int(idx_raw)
                    handle_troubleshoot_detail(c_idx)
                except ValueError:
                    console.print("[yellow]Número de caso inválido.[/yellow]")
                Prompt.ask("\n[dim]Presiona Enter para continuar...[/dim]")
            elif sub_opt == "3":
                q = Prompt.ask("\nIngresa síntoma o protocolo (ej: MTU, loop, flapping, jitter, o '0' para regresar)", default="TCP").strip()
                if q in ["0", "q", "regresar"]:
                    continue
                matches = engine.search_cases(q)
                if not matches:
                    console.print(f"[yellow]No se encontraron casos de diagnóstico para '{q}'.[/yellow]")
                else:
                    for m in matches:
                        orig_idx = next(i for i, c in enumerate(cases, 1) if c.id == m.id)
                        handle_troubleshoot_detail(orig_idx)
                Prompt.ask("\n[dim]Presiona Enter para continuar...[/dim]")

        except (KeyboardInterrupt, EOFError):
            break
        except Exception as e:
            console.print(Panel(f"[bold red]Error en módulo de troubleshooting:[/bold red] {e}", title="⚠️ Advertencia", border_style="yellow"))


def menu_standards():
    catalog = RFCCatalog()

    while True:
        try:
            console.print("\n[bold cyan]━━━ 📜 CATÁLOGO OFICIAL DE RFCS Y ESTÁNDARES IETF ━━━[/bold cyan]")
            console.print("1. Buscar RFC por Número o Protocolo (ej: 791, 1918, 7348, BGP, TCP)")
            console.print("2. Ver RFCs Destacados de la Base de Conocimientos")
            console.print("0. Regresar al Menú Principal")

            sub_opt = Prompt.ask("\nOpción", choices=["0", "1", "2"])

            if sub_opt == "0":
                break
            elif sub_opt == "1":
                q = Prompt.ask("\nNúmero de RFC o protocolo a consultar (o '0' para regresar)", default="7348").strip()
                if q in ["0", "q", "regresar"]:
                    continue
                handle_rfc_search(q)
                Prompt.ask("\n[dim]Presiona Enter para continuar...[/dim]")
            elif sub_opt == "2":
                handle_rfc_search("RFC")
                Prompt.ask("\n[dim]Presiona Enter para continuar...[/dim]")

        except (KeyboardInterrupt, EOFError):
            break
        except Exception as e:
            console.print(Panel(f"[bold red]Error en módulo de estándares:[/bold red] {e}", title="⚠️ Advertencia", border_style="yellow"))


def menu_labs():
    while True:
        try:
            console.print("\n[bold cyan]━━━ 🧪 BANCO DE 200 LABORATORIOS Y EMULACIÓN VIRTUAL ━━━[/bold cyan]")
            console.print("1. Ver los 10 Bloques Temáticos de Laboratorios (001 a 200)")
            console.print("2. Buscar Laboratorios por Tecnología o Certificación (ej: BGP, OSPF, EVPN, CCNA)")
            console.print("0. Regresar al Menú Principal")

            sub_opt = Prompt.ask("\nOpción", choices=["0", "1", "2"])

            if sub_opt == "0":
                break
            elif sub_opt == "1":
                handle_labs_list()
                Prompt.ask("\n[dim]Presiona Enter para continuar...[/dim]")
            elif sub_opt == "2":
                q = Prompt.ask("\nTecnología o certificación (ej: EVPN, MPLS, OSPF, CCNA, o '0' para regresar)", default="EVPN").strip()
                if q in ["0", "q", "regresar"]:
                    continue
                handle_labs_list(q)
                Prompt.ask("\n[dim]Presiona Enter para continuar...[/dim]")

        except (KeyboardInterrupt, EOFError):
            break
        except Exception as e:
            console.print(Panel(f"[bold red]Error en módulo de laboratorios:[/bold red] {e}", title="⚠️ Advertencia", border_style="yellow"))


def menu_examiner():
    while True:
        try:
            console.print("\n[bold cyan]━━━ 🎓 MÓDULO SIMULADOR DE CERTIFICACIONES ━━━[/bold cyan]")
            console.print("1. Modo Práctica (Retroalimentación y explicación inmediata en cada pregunta)")
            console.print("2. Modo Simulación de Examen (Calificación y revisión final)")
            console.print("0. Regresar al Menú Principal")

            sub_opt = Prompt.ask("\nOpción", choices=["0", "1", "2"])
            if sub_opt == "0":
                break

            count_raw = Prompt.ask("Cantidad de preguntas a responder (o '0' para regresar)", default="5").strip()
            if count_raw in ["0", "q", "regresar"]:
                continue
            try:
                count = int(count_raw)
            except ValueError:
                console.print("[yellow]Valor no numérico. Se usarán 5 preguntas por defecto.[/yellow]")
                count = 5

            if sub_opt == "1":
                handle_exam(mode_str="practice", count=count)
            elif sub_opt == "2":
                handle_exam(mode_str="simulation", count=count)

            Prompt.ask("\n[dim]Presiona Enter para continuar...[/dim]")

        except (KeyboardInterrupt, EOFError):
            break
        except Exception as e:
            console.print(Panel(f"[bold red]Error en módulo de examen:[/bold red] {e}", title="⚠️ Advertencia", border_style="yellow"))


def menu_copilot():
    while True:
        try:
            console.print("\n[bold cyan]━━━ 🧠 ASISTENTE & COPILOT EDC ━━━[/bold cyan]")
            console.print("1. Consulta Rápida (1 Pregunta)")
            console.print("2. Iniciar Chat Interactivo")
            console.print("3. Reconstruir Índice Semántico de Documentos")
            console.print("0. Regresar al Menú Principal")

            sub_opt = Prompt.ask("\nOpción", choices=["0", "1", "2", "3"])
            if sub_opt == "0":
                break
            elif sub_opt == "1":
                q = Prompt.ask("\nIngresa tu pregunta técnica (o '0' para regresar)", default="RFC 7348 VXLAN").strip()
                if q in ["0", "q", "regresar"]:
                    continue
                handle_copilot_ask(q)
                Prompt.ask("\n[dim]Presiona Enter para continuar...[/dim]")
            elif sub_opt == "2":
                handle_copilot_chat()
            elif sub_opt == "3":
                indexer = KnowledgeIndexer()
                chunks = indexer.build_index(force_rebuild=True)
                console.print(f"[bold green]✅ Índice reconstruido con éxito: {len(chunks)} secciones indexadas.[/bold green]")
                Prompt.ask("\n[dim]Presiona Enter para continuar...[/dim]")

        except (KeyboardInterrupt, EOFError):
            break
        except Exception as e:
            console.print(Panel(f"[bold red]Error en módulo Copilot:[/bold red] {e}", title="⚠️ Advertencia", border_style="yellow"))


# ============================================================================
# PARSEADOR CLI (SUBCOMANDOS)
# ============================================================================

def main():
    if len(sys.argv) == 1:
        interactive_menu()
        return

    parser = argparse.ArgumentParser(description="PyEDC - Enterprise Data & Connectivity Suite")
    subparsers = parser.add_subparsers(dest="subcommand", help="Módulos disponibles")

    # Subcomando: calc
    p_calc = subparsers.add_parser("calc", help="Calculadora y Diseñador de Red")
    p_calc.add_argument("calc_type", choices=["subnet", "vlsm", "mss", "optics", "fabric"])
    p_calc.add_argument("--cidr", help="Prefijo CIDR (ej: 192.168.1.0/24)")
    p_calc.add_argument("--hosts", help="Requerimientos de hosts (ej: 50,20,10,2)")
    p_calc.add_argument("--mtu", type=int, default=1500)
    p_calc.add_argument("--encaps", help="Encapsulamientos separados por coma (ej: ipsec_esp,gre,vlan_8021q)")
    p_calc.add_argument("--distance", type=float, default=10.0)
    p_calc.add_argument("--fiber", default="OS2_1310")
    p_calc.add_argument("--transceiver", default="10GBASE-LR")
    p_calc.add_argument("--leafs", type=int, default=4)
    p_calc.add_argument("--downlinks", type=int, default=48)
    p_calc.add_argument("--uplinks", type=int, default=4)

    # Subcomando: automator
    p_auto = subparsers.add_parser("automator", help="Automatización y Transpilador Multi-Vendor")
    p_auto.add_argument("action", choices=["translate", "matrix", "generate", "ports"])
    p_auto.add_argument("--cmd", help="Comando a traducir")
    p_auto.add_argument("--from-vendor", default="cisco")
    p_auto.add_argument("--to-vendor", default="huawei")
    p_auto.add_argument("--query", help="Término de búsqueda o puerto")
    p_auto.add_argument("--task", default="vlan")
    p_auto.add_argument("--vendor", default="cisco")

    # Subcomando: exam
    p_exam = subparsers.add_parser("exam", help="Simulador de Exámenes de Certificación")
    p_exam.add_argument("--mode", choices=["practice", "simulation"], default="practice")
    p_exam.add_argument("--count", type=int, default=10)

    # Subcomando: copilot
    p_copilot = subparsers.add_parser("copilot", help="Asistente y Buscador Semántico EDC")
    p_copilot.add_argument("action", choices=["ask", "chat", "reindex"])
    p_copilot.add_argument("--query", "-q", help="Pregunta para el Copilot")

    args = parser.parse_args()

    if args.subcommand == "calc":
        if args.calc_type == "subnet":
            handle_calc_subnet(args.cidr or "192.168.1.0/24")
        elif args.calc_type == "vlsm":
            handle_calc_vlsm(args.cidr or "192.168.1.0/24", args.hosts or "50,20,10,2")
        elif args.calc_type == "mss":
            encs = [e.strip() for e in args.encaps.split(",")] if args.encaps else ["ipsec_esp"]
            handle_calc_mss(args.mtu, encs)
        elif args.calc_type == "optics":
            handle_calc_optics(args.distance, args.fiber, args.transceiver)
        elif args.calc_type == "fabric":
            handle_calc_fabric(args.leafs, args.downlinks, args.uplinks)

    elif args.subcommand == "automator":
        if args.action == "translate":
            handle_transpile(args.cmd or "switchport mode trunk", args.from_vendor, args.to_vendor)
        elif args.action == "matrix":
            handle_matrix_search(args.query or "trunk")
        elif args.action == "generate":
            handle_generate_config(args.task, args.vendor, vlan_id=10, name="DEFAULT", interface="Gi0/1")
        elif args.action == "ports":
            handle_iana_ports(args.query or "445")

    elif args.subcommand == "exam":
        handle_exam(args.mode, args.count)

    elif args.subcommand == "copilot":
        if args.action == "ask":
            handle_copilot_ask(args.query or "RFC 7348 VXLAN")
        elif args.action == "chat":
            handle_copilot_chat()
        elif args.action == "reindex":
            indexer = KnowledgeIndexer()
            indexer.build_index(force_rebuild=True)
            console.print("[green]Índice actualizado.[/green]")


if __name__ == "__main__":
    main()
