# machine.py
from datetime import datetime
from maintenance_task import MaintenanceTask
from config import MACHINE_TYPES

class Machine:
    def __init__(self, name, machine_type, start_date=None, maintenance_tasks=None):
        self.name = name
        self.machine_type = machine_type  # Ejemplo: "coffee_machine", "grinder" o personalizado
        self.start_date = start_date if start_date else datetime.now().strftime("%Y-%m-%d")
        # maintenance_tasks es un diccionario: clave = task_id, valor = objeto MaintenanceTask.
        if maintenance_tasks:
            self.maintenance_tasks = maintenance_tasks
        else:
            # Si el tipo de máquina existe en MACHINE_TYPES, se crean las tareas por defecto.
            if machine_type in MACHINE_TYPES:
                default_tasks = MACHINE_TYPES[machine_type].get("maintenance", {})
                self.maintenance_tasks = {}
                for task_id, config in default_tasks.items():
                    self.maintenance_tasks[task_id] = MaintenanceTask(
                        task_id=task_id,
                        name=config["name"],
                        has_usage=config.get("has_usage", False),
                        threshold_days=config.get("threshold_days"),
                        threshold_usage=config.get("threshold_usage") if config.get("has_usage", False) else None,
                        last_date=None,
                        usage_count=0
                    )
            else:
                self.maintenance_tasks = {}

    def register_usage(self, task_id, quantity):
        if task_id in self.maintenance_tasks:
            self.maintenance_tasks[task_id].register_usage(quantity)
        else:
            raise KeyError("Tarea de mantenimiento no encontrada.")

    def register_maintenance(self, task_id):
        if task_id in self.maintenance_tasks:
            self.maintenance_tasks[task_id].register_maintenance()
        else:
            raise KeyError("Tarea de mantenimiento no encontrada.")

    def add_maintenance_task(self, task):
        if task.task_id in self.maintenance_tasks:
            raise ValueError("Ya existe una tarea con ese ID.")
        self.maintenance_tasks[task.task_id] = task

    def edit_maintenance_task(self, task):
        if task.task_id not in self.maintenance_tasks:
            raise KeyError("La tarea no existe.")
        self.maintenance_tasks[task.task_id] = task

    def remove_maintenance_task(self, task_id):
        if task_id in self.maintenance_tasks:
            del self.maintenance_tasks[task_id]
        else:
            raise KeyError("La tarea no existe.")

    def to_dict(self):
        return {
            "name": self.name,
            "machine_type": self.machine_type,
            "start_date": self.start_date,
            "maintenance_tasks": {task_id: task.to_dict() for task_id, task in self.maintenance_tasks.items()}
        }

    @classmethod
    def from_dict(cls, data):
        name = data.get("name")
        machine_type = data.get("machine_type")
        start_date = data.get("start_date")
        tasks_data = data.get("maintenance_tasks", {})
        maintenance_tasks = {}
        # Cargar cada tarea almacenada.
        for task_id, task_dict in tasks_data.items():
            maintenance_tasks[task_id] = MaintenanceTask.from_dict(task_id, task_dict)
        return cls(name, machine_type, start_date, maintenance_tasks)
