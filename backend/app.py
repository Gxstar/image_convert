from .api import Api
import webview

def main():
    window = webview.create_window("图片转换器", "http://localhost:5173", js_api=Api())
    webview.windows[0].state.user='gxstar'
    webview.start(debug=True)