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

def convert_flac(path, output_format='ALAC'):
    # Diccionario de configuración para diferentes formatos de salida
    formats = {
        'ALAC': {
            'ext': '.m4a', 
            'codec': 'alac', 
            'extra_params': ['-ar', '44100', '-ac', '2', '-sample_fmt', 's16p','-f', 'ipod']
        },
        'WAV': {
            'ext': '.wav', 
            'codec': 'pcm_s16le', 
            'extra_params': []
        },
        'AIFF': {
            'ext': '.aiff', 
            'codec': 'pcm_s16be', 
            'extra_params': []
        },
        'AAC': {
            'ext': '.m4a', 
            'codec': 'aac', 
            'extra_params': ['-ar', '44100', '-ac', '2', '-ab', '320k']
        },
        'MP3': {
            'ext': '.mp3', 
            'codec': 'libmp3lame', 
            'extra_params': ['-ar', '44100', '-ac', '2', '-q:a', '0']
        }
    }
    
    # Crear la carpeta para el formato si no existe
    output_directory = os.path.join(path, output_format)
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Ruta al ejecutable ffmpeg (ajustar según la ubicación real de ffmpeg)
    ffmpeg_executable = r'C:\ffmpeg\bin\ffmpeg.exe'

    # Mapear todos los archivos dentro del path proporcionado
    for filename in os.listdir(path):
        if filename.endswith('.flac'):
            full_path = os.path.join(path, filename)
            new_filename = os.path.splitext(filename)[0] + formats[output_format]['ext']
            new_path = os.path.join(output_directory, new_filename)

            codec = formats[output_format]['codec']
            extra_params = formats[output_format]['extra_params']
            
            command = [ffmpeg_executable, '-i', full_path, '-vn', '-acodec', codec] + extra_params + [new_path]
            
            process = subprocess.run(
                command, stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, text=True
            )
            
            # Imprimir la salida estándar y errores de ffmpeg
            print(process.stdout)
            print(process.stderr)
            
            # Verificar si el proceso no se ejecutó correctamente
            if process.returncode != 0:
                print(f'Error al convertir el archivo {filename}')
