# Connection
![image](https://user-images.githubusercontent.com/87471423/128171382-69617967-bb53-468e-81e2-62d5eac8264d.png)

-> Library, die es ermöglicht Daten an den Sever bzw. Client zu senden, ohne Daten dabei zu verlieren!

# Funktionen:
    o senden von Bildern zum Sever
    o senden von GIFS zum Sever
    o senden von MP3-Dateien zum Sever
    o senden von strings zum Sever
    o senden von executierbaren Funktionen mittels op_code zum Sever
    o Senden von strings zum Client
    
    -> Anmerkung:
       -> Der Sever (PI) soll alleine interargieren das heißt:
          o Alle Daten, die gesendet werden, müssen im ROM gespeichert werden
          o Erst wenn die Daten am ROM gespeichert sind, kann mit ihnen interargiert werden
            -> Ermögklicht sicherheit (keine Daten die verloren gehen können durch latenz

# Benötigte Librarys
    o socket:    -> Für die INET4 Verbindung zwischen Sever und Client
                 -> pip install socket
    o pickle:    -> Für die kompremierung von Daten, damit diese sich über den Socket senden lassen
                 -> pip3 install pickle
    o numpy:     -> Für die Datenverarbeitung der Numpy Arrays
                 -> pip install numpy
    o pydub:     -> Für die convertierung einer mp3 Datein in einen numpy array und zurück
                 -> pip install pydub
    o PILLOW:    -> Für das erstellen von GIFS und speichern am Sever
                 -> pip install pillow
    o opencv:    -> Für das speichern einzelner Bilder und anzeigen von GIFS zum debugging
                 -> pip install opencv-python
    o threading: -> für das abspielen einer mp3-Datei am Sever auch nasch schließung der Verbindung
                 -> pip install threading
    o pygame:    -> Für das abspielen von mp3-Dateien am Sever
                 -> pip install pygame

# Op-Code Tabelle für den Sever:
    o ss   -> speichert einen string in einem Textdokument am Sever
           -> args: (path_to_write, string_to_write, mode) mode = ('a' or 'w' or 'r+')
           
    o si   -> speichert ein Bild am Sever
           -> args: (image_data, data_name)
           
    o sm   -> speichert eine MP3-Datei am Sever
           -> args: (frame_rate, audio_data, file_name)
           
    o sg   -> speichert einen GIF am Sever
           -> args: (gif_fps, gif_data, file_name)
           
    o srto -> setzt ein neues Time Out für das Empfangen von Daten am Sever
           -> args: (int(time_out), ) 
           
    o cc   -> schießt die Verbindung zum Client am Sever
           -> args: (True, True)
           
    o ri   -> zeigt ein Bild am Pixel Boy
           -> args: (image_path) # image path on the Sever
           
    o rg   -> zeigt einen GIF am Pixel Boy
           -> args: (gif_path) # gif path on the Sever
           
    o rm   -> spielt eine MP3-Datein am Pixel Boy ab
           -> args: (mp3_path, thread) # if thread is True: the music will be continue after closing the socket
           
    o pm   -> pausiert die gerade spielende MP3-Datei
           -> args: (True, True)
           
    o um   -> setzt die gerade pausierte MP3-Datei fort
           -> args: (thread) # if thread is True: the music will be continue after closing the connection
           
    o sv   -> setzt ein Volumen für die gerade spielende MP3-Datei 
           -> args: (volume) (max=1, min = 0)
           
    o sptt -> setzt die Variable pass_time_out zu True -> Bewirkt, dass sich der Sever nicht meldet, 
              wenn kein op_code empfangen wurde
           -> args: (True, True)
           
    o sptf -> setzt die Variable pass_time_out zu False -> Bewirkt, dass sich der Sever beim Client
              in form von senden eines Time Out Errors (<'TimeOut>') beim Client meldet, wenn kein
              neuer op_code empfangen wurde
           -> args: (True, True)
           
    Bemerkung: args müssen immer ein tuple sein!!!!

# Verwendung:
    -> Für einen Test kann am Client (PC) das Programm connection_lib.py gestartet werden und am Sever das Programm Connection.py
    -> Beachte dabei, dass das Programm Connection.py zuerst gestartet wird

# Anmerkungen:
    -> Diese Library wird in laufe der Zeit immer wieder erneuert, in form von vergrößerung der op_code Tabelle
   
