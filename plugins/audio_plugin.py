import os
import wave
import pyaudio
from telegram import InlineKeyboardButton
from plugins import BotPlugin

class AudioPlugin(BotPlugin):
    @property
    def name(self) -> str:
        return "Микрофон"
        
    @property
    def description(self) -> str:
        return "Запись звука с микрофона"
        
    @property
    def buttons(self) -> list:
        return [
            [
                InlineKeyboardButton("🎤 5 сек", callback_data="audio_5"),
                InlineKeyboardButton("🎤 10 сек", callback_data="audio_10")
            ]
        ]
        
    async def handle_callback(self, callback_data: str, update, context) -> bool:
        if callback_data.startswith("audio_"):
            try:
                # Получаем длительность записи
                duration = int(callback_data.split("_")[1])
                
                # Настройки записи
                CHUNK = 1024
                FORMAT = pyaudio.paInt16
                CHANNELS = 1
                RATE = 44100
                
                # ��нициализируем PyAudio
                p = pyaudio.PyAudio()
                stream = p.open(format=FORMAT,
                              channels=CHANNELS,
                              rate=RATE,
                              input=True,
                              frames_per_buffer=CHUNK)
                
                # Записываем звук
                frames = []
                for i in range(0, int(RATE / CHUNK * duration)):
                    data = stream.read(CHUNK)
                    frames.append(data)
                
                # Закрываем поток
                stream.stop_stream()
                stream.close()
                p.terminate()
                
                # Сохраняем WAV
                wf = wave.open("microphone.wav", 'wb')
                wf.setnchannels(CHANNELS)
                wf.setsampwidth(p.get_sample_size(FORMAT))
                wf.setframerate(RATE)
                wf.writeframes(b''.join(frames))
                wf.close()
                
                # Отправляем аудио
                await update.callback_query.message.reply_audio(
                    audio=open("microphone.wav", "rb"),
                    caption=f"🎤 Запись {duration} сек"
                )
                
                # Удаляем временный файл
                os.remove("microphone.wav")
                
            except Exception as e:
                await update.callback_query.message.reply_text(f"❌ Ошибка: {str(e)}")
            return True
            
        return False 