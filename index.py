from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pymongo
from bson.objectid import ObjectId

MONGO_HOST = "localhost"
MONGO_PUERTO = "27017"
MONGO_TIEMPO_FUERA = 1000

MONGO_URI = "mongodb://" + MONGO_HOST + ":" + MONGO_PUERTO + "/"

MONGO_BASEDATOS = "Escuela"
MONGO_COLLECCION = "Alumnos"

cliente = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=MONGO_TIEMPO_FUERA)
basedatos = cliente[MONGO_BASEDATOS]
collection = basedatos[MONGO_COLLECCION]

ID_ALUMNO = ""

def mostrarDatos(nombre="", sexo="", Calificacion=""):
    objectobuscar = {}
    if len(nombre) != 0:
        objectobuscar["nombre"] = nombre
    if len(sexo) != 0:
        objectobuscar["sexo"] = sexo
    if len(Calificacion) != 0:
        objectobuscar["Calificacion"] = Calificacion

    try:
        registros = tabla.get_children()
        for registro in registros:
            tabla.delete(registro)

        # Mover el cliente aquí para asegurarse de que esté disponible
        cliente = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=MONGO_TIEMPO_FUERA)
        basedatos = cliente[MONGO_BASEDATOS]
        collection = basedatos[MONGO_COLLECCION]

        for documento in collection.find(objectobuscar):
            tabla.insert('', 0, text=documento["_id"], values=documento["nombre"])

        # Cerrar el cliente después de todas las operaciones
        cliente.close()

    except pymongo.errors.ServerSelectionTimeoutError as errorTiempo:
        print("Tiempo excedido" + str(errorTiempo))
    except pymongo.errors.ConnectionFailure as errorConexion:
        print("Fallo al conectarse a MongoDB " + str(errorConexion))


def Crearresgistro():
    if len(nombre.get()) != 0 and len(Calificacion.get()) != 0 and len(sexo.get()) != 0:
        try:
            documento = {"nombre": nombre.get(), "Calificacion": Calificacion.get(), "sexo": sexo.get()}
            collection.insert_one(documento)
            nombre.delete(0, END)
            sexo.delete(0, END)
            Calificacion.delete(0, END)
        except pymongo.errors.ConnectionFailure as error:
            print(error)
    else:
        messagebox.showerror(message="Los campos no pueden estar vacíos")

    mostrarDatos()


def dobleClickTabla(event):
    global ID_ALUMNO
    ID_ALUMNO = tabla.item(tabla.selection())["text"]
    documento = collection.find({"_id": ObjectId(ID_ALUMNO)})[0]
    nombre.delete(0, END)
    nombre.insert(0, documento["nombre"])
    sexo.delete(0, END)
    sexo.insert(0, documento["sexo"])
    Calificacion.delete(0, END)
    Calificacion.insert(0, documento["Calificacion"])
    crear["state"] = "disabled"
    editar["state"] = "normal"
    Borrar["state"] = "normal"


def editarregistro():
    global ID_ALUMNO
    if len(nombre.get()) != 0 and len(sexo.get()) != 0 and len(Calificacion.get()) != 0:
        try:
            idBuscar = {"_id": ObjectId(ID_ALUMNO)}
            nuevosvalores = {"nombre": nombre.get(), "sexo": sexo.get(), "Calificacion": Calificacion.get()}
            result = collection.update_one(idBuscar, {"$set": nuevosvalores})

            if result.modified_count > 0:
                print("Documento actualizado con éxito.")
            else:
                print("Ningún documento fue actualizado.")

            nombre.delete(0, END)
            sexo.delete(0, END)
            Calificacion.delete(0, END)
        except pymongo.errors.ConnectionFailure as error:
            print(error)
    else:
        messagebox.showerror("Los campos no pueden estar vacíos")
    mostrarDatos()
    crear["state"] = "normal"
    editar["state"] = "disabled"
    Borrar["state"] = "disabled"


def Borrarregistro():
    global ID_ALUMNO
    try:
        idBuscar = {"_id": ObjectId(ID_ALUMNO)}
        collection.delete_one(idBuscar)
        nombre.delete(0, END)
        sexo.delete(0, END)
        Calificacion.delete(0, END)

    except pymongo.errors.ConnectionFailure as error:
        print(error)
    crear["state"] = "normal"
    editar["state"] = "disabled"
    Borrar["state"] = "disabled"
    mostrarDatos()


def Buscarregistro():
    mostrarDatos(Buscarnombre.get(), Buscarsexo.get(), BuscarCalificacion.get())

ventana = Tk()
tabla = ttk.Treeview(ventana, columns=2)
tabla.grid(row=1, column=0, columnspan=2)
tabla.heading("#0", text="ID")
tabla.heading("#1", text="NOMBRE")

tabla.bind("<Double-Button-1>", dobleClickTabla)

Label(ventana, text="nombre").grid(row=2, column=0)
nombre = Entry(ventana)
nombre.grid(row=2, column=1, sticky=W+E)

Label(ventana, text="sexo").grid(row=3, column=0)
sexo = Entry(ventana)
sexo.grid(row=3, column=1, sticky=W+E)

Label(ventana, text="Calificacion").grid(row=4, column=0)
Calificacion = Entry(ventana)
Calificacion.grid(row=4, column=1, sticky=W+E)

crear = Button(ventana, text="Crear alumno", command=Crearresgistro, bg="green", fg="white")
crear.grid(row=5, columnspan=2, sticky=W+E)

editar = Button(ventana, text="Editar alumno", command=editarregistro, bg="yellow")
editar.grid(row=6, columnspan=2, sticky=W+E)
editar["state"] = "disabled"

Borrar = Button(ventana, text="Borrar alumno", command=Borrarregistro, bg="red", fg="white")
Borrar.grid(row=7, columnspan=2, sticky=W+E)
Borrar["state"] = "disabled"

Label(ventana, text="Buscar nombre").grid(row=8, column=0)
Buscarnombre = Entry(ventana)
Buscarnombre.grid(row=8, column=1, sticky=W+E)

Label(ventana, text="Buscar sexo").grid(row=9, column=0)
Buscarsexo = Entry(ventana)
Buscarsexo.grid(row=9, column=1, sticky=W+E)

Label(ventana, text="Buscar Calificacion").grid(row=10, column=0)
BuscarCalificacion = Entry(ventana)
BuscarCalificacion.grid(row=10, column=1, sticky=W+E)

Buscar = Button(ventana, text="Buscar alumno", command=Buscarregistro, bg="blue", fg="white")
Buscar.grid(row=11, columnspan=2, sticky=W+E)

cliente = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=MONGO_TIEMPO_FUERA)
basedatos = cliente[MONGO_BASEDATOS]
collection = basedatos[MONGO_COLLECCION]

mostrarDatos()
ventana.mainloop()
