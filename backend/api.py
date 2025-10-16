"""
pywebview链接前端的api函数入口
"""
import webview

class Api:
    def __init__(self):
        pass

    def choose_files(self):
        """
        调用pywebview的文件选择器，返回选择的文件路径
        """
        file_types=('图像文件 (*.bmp;*.jpg;*.jpeg;*.png;*.gif;*.webp;*.avif;*.heif;*.heic;*.tiff;*.tif;*.svg)', 'All files (*.*)')
        selected_files=webview.windows[0].create_file_dialog(dialog_type=webview.FileDialog.OPEN, allow_multiple=True, file_types=file_types)
        webview.windows[0].state.user='阿星'
        print(webview.windows[0].state.user)
        return selected_files
    
    def choose_dir(self):
        """
        调用pywebview的文件夹选择器，返回选择的文件夹路径
        """
        selected_dir=webview.windows[0].create_file_dialog(dialog_type=webview.FileDialog.FOLDER, allow_multiple=False, directory='')
        return selected_dir
