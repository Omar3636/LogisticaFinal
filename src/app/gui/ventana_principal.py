import tkinter as tk
from ..basededatos import conexion as bd
from tkinter import ttk, messagebox
from .dialogos.PedidoDialogo import PedidoDialogo
from src.app.servicios import reportes

class Aplicacion:
    def __init__(self, raiz):
        self.ventana = raiz
        self.ventana.title("Sistema de Gestión de Envíos y Logística")
        self.ventana.geometry("1920x1024")
        self.envios = self._cargar_envios_desde_bd()
        self._crear_cuadros()
        self._actualizar_lista()

    def _crear_cuadros(self):
        # Cuadro principal
        cuadro_principal = ttk.Frame(self.ventana, padding="10")
        cuadro_principal.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configuración de grid para ser responsivo
        self.ventana.columnconfigure(0, weight=1)
        self.ventana.rowconfigure(0, weight=1)
        cuadro_principal.columnconfigure(0, weight=1)
        cuadro_principal.rowconfigure(0, weight=0)
        cuadro_principal.rowconfigure(1, weight=1)
        cuadro_principal.rowconfigure(2, weight=0)

        # Título
        titulo = ttk.Label(cuadro_principal, text="Gestión de Envíos", font=("Arial", 14, "bold"))
        titulo.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Cuadro de la tabla
        cuadro_tabla = ttk.LabelFrame(cuadro_principal, text="Lista de Envíos", padding="10")
        cuadro_tabla.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 20))
        cuadro_tabla.columnconfigure(0, weight=1)
        cuadro_tabla.rowconfigure(0, weight=1)

        # Cuadro de envíos
        self._crear_tabla(cuadro_tabla)

        # Cuadro de botones
        cuadro_botones = ttk.Frame(cuadro_principal)
        cuadro_botones.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E))
        self._crear_botones(cuadro_botones)

    def _crear_tabla(self, parent):
        # Crear cuadro en formato "treeview (tabla)
        columnas = ("ID", "Proveedor", "Cliente", "Destino", "Estado", "Numero_seguimiento", "Fecha_entrega", "Fecha_ingreso")
        self.tabla_envios = ttk.Treeview(parent, columns=columnas, show="headings", height=15)

        # Configuración de columnas
        self.tabla_envios.heading("ID", text="ID")
        self.tabla_envios.heading("Proveedor", text="Proveedor")
        self.tabla_envios.heading("Cliente", text="Cliente")
        self.tabla_envios.heading("Destino", text="Destino")
        self.tabla_envios.heading("Estado", text="Estado")
        self.tabla_envios.heading("Numero_seguimiento", text="Numero de seguimiento")
        self.tabla_envios.heading("Fecha_entrega", text="Fecha de entrega")
        self.tabla_envios.heading("Fecha_ingreso", text="Fecha de ingreso")

        # Anchos de columnas
        self.tabla_envios.column("ID", width=20)
        self.tabla_envios.column("Proveedor", width=100)
        self.tabla_envios.column("Cliente", width=100)
        self.tabla_envios.column("Destino", width=200)
        self.tabla_envios.column("Estado", width=50)
        self.tabla_envios.column("Numero_seguimiento", width=50)
        self.tabla_envios.column("Fecha_entrega", width=50)
        self.tabla_envios.column("Fecha_ingreso", width=50)

        # Scrollbar para la tabla
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=self.tabla_envios.yview)
        self.tabla_envios.configure(yscrollcommand=scrollbar.set)

        # Grid de la tabla y scrollbar
        self.tabla_envios.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        # Configuración de grid weights (peso de cada fila o columna para responsividad.)
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)

    def _crear_botones(self, padre):
        # Botones principales
        boton_agregar = ttk.Button(padre, text="Agregar Envío", command=self.agregar_envio)
        boton_actualizar = ttk.Button(padre, text="Actualizar Envío", command=self.actualizar_envio)
        boton_eliminar = ttk.Button(padre, text="Eliminar Envío", command=self.eliminar_envio)
        boton_informe = ttk.Button(padre, text="Generar Informe", command=self.generar_informe)

        # Ubicación de botones
        boton_agregar.grid(row=0, column=0, padx=5, pady=10)
        boton_actualizar.grid(row=0, column=1, padx=5, pady=10)
        boton_eliminar.grid(row=0, column=2, padx=5, pady=10)
        boton_informe.grid(row=0, column=3, padx=5, pady=10)

    def _actualizar_lista(self):
        # bucle para limpiar la tabla
        for item in self.tabla_envios.get_children(): self.tabla_envios.delete(item)

        # Bucle para llenar con datos
        for envio in self.envios:
            self.tabla_envios.insert("", "end", values=(
                envio.id, envio.proveedor, envio.cliente, envio.destino,
                envio.estado, envio.numero_seguimiento, envio.fecha_entrega, envio.fecha_ingreso
            ))

    def agregar_envio(self):
        # Abre ventana para agregar nuevo envío
        dialogo = PedidoDialogo(self.ventana, "Agregar Envío")
        resultado = dialogo.mostrar()

        if resultado:
            # id temporal antes de su agregado en BD y asignación automática de ID.
            resultado.id= len(self.envios) + 1

            # Agregar el objeto Envio a la base de datos.
            self.envios.append(resultado)
            self._actualizar_lista()
            bd.agregar_bd(resultado)
            messagebox.showinfo("Éxito", "Envío agregado correctamente")

    def actualizar_envio(self):
        # Abre ventana para actualización de envío existente
        seleccion = self.tabla_envios.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona un envío para actualizar")
            return

        # Para obtener datos del envío seleccionado
        item = seleccion[0]
        valores = self.tabla_envios.item(item, "values")
        envio_id = int(valores[0])

        envio_existente = None
        for envio in self.envios:
            if envio.id == envio_id:
                envio_existente = envio
                break

        if not envio_existente:
            messagebox.showerror("Error", "No se encontró el envío seleccionado...")
            return

        dialogo = PedidoDialogo(self.ventana, "Actualizar Envío", envio_existente)
        resultado = dialogo.mostrar()

        if resultado:
            # Se actualiza el envío en la base de datos
            bd.actualizar_bd(resultado)
            self._actualizar_lista()
            messagebox.showinfo("Éxito", "Envío actualizado correctamente")

    def eliminar_envio(self):
        # Elimina el envío seleccionado
        seleccion = self.tabla_envios.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona un envío para eliminar")
            return

        item = seleccion[0]
        valores = self.tabla_envios.item(item, "values")
        envio_id = int(valores[0])

        if messagebox.askyesno("Confirmar", "¿Estás seguro de eliminar este envío?"):
            # Aquí se elimina los datos del envío seleccionado
            self.tabla_envios.delete(seleccion[0])
            bd.eliminar_bd(envio_id)

            messagebox.showinfo("Éxito", "Envío eliminado correctamente")

    def _cargar_envios_desde_bd(self):
        try:
            envios = bd.mostrar_todo_bd()
            return envios
        except Exception as e:
            print(f"Error al cargar envíos: {str(e)}")
            return []

    def generar_informe(self):
        try:
            envios = self._cargar_envios_desde_bd()
            reportes.generar_reporte_excel(envios)
            messagebox.showinfo("Informe", "Generando informe de envíos...")
        except Exception as e:
            print(f"Error al generar reporte excel: {str(e)}")
