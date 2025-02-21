from PIL import Image, ImageDraw
import os

def create_icons():
    """Create icons for different network devices."""
    icons_dir = 'icons'
    if not os.path.exists(icons_dir):
        os.makedirs(icons_dir)

    # Router
    img = Image.new('RGBA', (60, 60), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rectangle([10, 20, 50, 40], fill='#FF9800', outline='black', width=2)
    draw.line([20, 20, 20, 10], fill='black', width=2)
    draw.line([40, 20, 40, 10], fill='black', width=2)
    img.save(os.path.join(icons_dir, 'router.png'))

    # Switch
    img = Image.new('RGBA', (60, 60), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rectangle([5, 20, 55, 40], fill='#2196F3', outline='black', width=2)
    for i in range(5):
        x = 10 + i * 10
        draw.rectangle([x, 25, x + 5, 35], fill='black')
    img.save(os.path.join(icons_dir, 'switch.png'))

    # Firewall
    img = Image.new('RGBA', (60, 60), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rectangle([10, 10, 50, 50], fill='#f44336', outline='black', width=2)
    points = [30, 15, 45, 20, 45, 40, 30, 45, 15, 40, 15, 20]
    draw.polygon(points, outline='white', width=2)
    img.save(os.path.join(icons_dir, 'firewall.png'))

    # Server
    img = Image.new('RGBA', (60, 60), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rectangle([15, 10, 45, 50], fill='#4CAF50', outline='black', width=2)
    for i in range(3):
        y = 15 + i * 12
        draw.rectangle([18, y, 42, y + 8], fill='#333333')
    img.save(os.path.join(icons_dir, 'server.png'))

    # Client
    img = Image.new('RGBA', (60, 60), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rectangle([10, 10, 50, 40], fill='#9C27B0', outline='black', width=2)
    draw.rectangle([15, 15, 45, 35], fill='#E1BEE7')
    draw.line([30, 40, 30, 50], fill='black', width=2)
    draw.rectangle([20, 50, 40, 52], fill='black')
    img.save(os.path.join(icons_dir, 'client.png'))

    # Access Point
    img = Image.new('RGBA', (60, 60), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rectangle([20, 20, 40, 40], fill='#00BCD4', outline='black', width=2)
    for i in range(3):
        r = 10 + i * 6
        draw.arc([30-r, 30-r, 30+r, 30+r], -60, 60, fill='black', width=2)
    img.save(os.path.join(icons_dir, 'access_point.png'))

if __name__ == '__main__':
    create_icons()