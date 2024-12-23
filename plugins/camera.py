import cv2
import os
from . import BotPlugin
from telegram import Update
from telegram.ext import ContextTypes

class CameraPlugin(BotPlugin):
    """Плагин для работы с камерой"""
    
    @property
    def name(self) -> str:
        return "Camera"
        
    @property
    def description(self) -> str:
        return "Получение фото с камеры"
        
    @property
    def buttons(self) -> list:
        return [["📸 Фото с камеры"]]
        
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.message.text == "📸 Фото с камеры":
            try:
                # Открываем камеру
                cap = cv2.VideoCapture(0)
                
                # Делаем снимок
                ret, frame = cap.read()
                if not ret:
                    await update.message.reply_text("❌ Не удалось получить кадр с камеры")
                    return
                    
                # Сохраняем фото
                cv2.imwrite("camera.jpg", frame)
                cap.release()
                
                # Отправляем фото
                await update.message.reply_photo(
                    photo=open("camera.jpg", "rb"),
                    caption="📸 Фото с камеры"
                )
                
                # Удаляем временный файл
                os.remove("camera.jpg")
                
            except Exception as e:
                await update.message.reply_text(f"❌ Ошибка: {str(e)}")
                
            return True
            
        return False 