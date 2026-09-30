"""
Catálogo Oficial de RFCs y Estándares de la IETF / IEEE para PyEDC.
Extrae y consulta estándares documentados en 03_BIBLIOTECA_DOCUMENTAL_Y_RECURSOS_OFICIALES.md.
"""

import re
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from pyedc.config import BIBLIO_FILE


class RFCItem(BaseModel):
    rfc_id: str
    number: int
    title: str
    category: str
    url: str
    description: str


class RFCCatalog:
    def __init__(self):
        self.rfcs: List[RFCItem] = []
        self._load_rfcs()

    def _load_rfcs(self):
        if not BIBLIO_FILE.exists():
            return

        content = BIBLIO_FILE.read_text(encoding="utf-8")
        lines = content.splitlines()

        current_category = "General"
        in_rfc_section = False

        for line in lines:
            line_str = line.strip()

            if "## 2. Catálogo Oficial de RFCs" in line_str:
                in_rfc_section = True
                continue

            if in_rfc_section and line_str.startswith("## ") and not line_str.startswith("## 2."):
                in_rfc_section = False
                break

            if in_rfc_section and line_str.startswith("### "):
                current_category = line_str.replace("### ", "").strip()
                continue

            if in_rfc_section and line_str.startswith("* [RFC"):
                # Formato: * [RFC 791 - Internet Protocol (IPv4 Specification)](https://datatracker.ietf.org/doc/html/rfc791) - Define la estructura...
                match = re.search(r"\*\s+\[RFC\s*(\d+)\s*-\s*([^\]]+)\]\(([^)]+)\)\s*-\s*(.+)", line_str)
                if match:
                    num = int(match.group(1))
                    title = match.group(2).strip()
                    url = match.group(3).strip()
                    desc = match.group(4).strip()

                    self.rfcs.append(RFCItem(
                        rfc_id=f"RFC {num}",
                        number=num,
                        title=title,
                        category=current_category,
                        url=url,
                        description=desc,
                    ))

    def search(self, query: str) -> List[RFCItem]:
        """Busca RFCs por número, título, categoría o descripción."""
        q = query.strip().lower()
        if not q:
            return []

        # Si el usuario busca "rfc 791" o "791"
        num_match = re.search(r"\b(\d+)\b", q)
        target_num = int(num_match.group(1)) if num_match else None

        results = []
        for rfc in self.rfcs:
            if target_num is not None and rfc.number == target_num:
                results.insert(0, rfc)  # Prioridad máxima al número exacto
            elif q in rfc.rfc_id.lower() or q in rfc.title.lower() or q in rfc.description.lower() or q in rfc.category.lower():
                results.append(rfc)

        # Eliminar duplicados manteniendo orden
        seen = set()
        deduped = []
        for r in results:
            if r.number not in seen:
                seen.add(r.number)
                deduped.append(r)
        return deduped

    def get_categories(self) -> List[str]:
        return sorted(list(set(r.category for r in self.rfcs)))
