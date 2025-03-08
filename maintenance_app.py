# maintenance_app.py

import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk
from datetime import datetime
from PIL import Image, ImageTk  # Para cargar y mostrar el logo

from data_manager import DataManager
from machine import Machine
from config import MACHINE_TYPES

class MaintenanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Máquinas y Mantenimientos")
        self.root.geometry("1100x750")
        self.setup_styles()
        self.create_menubar()
        self.create_header()
        
        # Cargar datos de máquinas
        self.data = DataManager.load_data()
        self.machines = [Machine.from_dict(m) for m in self.data.get("machines", [])]
        
        # Ventana dividida en dos paneles
        self.paned = ttk.Panedwindow(self.root, orient=tk.HORIZONTAL)
        self.paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Panel izquierdo: listado de máquinas
        self.left_frame = ttk.Frame(self.paned, padding=10)
        self.paned.add(self.left_frame, weight=1)
        self.create_left_panel()
        
        # Panel derecho: detalles y controles de la máquina seleccionada
        self.right_frame = ttk.Frame(self.paned, padding=10)
        self.paned.add(self.right_frame, weight=3)
        self.create_right_panel()
        
        self.refresh_machine_list()
    
    def setup_styles(self):
        self.style = ttk.Style(self.root)
        self.style.theme_use('clam')
        self.style.configure('TFrame', background='#f7f7f7')
        self.style.configure('TLabel', background='#f7f7f7', font=('Segoe UI', 10))
        self.style.configure('Header.TLabel', font=('Segoe UI', 16, 'bold'), foreground='#333')
        self.style.configure('Treeview.Heading', font=('Segoe UI', 10, 'bold'))
        self.style.configure('Treeview', font=('Segoe UI', 10))
    
    def create_menubar(self):
        menubar = tk.Menu(self.root)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Nuevo", command=self.add_machine)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.root.quit)
        menubar.add_cascade(label="Archivo", menu=file_menu)
        
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Acerca de", command=self.show_about)
        menubar.add_cascade(label="Ayuda", menu=help_menu)
        self.root.config(menu=menubar)
    
    def create_header(self):
        self.header_frame = ttk.Frame(self.root, padding=10)
        self.header_frame.pack(fill=tk.X)
        try:
            # Cargar y redimensionar el logo (ajusta la ruta y el tamaño a tu gusto)
            logo_image = Image.open("logo.png")
            logo_image = logo_image.resize((64, 64), Image.Resampling.LANCZOS)
            self.logo_photo = ImageTk.PhotoImage(logo_image)
            
            # Mostrar el logo en el header
            logo_label = ttk.Label(self.header_frame, image=self.logo_photo)
            logo_label.pack(side=tk.LEFT)
            
            # Establecer el ícono de la ventana con el mismo logo
            self.root.iconphoto(False, self.logo_photo)
        except Exception as e:
            print("Error al cargar el logo:", e)
            logo_label = ttk.Label(self.header_frame, text="LOGO", style="Header.TLabel", foreground="#007acc")
            logo_label.pack(side=tk.LEFT)
        
        title = ttk.Label(self.header_frame, text="Gestión de Máquinas y Mantenimientos", style="Header.TLabel")
        title.pack(side=tk.LEFT, padx=10)
    
    def show_about(self):
        messagebox.showinfo(
            "Acerca de",
            "Aplicación de Gestión de Mantenimientos\nVersión 1.0\n© 2025 Tu Empresa",
            parent=self.root
        )
    
    def create_left_panel(self):
        tree_frame = ttk.Frame(self.left_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        # Definimos 3 columnas: "Name", "Type", "Start"
        self.tree = ttk.Treeview(
            tree_frame,
            columns=("Name", "Type", "Start"),
            show="headings",
            selectmode="browse"
        )
        
        # Configuramos los encabezados
        self.tree.heading("Name", text="Nombre")
        self.tree.heading("Type", text="Tipo")
        self.tree.heading("Start", text="Inicio")
        
        # Ajustamos el ancho y la alineación de cada columna
        self.tree.column("Name", width=120, anchor="center")
        self.tree.column("Type", width=120, anchor="center")
        self.tree.column("Start", width=100, anchor="center")
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree.bind("<<TreeviewSelect>>", self.on_machine_select)
        
        add_btn = ttk.Button(self.left_frame, text="Añadir Máquina", command=self.add_machine)
        add_btn.pack(pady=10)
        
        remove_btn = ttk.Button(self.left_frame, text="Eliminar Máquina", command=self.remove_machine)
        remove_btn.pack(pady=5)
    
    def create_right_panel(self):
        self.details_frame = ttk.Frame(self.right_frame)
        self.details_frame.pack(fill=tk.BOTH, expand=True)
    
    def refresh_machine_list(self):
        # Limpiamos la Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Insertamos las máquinas en la Treeview con sus 3 columnas
        for idx, machine in enumerate(self.machines):
            if machine.machine_type in MACHINE_TYPES:
                mtype = MACHINE_TYPES[machine.machine_type]['display_name']
            else:
                mtype = "Personalizada"
            
            self.tree.insert(
                "", "end",
                iid=idx,
                values=(machine.name, mtype, machine.start_date)
            )
    
    def on_machine_select(self, event):
        selected = self.tree.selection()
        if selected:
            idx = int(selected[0])
            self.show_machine_details(idx)
    
    def show_machine_details(self, idx):
        for widget in self.details_frame.winfo_children():
            widget.destroy()
        machine = self.machines[idx]
        
        # Determinamos el tipo para mostrar en la etiqueta
        if machine.machine_type in MACHINE_TYPES:
            type_display = MACHINE_TYPES[machine.machine_type]['display_name']
        else:
            type_display = machine.machine_type
        
        header_text = f"{machine.name} | Tipo: {type_display} | Inicio: {machine.start_date}"
        header_label = ttk.Label(self.details_frame, text=header_text, style="Header.TLabel")
        header_label.pack(anchor="w", pady=5)
        
        # Botón para gestionar tareas personalizadas
        manage_tasks_btn = ttk.Button(
            self.details_frame,
            text="Gestionar Tareas",
            command=lambda: self.open_manage_tasks(idx)
        )
        manage_tasks_btn.pack(anchor="e", pady=5)
        
        # Si existen tareas, se muestran en un Notebook; si no, se muestra un aviso.
        if machine.maintenance_tasks:
            notebook = ttk.Notebook(self.details_frame)
            notebook.pack(fill=tk.BOTH, expand=True, pady=10)
            
            for task_id, task in machine.maintenance_tasks.items():
                tab = ttk.Frame(notebook, padding=10)
                notebook.add(tab, text=task.name)
                
                info = "Último mantenimiento: "
                if task.last_date:
                    dt_last = datetime.strptime(task.last_date, "%Y-%m-%d")
                    days_elapsed = (datetime.now() - dt_last).days
                    info += f"{task.last_date} ({days_elapsed} días atrás)"
                else:
                    info += "N/A"
                
                if task.has_usage:
                    info += f"\nUso acumulado: {task.usage_count} litros\nThreshold uso: {task.threshold_usage} litros"
                
                info += f"\nThreshold tiempo: {task.threshold_days} días"
                
                info_label = ttk.Label(tab, text=info, font=('Segoe UI', 10))
                info_label.pack(anchor="w", pady=5)
                
                if task.has_usage:
                    qty_frame = ttk.Frame(tab)
                    qty_frame.pack(anchor="w", pady=5)
                    qty_label = ttk.Label(qty_frame, text="Cantidad (litros):")
                    qty_label.pack(side=tk.LEFT, padx=5)
                    qty_entry = ttk.Entry(qty_frame, width=10)
                    qty_entry.pack(side=tk.LEFT, padx=5)
                    
                    reg_usage_btn = ttk.Button(
                        qty_frame,
                        text="Registrar Uso",
                        command=lambda t_id=task_id, entry=qty_entry, m_idx=idx: self.register_usage(m_idx, t_id, entry)
                    )
                    reg_usage_btn.pack(side=tk.LEFT, padx=5)
                
                reg_maint_btn = ttk.Button(
                    tab,
                    text="Registrar Mantenimiento",
                    command=lambda t_id=task_id, m_idx=idx: self.register_maintenance(m_idx, t_id)
                )
                reg_maint_btn.pack(pady=5)
        else:
            no_tasks_label = ttk.Label(
                self.details_frame,
                text="No hay tareas definidas. Utiliza 'Gestionar Tareas' para agregarlas.",
                font=('Segoe UI', 10, 'italic')
            )
            no_tasks_label.pack(pady=20)
    
    def open_manage_tasks(self, machine_idx):
        ManageTasksDialog(self.root, self.machines[machine_idx], callback=lambda: self.after_manage_tasks(machine_idx))
    
    def after_manage_tasks(self, machine_idx):
        self.save_all_data()
        self.show_machine_details(machine_idx)
    
    def add_machine(self):
        name = simpledialog.askstring("Nueva Máquina", "Introduce el nombre de la máquina:", parent=self.root)
        if not name:
            return  # Se cancela si se pulsa Cancelar o no se introduce nombre
        
        machine_types_str = ", ".join([f"{k} ({v['display_name']})" for k, v in MACHINE_TYPES.items()])
        machine_type = simpledialog.askstring(
            "Tipo de Máquina",
            f"Introduce el tipo de máquina.\nOpciones: {machine_types_str}\n(O deja vacío para personalizada)",
            parent=self.root
        )
        
        if machine_type is None:
            return  # Se cancela
        
        if machine_type == "":
            machine_type = "personalizada"
        elif machine_type not in MACHINE_TYPES:
            machine_type = machine_type  # Permitir tipos personalizados
        
        start_date = simpledialog.askstring(
            "Fecha de inicio",
            "Introduce la fecha de inicio (YYYY-MM-DD) o deja en blanco para usar hoy:",
            parent=self.root
        )
        
        if start_date is None:
            return  # Se cancela
        
        if not start_date:
            start_date = datetime.now().strftime("%Y-%m-%d")
        else:
            try:
                datetime.strptime(start_date, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror(
                    "Error",
                    "Formato de fecha incorrecto. Se usará la fecha actual.",
                    parent=self.root
                )
                start_date = datetime.now().strftime("%Y-%m-%d")
        
        new_machine = Machine(name, machine_type, start_date)
        self.machines.append(new_machine)
        self.save_all_data()
        self.refresh_machine_list()
        
        messagebox.showinfo(
            "Máquina Agregada",
            f"Se ha agregado la máquina '{name}' de tipo {machine_type}.",
            parent=self.root
        )
    
    def remove_machine(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Seleccione una máquina para eliminar.", parent=self.root)
            return
        
        idx = int(selected[0])
        machine = self.machines[idx]
        
        if messagebox.askyesno("Confirmar", f"¿Está seguro de eliminar la máquina '{machine.name}'?", parent=self.root):
            del self.machines[idx]
            self.save_all_data()
            self.refresh_machine_list()
            
            # Limpia el panel de detalles si la máquina eliminada estaba seleccionada
            for widget in self.details_frame.winfo_children():
                widget.destroy()
            
            messagebox.showinfo("Eliminada", "Máquina eliminada.", parent=self.root)
    
    def register_usage(self, machine_idx, task_id, entry):
        quantity = entry.get()
        if not quantity:
            messagebox.showwarning("Aviso", "Debes ingresar una cantidad.", parent=self.root)
            return
        
        try:
            self.machines[machine_idx].register_usage(task_id, quantity)
        except ValueError as e:
            messagebox.showerror("Error", str(e), parent=self.root)
            return
        
        self.save_all_data()
        self.show_machine_details(machine_idx)
        
        messagebox.showinfo(
            "Uso Registrado",
            f"Se han registrado {quantity} litros para la tarea en {self.machines[machine_idx].name}.",
            parent=self.root
        )
    
    def register_maintenance(self, machine_idx, task_id):
        self.machines[machine_idx].register_maintenance(task_id)
        self.save_all_data()
        self.show_machine_details(machine_idx)
        
        messagebox.showinfo(
            "Mantenimiento Registrado",
            f"Mantenimiento registrado para la tarea en {self.machines[machine_idx].name}.",
            parent=self.root
        )
    
    def save_all_data(self):
        data_to_save = {"machines": [machine.to_dict() for machine in self.machines]}
        DataManager.save_data(data_to_save)


# --- Diálogos para gestionar tareas personalizadas ---

class ManageTasksDialog(tk.Toplevel):
    def __init__(self, parent, machine: Machine, callback=None):
        super().__init__(parent)
        self.title("Gestionar Tareas")
        self.machine = machine
        self.callback = callback
        self.geometry("600x400")
        self.transient(parent)
        self.grab_set()
        self.lift(parent)
        self.focus_force()
        self.create_widgets()
        self.refresh_task_list()
    
    def create_widgets(self):
        self.tasks_tree = ttk.Treeview(
            self,
            columns=("Name", "Uso", "T. días", "T. uso"),
            show="headings",
            selectmode="browse"
        )
        self.tasks_tree.heading("Name", text="Nombre")
        self.tasks_tree.heading("Uso", text="Usa contador")
        self.tasks_tree.heading("T. días", text="Threshold días")
        self.tasks_tree.heading("T. uso", text="Threshold uso")
        
        self.tasks_tree.column("Name", width=200)
        self.tasks_tree.column("Uso", width=80, anchor="center")
        self.tasks_tree.column("T. días", width=100, anchor="center")
        self.tasks_tree.column("T. uso", width=100, anchor="center")
        
        self.tasks_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=5)
        
        add_btn = ttk.Button(btn_frame, text="Agregar Tarea", command=self.add_task)
        add_btn.pack(side=tk.LEFT, padx=5)
        
        edit_btn = ttk.Button(btn_frame, text="Editar Tarea", command=self.edit_task)
        edit_btn.pack(side=tk.LEFT, padx=5)
        
        del_btn = ttk.Button(btn_frame, text="Eliminar Tarea", command=self.delete_task)
        del_btn.pack(side=tk.LEFT, padx=5)
        
        close_btn = ttk.Button(btn_frame, text="Cerrar", command=self.close)
        close_btn.pack(side=tk.LEFT, padx=5)
    
    def refresh_task_list(self):
        for item in self.tasks_tree.get_children():
            self.tasks_tree.delete(item)
        
        for task_id, task in self.machine.maintenance_tasks.items():
            uso = "Sí" if task.has_usage else "No"
            t_uso = task.threshold_usage if task.has_usage else "-"
            self.tasks_tree.insert("", "end", iid=task_id, values=(task.name, uso, task.threshold_days, t_uso))
    
    def add_task(self):
        dialog = TaskDialog(self, title="Agregar Tarea")
        self.wait_window(dialog)
        if dialog.result:
            task_id = f"{dialog.result['name']}_{int(datetime.now().timestamp())}"
            from maintenance_task import MaintenanceTask
            
            new_task = MaintenanceTask(
                task_id=task_id,
                name=dialog.result["name"],
                has_usage=dialog.result["has_usage"],
                threshold_days=dialog.result["threshold_days"],
                threshold_usage=dialog.result.get("threshold_usage"),
                last_date=None,
                usage_count=0
            )
            try:
                self.machine.add_maintenance_task(new_task)
            except ValueError as e:
                messagebox.showerror("Error", str(e), parent=self)
            self.refresh_task_list()
    
    def edit_task(self):
        selected = self.tasks_tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Seleccione una tarea para editar.", parent=self)
            return
        
        task_id = selected[0]
        task = self.machine.maintenance_tasks[task_id]
        dialog = TaskDialog(self, title="Editar Tarea", task=task)
        self.wait_window(dialog)
        
        if dialog.result:
            task.name = dialog.result["name"]
            task.has_usage = dialog.result["has_usage"]
            task.threshold_days = dialog.result["threshold_days"]
            task.threshold_usage = dialog.result.get("threshold_usage") if task.has_usage else None
            self.machine.edit_maintenance_task(task)
            self.refresh_task_list()
    
    def delete_task(self):
        selected = self.tasks_tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Seleccione una tarea para eliminar.", parent=self)
            return
        
        task_id = selected[0]
        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar la tarea seleccionada?", parent=self):
            self.machine.remove_maintenance_task(task_id)
            self.refresh_task_list()
    
    def close(self):
        if self.callback:
            self.callback()
        self.destroy()


class TaskDialog(tk.Toplevel):
    def __init__(self, parent, title="Nueva Tarea", task=None):
        super().__init__(parent)
        self.title(title)
        self.geometry("400x300")
        self.transient(parent)
        self.grab_set()
        self.lift(parent)
        self.focus_force()
        
        self.result = None
        self.task = task
        self.create_widgets()
        
        if task:
            self.populate_fields()
    
    def create_widgets(self):
        frame = ttk.Frame(self, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Nombre:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.name_entry = ttk.Entry(frame, width=30)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        self.has_usage_var = tk.BooleanVar()
        self.has_usage_check = ttk.Checkbutton(
            frame,
            text="Usa contador (litros)",
            variable=self.has_usage_var,
            command=self.toggle_threshold_usage
        )
        self.has_usage_check.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        
        ttk.Label(frame, text="Threshold días:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.threshold_days_entry = ttk.Entry(frame, width=10)
        self.threshold_days_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        
        ttk.Label(frame, text="Threshold uso (litros):").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.threshold_usage_entry = ttk.Entry(frame, width=10)
        self.threshold_usage_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=10)
        
        ok_btn = ttk.Button(btn_frame, text="Aceptar", command=self.on_ok)
        ok_btn.pack(side=tk.LEFT, padx=5)
        
        cancel_btn = ttk.Button(btn_frame, text="Cancelar", command=self.destroy)
        cancel_btn.pack(side=tk.LEFT, padx=5)
        
        self.toggle_threshold_usage()
    
    def populate_fields(self):
        self.name_entry.insert(0, self.task.name)
        self.has_usage_var.set(self.task.has_usage)
        self.threshold_days_entry.insert(0, str(self.task.threshold_days))
        
        if self.task.has_usage and self.task.threshold_usage is not None:
            self.threshold_usage_entry.insert(0, str(self.task.threshold_usage))
        
        self.toggle_threshold_usage()
    
    def toggle_threshold_usage(self):
        if self.has_usage_var.get():
            self.threshold_usage_entry.config(state="normal")
        else:
            self.threshold_usage_entry.delete(0, tk.END)
            self.threshold_usage_entry.config(state="disabled")
    
    def on_ok(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "El nombre es obligatorio.", parent=self)
            return
        
        try:
            threshold_days = int(self.threshold_days_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Threshold días debe ser un número entero.", parent=self)
            return
        
        result = {
            "name": name,
            "has_usage": self.has_usage_var.get(),
            "threshold_days": threshold_days
        }
        
        if self.has_usage_var.get():
            try:
                threshold_usage = float(self.threshold_usage_entry.get())
            except ValueError:
                messagebox.showerror("Error", "Threshold uso debe ser un número (puede tener decimales).", parent=self)
                return
            result["threshold_usage"] = threshold_usage
        
        self.result = result
        self.destroy()


# Para ejecutar directamente este archivo (si lo deseas):
if __name__ == "__main__":
    root = tk.Tk()
    app = MaintenanceApp(root)
    root.mainloop()
