import os
import subprocess

def get_fixed_song_name(path):
    
    # Lista todos los archivos en la carpeta.
    archives = os.listdir(path)
    
    # Itera sobre cada archivo en la carpeta.
    for arch_name in archives:
        # Construye la ruta completa al archivo.
        full_path = os.path.join(path, arch_name)
        
        # Verifica si es un archivo (no una carpeta).
        if os.path.isfile(full_path):
            # Encuentra el primer punto seguido de un espacio en el nombre del archivo.
            index = arch_name.find('. ')
            # Si encuentra el patrón, procede a renombrar.
            if index != -1:
                # El nuevo nombre será la parte del nombre del archivo después del "n. ".
                new_name = arch_name[index+2:]
                # Construye la ruta completa con el nuevo nombre.
                new_path = os.path.join(path, new_name)
                # Renombra el archivo.
                try:
                    os.rename(full_path, new_path)
    
                except:
                    os.remove(full_path)

def convert_flac_to_alac(path):
    # Crear la carpeta ALAC si no existe
    alac_directory = os.path.join(path, "ALAC")
    if not os.path.exists(alac_directory):
        os.makedirs(alac_directory)

    # Ruta al ejecutable ffmpeg
    ffmpeg_executable = r'C:\ffmpeg\bin\ffmpeg.exe' # Suponiendo que tu ffmpeg esta en disco C

    # Mapear todos los archivos dentro del path proporcionado
    for filename in os.listdir(path):
        # Comprobar si el archivo actual es un archivo FLAC
        if filename.endswith('.flac'):
            # Construir el path completo del archivo FLAC
            full_path = os.path.join(path, filename)
            # Construir el nuevo path dentro de la carpeta ALAC, con la extensión .m4a
            new_path = os.path.join(alac_directory, os.path.splitext(filename)[0] + '.m4a')

            # Ejecutar el comando ffmpeg para convertir de FLAC a ALAC sin procesar video
            process = subprocess.run(
                [ffmpeg_executable, '-i', full_path, '-vn', '-acodec', 'alac', new_path],
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                text=True
            )
            
            # Imprimir la salida estándar y errores de ffmpeg
            print(process.stdout)
            print(process.stderr)

            # Verificar si el proceso no se ejecutó correctamente
            if process.returncode != 0:
                print(f'Error al convertir el archivo {filename}')
