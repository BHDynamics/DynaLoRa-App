# External libraries imports
import serial
import serial.tools.list_ports as lp 
import re
import threading
import wx
import dongle.utils.events as ev
import struct
import time

# Internal imports
from dongle.utils.bytes_data import ByteCodes
from dongle.utils.trace import Trace

# Class to manage the connection with the device
class Device:
    """
    Class for controlling the communication 
    between the App and the USB device. 

    Serves as a manager for the device, 
    because stores all the information 
    relative to the serial connection. 

    First searches for an available device
    connected to a serial port, then checks 
    if the device is avalid one, checking the
    VID and PID with the registered devices
    for the app. When a device is found, connects
    to it and begins the communication. 

    Implements the interface "Observable", for
    sending messages to the different objects
    registered to the notifications of this object.

    Manages a thread that will check the 
    different information received from the 
    device connected.  
    """
#region Variables
    # Device connected 
    _device = None
    
    # Connection status
    _connected = False
    
    # Port of the device
    _port = None
    
    # Dictionary of registered devices
    _devices = {}
    
    # Connection thread to manage readings
    _connectionThread = None
    
    # Port controller thread
    _portController = None
    _stopEvent: threading.Event = None
    
    # wx listener
    _listener = None
    
    # Controller for closing app
    _alive = False
#endregion

    #------------------------------------------------
    #--------------------Private---------------------
    #------------------------------------------------

# region Construction
    def __init__(self, configuration, listener):
        """
        Basically search for available devices in serial port
        communication and check which one is the dongle. First
        read all valid VID:PID from the configuration value 
        passed in. After saving those values into an internal
        variable, search for available devices.

        If a registered device is found, connect to it and update
        connected value. 
        """
        self._alive = True
        data = {} # Dictionary with the VID:PID
        for dev in configuration:
            tempVID = dev["VID"][2:]
            tempPID = dev["PID"][2:]
            data["VID"] = bytes.fromhex(tempVID)
            data["PID"] = bytes.fromhex(tempPID)
            self._devices[dev["name"]] = data

            # Reset data
            data = {}
            
        self._listener = listener

        # Search for devices
        self.__search()
        if(self._port != None):
            # Update connection flag
            self._connected = True
            
            # Connect and etc.
            self._device = serial.Serial(self._port, 115200, timeout=1)
            
            # Begin connection thread to manage readings
            self._stopEvent = threading.Event()
            self._connectionThread = threading.Thread(name="Reading thread", target=self.__read, args=(self._devices, self._stopEvent))
            
            # Then start a daemon thread to check if device is still connected
            self._portController = threading.Thread(target=self.__check_connection, args=(self._stopEvent, self, self._port, 0.1))
            
            # Start threads
            self._connectionThread.start()
            self._portController.start()
            
            wx.PostEvent(self._listener, ev.SerialCTrue())
#endregion   
            
#region Connection Management  
    # Search for devices
    def __search(self):
        """
        This function searches for valid USB devices
        connected to USB ports in the computer.

        Gets a list of available ports and the devices
        connected to them. Then gets the different 
        VIDs and PIDs from the devices and checks their
        value with the devices registered. 

        If the device is one of the registered ones, then 
        saves the port to which is connected and ends.
        """
        for e in list(lp.comports()):
            # Get the vid and pid from the device
            info = e.hwid.split()
            if("VID:PID" in info):
                nStr = re.split(":|=", info[1])
                vid = bytes.fromhex(nStr[2])
                pid = bytes.fromhex(nStr[3])

                # Check values with registered devices
                for dev in self._devices:
                    if(self._devices[dev]["VID"] == vid and self._devices[dev]["PID"] == pid):
                        # Save port and end loops
                        try:
                            ser = serial.Serial(e.name, 115200, timeout=1)
                            self._port = e.name
                            print(self._port)
                            ser.close()
                            break
                        except serial.SerialException as e:
                            pass
                        
    
    # Connection checking  
    def __check_connection(self, stop_event, dev, port, interval=0.1):
        """
        Method to check if device gets disconnected. This is
        usefull for managing disconnection and save the state
        of the app if needed, or at least notify the user 
        if he wants to save the current state. 
        
        Checks constantly the list of available ports and then
        looks for the device's port. If the port is not found
        in the list, then notify the disconnection and begin 
        a process to save the state, stop threads and clean 
        the program of dead variables.

        Args:
            port (String): Port of the device connected.
            interval (float, optional): Sets the interval
                                        to sleep the thread.
                                        Defaults to 0.1.
        """
        while not stop_event.is_set():
            ports = [tuple(p) for p in list(lp.comports())]
            if not ports:
                print("No device is connected")
                dev.close()
                break
            
            deviceConnected = False
            
            for device in ports:
                if port in device:
                    # Check if port is not in available ports
                    # and notify its new status
                    deviceConnected = True
                    
            if not deviceConnected:
                dev.close
            
            time.sleep(interval)

    # Connection closing flow
    def __close_connection(self):
        """
        This function manages the disconnection of 
        the device. Checks that all threads stopped 
        and resets all data from this object, to 
        notify the GUI correctly.
        """
        # Set connection to False
        self._connected = False
        self._stopEvent.set()
        
        # Then wait for connection thread to end
        self._connectionThread.join()
        
        # Close device's connection
        self._device.close()
        
        # Remove device and connection data
        self._device = None
        self._port = None
        
        # Notify the GUI listener
        wx.PostEvent(self._listener, ev.SerialCDisconnect())
#endregion

