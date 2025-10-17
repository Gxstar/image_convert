"""
pywebview链接前端的api函数入口
"""
import webview
import os

class Api:
    def __init__(self):
        pass

    def choose_files(self):
        """
        调用pywebview的文件选择器，返回选择的文件路径
        """
        file_types=('图像文件 (*.bmp;*.jpg;*.jpeg;*.png;*.gif;*.webp;*.avif;*.heif;*.heic;*.tiff;*.tif;*.svg)', 'All files (*.*)')
        selected_files=webview.windows[0].create_file_dialog(dialog_type=webview.FileDialog.OPEN, allow_multiple=True, file_types=file_types)
        webview.windows[0].state.images.extend(selected_files)
        webview.windows[0].state.user='阿星'
        print(webview.windows[0].state.user)
        return 0
    
    def choose_dir(self):
        """
        调用pywebview的文件夹选择器，返回选择的文件夹路径
        """
        selected_dir=webview.windows[0].create_file_dialog(dialog_type=webview.FileDialog.FOLDER, allow_multiple=False, directory='')
        # 支持的图片格式
        image_formats=('.bmp', '.jpg', '.jpeg', '.png', '.gif', '.webp', '.avif', '.heif', '.heic', '.tiff', '.tif', '.svg')
        folder_path=selected_dir[0] if selected_dir else selected_dir
        selected_files=[]
        if folder_path:
            for file in os.listdir(folder_path):
                if file.endswith(image_formats):
                    selected_files.append(os.path.join(folder_path, file))
        webview.windows[0].state.images.extend(selected_files)
        return 0
