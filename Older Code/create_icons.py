from PIL import Image, ImageDraw
import os

def create_router_icon():
    img = Image.new('RGBA', (256, 256), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Router body
    draw.rectangle([48, 96, 208, 160], fill='#FF9800', outline='black', width=4)
    # Antennas
    draw.line([80, 96, 80, 48], fill='black', width=4)
    draw.line([176, 96, 176, 48], fill='black', width=4)
    # LED lights
    draw.ellipse([84, 120, 92, 128], fill='#4CAF50')
    draw.ellipse([108, 120, 116, 128], fill='#4CAF50')
    draw.ellipse([132, 120, 140, 128], fill='#4CAF50')
    
    return img

def create_switch_icon():
    img = Image.new('RGBA', (256, 256), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Switch body
    draw.rectangle([32, 96, 224, 160], fill='#2196F3', outline='black', width=4)
    # Ports
    for i in range(5):
        x = 48 + i * 32
        draw.rectangle([x, 112, x + 16, 144], fill='black')
        draw.ellipse([x, 104, x + 8, 112], fill='#4CAF50')
    
    return img

def create_firewall_icon():
    img = Image.new('RGBA', (256, 256), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Firewall body
    draw.rectangle([48, 48, 208, 208], fill='#f44336', outline='black', width=4)
    # Shield design
    points = [128, 64, 176, 80, 176, 144, 128, 176, 80, 144, 80, 80]
    draw.polygon(points, outline='white', width=4)
    
    return img

def create_server_icon():
    img = Image.new('RGBA', (256, 256), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Server rack
    draw.rectangle([64, 48, 192, 208], fill='#4CAF50', outline='black', width=4)
    # Server units
    for i in range(3):
        y = 64 + i * 48
        draw.rectangle([72, y, 184, y + 32], fill='#333333')
        draw.ellipse([84, y + 8, 92, y + 16], fill='#4CAF50')
    
    return img

def create_client_icon():
    img = Image.new('RGBA', (256, 256), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Monitor
    draw.rectangle([48, 48, 208, 168], fill='#9C27B0', outline='black', width=4)
    # Screen
    draw.rectangle([64, 64, 192, 152], fill='#E1BEE7')
    # Stand
    draw.line([128, 168, 128, 208], fill='black', width=4)
    draw.rectangle([88, 208, 168, 216], fill='black')
    
    return img

def create_access_point_icon():
    img = Image.new('RGBA', (256, 256), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # AP body
    draw.rectangle([88, 88, 168, 168], fill='#00BCD4', outline='black', width=4)
    # WiFi signals
    for i in range(3):
        r = 40 + i * 24
        draw.arc([128-r, 128-r, 128+r, 128+r], -60, 60, fill='black', width=4)
    # LED
    draw.ellipse([124, 124, 132, 132], fill='#4CAF50')
    
    return img

def main():
    # Create icons directory if it doesn't exist
    if not os.path.exists('icons'):
        os.makedirs('icons')
    
    # Create and save icons
    icons = {
        'router': create_router_icon(),
        'switch': create_switch_icon(),
        'firewall': create_firewall_icon(),
        'server': create_server_icon(),
        'client': create_client_icon(),
        'access_point': create_access_point_icon()
    }
    
    for name, icon in icons.items():
        icon.save(f'icons/{name}.png')
        print(f"Created {name}.png")

if __name__ == '__main__':
    main()