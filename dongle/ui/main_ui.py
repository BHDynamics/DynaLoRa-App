import wx
import os
import wx.adv
import dongle.utils.events as ev
import dongle.ui.dongle_ui as dng
import webbrowser

from dongle.device import Device
from dongle.utils.file_manager import Saver
from dongle.utils.file_manager import Opener
from dongle.utils.trace import Trace
from datetime import datetime

class MainFrame(wx.Frame):
    """
    This class is the main Frame controller, that
    manages the different views and situations related
    to the window. Creates the different menus and 
    sets their functionality. 
    
    Creates the device controller instance and tries
    to connect to a device. Can connect and disconnect
    a device, send messages to it and receive events
    from it. 

    Args:
        wx (wx.Frame): Inherits from wx.Frame
    """

#region Variables

    # Menus
    _fileMenu = None
    _deviceMenu = None
    _helpMenu = None
    _viewMenu = None    
    
    # Bars 
    _menuBar = None
    _statusBar: wx.StatusBar = None
    
    # Terminal
    _currentUI = None
    
    # USB Device instance
    _deviceInstance: Device = None
    
    # Utilities
    _fileOpener = Opener()
    _fileSaver = Saver()
    
    # App info
    _appInfo = None
    _devices = None

#endregion   

#region Window Construction

    #------------------------------------------------
    #-----------------Construction-------------------
    #------------------------------------------------
    
    def __init__(self, parent, path, filename):
        file = self._fileOpener.OpenJSONFile(path, filename)
        
        self._devices = file["devices"]
        urls = file["urls"]
        self._appInfo = file["info"]
        
        wx.Frame.__init__(self, parent, title=file["title"], size=(file["size"]["x"], file["size"]["y"]))
        
        # Try to connect to a device
        # This is done first to activate some options
        # of the menus
        self._deviceInstance = Device(self._devices, self)
        if not self._deviceInstance.is_connected():
            self._deviceInstance = None
            
        print(self._deviceInstance)
        
        # Create the menu bar
        self.__create_menu_bar(urls)
        
        # Layout creation is specific from other frame_types
        self._currentUI = dng.Dongle(self, 0, 0, 200, 200)
        
        self.__bind_handlers()
        
        self._statusBar = self.CreateStatusBar(2)
        self._statusBar.SetStatusText(" ", 0)
        
        if not self._deviceInstance:
            self._statusBar.SetStatusText("No device connected", 1)
        else:
            self._statusBar.SetStatusText("Device port: " + self._deviceInstance.get_port(), 1)
        
        self.Show()
        
        
    def __create_menu_bar(self, urls):
        """
        Creates the menubar that will appear at the top 
        of the window, with all the different options.

        Args:
            urls (dictionary): The different links with tutorials and info.
        """
        self._fileMenu = wx.Menu()
        self.__create_file_menu()
        
        self._deviceMenu = wx.Menu()
        self.__create_device_menu()
        
        self._helpMenu = wx.Menu()
        self.__create_help_menu(urls)
        
        self._viewMenu = wx.Menu()
        self.__create_view_menu()
        
        self._menuBar = wx.MenuBar()
        self._menuBar.Append(self._fileMenu, "&File")
        self._menuBar.Append(self._deviceMenu, "&Device")
        self._menuBar.Append(self._helpMenu, "&Help")
        self._menuBar.Append(self._viewMenu, "&View")
        
        self.SetMenuBar(self._menuBar)
        
    def __create_device_menu(self):
        """
        This function creates the menu that manages
        the different options related to the device 
        and it's possibilities. 
        """
        devConnect = self._deviceMenu.Append(wx.ID_ANY, "&Connect Device", "Connects app to a USB device (if plugged)")
        self.Bind(wx.EVT_MENU, self.OnUserConnect, devConnect)

        devDisconnect = self._deviceMenu.Append(wx.ID_ANY, "&Disconnect Device", "Disconnects app from current connected device")
        self.Bind(wx.EVT_MENU, self.OnUserDisconnect, devDisconnect)
        self._deviceMenu.AppendSeparator()
        
        devInfo = self._deviceMenu.Append(wx.ID_ANY, "&Info.", "Shows information about the connected device")
        self.Bind(wx.EVT_MENU, self.OnDeviceInfo, devInfo)
        
        # devReceivedTest = self._deviceMenu.Append(wx.ID_ANY, "&Test Receiving", "Tests receiving messages and writing info in log system")
        # self.Bind(wx.EVT_MENU, self.OnRead, devReceivedTest)
        
    def __create_help_menu(self, urls):
        """
        This method creates the menu option that gives the user access to different
        options related with getting help, information, etc. 
        
        Currently it only has 3 buttons, but more can be added anytime. 
        """
        # Create and bind report button to open webbrowser
        reportButton = self._helpMenu.Append(wx.ID_ANY, "&Report", "Report an issue or give any feedback you consider is relevant")
        self.Bind(wx.EVT_MENU,
                  lambda evt, temp=urls["report"]: self.OnHelpMenuButton(evt, temp),
                  reportButton)
        
        # Create tutorial menu and bind all different buttons
        tutorialMenu = wx.Menu()
        
        # Create dongle tutorial button
        dongleTutorial = tutorialMenu.Append(wx.ID_ANY, "&Dongle", "Access dongle programming tutorials")
        self.Bind(wx.EVT_MENU,
                  lambda evt, temp=urls["tutorials"]["dongle"]: self.OnHelpMenuButton(evt, temp),
                  dongleTutorial)
        
        # Create DynOSSAT EDU tutorial button
        satTutorial = tutorialMenu.Append(wx.ID_ANY, "&DynOSSAT", "Access DynOSSAT programming and hardware tutorials")
        self.Bind(wx.EVT_MENU,
                  lambda evt, temp=urls["tutorials"]["dynosat"]: self.OnHelpMenuButton(evt, temp),
                  satTutorial)
        
        # Create App tutorial button
        appTutorial = tutorialMenu.Append(wx.ID_ANY, "&App", "Access app documentation, tutorials and source code in github")
        self.Bind(wx.EVT_MENU,
                  lambda evt, temp=urls["tutorials"]["app"]: self.OnHelpMenuButton(evt, temp),
                  appTutorial)
        
        # Now append that menu to the main help menu
        self._helpMenu.Append(wx.ID_ANY, "&Tutorials", tutorialMenu)
        
        # Separate options
        self._helpMenu.AppendSeparator()
        
        # Create and bind Info button to give info about the app
        infoButton = self._helpMenu.Append(wx.ID_ANY, "&Info.", "Consult information about the app")
        self.Bind(wx.EVT_MENU, self.OnInfo, infoButton)
        
    def __create_view_menu(self):
        h = 0
        
    def __create_file_menu(self):
        """
        Method to create the file menu in the top menu bar. 
        It is separated to make all programm more readable
        and easier to add new things and options. 
        """
        # Create, add and bind "Open" option
        logOpener = self._fileMenu.Append(wx.ID_OPEN, "&Open Log", "Open some log stored in app data.")
        self.Bind(wx.EVT_MENU, self.OnOpen, logOpener)
        
        # Create, add and bind "Save" option
        logSaver = self._fileMenu.Append(wx.ID_SAVE, "&Save Log", "Saves current log into a file at " + self._fileSaver.GetSavingDir())
        self.Bind(wx.EVT_MENU, self.OnSave, logSaver)
        
        # Create, add and bind "Save As" option
        logAsSaver = self._fileMenu.Append(wx.ID_SAVEAS, "&Save Log As...", "Saves the actual log into a specified location")
        self.Bind(wx.EVT_MENU, self.OnSaveAs, logAsSaver)
        
        # Clear log option
        loggerCleaner = self._fileMenu.Append(wx.ID_ANY, "&Clear Log", "Deletes all data in the current log")
        self.Bind(wx.EVT_MENU, self.OnClearLog, loggerCleaner)
        self._fileMenu.AppendSeparator()
        
        # Aquí irían las preferencies
        # Create, add and bind "Exit" option 
        closer = self._fileMenu.Append(wx.ID_EXIT, "&Exit", "Exit and close app.")
        self.Bind(wx.EVT_MENU, self.OnExit, closer)
        
    def __bind_handlers(self):
        """
        Subscribe this class and object to all important 
        events from wx and own created events. 
        """
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Bind(wx.EVT_MENU, self.OnExit, id=wx.ID_EXIT)
        
        # Attach read events
        self.Bind(ev.EVT_SERIALR, self.OnRead)
        self.Bind(ev.EVT_SERIALRM, self.OnReadMessage)
        # Bind reading error (disconnection) and serial frame error
        self.Bind(ev.EVT_SERIALRE, self.OnReadError)
        self.Bind(ev.EVT_SERIALFE, self.OnReadError)
        
        # Attach writing events
        self.Bind(ev.EVT_SERIALW, self.OnWrite)
        self.Bind(ev.EVT_SERIALWE, self.OnWriteError)
        
        # Attach connection events
        self.Bind(ev.EVT_SERIALC, self.OnConnect)
        self.Bind(ev.EVT_SERIALCE, self.OnConnectionError)
        self.Bind(ev.EVT_SERIALD, self.OnDisconnect)
        
    #------------------------------------------------
    #-----------------Construction-------------------
    #------------------------------------------------

