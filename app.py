import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import pandas as pd

# Variables globales para almacenar los DataFrames cargados
df = None

def proceso_uno():
    global df
    try:
        # Abrir el cuadro de diálogo para seleccionar el archivo CSV
        archivo_csv = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv")],
            title="Selecciona un archivo CSV"
        )
        
        # Intentar cargar el CSV en un DataFrame con codificación UTF-8
        try:
            df = pd.read_csv(archivo_csv, sep=';', encoding='utf-8')
        except UnicodeDecodeError:
            # Si falla, intentar cargar con codificación ISO-8859-1
            df = pd.read_csv(archivo_csv, sep=';', encoding='ISO-8859-1')
        
        # Mostrar mensaje de éxito
        messagebox.showinfo("Carga exitosa", "Ya se cargó CSV con datos")
        
        # Seleccionar las columnas deseadas
        df_export = df[['IdProducto', 'Codebar', 'Cantidad']]
        
        # Convertir todos los valores de Codebar a cadenas y eliminar puntos
        df_export['Codebar'] = df_export['Codebar'].astype(str).str.replace('.', '', regex=False)
        
        # Abrir el cuadro de diálogo para seleccionar la ubicación y nombre del archivo de exportación
        archivo_txt = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt")],
            title="Guardar archivo como"
        )
        
        # Exportar el DataFrame a un archivo de texto sin títulos de columna
        df_export.to_csv(archivo_txt, sep=';', index=False, header=False, quoting=3) # 3 corresponds to csv.QUOTE_NONE
        
        # Mostrar mensaje de éxito
        messagebox.showinfo("Exportación exitosa", "El archivo se ha exportado correctamente")
    
    except Exception as e:
        # Imprimir el error en la consola
        print(f"Error durante el proceso: {e}")
        messagebox.showerror("Error", f"Error durante el proceso: {e}")

def proceso_dos():
    global df
    try:
        # Lista para almacenar todos los DataFrames cargados
        dfs = []

        # Abrir cuadros de diálogo para seleccionar múltiples archivos CSV
        archivos_csv = filedialog.askopenfilenames(
            filetypes=[("CSV files", "*.csv")],
            title="Selecciona archivos CSV para combinar"
        )
        
        # Cargar cada CSV en un DataFrame y agregarlo a la lista
        for archivo_csv in archivos_csv:
            try:
                df_temp = pd.read_csv(archivo_csv, sep=';', encoding='utf-8')
                dfs.append(df_temp)
            except UnicodeDecodeError:
                # Si falla, intentar cargar con codificación ISO-8859-1
                df_temp = pd.read_csv(archivo_csv, sep=';', encoding='ISO-8859-1')
                dfs.append(df_temp)

        # Combinar todos los DataFrames en uno único, eliminando duplicados por 'IdProducto'
        df_combined = pd.concat(dfs).drop_duplicates(subset='IdProducto')

        # Mostrar mensaje de éxito
        messagebox.showinfo("Combinación exitosa", "Se han combinado y eliminado duplicados de los CSV")

        # Seleccionar el archivo Excel que contiene los productos a excluir
        archivo_excel = filedialog.askopenfilename(
            filetypes=[("Excel files", "*.xls;*.xlsx")],
            title="Selecciona un archivo Excel para excluir productos"
        )

        # Cargar el Excel y obtener los productos a partir de la fila 13 (índice 12)
        df_excel = pd.read_excel(archivo_excel, skiprows=12)

        # Obtener los IdProductos del Excel
        idproductos_excel = df_excel['IDProducto']

        # Excluir los productos del DataFrame combinado
        df_combined = df_combined[~df_combined['IdProducto'].isin(idproductos_excel)]

        # Seleccionar las columnas deseadas
        df_export = df_combined[['IdProducto', 'Codebar', 'Cantidad']]
        
        # Convertir todos los valores de Codebar a cadenas y eliminar puntos
        df_export['Codebar'] = df_export['Codebar'].astype(str).str.replace('.', '', regex=False)
        
        # Abrir el cuadro de diálogo para seleccionar la ubicación y nombre del archivo de exportación
        archivo_txt = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt")],
            title="Guardar archivo como"
        )
        
        # Exportar el DataFrame a un archivo de texto sin títulos de columna
        df_export.to_csv(archivo_txt, sep=';', index=False, header=False, quoting=3) # 3 corresponds to csv.QUOTE_NONE
        
        # Mostrar mensaje de éxito
        messagebox.showinfo("Exportación exitosa", "El archivo se ha exportado correctamente")
    
    except Exception as e:
        # Imprimir el error en la consola
        print(f"Error durante el proceso: {e}")
        messagebox.showerror("Error", f"Error durante el proceso: {e}")

# Función para hacer que la ventana sea movible
def hacer_ventana_movible(event):
    root.geometry(f'+{event.x_root}+{event.y_root}')

# Configurar la ventana principal de Tkinter
root = tk.Tk()
root.title("Cargar y Exportar CSV")
root.geometry("400x300")
root.configure(bg="#2e3f4f")

# Hacer que la ventana sea movible
root.bind('<B1-Motion>', hacer_ventana_movible)

# Configurar el estilo de la aplicación
style = ttk.Style()
style.theme_use('clam')

style.configure("TButton",
                font=("Helvetica", 12),
                padding=10,
                background="#2e3f4f",
                foreground="#ffffff",
                borderwidth=1,
                relief="solid")

style.map("TButton",
          background=[('active', '#3e5f7f')],
          foreground=[('active', '#ffffff')])

style.configure("TLabel",
                font=("Helvetica", 12),
                background="#2e3f4f",
                foreground="#ffffff")

style.configure("TFrame",
                background="#2e3f4f")

# Crear un marco para los botones
frame = ttk.Frame(root, padding="20")
frame.pack(fill="both", expand=True)

# Crear el botón para el Proceso Uno
boton_proceso_uno = ttk.Button(frame, text="Proceso Uno", command=proceso_uno)
boton_proceso_uno.pack(pady=10)

# Crear el botón para el Proceso Dos
boton_proceso_dos = ttk.Button(frame, text="Proceso Dos", command=proceso_dos)
boton_proceso_dos.pack(pady=10)

# Ejecutar la aplicación de Tkinter
root.mainloop()
