"""
Dongle App, an app to control the information
received from and sent to a device, satellite
or LoRa dongle. 

Main app controller. This should initialize the 
app, set the different controllers and managers
to work and make them work together. 
"""
# Import
import wx
import rapidjson
import os

# from
from dongle.ui.main_ui import MainFrame
from dongle.device import Device

relativePath = os.path.dirname(os.path.abspath(__file__))

def run():
    """
    Main function that sets the application and all 
    necessary objects to make it run properly. 

    Initializes the window and the different sizers 
    and sets them to work together.
    """
    # Create App instance
    app = wx.App(False)
    
    frame = MainFrame(None, relativePath, "data/cnf/app.json")

    # Set the app to detect events
    app.MainLoop()