#endregion    

#region Event Handlers
  
    #------------------------------------------------
    #----------------Event Handling------------------
    #------------------------------------------------   

#region Device Handling
    #---------------DEVICE HANDLER------------------
    
    def __format_parameters(self, data):
        """
        Method to convert the different parameters into 
        something more readable. 

        Args:
            data (str/bytes): Parameters

        Returns:
            str: Formated parameters.
        """
        lengthParams = int(data[0])
        params = ""
        
        for i in range(0, lengthParams):
            params += (data[1 + i] + ";")
        
        return params
     
    def OnRead(self, event):
        """
        Method called when some new line is available 
        to read from the device. 
        Receives this new line and formats it so that 
        the user can understand what message is sent. 

        Args:
            event (EVT_SERIALR): Serial read event. 
        """
        # TODO: Manage different types of codification
        # Extract trace from event.
        # Try to decode into a string
        newStr = event.data.decode('utf-8')
        if ";" in newStr:
            # If the string contains a ; will assume that 
            # the trace a string-codified one.
            traceData = newStr.split(";")
            messageComm = (traceData[0] == "DLM")
            traceData.pop(0)
            traceData.pop(len(traceData) - 1)
            
            message: str = None
            
            # TODO: This should change to identify the different commands
            # and messages received to show different information to the user.
            if traceData[0] != "0":
                if messageComm:
                    message = "[In]: {mess}                     {timestamp}\n".format(
                        mess=traceData[1], 
                        timestamp=datetime.fromtimestamp(float(traceData[len(traceData) - 1])).strftime("%Y-%M-%D %H:%M:%S")
                    )
                else:
                    message = "[In]: {comm} (Params): {params}                     {timestamp}\n".format(
                        comm=traceData[1],
                        params=self.__format_parameters(traceData), 
                        timestamp=datetime.fromtimestamp(float(traceData[len(traceData) - 1])).strftime("%Y-%M-%D %H:%M:%S")
                    )
            else:
                message = "[In]: {comm}                     {timestamp}\n".format(
                    comm=traceData[1],
                    timestamp=datetime.fromtimestamp(float(traceData[len(traceData) - 1])).strftime("%Y-%M-%D %H:%M:%S")
                )
                
            self._currentUI.OnResponse(message)
        else:
            x = 0
            # Implement Byte processing
            
    def OnReadMessage(self, event):
        """
        Method called when the device throws a new message.

        Args:
            event (EVT_SERIALRM): Message received from serial.
        """
        # Avoid lines with only \r\n
        if event.data != b'\r\n':
            # Now transform message into string and clean it from \r\n
            message = bytearray(event.data).decode("utf-8")
            message = message.strip()
            self._currentUI.OnResponse("[System] " + message + "\n")
    
    def WriteDevice(self, dat: Trace):
        """
        Method called when user wants to send some 
        command to the device. Checks if a device is connected
        and then sends the message. 
        
        If not, notifies the user writing a message in the 
        command log.

        Args:
            dat (Trace): Trace to send to the device.
        """
        # Check device is connected
        if self._deviceInstance:
            self._deviceInstance.write(dat)
        else:
            self._currentUI.OnResponse("[System] Device is not connected, can't send command.\n")
        
    def OnWrite(self, event):
        """
        Method called to notify the user that the command 
        or message has been correctly sent to the device. 
        Writes a message on the log. 

        Args:
            event (EVT_SERIALW): Correctly writing message.
        """
        # TODO: This can be done better. 
        self._currentUI.OnResponse("[System] Message correctly sent.\n")
        
    def OnWriteError(self, event):
        """
        Method called when an error occured while writing
        in the device. Writes a message on the log showing
        the error.

        Args:
            event (EVT_SERIALWE): Serial writing error.
        """
        self._currentUI.OnResponse("[System] Error while writing on the device. Error: " + str(event.data) + "\n")
        
    def OnReadError(self, event):
        """
        Function to manage when an error reading data 
        from the device occured. Writes a message into 
        the log for the user to see it, and store it if
        neccesary for later analysis. 

        Args:
            event (EVT_SERIALRE): Serial read error. 
        """
        self._currentUI.OnResponse("[System] Error while reading from the device. Error: " + str(event.data) + "\n")
        
    # Device status checking    
    def OnConnectionError(self, event):
        """
        Method called when the connection with the device could 
        not be completed succesfully. Show a dialog to the user 
        and then delete device instance.

        Args:
            event (EVT_SERIALCE): [description]
        """
        dlg = wx.MessageDialog(self, "Something went wrong with serial connection.")
        dlg.ShowModal()
        dlg.Destroy()
        self._deviceInstance = None 
        
    def OnConnect(self, event):
        """
        This method is in charge of managing that the device
        has connected. It's job is to update some information
        in the GUI and notify the user that device is connected.

        Args:
            event (EVT_SERIALC): Device connection event.
        """
        self._statusBar.SetStatusText("Device port: " + self._deviceInstance.get_port(), 1)
        dlg = wx.MessageDialog(self, "Device connected!")
        dlg.ShowModal()
        dlg.Destroy()    
        
    def OnDisconnect(self, event):
        """
        This method is in charge of managing the device
        disconnection from USB serial port. Shows a 
        dialog that notifies the disconnection and then 
        updates the GUI to disable some options.

        Args:
            event (EVT_SERIALD): Serial disconnection.
        """
        self._statusBar.SetStatusText("No device connected", 1)
        dlg = wx.MessageDialog(self, "Device disconnected!")
        dlg.ShowModal()
        dlg.Destroy()
    
    #---------------DEVICE HANDLER------------------
