import pandas as pd
from func_porcentaje import contar_usuarios_porcentaje_avance, obtener_porcentaje_avance_aplicaciones,obtener_porcentaje_avance_total_usuarios,generar_grafico_lineas



# Leer el archivo de Excel con las tres hojas
archivo_excel = "matriz_ejemplo.xlsx"
archivo_csv = "PorcentajeGlobaldiario.csv"
df_analisis,porcentaje_avance_por_usuario,df_concatenado = obtener_porcentaje_avance_total_usuarios(archivo_excel,archivo_csv)

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

generar_grafico_lineas(archivo_csv)