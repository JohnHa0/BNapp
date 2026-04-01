from PIL import Image, ImageDraw, ImageFont
import math, os

def render_icon(size_px, output_path):
    img = Image.new('RGBA', (size_px, size_px), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    
    radius = int(size_px * 0.22)
    bg_col = (15, 23, 42)
    d.rounded_rectangle([(0, 0), (size_px-1, size_px-1)], radius=radius, fill=bg_col)
    
    center = size_px / 2
    glow_r = int(size_px * 0.38)
    for i in range(glow_r, 0, -1):
        alpha = int(40 * (i / glow_r))
        d.ellipse([center-i, center-i, center+i, center+i], fill=(79, 70, 229, alpha))
    
    r_outer = size_px * 0.30
    nodes = [
        (center, center - r_outer),
        (center - r_outer * 0.866, center + r_outer * 0.5),
        (center + r_outer * 0.866, center + r_outer * 0.5),
        (center, center),
    ]
    
    line_w = max(2, int(size_px * 0.035))
    edge_color = (99, 102, 241)
    for i in range(3):
        d.line([nodes[i], nodes[3]], fill=edge_color, width=line_w)
    for i in range(3):
        d.line([nodes[i], nodes[(i+1)%3]], fill=(71, 85, 105, 120), width=max(1, line_w//2))
    
    node_r = int(size_px * 0.07)
    node_cols = [(0, 240, 255), (16, 185, 129), (251, 113, 133), (245, 158, 11)]
    for i, pt in enumerate(nodes):
        bbox = [pt[0]-node_r, pt[1]-node_r, pt[0]+node_r, pt[1]+node_r]
        d.ellipse(bbox, fill=node_cols[i], outline=(255,255,255,200), width=max(1, int(line_w*0.6)))
    
    if size_px >= 64:
        try:
            font_size = int(node_r * 1.2)
            font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', font_size)
            bbox_text = d.textbbox((0,0), 'D', font=font)
            tw = bbox_text[2] - bbox_text[0]
            th = bbox_text[3] - bbox_text[1]
            d.text((center - tw/2, center - th/2 - bbox_text[1]), 'D', fill=(15, 23, 42), font=font)
        except:
            pass
        
    img.save(output_path)

icon_dir = '/home/junyao/文档/Code/BNapp/src-tauri/icons'
os.makedirs(icon_dir, exist_ok=True)

sizes = {
    'icon.png': 1024,
    '32x32.png': 32,
    '64x64.png': 64,
    '128x128.png': 128,
    '128x128@2x.png': 256,
    'Square30x30Logo.png': 30,
    'Square44x44Logo.png': 44,
    'Square71x71Logo.png': 71,
    'Square89x89Logo.png': 89,
    'Square107x107Logo.png': 107,
    'Square142x142Logo.png': 142,
    'Square150x150Logo.png': 150,
    'Square284x284Logo.png': 284,
    'Square310x310Logo.png': 310,
    'StoreLogo.png': 50,
}

for name, s in sizes.items():
    render_icon(s, os.path.join(icon_dir, name))
    print(f'Generated {name} ({s}x{s})')

icon_1024 = Image.open(os.path.join(icon_dir, 'icon.png'))
ico_sizes = [(16,16), (32,32), (48,48), (64,64), (128,128), (256,256)]
icon_1024.save(os.path.join(icon_dir, 'icon.ico'), format='ICO', sizes=ico_sizes)
print('Generated icon.ico')

print('All icons generated successfully!')
