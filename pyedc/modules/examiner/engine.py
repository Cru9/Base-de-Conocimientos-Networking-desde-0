"""
Motor de ejecución de exámenes y sesiones de certificación en consola para PyEDC.
"""

import sys
import random
import time
from enum import Enum
from typing import List, Dict, Optional, Any

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
from rich.prompt import Prompt
from .parser import QuestionItem, load_all_question_banks

console = Console()


class ExamMode(str, Enum):
    PRACTICE = "practice"      # Retroalimentación y explicación inmediata
    SIMULATION = "simulation"  # Modo examen con calificación final al concluir


class ExamSession:
    def __init__(self, questions: List[QuestionItem], mode: ExamMode = ExamMode.PRACTICE, count: Optional[int] = None, shuffle: bool = True):
        self.all_questions = questions
        self.mode = mode
        
        selected = list(questions)
        if shuffle:
            random.shuffle(selected)
        if count and count < len(selected):
            selected = selected[:count]

        self.questions = selected
        self.user_answers: Dict[str, str] = {}
        self.score = 0
        self.start_time = 0.0
        self.end_time = 0.0

    def run_interactive(self) -> Dict[str, Any]:
        """Ejecuta la sesión interactiva en la terminal."""
        if not self.questions:
            console.print("[bold red]❌ No se encontraron preguntas para iniciar el examen.[/bold red]")
            return {}

        console.clear()
        console.print(Panel(
            f"[bold cyan]🏛️ SIMULADOR DE CERTIFICACIÓN EDC[/bold cyan]\n"
            f"[dim]Modo: {self.mode.value.upper()} | Total de preguntas: {len(self.questions)}[/dim]\n"
            f"[yellow]Escribe A, B, C o D para responder. Escribe 'Q' para salir.[/yellow]",
            border_style="cyan"
        ))

        self.start_time = time.time()
        self.score = 0

        for idx, q in enumerate(self.questions, start=1):
            console.print(f"\n[bold yellow]━━━ Pregunta {idx} de {len(self.questions)} [{q.topic}] ━━━[/bold yellow]")
            console.print(f"[bold white]{q.question}[/bold white]\n")

            for letter in sorted(q.options.keys()):
                console.print(f"  [bold cyan]{letter})[/bold cyan] {q.options[letter]}")

            while True:
                choice = Prompt.ask("\n[bold green]Tu respuesta[/bold green]", choices=["A", "B", "C", "D", "Q", "a", "b", "c", "d", "q"]).upper()
                if choice:
                    break

            if choice == "Q":
                console.print("[yellow]Examen interrumpido por el usuario.[/yellow]")
                break

            self.user_answers[q.id] = choice
            is_correct = (choice == q.correct_answer)

            if is_correct:
                self.score += 1

            if self.mode == ExamMode.PRACTICE:
                if is_correct:
                    console.print(Panel(
                        f"[bold green]✅ ¡CORRECTO![/bold green]\n\n"
                        f"[dim]{q.explanation}[/dim]",
                        border_style="green",
                    ))
                else:
                    console.print(Panel(
                        f"[bold red]❌ INCORRECTO. Tu respuesta: {choice} | Respuesta correcta: {q.correct_answer}[/bold red]\n\n"
                        f"[bold]Explicación técnica:[/bold]\n{q.explanation}",
                        border_style="red",
                    ))
                Prompt.ask("[dim]Presiona Enter para continuar...[/dim]")

        self.end_time = time.time()
        return self.show_results()

    def show_results(self) -> Dict[str, Any]:
        """Muestra la cartilla de calificaciones y recomendaciones de estudio."""
        total = len(self.user_answers)
        if total == 0:
            return {"score": 0, "total": 0, "percentage": 0}

        percentage = round((self.score / total) * 100, 2)
        elapsed_seconds = round(self.end_time - self.start_time, 1)
        passed = percentage >= 80.0

        status_text = "[bold green]APROBADO (PASS)[/bold green]" if passed else "[bold red]NO APROBADO (FAIL)[/bold red]"

        console.print("\n")
        console.print(Panel(
            f"[bold cyan]📊 RESULTADOS FINALES DE LA EVALUACIÓN[/bold cyan]\n\n"
            f"Estado: {status_text}\n"
            f"Puntaje Obtenido: [bold]{self.score} / {total}[/bold] ({percentage}%)\n"
            f"Umbral de Aprobación Oficial: [bold]80.0%[/bold]\n"
            f"Tiempo Empleado: [bold]{elapsed_seconds} s[/bold]",
            border_style="green" if passed else "red"
        ))

        # Tabla de desglose
        table = Table(title="Desglose por Pregunta", border_style="dim")
        table.add_column("#", style="dim", width=4)
        table.add_column("Pregunta", style="white", max_width=45)
        table.add_column("Tu Resp.", justify="center", width=8)
        table.add_column("Correcta", justify="center", width=8)
        table.add_column("Resultado", justify="center", width=12)

        for idx, q in enumerate(self.questions[:total], start=1):
            user_ans = self.user_answers.get(q.id, "-")
            ok = (user_ans == q.correct_answer)
            res = "[green]✓ Correcto[/green]" if ok else "[red]✗ Fallo[/red]"
            table.add_row(str(idx), q.question[:45] + "...", user_ans, q.correct_answer, res)

        console.print(table)

        if not passed:
            console.print("\n[bold yellow]💡 Recomendación de Estudio EDC:[/bold yellow]")
            console.print("Revisa los temas fallidos en la carpeta [bold cyan]WIKI_EDC[/bold cyan] y el [bold cyan]02_DICCIONARIO_DEFINICIONES_Y_GLOSARIO_TECNICO.md[/bold cyan].")

        return {
            "score": self.score,
            "total": total,
            "percentage": percentage,
            "passed": passed,
            "time_seconds": elapsed_seconds,
        }