#endregion

#region Device Menu Option
    #-----------------DEVICE MENU-------------------
    # This functions and methods are the ones that manage the 
    # different events generated by the device menu, telling 
    # the App when to connect or disconnect a device.
        
    def OnUserConnect(self, event):
        """
        Method called when the user wants to connect the device to
        the App. Creates a new device instance and initializes it
        using this own object as listener and main communications 
        intermediate.

        Args:
            event (wx.EVT_MENU): Menu event.
        """
        if not self._deviceInstance:
            self._deviceInstance = Device(self._devices, self)
            if not self._deviceInstance.is_connected():
                self._deviceInstance = None
                dlg = wx.MessageDialog(self, 
                               "No devices found.")
                dlg.ShowModal()
                dlg.Destroy()
        else:
            dlg = wx.MessageDialog(self, 
                               "Device already connected.")
            dlg.ShowModal()
            dlg.Destroy()
        
    def OnUserDisconnect(self, event):
        """
        Method called when the user disconnects the device 
        from the device menu. Closes the device instance and 
        port connection and deletes the instance of the 
        device.

        Args:
            event (wx.EVT_MENU): Menu event.
        """
        if self._deviceInstance:
            self._deviceInstance.close()
            self._deviceInstance = None
        else:
            dlg = wx.MessageDialog(self, 
                               "Device is not connected.")
            dlg.ShowModal()
            dlg.Destroy()
        
    def OnDeviceInfo(self, event):
        """
        Method called when the user wants to know information 
        about the device connected with the app. Shows a dialog
        with all relevant data related to the device. 

        Args:
            event (wx.EVT_MENU): Menu event.
        """
        # Create string info
        # TODO: Retocar esto con info del dispositivo.
        info = wx.adv.AboutDialogInfo()
        
        description = " "
        
        if self._deviceInstance:
            data = self._deviceInstance.get_port_data()
            generalData = data[2].split(" ")
            description = """
            PORT: {port}\n
            Type: {device}\n
            {dat}\n
            Serial number: {serNumb}\n
            Location: {loc}\n
            """.format(
                port=data[0],
                device=data[1],
                dat=generalData[1],
                serNumb=generalData[2],
                loc=generalData[3]
            )
            
            info.SetName("Device")
            info.SetDescription(description)
            
        else:
            dlg = wx.MessageDialog(self, 
                               "Device is not connected.")
            dlg.ShowModal()
            dlg.Destroy()     
        
        wx.adv.AboutBox(info)

    #-----------------DEVICE MENU-------------------
