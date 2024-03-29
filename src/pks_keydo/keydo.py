import tkinter
import webview


def main():
    print("Hello world")
    tk = tkinter.Tk()
    tk.geometry("800x450")
    webview.create_window("TEsting", "https://google.com")
    webview.start()
