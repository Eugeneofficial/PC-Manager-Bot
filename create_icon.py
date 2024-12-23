from PIL import Image, ImageDraw, ImageFont

def create_icon():
    # Создаем новое изображение
    size = (256, 256)
    image = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # Рисуем круг
    circle_bbox = (20, 20, 236, 236)
    draw.ellipse(circle_bbox, fill='#1a73e8')
    
    # Добавляем текст
    text = "PC"
    try:
        font = ImageFont.truetype("arial.ttf", 120)
    except:
        font = ImageFont.load_default()
    
    # Центрируем текст
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    text_x = (size[0] - text_width) // 2
    text_y = (size[1] - text_height) // 2
    
    # Рисуем текст
    draw.text((text_x, text_y), text, font=font, fill='white')
    
    # Сохраняем как ICO
    image.save('icon.ico', format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])

if __name__ == '__main__':
    create_icon() 