#endregion
    
#region Help Menu Option
    #------------------HELP MENU--------------------
    def OnHelpMenuButton(self, event, url):
        """
        This function opens a webbrowser with an specific 
        url provided by the event. This is used to 
        access the different tutorials, contact and 
        many more options provided in the internet and 
        concerning this app and hardware. 

        Args:
            event (EVT_MENU): wx event
            url (str): URL to open in the browser
        """
        # Open webbrowser
        webbrowser.open(url)
        
    def OnInfo(self, event):
        """
        This function shows a dialog with all the information
        about this app. Version, build, target OS, etc.

        Args:
            event (EVT_MENU): wx Event
        """
        # Create string info
        info = wx.adv.AboutDialogInfo()
        
        description = """
        OS: {OS}\n
        Commit: {comm}\n
        Date: {date}\n
        wxPython Vers: {wx}\n
        Python Vers: {pyth}\n
        """.format(
            OS=self._appInfo["OS"],
            comm=self._appInfo["Commit"],
            date=self._appInfo["Date"],
            wx=self._appInfo["wxPython"],
            pyth=self._appInfo["Python"]
        )
        
        info.SetName("Dongle App")
        info.SetDescription(description)
        info.SetVersion(self._appInfo["vers"])
        info.SetWebSite(self._appInfo["web"])
        info.AddDeveloper("BHDynamics")
        
        
        wx.adv.AboutBox(info)
        
    #------------------HELP MENU--------------------
