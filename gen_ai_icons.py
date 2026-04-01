import os
from PIL import Image

image_path = "/home/junyao/.gemini/antigravity/brain/a08d39ab-5d37-4669-a050-c07d03f6e912/bnapp_icon_v3_1775051587175.png"
icon_dir = '/home/junyao/文档/Code/BNapp/src-tauri/icons'

img = Image.open(image_path).convert("RGBA")

# Resize to square if it's not (it should be 1024x1024)
w, h = img.size
min_side = min(w, h)
left = (w - min_side) / 2
top = (h - min_side) / 2
right = (w + min_side) / 2
bottom = (h + min_side) / 2
img = img.crop((left, top, right, bottom))

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
    resized = img.resize((s, s), Image.Resampling.LANCZOS)
    resized.save(os.path.join(icon_dir, name))
    print(f'Done {name} - {s}x{s}')

icon_1024 = Image.open(os.path.join(icon_dir, 'icon.png'))
ico_sizes = [(16,16), (32,32), (48,48), (64,64), (128,128), (256,256)]
icon_1024.save(os.path.join(icon_dir, 'icon.ico'), format='ICO', sizes=ico_sizes)
icon_1024.save(os.path.join(icon_dir, 'icon.icns'), format='ICNS')

print('Finished all icon generation!')
