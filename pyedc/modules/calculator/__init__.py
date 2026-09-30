"""
Módulo de Cálculo y Diseño de Ingeniería de Redes para PyEDC.
"""

from .subnetting import calculate_vlsm, calculate_subnet_info
from .mtu_mss import calculate_mtu_mss, ENCAPSULATION_OVERHEADS
from .optics import calculate_optical_budget, OPTICAL_TRANSCEIVERS
from .fabric_design import calculate_spine_leaf

__all__ = [
    "calculate_vlsm",
    "calculate_subnet_info",
    "calculate_mtu_mss",
    "ENCAPSULATION_OVERHEADS",
    "calculate_optical_budget",
    "OPTICAL_TRANSCEIVERS",
    "calculate_spine_leaf",
]
