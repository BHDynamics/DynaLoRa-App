import wx

class MainWindow(wx.Frame):

    def create_menu(self):
        self.fileMenu.Append(wx.ID_ABOUT, "&About", "Information about this program")
        self.fileMenu.AppendSeparator()
        self.fileMenu.Append(wx.ID_EXIT, "&Exit", "Terminate program")


    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(200, 100))
        self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.CreateStatusBar()

        self.fileMenu = wx.Menu()

        self.create_menu()

        self.menuBar = wx.MenuBar()

        self.menuBar.Append(self.fileMenu, "&File")
        
        self.SetMenuBar(self.menuBar) 
        self.Show(True)
