import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd

# Variables globales para almacenar el DataFrame cargado
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
        df_export.to_csv(archivo_txt, sep=';', index=False, header=False)
        
        # Mostrar mensaje de éxito
        messagebox.showinfo("Exportación exitosa", "El archivo se ha exportado correctamente")
    
    except Exception as e:
        # Imprimir el error en la consola
        print(f"Error durante el proceso: {e}")
        messagebox.showerror("Error", f"Error durante el proceso: {e}")

# Configurar la ventana principal de Tkinter
root = tk.Tk()
root.title("Cargar y Exportar CSV")

# Crear el botón para el Proceso Uno
boton_proceso_uno = tk.Button(root, text="Proceso Uno", command=proceso_uno)
boton_proceso_uno.pack(pady=20)

# Ejecutar la aplicación de Tkinter
root.mainloop()
