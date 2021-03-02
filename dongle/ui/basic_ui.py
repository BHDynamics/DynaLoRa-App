"""Basic UI file

This file contains the BasicUI class that creates the different logs
and texts. Binds the different events to the logs and the functions
that updates the logs and texts.
"""
# Standard imports
import os
import math
from datetime import datetime

# Third parties
import wx
import wx.stc as stc

# Internal imports
from dongle.utils.file_manager import Opener
from dongle.utils.trace import Trace
import dongle.utils.events as ev

class BasicUI:
    """
    This class is the basic UI to 
    control the dongle. It contains some basic
    objects that will be used by the different
    implementations of the UI.
    
    It also implements some methods that update
    the different UI elements that are the same
    between the different interfaces.
    """
#region Variables
    # Utilities
    _fOpener = Opener()
    _confFile = ""
    _window = None
    _conf = None
    _dataPath = os.path.abspath(os.path.join(os.path.dirname( __file__ ),
                           '..', 'data/cnf'))
    
    # Panel
    _mainPanel: wx.Panel = None
    
    # Sizers
    _mainSizer: wx.BoxSizer = None
    _inputSizer: wx.BoxSizer = None
    _logSizer: wx.BoxSizer = None
    
    # TextCTRLS
    _commandNameCtrl: wx.TextCtrl = None
    _commandParamsCtrl: wx.TextCtrl = None
    _logCtrl: wx.TextCtrl = None
    
    # Buttons
    _sendButton: wx.Button = None
    
    # Checkboxes
    _traceType: wx.CheckBox = None
    
    # Current trace
    _currTrace: Trace = None
    
    # Colors
    _outC = (8, 0, 255, 255)
    _inC = (8, 0, 255, 255)
    _sysC = (197, 252, 239, 255)
    _baseC = (0, 0, 0, 0)
#endregion
    
#region Private methods and Constructor
    def __init__(self, mainWin, x, y, w, h):
        self._window = mainWin
        
        # First open configuration file
        self._conf = self._fOpener.OpenJSONFile(self._dataPath, self._confFile)
        
        # Create UI
        self._mainPanel = wx.Panel(mainWin, wx.ID_ANY, pos=(x, y), 
                                   size=(w, h))
        self._mainSizer = wx.BoxSizer(wx.VERTICAL)
        
        # Create Trace Data
        self._currTrace = Trace("", "", [], [])
        
    def __write_line(self, newLine):
        """
        This function writes a line into the log
        TextCtrl.
        
        First prepares the text to write it in the
        correct color. Then writes it. (Not implemented yet)

        Args:
            line (str): Line to write on the log.
        """
        #self._logCtrl.SetReadOnly(False)
        self._logCtrl.write(newLine)
        #self._logCtrl.SetReadOnly(True)
        self._logCtrl.ScrollLines(1)
#endregion  
   
#region UI
    #------------------------------------------------
    #------------------UI Creation-------------------
    #------------------------------------------------ 
     
    def _create_input_console(self, inputData):
        """
        This function creates the input TextCtrl
        and button, placing the different objects
        and setting it's size. 
        
        The construction data is received from a JSON
        file. 

        Args:
            inputData (hashmap): Data decoded from a JSON.
        """
        # Text Data
        nData = inputData["command_name"]
        tData = inputData["command_text"]
        
        # Button Data
        bData = inputData["send_button"]
        
        # Add title text
        tBox = wx.BoxSizer(wx.HORIZONTAL)
        text = wx.StaticText(self._mainPanel, label='Input')
        tBox.Add(text)
        self._mainSizer.Add(tBox, flag=wx.LEFT | wx.TOP, 
                            border=inputData["padding"])
        self._mainSizer.Add((-1, 5))
        
        # Add text controllers    
        self._inputSizer = wx.BoxSizer(wx.HORIZONTAL)
        self._commandNameCtrl = wx.TextCtrl(self._mainPanel,
                                            wx.ID_ANY, "",
                                            style=wx.TE_READONLY 
                                            | wx.TE_CENTER,
                                            size=(nData["size"]["w"], 
                                            nData["size"]["h"]))
        self._commandParamsCtrl = wx.TextCtrl(self._mainPanel, 
                                              wx.ID_ANY, "",
                                              size=(tData["size"]["w"], 
                                              tData["size"]["h"]))
        self._sendButton = wx.Button(self._mainPanel, 
                                     label=bData["txt"], 
                                     size=(bData["size"]["w"], 
                                     bData["size"]["h"]))
        self._sendButton.SetDefault()
        self._window.Bind(wx.EVT_BUTTON, self.OnCommandSend, self._sendButton)
        self._inputSizer.Add(self._commandNameCtrl, border=nData["padding"])  
        self._inputSizer.Add(self._commandParamsCtrl, proportion=1, 
                             border=tData["padding"])
        self._inputSizer.Add((-1, 10))
        self._inputSizer.Add(self._sendButton, flag=wx.RIGHT, 
                             border=bData["padding"])
        
        # Add it to the main sizer
        self._mainSizer.Add(self._inputSizer, 
                            flag=wx.RIGHT | wx.LEFT | wx.EXPAND, 
                            border=inputData["padding"])  
        
        # Add some space between
        self._mainSizer.Add((-1, 10))      
        
    def _create_log(self, logData):
        """
        Function that creates a Log for showing the
        conversation between the App and the dongle
        device. 

        Args:
            logData (hashmap): Decoded data from a JSON.
        """
        # Add title text
        tBox = wx.BoxSizer(wx.HORIZONTAL)
        text = wx.StaticText(self._mainPanel, label='Log')
        tBox.Add(text)
        self._mainSizer.Add(tBox, flag=wx.LEFT | wx.TOP, 
                            border=logData["padding"])
        self._mainSizer.Add((-1, 5))
        
        # Add console and Log
        self._logSizer = wx.BoxSizer(wx.HORIZONTAL)
        self._logCtrl = wx.TextCtrl(self._mainPanel, 
                                           wx.ID_ANY, 
                                           style=wx.TE_READONLY 
                                           | wx.TE_MULTILINE | wx.TE_RICH, 
                                           name=stc.STCNameStr)
        #self._logCtrl.SetReadOnly(True)
        self._logSizer.Add(self._logCtrl, proportion=1, flag=wx.EXPAND)
        self._mainSizer.Add(self._logSizer, 
                            proportion=1, 
                            flag=wx.LEFT | wx.RIGHT | wx.EXPAND, 
                            border=logData["padding"])
        # Add some space at the end
        self._mainSizer.Add((-1, 10))  
    
    #------------------------------------------------
    #------------------UI Creation-------------------
    #------------------------------------------------
