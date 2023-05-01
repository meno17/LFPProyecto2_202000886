import math
import os
from tkinter import *
import webbrowser as wb
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox as mb

import pymongo
import ply.lex as lex   
from errores import Errores

#ANALIZADOR LEXICO-----------------------------------
tokens = [
    'CREATE', 'DATABASE', 'COLLECTION', 'INSERT', 'INTO', 'VALUES',
    'STRING', 'NUMBER', 'COMMA', 'LPAREN', 'RPAREN'
]

#DEFINIMOS EL VALOR DE LOS TOKENS
t_CREATE = r'create'
t_DATABASE = r'database'
t_COLLECTION = r'collection'
t_INSERT = r'insert'
t_INTO = r'into'
t_VALUES = r'values'
t_COMMA = r','
t_LPAREN = r'\('
t_RPAREN = r'\)'

def t_NUMBER(t):
    r"\d+(\.\d+)?"
    t.value = float(t.value)
    return t

def t_STRING(t):
    r'"[^"]*"'
    t.value = t.value[1:-1]
    return t
def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)

t_ignore = " \t"


errores_=[]
def t_error(t):
    erro='"{ERROR""Descripcion-Token:" {"Lexema: "%s" "En linea:"' % t.value[0],t.lineno ,'}','}'
    error = Errores(t.value[0],'Error Lexico', find_column(input,t),t.lineno)
    errores_.append(error)
    errores_list.insert(tk.END, str(erro))

    t.lexer.skip(1)

lexer = lex.lex()

    

#ANALIZADOR SINTACTICO--------------------------------------------------

def p_instrccuinInicial(t):
    'init : RBRACE '
    t[0]=t[1]
    return [0]

def p_error(t):
    print("Error de sintaxis en '%s'" % t.value," Linea:", t.lineno, " Columna:",find_column(input,t))

def find_column(inp, tk):
    try:
        line_start = inp.rfind('\n',0,tk.lexpos) + 1
        return (tk.lexpos - line_start) + 1
    except:
        return 0

def p_statement_create_database(p):
    '''statement : CREATE DATABASE STRING'''
    client = pymongo.MongoClient()
    db_name = p[3].strip('"')
    client[db_name]

def p_statement_create_collection(p):
    '''statement : CREATE COLLECTION STRING'''
    db = pymongo.MongoClient().get_database('test')
    collection_name = p[3].strip('"')
    db[collection_name]

def p_statement_insert(p):
    '''statement : INSERT INTO STRING VALUES LPAREN value_list RPAREN'''
    db = pymongo.MongoClient().get_database('test')
    collection_name = p[3].strip('"')
    values = p[6]
    db[collection_name].insert_many(values)

