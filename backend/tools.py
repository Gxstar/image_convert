import os
import hashlib
from pathlib import Path
from PIL import Image
import base64
import io

class ThumbnailCache:
    def __init__(self):
        self.cache_dir = Path.home() / '.image_convert_cache' / 'thumbnails'
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def get_cache_key(self, image_path):
        return hashlib.md5(str(image_path).encode()).hexdigest()
    
    def get_thumbnail(self, image_path, max_size=150):
        cache_key = self.get_cache_key(image_path)
        cache_file = self.cache_dir / f"{cache_key}.jpg"
        
        if cache_file.exists():
            with open(cache_file, 'rb') as f:
                img_base64 = base64.b64encode(f.read()).decode()
                return f"data:image/jpeg;base64,{img_base64}"
        return None
    
    def generate_thumbnail(self, image_path, max_size=150):
        cache_key = self.get_cache_key(image_path)
        cache_file = self.cache_dir / f"{cache_key}.jpg"
        
        try:
            with Image.open(image_path) as img:
                img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
                
                if img.mode in ('RGBA', 'LA'):
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                    img = background
                
                img.save(cache_file, 'JPEG', quality=75)
                return True
        except:
            return False