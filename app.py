from tkinter import *
from tkinter.ttk import *
from tkinter import ttk
from tkinter import font
from tkinter import messagebox
from tkinter.filedialog import askdirectory
import os
import re

""""""""""""""""""""""""
# FUNCTIONS
""""""""""""""""""""""""
def seleccionar_carpeta():
    carpeta = askdirectory()
    if carpeta:
        ruta_var.set(carpeta)
        cargar_archivos(carpeta, listbox, progressbar)

def cargar_archivos(ruta, listbox, progressbar):
    listbox.delete(0, END)
    
    archivos = [item for item in os.listdir(ruta) if os.path.isfile(os.path.join(ruta, item))]
    total = len(archivos)
    
    if total == 0:
        return
    
    progressbar.grid()
    progressbar['maximum'] = total
    progressbar['value'] = 0
    
    for i, archivo in enumerate(sorted(archivos)):
        listbox.insert(END, archivo)
        progressbar['value'] = i + 1
        progressbar.update()
    
    progressbar.grid_remove()

def cargar_desde_entry(event, entry_ruta, listbox):
    ruta = entry_ruta.get().strip()
    if os.path.isdir(ruta):
        cargar_archivos(ruta, listbox, progressbar)
    else:
        messagebox.showerror("Error!", "Ruta de carpeta no existe")

def buscar_duplicados(entry_ruta, progressbar):
    ruta = entry_ruta.get()
    if not ruta:
        messagebox.showerror("Error!", "Carga primero una carpeta")
        return
    archivos = [item for item in os.listdir(ruta) if os.path.isfile(os.path.join(ruta, item))]
    duplicados = []
    
    for archivo in archivos:
        nombre, extension = os.path.splitext(archivo)
        if re.search(r'\s\(\d+\)$', nombre) or re.search(r'\s\bcopia\b$', nombre, re.IGNORECASE):
            duplicados.append(archivo)
    
    if len(duplicados) == 0:
        messagebox.showinfo("Info", "No se han encontrado archivos duplicados")
        return
    
    if messagebox.askyesno("Info", f"Archivos duplicados encontrados:\n{duplicados}\nEliminar?"):
        total = len(duplicados)
        progressbar.grid()
        progressbar['maximum'] = total
        progressbar['value'] = 0
        for i, duplicado in enumerate(duplicados):
            ruta_archivo = os.path.join(ruta, duplicado)
            progressbar['value'] = i + 1
            progressbar.update()
            try:
                os.remove(ruta_archivo)
            except Exception as e:
                messagebox.showerror("Ha habido un error!", f"Ha habido un error al intentar eliminar los archivos\n{e}")
                progressbar.grid_remove()
                cargar_archivos(ruta, listbox, progressbar)
        progressbar.grid_remove()
        messagebox.showinfo("Info", "Archivos eliminados correctamente")
        cargar_archivos(ruta, listbox, progressbar)



root = Tk()
root.title("Gestor de nombres")
style = ttk.Style()
style.theme_use('alt')
style.configure('Vertical.TScrollbar',
    gripcount=0,
    background="#999999",
    darkcolor='#777777',
    lightcolor='#BBBBBB',
    troughcolor='#666666',
    bordercolor='#777777',
    arrowcolor='white'
)
style.configure('Custom.TButton',
    font=('TkDefaultFont', 11),
    padding=8
)

""""""""""""""""""""""""
# MAIN FRAME
""""""""""""""""""""""""
mainframe = ttk.Frame(root, padding=50)
mainframe.grid(column=0, row=0, sticky=(N,W,E,S))
mainframe.grid_rowconfigure(1, minsize=150)
mainframe.grid_rowconfigure(0, minsize=100)
mainframe.grid_columnconfigure(2, minsize=700)
mainframe.grid_columnconfigure(3, minsize=200)


""""""""""""""""""""""""
# FRAME PREVIEW
""""""""""""""""""""""""
preview_frame = ttk.Frame(
    mainframe,
    height=250, width=250,
    borderwidth=5, relief='ridge'
)
preview_frame.grid(column=1, row=0, sticky=(N, W, E, S), rowspan=1)
preview_frame.grid_propagate(False)


""""""""""""""""""""""""
# LISTBOX
""""""""""""""""""""""""
listbox_frame = ttk.Frame(
    mainframe, height=500,
    borderwidth=5, relief='ridge'
)
listbox_frame.grid(column=2, row=0, sticky=(N, W, E, S), rowspan=2)
listbox_frame.grid_propagate(False)

listbox_font = font.Font(family='TkDefaultFont', size=16)
listbox = Listbox(
    listbox_frame,
    borderwidth=0,
    font=listbox_font,
    activestyle='none'
)
listbox.pack(fill=BOTH, expand=True)

listbox_scroll = ttk.Scrollbar(
    listbox,
    orient=VERTICAL,
    command=listbox.yview,
    style='Vertical.TScrollbar'
)
listbox.configure(yscrollcommand=listbox_scroll.set)
listbox_scroll.pack(side=RIGHT, fill=Y)

progressbar = ttk.Progressbar(listbox_frame, orient=HORIZONTAL, mode='determinate')
progressbar.grid(sticky=(W, E, S, N), padx=5, pady=5)
progressbar.grid_remove() 


""""""""""""""""""""""""
# BOTONES
""""""""""""""""""""""""
btn_frame = ttk.Frame(
    mainframe,
    borderwidth=1, relief='ridge',
    padding=10,
)
btn_frame.grid_configure(column=3, row=0, sticky=(N, W, E), rowspan=1)
btn_frame.grid_propagate(False)

btn_duplicados = ttk.Button(
    btn_frame,
    text='Buscar duplicados',
    style='Custom.TButton',
    command=lambda: buscar_duplicados(entry_ruta, progressbar)
)
btn_duplicados.pack(side=TOP, pady=10)

btn_renombrar = ttk.Button(
    btn_frame,
    text='Renombrar',
    style='Custom.TButton',
    # command=renombrar,
    state='disabled'
)
btn_renombrar.pack(pady=10)

btn_eliminar = ttk.Button(
    btn_frame,
    text="Eliminar Archivo",
    style='Custom.TButton',
    # command=eliminar
    state='disabled'
)
btn_eliminar.pack(pady=10)


""""""""""""""""""""""""
# FOLDER SELECTOR
""""""""""""""""""""""""
folderSelect_frame = ttk.Frame(
    mainframe,
    borderwidth=0
)
folderSelect_frame.grid(column=2, row=2)

ruta_var = StringVar()
btn_path = ttk.Button(
    folderSelect_frame,
    text='Abrir Carpeta',
    command=seleccionar_carpeta
)
btn_path.pack(pady=5)

entry_ruta = ttk.Entry(folderSelect_frame, textvariable=ruta_var, width=100)
entry_ruta.pack(pady=5)
entry_ruta.bind('<Return>', lambda event: cargar_desde_entry(event, entry_ruta, listbox))

for child in mainframe.winfo_children(): 
    child.grid_configure(padx=10, pady=5)
root.mainloop()