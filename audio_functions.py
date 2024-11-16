import speech_recognition
import pyttsx3
import time
import pyaudio
import wave
import tempfile
import keyboard


def record_audio(sample_rate=16000, channels=1, chunk=2048):
    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16,
        channels=channels,
        rate=sample_rate,
        input=True,
        frames_per_buffer=chunk,
    )
    button = 'shift'
    print(f"Нажмите и удерживайте кнопку {button}, чтобы начать запись...")
    frames = []
    keyboard.wait(button)
    print("Запись... (Отпустите PAUSE, чтобы остановить)")
    while keyboard.is_pressed(button):
        data = stream.read(chunk)
        frames.append(data)
    print("Запись завершена.")
    stream.stop_stream()
    stream.close()
    p.terminate()
    return frames, sample_rate


def save_audio(frames, sample_rate):
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
        wf = wave.open(temp_audio.name, "wb")
        wf.setnchannels(1)
        wf.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))
        wf.setframerate(sample_rate)
        wf.writeframes(b"".join(frames))
        wf.close()
        return temp_audio.name


def listen():
    try:
        frames, sample_rate = record_audio()
        file = save_audio(frames, sample_rate)
        sample = speech_recognition.AudioFile(file)
        r = speech_recognition.Recognizer()
        with sample as audio:
            content = r.record(audio)
            r.adjust_for_ambient_noise(audio)
        return r.recognize_google(content, language="ru-RU").lower()
    except speech_recognition.UnknownValueError: 
            return ''


def say(text_to_speech):
    time.sleep(1)
    ttsEngine.say(str(text_to_speech))
    ttsEngine.runAndWait()


ttsEngine = pyttsx3.init()
voices = ttsEngine.getProperty("voices")
ttsEngine.setProperty("voice", voices[0].id)