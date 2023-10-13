import tkinter
from tkinter import messagebox
from tkinter import *
import tkinter.ttk, time, sqlite3, locale, subprocess, webbrowser, PIL
from PIL import Image, ImageTk

class Ventana_Principal(Frame):
#--------------------------------------------------------------------#
    #Inicia el Constructor y el contructor de la clase Heredada
    def __init__(self, master, nombre_company, base_Datos, imagen1, imagen2, icon, image, pdf, **kwargs):
        super().__init__(master, width=1280, height=720)
        self.master = master
        self.nombre_company = nombre_company
        self.base_Datos = base_Datos
        self.imagensupplier = imagen1
        self.imagencalculadora = imagen2
        self.icon = icon
        self.image = image
        self.pdf = pdf
        self.datos_fila_eliminar = {}
        self.prodFrame = None
        self.servFrame = None
        self.provFrame = None
        self.crearProvFrame = None
        self.compania_seleccionada = None
        self.datos_entry = {}
        self.tituloTablas={}
        self.ventana_detalle_frame = None
        self.ventana_detalle=None
        self.valor_tercera_columna = None
        self.valor_segunda_columna = None
        self.agregarCompanyFrame = None
        self.agregar_modificar_ProvFrame = None
        self.datos_ingresados_agregar = {}
        self.datos_ingresados_agregar_Producto = {}
        self.datos_ingresados_agregar_Servicio = {}
        self.datos_ingresados_modificar = {}
        self.titles = []
        self.tabla_columna_Company = {
            "CompanyT": "Company",
            "CanalT": "Canal",
            "PaisT": "Pais",
            "CiudadT": "Ciudad"
        }
        self.tabla_columna_Producto = {
            "CompanyT": "Company",
            "TipoProductoT": "Tipo",
            "GradoT": "Grado",
            "TratamientoTT": "Tratamiento",
            "NormaPT": "Norma"
        }

        self.tabla_columna_Servicio = {
            "CompanyT": "Company",
            "TipoServicioT": "Tipo",
            "NormaST": "Norma"
        }
        self.compania_seleccionada = None

        self.estilo_treeview = tkinter.ttk.Style()
        self.estilo_treeview.configure("Treeview", rowheight=30, font=("Arial", 20))

        self.red_Font = "#FF3F3F"
        self.grey_Font = "#CFCFCF"
        self.blue_low_Font = "#3AA2E5"
        self.white_Font = "#F3F3F3"
        self.blue_strong_Font ="#5469FF"
        self.black_Font = "#34373A"

        self.createSideTape()
        self.time_update()


#*******************************************************************************************
#*******************************************************************************************
# ------------------------------------------------------------------------------------------

                    # CREAR EL MENU DE OPCIONES AGREGAR, MODIFICAR Y ELIMINAR

# ------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------
    # Se necesita el nombre de la compañia
    def funcion_agregar_datos_Prov(self, ventana):
        # Crear una nueva ventana para agregar datos del proveedor
        ventana_agregar = Toplevel(ventana)
        ventana_agregar.title("Agregar Datos del Proveedor")
        ventana_agregar.wm_iconbitmap(self.icon)

        w = 700
        h = 410

        self.dimension_ventana(w,h,ventana_agregar)

        etiquetas = ["Nombre", "División", "Cargo", "Correo", "Teléfono", "Página Web", "Linea de Credito",
                     "Limite de Credito", "Fecha de Registro"]
        consultaSQL = ["Nombre", "Division", "Cargo", "Correo", "Telefono", "Web", "LineaC", "LimiteC", "FechaR"]
        datos_widgets = {}

        # Obtener los datos de la consulta para los widgets
        consulta = f"SELECT {', '.join(consultaSQL)} FROM ProvDatosT WHERE Company = ?;"
        parametros = (self.compania_seleccionada,)
        resultados = self.consultas_y_modificacion_SQL(consulta, parametros, "2",
                                                       ventana_agregar)  # Se utiliza fetchone() para obtener solo un resultado

        resultados = resultados if resultados is not None else []

        for i, etiqueta in enumerate(etiquetas):
            label = Label(ventana_agregar, text=etiqueta, font=("Arial", 18))
            label.place(x=20, y=40 * i, width=200)

            # Si la etiqueta es "Página Web", mostrar un label con el valor de la consulta
            if etiqueta == "Página Web" or etiqueta == "Linea de Credito" or etiqueta == "Limite de Credito" or etiqueta == "Fecha de Registro":
                valor = resultados[i] if i < len(resultados) else ""
                entry = Entry(ventana_agregar, font=("Arial", 14))
                entry.place(x=240, y=40 * i, width=400)  # Ajusta 'x', 'y' y 'width' según tus necesidades
                entry.insert(0, valor)
                datos_widgets[etiqueta] = entry

            else:
                entry_observacion = Entry(ventana_agregar, font=("Arial", 14))
                entry_observacion.place(x=240, y=40 * i, width=400)  # Ajusta 'x', 'y' y 'width' según tus necesidades
                datos_widgets[etiqueta] = entry_observacion

        # Función para guardar los datos en la base de datos
        def guardar_datos():
            datos_proveedor = []
            for etiqueta in etiquetas:
                widget = datos_widgets[etiqueta]
                if isinstance(widget, tkinter.Entry):
                    valor = widget.get().upper()
                else:
                    valor = None
                datos_proveedor.append(valor)

            # Realizar la consulta para insertar los datos en la base de datos
            consulta = "INSERT INTO ProvDatosT (Company, Nombre, Division, Cargo, Correo, Telefono, Web, LineaC, LimiteC, FechaR) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"
            parametros = tuple([self.compania_seleccionada.upper()] + datos_proveedor)
            self.consultas_y_modificacion_SQL(consulta, parametros, "3", ventana_agregar)

            # Cerrar la ventana después de guardar los datos
            ventana_agregar.destroy()

            # Actualizar la ventana de detalles para mostrar los nuevos datos agregados
            self.abrir_ventana()


        # Botones para guardar o cancelar
        y_boton = 36 * (len(etiquetas) + 1)

        boton_guardar = Button(ventana_agregar, text="Guardar", command=guardar_datos, font=("Arial", 14))
        boton_guardar.place(x=175, y=y_boton, width=150)  # Ajusta 'x', 'y' y 'width' según tus necesidades

        boton_cancelar = Button(ventana_agregar, text="Cancelar", command=ventana_agregar.destroy, font=("Arial", 14))
        boton_cancelar.place(x=350, y=y_boton, width=150)  # Ajusta 'x', 'y' y 'width' según tus necesidades

        for combobox in datos_widgets.values():
            combobox.config(state="normal")

        ventana_agregar.bind("<Control-s>", guardar_datos)
        ventana_agregar.bind("<Control-S>", guardar_datos)
        ventana_agregar.bind("<Escape>", ventana_agregar.destroy)
# -----------
    # Se necesita el nombre de la compañia y el nombre de la persona
    def funcion_modificar_datos_Prov(self):

        ventana_modificar = Toplevel(self.ventana_detalle)
        ventana_modificar.title("Modificar Datos del Proveedor")
        ventana_modificar.wm_iconbitmap(self.icon)

        w = 700 # Ancho (x)
        h = 410 # Alto (y)

        self.dimension_ventana(w, h, ventana_modificar)


        # Etiquetas y widgets para mostrar y modificar los datos
        etiquetas = ["Nombre", "División", "Cargo", "Correo", "Teléfono", "Página Web", "Linea de Credito", "Limite de Credito", "Fecha de Registro"]
        consultaSQL = ["Nombre", "Division", "Cargo", "Correo", "Telefono", "Web", "LineaC", "LimiteC", "FechaR"]
        datos_widgets = {}

        # Obtener los datos de la consulta para los widgets
        consulta = f"SELECT {', '.join(consultaSQL)} FROM ProvDatosT WHERE Company = ? AND Nombre = ? AND Division = ?;"
        parametros = (self.compania_seleccionada, self.valor_segunda_columna, self.valor_tercera_columna)
        resultados = self.consultas_y_modificacion_SQL(consulta, parametros, "2", ventana_modificar)

        for i, etiqueta in enumerate(etiquetas):
            label = Label(ventana_modificar, text=etiqueta, font=("Arial", 18))
            label.place(x=20, y=40 * i, width=200)
            valor = resultados[i]
            entry = Entry(ventana_modificar, font=("Arial", 14))
            entry.insert(0, valor if valor is not None else "")  # Insertar el valor actual en el Entry
            entry.place(x=240, y=40 * i, width=400)  # Ajusta 'x', 'y' y 'width' según tus necesidades
            datos_widgets[etiqueta] = entry

            # Función para guardar los datos modificados en la base de datos

        def guardar_modificacion():
            datos_proveedor = []
            for etiqueta in etiquetas:
                widget = datos_widgets[etiqueta]
                valor = widget.get().upper()  # Convertir a mayúsculas antes de guardar
                datos_proveedor.append(valor)

            # Realizar la consulta para actualizar los datos en la base de datos
            consulta = "UPDATE ProvDatosT SET Nombre=?, Division=?, Cargo=?, Correo=?, Telefono=?, Web=?, LineaC = ?, LimiteC = ?, FechaR = ? WHERE Company = ? AND Division = ? AND Nombre = ?;"
            parametros =  tuple(datos_proveedor) + (self.compania_seleccionada, self.valor_tercera_columna, self.valor_segunda_columna)
            self.consultas_y_modificacion_SQL(consulta, parametros, "3", ventana_modificar)

            # Cerrar la ventana después de guardar los datos modificados
            ventana_modificar.destroy()

            # Actualizar la ventana de detalles para mostrar los datos modificados
            self.abrir_ventana()

        y_boton = 36 * (len(etiquetas) + 1)

        # Botones para guardar o cancelar
        boton_guardar = Button(ventana_modificar, text="Guardar", command=guardar_modificacion, font=("Arial", 14), relief="ridge")
        boton_guardar.place(x=175, y=y_boton, width=150)  # Ajusta 'x', 'y' y 'width' según tus necesidades

        boton_cancelar = Button(ventana_modificar, text="Cancelar", command=ventana_modificar.destroy, font=("Arial", 14), relief="ridge")
        boton_cancelar.place(x=350, y=y_boton, width=150)  # Ajusta 'x', 'y' y 'width' según tus necesidades

        ventana_modificar.bind("<Control-s>", guardar_modificacion)
        ventana_modificar.bind("<Control-S>", guardar_modificacion)
        ventana_modificar.bind("<Escape>", ventana_modificar.destroy)

# -----------
    def funcion_eliminar_datos_Prov(self):
        # Mostrar ventana de alerta para confirmar la eliminación
        confirmar_eliminar = messagebox.askyesno("Eliminar datos", "¿Está seguro que desea eliminar los datos?", parent=self.ventana_detalle)
        if confirmar_eliminar:
            # Consulta para verificar si existen registros asociados a la división seleccionada
            consulta = "SELECT COUNT(*) FROM ProvDatosT WHERE Company=? AND Division=? AND Nombre = ?;"
            parametros = (self.compania_seleccionada, self.valor_tercera_columna, self.valor_segunda_columna)
            # Abre la conexión a la base de datos y ejecuta la consulta para contar los registros asociados a la división
            registros_asociados = self.consultas_y_modificacion_SQL(consulta, parametros, "2", self.ventana_detalle)

            if registros_asociados == 0: # Si no hay registros asociados, eliminar toda la compañía de la tabla ProvDatosT
                consulta = "DELETE FROM ProvDatosT WHERE Company=?;"
                parametros = (self.compania_seleccionada,)
                self.consultas_y_modificacion_SQL(consulta, parametros, "3", self.ventana_detalle)

            else: # Si hay registros asociados, eliminar solo el registro específico correspondiente a la compañía, la división y el nombre
                consulta = "DELETE FROM ProvDatosT WHERE Company=? AND Division=? AND Nombre=?;"
                parametros = (self.compania_seleccionada, self.valor_tercera_columna, self.valor_segunda_columna)
                self.consultas_y_modificacion_SQL(consulta, parametros, "3", self.ventana_detalle)


            if registros_asociados == 0:
                consulta = "DELETE FROM ProvDatosT WHERE Company=?;"
                parametros = (self.compania_seleccionada,)
                self.consultas_y_modificacion_SQL(consulta, parametros, "3", self.ventana_detalle)

            else:
                consulta = "DELETE FROM ProvDatosT WHERE Company=? AND Division=? AND Nombre=?;"
                parametros = (self.compania_seleccionada, self.valor_tercera_columna, self.valor_segunda_columna)
                self.consultas_y_modificacion_SQL(consulta, parametros, "3", self.ventana_detalle)

            self.abrir_ventana()

            if registros_asociados == 0:
                # Cierra la ventana de detalles para el proveedor actual después de eliminar
                self.ventana_detalle.destroy()
        else:
            return