def p_value_list(p):
    '''value_list : value_list COMMA value
                  | value'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[1].append(p[3])
        p[0] = p[1]

def p_value(p):
    '''value : STRING
             | NUMBER'''
    p[0] = p[1]

def analizador():
    data = ingreso.get("1.0", tk.END)
    lexer.input(data)
    tokens_list.delete(0, tk.END)
    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens_list.insert(tk.END, str(tok)) 
    
#PARTE GRAFICA-----------------------------------------------------------
    
class VentanaBienvenida():
    def __init__(self):
        self.ventana_bienvenida=Tk()
        self.ventana_bienvenida.title("BIENVENIDO!!!")
        self.ventana_bienvenida.resizable(0,0)
        self.ventana_bienvenida.geometry("450x250+500+250")
        self.contenedor()

    def contenedor(self):
        #Se crea el widget Frame para ilustrar botones dentro de el
        self.frame_bienvenida = Frame(height=200,width=400)
        #configuracion del Frame y del color del fondo 
        self.frame_bienvenida.config(bg="#00F3FF")
        #Empaquetando el frame a la ventana raiz
        self.frame_bienvenida.pack(padx=20,pady=20)
        #Mensaje de bienvenida con estilo 
        label_bienvenida = Label(self.frame_bienvenida,bg="#F94B5E" ,fg="white", text="|----------BIENVENIDOS----------|")
        #posición de el widget Label
        label_bienvenida.place(x=50,y=10)
        #estilo de letra
        label_bienvenida.config(font=("Consolas",13))

        #-----BOTONES-----
        boton_ventana_analizador= Button(self.frame_bienvenida,bg="#F94B5E", text="IR A ANALIZADOR",command=self.inicioVentanaAlizador)
        boton_ventana_analizador.pack()
        boton_ventana_analizador.place(x=120,y=50,height=50,width=150)
        boton_salir= Button(self.frame_bienvenida,bg="#F94B5E", text="SALIR",command=self.salir)
        boton_salir.pack()
        boton_salir.place(x=120,y=125,height=50,width=150)
        self.frame_bienvenida.mainloop()

    def inicioVentanaAlizador(self):
        self.ventana_bienvenida.destroy()
        VentanaAnalizador()
    def salir(self):
        self.ventana_bienvenida.destroy()

class VentanaAnalizador():
    def __init__(self):
        self.ventana_analizador= Tk()
        self.ventana_analizador.title("ANALIZADOR LEXICO")
        self.ventana_analizador.resizable(0,0)
        self.ventana_analizador.geometry("1200x700+180+50")
        self.ventana_analizador.configure(bg="#F94B5E")

        #BARRA ARCHIVO
        barraMenu=Menu(self.ventana_analizador)
        menuArchivo=Menu(barraMenu)
        

        menuArchivo.add_command(label="Abrir",command=self.abrir_archivo)
        menuArchivo.add_command(label="Guardar",command=self.guardar)
        menuArchivo.add_command(label="Guardar Como",command=self.guardarComo)
        menuArchivo.add_separator()
        menuArchivo.add_command(label="Analizar",command=analizador)
        menuArchivo.add_separator()
        menuArchivo.add_command(label="Salir",command=self.salir)
        barraMenu.add_cascade(label="Archivo",menu=menuArchivo)

        #BARRA AYUDA
        menuAyuda=Menu(barraMenu)

        menuAyuda.add_command(label="Temas de ayuda",command=self.temasAyuda)
        barraMenu.add_cascade(label="Ayuda",menu=menuAyuda)

        self.ventana_analizador.config(menu=barraMenu)



        #CAJA DE TEXTO
        global ingreso
        ingreso = Text(self.ventana_analizador, height = 40, width = 100)
        ingreso.place(x=25,y=25)
        #LISTBOX PARA LOS TOKENS ENCONTRADOS
        global tokens_list
        tokens_list = Listbox(self.ventana_analizador, height = 10, width = 55)
        tokens_list.place(x=850,y=100)
        #LISTBOX PARA LOS ERRORES ENCONTRADOS
        global errores_list
        errores_list = Listbox(self.ventana_analizador, height = 10, width = 55)
        errores_list.place(x=850,y=400)        
        #EJECUTAR VENTANA_ANALIZADOR
        self.ventana_analizador.mainloop()

    def usuario(self):
        os.system("MANUAL_DE_USUARIO")
    def tecnico(self):
        os.system("MANUAL_DE_USUARIO")
    def salir(self):
        self.ventana_analizador.destroy()

    def abrir_archivo(self):
        x = ""
        Tk().withdraw()
        try:
            filename = fd.askopenfilename(title='Selecciona un archivo',filetypes=[('All Files', '*')])
            # print(filename)
            with open(filename, encoding='utf-8') as infile:
                x = infile.read().strip()
                
                examinar = x
                ingreso.insert(1.0,x)
        except:
            mb.showerror("Error", "Archivo incorrecto")
            return

    def guardar(self):
        file = fd.asksaveasfile(filetypes=[("txt file", ".txt")],
                                        defaultextension=".txt")
        filetext = str(ingreso.get(1.0,END))
        file.write(filetext)
        file.close()
    def guardarComo(self):
        file = fd.asksaveasfile(filetypes=[
                                            ("txt file", ".txt"),
                                            ("Html file", ".html"),
                                            ("Documento",".doc"),
                                            ("Imagen jpg",".jpg"),
                                            ("Imagen png",".png"),
                                            ("Lectura (PDF)",".pdf"),
                                            ("All files",".*")],
                                        defaultextension=".txt")
        filetext = str(ingreso.get(1.0,END))
        file.write(filetext)
        file.close()

    def temasAyuda(self):
        self.ventana_analizador.destroy()
        TemasAyuda()

class TemasAyuda():
    def __init__(self):
        self.menu = Tk()
        self.menu.title("Analizador  Lexico")
        self.menu.resizable(0,0)
        self.menu.geometry("550x200+500+250")
        self.menu.configure(bg="#F94B5E")
        self.container()

    def container(self):
        self.frame = Frame(height=500,width=800)
        self.frame.config(bg="#F94B5E")
        self.frame.pack(padx=20,pady=20)

        curso = Label(self.frame,bg="#63a194" , text="\n|        Lenguajes Formales y de Programación       |"
                                                     "\n|                     Seccion: A+                   |"
                                                     "\n|      202000886 - José Ricardo Menocal Kong        |")
        curso.pack
        curso.place(x=10,y=30)
        curso.config(font=("Consolas",13))


        
        botonIniciar =  Button(self.frame,bg="#ffffff",font=("Consolas",12),text="Cerra",command=self.cerrar)
        botonIniciar.place(x=215,y=120)
        botonIniciar.pack
        self.frame.mainloop()

    def cerrar(self):
        self.menu.destroy()
        VentanaAnalizador()
       

VentanaBienvenida()