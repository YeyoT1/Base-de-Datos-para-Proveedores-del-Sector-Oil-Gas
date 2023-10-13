import Proveeduria
import PIL
from PIL import Image, ImageTk
import sqlite3, os, json, tempfile, webbrowser, concurrent.futures, time
from tkinter import ttk
from tkinter import *
from tkinter import messagebox

nombre_company = " "	                        #colocar el nombre de la compañia
ruta_server = " "	                            #Colocar la ruta del servidor si se desea colocar en servidor y que sea cliente remoto, Ejemplo --> "\\\\192.168.1.2\\Documentos\\Nueva Carpeta"
numero_telefono = " "	                        #Colocar el numero de telefono para el uso de Soporte Técnico
icono = default="@shell32.dll,-154"             #Colocar el nombre del archivo, Ejemplo --> icono.ico
login = "default"                           #Colocar el nombre del archivo, Ejemplo --> Login.png (Recomendado --> 350 x 223 pixeles)

def buscar_archivo(ruta, nombre_archivo):
    ruta_archivo = os.path.join(ruta, nombre_archivo)
    if os.path.exists(ruta_archivo):
        return ruta_archivo
    return None

def buscar_archivo_en_servidor_o_local(nombre_archivo, rutas, cache):
    if nombre_archivo in cache:
        ruta_cache = cache[nombre_archivo]
        if os.path.exists(ruta_cache):
            return ruta_cache

    with concurrent.futures.ThreadPoolExecutor() as executor:
        resultados = list(executor.map(lambda ruta: buscar_archivo(ruta, nombre_archivo), rutas))

    for resultado in resultados:
        if resultado is not None:
            cache[nombre_archivo] = resultado
            guardar_cache(cache_carpeta, cache)
            return resultado
    return None

def cargar_cache(carpeta):
    try:
        cache_file = os.path.join(carpeta, "cache.json")
        with open(cache_file, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def guardar_cache(carpeta, cache):
    cache_file = os.path.join(carpeta, "cache.json")
    with open(cache_file, "w") as file:
        json.dump(cache, file)

ruta_servidor = ruta_server
ruta_local = os.path.dirname(os.path.abspath(__file__))
cache_carpeta = os.path.join(tempfile.gettempdir(), f"{nombre_company}_cache")

if not os.path.exists(cache_carpeta):
    os.makedirs(cache_carpeta)

cache = cargar_cache(cache_carpeta)

image = buscar_archivo_en_servidor_o_local(f"{login}.png", [ruta_local, ruta_servidor], cache)
icon = buscar_archivo_en_servidor_o_local(f"{icono}", [ruta_local, ruta_servidor], cache)
imagenSupplier = buscar_archivo_en_servidor_o_local("supplier.png", [ruta_local, ruta_servidor], cache)
imagenCalculadora = buscar_archivo_en_servidor_o_local("calculadora.png", [ruta_local, ruta_servidor], cache)
base_Datos = buscar_archivo_en_servidor_o_local("DB.db", [ruta_local, ruta_servidor], cache)
pdf = buscar_archivo_en_servidor_o_local("Manual_Usuario.pdf", [ruta_local, ruta_servidor], cache)


def dimension(ventana, window_width, window_height):

    # Obtén el ancho y la altura de la pantalla
    screen_width = ventana.winfo_screenwidth()
    screen_height = ventana.winfo_screenheight()

    # Calcula las coordenadas (x, y) para centrar la ventana principal
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height - 60) // 2

    ventana.geometry(f"{window_width}x{window_height}+{x}+{y}")
    ventana.minsize(window_width, window_height)
    ventana.maxsize(window_width, window_height)


def main():
    master = Tk()
    master.wm_title(f"{nombre_company} - Proveeduría")

    master.wm_iconbitmap(icon)

    window_width = 1280
    window_height = 720

    dimension(master, window_width, window_height)

    def cerrarVentana(event):
        master.destroy()

    master.bind("<Control-q>", cerrarVentana)
    master.bind("<Control-Q>", cerrarVentana)

    app = Proveeduria.Ventana_Principal(master, nombre_company, base_Datos, imagenSupplier, imagenCalculadora, icon, image, pdf)
    app.mainloop()

