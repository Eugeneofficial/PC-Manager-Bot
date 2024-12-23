import os
import pyaudio
import wave
from . import BotPlugin
from telegram import Update
from telegram.ext import ContextTypes

class AudioPlugin(BotPlugin):
    """Плагин для записи звука с микрофона"""
    
    @property
    def name(self) -> str:
        return "Audio"
        
    @property
    def description(self) -> str:
        return "Запись звука с микрофона"
        
    @property
    def buttons(self) -> list:
        return [["🎤 Запись 5 сек", "🎤 Запись 10 сек"]]
        
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if "🎤 Запись" in update.message.text:
            try:
                # Определяем длительность записи
                duration = 5 if "5 сек" in update.message.text else 10
                
                await update.message.reply_text(f"🎤 Запись {duration} секунд...")
                
                # Параметры записи
                CHUNK = 1024
                FORMAT = pyaudio.paInt16
                CHANNELS = 1
                RATE = 44100
                
                # Инициализируем PyAudio
                p = pyaudio.PyAudio()
                
                # Открываем поток для записи
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
                
                # Сохраняем в WAV
                wf = wave.open("microphone.wav", 'wb')
                wf.setnchannels(CHANNELS)
                wf.setsampwidth(p.get_sample_size(FORMAT))
                wf.setframerate(RATE)
                wf.writeframes(b''.join(frames))
                wf.close()
                
                # Отправляем файл
                await update.message.reply_audio(
                    audio=open("microphone.wav", "rb"),
                    caption=f"🎤 Запись {duration} сек"
                )
                
                # Удаляем временный файл
                os.remove("microphone.wav")
                
            except Exception as e:
                await update.message.reply_text(f"❌ Ошибка: {str(e)}")
                
            return True
            
        return False 