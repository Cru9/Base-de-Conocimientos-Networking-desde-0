"""
Motor del Diccionario Enciclopédico Técnico de Redes y Ciberseguridad EDC.
Extrae y consulta +200 términos formalmente clasificados desde 02_DICCIONARIO_DEFINICIONES_Y_GLOSARIO_TECNICO.md.
"""

import re
import random
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from pyedc.config import GLOSSARY_FILE


class GlossaryTerm(BaseModel):
    term: str
    letter: str
    domain_layer: str = ""
    standards: List[str] = Field(default_factory=list)
    definition: str = ""


class GlossaryEngine:
    def __init__(self):
        self.terms: List[GlossaryTerm] = []
        self._load_glossary()

    def _load_glossary(self):
        if not GLOSSARY_FILE.exists():
            return

        content = GLOSSARY_FILE.read_text(encoding="utf-8")
        
        # Separar por bloques de letras (### A, ### B...)
        letter_blocks = re.split(r"\n###\s+([A-Z])\s*\n", content)
        if len(letter_blocks) < 3:
            return

        # Vienen en pares: [preámbulo, letra1, texto1, letra2, texto2...]
        for i in range(1, len(letter_blocks), 2):
            letter = letter_blocks[i].strip()
            block_text = letter_blocks[i + 1]

            # Cada término empieza con #### **NOMBRE_TERMINO**
            term_splits = re.split(r"\n####\s+\*\*([^*]+)\*\*", block_text)
            for j in range(1, len(term_splits), 2):
                term_name = term_splits[j].strip()
                term_body = term_splits[j + 1].strip()

                domain_layer = ""
                standards = []
                definition = ""

                # Extraer Dominio / Capa
                dom_match = re.search(r"-\s+\*\*Dominio\s*/\s*Capa:\*\*\s*(.+)", term_body, re.IGNORECASE)
                if dom_match:
                    domain_layer = dom_match.group(1).strip()

                # Extraer Estándares
                std_match = re.search(r"-\s+\*\*Estándar(?:es)?:\*\*\s*(.+)", term_body, re.IGNORECASE)
                if std_match:
                    std_raw = std_match.group(1).strip()
                    standards = [s.strip() for s in std_raw.split(",") if s.strip()]

                # Extraer Definición
                def_match = re.search(r"-\s+\*\*Definición:\*\*\s*(.+?)(?=\n-|\Z)", term_body, re.DOTALL | re.IGNORECASE)
                if def_match:
                    definition = def_match.group(1).strip()
                else:
                    # Si no tiene viñeta explícita de definición, tomar el resto del cuerpo
                    clean_lines = [l for l in term_body.splitlines() if not l.startswith("- **Dominio") and not l.startswith("- **Estándar")]
                    definition = "\n".join(clean_lines).strip()

                self.terms.append(GlossaryTerm(
                    term=term_name,
                    letter=letter,
                    domain_layer=domain_layer,
                    standards=standards,
                    definition=definition,
                ))

    def search(self, query: str) -> List[GlossaryTerm]:
        """Busca términos por acrónimo, nombre, dominio o palabra clave."""
        q = query.strip().lower()
        if not q:
            return []

        results = []
        for t in self.terms:
            if q in t.term.lower() or q in t.definition.lower() or q in t.domain_layer.lower() or any(q in s.lower() for s in t.standards):
                results.append(t)
        return results

    def get_by_letter(self, letter: str) -> List[GlossaryTerm]:
        """Devuelve todos los términos que comienzan con una letra dada."""
        let = letter.strip().upper()
        return [t for t in self.terms if t.letter == let]

    def get_random_term(self) -> Optional[GlossaryTerm]:
        """Devuelve un término aleatorio para estudio estilo flashcard."""
        if not self.terms:
            return None
        return random.choice(self.terms)

    def get_available_letters(self) -> List[str]:
        """Devuelve la lista de letras con términos registrados."""
        return sorted(list(set(t.letter for t in self.terms)))
