import cv2
from telegram import InlineKeyboardButton
from plugins import BotPlugin

class CameraPlugin(BotPlugin):
    @property
    def name(self) -> str:
        return "Камера"
        
    @property
    def description(self) -> str:
        return "Получение фото с веб-камеры"
        
    @property
    def buttons(self) -> list:
        return [
            [
                InlineKeyboardButton("📸 Фото", callback_data="camera_photo"),
            ]
        ]
        
    async def handle_callback(self, callback_data: str, update, context) -> bool:
        if callback_data == "camera_photo":
            try:
                # Захват кадра с камеры
                cap = cv2.VideoCapture(0)
                ret, frame = cap.read()
                
                if ret:
                    # Сохраняем фото
                    cv2.imwrite("camera.jpg", frame)
                    cap.release()
                    
                    # Отправляем фото
                    await update.callback_query.message.reply_photo(
                        photo=open("camera.jpg", "rb"),
                        caption="📸 Фото с камеры"
                    )
                    
                    # Удаляем временный файл
                    import os
                    os.remove("camera.jpg")
                else:
                    await update.callback_query.message.reply_text("❌ Не удалось получить кадр с камеры")
            except Exception as e:
                await update.callback_query.message.reply_text(f"❌ Ошибка: {str(e)}")
            return True
            
        return False 