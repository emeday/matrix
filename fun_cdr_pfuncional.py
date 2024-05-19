import pandas as pd

def generate_data_cdr_pfuncional(df_libro1, df_libro2, filtro):
    # Realizar la combinación de datos
    merged_df = pd.merge(df_libro1, df_libro2, left_on=['cdr', 'puesto funcional'], right_on=['cdr', 'Puesto Funcional'], how='left')

    # Reemplazar valores nulos en las columnas 'Aplicación' y 'Rol' con una cadena vacía
    merged_df['Aplicación'] = merged_df['Aplicación'].fillna('')
    merged_df['Rol'] = merged_df['Rol'].fillna('')

    # Crear una lista para almacenar los resultados finales
    resultados = []

    # Inicializar variables para la aplicación previa y los roles previos por clave
    prev_apps = {}
    prev_roles = {}

    # Iterar sobre cada fila del DataFrame combinado
    for index, row in merged_df.iterrows():
        # Obtener la clave de la fila actual
        clave = f"{row['cdr']}_{row['puesto funcional']}"

        # Obtener la aplicación y los roles de la fila actual
        aplicacion = row['Aplicación'].strip()
        rol = row['Rol'].strip()

        # Si la aplicación actual es NaN, usar la aplicación previa de la misma clave
        if not aplicacion:
            aplicacion = prev_apps.get(clave, '')
        else:
            prev_apps[clave] = aplicacion

        # Si los roles de la fila actual son diferentes de los roles previos de la misma clave, agregarlos al resultado
        if rol and rol != prev_roles.get(clave, ''):
            # Agregar la aplicación y los roles al resultado
            resultados.append({**row.to_dict(), 'Aplicación': aplicacion, 'Rol': rol})

        # Actualizar los roles previos por clave
        prev_roles[clave] = rol

    # Crear un DataFrame a partir de los resultados
    final_df = pd.DataFrame(resultados)

    # Agrupar los roles por clave y aplicaciones y concatenarlos con comas
    final_df = final_df.groupby(list(df_libro1.columns) + ['Aplicación'])['Rol'].apply(', '.join).reset_index(name='aplicación -> rol')

   
    return final_df