#endregion

#region File Menu Option
    #------------------FILE MENU--------------------
       
    def OnOpen(self, event):
        """
        Method that manages the opening option. Creates
        a new dialog to let the user choose a file with 
        logs to open. Then calls for the fileOpener's
        OpenFile and then notifies the terminal to update
        the texts that it's showing.

        Args:
            event (wxEven): Event that calls for this method.
        """
        # Create a dialog to get the file to open
        dirName = ''
        dlg = wx.FileDialog(self, "Choose file", dirName, "", "*.*", wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            fileName = dlg.GetFilename()
            dirName = dlg.GetDirectory()
            
            # Notify terminal
            self.UpdateTerminal(os.path.join(dirName, fileName))
            
        
    def OnSave(self, event):
        """
        This method saves log data generated in the current session
        to a save file within the program. It is called when
        the app generates an event of saving from the menu. 

        Args:
            event (EVT_MENU): Event produced by a menu.
        """
        # Get data and save it into a file
        data = self.GetTerminalData()
        self._fileSaver.SaveTextLog(data)
    
    def OnSaveAs(self, event):
        """
        Method that saves log data generated in the current session
        into a file specified by the user. 

        Args:
            event (EVT_MENU): Event produced by a menu
        """
        # Create dialog
        dlg = wx.FileDialog(self, "Save file with name...", "", "", "*.*", wx.FD_SAVE)
        if dlg.ShowModal() == wx.ID_OK:
            # Retrieve data from dialog
            fileName = dlg.GetFilename()
            dirName = dlg.GetDirectory()
            data = self.GetTerminalData()
            
            # Save data into file
            self._fileSaver.SaveTextLogAs(dirName, fileName, data)
            
    def OnClearLog(self, event):
        """
        This method is used to clear the current log
        and leave it empty.

        Args:
            event (EVT_MENU): Event received from the button
        """
        # Show a message to validate user's actions
        # "style" marks the type of window message to show
        dlg = wx.MessageDialog(self, 
                               "You are going to delete the current log completely.\n" +
                               "Continue deleting current log?",
                               style=wx.OK|wx.CANCEL|wx.CENTER)
        if dlg.ShowModal() == wx.ID_OK:
            self._currentUI.ClearLog()
          
        dlg.Destroy()
        
        
    def OnExit(self, event):
        """
        Exit point, called from menu.

        Args:
            event (EVT_MENU): Exiting event.
        """
        self.Close(True)

    #------------------FILE MENU--------------------
#endregion

#region App Live Management
    #---------------EXIT MANAGEMENT-----------------
        
    def OnClose(self, event):
        """
        Closing function. Called when app is 
        shutdown by the user. Ends all communications
        with the device and notifies it for closing
        serial connection and end all threads. 

        Args:
            event (wxEvent): Closing event
        """
        # Check if some device is connected
        if self._deviceInstance and self._deviceInstance._connected:
            self._deviceInstance.close()
            self._deviceInstance = None
        
        # Destroy this window
        self.Destroy()
    
    #---------------EXIT MANAGEMENT-----------------
#endregion        
    #------------------------------------------------
    #----------------Event Handling------------------
    #------------------------------------------------  

#endregion 
  
#region UI Management
  
    #------------------------------------------------
    #-----------------UI Management------------------
    #------------------------------------------------  
    
    def UpdateTerminal(self, data):
        self._currentUI.LoadLog(data)
        
    def GetTerminalData(self):
        data = "".join(self._currentUI.GetLogData())
        return data
    
    #------------------------------------------------
    #-----------------UI Management------------------
    #------------------------------------------------ 

#endregion   
         