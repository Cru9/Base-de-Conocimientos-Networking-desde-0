"""
Extractor y parseador de bancos de preguntas de certificación desde archivos Markdown.
"""

import re
from pathlib import Path
from typing import List, Dict, Optional
from pydantic import BaseModel, Field
from pyedc.config import MODULOS_DIR, WIKI_DIR


class QuestionItem(BaseModel):
    id: str
    topic: str
    source_file: str
    question: str
    options: Dict[str, str] = Field(default_factory=dict)
    correct_answer: str
    explanation: str


def parse_question_file(file_path: Path) -> List[QuestionItem]:
    """
    Lee un archivo Markdown que contiene bloques de preguntas y extrae los ítems.
    """
    if not file_path.exists():
        return []

    content = file_path.read_text(encoding="utf-8")
    
    # Expresión regular para bloques de preguntas
    # Detecta: ### ❓ Pregunta X o ### Pregunta X
    q_blocks = re.split(r"###\s+(?:❓\s*)?Pregunta\s+(\d+)", content)
    if len(q_blocks) < 2:
        return []

    items = []
    current_topic = file_path.stem.replace("_", " ")

    # Detectar tema del bloque si existe
    header_block = q_blocks[0]
    topic_match = re.search(r"##\s+(?:📌\s*)?BLOQUE\s*\d*:\s*(.+)", header_block, re.IGNORECASE)
    if topic_match:
        current_topic = topic_match.group(1).strip()

    # Los splits vienen en pares: [encabezado, num1, cuerpo1, num2, cuerpo2, ...]
    for i in range(1, len(q_blocks), 2):
        q_num = q_blocks[i]
        q_body = q_blocks[i + 1]

        # Extraer opciones (A, B, C, D)
        options = {}
        opt_matches = re.findall(r"([A-D])\)\s+(.+?)(?=(?:[A-D]\)|\<details\>|\Z))", q_body, re.DOTALL)
        for letter, text in opt_matches:
            clean_text = " ".join(text.strip().splitlines())
            options[letter.upper()] = clean_text.strip()

        # Extraer texto de la pregunta (todo antes de 'A)')
        q_text_match = re.search(r"^(.*?)(?=[A-D]\))", q_body, re.DOTALL)
        if q_text_match:
            question_text = " ".join(q_text_match.group(1).strip().splitlines()).strip()
        else:
            question_text = f"Pregunta {q_num}"

        # Extraer respuesta correcta
        ans_match = re.search(r"\*\*Respuesta Correcta:\*\*\s*`?([A-D])`?", q_body, re.IGNORECASE)
        correct_answer = ans_match.group(1).upper() if ans_match else ""

        # Extraer explicación
        exp_match = re.search(r"\*\*Explicación:\*\*\s*(.+?)(?=\</details\>|\Z)", q_body, re.DOTALL)
        if exp_match:
            explanation = " ".join(exp_match.group(1).strip().splitlines()).strip()
            # Limpiar prefijo > si existe
            explanation = re.sub(r"^>\s*", "", explanation, flags=re.MULTILINE).strip()
        else:
            explanation = "Sin explicación detallada registrada."

        if options and correct_answer:
            items.append(QuestionItem(
                id=f"{file_path.stem}_Q{q_num}",
                topic=current_topic,
                source_file=file_path.name,
                question=question_text,
                options=options,
                correct_answer=correct_answer,
                explanation=explanation,
            ))

    return items


def load_all_question_banks() -> List[QuestionItem]:
    """Busca y carga todas las preguntas disponibles en el repositorio."""
    all_questions = []

    # 1. Banco maestro en Modelo OSI
    main_bank = MODULOS_DIR / "01_Fundamentos_Fisicos_y_OSI" / "01_Modelo_OSI" / "09_BANCO_DE_PREGUNTAS_Y_CASOS_TIPO_CERTIFICACION.md"
    if main_bank.exists():
        all_questions.extend(parse_question_file(main_bank))

    # 2. Escanear otros archivos que contengan bancos de preguntas
    for p in MODULOS_DIR.rglob("*.md"):
        if p != main_bank and ("PREGUNTA" in p.name.upper() or "BANCO" in p.name.upper()):
            qs = parse_question_file(p)
            all_questions.extend(qs)

    return all_questions