#region Reading data from the device
    def __validate_frame(self, frame):
        """
        This function validates a frame received 
        from the device, checking if some information
        was corrupted during transmission.
        
        This also can be used to check if the frame
        that is going to be send is correct. This means
        the information is correctly coded and the
        bytes that are going to be send are correct. 

        Args:
            frame (ByteList): The list of bytes 
                              representing the frame
            send (Bool): Flag for checking sending message
                         or received message.

        Returns:
            Bool: Returns whether frame is valid.
        """
        newStr = frame.decode('utf-8')
        if ";" not in newStr:
            # Check sending message
            last = len(frame) - 1
            
            if(frame[0] != ByteCodes.SOF_R or frame[last] != ByteCodes.EOF_R):
                return False
            else:
                # Checksum 
                calculateSum = frame.copy()
                del calculateSum[0]
                del calculateSum[(len(calculateSum) - 3):(len(calculateSum) - 1)]
                checkSum = sum(calculateSum)
                frameCheck = int.from_bytes(bytes([frame[last - 2], frame[last - 1]]), "big")
                
                if(checkSum == frameCheck):
                    # Frame is not corrupted
                    return True
                else:
                    return False
        else:
            temp = newStr.split(";")
            
            if (temp[0] == "DLR" or temp[0] == "DLM") and (temp[len(temp) - 1] == "EOR" or temp[len(temp) - 1] == "EOM"):
                return True
            else:
                return False

    
    def __read(self, iter, stop_event):
        """
        Function that manages the information received from 
        the device. Manages the different responses and 
        checks if the information received is not corrupted.
        
        Then if the frame is not corrupted and is valid, throws 
        a WX event created previously with the data received
        from the USB device. If the frame is corrupted, then 
        throws a self-made error event to notify the GUI to 
        change and show the error. 
        """
        print("Starting read thread")
        while not stop_event.is_set():
            #print("We keep reading")
            # Controlling an error while reading
            # This one can occur when the device 
            # disconnects abruptly and the controlling
            # had no time to manage the disconnection
            try:
                # Check if bytes are available on the device
                # and read them, then notify observers for 
                # updating info on screen
                b = self._device.readline(self._device.in_waiting)
                if b:
                    print(b)
                    if self.__validate_frame(b):
                        wx.PostEvent(self._listener, ev.SerialREvent(data=b))
                    else:
                        message = b.decode('utf-8')
                        if "Overflow" not in message:
                            wx.PostEvent(self._listener, ev.SerialRMessage(data=b))
                        else:
                            wx.PostEvent(self._listener, ev.SerialRFrameErr(data=b))
            
            except serial.SerialException as e:
                print("Error")
                # Writing error occured while sending data to USB device
                wx.PostEvent(self._listener, ev.SerialRError(data=e))

#endregion 

    #------------------------------------------------
    #--------------------Private---------------------
    #------------------------------------------------

#region Device control and checking
    def close(self):
        """
        This function is in charge of closing port connection
        and communications. Changes _alive flag, indicating
        that app is no more alive and terminates all threads.
        
        Then closes serial.
        """
        self._alive = False
        self.__close_connection()

    # Check device status
    def is_connected(self):
        """
        Returns the status of the serial connection. 
        True when connected and False when not. 
        """
        return self._connected
    
    def get_port(self):
        """
        Returns the port to which the device is connected.
        Use this only to check a string.

        Returns:
            str: Connected port
        """
        return self._port
    
    def get_port_data(self):
        """
        Searches for the port information and returns it.

        Returns:
            str: Port information (if device is connected)
        """
        if self.is_connected():
            ports = [tuple(p) for p in list(lp.comports())]
            if not ports:
                return "No device is connected"
    
            for device in ports:
                if self._port in device:
                    # Check if port is not in available ports
                    # and notify its new status
                    return device
        else:
            return "No device connected"
#endregion

#region Writing
    def write(self, trace: Trace):
        """
        This method is used to write some information in the 
        USB device with a specific command. First checks that
        is a valid command and then creates the frame to send 
        to the device. After that, checks that the frame is
        valid and then writes it on the device. 

        Args:
            command (Bytes): Command to send
            payload (Bytes): Byte array with the command data
            string (boolean): Flag that indicates if sending 
                              uses strings or bytes as sending
                              method.
        """
        data = None        
        # Check connection status
        if self.is_connected():
            try:
                # Check if trace is string mode or byte mode
                if not trace.GetIsString():
                    
                    # Check if it is a reboot command
                    if trace.GetCommandCode() == b'\x04':
                        # If so, send it without doing anything else
                        self._device.write(b'\x03')
                        self._device.write(trace.GetCommandCode())
                    else:
                        # First create frame
                        data = []
                        
                        # Add data to byte array
                        data.extend(struct.pack('<H', len(trace.GetParamsCode())))
                        data.extend(trace.GetCommandCode())
                        data.extend(trace.GetParametersBytes())
                        
                        # Calculate hash
                        checksum = ByteCodes.crc16(data) # This converts to byte list
                        data.extend(checksum)
                        
                        # Set values of start and end
                        data.insert(0, ByteCodes.SOF)
                        data.append(ByteCodes.EOF)
                    
                        self._device.write(data)
                else:
                    # Calculate the number of parameters
                    length = trace.GetParams().split(";")
                    
                    # Now create frame
                    data = 'DLC;{leng};{comm};{pld};{tmp}'.format(
                        leng=len(length),
                        comm=trace.GetCommand(),
                        pld=str(trace.GetParams()),
                        tmp=str(trace.GetTimeStamp())
                    ) # string.format
                    # For debugging, print trace
                    print(data)
                    print(data.encode())
                
                    self._device.write(data.encode())
                
                
            except serial.SerialException as e:
                # Writing error occured while sending data to USB device
                wx.PostEvent(self._listener, ev.SerialWErr(data=e))
        else:
            # Device not connected, not sending data, throw an error (tuercebotas)
            wx.PostEvent(self._listener, ev.SerialCFalse())
#endregion