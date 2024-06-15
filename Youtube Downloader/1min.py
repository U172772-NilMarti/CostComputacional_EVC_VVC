import os
from moviepy.video.io.VideoFileClip import VideoFileClip

# Ruta al directorio principal del USB
usb_path = '/media/nil/VIDEOS_TFG'


# Función para cortar un video a 1 minuto y borrar el original
def cortar_video(video_path):
    # Nombre del archivo sin la extensión
    file_name = os.path.splitext(os.path.basename(video_path))[0]

    # Directorio donde se guardará el video cortado
    output_path = os.path.join(os.path.dirname(video_path), file_name + '-.mp4')

    # Cargar el video
    video = VideoFileClip(video_path)

    # Cortar el video a 1 minuto (60 segundos)
    video_cortado = video.subclip(0, 60)

    # Guardar el video cortado
    video_cortado.write_videofile(output_path, codec='libx264', fps=video.fps)

    # Cerrar el video original y el video cortado
    video.close()
    video_cortado.close()

    # Eliminar el video original
    os.remove(video_path)


# Recorrer todas las carpetas y archivos dentro del USB
for root, dirs, files in os.walk(usb_path):
    for file in files:
        # Verificar si el archivo es un video
        if file.endswith(('.mp4', '.avi', '.mkv', '.mov')):
            # Obtener la ruta completa del video
            video_path = os.path.join(root, file)
            # Cortar el video a 1 minuto y borrar el original
            cortar_video(video_path)