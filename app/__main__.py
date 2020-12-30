import sys
import wx
from app.src_windows.main_window import MainWindow

def main(args=None):
    """ 
    This is the main entry point of the application
    """
    if args is None:
        args = sys.argv[1:]

    app = wx.App(False)
    frame = MainWindow(None, "Text Editor")
    app.MainLoop()

if __name__ == "__main__":
    main()