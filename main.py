import configparser
import pandas as pd
from fun_cdr_pfuncional import generate_data_cdr_pfuncional
from fun_pfuncional import generate_data_pfuncional
from datetime import datetime

# Capturar la fecha y hora actual
fecha_actual = datetime.now()

def emeday():
    text = '''
    created by ©

▓█████  ███▄ ▄███▓▓█████ ▓█████▄  ▄▄▄      ▓██   ██▓
▓█   ▀ ▓██▒▀█▀ ██▒▓█   ▀ ▒██▀ ██▌▒████▄     ▒██  ██▒
▒███   ▓██    ▓██░▒███   ░██   █▌▒██  ▀█▄    ▒██ ██░
▒▓█  ▄ ▒██    ▒██ ▒▓█  ▄ ░▓█▄   ▌░██▄▄▄▄██   ░ ▐██▓░
░▒████▒▒██▒   ░██▒░▒████▒░▒████▓  ▓█   ▓██▒  ░ ██▒▓░
░░ ▒░ ░░ ▒░   ░  ░░░ ▒░ ░ ▒▒▓  ▒  ▒▒   ▓▒█░   ██▒▒▒ 
 ░ ░  ░░  ░      ░ ░ ░  ░ ░ ▒  ▒   ▒   ▒▒ ░ ▓██ ░▒░ 
   ░   ░      ░      ░    ░ ░  ░   ░   ▒    ▒ ▒ ░░  
   ░  ░       ░      ░  ░   ░          ░  ░ ░ ░     
                          ░                 ░ ░     

    '''
    print(text)

def main():
    # Leer los parámetros desde el archivo de configuración
    config = configparser.ConfigParser()
    config.read('config.properties')

    libro1_path = config['FILES']['pathINUserData']
    libro2_path = config['FILES']['pathINMatrix']
    flag_filtro = config['FILES']['filtro']

    pathOUTpf = config['FILES']['pathOUTpf']
    pathOUTcdrpf = config['FILES']['pathOUTcdrpf']

    
    fecha_formateada = fecha_actual.strftime("%d%m%Y")  
    output_file_pf= pathOUTpf.replace("fecha", f"_{fecha_formateada}")
    output_file_cdr_pf= pathOUTcdrpf.replace("fecha", f"_{fecha_formateada}")

    # Cargar los DataFrames desde los archivos xlsx
    df_libro1 = pd.read_excel(libro1_path)
    df_libro2 = pd.read_excel(libro2_path)


    flag_filtro = int(flag_filtro)

    if flag_filtro ==0:
        # Llamar a la función para generar los datos filtrados solo por puesto funcional
        df_datos_extra_only_pf = generate_data_pfuncional(df_libro1, df_libro2)

        # Guardar el resultado en un nuevo archivo Excel
        #output_file_pf = f'Libro1_con_datos_{filtro.replace(" ", "_")}.xlsx'
        df_datos_extra_only_pf.to_excel(output_file_pf, index=False)

        print(f"Se ha generado el archivo {output_file_pf}")
    elif flag_filtro == 1:
        filtro ="CDR y Puesto Funcional"
        # Llamar a la función para generar los datos filtrados por cdr y puesto funconal
        df_datos_extra_cdr_pf = generate_data_cdr_pfuncional(df_libro1, df_libro2, filtro)

        # Guardar el resultado en un nuevo archivo Excel
        output_file_cdr_pf = f'Libro1_con_datos_{filtro.replace(" ", "_")}.xlsx'
        df_datos_extra_cdr_pf.to_excel(output_file_cdr_pf, index=False)

        print(f"Se ha generado el archivo {output_file_cdr_pf}")

    

if __name__ == "__main__":
    emeday()
    main()
