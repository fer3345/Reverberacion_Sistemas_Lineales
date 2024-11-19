import numpy as np
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plot
from scipy.io import wavfile
import pygame


def import_audio(audio_name):
    rate, audio = wavfile.read(audio_name)
    if audio.ndim > 1:
        audio = np.mean(audio, axis=1)
    return rate, audio


def convolution(original, impulse_response):
    len_original = len(original)
    len_impulse = len(impulse_response)
    len_output = len_original + len_impulse - 1

    new_audio = np.zeros(len_output)

    print("Realizando convolucion...\n")
    for i in range(len_original):
        new_audio[i:i + len_impulse] += original[i] * impulse_response  #Ocupando la linealidad de la convolución

    print("Se ha realizado la convolución...\n")
    return new_audio


def export_audio(new_audio, sample_rate, name_file):
    new_audio = new_audio / np.max(np.abs(new_audio)) * 32767
    wavfile.write(name_file, sample_rate, new_audio.astype(np.int16))


def resample_audio(audio, rate_original, target_rate):
    if rate_original == target_rate:
        return audio
    duration = len(audio) / rate_original
    target_length = int(duration * target_rate)
    original_indices = np.linspace(0, len(audio) - 1, num=target_length)
    resampled_audio = np.interp(original_indices, np.arange(len(audio)), audio)
    return resampled_audio


def plot_signals(original_audio, impulse_audio, convolution_audio, sample_rate,path_photo):
    time_original = np.linspace(0, len(original_audio) / sample_rate, num=len(original_audio))
    time_impulse = np.linspace(0, len(impulse_audio) / sample_rate, num=len(impulse_audio))
    time_convolution = np.linspace(0, len(convolution_audio) / sample_rate, num=len(convolution_audio))

    plot.figure(figsize=(12, 8))

    plot.subplot(3, 1, 1)
    plot.plot(time_original, original_audio, color='b')
    plot.title("Señal del Audio Original")
    plot.xlabel("Tiempo[s]")
    plot.ylabel("Amplitud")

    plot.subplot(3, 1, 2)
    plot.plot(time_impulse, impulse_audio, color='r')
    plot.title("Respuesta del Impulso")
    plot.xlabel("Tiempo[s]")
    plot.ylabel("Amplitud")

    plot.subplot(3, 1, 3)
    plot.plot(time_convolution, convolution_audio, color='g')
    plot.title("Señal de Audio Convolucionado")
    plot.xlabel("Tiempo[s]")
    plot.ylabel("Amplitud")

    plot.tight_layout()
    plot.savefig(path_photo)


def audio_impulse(audio_path):
    rate, audio = import_audio(audio_path)
    if rate != original_rate:
        audio = resample_audio(audio, rate, original_rate)
        rate = original_rate
    return rate, audio


def play_audios(original, impulse, new_audio):
    print("¿Desea reproducir el audio original?\n1. SI\n2. NO")
    opc = int(input("Ingrese una opcion\n"))
    if opc == 1:
        print("\nReproduciendo Audio Original...")
        pygame.mixer.init()
        pygame.mixer.music.load(original)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

    print("\nReproduciendo Audio del Impulso...")
    pygame.mixer.init()
    pygame.mixer.music.load(impulse)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    print("\nReproduciendo Nuevo Audio...")
    pygame.mixer.init()
    pygame.mixer.music.load(new_audio)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)


original_rate, original_audio = import_audio('Audios/Audio_Original.wav')
option = 0

while option != 5:

    print(
        "1. Convolucionar primer audio.\n2. Convolucionar segundo audio\n3. Convolucionar tercer audio\n4. "
        "Convolucionar cuarto audio\n5. Salir del programa.")
    option = int(input("Ingrese una opcion del menu:\n"))

    match option:
        case 1:
            impulse_rate, impulse_audio = audio_impulse('Audios/IslaMujeresCave.wav')
            convolution_audio = convolution(original_audio, impulse_audio)
            export_audio(convolution_audio, original_rate, 'Audios/Audio1.wav')
            plot_signals(original_audio, impulse_audio, convolution_audio, original_rate, 'Imagenes/Señales_Audio1.png')
            play_audios('Audios/Audio_Original.wav', 'Audios/IslaMujeresCave.wav', 'Audios/Audio1.wav')
        case 2:
            impulse_rate, impulse_audio = audio_impulse('Audios/BatteryQuarles.wav')
            convolution_audio = convolution(original_audio, impulse_audio)
            export_audio(convolution_audio, original_rate, 'Audios/Audio2.wav')
            plot_signals(original_audio, impulse_audio, convolution_audio, original_rate, 'Imagenes/Señales_Audio2.png')
            play_audios('Audios/Audio_Original.wav', 'Audios/BatteryQuarles.wav', 'Audios/Audio2.wav')

        case 3:
            impulse_rate, impulse_audio = audio_impulse('Audios/WaterplacePark.wav')
            convolution_audio = convolution(original_audio, impulse_audio)
            export_audio(convolution_audio, original_rate, 'Audios/Audio3.wav')
            plot_signals(original_audio, impulse_audio, convolution_audio, original_rate, 'Imagenes/Señales_Audio3.png')
            play_audios('Audios/Audio_Original.wav', 'Audios/WaterplacePark.wav', 'Audios/Audio3.wav')

        case 4:
            impulse_rate, impulse_audio = audio_impulse('Audios/Space4ArtGallery.wav')
            convolution_audio = convolution(original_audio, impulse_audio)
            export_audio(convolution_audio, original_rate, 'Audios/Audio4.wav')
            plot_signals(original_audio, impulse_audio, convolution_audio, original_rate, 'Imagenes/Señales_Audio4.png')
            play_audios('Audios/Audio_Original.wav', 'Audios/Space4ArtGallery.wav', 'Audios/Audio4.wav')
        case 5:
            print("Saliendo del programa...\n")