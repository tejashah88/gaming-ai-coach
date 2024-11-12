from modules.text_to_speech.offline.windows_tts import WindowsTTS


if __name__ == '__main__':
    tts_voice = WindowsTTS()
    tts_voice.set_voice_settings(rate=2.00, volume=1.00)
    tts_voice.speak('Hello world!')
