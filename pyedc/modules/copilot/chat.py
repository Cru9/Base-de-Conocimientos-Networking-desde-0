"""
Asistente y Chat Técnico EDC con recuperación contextual (Copilot RAG).
"""

import sys
from typing import Optional, List

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
from rich.markdown import Markdown
from rich.prompt import Prompt
from .retriever import KnowledgeRetriever, DocumentChunk

console = Console()


class CopilotAssistant:
    def __init__(self, retriever: Optional[KnowledgeRetriever] = None):
        self.retriever = retriever or KnowledgeRetriever()

    def query(self, user_question: str, top_k: int = 3) -> None:
        """Responde a una consulta técnica mostrando los fragmentos más relevantes y citas exactas."""
        results = self.retriever.search(user_question, top_k=top_k)

        if not results:
            console.print(Panel(
                f"[yellow]No se encontraron coincidencias exactas para:[/yellow] '{user_question}'\n\n"
                "[dim]Sugerencia: Prueba con términos más generales (ej: 'VLAN', 'BGP', 'OSPF', 'IPsec', 'RFC 7348').[/dim]",
                title="🔍 Copilot EDC",
                border_style="yellow"
            ))
            return

        console.print(f"\n[bold green]📚 Encontrados {len(results)} fragmentos relevantes en la Base de Conocimientos EDC:[/bold green]\n")

        for idx, (chunk, score) in enumerate(results, start=1):
            rfcs_str = f" | [bold cyan]{', '.join(chunk.rfcs_mentioned)}[/bold cyan]" if chunk.rfcs_mentioned else ""
            header = f"[bold white]#{idx} - {chunk.section_title}[/bold white] [dim]({chunk.file_path}) [Score: {score}]{rfcs_str}[/dim]"

            # Mostrar contenido formateado (máximo 600 caracteres por snippet)
            content_preview = chunk.content
            if len(content_preview) > 650:
                content_preview = content_preview[:650] + "\n\n... *(Continúa en el archivo original)*"

            console.print(Panel(
                Markdown(content_preview),
                title=header,
                border_style="cyan" if idx == 1 else "dim",
                padding=(1, 2)
            ))

    def interactive_chat(self) -> None:
        """Inicia una sesión interactiva de preguntas y respuestas en consola."""
        console.clear()
        console.print(Panel(
            "[bold cyan]🧠 ASISTENTE TÉCNICO & COPILOT EDC[/bold cyan]\n"
            "[dim]Haz preguntas técnicas sobre Switching, Routing, Ciberseguridad, DataCenter, RFCs o Comandos Multi-Vendor.[/dim]\n"
            "[yellow]Escribe tu pregunta o 'salir' para volver al menú.[/yellow]",
            border_style="cyan"
        ))

        while True:
            q = Prompt.ask("\n[bold green]Pregunta a EDC[/bold green]").strip()
            if not q:
                continue
            if q.lower() in ["salir", "exit", "quit", "q"]:
                break

            self.query(q)
