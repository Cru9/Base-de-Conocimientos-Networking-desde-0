"""
Calculadora de Presupuesto Óptico (Optical Link Budget) y Atenuación de Fibra Óptica.
Conforme a estándares TIA-568-D e ISO/IEC 11801.
"""

from typing import Dict, Any

FIBER_STANDARDS = {
    "OS2_1310": {"name": "Monomodo OS2 @ 1310nm", "loss_per_km": 0.40, "type": "SMF"},
    "OS2_1550": {"name": "Monomodo OS2 @ 1550nm", "loss_per_km": 0.25, "type": "SMF"},
    "OS1_1310": {"name": "Monomodo OS1 @ 1310nm", "loss_per_km": 1.00, "type": "SMF"},
    "OM3_850":  {"name": "Multimodo OM3 @ 850nm (Laser-Optimized)", "loss_per_km": 3.00, "type": "MMF"},
    "OM4_850":  {"name": "Multimodo OM4 @ 850nm", "loss_per_km": 3.00, "type": "MMF"},
    "OM1_850":  {"name": "Multimodo Legacy OM1 62.5/125 @ 850nm", "loss_per_km": 3.50, "type": "MMF"},
}

OPTICAL_TRANSCEIVERS = {
    "10GBASE-SR": {
        "description": "10Gbps Corto Alcance Multimodo 850nm",
        "tx_min_dbm": -7.3,
        "rx_sensitivity_dbm": -9.9,
        "fiber_pref": "OM3_850",
    },
    "10GBASE-LR": {
        "description": "10Gbps Largo Alcance Monomodo 1310nm (hasta 10km)",
        "tx_min_dbm": -8.2,
        "rx_sensitivity_dbm": -14.4,
        "fiber_pref": "OS2_1310",
    },
    "10GBASE-ER": {
        "description": "10Gbps Extra Alcance Monomodo 1550nm (hasta 40km)",
        "tx_min_dbm": -4.7,
        "rx_sensitivity_dbm": -15.8,
        "fiber_pref": "OS2_1550",
    },
    "10GBASE-ZR": {
        "description": "10Gbps Alcance Ultra Extendido Monomodo 1550nm (hasta 80km)",
        "tx_min_dbm": 0.0,
        "rx_sensitivity_dbm": -24.0,
        "fiber_pref": "OS2_1550",
    },
    "25GBASE-SR": {
        "description": "25Gbps Multimodo 850nm SFP28",
        "tx_min_dbm": -6.4,
        "rx_sensitivity_dbm": -8.4,
        "fiber_pref": "OM4_850",
    },
    "25GBASE-LR": {
        "description": "25Gbps Monomodo 1310nm SFP28 (hasta 10km)",
        "tx_min_dbm": -7.0,
        "rx_sensitivity_dbm": -13.3,
        "fiber_pref": "OS2_1310",
    },
    "40GBASE-SR4": {
        "description": "40Gbps MPO/MTP Multimodo 850nm QSFP+",
        "tx_min_dbm": -7.6,
        "rx_sensitivity_dbm": -9.5,
        "fiber_pref": "OM4_850",
    },
    "100GBASE-LR4": {
        "description": "100Gbps WDM Monomodo QSFP28 (hasta 10km)",
        "tx_min_dbm": -4.3,
        "rx_sensitivity_dbm": -10.6,
        "fiber_pref": "OS2_1310",
    },
}


def calculate_optical_budget(
    distance_km: float,
    fiber_type: str = "OS2_1310",
    num_connectors: int = 2,
    loss_per_connector: float = 0.5,
    num_splices: int = 2,
    loss_per_splice: float = 0.1,
    safety_margin: float = 3.0,
    transceiver_model: str = "10GBASE-LR",
    custom_tx_min: float = None,
    custom_rx_sens: float = None,
) -> Dict[str, Any]:
    """
    Calcula la atenuación total de canal y valida si el presupuesto óptico es viable.
    """
    fiber_info = FIBER_STANDARDS.get(fiber_type, FIBER_STANDARDS["OS2_1310"])
    cable_loss = distance_km * fiber_info["loss_per_km"]
    connector_loss = num_connectors * loss_per_connector
    splice_loss = num_splices * loss_per_splice
    
    total_link_loss = cable_loss + connector_loss + splice_loss + safety_margin

    if transceiver_model in OPTICAL_TRANSCEIVERS:
        xcvr = OPTICAL_TRANSCEIVERS[transceiver_model]
        tx_min = xcvr["tx_min_dbm"] if custom_tx_min is None else custom_tx_min
        rx_sens = xcvr["rx_sensitivity_dbm"] if custom_rx_sens is None else custom_rx_sens
    else:
        tx_min = -8.0 if custom_tx_min is None else custom_tx_min
        rx_sens = -14.0 if custom_rx_sens is None else custom_rx_sens

    power_budget = tx_min - rx_sens
    operating_margin = power_budget - total_link_loss

    if operating_margin >= 3.0:
        status = "EXCELENTE"
        recommendation = "El enlace cuenta con un margen óptico muy seguro (>= 3 dB)."
    elif operating_margin >= 0.0:
        status = "VIABLE CON RIESGO"
        recommendation = "El enlace operará, pero el margen de envejecimiento es estrecho (< 3 dB)."
    else:
        status = "NO VIABLE (ATENUACIÓN EXCESIVA)"
        recommendation = "El enlace caerá por falta de potencia óptica. Requiere transceptores de mayor alcance (ej: ER/ZR) o amplificación EDFA."

    return {
        "transceiver": transceiver_model,
        "fiber_type": fiber_info["name"],
        "distance_km": distance_km,
        "cable_loss_db": round(cable_loss, 3),
        "connectors_loss_db": round(connector_loss, 3),
        "splices_loss_db": round(splice_loss, 3),
        "safety_margin_db": round(safety_margin, 2),
        "total_link_attenuation_db": round(total_link_loss, 3),
        "power_budget_db": round(power_budget, 2),
        "operating_margin_db": round(operating_margin, 3),
        "status": status,
        "recommendation": recommendation,
        "details": {
            "tx_power_min_dbm": tx_min,
            "rx_sensitivity_dbm": rx_sens,
        },
    }
