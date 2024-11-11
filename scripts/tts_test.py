from services.tts_voice import TTSVoice


if __name__ == '__main__':
    tts_voice = TTSVoice()
    tts_voice.set_voice_settings(rate=2.00, volume=1.00)
    tts_voice.speak('Hello world!')
