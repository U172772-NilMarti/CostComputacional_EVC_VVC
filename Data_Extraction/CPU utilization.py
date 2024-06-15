import os
import pandas as pd
import functions
import mysql.connector
import subprocess


def error_message():
    print("El input de l'usuari és incorrecte. Ha de ser 1, 2, 3 o 4.")

def vvc_encoder(video_path, yuv_path):
    # Obtener la resolución del video
    width, height = functions.get_video_resolution(video_path)
    functions.convertir_a_yuv(video_path, yuv_path)

    if width is None or height is None:
        print("No se pudo obtener la resolución del video.")
        return

    resolution = f"{width}x{height}"

    output_VVC = "/home/nil/Desktop/VVC_files/output_codification/output.266"
    ruta_VVC = "/home/nil/Desktop/VVC_files/output_codification"

    ruta_nmon = "/home/nil/Desktop/VVC_files/nmon_videos"
    functions.ejecutar_nmon(ruta_nmon)

    command = ["vvencapp", "--preset", "medium", "-i", yuv_path, "-s", resolution, "-r", "25", "-o",
               output_VVC]

    inicio = functions.iniciar_contador()

    try:
        subprocess.run(command, check=True)
        print("Codificación completada.")
    except subprocess.CalledProcessError as e:
        print("Error durante la codificación:", e)

    execution_time = functions.detener_contador(inicio)
    functions.detener_proceso_nmon(ruta_nmon)
    functions.analizar_archivo_nmon(ruta_nmon)

    # Cargar el archivo CSV en un DataFrame
    df = pd.read_csv('/home/nil/Desktop/VVC_files/nmon_videos/testOut/csv/CPU_ALL.csv')
    # Calcular la media de la columna 'User%' y Sys%
    CPU_user = df['User%'].mean()
    CPU_system = df['Sys%'].mean()
    df2 = pd.read_csv('/home/nil/Desktop/VVC_files/nmon_videos/testOut/csv/MEM.csv')
    RAM_active = df2['active'].mean()

    # BORRAR CONTINGUT DE LES CARPETES UNA VEGADA EL VIDEO S'HA CODIFICAT, EXTRET LES DADES I GUARDADES EN VARIABLES
    functions.borrar_contenido_carpeta(ruta_nmon)
    functions.borrar_contenido_carpeta(ruta_VVC)
    functions.borrar_contenido_carpeta(yuv_path_carpeta)

    print("CPU_USER: ", CPU_user)
    print("CPU_SYS: ", CPU_system)
    print("RAM: ", RAM_active)
    print("TIME: ", execution_time)

    return CPU_user, CPU_system, RAM_active, execution_time


def evc_encoder(video_path, yuv_path):
    # Obtindre la resolució del video
    width, height = functions.get_video_resolution(video_path)
    functions.convertir_a_yuv(video_path, yuv_path)

    if width is None or height is None:
        print("No se pudo obtener la resolución del video.")
        return

    # Convertir la resolució a cadenas de text
    width_str = str(width)
    height_str = str(height)

    output_EVC = "/home/nil/Desktop/EVC_files/output_codification/output.evc"
    ruta_EVC = "/home/nil/Desktop/EVC_files/output_codification"

    ruta_nmon = "/home/nil/Desktop/EVC_files/nmon_videos"
    functions.ejecutar_nmon(ruta_nmon)

    command = ["xeveb_app", "-i", yuv_path, "-w", width_str, "-h", height_str, "-z", "25", "-o",
               output_EVC]

    inicio = functions.iniciar_contador()

    try:
        subprocess.run(command, check=True)
        print("Codificación completada.")
    except subprocess.CalledProcessError as e:
        print("Error durante la codificación:", e)

    execution_time = functions.detener_contador(inicio)
    functions.detener_proceso_nmon(ruta_nmon)
    functions.analizar_archivo_nmon(ruta_nmon)

    # Cargar el archivo CSV en un DataFrame
    df = pd.read_csv('/home/nil/Desktop/EVC_files/nmon_videos/testOut/csv/CPU_ALL.csv')
    # Calcular la media de la columna 'User%' y Sys%
    CPU_user = df['User%'].mean()
    CPU_system = df['Sys%'].mean()
    df2 = pd.read_csv('/home/nil/Desktop/EVC_files/nmon_videos/testOut/csv/MEM.csv')
    RAM_active = df2['active'].mean()

    # BORRAR CONTINGUT DE LES CARPETES UNA VEGADA EL VIDEO S'HA CODIFICAT, EXTRET LES DADES I GUARDADES EN VARIABLES
    functions.borrar_contenido_carpeta(ruta_nmon)
    functions.borrar_contenido_carpeta(ruta_EVC)
    functions.borrar_contenido_carpeta(yuv_path_carpeta)

    print("CPU_USER: ", CPU_user)
    print("CPU_SYS: ", CPU_system)
    print("RAM: ", RAM_active)
    print("TIME: ", execution_time)

    return CPU_user, CPU_system, RAM_active, execution_time


