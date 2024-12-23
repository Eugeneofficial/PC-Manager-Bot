import os
import subprocess
from PIL import Image, ImageDraw, ImageFont

def create_icon():
    """Create an icon for the application"""
    size = 256
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw circle background
    circle_color = (0, 120, 212)  # Windows blue
    draw.ellipse([10, 10, size-10, size-10], fill=circle_color)
    
    # Add text
    try:
        font = ImageFont.truetype("arial.ttf", 120)
    except:
        font = ImageFont.load_default()
        
    text = "PC"
    text_color = (255, 255, 255)  # White
    
    # Center text
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    x = (size - text_width) // 2
    y = (size - text_height) // 2
    
    draw.text((x, y), text, font=font, fill=text_color)
    
    # Save as ICO
    img.save("icon.ico", format="ICO", sizes=[(256, 256)])

def create_example_config():
    """Create example config file"""
    config = {
        "TELEGRAM_TOKEN": "YOUR_BOT_TOKEN_HERE",
        "AUTHORIZED_USERS": [123456789]
    }
    
    with open("config.json.example", "w") as f:
        import json
        json.dump(config, f, indent=4)

def build_installer():
    """Build the installer using NSIS"""
    try:
        # Create icon
        create_icon()
        
        # Create example config
        create_example_config()
        
        # Check if NSIS is installed
        makensis_path = r"C:\Program Files (x86)\NSIS\makensis.exe"
        if not os.path.exists(makensis_path):
            print("Error: NSIS not found. Please install NSIS from https://nsis.sourceforge.io/")
            return False
            
        # Build installer
        result = subprocess.run([makensis_path, "installer.nsi"], 
                              capture_output=True, 
                              text=True)
                              
        if result.returncode == 0:
            print("Installer built successfully!")
            print("Output file: PC-Manager-Bot-Setup.exe")
            return True
        else:
            print("Error building installer:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"Error building installer: {str(e)}")
        return False

if __name__ == "__main__":
    build_installer() 