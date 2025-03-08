# Gestión de Máquinas y Mantenimientos

Este proyecto es una aplicación de escritorio en Python para gestionar el mantenimiento de máquinas de café y grinders. La aplicación permite:

- **Agregar y eliminar máquinas:** Registra tus equipos, define su tipo y la fecha de inicio de uso.
- **Registro de uso y mantenimiento:** Lleva un seguimiento del uso (en litros) y del mantenimiento realizado para cada tarea.
- **Tareas personalizadas:** Configura tareas de mantenimiento con thresholds (umbral de tiempo y uso) adaptables a cada máquina.
- **Interfaz gráfica profesional:** Basada en Tkinter y ttk, con un header que muestra un logo y una lista de máquinas en un Treeview con sus detalles.

## Estructura del Proyecto

La estructura de archivos es la siguiente:

coffee_maintenance/
├── config.py            # Configuración global (tipos de máquina y tareas predeterminadas)
├── data_manager.py      # Gestión de carga y guardado de datos en formato JSON
├── maintenance_app.py   # Interfaz gráfica principal de la aplicación
├── machine.py           # Clase para representar una máquina
├── maintenance_task.py  # Clase para representar una tarea de mantenimiento
├── main.py              # Punto de entrada de la aplicación
└── logo.png             # Logo de la aplicación


## Requisitos

- **Python 3.x**
- **Tkinter** (normalmente incluido con Python)
- **Pillow** (para el manejo de imágenes)

### Instalación de Pillow

Para instalar Pillow, utiliza pip:

pip install pillow
