from tkinter import Tk, Label, Entry, Button, messagebox, simpledialog
from tkinter import ttk
from pytube import YouTube
from PIL import Image, ImageTk
import threading
import subprocess
import requests
import os


class YouTubeDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader")

        # Posición y tamaño VENTANA
        window_width = 800
        window_height = 1200
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2

        self.root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
        self.root.configure(bg="gray")  # Color de fondo blanco

        # FONDO MOBIL
        background_image = Image.open("YT15.jpeg")
        background_photo = ImageTk.PhotoImage(background_image)

        # LABEL FONDO
        background_label = Label(root, image=background_photo, bg="white")
        background_label.image = background_photo
        background_label.place(relx=0.5, rely=0.5, anchor="center")

        # POSICIÓN LABELS Y BOTONES
        self.url_label = Label(root, text="Enter the YouTube URL: ", font=("Arial", 14), fg="red", bg="white")
        self.url_label.place(relx=0.5, rely=0.2, anchor="center")

        self.url_entry = Entry(root, width=40, font=("Arial", 12))
        self.url_entry.place(relx=0.5, rely=0.3, anchor="center")

        # ESTILO BOTONES
        style = ttk.Style()
        style.configure("TButton",
                        font=("Arial", 12),
                        padding=10,
                        foreground="white",  # Texto blanco
                        background="red")  # Fondo rojo

        style.map("TButton",
                  foreground=[('active', 'white')],
                  background=[('active', 'dark red')])

        self.download_button = ttk.Button(root, text="Download", command=self.download_video, style="TButton")
        self.download_button.place(relx=0.5, rely=0.8, anchor="center")

        self.info_label = Label(root, text="", wraplength=500, justify="left", font=("Arial", 12), fg="red", bg="white")
        self.info_label.place(relx=0.501, rely=0.45, anchor="center")

    def clear_info_label(self):
        self.info_label.config(text="")

    def show_info(self, info_text):
        self.clear_info_label()
        self.info_label.config(text=info_text)
        self.root.update_idletasks()

    def download_video(self):
        self.clear_info_label()

        url = self.url_entry.get()
        try:
            video_streams = self.sort_streams(url)

            info_text = self.get_quality_info(video_streams)
            self.show_info(info_text)

            choice = self.ask_for_choice(len(video_streams))
            if choice is not None:
                stream_to_download = video_streams[choice - 1]
                video_title = YouTube(url).title
                file_name = f"{video_title}.mp4"

                info_text += f"You are downloading the video '{video_title}' with resolution {stream_to_download.resolution} and format {stream_to_download.mime_type}...\n"
                self.show_info(info_text)

                download_thread = threading.Thread(target=self.download_thread,
                                                   args=(stream_to_download, file_name, video_title))
                download_thread.start()

        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")

    def download_thread(self, stream, file_name, video_title):
        try:
            url = stream.url
            response = requests.get(url, stream=True)
            with open(file_name, 'wb') as file:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        file.write(chunk)

            audio_file_name = f"{video_title}.mp3"
            if self.download_audio(audio_file_name):
                output_file_name = f"{video_title}-.mp4"
                if self.merge_audio_video(file_name, audio_file_name, output_file_name):
                    self.show_info(f"The video '{video_title}' was downloaded successfully!")
                    # Eliminar archivos de video y audio no deseados
                    os.remove(file_name)
                    os.remove(audio_file_name)
        except Exception as e:
            messagebox.showerror("Error during download", f"Error: {str(e)}")

    def download_audio(self, file_name):
        try:
            url = self.url_entry.get()
            yt = YouTube(url)
            audio_stream = yt.streams.filter(only_audio=True).first()
            audio_stream.download(output_path='.', filename=file_name)
            return True
        except Exception as e:
            messagebox.showerror("Error during audio download", f"Error: {str(e)}")
            return False

    def merge_audio_video(self, video_file, audio_file, output_file):
        try:
            # Comando para fusionar el video y el audio usando ffmpeg
            command = ['ffmpeg', '-i', video_file, '-i', audio_file, '-c:v', 'copy', '-c:a', 'aac', '-strict', 'experimental', output_file]
            subprocess.run(command, check=True)
            return True
        except Exception as e:
            messagebox.showerror("Error during audio-video merging", f"Error: {str(e)}")
            return False

    def sort_streams(self, url):
        my_video = YouTube(url)
        return my_video.streams.filter(file_extension='mp4').order_by('resolution')

    def ask_for_choice(self, max_value):
        return simpledialog.askinteger("Choose a quality", "Enter the quality number:", minvalue=1, maxvalue=max_value)

    def get_quality_info(self, video_streams):
        info_text = "Available qualities:\n"
        for i, stream in enumerate(video_streams, 1):
            info_text += f'{i}. {stream.resolution} - {stream.mime_type}\n'
        info_text += "\n"
        return info_text


if __name__ == "__main__":
    root = Tk()
    app = YouTubeDownloaderApp(root)
    root.mainloop()