def evc_ffmpeg_encoder(video_path, yuv_path):
    # Obtener la resolución del video
    width, height = functions.get_video_resolution(video_path)
    functions.convertir_a_yuv(video_path, yuv_path)

    if width is None or height is None:
        print("No se pudo obtener la resolución del video.")
        return

    # Convertir la resolución a cadenas de texto
    resolution = f"{width}x{height}"

    output_EVC_ffmpeg = "/home/nil/Desktop/EVC_ffmpeg_files/output_codification/output.evc"
    ruta_EVC_ffmpeg = "/home/nil/Desktop/EVC_ffmpeg_files/output_codification"

    ruta_nmon = "/home/nil/Desktop/EVC_ffmpeg_files/nmon_videos"
    functions.ejecutar_nmon(ruta_nmon)

    command = ["ffmpeg", "-f", "rawvideo", "-pix_fmt", "yuv420p", "-s:v", resolution, "-r", "25", "-i", yuv_path, "-c:v",
               "libxeve", "-f", "rawvideo" , output_EVC_ffmpeg]

    inicio = functions.iniciar_contador()

    try:

        subprocess.run(command, check=True)
        print("Codificación completada.")
    except subprocess.CalledProcessError as e:
        print("Error durante la codificación:", e)

    execution_time = functions.detener_contador(inicio)
    functions.detener_proceso_nmon(ruta_nmon)
    functions.analizar_archivo_nmon(ruta_nmon)

    # Cargar el archivo CSV en un DataFrame
    df = pd.read_csv('/home/nil/Desktop/EVC_ffmpeg_files/nmon_videos/testOut/csv/CPU_ALL.csv')
    # Calcular la media de la columna 'User%' y Sys%
    CPU_user = df['User%'].mean()
    CPU_system = df['Sys%'].mean()
    df2 = pd.read_csv('/home/nil/Desktop/EVC_ffmpeg_files/nmon_videos/testOut/csv/MEM.csv')
    RAM_active = df2['active'].mean()

    # BORRAR CONTINGUT DE LES CARPETES UNA VEGADA EL VIDEO S'HA CODIFICAT, EXTRET LES DADES I GUARDADES EN VARIABLES
    functions.borrar_contenido_carpeta(ruta_nmon)
    functions.borrar_contenido_carpeta(ruta_EVC_ffmpeg)
    functions.borrar_contenido_carpeta(yuv_path_carpeta)

    print("CPU_USER: ", CPU_user)
    print("CPU_SYS: ", CPU_system)
    print("RAM: ", RAM_active)
    print("TIME: ", execution_time)

    return CPU_user, CPU_system, RAM_active, execution_time


def aplicar_codificacion(video_path, option, yuv_path):
    match option:
        case 1:
            #VVC ENCODER
            return vvc_encoder(video_path, yuv_path)

        case 2:
            #EVC ENCODER
            return evc_encoder(video_path, yuv_path)

        case 3:
            # FFMPEG ENCODER
            return evc_ffmpeg_encoder(video_path, yuv_path)
        case 4:
            # EXIT
            print("Sortint del programa")
            return 0
        case _:
            error_message()


# Connexió a la base de dades MySQL
conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="NmV008$$",
    database="TFG_DATABASE"
)
cursor = conexion.cursor()

# Ruta de la carpeta principal
carpeta_principal = '/media/nil/VIDEOS_TFG'


# Base de dades MySQL
query = """
CREATE TABLE IF NOT EXISTS VIDEOS (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255),
    categoria VARCHAR(255)
);
"""

cursor.execute(query)
cursor.fetchall()  # Netejar resultats pendents

