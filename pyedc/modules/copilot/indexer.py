"""
Indexador de contenidos y fragmentación semántica de la Base de Conocimientos EDC.
"""

import json
import re
from pathlib import Path
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from pyedc.config import BASE_DIR, WIKI_DIR, MODULOS_DIR, GLOSSARY_FILE, CHEAT_SHEET_FILE, DATA_DIR


class DocumentChunk(BaseModel):
    id: str
    file_path: str
    file_name: str
    section_title: str
    content: str
    rfcs_mentioned: List[str] = Field(default_factory=list)
    char_count: int = 0


class KnowledgeIndexer:
    def __init__(self, cache_file: Optional[Path] = None):
        self.cache_file = cache_file or (DATA_DIR / "kb_index.json")
        self.chunks: List[DocumentChunk] = []

    def extract_rfcs(self, text: str) -> List[str]:
        """Detecta menciones a estándares RFC (ej: RFC 7348, RFC 1918)."""
        matches = re.findall(r"\bRFC\s*(\d+)\b", text, re.IGNORECASE)
        return sorted(list(set(f"RFC {m}" for m in matches)))

    def chunk_markdown_file(self, file_path: Path) -> List[DocumentChunk]:
        """Divide un archivo Markdown en fragmentos por secciones (# o ##)."""
        if not file_path.exists():
            return []

        try:
            content = file_path.read_text(encoding="utf-8")
        except Exception:
            return []

        rel_path = str(file_path.relative_to(BASE_DIR)).replace("\\", "/")
        sections = re.split(r"\n(?=#{1,3}\s+)", content)
        chunks = []

        for idx, sec in enumerate(sections):
            text = sec.strip()
            if not text or len(text) < 40:
                continue

            # Extraer título de la sección
            first_line = text.splitlines()[0]
            sec_title_match = re.search(r"^#{1,3}\s+(.+)", first_line)
            sec_title = sec_title_match.group(1).strip() if sec_title_match else file_path.stem

            rfcs = self.extract_rfcs(text)

            chunk = DocumentChunk(
                id=f"{file_path.stem}_sec_{idx}",
                file_path=rel_path,
                file_name=file_path.name,
                section_title=sec_title,
                content=text,
                rfcs_mentioned=rfcs,
                char_count=len(text),
            )
            chunks.append(chunk)

        return chunks

    def build_index(self, force_rebuild: bool = False) -> List[DocumentChunk]:
        """Escanea todos los archivos Markdown de la base de conocimientos."""
        if not force_rebuild and self.cache_file.exists():
            try:
                data = json.loads(self.cache_file.read_text(encoding="utf-8"))
                self.chunks = [DocumentChunk(**item) for item in data]
                return self.chunks
            except Exception:
                pass  # Si el caché falla, reconstruir

        all_chunks = []

        # 1. Indexar WIKI_EDC
        if WIKI_DIR.exists():
            for f in WIKI_DIR.glob("*.md"):
                all_chunks.extend(self.chunk_markdown_file(f))

        # 2. Indexar Modulos_Clasificados
        if MODULOS_DIR.exists():
            for f in MODULOS_DIR.rglob("*.md"):
                all_chunks.extend(self.chunk_markdown_file(f))

        # 3. Indexar archivos maestros de la raíz
        for f in [GLOSSARY_FILE, CHEAT_SHEET_FILE]:
            if f.exists():
                all_chunks.extend(self.chunk_markdown_file(f))

        self.chunks = all_chunks

        # Guardar en caché
        try:
            self.cache_file.write_text(
                json.dumps([c.model_dump() for c in all_chunks], ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
        except Exception:
            pass

        return self.chunks
