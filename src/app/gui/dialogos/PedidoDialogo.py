import tkinter as tk
from tkinter import ttk, messagebox
from src.app.modelos.envio import Envio


class PedidoDialogo:
    def __init__(self, parent, titulo, envio_existente=None):
        self.parent = parent
        self.titulo = titulo
        self.envio_existente = envio_existente
        self.resultado = None

    def mostrar(self):
        self.dialogo = tk.Toplevel(self.parent)
        self.dialogo.title(self.titulo)
        self.dialogo.geometry("400x300")
        self.dialogo.transient(self.parent)
        self.dialogo.grab_set()

        # Configuración para centrar la ventana
        self.dialogo.geometry("+%d+%d" % (self.parent.winfo_rootx() + 50, self.parent.winfo_rooty() + 50))
        self._crear_formulario()
        self.dialogo.wait_window()
        return self.resultado

    def _crear_formulario(self):
        cuadro_principal = ttk.Frame(self.dialogo, padding="20")
        cuadro_principal.pack(fill=tk.BOTH, expand=True)

        # Obtener datos del envío existente o crear diccionario vacío
        if self.envio_existente:
            # Si es un objeto Envio, convertir a diccionario
            datos = self.envio_existente.to_dict()
        else:
            datos = {}

        # Widgets o campos del formulario
        ttk.Label(cuadro_principal, text="Proveedor:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.proveedor_var = tk.StringVar(value=datos.get("proveedor", ""))
        ttk.Entry(cuadro_principal, textvariable=self.proveedor_var, width=30).grid(row=0, column=1, pady=5, padx=(10, 0))

        ttk.Label(cuadro_principal, text="Cliente:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.cliente_var = tk.StringVar(value=datos.get("cliente", ""))
        ttk.Entry(cuadro_principal, textvariable=self.cliente_var, width=30).grid(row=1, column=1, pady=5, padx=(10, 0))

        ttk.Label(cuadro_principal, text="Destino:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.destino_var = tk.StringVar(value=datos.get("destino", ""))
        ttk.Entry(cuadro_principal, textvariable=self.destino_var, width=30).grid(row=2, column=1, pady=5, padx=(10, 0))

        ttk.Label(cuadro_principal, text="Estado:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.estado_var = tk.StringVar(value=datos.get("estado", "Pendiente"))
        estado_combo = ttk.Combobox(cuadro_principal, textvariable=self.estado_var,
                                    values=["Pendiente", "En tránsito", "Entregado", "Cancelado"],
                                    state="readonly", width=27)
        estado_combo.grid(row=3, column=1, pady=5, padx=(10, 0))

        ttk.Label(cuadro_principal, text="Número de seguimiento:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.numero_seguimiento_var = tk.StringVar(value=datos.get("numero_seguimiento", ""))
        ttk.Entry(cuadro_principal, textvariable=self.numero_seguimiento_var, width=30).grid(row=4, column=1, pady=5, padx=(10, 0))

        ttk.Label(cuadro_principal, text="Fecha de entrega:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.fecha_entrega_var = tk.StringVar(value=datos.get("fecha_entrega", ""))
        ttk.Entry(cuadro_principal, textvariable=self.fecha_entrega_var, width=30).grid(row=5, column=1, pady=5, padx=(10, 0))

        # Cuadros para botones
        btn_frame = ttk.Frame(cuadro_principal)
        btn_frame.grid(row=6, column=0, columnspan=2, pady=20)

        ttk.Button(btn_frame, text="Guardar", command=self._guardar).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancelar", command=self._cancelar).pack(side=tk.LEFT, padx=5)

    def _guardar(self):
        # Validar datos
        if not all([self.proveedor_var.get(), self.cliente_var.get(), self.destino_var.get(), self.numero_seguimiento_var.get(),
                    self.fecha_entrega_var.get(),]):
            tk.messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        try:
            # Determina si el envio ya existia o es uno nuevo.
            if self.envio_existente:
                # Para actualizar un envío existente
                self.envio_existente.proveedor = self.proveedor_var.get()
                self.envio_existente.cliente = self.cliente_var.get()
                self.envio_existente.destino = self.destino_var.get()
                self.envio_existente.estado = self.estado_var.get()
                self.envio_existente.numero_seguimiento = self.numero_seguimiento_var.get()
                self.envio_existente.fecha_entrega = self.fecha_entrega_var.get()

                self.resultado = self.envio_existente
            else:
                # Para crear una nueva instancia de la clase envio
                self.resultado = Envio(
                    proveedor=self.proveedor_var.get(),
                    cliente=self.cliente_var.get(),
                    destino=self.destino_var.get(),
                    estado=self.estado_var.get(),
                    numero_seguimiento=self.numero_seguimiento_var.get(),
                    fecha_entrega=self.fecha_entrega_var.get(),

                )
        except Exception as e:
            tk.messagebox.showerror("Error", f"Error al guardar: {str(e)}")

        self.dialogo.destroy()

    def _cancelar(self):
        self.resultado = None
        self.dialogo.destroy()