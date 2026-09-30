"""
Módulo de Automatización y Transpilador Multi-Vendor de PyEDC.
"""

from .transpiler import translate_command, translate_batch, get_supported_vendors, find_equivalent_task
from .generator import generate_device_config, TemplateTask

__all__ = [
    "translate_command",
    "translate_batch",
    "get_supported_vendors",
    "find_equivalent_task",
    "generate_device_config",
    "TemplateTask",
]
