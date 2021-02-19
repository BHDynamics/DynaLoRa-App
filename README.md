DynaLoRa-App
---

A crossplatform-desktop app for controlling the DynaLoRa device and send messages, 
set the device to hear for new commands and incomming messages and much more.

Description
------

This is a Desktop Application for the device DynaLoRa-USB. It's functionality 
is to control some commands that can be sent to the device in order to make it
work. 

The currently supported commands are: Listening for messages (RX), Sending 
a message (TX), Place in Queue (PLQ), Send queue (TXQ), Clear Queue (FQ) and 
Reboot system (RBT). The Reboot system command needs the String-type trace 
checkbox to be unchecked, this will be fixed in later versions. 

Current log can be saved in a file, that if there is no path provided for the 
file to be saved, it will be automatically saved in the Users path under the 
folder BHDYN. Some help and tutorials can be found inside the app that lead to 
a web page with information about the device and an email to contact us if there
is any problem. 


Adding features, modifying the app
------

If you want to add new features to the app or contribute to it's development go 
to our [repository](https://github.com/BHDynamics/DynaLoRa-App "BHDynamics repo") and clone
it in your system. Make sure that some version of `python 3.X` is installed in your machine
and run **setup.py** file. This will install the different dependencies that the 
app needs. This includes: *wxPython*, the GUI library that manages the interactable 
part; *python-rapidjson*, a json loading library that is very efficient and quick; and
*pyserial*, the library that manages the connection with the USB port. 

It will also install **pyinstaller**, which is the tool used to build the app. With this
library you make your own build to test that what you did can work correctly and 
without python installed in a machine. To do this, you just need to run the 
*build_OS* file found within the files of the repository. For windows systems use
*build_win.bat* and for unix-like systems (raspbian, ubuntu, debian, etc.) run
*build_unix.sh*. This file can also be used in MacOS. This file will run the 
**setup.py** file too, for assuring that all dependencies are correctly installed. 

If your modification only adds more buttons, just add the corresponding button
information in the "dongle_ui.json". The format is simple:

{
    `command`: "RX",
    `txt`: "RX",
    `byte`: "FFFF"
}

The `command` field is for the command name and the string that will be sent to the 
device to execute that command. The `txt` field is for the text that will be shown 
later in the button. The `byte` field is for sending byte-codified traces, this will
be the byte that is going to identify the command. 

If some modification os going to be added to the app, consult the documentation
provided at **PLACEHOLDER**. 