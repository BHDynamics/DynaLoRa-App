import wx
import wx.stc as stc
import math

import dongle.ui.basic_ui as bUI

class Dongle(bUI.BasicUI):
    """
    This class contains the UI for controlling 
    the dongle only, with the specified commands
    that can be sent to the device. 
    
    It's created from a json file that contains
    the complete UI configuration, storing the
    max number of buttons per raw in the button
    grid, the different buttons and the data 
    related to the buttons. 
    """
#region Variables
    # Sizers
    _buttonGrid: wx.GridSizer = None
#endregion
    
#region Construction
    #------------------------------------------------
    #--------------------Private---------------------
    #------------------------------------------------
       
    def __init__(self, mainWin, x, y, w, h):
        """
        Constructor of the UI to manage and communicate
        with the dynalora. Creates a grid with buttons
        that represent the different commands registered
        in the JSON configuration file. 
        
        Then creates the different logs and data representing
        objects. 

        Args:
            mainWin (wx.Frame): Main frame of the App
            x (int): X position of the Sizer
            y (int): Y position of the Sizer
            w (int): Width of the Sizer.
            h (int): Height of the Sizer.
        """
        self._confFile = "dongle_ui.json"
        super().__init__(mainWin, x, y, w, h)
        
        # Create connection status data
        
        # Create buttons
        # Add title text
        tBox = wx.BoxSizer(wx.HORIZONTAL)
        text = wx.StaticText(self._mainPanel, label='Commands')
        tBox.Add(text)
        self._mainSizer.Add(tBox, flag=wx.LEFT | wx.TOP, border=self._conf["input"]["padding"])
        self._mainSizer.Add((-1, 5))
        
        cols = self._conf["buttonsPerRaw"]
        rows = math.ceil(len(self._conf["buttons"]) / cols)
        self._buttonGrid = wx.GridSizer(rows, cols, self._conf["verticalGap"], self._conf["horizontalGap"])
        self.__place_buttons(self._conf["buttonsSize"], self._conf["buttons"])
        
        self._mainSizer.Add(self._buttonGrid, flag=wx.RIGHT | wx.LEFT | wx.EXPAND, border=self._conf["log"]["padding"])
        
        self._mainSizer.Add((-1, 10))
        
        # Create parameters and sending box
        self._create_input_console(self._conf["input"])
        
        # Set checkbox 
        temp = wx.BoxSizer(wx.HORIZONTAL)
        self._traceType = wx.CheckBox(self._mainPanel, label="String-type trace")
        self._traceType.SetValue(wx.CheckBoxState(wx.CHK_CHECKED))
        temp.Add(self._traceType, flag=wx.LEFT)
        self._mainSizer.Add(temp, flag=wx.LEFT, border=self._conf["log"]["padding"])
        
        # Create output console and log box
        self._create_log(self._conf["log"])
        
        # Add BoxSizer to panel
        #self._mainPanel.SetSizer(self._mainSizer)
        self._mainPanel.SetSizerAndFit(self._mainSizer)
        
    def __place_buttons(self, bSize, buttons):
        """
        This function instantiates all buttons into the 
        buttonGrid that represents the command sending event.
        
        Sets the label defines in the JSON file and then binds
        it to an event to make visual changes. 

        Args:
            buttons (list): List with all the buttons to
            instantiate.
        """
        for b in buttons: 
            # First instantiate a new button           
            nButton = wx.Button(self._mainPanel, label=b["txt"], size=(bSize["w"], bSize["h"]))
            
            # Bind it 
            sendData = [b["command"], b["byte"]]
            self._window.Bind(wx.EVT_BUTTON, 
                         lambda evt, temp=sendData: self.OnCommandButtonClick(evt, temp),
                         nButton)
            
            # And add it to the Grid
            self._buttonGrid.Add(nButton, 0, wx.LEFT | wx.RIGHT, 5)

    #------------------------------------------------
    #--------------------Private---------------------
    #------------------------------------------------
#endregion 

#region Events
    #------------------------------------------------
    #----------------Event Handling------------------
    #------------------------------------------------            
    
    def OnCommandButtonClick(self, event, data):
        """
        This function is called when a button is pressed and 
        selected. Notifies the different elemments of the UI
        to update themselves with new information and data. 

        Args:
            event (wxEvent): Event 
            data (list): List containing the command and byte code
        """
        # For the moment this function is still here but can be moved to other class
        # Update current trace data
        self._currTrace.SetCommand(data[0])
        self._currTrace.SetCommandCode(bytes.fromhex(data[1]))
        
        # Modify the input terminal.
        self._commandNameCtrl.SetValue("")
        self._commandNameCtrl.SetValue(data[0])
        
        self._commandParamsCtrl.SetValue("")
        self._traceType.SetValue(wx.CheckBoxState(wx.CHK_CHECKED))
        
    #------------------------------------------------
    #----------------Event Handling------------------
    #------------------------------------------------
#endregion        