# ------------------------------------------------------------------------------------------

                    # CREAR EL MENU DE OPCIONES AGREGAR Y ELIMINAR PRODUCTO SERVICIO

# ------------------------------------------------------------------------------------------
    #este es cuando se quiere agregar un producto y se ve desde el treeview
    def funcion_agregar_Prod_Serv(self, tipo):
        if self.compania_seleccionada is None:
            messagebox.showwarning("Advertencia", "Por favor, seleccione una empresa", parent=self.ventana_busqueda)
        elif self.compania_seleccionada != None and self.compania_seleccionada != "-------------------------":
            ventana_agregar_Prod_Serv = Toplevel()
            ventana_agregar_Prod_Serv.title("Agregar Producto" if tipo == "p" else "Agregar Servicio")
            ventana_agregar_Prod_Serv.wm_iconbitmap(self.icon)
            ventana_agregar_Prod_Serv.title(f"Agregar Producto o Servicio para la compañia -> {self.compania_seleccionada}")

            w = 1160
            h = 400

            self.dimension_ventana(w, h, ventana_agregar_Prod_Serv)

            alerta = True
            frame = Frame(ventana_agregar_Prod_Serv, bg=self.grey_Font)
            frame.place(x=0, y=0, relheight=1, relwidth=1)
            self.confWidget_Prod_Serv(50,frame,alerta, ventana_agregar_Prod_Serv, False)

            def cerrarVentana(event):
                ventana_agregar_Prod_Serv.destroy()
                self.actualizarTreeview()

            ventana_agregar_Prod_Serv.bind("<Control-w>", cerrarVentana)
            ventana_agregar_Prod_Serv.bind("<Control-W>", cerrarVentana)
            self.actualizarTreeview()

            ventana_agregar_Prod_Serv.mainloop()


    # ELIMINAR PRODUCTO // SERVICIO

    def funcion_eliminar_Prod_Serv(self, event):
        if self.compania_seleccionada != None:
            confirmar_eliminar_Prod_Serv = messagebox.askyesno("Eliminar Producto o Servicio", "¿Está seguro que desea eliminar el producto o servicio?", parent=self.ventana_busqueda)
            if confirmar_eliminar_Prod_Serv:
                # Construir la consulta SQL para eliminar los datos de la tabla
                if self.seleccion == "p":
                    tabla = "ProvProductosT"
                else:
                    tabla = "ProvServiciosT"

                consulta = f"DELETE FROM {tabla} WHERE Company = '{self.compania_seleccionada}' AND  "
                condiciones = []
                valores = []
                for columna, valor in self.datos_fila_eliminar_Prod_Serv.items():
                    if valor == "":
                        condiciones.append(f"{columna} IS NULL")
                    else:
                        condiciones.append(f"{columna} = ?")
                        valores.append(valor)
                consulta += " AND ".join(condiciones)

                # Ejecutar la consulta SQL para eliminar los datos de la tabla
                parametros = tuple(valores)
                self.consultas_y_modificacion_SQL(consulta, parametros, "3", self.ventana_busqueda)


                if tabla == "ProvProductosT" or tabla == "ProvServiciosT":
                    if tabla == "ProvProductosT":
                        tabla_dic = {'Tipo': 'TipoProductoT', 'Grado': 'GradoT',
                                     'Tratamiento': 'TratamientoTT', 'Norma': 'NormaPT'}
                    else:
                        tabla_dic = {'Tipo': 'TipoServicioT', 'Norma': 'NormaST'}

                    for columna, valor in self.datos_fila_eliminar_Prod_Serv.items():
                        if valor != "NULL":
                            tabla_relacionada = tabla_dic.get(columna)

                            if isinstance(valor, int):
                                valor = str(valor)

                            if tabla_relacionada is None:
                                continue

                            consulta = f"SELECT * FROM {tabla} WHERE {columna} = ?"
                            parametros = (valor,)
                            rows_Tablas = self.consultas_y_modificacion_SQL(consulta, parametros, "1", self.ventana_busqueda)

                            if rows_Tablas:
                                continue

                            else:
                                consulta = f"DELETE FROM {tabla_relacionada} WHERE {columna} = ?"
                                parametros = (valor,)
                                self.consultas_y_modificacion_SQL(consulta, parametros, "3", self.ventana_busqueda)

                        else:
                            continue


                # Consultar si aún existen registros con la compañía seleccionada
                consulta = "SELECT Company FROM ProvServiciosT WHERE Company = ? UNION ALL SELECT Company FROM ProvProductosT WHERE Company = ?"
                parametros = (self.compania_seleccionada, self.compania_seleccionada)
                rows = self.consultas_y_modificacion_SQL(consulta, parametros, "1", self.ventana_busqueda)


                if rows:
                    self.actualizarTreeview()
                else:

                    confirmar_eliminar_Company = messagebox.askyesno("Eliminar datos",
                                                                     "No hay Productos ni Servicios en esta compañía \n \n \n ¿Desea eliminar la compañia?.",
                                                                     parent=self.ventana_busqueda)

                    if confirmar_eliminar_Company:
                        self.eliminar_company()
                        self.actualizarTreeview()

                    else:
                        self.actualizarTreeview()

        else:
            messagebox.showwarning("Advertencia", "Por favor, seleccione una empresa", parent=self.ventana_busqueda)


    def funcion_eliminar_Company(self):

        if self.compania_seleccionada is None:
            messagebox.showwarning("Advertencia", "Por favor, seleccione una empresa", parent=self.ventana_busqueda)
        else:
            confirmar_eliminar_Company = messagebox.askyesno("Eliminar Compañia", f"¿Desea eliminar la compañia {self.compania_seleccionada}?.", parent=self.ventana_busqueda)

            if confirmar_eliminar_Company:
                self.eliminar_company()
                self.actualizarTreeview()

            else:
                self.actualizarTreeview()

    def eliminar_company(self):

        # Lista de nombres de tablas a eliminar
        tablas_eliminar = ["ProvProductosT", "ProvServiciosT", "ProvDatosT", "CompanyT"]

        for tabla in tablas_eliminar:
            consulta = f"SELECT * FROM {tabla} WHERE Company = ?"
            parametros = (self.compania_seleccionada,)
            rows_General = self.consultas_y_modificacion_SQL(consulta, parametros, "1",self.ventana_busqueda)

            if rows_General:
                consulta = f"DELETE FROM {tabla} WHERE Company = ?"
                parametros = (self.compania_seleccionada,)
                self.consultas_y_modificacion_SQL(consulta, parametros, "3", self.ventana_busqueda)

            if tabla == "CompanyT":
                tabla_dic = {'Pais': 'PaisT', 'Ciudad': 'CiudadT'}

                for columna, valor in self.datos_fila_eliminar_Company.items():
                    tabla_relacionada = tabla_dic.get(columna)

                    if tabla_relacionada is None:
                        continue

                    consulta = f"SELECT * FROM {tabla} WHERE {columna} = ?"
                    parametros = (valor,)
                    rows_Tablas = self.consultas_y_modificacion_SQL(consulta, parametros, "1", self.ventana_busqueda)

                    if rows_Tablas:
                        continue

                    else:
                        consulta = f"DELETE FROM {tabla_relacionada} WHERE {columna} = ?"
                        parametros = (valor,)
                        self.consultas_y_modificacion_SQL(consulta, parametros, "3", self.ventana_busqueda)

            if tabla == "ProvProductosT" or tabla == "ProvServiciosT":
                if tabla == "ProvProductosT":
                    tabla_dic = {'Tipo': 'TipoProductoT', 'Grado': 'GradoT',
                                 'Tratamiento': 'TratamientoTT', 'Norma': 'NormaPT'}
                else:
                    tabla_dic = {'Tipo': 'TipoServicioT', 'Norma': 'NormaST'}

                for columna, valor in self.datos_fila_eliminar_Prod_Serv.items():
                    if valor != "":
                        tabla_relacionada = tabla_dic.get(columna)

                        if isinstance(valor, int):
                            valor = str(valor)

                        if tabla_relacionada is None:
                            continue

                        consulta = f"SELECT * FROM {tabla} WHERE {columna} = ?"
                        parametros = (valor,)
                        rows_Tablas = self.consultas_y_modificacion_SQL(consulta, parametros, "1", self.ventana_busqueda)

                        if rows_Tablas:
                            continue

                        else:
                            consulta = f"DELETE FROM {tabla_relacionada} WHERE {columna} = ?"
                            parametros = (valor,)
                            self.consultas_y_modificacion_SQL(consulta, parametros, "3", self.ventana_busqueda)

                    else:
                        continue

    def actualizarTreeview(self):
        # Si todavía hay registros con la compañía seleccionada, actualiza el treeview
        self.treeview.delete(*self.treeview.get_children())
        self.treeview.destroy()
        self.compania_seleccionada = None

        # Volver a crear el treeview
        self.createTreeview()

    # ------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------

#*******************************************************************************************
#*******************************************************************************************

#------------ CREA BOTON UN FRAME PARA LA BUSQUEDA GENERAL-------------------------------------------------------#
    def funBotonProv1(self):
        #Habilitar y deshabilitar los botones de las cinta
        self.boton_imagen1.deshabilitar()
        self.boton_imagen2.habilitar()
        """--------------------------"""
        # Crear un nuevo Frame
        self.provFrame = Frame(self)
        self.provFrame.place(x=120, y=0, relheight=1, relwidth=1)
        """--------------------------"""
        #Crea un Frame cinta dentro del nuevo Frame
        self.cintaProvFrame = Frame(self.provFrame, bg=self.blue_strong_Font)
        self.cintaProvFrame.place(x=0, y=0, height=55, relwidth=1)
        """--------------------------"""
        # -------------CREA UN FRAME PARA AGREGAR PROV, PRODUCTO Y SERVICIO -------------------
        self.provFrame1 = Frame(self.provFrame, bg=self.grey_Font)
        self.provFrame1.place(x=0, y=55, relheight=1, relwidth=1)

        # CREAR EL BOTON AGREGAR EMPRESA
        self.botonAgregar = Button(self.cintaProvFrame, text="AGREGAR EMPRESA", font=("Arial Bold", 20, "bold"),
                                   command=self.agregar_Company)
        self.botonAgregar.place(x=43, y=5, height=45, width=300)

        """--------------------------"""
        # Se crea boton de productos con opcion para deshabilitar
        self.botonProd = Button(self.cintaProvFrame, text="PRODUCTO", font=("Arial Bold", 20, "bold"),
                                command=self.prod)
        self.botonProd.place(x=429, y=5, height=45, width=300)
        """--------------------------"""
        # Se crea boton de servicios con opcion para deshabilitar
        self.botonServ = Button(self.cintaProvFrame, text="SERVICIO", font=("Arial Bold", 20, "bold"),
                                command=self.serv)
        self.botonServ.place(x=815, y=5, height=45, width=300)