def log():

    def llamar_soporte():
        # Cambia el número por el que deseas llamar
        webbrowser.open(f"https://api.whatsapp.com/send/?phone={numero_telefono}&text&type=phone_number&app_absent=0")

    def mostrar_soporte_tecnico():
        resultado = messagebox.askyesnocancel("Soporte Técnico", "¿Deseas mandar mensaje al Soporte Técnico?", default=messagebox.YES, type=messagebox.YESNO)

        if resultado:
            llamar_soporte()

    if not base_Datos:
        def mostrar_error_y_soporte():
            messagebox.showerror("Advertencia", "No se ha encontrado la 'Base Datos'. Verifica la conexión o llame a soporte técnico")
            mostrar_soporte_tecnico()

        mostrar_error_y_soporte()

        return

    log = Tk()
    log.wm_title(f"{nombre_company} - Inicio de sesión")

    def buscar_User_pass():
        user = user_Entry.get()  # obtiene el Usuario
        password = pass_Entry.get()  # Obtiene contraseña

        if user == "admin" and password == "admin":
            open_admin_window(log)

        else:
            consulta = "SELECT * FROM ArchivoUserPassT WHERE user = ? AND pass = ?"
            parametros = (user, password,)
            # Execute the query with user and password as parameters
            resultado = consultas_y_modificacion_SQL(consulta, parametros, True, log)

            if resultado:
                log.destroy()
                main()
            else:
                messagebox.showerror("Error de Inicio de Sesión", "El usuario o contraseña inválidos")
                pass_Entry.delete(0, END)

    window_width = 630
    window_height = 370

    dimension(log, window_width, window_height)

    log.wm_iconbitmap(icon)

    imagen = PIL.Image.open(image)
    photo = PIL.ImageTk.PhotoImage(imagen)

    log_frame = Frame(log, bg="white")
    log_frame.place(x=0, y=0, relheight=1, relwidth=1)

    log_label = Label(log_frame, image=photo)
    log_label.place(x=140, y=0, width=350, height=170)

    user_Label = Label(log_frame, text="USUARIO", font=("Arial Bold", 16, "bold"))
    user_Label.place(x=50, y=200, width=150, height=40)

    user_Entry = Entry(log_frame, font=("Arial Bold", 16, "bold"))
    user_Entry.place(x=200, y=200, width=350, height=40)

    pass_Label = Label(log_frame, text="CONTRASEÑA", font=("Arial Bold", 16, "bold"))
    pass_Label.place(x=50, y=250, width=150, height=40)

    pass_Entry = Entry(log_frame, font=("Arial Bold", 16, "bold"), show="*")
    pass_Entry.place(x=200, y=250, width=350, height=40)

    # Function to toggle password visibility
    def toggle_password_visibility():
        if show_pass_var.get() == 1:
            pass_Entry.config(show="")
        else:
            pass_Entry.config(show="*")

    show_pass_var = IntVar()  # Variable to hold checkbox state
    show_pass_checkbox = Checkbutton(log_frame, text="MOSTRAR CONTRASEÑA", font=("Arial Bold", 10, "bold"), variable=show_pass_var, command=toggle_password_visibility)
    show_pass_checkbox.place(x=215, y=300, width=200, height=25)

    # Button to toggle password visibility
    toggle_button = Button(log_frame, text="INICIAR SESION", command=buscar_User_pass)
    toggle_button.place(x=215, y=330, width=200, height=30)


    def cerrarVentana(event):
        log.destroy()

    log.bind("<Control-q>", cerrarVentana)
    log.bind("<Control-Q>", cerrarVentana)

    log.bind("<Return>", lambda event: buscar_User_pass())

    log.mainloop()


def open_admin_window(ventana):
    admin_window = Toplevel(ventana)
    admin_window.wm_title(f"{nombre_company} - Administrador")
    admin_window.wm_iconbitmap(icon)

    def cerrarVentana(event):
        admin_window.destroy()

    admin_window.bind("<Control-w>", cerrarVentana)
    admin_window.bind("<Control-W>", cerrarVentana)

    window_width = 500
    window_height = 180

    dimension(admin_window, window_width, window_height)

    # Labels and entries for new user and password
    new_user_label = Label(admin_window, text="Nuevo Usuario", font=("Arial Bold", 16, "bold"))
    new_user_label.place(x=10, y=10)

    new_user_entry = Entry(admin_window, font=("Arial Bold", 16, "bold"))
    new_user_entry.place(x=230, y=10)

    new_pass_label = Label(admin_window, text="Nueva Contraseña", font=("Arial Bold", 16, "bold"))
    new_pass_label.place(x=10, y=60)

    new_pass_entry = Entry(admin_window, font=("Arial Bold", 16, "bold"))
    new_pass_entry.place(x=230, y=60)

    def add_new_user():
        new_user = new_user_entry.get()
        new_pass = new_pass_entry.get()

        if new_user and new_pass:
            add_user_to_database(new_user, new_pass, admin_window)

        elif new_user and new_pass == None:
            messagebox.showerror("Error", "Por favor ingresa su contraseña.")

    # Button to add new user and password to the database
    add_button = Button(admin_window, text="Agregar Usuario", font=("Arial Bold", 16, "bold"), command=add_new_user)
    add_button.place(x=50, y=100, width=200, height=50)

    # Button to open a window displaying users and passwords
    view_users_button = Button(admin_window, text="Ver Usuarios", font=("Arial Bold", 16, "bold"), command=lambda: view_users(ventana))
    view_users_button.place(x=250, y=100, width=200, height=50)

    admin_window.bind("<Control-n>", add_new_user)
    admin_window.bind("<Control-N>", add_new_user)
    admin_window.mainloop()

