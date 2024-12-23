from PIL import Image, ImageDraw

# Создаем новое изображение
size = 256
img = Image.new('RGBA', (size, size), color=(0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# Рисуем круг
circle_color = (65, 105, 225)  # Royal Blue
margin = size // 8
circle_bbox = [margin, margin, size - margin, size - margin]
draw.ellipse(circle_bbox, fill=circle_color)

# Рисуем "PC" текст
text_color = (255, 255, 255)  # White
draw.text((size//3, size//3), "PC", fill=text_color, font=None, font_size=size//3)

# Сохраняем как .ico
img.save('icon.ico', format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)]) 