# ------ BOTON DE PESOS FUTURA MEJORA --------------------------------------------------------------#

    def funBotonProv2(self):
        #Habilitar y deshabilitar los botones de las cinta
        self.boton_imagen2.deshabilitar()
        self.boton_imagen1.habilitar()

        if self.provFrame and self.provFrame.winfo_ismapped():
            self.provFrame.destroy()

# ------------------------------ CREA COMPAÑYA Y MODIFICAR --------------------------------------#
        # ------------------------------------------------------------#
                # CREACION DE ENTRY PARA MODIFICAR COMPAÑIA #
        # ------------------------------------------------------------#

    def agregar_Company(self):

        # Restablecer los frames y los datos de entrada
        if self.servFrame and self.servFrame.winfo_exists():
            if self.servFrame.winfo_ismapped():
                self.servFrame.destroy()
            self.servFrame.destroy()
            if self.datos_entry != {}:
                self.datos_entry = {}
            self.servFrame = None

        if self.prodFrame and self.prodFrame.winfo_exists():
            if self.prodFrame.winfo_ismapped():
                self.prodFrame.destroy()
            self.prodFrame.destroy()
            if self.datos_entry != {}:
                self.datos_entry = {}
            self.prodFrame = None

        self.botonProd.config(state=NORMAL, relief="raised")
        self.botonServ.config(state=NORMAL, relief="raised")
        self.botonAgregar.config(state=DISABLED, relief="sunken")

        self.crearProvFrame = Frame(self.provFrame1, bg=self.grey_Font)
        self.crearProvFrame.place(x=0, y=0, relheight=1, relwidth=1)

        self.cintaEditor = Frame(self.crearProvFrame, bg=self.red_Font)
        self.cintaEditor.place(x=0, y=0, height=55, relwidth=1)

        ventana = self

        self.compania_seleccionada = None

        # Crear el botón "AGREGAR EMPRESA" y asociar la función adecuada
        self.boton_agregar_Company = Button(self.cintaEditor, text="AGREGAR EMPRESA", font=("Arial Bold", 18, "bold"), command=lambda: self.campos_agregar_Company(ventana, "1"))
        self.boton_agregar_Company.place(x=65, y=5, height=45, width=450)

        # Crear el botón "AGREGAR PRODUCTOS / SERVICIOS" y asociar la función adecuada
        self.boton_modificar = Button(self.cintaEditor, text="AGREGAR PRODUCTOS / SERVICIOS", font=("Arial Bold", 18, "bold"), command=lambda: self.campos_agregar_Productos_Servicios(ventana, "2"))
        self.boton_modificar.place(x=650, y=5, height=45, width=450)

        # ------------------------------------------------------------#
                # CREACION DE ENTRY PARA MODIFICAR COMPAÑIA #
        # ------------------------------------------------------------#

# --------------------- CREAR WIDGETS PARA AGREGAR PRODUCTOS A  LA COMPAÑIA ---------------------

    def campos_agregar_Productos_Servicios(self, ventana, selected):

        self.compania_seleccionada = None

        if self.agregarCompanyFrame and self.agregarCompanyFrame.winfo_exists():
            self.agregarCompanyFrame.destroy()

        # Crear una variable de instancia para almacenar el valor seleccionado en el Combobox
        self.combo_selected_value = StringVar()
        self.combo_selected_value.set("")  # Valor inicial vacío

        # Habilitar el botón de modificación y deshabilitar el botón de agregar
        self.boton_modificar.config(state=DISABLED, relief="sunken")
        self.boton_agregar_Company.config(state=NORMAL, relief="raised")

        # Destruir el frame actual si existe
        if self.agregar_modificar_ProvFrame and self.agregar_modificar_ProvFrame.winfo_exists():
            self.agregar_modificar_ProvFrame.destroy()

        # Crea el frame para modificar la empresa con producto
        self.agregar_modificar_ProvFrame = Frame(self.crearProvFrame, bg=self.grey_Font)
        self.agregar_modificar_ProvFrame.place(x=0, y=55, relheight=1, width=1160)

        # Agregar combobox para seleccionar la compañía
        label = Label(self.agregar_modificar_ProvFrame, text="SELECCIONE COMPAÑIA", font=("Arial bold", 18))
        label.place(x=180, y=15, height=30, width=400)
        self.combo_var = StringVar()
        self.combo = tkinter.ttk.Combobox(self.agregar_modificar_ProvFrame, textvariable=self.combo_var, font=("Arial bold", 18), state="readonly")
        self.combo.place(x=180, y=45, height=30, width=400)

        # Obtener las compañías de la base de datos y añadirlas al combobox
        consulta = "SELECT DISTINCT Company FROM CompanyT"
        parametros = "1"
        companies = self.consultas_y_modificacion_SQL(consulta, parametros, "1", ventana)
        company_names = [company[0] for company in companies]
        self.combo['values'] = company_names

        self.combo.bind("<<ComboboxSelected>>", self.on_combo_select)

        alerta = True

        self.boton_Prod_Serv = Button(self.agregar_modificar_ProvFrame, text="SELECCIONAR COMPAÑIA", font=("Arial", 20),
                # yP // yS // Frame donde se va a colocar
                command=lambda: self.alerta_company(200, self.agregar_modificar_ProvFrame,alerta, ventana, selected)) #selected = "1" eliminar contenido widget
        self.boton_Prod_Serv.place(x=80, y=90, width=1000, height=30)

    def alerta_company(self, yP, frame, alerta, ventana, selected):
        if self.compania_seleccionada is None:
            tkinter.messagebox.showwarning("Alerta", "Por favor, seleccione una compañía.")

        else:
            self.confWidget_Prod_Serv(yP, frame, alerta, ventana, selected)
            self.combo.state(["disabled"])
            self.boton_Prod_Serv.config(state=DISABLED, relief="sunken")


    def on_combo_select(self, event):
        self.combo_selected_value.set(self.combo_var.get())
        self.compania_seleccionada = self.combo_selected_value.get()

# --------------------- CREAR WIDGETS PARA AGREGAR COMPAÑIA CON PRODUCTO ---------------------

    def campos_agregar_Company(self, ventana, selected):

        self.compania_seleccionada = None

        if self.agregar_modificar_ProvFrame and self.agregar_modificar_ProvFrame.winfo_exists():
            self.agregar_modificar_ProvFrame.destroy()

        self.boton_modificar.config(state=NORMAL, relief="raised")
        self.boton_agregar_Company.config(state=DISABLED, relief="sunken")

        # Destruir el frame actual si existe
        if self.agregarCompanyFrame and self.agregarCompanyFrame.winfo_exists():
            self.agregarCompanyFrame.destroy()

        # Crea el frame para agregar la empresa con producto
        self.agregarCompanyFrame = Frame(self.crearProvFrame, bg=self.grey_Font)
        self.agregarCompanyFrame.place(x=0, y=55, relheight=1, width=1160)

        # "Compañía", "País", "Ciudad", "Canal"
        y = 15
        # x, y, w, title, tabla
        self.widget_agr(30, y, 350, "COMPAÑIA", "CompanyT", ventana)
        self.widget_agr(440, y, 180, "CANAL", "CanalT", ventana)
        self.widget_agr(670, y,200, "PAIS", "PaisT", ventana)
        self.widget_agr(920, y, 200, "CIUDAD", "CiudadT", ventana)

        selected = "2" # selected = "2" eliminar el contenido de los widgets al dar botón guardar (self.boton_Company)

        self.boton_Company = Button (self.agregarCompanyFrame, text="SIGUIENTE", font=("Arial", 20), command=lambda: self.agregarCompanyBoton(ventana, selected))
        self.boton_Company.place(x=80, y= y +75, width=1000, height=30)


# --------------------- # --------------------- # crear_campos_agregar_Company # --------------------- # --------------------- # ---------------------
    def widget_agr(self, x, y, w, title, tabla, ventana):
        yh = 30
        yant = 0
        if title == "COMPAÑIA":
            label = Label(self.agregarCompanyFrame, text=title, font=("Arial blod", 18, "bold"))
            label.place(x=x, y=y, height=yh, width=w)
            entry = Entry(self.agregarCompanyFrame, font=("Arial", 16))
            entry.place(x=x, y=y + yh + yant, height=yh, width=w)

            self.datos_ingresados_agregar[tabla] = entry

        else:
            columna = self.tabla_columna_Company.get(tabla)

            consulta = f"SELECT DISTINCT {columna} FROM {tabla}"
            parametros = "1"
            rows = self.consultas_y_modificacion_SQL(consulta, parametros, "1", ventana)

            v = [row[0] for row in rows]
            label = Label(self.agregarCompanyFrame, text=title, font=("Arial blod", 18, "bold"))
            label.place(x=x, y=y, height=yh, width=w)

            combobox = tkinter.ttk.Combobox(self.agregarCompanyFrame, values=v, font=("Arial", 16))
            combobox.place(x=x, y=y + yh + yant, height=yh, width=w)

            if title == "CANAL":
                combobox.config(state="readonly")

            self.datos_ingresados_agregar[tabla] = combobox

        self.titles.append(title)

# ---------------------
    def agregarCompanyBoton(self, ventana, selected):
        datos_a_agregar = []
        columnas_a_agregar = []
        for tabla, widget in self.datos_ingresados_agregar.items():
            if isinstance(widget, Entry):
                columna = self.tabla_columna_Company.get(tabla)
                if columna is not None:
                    valor = widget.get().upper()
                    if not valor:
                        titulo_actual = self.titles[len(columnas_a_agregar)]
                        messagebox.showwarning("Advertencia", f"Debes ingresar un valor para {titulo_actual}.")
                        return
                    columnas_a_agregar.append(columna)  # Agregar el nombre completo de la columna
                    datos_a_agregar.append(valor)
            elif isinstance(widget, tkinter.ttk.Combobox):
                columna = self.tabla_columna_Company.get(tabla)
                if columna is not None:
                    valor = widget.get().upper()
                    if not valor:
                        titulo_actual = self.titles[len(columnas_a_agregar)]
                        messagebox.showwarning("Advertencia", f"Debes seleccionar una opción para {titulo_actual}.")
                        return
                    columnas_a_agregar.append(columna)  # Agregar el nombre completo de la columna
                    datos_a_agregar.append(valor)

        consulta = "SELECT * FROM CompanyT WHERE Company=?"
        parametros = (datos_a_agregar[0],)
        row = self.consultas_y_modificacion_SQL(consulta, parametros, "2", ventana)

        if row is not None:
            messagebox.showwarning("Advertencia", "El nombre de la compañía ya existe en la base de datos.")
            return
        else:
            # Comprobar si existen los valores ingresados en la tabla correspondiente
            for columna, valor in zip(columnas_a_agregar, datos_a_agregar):
                if columna in self.tabla_columna_Company.values():
                    # Si el valor está en el diccionario, entonces tienes la tabla correspondiente
                    tabla = next(key for key, value in self.tabla_columna_Company.items() if value == columna)
                    consulta = f"SELECT * FROM {tabla} WHERE {columna}=?"
                    parametros = (valor,)
                    row = self.consultas_y_modificacion_SQL(consulta, parametros, "2", ventana)

                    if row is None:
                        # Si el valor no existe, agregarlo a la tabla correspondiente
                        self.agregar_nuevo_valor(tabla, columna, tuple(columnas_a_agregar), valor, tuple(datos_a_agregar), ventana, selected)

        # ______ AGREGAR VALOR A SQL DESPUES DE PRESIONAR EL BOTON SIGUIENTE



