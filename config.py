# config.py

DATA_FILE = 'machines_data.json'

MACHINE_TYPES = {
    "coffee_machine": {
        "display_name": "Cafetera",
        "maintenance": {
            "filter": {
                "name": "Cambio de Filtro",
                "has_usage": True,
                "threshold_days": 90,
                "threshold_usage": 40
            },
            "descale": {
                "name": "Descalcificación",
                "has_usage": True,
                "threshold_days": 90,
                "threshold_usage": 300
            }
        }
    },
    "grinder": {
        "display_name": "Grinder",
        "maintenance": {
            "cleaning": {
                "name": "Limpieza del Grinder",
                "has_usage": False,
                "threshold_days": 30
            }
        }
    }
}
