import pandas as pd
import os
from datetime import datetime
import matplotlib.pyplot as plt




def obtener_porcentaje_avance_total_usuarios(archivo_excel,archivo_csv):
    # Leer todas las hojas y concatenarlas
    hojas = ["equipo I", "equipo II", "equipo III"]
    dfs = [pd.read_excel(archivo_excel, sheet_name=hoja) for hoja in hojas]
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

    # Obtener la fecha actual
    fecha_actual = datetime.now().strftime("%Y-%m-%d")

    # Verificar si el archivo CSV existe y si ya tiene datos para la fecha actual
    if os.path.exists(archivo_csv):
        df_csv = pd.read_csv(archivo_csv)
        if 'Fecha' in df_csv.columns and fecha_actual in df_csv['Fecha'].values:
            print(f"El porcentaje de avance para la fecha {fecha_actual} ya existe en el archivo CSV.")
        else:
            # Guardar el porcentaje global de avance y la fecha en el archivo CSV
            with open(archivo_csv, 'a') as f:
                f.write(f"{fecha_actual},{porcentaje_global_avance}\n")
    else:
        # Crear el archivo CSV y agregar la primera fila con encabezado
        with open(archivo_csv, 'w') as f:
            f.write("Fecha,Porcentaje Global de Avance\n")
            f.write(f"{fecha_actual},{porcentaje_global_avance}\n")
    
    return df_analisis, porcentaje_avance_por_usuario, df_concatenado

def obtener_porcentaje_avance_aplicaciones(df_concatenado):
    porcentaje_avance_por_aplicacion = {}
    aplicaciones_completadas = {}
    aplicaciones_pendientes = {}

    # Iterar sobre cada fila del DataFrame
    for _, row in df_concatenado.iterrows():
        app = row['aplicación']
        resultado = row['resultado']
        usuario = row['codigo']

        # Si el resultado no es NaN y no está vacío
        if pd.notna(resultado) and resultado.strip():
            if resultado.strip() == "ok":
                if app not in aplicaciones_completadas:
                    aplicaciones_completadas[app] = set()
                aplicaciones_completadas[app].add(usuario)
            elif resultado.strip() == "pendiente":
                if app not in aplicaciones_pendientes:
                    aplicaciones_pendientes[app] = set()
                aplicaciones_pendientes[app].add(usuario)

    # Calcular el porcentaje de avance para cada aplicación
    for app, usuarios_completados in aplicaciones_completadas.items():
        usuarios_pendientes = aplicaciones_pendientes.get(app, set())
        total_usuarios_app = len(usuarios_completados) + len(usuarios_pendientes)
        total_aplicaciones_app = len(df_concatenado[df_concatenado['aplicación'] == app]['codigo'].unique())

        if total_usuarios_app != 0:
            porcentaje_avance_por_aplicacion[app] = round((len(usuarios_completados) / total_usuarios_app) * 100, 2)
        else:
            porcentaje_avance_por_aplicacion[app] = 0

    # Calcular el porcentaje de avance para aplicaciones pendientes para todos los usuarios
    for app, usuarios_pendientes in aplicaciones_pendientes.items():
        if app not in porcentaje_avance_por_aplicacion:
            porcentaje_avance_por_aplicacion[app] = 0

    # Crear DataFrame de porcentaje de avance por aplicación
    df_porcentaje_avance_aplicaciones = pd.DataFrame.from_dict(porcentaje_avance_por_aplicacion, orient='index', columns=["Porcentaje de Avance"])

    # Contar el total de aplicaciones y las aplicaciones en cada categoría de avance
    total_aplicaciones = len(df_porcentaje_avance_aplicaciones)
    aplicaciones_100 = sum(1 for porcentaje in porcentaje_avance_por_aplicacion.values() if porcentaje == 100)
    aplicaciones_50 = sum(1 for porcentaje in porcentaje_avance_por_aplicacion.values() if porcentaje >= 50 and porcentaje < 100)
    aplicaciones_menos_50 = sum(1 for porcentaje in porcentaje_avance_por_aplicacion.values() if porcentaje < 50)

    # Crear DataFrame de resumen de avance por aplicación
    data_resumen = {
        "Total de Aplicaciones": [total_aplicaciones],
        "Aplicaciones al 100%": [aplicaciones_100],
        "Aplicaciones al 50%": [aplicaciones_50],
        "Aplicaciones menos del 50%": [aplicaciones_menos_50]
    }
    df_resumen = pd.DataFrame(data_resumen)

    return df_porcentaje_avance_aplicaciones, df_resumen

def contar_usuarios_porcentaje_avance(porcentaje_avance_por_usuario):
    total_usuarios = len(porcentaje_avance_por_usuario)
    avance_100 = sum(1 for porcentaje in porcentaje_avance_por_usuario.values() if porcentaje == 100)
    
    # Contar usuarios con avance del 50% excluyendo a los que ya están al 100%
    avance_50 = sum(1 for porcentaje in porcentaje_avance_por_usuario.values() if porcentaje >= 50 and porcentaje < 100 and porcentaje_avance_por_usuario != 100)
    
    # Contar usuarios con avance menos del 50%
    menos_50 = sum(1 for porcentaje in porcentaje_avance_por_usuario.values() if porcentaje < 50)
    
    return total_usuarios, avance_100, avance_50, menos_50

def generar_grafico_lineas(archivo_csv):
    # Leer el archivo CSV
    df_csv = pd.read_csv(archivo_csv)

    # Convertir la columna 'Fecha' a datetime
    df_csv['Fecha'] = pd.to_datetime(df_csv['Fecha'])

    # Ordenar el DataFrame por fecha
    df_csv = df_csv.sort_values('Fecha')

    # Generar el gráfico de líneas
    plt.figure(figsize=(10, 6))
    plt.plot(df_csv['Fecha'], df_csv['Porcentaje Global de Avance'], marker='o')
    plt.xlabel('Fecha')
    plt.ylabel('Porcentaje Global de Avance')
    plt.title('Avance Global por Día')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("grafico_avance.png")
    plt.show()