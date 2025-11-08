import tkinter as tk
from tkinter import ttk, messagebox
from crud_service import (
    init, crear_proyecto, listar_proyectos, obtener_proyecto,
    actualizar_proyecto, eliminar_proyecto, simular_proyecto
)
import logger_base as _log
from constants import TIPOS_PROYECTO

log = _log.log

DARK_BG = "#0f172a"    # slate-900
DARK_FG = "#e2e8f0"    # slate-200
ACCENT   = "#22c55e"   # green-500
ACCENT_H = "#16a34a"   # green-600
MUTED    = "#94a3b8"   # slate-400

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        log.info('Inicializando aplicación de Simulador Ambiental')
        self.title("Simulador Ambiental — WIP")
        self.geometry("980x600")
        self.minsize(900, 560)
        self._style()
        init()
        self._build_ui()
        self._refresh_list()
        log.debug('Aplicación inicializada correctamente')

    # ---------------------- Estilos ----------------------
    def _style(self):
        style = ttk.Style(self)
        # Usa 'clam' para permitir custom colors en ttk
        try:
            style.theme_use("clam")
        except:
            pass

        # Botón primario
        style.configure("Primary.TButton", foreground="white", background=ACCENT, borderwidth=0, focusthickness=3, padding=(12,7))
        style.map("Primary.TButton",
                  background=[("active", ACCENT_H), ("pressed", ACCENT_H)])
        # Botón suave
        style.configure("Soft.TButton", foreground="#0f172a", background="#e2e8f0", padding=(10,6), borderwidth=0)
        style.map("Soft.TButton", background=[("active", "#cbd5e1")])

        # Cards
        style.configure("Card.TLabelframe", background="white")
        style.configure("Card.TLabelframe.Label", font=("", 10, "bold"))
        style.configure("TLabel", background="white")
        style.configure("TEntry", fieldbackground="white")
        style.configure("TCombobox", fieldbackground="white")

        # Treeview
        style.configure("Treeview",
                        background="white",
                        fieldbackground="white",
                        rowheight=26)
        style.configure("Sidebar.Treeview",
                        background=DARK_BG, fieldbackground=DARK_BG,
                        foreground=DARK_FG)
        style.map("Sidebar.Treeview",
                  background=[("selected", "#1f2937")],
                  foreground=[("selected", "white")])

    # ---------------------- UI ----------------------
    def _build_ui(self):
        # Paned master: sidebar + main
        paned = ttk.Panedwindow(self, orient="horizontal")
        paned.pack(fill="both", expand=True)

        # -------- Sidebar (oscuro)
        self.sidebar = tk.Frame(paned, bg=DARK_BG, width=280)
        paned.add(self.sidebar, weight=0)

        self._build_sidebar()

        # -------- Main (tabs + content)
        main = tk.Frame(paned, bg="white")
        paned.add(main, weight=1)

        # Header
        header = tk.Frame(main, bg="white")
        header.pack(fill="x", padx=14, pady=(12,0))

        title = tk.Label(header, text="Simulador Ambiental", font=("", 16, "bold"), bg="white", fg="#0f172a")
        title.pack(side="left")

        # Acciones primarias
        actions = tk.Frame(header, bg="white")
        actions.pack(side="right")
        ttk.Button(actions, text="Crear", style="Primary.TButton", command=self._crear).pack(side="left", padx=6)
        ttk.Button(actions, text="Actualizar", style="Soft.TButton", command=self._actualizar).pack(side="left", padx=6)
        ttk.Button(actions, text="Eliminar", style="Soft.TButton", command=self._eliminar).pack(side="left", padx=6)

        # Tabs
        self.tabs = ttk.Notebook(main)
        self.tabs.pack(fill="both", expand=True, padx=12, pady=12)

        self.tab_proyectos = tk.Frame(self.tabs, bg="white")
        self.tab_sim = tk.Frame(self.tabs, bg="white")
        self.tab_logs = tk.Frame(self.tabs, bg="white")

        self.tabs.add(self.tab_proyectos, text="Proyectos")
        self.tabs.add(self.tab_sim, text="Simulación")
        self.tabs.add(self.tab_logs, text="Logs")

        self._build_tab_proyectos()
        self._build_tab_sim()
        self._build_tab_logs()

    # ---------------------- Sidebar ----------------------
    def _build_sidebar(self):
        # Logo / título
        tk.Label(self.sidebar, text="Proyectos", fg=DARK_FG, bg=DARK_BG, font=("", 12, "bold")).pack(anchor="w", padx=14, pady=(14,6))

        # Search
        search_wrap = tk.Frame(self.sidebar, bg=DARK_BG)
        search_wrap.pack(fill="x", padx=12, pady=(0,8))
        self.var_search = tk.StringVar()
        ent = ttk.Entry(search_wrap, textvariable=self.var_search)
        ent.pack(side="left", fill="x", expand=True)
        ttk.Button(search_wrap, text="Buscar", command=self._search, style="Soft.TButton").pack(side="left", padx=6)

        # Treeview listado
        cols = ("id", "nombre", "tipo")
        self.tree = ttk.Treeview(self.sidebar, columns=cols, show="headings", style="Sidebar.Treeview")
        self.tree.heading("id", text="ID")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("tipo", text="Tipo")
        self.tree.column("id", width=50, anchor="w")
        self.tree.column("nombre", width=150, anchor="w")
        self.tree.column("tipo", width=90, anchor="w")
        self.tree.pack(fill="both", expand=True, padx=8, pady=8)
        self.tree.bind("<<TreeviewSelect>>", self._on_select)

        # Footer hint
        tk.Label(self.sidebar, text="Tip: doble clic para cargar al formulario",
                 fg=MUTED, bg=DARK_BG, font=("", 9)).pack(anchor="w", padx=12, pady=(0,12))
        self.tree.bind("<Double-1>", self._on_row_double)

    # ---------------------- Tab Proyectos ----------------------
    def _build_tab_proyectos(self):
        container = tk.Frame(self.tab_proyectos, bg="white")
        container.pack(fill="both", expand=True)

        # Grid config
        container.columnconfigure(0, weight=1)
        container.columnconfigure(1, weight=1)
        container.rowconfigure(0, weight=1)

        # Card Formulario
        frm = ttk.LabelFrame(container, text="Proyecto", style="Card.TLabelframe")
        frm.grid(row=0, column=0, sticky="nsew", padx=(0,8), pady=4, ipadx=6, ipady=6)
        frm.columnconfigure(1, weight=1)

        self.var_id = tk.StringVar()
        self.var_nombre = tk.StringVar()
        self.var_tipo = tk.StringVar(value=TIPOS_PROYECTO[0])
        self.var_area = tk.StringVar(value="1.0")
        self.var_duracion = tk.StringVar(value="6")
        self.var_ubicacion = tk.StringVar()
        self.var_intensidad = tk.StringVar(value="5")

        r = 0
        ttk.Label(frm, text="ID").grid(row=r, column=0, sticky="w", padx=6, pady=6)
        ttk.Entry(frm, textvariable=self.var_id, width=18).grid(row=r, column=1, sticky="we", padx=6, pady=6)
        r += 1
        ttk.Label(frm, text="Nombre").grid(row=r, column=0, sticky="w", padx=6, pady=6)
        ttk.Entry(frm, textvariable=self.var_nombre).grid(row=r, column=1, sticky="we", padx=6, pady=6)
        r += 1
        ttk.Label(frm, text="Tipo").grid(row=r, column=0, sticky="w", padx=6, pady=6)
        ttk.Combobox(frm, textvariable=self.var_tipo, values=TIPOS_PROYECTO, state="readonly").grid(row=r, column=1, sticky="w", padx=6, pady=6)
        r += 1

        g2 = tk.Frame(frm, bg="white")
        g2.grid(row=r, column=0, columnspan=2, sticky="we", padx=6)
        for i in range(4): g2.columnconfigure(i, weight=1)

        ttk.Label(g2, text="Área (ha)").grid(row=0, column=0, sticky="w", pady=(0,2))
        ttk.Entry(g2, textvariable=self.var_area, width=10).grid(row=1, column=0, sticky="we", padx=(0,6))

        ttk.Label(g2, text="Duración (meses)").grid(row=0, column=1, sticky="w", pady=(0,2))
        ttk.Entry(g2, textvariable=self.var_duracion, width=10).grid(row=1, column=1, sticky="we", padx=(0,6))

        ttk.Label(g2, text="Intensidad (1-10)").grid(row=0, column=2, sticky="w", pady=(0,2))
        ttk.Entry(g2, textvariable=self.var_intensidad, width=10).grid(row=1, column=2, sticky="we", padx=(0,6))

        ttk.Label(g2, text="Ubicación").grid(row=0, column=3, sticky="w", pady=(0,2))
        ttk.Entry(g2, textvariable=self.var_ubicacion).grid(row=1, column=3, sticky="we")

        # Hint
        tk.Label(frm, text="ID y Nombre son obligatorios. Números válidos en área, duración e intensidad.",
                 bg="white", fg="#475569").grid(row=r+1, column=0, columnspan=2, sticky="w", padx=6, pady=(8,0))

        # Card Resumen selección
        resume = ttk.LabelFrame(container, text="Resumen del proyecto seleccionado", style="Card.TLabelframe")
        resume.grid(row=0, column=1, sticky="nsew", padx=(8,0), pady=4)
        resume.columnconfigure(0, weight=1)
        self.lbl_resumen = tk.Label(resume, text="Ningún proyecto seleccionado.", bg="white", justify="left")
        self.lbl_resumen.grid(row=0, column=0, sticky="nw", padx=8, pady=8)

    # ---------------------- Tab Simulación ----------------------
    def _build_tab_sim(self):
        simfrm = ttk.LabelFrame(self.tab_sim, text="Cálculo de Impacto", style="Card.TLabelframe")
        simfrm.pack(fill="both", expand=True, padx=4, pady=4)
        inner = tk.Frame(simfrm, bg="white")
        inner.pack(fill="both", expand=True, padx=8, pady=8)

        tk.Label(inner, text="Selecciona un proyecto en la barra izquierda o escribe un ID y ejecuta la simulación.",
                 bg="white", fg="#475569").pack(anchor="w")

        btns = tk.Frame(inner, bg="white")
        btns.pack(fill="x", pady=(10,6))
        ttk.Button(btns, text="Simular Impacto", style="Primary.TButton", command=self._simular).pack(side="left")

        self.txt_result = tk.Text(inner, height=14, bg="#f8fafc", relief="flat")
        self.txt_result.pack(fill="both", expand=True, pady=(6,0))

    # ---------------------- Tab Logs ----------------------
    def _build_tab_logs(self):
        wrap = tk.Frame(self.tab_logs, bg="white")
        wrap.pack(fill="both", expand=True, padx=6, pady=6)
        tk.Label(wrap, text="Eventos recientes", bg="white", fg="#475569").pack(anchor="w")
        self.txt_logs = tk.Text(wrap, height=18, bg="#f8fafc", relief="flat")
        self.txt_logs.pack(fill="both", expand=True, pady=6)

    # ---------------------- Helpers ----------------------
    def _log_ui(self, msg: str):
        try:
            self.txt_logs.insert("end", msg + "\n")
            self.txt_logs.see("end")
        except:
            pass

    def _refresh_list(self, filtro: str = ""):
        log.debug('Actualizando lista de proyectos')
        for row in self.tree.get_children():
            self.tree.delete(row)

        proyectos = listar_proyectos()
        log.info(f'Se encontraron {len(proyectos)} proyectos')

        for p in proyectos:
            if filtro and filtro.lower() not in f"{p.id} {p.nombre} {p.tipo}".lower():
                continue
            self.tree.insert("", "end", values=(p.id, p.nombre, p.tipo))

        self._log_ui(f"Listado actualizado. {len(proyectos)} proyectos.")

    def _search(self):
        self._refresh_list(self.var_search.get().strip())

    def _current_id_from_tree(self):
        sel = self.tree.selection()
        if not sel:
            return None
        values = self.tree.item(sel[0], "values")
        return values[0] if values else None

    def _fill_form(self, p):
        self.var_id.set(p.id)
        self.var_nombre.set(p.nombre)
        self.var_tipo.set(p.tipo)
        self.var_area.set(str(p.area_ha))
        self.var_duracion.set(str(p.duracion_meses))
        self.var_ubicacion.set(p.ubicacion)
        self.var_intensidad.set(str(p.intensidad))
        self.lbl_resumen.config(text=f"ID: {p.id}\nNombre: {p.nombre}\nTipo: {p.tipo}\nÁrea: {p.area_ha} ha\nDuración: {p.duracion_meses} meses\nIntensidad: {p.intensidad}\nUbicación: {p.ubicacion}")

    # ---------------------- Eventos ----------------------
    def _on_select(self, _evt):
        pid = self._current_id_from_tree()
        if not pid:
            return
        p = obtener_proyecto(pid)
        if p:
            self._fill_form(p)

    def _on_row_double(self, _evt):
        self._on_select(_evt)
        self.tabs.select(self.tab_proyectos)

    # ---------------------- CRUD ----------------------
    def _crear(self):
        log.info('Creando proyecto')
        try:
            data = dict(
                id=self.var_id.get().strip(),
                nombre=self.var_nombre.get().strip(),
                tipo=self.var_tipo.get().strip(),
                area_ha=float(self.var_area.get() or 0),
                duracion_meses=int(self.var_duracion.get() or 0),
                ubicacion=self.var_ubicacion.get().strip(),
                intensidad=int(self.var_intensidad.get() or 5),
            )
            
            crear_proyecto(data)
            self._refresh_list()
            self._log_ui(f"Proyecto {data['id']} creado.")
            messagebox.showinfo("OK", f"Proyecto {data['id']} creado exitosamente")
            
        except ValueError as e:
            messagebox.showerror("Error de validación", str(e))
            log.error(f'Error de validación al crear proyecto: {e}')
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")
            log.error(f'Error inesperado al crear proyecto: {e}')

    def _actualizar(self):
        pid = self._current_id_from_tree() or self.var_id.get().strip()
        if not pid:
            messagebox.showinfo("Info", "Selecciona un proyecto o escribe un ID")
            return

        cambios = {
            "nombre": self.var_nombre.get().strip(),
            "tipo": self.var_tipo.get().strip(),
            "area_ha": self.var_area.get().strip(),
            "duracion_meses": self.var_duracion.get().strip(),
            "ubicacion": self.var_ubicacion.get().strip(),
            "intensidad": self.var_intensidad.get().strip(),
        }
        ok = actualizar_proyecto(pid, cambios)
        if not ok:
            messagebox.showwarning("No encontrado", f"No existe el proyecto {pid}")
        else:
            self._refresh_list()
            self._log_ui(f"Proyecto {pid} actualizado.")
            messagebox.showinfo("OK", f"Proyecto {pid} actualizado")

    def _eliminar(self):
        pid = self._current_id_from_tree() or self.var_id.get().strip()
        if not pid:
            messagebox.showinfo("Info", "Selecciona un proyecto o escribe un ID")
            return
        if eliminar_proyecto(pid):
            self._refresh_list()
            self._log_ui(f"Proyecto {pid} eliminado.")
            messagebox.showinfo("Eliminado", f"Proyecto {pid} eliminado")
        else:
            messagebox.showwarning("No encontrado", f"No existe el proyecto {pid}")

    # ---------------------- Simulación ----------------------
    def _simular(self):
        pid = self._current_id_from_tree() or self.var_id.get().strip()
        if not pid:
            messagebox.showinfo("Info", "Selecciona un proyecto o escribe un ID")
            return
        imp = simular_proyecto(pid)
        if not imp:
            messagebox.showwarning("No encontrado", f"No existe el proyecto {pid}")
            return

        self.tabs.select(self.tab_sim)
        self.txt_result.delete("1.0", tk.END)
        self.txt_result.insert(tk.END, f"Proyecto: {imp.proyecto_id}\n")
        self.txt_result.insert(tk.END, f"Impacto (riesgo): {imp.riesgo_total:.1f}%\n\n")
        self.txt_result.insert(tk.END, "Puntajes (100=mejor)\n")
        self.txt_result.insert(tk.END, f"  • Aire: {imp.calidad_aire:.1f}\n")
        self.txt_result.insert(tk.END, f"  • Agua: {imp.calidad_agua:.1f}\n")
        self.txt_result.insert(tk.END, f"  • Biodiversidad: {imp.biodiversidad:.1f}\n")
        self.txt_result.insert(tk.END, f"  • Uso del suelo: {imp.uso_suelo:.1f}\n")
        if getattr(imp, "recomendaciones", None):
            self.txt_result.insert(tk.END, "\nRecomendaciones:\n")
            for k, v in imp.recomendaciones.items():
                self.txt_result.insert(tk.END, f"  - {k}: {v}\n")

        self._log_ui(f"Simulación {pid}: riesgo {imp.riesgo_total:.1f}%")

if __name__ == "__main__":
    log.info('Iniciando aplicación Simulador Ambiental')
    App().mainloop()
    log.info('Aplicación finalizada')