def view_users(ventana):

    consulta = "SELECT user, pass FROM ArchivoUserPassT"
    parametros = "1"

    resultado =  consultas_y_modificacion_SQL(consulta, parametros, True, ventana)

    users_window = Toplevel(ventana)
    users_window.wm_title(f"{nombre_company} - Usuarios Registrados")
    users_window.wm_iconbitmap(icon)

    # Botón del teclado "supr" para borrar el usuario del sistema
    menu = Menu(users_window)
    users_window.config(menu=menu)
    menu.add_command(label="Eliminar Usuario", command=lambda: delete_user(users_tree, users_window))

    window_width = 500
    window_height = 200

    dimension(users_window, window_width, window_height)

    users_tree = ttk.Treeview(users_window, columns=("Usuario", "Contraseña"), show="headings")
    users_tree.heading("Usuario", text="Usuario")
    users_tree.heading("Contraseña", text="Contraseña")

    users_tree.tag_configure("heading", font=("Arial Bold", 22))  # Set font for column headings

    users_tree.pack(padx=10, pady=10)

    for user, password in resultado:
        users_tree.insert("", "end", values=(user, password))

    users_tree.config(selectmode="browse")

    users_tree.bind("<Delete>", lambda event: delete_user(users_tree, users_window))

    def cerrarVentana(event):
        users_window.destroy()

    users_window.bind("<Control-w>", cerrarVentana)
    users_window.bind("<Control-W>", cerrarVentana)
    users_window.mainloop()


def delete_user(users_tree, ventana):
    selected_item = users_tree.selection()
    if selected_item:
        item = users_tree.item(selected_item)
        user = item["values"][0]  # Get the selected user

        # Show a confirmation dialog
        confirmacion = messagebox.askyesno("Confirmar Eliminación", f"¿Deseas eliminar el usuario '{user}'?", parent=ventana)

        if confirmacion:
            consulta = "DELETE FROM ArchivoUserPassT WHERE user = ?"
            parametros = (user,)
            consultas_y_modificacion_SQL(consulta, parametros, False, ventana)

            # Elimina el Item seleccionado en el Treeview
            users_tree.delete(selected_item)
    else:
        messagebox.showerror("Advertencia", "Seleccione un usuario a eliminar.", parent=ventana)

def add_user_to_database(user, password, ventana):

    consulta = "SELECT * FROM ArchivoUserPassT WHERE user = ?"
    parametros = (user,)
    existing_user=consultas_y_modificacion_SQL(consulta, parametros, True, ventana)
    # Valida si existe un usuario

    if existing_user:
        messagebox.showerror("Usuario Existente", "El usuario ya existe en la base de datos.", parent=ventana)
        return
    else:
        # Agrega un nuevo usuario a la base de datos
        consulta = "INSERT INTO ArchivoUserPassT (user, pass) VALUES (?, ?)"
        parametros = (user, password,)
        consultas_y_modificacion_SQL(consulta, parametros, False, ventana)
        messagebox.showinfo("Usuario Agregado", "El nuevo usuario ha sido agregado a la base de datos.", parent=ventana)

def establecer_conexion():
    intentos = 0
    max_intentos = 5  # Establece el número máximo de intentos

    while intentos < max_intentos:
        try:
            conn = sqlite3.connect(base_Datos)
            return conn
        except sqlite3.Error as e:
            intentos += 1
            time.sleep(1)
    return None

# Realizar conexión consultar y modificar
def consultas_y_modificacion_SQL(consulta, parametros, seleccion, ventana):
    conn = establecer_conexion()

    if conn is None:
        respuesta = messagebox.askyesno("Advertencia", "Reintentar conexión a la Base de Datos.", parent=ventana)

        if respuesta:
            conn = establecer_conexion()
        else:
            return

    cursor = conn.cursor()

    if parametros == "1": # Sin parametros para consultas
        parametros = ()

    if seleccion: #Consulta SELECT (True)
        cursor.execute(consulta, parametros)
        resultado = cursor.fetchall()
        conn.close()  # Cierra la conexión después de obtener el resultado
        return resultado

    else: # Consulta y guardar cambios (False)
        cursor.execute(consulta, parametros)
        conn.commit()
        conn.close()  # Cierra la conexión después de la modificación


if __name__ == "__main__":
    log()
