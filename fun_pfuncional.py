import pandas as pd

def generate_data_pfuncional(libro1_file, libro2_file):
    # Cargar los datos de los archivos Excel
    df_libro1 = libro1_file
    df_libro2 = libro2_file

    # Realizar la combinación de datos
    merged_df = pd.merge(df_libro1, df_libro2, left_on='puesto funcional', right_on='Puesto Funcional', how='left')

    # Reemplazar valores nulos en las columnas 'Aplicación' y 'Rol' con una cadena vacía
    merged_df['Aplicación'] = merged_df['Aplicación'].fillna('')
    merged_df['Rol'] = merged_df['Rol'].fillna('')

    # Crear una lista para almacenar los resultados finales
    resultados = []

    # Inicializar variables para la aplicación previa y los roles previos por puesto funcional
    prev_apps = {}
    prev_roles = {}

    # Iterar sobre cada fila del DataFrame combinado
    for index, row in merged_df.iterrows():
        # Obtener el puesto funcional de la fila actual
        puesto_funcional = row['puesto funcional']

        # Obtener la aplicación y los roles de la fila actual
        aplicacion = row['Aplicación'].strip()
        rol = row['Rol'].strip()

        # Si la aplicación actual es NaN, usar la aplicación previa del mismo puesto funcional
        if not aplicacion:
            aplicacion = prev_apps.get(puesto_funcional, '')
        else:
            prev_apps[puesto_funcional] = aplicacion

        # Si los roles de la fila actual son diferentes de los roles previos del mismo puesto funcional, agregarlos al resultado
        if rol and rol != prev_roles.get(puesto_funcional, ''):
            # Agregar la aplicación y los roles al resultado
            resultados.append({'puesto funcional': puesto_funcional, 'Aplicación': aplicacion, 'Rol': rol})

        # Actualizar los roles previos por puesto funcional
        prev_roles[puesto_funcional] = rol

    # Crear un DataFrame a partir de los resultados
    final_df = pd.DataFrame(resultados)

    # Agrupar los roles por puesto funcional y aplicaciones y concatenarlos con comas
    final_df = final_df.groupby(['puesto funcional', 'Aplicación'])['Rol'].apply(', '.join).reset_index(name='rol')

    # Unir el DataFrame final con los datos originales de Libro1
    final_df = pd.merge(df_libro1, final_df, on='puesto funcional', how='left')

    # Rellenar valores NaN en la columna 'aplicación -> rol' con una cadena vacía
    final_df['rol'] = final_df['rol'].fillna('')

    # Guardar el resultado en un nuevo archivo Excel
    #final_df.to_excel(output_file, index=False)

    return final_df

# Ejemplo de uso:
# generar_datos_extra('Libro1.xlsx', 'Libro2.xlsx', 'Libro1_con_datos_extra.xlsx')
