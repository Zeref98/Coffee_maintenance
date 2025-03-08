# maintenance_task.py
from datetime import datetime

class MaintenanceTask:
    def __init__(self, task_id, name, has_usage, threshold_days, threshold_usage=None, last_date=None, usage_count=0):
        self.task_id = task_id  # Identificador único de la tarea
        self.name = name
        self.has_usage = has_usage
        self.threshold_days = threshold_days
        self.threshold_usage = threshold_usage if has_usage else None
        self.last_date = last_date  # Fecha del último mantenimiento (YYYY-MM-DD)
        self.usage_count = usage_count if has_usage else None

    def register_usage(self, quantity):
        if self.has_usage:
            try:
                qty = float(quantity)
                self.usage_count += qty
            except ValueError:
                raise ValueError("La cantidad debe ser un número.")

    def register_maintenance(self):
        self.last_date = datetime.now().strftime("%Y-%m-%d")
        if self.has_usage:
            self.usage_count = 0

    def to_dict(self):
        d = {"name": self.name,
             "has_usage": self.has_usage,
             "threshold_days": self.threshold_days,
             "threshold_usage": self.threshold_usage,
             "last_date": self.last_date}
        if self.has_usage:
            d["usage_count"] = self.usage_count
        return d

    @classmethod
    def from_dict(cls, task_id, data):
        # Se espera que en data estén almacenados todos los parámetros necesarios.
        return cls(
            task_id=task_id,
            name=data.get("name"),
            has_usage=data.get("has_usage", False),
            threshold_days=data.get("threshold_days"),
            threshold_usage=data.get("threshold_usage"),
            last_date=data.get("last_date"),
            usage_count=data.get("usage_count", 0)
        )
