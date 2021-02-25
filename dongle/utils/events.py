"""Events

This file contains the different events needed for the app to work 
correctly. This events are self-made and integrated with wxPython's
events. 
"""
# WX import
import wx
import wx.lib.newevent as ne

# Serial CONNECTION events
SerialCTrue, EVT_SERIALC = ne.NewEvent()
SerialCError, EVT_SERIALCE = ne.NewEvent()
SerialCDisconnect, EVT_SERIALD = ne.NewEvent()
SERIALC = wx.NewEventType()

# Serial READING events
SerialREvent, EVT_SERIALR = ne.NewEvent()
SerialRError, EVT_SERIALRE = ne.NewEvent()
SerialRMessage, EVT_SERIALRM = ne.NewEvent()
SerialRFrameErr, EVT_SERIALFE = ne.NewEvent()
SERIALR = wx.NewEventType()

# Serial WRITING events
SerialWEvent, EVT_SERIALW = ne.NewEvent()
SerialWErr, EVT_SERIALWE = ne.NewEvent()
SERIALW = wx.NewEventType()

# Device connection MENU events
DeviceDEvent, EVT_DEVDISCONNECT = ne.NewEvent()
DeviceCEvent, EVT_DEVCONNECT = ne.NewEvent()
DEVEVENT = wx.NewEventType()

# Terminal events
TerminalSend, EVT_SEND = ne.NewEvent()
TEVENT = wx.NewEventType()

# Button events
ButtonSelectedEvent, EVT_SELECT = ne.NewEvent()
BUEVENT = wx.NewEventType()