import pandas as pd

# Función para convertir valores a string y evitar notación científica
def to_string(val):
    return str(val)

# Intentar leer el archivo con diferentes codificaciones
try:
    df = pd.read_csv('productos.csv', sep=";", encoding='latin1', converters={'Codebar': to_string})
except UnicodeDecodeError:
    df = pd.read_csv('productos.csv', sep=";", encoding='cp1252', converters={'Codebar': to_string})

# Verificar los datos leídos
print(df.head())

# Si deseas guardar el DataFrame nuevamente en un CSV
df.to_csv('productos_limpio.csv', index=False)