#endregion     

#region Events    
    #------------------------------------------------
    #----------------Event Handling------------------
    #------------------------------------------------  
    
    def OnCommandSend(self, event):
        """
        Function that sends some command written by the 
        user. Differences between a normal command and
        the reboot command.
        
        When the command sent is the rebooting, prepares
        everything to send a command without parameters. 
        
        First writes info in the log and then sends the
        command. 

        Args:
            event (EVT_BUTTON): Sending button event.
        """
        text = self._commandParamsCtrl.GetLineText(0)
        instant = datetime.now()
        self._currTrace.SetParameters(text)
        self._currTrace.SetIsString(self._traceType.GetValue()) 
        self._currTrace.SetTimeStamp(int(datetime.timestamp(instant)))       
        self.__write_line("[Out]: " + self._currTrace.GetCommand() 
                            + " (Params): " + self._currTrace.GetParams() 
                            + "                     " 
                            + instant.strftime("%Y-%M-%D %H:%M:%S") 
                            + "\n") 
        self._window.WriteDevice(self._currTrace)
        
    def OnResponse(self, newLine):
        """
        Method called when some response is received from 
        the device. Writes the new response into the response
        log. May be overwritten for managing the responses.
        
        (PS)
        Made separately from the writing function because
        it may need some additions in the future. 

        Args:
            data (str/bytes): Data to write, bytes not supported yet
        """       
        self.__write_line(newLine)    
        
    #------------------------------------------------
    #----------------Event Handling------------------
    #------------------------------------------------ 
#endregion

#region Log Data
    #------------------------------------------------
    #-----------------Data Handling------------------
    #------------------------------------------------

    def AutoSendCommand(self):
        """Auto-sending a command. 

        This function sends a command directly to the dongle, without
        updating the input log and all. Creates the different parameters 
        needed and sends it. 
        """
        if self._currTrace.GetCommand() == "REBOOT":
            instant = datetime.now()
            self._currTrace.SetParameters(None)
            self._currTrace.SetIsString(False)
            self._currTrace.SetTimeStamp(datetime.timestamp(instant))       
            self.__write_line("[Out]: " + self._currTrace.GetCommand() 
                                + "                     " 
                                + instant.strftime("%Y-%M-%D %H:%M:%S") 
                                + "\n")  
        else:
            instant = datetime.now()
            self._currTrace.SetIsString(True)
            self._currTrace.SetTimeStamp(datetime.timestamp(instant))       
            self.__write_line("[Out]: " + self._currTrace.GetCommand() 
                              + "                     " 
                              + instant.strftime("%Y-%M-%D %H:%M:%S") 
                              + "\n")

        self._window.WriteDevice(self._currTrace)
    
    def ClearLog(self):
        """Clearing log method.

        Clears all data currently in the Log. Sets it's value
        to " " and updates. 
        """
        self._logCtrl.Remove(0, self._logCtrl.GetLastPosition())
    
    def LoadLog(self, data):
        """Load Log with data

        Sets the value of the Log with the data of a specified file
        reading it and displaying the text. 

        Args:
            data (path): File with the data to load in the Log. 
        """
        self.ClearLog()
        self._logCtrl.LoadFile(data)
    
    def GetLogData(self):
        """Get data from the log.

        This method gets all text that is currently in the log and then
        returns it as a string list. 

        Returns:
            List(str): List with all the text lines in the log.
        """
        # String list
        strings = []
        
        # Total number of lines in log
        total = self._logCtrl.GetNumberOfLines()
        
        # Read all lines
        for i in range(total):
            strings.append(self._logCtrl.GetLineText(i) + "\n")
        
        # Return lines
        return strings
    
    #------------------------------------------------
    #-----------------Data Handling------------------
    #------------------------------------------------
#endregion  