# ---------------------
    def agregar_nuevo_valor(self, tabla, columna, columnas, company, valores, ventana, selected):
        if tabla != "CompanyT" and tabla != "CanalT":
            consulta = f"INSERT INTO {tabla} ({columna}) VALUES (?)"
            parametros = (company,)
            self.consultas_y_modificacion_SQL(consulta, parametros, "3", ventana)

        elif tabla == "CompanyT":
            self.compania_seleccionada = company
            placeholders = ", ".join(["?" for _ in columnas])
            columnas_str = ", ".join(columnas)

            consulta = f"INSERT INTO {tabla}({columnas_str}) VALUES ({placeholders})"
            parametros = (valores)
            self.consultas_y_modificacion_SQL(consulta, parametros, "3", ventana)


        if isinstance(self.datos_ingresados_agregar[tabla], tkinter.ttk.Combobox):
            self.actualizar_combobox(tabla, columna, self.datos_ingresados_agregar[tabla], ventana)

        # Deshabilitar el boton Siguiente
        self.boton_Company.config(state=DISABLED, relief="sunken")

        for widget in self.agregarCompanyFrame.winfo_children():
            widget.config(state="disabled")

        alerta = False

        # yP // yS // Frame donde se va a colocar
        self.confWidget_Prod_Serv(220, self.agregarCompanyFrame,alerta, ventana, selected)

# --------------------- # --------------------- # confWidget_Prod_Serv # --------------------- # --------------------- # ---------------------
    # yP // yS // Frame donde se va a colocar
    def confWidget_Prod_Serv(self, yP, frame, alerta, ventana, selected):
        # -----____---- Crear widgets despues de agregar la compañia

        yS = 210 + yP
        # PRODUCTOS
        self.provProducto_ServicioWidget(36, yP - 60, 800, "AGREGAR PRODUCTOS", "pass", "p", frame, ventana)
        self.provProducto_ServicioWidget(16, yP, 300, self.compania_seleccionada, "CompanyT", "p", frame, ventana)
        self.provProducto_ServicioWidget(348, yP, 280, "TIPO PRODUCTO", "TipoProductoT", "p", frame, ventana)
        self.provProducto_ServicioWidget(660, yP, 120, "GRADO", "GradoT", "p", frame, ventana)
        self.provProducto_ServicioWidget(812, yP, 175, "TRATAMIENTO", "TratamientoTT", "p", frame, ventana)
        self.provProducto_ServicioWidget(1019, yP, 100, "NORMA", "NormaPT", "p", frame, ventana)
        boton1 = Button(frame, text="GUARDAR", font=("Arial", 20))
        boton1.place(x=580, y=yP + 90, width=500, height=30)
        #Agregar Servicio a una compañia y limpiar los combox de Prod y Serv
        boton1.config(command=lambda: [self.agregarProductoServicioBoton("p", alerta, ventana),
                                            self.limpiar_campos(boton1, ventana, selected, "p")])

        # SERVICIOS
        self.provProducto_ServicioWidget(36, (yS - 60), 800, "AGREGAR SERVICIOS", "", "s", frame, ventana)
        self.provProducto_ServicioWidget(16, yS, 300, self.compania_seleccionada, "CompanyT", "s", frame, ventana)
        self.provProducto_ServicioWidget(348, yS, 280, "TIPO SERVICIO", "TipoServicioT", "s", frame, ventana)
        self.provProducto_ServicioWidget(660, yS, 120, "NORMA", "NormaST", "s", frame, ventana)
        boton2 = Button(frame, text="GUARDAR", font=("Arial", 20))
        boton2.place(x=580, y=yS + 90, width=500, height=30)
        # Agregar Servicio a una compañia y limpiar los combox de Prod y Serv
        boton2.config(command=lambda: [self.agregarProductoServicioBoton("s", alerta, ventana),
                                       self.limpiar_campos(boton2, ventana, selected, "s")])

# -----____---- Crea Widget con el dato de la compañia
    def provProducto_ServicioWidget(self, x, y, w, title, tabla, t, frame, ventana):
        yh = 30
        yant = 25
        columna = None

        if title == "AGREGAR PRODUCTOS" or title == "AGREGAR SERVICIOS":
            if t == "p":
                label = Label(frame, text=title, font=("Arial bold", 18, "bold"))
                label.place(x=x, y=y + yant + 10, height=yh + 10, width=w)
            elif t == "s":
                label = Label(frame, text=title, font=("Arial bold", 18, "bold"))
                label.place(x=x, y=y + yant + 10, height=yh + 10, width=w)

        elif tabla == "CompanyT":
            label = Label(frame, text="COMPAÑIA", font=("Arial bold", 18, "bold"))
            label.place(x=x, y=y + yant, height=yh, width=w)
            entry_var = StringVar()
            entry_var.set(title)
            entry = Entry(frame, font=("Arial bold", 14), textvariable=entry_var, state="readonly")
            entry.place(x=x, y=y + yh + yant, height=yh, width=w)

            if t == "p":
                self.datos_ingresados_agregar_Producto[tabla] = entry
            else:
                self.datos_ingresados_agregar_Servicio[tabla] = entry

        else:
            if t == "p":
                columna = self.tabla_columna_Producto.get(tabla)
            elif t == "s":
                columna = self.tabla_columna_Servicio.get(tabla)

            consulta = f"SELECT DISTINCT {columna} FROM {tabla}"
            parametros = "1"
            rows = self.consultas_y_modificacion_SQL(consulta, parametros, "1", ventana)
            v = [row[0] for row in rows]

            label = Label(frame, text=title, font=("Arial bold", 18))
            label.place(x=x, y=y + yant, height=yh, width=w)
            combobox = tkinter.ttk.Combobox(frame, values=v, font=("Arial", 16))
            combobox.place(x=x, y=y + yh + yant, height=yh, width=w)

            if t == "p":
                self.datos_ingresados_agregar_Producto[tabla] =  combobox
            else:
                self.datos_ingresados_agregar_Servicio[tabla] = combobox


#_____ Guardar los valores en las variables para analizar si existen en las Tablas
    def agregarProductoServicioBoton(self, tipo, alerta, ventana):
        datos_a_agregar = []
        columnas_a_agregar = []
        datos_a_agregar1 = []
        columnas_a_agregar1 = []
        placeholders = []

        if tipo == "p":
            datos_ingresados_agregar_Prod_Serv = self.datos_ingresados_agregar_Producto
            tabla_columna_Prod_Serv = self.tabla_columna_Producto
            tabla_general = "ProvProductosT"

        else:
            datos_ingresados_agregar_Prod_Serv = self.datos_ingresados_agregar_Servicio
            tabla_columna_Prod_Serv = self.tabla_columna_Servicio
            tabla_general = "ProvServiciosT"

        for tabla, widget in datos_ingresados_agregar_Prod_Serv.items():
            if isinstance(widget, (Entry, tkinter.ttk.Combobox)):
                columna = tabla_columna_Prod_Serv.get(tabla)
                if columna is not None:
                    valor = widget.get().upper()
                    if valor:
                        columnas_a_agregar.append(columna)
                        datos_a_agregar.append(valor)
                        columnas_a_agregar1.append(columna)
                        datos_a_agregar1.append(valor)
                    else:
                        columnas_a_agregar1.append(columna)
                        datos_a_agregar1.append(None)


        # Comprobar si existen los valores ingresados en la tabla correspondiente
        for columna, valor in zip(columnas_a_agregar, datos_a_agregar):
            if columna in tabla_columna_Prod_Serv.values():
                if valor != "":
                    # Si el valor está en el diccionario, entonces tienes la tabla correspondiente
                    tabla = next(key for key, value in tabla_columna_Prod_Serv.items() if value == columna)
                    consulta = f"SELECT * FROM {tabla} WHERE {columna}=?"
                    parametros = (valor,)
                    row = self.consultas_y_modificacion_SQL(consulta, parametros, "2", ventana)
                    if row is None:
                        # Si el valor no existe, agregarlo a la tabla correspondiente
                        self.agregar_nuevo_Producto_Servicio(tabla, columna, valor, tipo, ventana)

        columnas_str = ", ".join(tuple(columnas_a_agregar))
        valores_str = ", ".join([f"'{valor}'" for valor in datos_a_agregar])

        # Si es True ---> Cuando se va a agregar un producto o servicio con combox de seleecionar compañia
        for columna, valor in zip(columnas_a_agregar1, datos_a_agregar1):
            if valor is None:
                placeholders.append(f"{columna} IS NULL")
            else:
                placeholders.append(f"{columna} = '{valor}'")

        placeholders_str = " AND ".join(placeholders)

        consulta = f"SELECT * FROM {tabla_general} WHERE {placeholders_str}"
        parametros = "1"
        row_alerta = self.consultas_y_modificacion_SQL(consulta, parametros, "2", ventana)

        # Comprobar si "Tipo" está vacío o si otros campos están vacíos
        if any(columna == "Tipo" and valor is None for columna, valor in zip(columnas_a_agregar1, datos_a_agregar1)):
            if tipo == "p":
                messagebox.showwarning("Advertencia",
                                       f"Por favor ingresa un Producto para {self.compania_seleccionada}.",
                                       parent=ventana)
                return
            else:
                messagebox.showwarning("Advertencia",
                                       f"Por favor ingresa un Servicio para {self.compania_seleccionada}.",
                                       parent=ventana)
                return

        else:
            if row_alerta is None:
                consulta = f"INSERT INTO {tabla_general}({columnas_str}) VALUES ({valores_str})"
                parametros = "1"
                self.consultas_y_modificacion_SQL(consulta, parametros, "3", ventana)
                messagebox.showinfo("Éxito", "Se agregó correctamente!!.", parent=ventana)

                if alerta:
                    self.boton_Prod_Serv.config(text="SELECCIONAR OTRA COMPAÑIA", state=NORMAL, relief="raised",
                                                command=lambda: self.limpiar_campos(self.boton_Prod_Serv, ventana, "3", tipo))
                else:
                    self.boton_Company.config(text="AGREGAR OTRA COMPAÑIA", state=NORMAL, relief="raised",
                                              command=lambda: self.limpiar_campos(self.boton_Company, ventana, "1",
                                                                                  tipo))
            else:
                if tipo == "p":
                    messagebox.showwarning("Advertencia",
                                           f"El Producto ya existe para {self.compania_seleccionada}, por favor ingrese otro Producto.",
                                           parent=ventana)

                else:
                    messagebox.showwarning("Advertencia",
                                           f"El Servicio ya existe para {self.compania_seleccionada}, por favor ingrese otro Servicio.",
                                           parent=ventana)
                    return

    def limpiar_campos(self, boton, ventana, selected, tipo):
        datos = {}
        canal_combobox = None
        if selected == "1":
            for widget in self.agregarCompanyFrame.winfo_children():
                widget.config(state="normal")
            agregar = self.agregarCompanyBoton
            datos = self.datos_ingresados_agregar
            boton.config(text="SIGUIENTE", state=NORMAL, relief="raised", command=lambda: agregar(ventana, selected))
            canal_combobox = self.datos_ingresados_agregar.get("CanalT")

        if selected == "3":
            self.combo.configure(state="readonly")
            self.combo_var.set('')
            agregar = self.agregarProductoServicioBoton
            datos = self.datos_ingresados_agregar_Producto if tipo == "p" else self.datos_ingresados_agregar_Servicio
            boton.config(text="SIGUIENTE", state=NORMAL, relief="raised", command=lambda: agregar(ventana, selected))

        #Widgets general "GUARDAR", siempre ejecutar
        if selected == "2":
            agregar = self.agregarProductoServicioBoton
            datos = self.datos_ingresados_agregar_Producto if tipo == "p" else self.datos_ingresados_agregar_Servicio

        for widget in datos.values():
            if isinstance(widget, Entry):
                widget.delete(0, 'end')
            elif isinstance(widget, tkinter.ttk.Combobox):
                widget.set('')
        if canal_combobox:
            canal_combobox.set('')



