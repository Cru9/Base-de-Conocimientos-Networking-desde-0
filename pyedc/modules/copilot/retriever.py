"""
Motor de Búsqueda Semántica y Recuperación de Información Técnica (Retriever) para PyEDC.
"""

import math
import re
import unicodedata
from typing import List, Dict, Tuple, Any
from .indexer import KnowledgeIndexer, DocumentChunk


def normalize_text(text: str) -> str:
    """Normaliza texto: minúsculas, elimina acentos diacríticos y puntuación excesiva."""
    text = text.lower()
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    text = re.sub(r"[^\w\s-]", " ", text)
    return text


class KnowledgeRetriever:
    def __init__(self, indexer: KnowledgeIndexer = None):
        self.indexer = indexer or KnowledgeIndexer()
        self.chunks = self.indexer.build_index()

    def search(self, query: str, top_k: int = 5) -> List[Tuple[DocumentChunk, float]]:
        """
        Busca los fragmentos más relevantes para una consulta técnica.
        Aplica scoring ponderado (título, RFCs, coincidencias exactas y densidad de términos).
        """
        if not self.chunks:
            return []

        norm_query = normalize_text(query)
        query_terms = [t for t in norm_query.split() if len(t) >= 2]
        if not query_terms:
            return []

        # Detectar si el usuario busca un RFC específico (ej: RFC 7348)
        rfc_match = re.search(r"rfc\s*(\d+)", query, re.IGNORECASE)
        target_rfc = f"RFC {rfc_match.group(1)}" if rfc_match else None

        scored_chunks = []

        for chunk in self.chunks:
            score = 0.0
            norm_title = normalize_text(chunk.section_title)
            norm_file = normalize_text(chunk.file_name)
            norm_content = normalize_text(chunk.content)

            # 1. Coincidencia directa de RFC (Boost muy alto)
            if target_rfc and target_rfc in chunk.rfcs_mentioned:
                score += 50.0

            # 2. Coincidencia en título de sección (Boost alto)
            for term in query_terms:
                if term in norm_title:
                    score += 15.0
                if term in norm_file:
                    score += 8.0

            # 3. Frecuencia y presencia de términos en el contenido
            matched_terms_count = 0
            for term in query_terms:
                count = norm_content.count(term)
                if count > 0:
                    matched_terms_count += 1
                    # Frecuencia logarítmica para evitar saturación
                    score += 1.0 + math.log(count + 1)

            # Bonus si contiene todos los términos buscados
            if len(query_terms) > 1 and matched_terms_count == len(query_terms):
                score += 12.0

            # Bonus por frase exacta
            if norm_query in norm_content:
                score += 20.0

            if score > 0.0:
                scored_chunks.append((chunk, round(score, 2)))

        scored_chunks.sort(key=lambda x: x[1], reverse=True)
        return scored_chunks[:top_k]
