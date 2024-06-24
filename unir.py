import os
import pandas as pd

# Función para listar archivos CSV en un directorio
def listar_archivos_csv(directorio):
    archivos = [f for f in os.listdir(directorio) if f.endswith('.csv')]
    return archivos

# Función para concatenar un número específico de archivos CSV
def concatenar_archivos_csv(directorio, num_archivos, output_file):
    archivos = listar_archivos_csv(directorio)
    
    if num_archivos > len(archivos):
        raise ValueError("El número de archivos solicitados excede la cantidad de archivos disponibles en el directorio.")
    
    archivos_a_concatenar = archivos[:num_archivos]
    
    dataframes = []
    for archivo in archivos_a_concatenar:
        ruta_archivo = os.path.join(directorio, archivo)
        df = pd.read_csv(ruta_archivo)
        dataframes.append(df)
    
    df_concatenado = pd.concat(dataframes, ignore_index=True)
    df_concatenado.to_csv(output_file, index=False)

# Parámetros
directorio = 'CICIoT2023'  # Directorio con los archivos CSV
num_archivos = 8 # Número de archivos a concatenar
output_file = 'muestra.csv'  # Nombre del archivo de salida

# Ejecutar la concatenación
concatenar_archivos_csv(directorio, num_archivos, output_file)