#_____ Agregar valores en las Tablas si existen los valores
    def agregar_nuevo_Producto_Servicio(self, tabla, columna, valor, tipo, ventana):
        datos_ingresados_agregar = self.datos_ingresados_agregar_Producto if tipo == "p" else self.datos_ingresados_agregar_Servicio

        if tabla != "CompanyT":
            consulta = f"INSERT INTO {tabla} ({columna}) VALUES (?)"
            parametros = (valor,)
            self. consultas_y_modificacion_SQL(consulta, parametros, "3", ventana)

        # Actualizar combobox si es necesario
        if isinstance(datos_ingresados_agregar[tabla], tkinter.ttk.Combobox):
            self.actualizar_combobox(tabla, columna, datos_ingresados_agregar[tabla], ventana)


# --------------------- # --------------------- # --------------------- # --------------------- # ---------------------

#_____ ACTUALIZAR CON VALORES DE TABLA Y COLUMNA Y GUARDARLO EN EL COMBOX
    def actualizar_combobox(self,tabla, columna, widget, ventana):
        consulta = f"SELECT {columna} FROM {tabla}"
        parametros = "1"
        rows = self.consultas_y_modificacion_SQL(consulta, parametros, "1", ventana)
        v = [row[0] for row in rows]
        widget['values'] = v



    # ------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------

    #------------------------------ CREA LAS LISTA --------------------------------------#

        # ------------------------------------------------------------#
                        # CREACION DE LISTA DE PRODUCTOS #
        # ------------------------------------------------------------#

    def prod(self):

        if self.servFrame and self.servFrame.winfo_exists():
            if self.servFrame.winfo_ismapped():
                self.servFrame.destroy()
            self.servFrame.destroy()
            if self.datos_entry != {}:
                self.datos_entry = {}
            self.servFrame = None

        if self.crearProvFrame and self.crearProvFrame.winfo_exists():
            if self.crearProvFrame.winfo_ismapped():
                self.crearProvFrame.destroy()
            self.crearProvFrame.destroy()
            if self.datos_entry != {}:
                self.datos_entry = {}
            self.crearProvFrame = None

        self.prodFrame=Frame(self.provFrame1, bg=self.grey_Font)
        self.prodFrame.place(x=0, y=0, relheight=1, relwidth=1)
        self.botonProd.config(state=DISABLED, relief="sunken")
        self.botonServ.config(state=NORMAL, relief="raised")
        self.botonAgregar.config(state=NORMAL, relief="raised")

        # CONFIGURAR EL FRAME CON SU ETIQUETA, LISTA, SCRROL Y EL CUADRO DE TEXTO #

        #Dimension en X = 217 (label, listbox, scroll, entry)
        #Dimension en Y = 217 (label, listbox, scroll, entry)
        # ---------------------------------------------------------------------------------------
        # (Frame, titutlo_de_las_Tablas, posicion_x, posicion_y, columna_en_SQL, tabla_en_SQL)
        # ---------------------------------------------------------------------------------------
        self.seleccion = "p"
        # Crear Widges
        self.crearNuevosWidgets(self.prodFrame)

        # Crear Boton busqueda
        self.createButtonShare(self.prodFrame)


        # ------------------------------------------------------------#
                        # CREACION DE LISTA DE SERVICIOS #
        # ------------------------------------------------------------#


    def serv(self):
        if self.prodFrame and self.prodFrame.winfo_exists():
            if self.prodFrame.winfo_ismapped():
                self.prodFrame.destroy()
            self.prodFrame.destroy()
            if self.datos_entry != {}:
                self.datos_entry = {}
            self.prodFrame = None

        if self.crearProvFrame and self.crearProvFrame.winfo_exists():
            if self.crearProvFrame.winfo_ismapped():
                self.crearProvFrame.destroy()
            self.crearProvFrame.destroy()
            if self.datos_entry != {}:
                self.datos_entry = {}
            self.crearProvFrame = None

        self.servFrame=Frame(self.provFrame1, bg=self.grey_Font)
        self.servFrame.place(x=0, y=0, relheight=1, relwidth=1)
        self.botonProd.config(state=NORMAL, relief="raised")
        self.botonServ.config(state=DISABLED, relief="sunken")
        self.botonAgregar.config(state=NORMAL, relief="raised")

        # ---------------------------------------------------------------------------------------
        # (Frame, titutlo_de_las_Tablas, posicion_x, posicion_y, columna_en_SQL, tabla_en_SQL)
        # ---------------------------------------------------------------------------------------
        self.seleccion = "s"
        # Crear Widges
        self.crearNuevosWidgets(self.servFrame)

        # Crear Boton busqueda
        self.createButtonShare(self.servFrame)