query = """
CREATE TABLE IF NOT EXISTS VVC_ENCODER (
    id INT AUTO_INCREMENT PRIMARY KEY,
    CPU_user FLOAT,
    CPU_system FLOAT,
    RAM_active FLOAT,
    execution_time FLOAT 
);
"""

cursor.execute(query)
cursor.fetchall()  # Netejar resultats pendents

query = """
CREATE TABLE IF NOT EXISTS EVC_ENCODER (
    id INT AUTO_INCREMENT PRIMARY KEY,
    CPU_user FLOAT,
    CPU_system FLOAT,
    RAM_active FLOAT,
    execution_time FLOAT
);
"""

cursor.execute(query)
cursor.fetchall()  # Netejar resultats pendents

query = """
CREATE TABLE IF NOT EXISTS EVC_FFMPEG_ENCODER (
    id INT AUTO_INCREMENT PRIMARY KEY,
    CPU_user FLOAT,
    CPU_system FLOAT,
    RAM_active FLOAT,
    execution_time FLOAT
);
"""

cursor.execute(query)
conexion.commit()

#Menú de l'aplicació a la terminal
menu = {
    1: "VVC encoder",
    2: "EVC encoder",
    3: "FFMPEG EVC encoder",
    4: "Exit"
}

# Imprimir el mensaje inicial
print("Tria una opció del 1 al 4")
print("----------------------------------")

# Imprimir las opciones en el formato deseado
for key, value in menu.items():
    print(f"Opció {key}: {value}")

opcio = int(input("Opció: "))


conexion.commit()

# Reiniciar el contador de ID autoincremental en 1
cursor.execute("ALTER TABLE VIDEOS AUTO_INCREMENT = 1")
cursor.execute("ALTER TABLE VVC_ENCODER AUTO_INCREMENT = 1")
cursor.execute("ALTER TABLE EVC_ENCODER AUTO_INCREMENT = 1")
cursor.execute("ALTER TABLE EVC_FFMPEG_ENCODER AUTO_INCREMENT = 1")
conexion.commit()

yuv_path = "/home/nil/Desktop/YUV_videos/video.yuv"
yuv_path_carpeta = "/home/nil/Desktop/YUV_videos"

# Recorrem la carpeta principal y les seves subcarpetas
for categoria in os.listdir(carpeta_principal):
    categoria_path = os.path.join(carpeta_principal, categoria)
    if os.path.isdir(categoria_path):
        for video_file in os.listdir(categoria_path):
            if video_file.endswith('.mp4'):
                video_path = os.path.join(categoria_path, video_file)

                # Aplicar la función de codificació al vídeo
                CPU_user, CPU_system, RAM_active, execution_time = aplicar_codificacion(video_path, opcio, yuv_path)
                functions.borrar_contenido_carpeta(yuv_path_carpeta)

                # Obtindre el nom del vídeo
                nombre_video = os.path.splitext(video_file)[0]

                # Insertar información a la base de dades

                # QUERY 1 (taula 1) només ho necessitem executar un cop
                insert_query1 = "INSERT INTO VIDEOS (nombre, categoria) VALUES (%s, %s)"
                data1 = (nombre_video, categoria)
                cursor.execute(insert_query1, data1)
                conexion.commit()

                # QUERY 2 (taula 2)
                if opcio == 1:
                    insert_query2 = "INSERT INTO VVC_ENCODER (CPU_user, CPU_system, RAM_active, execution_time) VALUES (%s, %s, %s, %s)"
                    data2 = (CPU_user, CPU_system, RAM_active, execution_time)
                    cursor.execute(insert_query2, data2)
                    conexion.commit()

                elif opcio == 2:
                    # QUERY 3 (taula 3)
                    insert_query3 = "INSERT INTO EVC_ENCODER (CPU_user, CPU_system, RAM_active, execution_time) VALUES (%s, %s, %s, %s)"
                    data3 = (CPU_user, CPU_system, RAM_active, execution_time)
                    cursor.execute(insert_query3, data3)
                    conexion.commit()

                elif opcio == 3:
                    # QUERY 3 (taula 3)
                    insert_query3 = "INSERT INTO EVC_FFMPEG_ENCODER (CPU_user, CPU_system, RAM_active, execution_time) VALUES (%s, %s, %s, %s)"
                    data4 = (CPU_user, CPU_system, RAM_active, execution_time)
                    cursor.execute(insert_query3, data4)
                    conexion.commit()



# Tancar connexió con la base de dades
conexion.close()



