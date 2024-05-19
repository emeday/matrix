import pandas as pd
from func_porcentaje import contar_usuarios_porcentaje_avance, obtener_porcentaje_avance_aplicaciones



# Leer el archivo de Excel con las tres hojas
archivo_excel = "matriz_ejemplo.xlsx"
obtener_porcentaje_avance_aplicaciones(archivo_excel)
hojas = ["equipo I", "equipo II", "equipo III"]

# Leer todas las hojas y concatenarlas
dfs = [pd.read_excel(archivo_excel, sheet_name=hoja) for hoja in hojas]

# Concatenar los dataframes y resetear los índices
df_concatenado = pd.concat(dfs, ignore_index=True)

# Inicializar un diccionario para almacenar las aplicaciones completadas por usuario
aplicaciones_completadas_por_usuario = {}

# Calcular las aplicaciones completadas por usuario
for index, row in df_concatenado.iterrows():
    usuario = row['codigo']
    if isinstance(row['resultado'], str):
        aplicaciones_completadas = [app.strip() for app in row['resultado'].split(',') if app.strip() == "ok"]
        if usuario in aplicaciones_completadas_por_usuario:
            aplicaciones_completadas_por_usuario[usuario].extend(aplicaciones_completadas)
        else:
            aplicaciones_completadas_por_usuario[usuario] = aplicaciones_completadas

# Calcular el porcentaje de avance de cada usuario
porcentaje_avance_por_usuario = {}
for usuario, apps_completadas in aplicaciones_completadas_por_usuario.items():
    total_apps_usuario = len(df_concatenado[df_concatenado['codigo'] == usuario]['aplicación'].unique())
    porcentaje_avance_por_usuario[usuario] = round((len(apps_completadas) / total_apps_usuario) * 100, 2)

# Calcular el porcentaje global de avance
porcentaje_global_avance = round(sum(porcentaje_avance_por_usuario.values()) / len(porcentaje_avance_por_usuario), 2)

# Crear un DataFrame para el análisis de los datos
df_analisis = pd.DataFrame.from_dict(porcentaje_avance_por_usuario, orient='index', columns=["Porcentaje de Avance por Usuario"])

# Agregar el nombre del usuario como una columna adicional
nombres_usuario = {codigo: df_concatenado[df_concatenado['codigo'] == codigo]['nombre'].iloc[0] for codigo in porcentaje_avance_por_usuario.keys()}
df_analisis["Nombre"] = df_analisis.index.map(nombres_usuario)

# Agregar el porcentaje global de avance como una columna adicional
df_analisis["Porcentaje Global de Avance"] = porcentaje_global_avance

# Reordenar las columnas para tener el nombre al principio
df_analisis = df_analisis[["Nombre", "Porcentaje de Avance por Usuario", "Porcentaje Global de Avance"]]

# Imprimir el DataFrame de análisis con formato de dos decimales
pd.options.display.float_format = '{:.2f}'.format
print("Análisis de Avance:")
print(df_analisis)



# Ejemplo de uso:
total_usuarios, avance_100, avance_50, menos_50 = contar_usuarios_porcentaje_avance(porcentaje_avance_por_usuario)

# Crear un DataFrame con los resultados
data = {
    "Categoría de Avance": ["Total de Usuarios", "Avance del 100%", "Avance del 50%", "Menos del 50%"],
    "Cantidad de Usuarios": [total_usuarios, avance_100, avance_50, menos_50]
}
df_resultados = pd.DataFrame(data)

# Imprimir el DataFrame
print("Resultados de Avance por Usuario:")
print(df_resultados)


# Ejemplo de uso:
df_porcentaje_avance_aplicaciones, df_resumen = obtener_porcentaje_avance_aplicaciones(df_concatenado)

print("Porcentaje de Avance por Aplicación:")
print(df_porcentaje_avance_aplicaciones)
print("\nResumen de Avance por Aplicación:")
print(df_resumen)