# ------------------------ CREA BOTON DE BUSQUEDA E INICIAR EL TREEVIEW------------------------------------------------#
    def buscarBoton(self):

        # Crear la ventana de búsqueda
        self.ventana_busqueda = Toplevel(self)
        self.ventana_busqueda.title("Búsqueda Servicio" if self.seleccion == "s" else "Búsqueda Producto")
        self.ventana_busqueda.wm_iconbitmap(self.icon)

        self.menu = Menu(self.ventana_busqueda)
        self.ventana_busqueda.config(menu=self.menu)

        self.menu_opciones_Prod_Serv = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Opciones", menu=self.menu_opciones_Prod_Serv)

        if self.menu_opciones_Prod_Serv:
            self.menu_opciones_Prod_Serv.delete(0, "end")

        if self.seleccion == "p":
            self.menu_opciones_Prod_Serv.add_command(label="Agregar Producto o Servicio", command=lambda: self.funcion_agregar_Prod_Serv("p"))
            self.menu_opciones_Prod_Serv.add_command(label="Eliminar Producto o Servicio",  command=lambda: self.funcion_eliminar_Prod_Serv("p"))
            self.menu_opciones_Prod_Serv.add_command(label="Eliminar Compañia", command=lambda: self.funcion_eliminar_Company())

        else:
            self.menu_opciones_Prod_Serv.add_command(label="Agregar Producto o Servicio", command=lambda: self.funcion_agregar_Prod_Serv("s"))
            self.menu_opciones_Prod_Serv.add_command(label="Eliminar Producto o Servicio", command=lambda: self.funcion_eliminar_Prod_Serv("s"))
            self.menu_opciones_Prod_Serv.add_command(label="Eliminar Compañia", command=lambda: self.funcion_eliminar_Company())

        w = 1340
        h = 730

        self.dimension_ventana(w, h, self.ventana_busqueda)


        # Función para cerrar la ventana con la tecla Control "+" W
        def cerrarVentana(event):
            self.ventana_busqueda.destroy()
            self.actualizarDespuesDeCerrarBusqueda()

        self.ventana_busqueda.bind("<Control-w>", cerrarVentana)
        self.ventana_busqueda.bind("<Control-W>", cerrarVentana)

        # Crear un frame dentro de la ventana
        self.frame_busqueda = Frame(self.ventana_busqueda)
        self.frame_busqueda.place(x=0, y=0, relheight=1, relwidth=1)

        # Mostrar la ventana de búsqueda centrada en la pantalla con zoom en cuenta

        # Crear el Treeview y otros elementos necesarios
        self.createTreeview()
        self.ventana_busqueda.protocol("WM_DELETE_WINDOW", self.actualizarDespuesDeCerrarBusqueda)
        # Mostrar la ventana de búsqueda
        self.ventana_busqueda.mainloop()


    def actualizarDespuesDeCerrarBusqueda(self):
        self.ventana_busqueda.destroy()

        # Eliminar los widgets anteriores en función de la selección
        if self.seleccion == "p":
            self.eliminarWidgets(self.prodFrame)
        else:
            self.eliminarWidgets(self.servFrame)

        # Realizar las actualizaciones necesarias en los widgets aquí
        if self.seleccion == "p":
            self.crearNuevosWidgets(self.prodFrame)
            self.createButtonShare(self.prodFrame)
        else:
            self.crearNuevosWidgets(self.servFrame)
            self.createButtonShare(self.servFrame)

        # Limpiar los valores de los Entry
        self.limpiarValoresEntry()

    def limpiarValoresEntry(self):
        for tabla in self.datos_entry:
            self.datos_entry[tabla] = ""


    def eliminarWidgets(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()


    def crearNuevosWidgets(self, frame):
        # Agregar 8 veces la función createWidgetG
        self.createWidgetG(frame, "COMPAÑIA", 122, 100, "Company", "CompanyT")
        self.createWidgetG(frame, "CANAL", 355, 100, "Canal", "CanalT")
        self.createWidgetG(frame, "PAIS", 588, 100, "Pais", "PaisT")
        self.createWidgetG(frame, "CIUDAD", 821, 100, "Ciudad", "CiudadT")
        if self.seleccion == "p":
            # Crear las siguientes 4 tablas en la segunda fila
            self.createWidgetG(frame, "PRODUCTO", 122, 355, "Tipo", "TipoProductoT")
            self.createWidgetG(frame, "GRADO", 355, 355, "Grado", "GradoT")
            self.createWidgetG(frame, "TRATAMIENTO", 588, 355, "Tratamiento", "TratamientoTT")
            self.createWidgetG(frame, "NORMA", 821, 355, "Norma", "NormaPT")

        else:
            self.createWidgetG(frame, "SERVICIO", 355, 355, "Tipo", "TipoServicioT")
            self.createWidgetG(frame, "NORMA", 588, 355, "Norma", "NormaST")



# --------------------------- INICIO PARA CREAR EL TREEVIEW EN UNA VENTANA NUEVA -----------------------------------------------------------

    def createTreeview(self):

        self.tituloTablas = {
            'Producto': [ 'CANAL', 'PAIS', 'CIUDAD', 'TIPO', 'GRADO', 'TRAT. T.', 'NORMA'],
            'Servicio': [ 'CANAL', 'PAIS', 'CIUDAD', 'TIPO', 'NORMA']}

        self.tituloTablasSQL={
            'Producto': ['Company', 'Canal', 'Pais', 'Ciudad', 'Tipo', 'Grado', 'Tratamiento', 'Norma'],
            'Servicio': ['Company', 'Canal', 'Pais', 'Ciudad', 'Tipo', 'Norma']}

        if self.seleccion == "p":
            tabla_variable = 'Producto'
        else:
            tabla_variable = 'Servicio'

        self.compania_seleccionada = None

        self.nuevo_diccionario = {}

        # ---------------------------------- INICIO DE LA FILTRO DE BUSQUEDA, TREEVIEW ---------------------------------------------------#

        # ------------------------------------------------------------------------------------------

        # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

        if self.seleccion == "s":
            anchos_columnas = {
                'CANAL': 100,
                'PAIS': 100,
                'CIUDAD': 80,
                'TIPO': 250,
                'NORMA': 55}

            for clave, valor in self.datos_entry.items():
                if valor:  # Verificar si el valor no está vacío
                    if clave == "CompanyT":
                        nueva_clave = "CompanyT.Company"
                    elif clave == "CanalT":
                        nueva_clave = "CompanyT.Canal"
                    elif clave == "PaisT":
                        nueva_clave = "CompanyT.Pais"
                    elif clave == "CiudadT":
                        nueva_clave = "CompanyT.Ciudad"
                    elif clave == "TipoServicioT":
                        nueva_clave = "ProvServiciosT.Tipo"
                    elif clave == "NormaST":
                        nueva_clave = "ProvServiciosT.Norma"
                    else:
                        nueva_clave = clave

                    self.nuevo_diccionario[nueva_clave] = valor
        else:
            anchos_columnas = {
                'CANAL': 120,
                'PAIS': 150,
                'CIUDAD': 150,
                'TIPO': 300,
                'GRADO': 100,
                'TRAT. T.': 100,
                'NORMA': 100}

            for clave, valor in self.datos_entry.items():
                if valor:  # Verificar si el valor no está vacío
                    if clave == "CompanyT":
                        nueva_clave = "CompanyT.Company"
                    elif clave == "CanalT":
                        nueva_clave = "CompanyT.Canal"
                    elif clave == "PaisT":
                        nueva_clave = "CompanyT.Pais"
                    elif clave == "CiudadT":
                        nueva_clave = "CompanyT.Ciudad"
                    elif clave == "TipoProductoT":
                        nueva_clave = "ProvProductosT.Tipo"
                    elif clave == "GradoT":
                        nueva_clave = "ProvProductosT.Grado"
                    elif clave == "TratamientoTT":
                        nueva_clave = "ProvProductosT.Tratamiento"
                    elif clave == "NormaPT":
                        nueva_clave = "ProvProductosT.Norma"
                    else:
                        nueva_clave = clave

                    self.nuevo_diccionario[nueva_clave] = valor

        # -------- Pone el titulo de las TABLAS en la variable Columna
        columnas = self.tituloTablas.get(tabla_variable, [])
        self.treeview = tkinter.ttk.Treeview(self.frame_busqueda, columns=columnas)

        # Establecer el encabezado de la columna #0 con el nombre "COMPAÑIA"
        self.treeview.heading('#0', text='COMPAÑIA')
        self.treeview.column('#0', width=300)


        # Configurar las dimensiones de columnas y encabezado
        for columna in columnas:
            if columna == 'COMPAÑIA':
                continue  # Saltar la configuración de la columna "COMPAÑIA" en el bucle inicial

            ancho_columna = anchos_columnas.get(columna, 200)  # Ancho predeterminado: 200
            self.treeview.heading(columna, text=columna)
            self.treeview.column(columna, width=ancho_columna, anchor=tkinter.CENTER)

        # ---- Configurar la fuente
        self.estilo_treeview = tkinter.ttk.Style()

        if self.seleccion == "s":
            consulta = f"SELECT CompanyT.Company, CompanyT.Canal, CompanyT.Pais, CompanyT.Ciudad, ProvServiciosT.Tipo, ProvServiciosT.Norma " \
                   f"FROM CompanyT " \
                   f"JOIN ProvServiciosT ON CompanyT.Company = ProvServiciosT.Company"
        else:
            consulta = f"SELECT CompanyT.Company, CompanyT.Canal, CompanyT.Pais, CompanyT.Ciudad, ProvProductosT.Tipo, ProvProductosT.Grado, ProvProductosT.Tratamiento, ProvProductosT.Norma " \
                       f"FROM CompanyT " \
                       f"JOIN ProvProductosT ON CompanyT.Company = ProvProductosT.Company"

        parametros = []  # Declarar la variable 'valores' como una lista vacía

        if self.nuevo_diccionario:
            consulta += " WHERE "

            condiciones = []
            for clave, valor in self.nuevo_diccionario.items():
                condicion = f"{clave} LIKE ?"  # Sin los comodines % en el valor
                condiciones.append(condicion)
                parametros.append(f"%{valor}%")  # Agregar los comodines % aquí

            consulta += " AND ".join(condiciones)

        if self.nuevo_diccionario:
            resultados = self.consultas_y_modificacion_SQL(consulta, parametros, "1", self.ventana_busqueda)
        else:
            parametros = "1"
            resultados = self.consultas_y_modificacion_SQL(consulta, parametros, "1", self.ventana_busqueda)

        self.estilo_treeview.configure("Treeview.Heading", font=("Arial", 15, "bold"))  # Titulos
        self.treeview.tag_configure("mytag", font=("Arial", 13))  # Columna primaria
        self.treeview.tag_configure("mytag2", font=("Arial", 11))  # Columna secundaria

        # Crear un diccionario para almacenar los elementos secundarios por valor de "CompanyT.Company"
        elementos_secundarios = {}

        for resultado in resultados:
            company = resultado[0]
            valores_filtrados = [valor if valor is not None else "" for valor in resultado[1:]] # Si el valor es None, deja el campo vacio

            if company not in elementos_secundarios:
                # Si es la primera vez que se encuentra el valor de "CompanyT.Company", se crea el elemento de nivel 1
                item1 = self.treeview.insert("", "end", text=company, values=valores_filtrados)
                elementos_secundarios[company] = item1
                separator = "-" * 25  # Ajusta el número de guiones según el ancho deseado
                self.treeview.insert("", "end", text=separator, tags=("separator",))

            else:
                # Si el valor ya existe, se inserta como elemento secundario en la columna "COMPAÑIA"
                item2 = self.treeview.insert(elementos_secundarios[company], "end", values=valores_filtrados)


        self.treeview.bind("<Double-1>", self.manejar_doble_clic)

        self.treeview.pack(fill='both', expand=True)

        def on_treeview_select(event):
            seleccion = self.treeview.selection()
            if seleccion:
                item = seleccion[0]  # Obtén el primer elemento seleccionado
                item_id = self.treeview.focus()
                text = self.treeview.item(item_id, "text")

                # Verifica si el elemento seleccionado es un separador
                if text == "-" * 25:
                    self.compania_seleccionada = None
                else:
                    tags = self.treeview.item(item_id, "tags")
                    if "mytag" in tags:
                        # El elemento seleccionado es un padre
                        company_value = self.treeview.item(item_id, "text")
                        self.compania_seleccionada = company_value
                    else:
                        # El elemento seleccionado es un hijo
                        parent_item_id = self.treeview.parent(item_id)
                        company_value = self.treeview.item(parent_item_id, "text")
                        self.compania_seleccionada = company_value

                    # Obtener todos los datos de la fila seleccionada
                    values = self.treeview.item(item_id)['values']

                    # Resto del código para procesar los datos...

                    # Crear el diccionario con las claves modificadas
                    self.datos_fila_eliminar_original = dict(zip(self.treeview['columns'], values))
                    self.datos_fila_eliminar_nueva_clave = self.cambiar_claves(self.datos_fila_eliminar_original)

                    # Crear una lista con las claves permitidas
                    claves_permitidas_Prod = ['Tipo', 'Grado', 'Tratamiento', 'Norma']
                    claves_permitidas_Serv = ['Tipo', 'Norma']
                    claves_permitidas_Company = ['Canal', 'Pais', 'Ciudad']

                    claves_permitidas = claves_permitidas_Prod if self.seleccion == "p" else claves_permitidas_Serv

                    # Crear un nuevo diccionario solo con las claves permitidas y sus correspondientes valores
                    self.datos_fila_eliminar_Prod_Serv = {clave: valor for clave, valor in
                                                          self.datos_fila_eliminar_nueva_clave.items() if
                                                          clave in claves_permitidas}
                    # Crear un nuevo diccionario solo con las claves permitidas y sus correspondientes valores
                    self.datos_fila_eliminar_Company = {clave: valor for clave, valor in
                                                        self.datos_fila_eliminar_nueva_clave.items() if
                                                        clave in claves_permitidas_Company}

            self.treeview.bind("<Delete>", self.funcion_eliminar_Prod_Serv)

        self.treeview.bind("<<TreeviewSelect>>", on_treeview_select)

        # ----------- CONFIGURACION DE TAMAÑO DE LETRA Y FUENTE --------------
        for item in self.treeview.get_children():
            self.treeview.item(item, tags="mytag")
            for child_item in self.treeview.get_children(item):
                self.treeview.item(child_item, tags="mytag2")

# ---------""""-------------------------------%%%%%%%%-----------------------""""----------- #


                    # FUNCIONES PARA CREAR PESTAÑA DE DATOS DEL PROVEEDOR

# ---------""""-------------------------------%%%%%%%%-----------------------""""----------- #

# ------------------------------------------------------------------------------------------

             # FUNCION ABRIR LOS CAMPOS DEL TREEVIEW

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


             # FUNCION PARA UTILIZAR DOBLE CLICL, GUARDAR COMPAÑIA Y ABRIR UNA VENTANA NUEVA CON LOS DATOS

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

    def manejar_doble_clic(self, event):
        self.treeview = event.widget
        item = self.treeview.identify("item", event.x, event.y)
        if item:
            valores = self.treeview.item(item, "values")
            if valores:
                self.abrir_ventana()
        return "break"

# ------------------------------------------------------------------------------------------
    # Se cambian las claves de las columnas del treeview por las columnas de SQL
    def cambiar_claves(self, diccionario_original):
        if self.seleccion == "p":
            claves_modificadas = {
                'CANAL': 'Canal',
                'PAIS': 'Pais',
                'CIUDAD': 'Ciudad',
                'TIPO': 'Tipo',
                'GRADO': 'Grado',
                'TRAT. T.': 'Tratamiento',
                'NORMA': 'Norma'
            }
        else:
            claves_modificadas = {
                'CANAL': 'Canal',
                'PAIS': 'Pais',
                'CIUDAD': 'Ciudad',
                'TIPO': 'Tipo',
                'NORMA': 'Norma'
            }

        diccionario_modificado = {}
        for clave, valor in diccionario_original.items():
            nueva_clave = claves_modificadas.get(clave, clave)
            diccionario_modificado[nueva_clave] = valor

        return diccionario_modificado


    # Luego, en tu función on_treeview_select, puedes utilizar esta función para obtener el diccionario con las claves modificadas:

    def on_treeview_select(self, event):
        # Obtener el identificador del elemento seleccionado
        item_id = self.treeview.focus()
        tags = self.treeview.item(item_id, "tags")

        values = self.treeview.item(item_id, "values")
        if values and values[0] == "-" * 25:
            self.compania_seleccionada = None

        else:
            values = self.treeview.item(item_id, "values")
            if values:
                if "mytag" in tags:
                    # El elemento seleccionado es un padre
                    company_value = self.treeview.item(item_id, "text")
                    self.compania_seleccionada = company_value

                else:
                    # El elemento seleccionado es un hijo
                    parent_item_id = self.treeview.parent(item_id)
                    company_value = self.treeview.item(parent_item_id, "text")
                    self.compania_seleccionada = company_value

                # Obtener todos los datos de la fila seleccionada
                values = self.treeview.item(item_id)['values']

                # Crear el diccionario con las claves modificadas
                self.datos_fila_eliminar_original = dict(zip(self.treeview['columns'], values))
                self.datos_fila_eliminar_nueva_clave = self.cambiar_claves(self.datos_fila_eliminar_original)

                # Crear una lista con las claves permitidas
                claves_permitidas_Prod = ['Tipo', 'Grado', 'Tratamiento', 'Norma']
                claves_permitidas_Serv = ['Tipo', 'Norma']
                claves_permitidas_Company = ['Canal', 'Pais', 'Ciudad']

                claves_permitidas = claves_permitidas_Prod if self.seleccion == "p" else claves_permitidas_Serv

                # Crear un nuevo diccionario solo con las claves permitidas y sus correspondientes valores
                self.datos_fila_eliminar_Prod_Serv = {clave: valor for clave, valor in self.datos_fila_eliminar_nueva_clave.items() if clave in claves_permitidas}

                # Crear un nuevo diccionario solo con las claves permitidas y sus correspondientes valores
                self.datos_fila_eliminar_Company = {clave: valor for clave, valor in self.datos_fila_eliminar_nueva_clave.items() if clave in claves_permitidas_Company}


                self.treeview.bind("<Delete>", self.funcion_eliminar_Prod_Serv)


# ---------------------------- FUNCION PARA VERIFICAR Y ELIMINAR EL INDICE DEL MENU

    def verificar_y_eliminar_opcion(self, nombre_opcion):
        if self.menu_opciones and self.menu_opciones.index(END) != '':
            self.menu_opciones.delete(0, END)
# ------------------------------------------------------------------------------------------

                    # CREAR NUEVA VENTANA CON LOS DATOS PARA PRODUCTO

# ------------------------------------------------------------------------------------------

    def abrir_ventana(self):

        self.itemTreeview = self.treeview.focus()
        self.valoresTreeview = self.treeview.item(self.itemTreeview, "text")

        if self.valoresTreeview:

            # Consulta para crear botones si hay mas de 1 Compañia
            consulta = "SELECT * FROM ProvDatosT WHERE Company = ?;"
            parametros = (self.compania_seleccionada,)

            self.resultadosDatosProv = self.consultas_y_modificacion_SQL(consulta, parametros, "1",
                                                                         self.ventana_detalle)
            # SI NO HAY UN DATO DEL PROVEEDOR
            if len(self.resultadosDatosProv) == 0:
                self.funcion_agregar_datos_Prov(self.ventana_busqueda)

                if self.ventana_detalle:
                    self.ventana_detalle.destroy()


            else:
                self.compania_seleccionada = self.valoresTreeview

                # Cerrar la ventana de detalles anterior si existe
                if self.ventana_detalle:
                    self.ventana_detalle.destroy()

                # Crear una nueva ventana
                self.ventana_detalle = Toplevel(self.ventana_busqueda)
                self.ventana_detalle.title("Datos del Proveedor - " + self.compania_seleccionada)
                self.ventana_detalle.wm_iconbitmap(self.icon)

                # ---------- Crea el menu
                self.menu_desplegable = Menu(self.ventana_detalle)
                self.ventana_detalle.config(menu=self.menu_desplegable)

                self.menu_opciones = Menu(self.menu_desplegable, tearoff=0)
                self.menu_desplegable.add_cascade(label="Opciones", menu=self.menu_opciones)

                if self.menu_opciones:
                    self.menu_opciones.delete(0, "end")

                def cerrarVentana(event):
                    self.ventana_detalle.destroy()


                self.ventana_detalle.bind("<Control-w>", cerrarVentana)
                self.ventana_detalle.bind("<Control-W>", cerrarVentana)

                width = 700
                height = 450

                self.dimension_ventana(width,height,self.ventana_detalle)

                self.botones_detalle = []

            # --- SI HAY MAS DE 1 DATO DE PROVEEDORES

                if len(self.resultadosDatosProv) > 1:
                    self.verificar_y_eliminar_opcion("Agregar Contacto")
                    self.verificar_y_eliminar_opcion("Modificar Contacto")
                    self.verificar_y_eliminar_opcion("Eliminar Contacto")

                    self.menu_opciones.add_command(label="Agregar Contacto", command=lambda vent=self.ventana_detalle: self.funcion_agregar_datos_Prov(vent))

                    for resultado in self.resultadosDatosProv:
                        valor = resultado[2]
                        valor2 = resultado[1]

                        boton_detalle = Button(self.ventana_detalle, text=valor + " - " + valor2, command=lambda div=valor, name=valor2: self.crear_nuevo_frame(div, name))
                        self.botones_detalle.append(boton_detalle)

                    for boton in self.botones_detalle:
                        boton.config(font=22)
                        boton.place(x=10, y=1 * (len(self.botones_detalle) + 1) + 50 * self.botones_detalle.index(boton),relwidth=.97)  # Ajusta 'x', 'y' y 'width' según tus necesidades

            # --- SI HAY 1 DATO DE PROVEEDOR

                elif len(self.resultadosDatosProv) == 1:

                    self.verificar_y_eliminar_opcion("Agregar Contacto")
                    self.verificar_y_eliminar_opcion("Modificar Contacto")
                    self.verificar_y_eliminar_opcion("Eliminar Contacto")

                    self.menu_opciones.add_command(label="Agregar Contacto", command=lambda vent=self.ventana_detalle: self.funcion_agregar_datos_Prov(vent))
                    self.menu_opciones.add_command(label="Modificar Contacto", command=self.funcion_modificar_datos_Prov)
                    self.menu_opciones.add_command(label="Eliminar Contacto", command=self.funcion_eliminar_datos_Prov)

                    consulta = "SELECT Nombre, Division, Cargo, Correo, Telefono, Web, LineaC, LimiteC, FechaR FROM ProvDatosT WHERE Company = ?;"
                    parametros = (self.compania_seleccionada,)
                    resultados = self.consultas_y_modificacion_SQL(consulta, parametros, "1", self.ventana_detalle)

                    etiquetas = ["Nombre", "División", "Cargo", "Correo", "Teléfono", "Página Web", "Linea de Credito", "Limite de Credito", "Fecha de Registro"]

                    for valor in self.resultadosDatosProv:
                        self.valor_tercera_columna = valor[2]
                        self.valor_segunda_columna = valor[1]

                    for i in range(len(etiquetas)):
                        etiqueta = etiquetas[i]
                        valor = resultados[0][i]

                        if etiqueta == "Correo":
                            if valor != "":
                                label_etiqueta = Label(self.ventana_detalle, text=etiqueta + ":", font=("Arial", 18))
                                label_etiqueta.place(x=10, y=50 * i, width=225)

                                texto = "PRESIONE PARA CREAR UN CORREO"

                                def copiar_correo(valor):
                                    self.master.clipboard_clear()
                                    self.master.clipboard_append(valor.lower())
                                    subprocess.run(["start", "mailto:" + valor.lower()], shell=True)

                                boton_correo = Button(self.ventana_detalle, text=texto, font=("Arial", 16), relief="raised",
                                                         command=lambda v=valor: copiar_correo(v))
                                boton_correo.place(x=230, y=49 * i, width=460)

                            else:
                                texto = "AGREGUE UN CORREO"
                                label_etiqueta = Label(self.ventana_detalle, text=etiqueta + ":", font=("Arial", 16))
                                label_etiqueta.place(x=10, y=50 * i, width=225)

                                boton_web = Button(self.ventana_detalle, text=texto, font=("Arial", 16), state=DISABLED, relief="sunken")
                                boton_web.place(x=230, y=49 * i, width=460)

                        elif etiqueta == "Página Web":
                            if valor != "":
                                texto = "PRESIONE PARA ABRIR LA PAGINA WEB"
                                label_etiqueta = Label(self.ventana_detalle, text=etiqueta + ":", font=("Arial", 18))
                                label_etiqueta.place(x=10, y=50 * i, width=225)

                                boton_web = Button(self.ventana_detalle, text=texto, font=("Arial", 16), relief="raised",
                                                   command=lambda v=valor: self.abrir_pagina_web(v))
                                boton_web.place(x=230, y=49 * i, width=460)

                            else:
                                texto = "AGREGUE UNA PAGINA WEB"
                                label_etiqueta = Label(self.ventana_detalle, text=etiqueta + ":", font=("Arial", 18))
                                label_etiqueta.place(x=10, y=50 * i, width=225)

                                boton_web = Button(self.ventana_detalle, text=texto, font=("Arial", 16), state=DISABLED, relief="sunken")
                                boton_web.place(x=230, y=49 * i, width=460)


                        else:

                            label_etiqueta = Label(self.ventana_detalle, text=etiqueta + ":", font=("Arial", 18))
                            label_etiqueta.place(x=10, y=50 * i, width=225)

                            label_valor = Label(self.ventana_detalle, text=valor, font=("Arial", 18))
                            label_valor.place(x=230, y=49 * i, width=460)




# ********************** EVENTO CON LA TECLA CRTL DEL TECLADO **********************


    def volver_acrear_botones(self, event):
        self.destruir_frame()
        self.mostrar_botones()

# ------------------------------------------------------------------------------------------

             # FUNCION PARA DESTRUIR LOS FRAME DE LA VENTANA DE DATOS DE PROVEEDOR

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

    def destruir_frame(self):
        if self.ventana_detalle_frame:
            self.ventana_detalle_frame.destroy()
            self.ventana_detalle_frame = None

# ------------------------------------------------------------------------------------------

             # FUNCION PARA MOSTRAR LOS BOTONES DESPUES DE UTILIZAR CTRL

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

    def mostrar_botones(self):
        for boton in self.botones_detalle:
            boton.destroy()

        self.botones_detalle = []
        width = 700
        height = 450

        self.dimension_ventana(width, height, self.ventana_detalle)

        if self.ventana_detalle:
            if len(self.resultadosDatosProv) > 1:
                self.verificar_y_eliminar_opcion("Agregar Contacto")
                self.verificar_y_eliminar_opcion("Modificar Contacto")
                self.verificar_y_eliminar_opcion("Eliminar Contacto")

                self.menu_opciones.add_command(label="Agregar Contacto", command=lambda vent=self.ventana_detalle: self.funcion_agregar_datos_Prov(vent))

                for resultado in self.resultadosDatosProv:
                    valor = resultado[2]  # Obtener el valor relevante para el botón (en este caso, la tercera columna)
                    valor2 = resultado[1]
                    self.valor_tercera_columna = resultado[2]
                    self.valor_segunda_columna = resultado[1]

                    # Crear el botón con el valor obtenido
                    boton_detalle = Button(self.ventana_detalle, text=valor + " - " + valor2,
                                           command=lambda div=valor, name=valor2: self.crear_nuevo_frame(div, name))
                    self.botones_detalle.append(boton_detalle)

            for boton in self.botones_detalle:
                boton.config(font=22)
                boton.place(x=10, y=1 * (len(self.botones_detalle) + 1) + 50 * self.botones_detalle.index(boton),
                            relwidth=.97)  # Ajusta 'x', 'y' y 'width' según tus necesidades

# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&---------------&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

             # FUNCION PARA ELIMINAR LOS BOTONES CUANDO SE PRECIONA

# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&---------------&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&


    def destruir_botones(self):
        if self.ventana_detalle:
            for boton in self.botones_detalle:
                boton.destroy()
            #self.destruir_frame()

# *************************************************************************************

             # FUNCION PARA MOSTRAR LOS DATOS DE NUEVO SI HABIA BOTONES

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


    def crear_nuevo_frame(self,division, name):
        self.verificar_y_eliminar_opcion("Agregar Contacto")
        self.verificar_y_eliminar_opcion("Modificar Contacto")
        self.verificar_y_eliminar_opcion("Eliminar Contacto")

        self.menu_opciones.add_command(label="Modificar Contacto", command=self.funcion_modificar_datos_Prov)
        self.menu_opciones.add_command(label="Eliminar Contacto", command=self.funcion_eliminar_datos_Prov)
        self.valor_tercera_columna = division
        self.valor_segunda_columna = name


# ------------- CREA DE NUEVO VENTANA DE DATOS DE PROVEEDORES PARA PRODUCTO -------------------------------------------------------------------------------------
        if self.seleccion in ["p", "s"]:
            width = 700
            height = 450

            self.dimension_ventana(width,height,self.ventana_detalle)

            self.ventana_detalle_frame = Frame(self.ventana_detalle)
            self.ventana_detalle_frame.place(x=0, y=0, relwidth=1, relheight=1)

            self.destruir_botones()

            # Consulta para obtener los valores de los labels filtrados por división
            consulta = "SELECT Nombre, Division, Cargo, Correo, Telefono, Web, LineaC, LimiteC, FechaR FROM ProvDatosT WHERE Company = ? AND Division = ? AND Nombre = ?;"
            parametros = (self.compania_seleccionada, division, name)
            resultados = self.consultas_y_modificacion_SQL(consulta, parametros, "1", self.ventana_detalle)

            if len(resultados) > 0:
                # Crear los labels con los datos obtenidos de la consulta
                etiquetas = ["Nombre", "División", "Cargo", "Correo", "Teléfono", "Página Web", "Linea de Credito",
                             "Limite de Credito", "Fecha de Registro"]

                for i in range(len(etiquetas)):
                    etiqueta = etiquetas[i]
                    valor = resultados[0][i]

                    if etiqueta == "Correo":
                        if valor != "":
                            label_etiqueta = Label(self.ventana_detalle_frame, text=etiqueta + ":", font=("Arial", 18))
                            label_etiqueta.place(x=10, y=50 * i, width=225)

                            texto = "PRESIONE PARA CREAR UN CORREO"

                            def copiar_correo(valor):
                                self.master.clipboard_clear()
                                self.master.clipboard_append(valor.lower())
                                subprocess.run(["start", "mailto:" + valor.lower()], shell=True)

                            boton_correo = Button(self.ventana_detalle_frame, text=texto, font=("Arial", 16), relief="raised",
                                                  command=lambda v=valor: copiar_correo(v))
                            boton_correo.place(x=230, y=49 * i, width=460)

                        else:
                            texto = "AGREGUE UN CORREO"
                            label_etiqueta = Label(self.ventana_detalle_frame, text=etiqueta + ":", font=("Arial", 16))
                            label_etiqueta.place(x=10, y=50 * i, width=225)

                            boton_web = Button(self.ventana_detalle_frame, text=texto, font=("Arial", 16), state=DISABLED,
                                               relief="sunken")
                            boton_web.place(x=230, y=49 * i, width=460)

                    elif etiqueta == "Página Web":
                        if valor != "":
                            texto = "PRESIONE PARA ABRIR LA PAGINA WEB"
                            label_etiqueta = Label(self.ventana_detalle_frame, text=etiqueta + ":", font=("Arial", 18))
                            label_etiqueta.place(x=10, y=50 * i, width=225)

                            boton_web = Button(self.ventana_detalle_frame, text=texto, font=("Arial", 16), relief="raised",
                                               command=lambda v=valor: self.abrir_pagina_web(v))
                            boton_web.place(x=230, y=49 * i, width=460)

                        else:
                            texto = "AGREGUE UNA PAGINA WEB"
                            label_etiqueta = Label(self.ventana_detalle_frame, text=etiqueta + ":", font=("Arial", 18))
                            label_etiqueta.place(x=10, y=50 * i, width=225)

                            boton_web = Button(self.ventana_detalle_frame, text=texto, font=("Arial", 16), state=DISABLED, relief="sunken")
                            boton_web.place(x=230, y=49 * i, width=460)

                    else:

                        label_etiqueta = Label(self.ventana_detalle_frame, text=etiqueta + ":", font=("Arial", 18))
                        label_etiqueta.place(x=10, y=50 * i, width=225)

                        label_valor = Label(self.ventana_detalle_frame, text=valor, font=("Arial", 18))
                        label_valor.place(x=230, y=49 * i, width=460)

            self.ventana_detalle.bind("<Escape>", self.volver_acrear_botones)
        

    def abrir_pagina_web(self, url):
        if url is not None:
            try:
                selected_browser = webbrowser.get()
                selected_browser.open(url.lower(), new=2)
            except webbrowser.Error:
                messagebox.showerror("Error", "No se puede abrir la Página Web.", parent=self.ventana_detalle)

# *************************************************************************************

             # FUNCION PARA MOSTRAR LOS DATOS DE NUEVO SI HABIA BOTONES

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

# ------------------------------------------------------------------------#
    def createButtonShare(self,frame):
            self.botonBusquedaW=Button(frame,text="BUSCAR",font=("Arial Bold", 30, "bold"),command=self.buscarBoton)
            self.botonBusquedaW.place(x=480, y=601, width=200, height=40)


# ------------------------------------------------------------------------------------------

                    # FUNCIONES PARA CREAR WIDGETS Y FRAME

# ------------------------------------------------------------------------------------------

# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&---------------&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

             # FUNCION PARA MOSTRAR WIDGET (LABEL, LISTBOX, SCROLL), PARA CREAR EL FILTRO

# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&---------------&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&


    def createWidgetG(self, frame, tTablas, x, y, columna, tabla):
        # Label
        xlabel = x
        ylabel = y
        wlabel=217 # ancho x (direccion izquierda)
        hlabel=25 # alto y (direccion abajo)
        # Label
        label_widget = Label(frame, text=tTablas, font=("Arial Bold", 22, "bold"), justify="center")
        label_widget.place(x=xlabel, y=ylabel, width=wlabel, height=hlabel)

        # Listbox valores
        xlist=xlabel
        ylist=ylabel+hlabel+6
        wlist = 202  # ancho x (direccion izquierda)
        hlist = 150  # alto y (direccion abajo)
        # Listbox
        listbox_widget = Listbox(frame, font=("Arial", 12,))
        listbox_widget.place(x=xlist, y=ylist, width=wlist, height=hlist)

        # Scrollbar valores
        wscroll=15 #ancho x (direccion izquierda)
        # Scrollbar
        scrollbar_widget = Scrollbar(frame, command=listbox_widget.yview,width=wscroll)
        scrollbar_widget.place(x=(xlist+wlist), y=ylist, height=hlist)
        listbox_widget.config(yscrollcommand=scrollbar_widget.set)

        # Entry valores
        xentry=xlabel
        yentry=ylist+hlist+6
        wentry=wlist+wscroll #ancho x (direccion izquierda)
        hentry=30
        #Entry
        entry_var = StringVar()
        entry_widget = Entry(frame, textvariable=entry_var,font=("Arial Bold", 13, "bold"))
        entry_widget.place(x=xentry, y=yentry, width=wentry,height=hentry)

        # ------------------------------------------------------------#

        # Ejecutar consulta para obtener los datos de la tabla correspondiente
        consulta = f"SELECT {columna} FROM {tabla}"
        parametros = "1"
        ventana = self
        rows = self.consultas_y_modificacion_SQL(consulta, parametros, "1", ventana)

        for row in rows:
            listbox_widget.insert(END, row[0])  # Suponiendo que el nombre está en la columna 1

        # ------------------------------------------------------------#

        def clear_entry(event):
            if not entry_var.get():
                entry_widget.delete(0, END)

        entry_widget.bind("<<FocusOut>>", clear_entry)  # Vincular el evento FocusOut al Entry

        def on_select(event):
            selected_index = listbox_widget.curselection()
            if selected_index:
                selected_value = listbox_widget.get(selected_index)
                entry_var.set(selected_value)
                self.datos_entry[tabla] = selected_value  # Almacenar el valor en el diccionario

        listbox_widget.bind("<<ListboxSelect>>", on_select)
        entry_var.trace_add('write', lambda *args: self.datos_entry.__setitem__(tabla, entry_var.get()))  # Actualizar el valor en el diccionario en cada cambio del Entry

# *********************************---------------******************************************

                    # FUNCIONES PARA CREAR CINTA LATERIAL IZQUIERDA

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

    def abrir_PDF(self):
        if self.pdf:
            webbrowser.open(self.pdf)


    def createSideTape(self):

        self.place(x=0, y=0, relheight=1, relwidth=1)

        label = Label(self, text="BIENVENIDO", font=("Arial Bold", 30, "bold"))
        label.place(x=510, y=30 , width=500, height=30)

        imagen = PIL.Image.open(self.image)
        photo = PIL.ImageTk.PhotoImage(imagen)

        log_label = Label(self, image=photo)
        log_label.image = photo
        log_label.place(x=585, y=100, width=350, height=170)

        boton = Button(self, text="ABRIR MANUAL DE USUARIO", font=("Arial Bold", 18, "bold"), command=self.abrir_PDF)
        boton.place(x=510, y=350 , width=500, height=150)

        # Frame de cinta de reloj (se ocupa place())
        self.fraClock = Frame(self)
        self.fraClock.place(x=0, y=0, height=55, width=120)
        #Etiqueta de Reloj
        self.labClock = Label(self.fraClock, font=("Arial Bold", 20, "bold"))
        self.labClock.place(x=0, relheight=1, width=120)

        # Frame cina de opciones (se ocupa place())
        self.fraCinta = Frame(self)
        self.fraCinta.place(x=0, y=55, width=120, relheight=1)

        # ------- Boton Proveedores 120x120 pixeles
        #Imagen de 110 x 110
        self.boton_imagen1 = BotonImagen(self.fraCinta, self.imagensupplier , command=self.funBotonProv1)
        self.boton_imagen1.place(x=1, y=5)

        # ------- Boton calculadora.png 120x120 pixeles
        # Imagen de 110 x 110
        self.boton_imagen2 = BotonImagen(self.fraCinta, self.imagencalculadora, command=self.funBotonProv2)
        self.boton_imagen2.place(x=1, y=130)

    def establecer_conexion(self):
        intentos = 0
        max_intentos = 5  # Establece el número máximo de intentos

        while intentos < max_intentos:
            try:
                conn = sqlite3.connect(self.base_Datos)
                return conn
            except sqlite3.Error as e:
                intentos += 1
                time.sleep(2)
        return None


    def consultas_y_modificacion_SQL(self, consulta, parametros, seleccion, ventana):
        conn = self.establecer_conexion()

        if conn is None:
            respuesta = messagebox.askyesno("Advertencia", "Reintentar conexión a la Base de Datos.", parent=ventana)

            if respuesta:
                conn = self.establecer_conexion()
            else:
                return None

        cursor = conn.cursor()

        if parametros == "1":
            parametros = ()


        if seleccion == "1": #Consulta con muchos resultados
            cursor.execute(consulta, parametros)
            resultados = cursor.fetchall()
            conn.close()  # Cierra la conexión después de obtener el resultado
            return resultados

        elif seleccion == "2": #consulta de 1 resultado
            cursor.execute(consulta, parametros)
            resultados = cursor.fetchone()
            conn.close()  # Cierra la conexión después de obtener el resultado
            return resultados

        elif seleccion == "3":
            cursor.execute(consulta, parametros)
            conn.commit()
            conn.close() # Cierra la conexión después de guardar


# ------------------------------------------------------------------------------------------

                    # FUNCION PARA EL RELOJ

# ------------------------------------------------------------------------------------------

    # ------- Actualización de la hora MODIFICA EL COLOR Y LA FUENTE (self.labClock.config)
    locale.setlocale(locale.LC_ALL, '')
    def time_update(self):
        current_time = time.strftime("%I:%M:%S")
        if self.labClock.cget("relief") == "sunken":
            self.labClock.config(text=current_time, relief="raised", fg="black", bg="#F3F3F3")
        else:
            self.labClock.config(text=current_time, relief="sunken", fg="white", bg="#34373A")
        self.labClock.after(1000, self.time_update)


    def dimension_ventana(self,w,h,ventana):

        # Obtener el ancho y la altura de la pantalla
        screen_width = ventana.winfo_screenwidth()
        screen_height = ventana.winfo_screenheight()

        # Calcula las coordenadas (x, y) para centrar la ventana de búsqueda
        x = (screen_width - w) // 2
        y = (screen_height - h - 60) // 2

        # Establecer las dimensiones y la posición de la ventana de búsqueda
        ventana.geometry(f"{w}x{h}+{x}+{y}")
        ventana.maxsize(w, h)
        ventana.minsize(w, h)


# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

                    # CLASE PARA GENERAR BOTONES CON UNA IMAGEN

# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

class BotonImagen(Button):
    def __init__(self, master=None, imagen=None, **kwargs):
        self.imagen = self.cargar_imagen(imagen)
        super().__init__(master, image=self.imagen, **kwargs)


    def cargar_imagen(self, ruta_imagen):
        imagen = PhotoImage(file=ruta_imagen)
        self.imagen_ref = imagen
        return imagen

    def habilitar(self):
        self.config(state=NORMAL, relief="raised")
        self.habilitado = True

    def deshabilitar(self):
        self.config(state=DISABLED, relief="sunken")
        self.habilitado = False
#---------------------------------------------------------------------#