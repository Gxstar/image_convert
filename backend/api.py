import webview
import os
import threading
from .tools import ThumbnailCache

class Api:
    def __init__(self):
        self.thumbnail_cache = ThumbnailCache()
        self.generating = set()
    
    def get_image_list(self):
        """获取图片列表信息"""
        images = webview.windows[0].state.images
        return [{
            'id': i,
            'path': path,
            'name': os.path.basename(path)
        } for i, path in enumerate(images)]
    
    def get_thumbnail(self, image_path, image_id):
        """获取缩略图"""
        # 先检查缓存
        cached = self.thumbnail_cache.get_thumbnail(image_path)
        if cached:
            return cached
        
        # 后台生成
        if image_path not in self.generating:
            self.generating.add(image_path)
            thread = threading.Thread(target=self._generate_thumbnail, args=(image_path, image_id))
            thread.daemon = True
            thread.start()
        
        return None
    
    def _generate_thumbnail(self, image_path, image_id):
        """后台生成缩略图"""
        self.thumbnail_cache.generate_thumbnail(image_path)
        self.generating.discard(image_path)
    
    def start_batch_thumbnail_generation(self):
        """启动批量缩略图生成"""
        images = webview.windows[0].state.images
        thread = threading.Thread(target=self._batch_generate, args=(images,))
        thread.daemon = True
        thread.start()
        return len(images)
    
    def _batch_generate(self, image_paths):
        """批量生成所有缩略图"""
        for path in image_paths:
            if path not in self.generating:
                self.generating.add(path)
                self.thumbnail_cache.generate_thumbnail(path)
                self.generating.discard(path)
    
    def _generate_new_thumbnails(self, new_files):
        """为新添加的文件生成缩略图"""
        for path in new_files:
            if path not in self.generating:
                self.generating.add(path)
                self.thumbnail_cache.generate_thumbnail(path)
                self.generating.discard(path)
    
    def choose_files(self):
        """选择文件 - 添加到现有列表并立即生成缩略图"""
        file_types = ('图像文件 (*.bmp;*.jpg;*.jpeg;*.png;*.gif;*.webp;*.avif;*.heif;*.heic;*.tiff;*.tif;*.svg)', 'All files (*.*)')
        selected_files = webview.windows[0].create_file_dialog(dialog_type=webview.FileDialog.OPEN, allow_multiple=True, file_types=file_types)
        
        if selected_files:
            webview.windows[0].state.images.extend(selected_files)
            # 立即开始生成新添加文件的缩略图
            thread = threading.Thread(target=self._generate_new_thumbnails, args=(selected_files,))
            thread.daemon = True
            thread.start()
        
        return len(webview.windows[0].state.images)
    
    def clear_images(self):
        """清空图片列表"""
        webview.windows[0].state.images = []
        return 0
      
    def choose_dir(self):
        """选择文件夹 - 添加到现有列表并立即生成缩略图"""
        selected_dir = webview.windows[0].create_file_dialog(dialog_type=webview.FileDialog.FOLDER, allow_multiple=False, directory='')
        image_formats = ('.bmp', '.jpg', '.jpeg', '.png', '.gif', '.webp', '.avif', '.heif', '.heic', '.tiff', '.tif', '.svg')
        
        if selected_dir and selected_dir[0]:
            folder_path = selected_dir[0]
            selected_files = []
            for file in os.listdir(folder_path):
                if file.lower().endswith(image_formats):
                    selected_files.append(os.path.join(folder_path, file))
            
            if selected_files:
                webview.windows[0].state.images.extend(selected_files)
                # 立即开始生成新添加文件的缩略图
                thread = threading.Thread(target=self._generate_new_thumbnails, args=(selected_files,))
                thread.daemon = True
                thread.start()
        
        return len(webview.windows[0].state.images)
