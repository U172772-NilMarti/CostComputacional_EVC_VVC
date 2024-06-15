import os
import shutil
import subprocess
import time


def ejecutar_nmon(ruta):
    # Crear la carpeta si no existe
    if not os.path.exists(ruta):
        os.makedirs(ruta)

    # Cambiar al directorio donde se guardarán los archivos nmon
    os.chdir(ruta)

    # Ejecutar el comando para iniciar nmon y guardar la salida en un archivo
    os.system("nmon -f -s 5")


def detener_proceso_nmon(ruta_carpeta):
    # Verificar si la ruta especificada es un directorio válido
    if not os.path.isdir(ruta_carpeta):
        print("La ruta especificada no es un directorio válido.")
        return

    # Obtener la lista de archivos en la carpeta
    archivos_en_carpeta = os.listdir(ruta_carpeta)

    # Filtrar los archivos .nmon en la carpeta
    archivos_nmon = [archivo for archivo in archivos_en_carpeta if archivo.endswith(".nmon")]

    # Verificar si se encontraron archivos .nmon en la carpeta
    if not archivos_nmon:
        print("No se encontraron archivos .nmon en la carpeta especificada.")
        return

    # Buscar procesos nmon en ejecución
    try:
        output = subprocess.check_output(["pgrep", "nmon"]).decode("utf-8").strip()
        pids = output.split("\n")
    except subprocess.CalledProcessError:
        print("No se encontraron procesos nmon en ejecución.")
        return

    # Detener el proceso nmon asociado a cada archivo .nmon encontrado
    for archivo_nmon in archivos_nmon:
        for pid in pids:
            try:
                subprocess.run(["kill", pid])
                print(f"Proceso nmon asociado con '{archivo_nmon}' detenido.")
                break  # Salir del bucle una vez que se haya detenido el proceso nmon
            except Exception as e:
                print(f"Error al detener el proceso nmon asociado con '{archivo_nmon}': {e}")

def analizar_archivo_nmon(ruta):
    # Cambiar al directorio donde se encuentran los archivos nmon
    os.chdir(ruta)

    # Obtener el nombre del archivo nmon
    archivos_nmon = [archivo for archivo in os.listdir() if archivo.endswith(".nmon")]

    # Verificar si hay archivos nmon
    if not archivos_nmon:
        print("No se encontraron archivos nmon en la carpeta especificada.")
        return

    # Ejecutar el comando pyNmonAnalyzer para analizar el archivo nmon
    for archivo_nmon in archivos_nmon:
        comando = f"pyNmonAnalyzer -c -o testOut -i {archivo_nmon}"
        os.system(comando)

def convertir_a_yuv(video_path, output_path):

    comando = ["ffmpeg", "-i", video_path, "-pix_fmt", "yuv420p", output_path]
    try:
        # Ejecuta el comando ffmpeg
        subprocess.run(comando, check=True)
        print("Conversión completada.")
    except subprocess.CalledProcessError as e:
        print("Error al convertir el video:", e)


def get_video_resolution(video_path):
    # Comando para obtener la resolución del video usando ffmpeg
    command = ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=s=x:p=0", video_path]
    # Ejecutar el comando y obtener la salida
    output = subprocess.check_output(command).decode().strip()
    # Dividir la salida en ancho y alto
    width, height = map(int, output.split("x"))
    return width, height


def borrar_contenido_carpeta(carpeta):
    # Obtener la lista de archivos y directorios en la carpeta
    contenido = os.listdir(carpeta)

    # Recorrer el contenido y borrar cada elemento
    for elemento in contenido:
        elemento_path = os.path.join(carpeta, elemento)
        # Verificar si el elemento es un archivo o un directorio
        if os.path.isfile(elemento_path):
            os.remove(elemento_path)  # Borrar archivo
        elif os.path.isdir(elemento_path):
            # Eliminar directorio recursivamente
            shutil.rmtree(elemento_path)


def iniciar_contador():
    inicio = time.time()  # Obtiene el tiempo actual en segundos
    return inicio

def detener_contador(inicio):
    fin = time.time()  # Obtiene el tiempo actual en segundos
    tiempo_transcurrido = fin - inicio  # Calcula la diferencia de tiempo
    return tiempo_transcurrido
