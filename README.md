# Estudi dels codificadors EVC i VVC i càlcul del seu rendiment computacional
Aquest repositori s'ha creat per oferir una eina de codi obert a tothom que vulgui calcular el rendiment i cost computacional del procés de codificació amb còdecs EVC, ffmpeg EVC o VVC.

En aquest repositori trobarem dues carpetes, una per veure els arxius de com he extret les dades i pujades a la base de dades, i l'altra carpeta per veure com he fet l'aplicació per descarregar vídeos de YouTube.

Per poder fer l'extracció de les dades de forma còmoda i eficient, he creat un petit menú des de la
consola de Python, on l'usuari ha de triar entre el tipus de còdec que vol utilitzar. Si l’usuari introdueix
el número 1, s'utilitza el codificador Versatile Video Coding, el número 2 s'usarà el còdec Essential
Video Coding, i si es prem el 3 s'usarà la versió amb ffmpeg d'Essential Video Coding. L'opció 4 és
per sortir d'aquest menú en cas de voler sortir de l'execució.

Utilitzant les llibreries pytube i tkinter, vaig fer una interfície gràfica amb python on
utilitzant el link de l’url del vídeo de YouTube desitjat, permet descarregar-lo en diferents qualitats.
