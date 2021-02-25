"""Trace file.

This file contains the class Trace, which represents the information 
that will be sent to the USB device. It is made to only manage the 
information. 
"""
class Trace:
    """
    Class to store sending info. Used for 
    managing the different information that 
    is needed to be sent and received. 

    Returns:
        str: Command to send or it's parameters
    """
    __command = None
    __params = None
    __commandBytes = None
    __paramBytes = None
    __isstring = False
    __timestamp = None
    
    def __init__(self, command, param, cBytes, pBytes):
        """
        This class is used to store the value of the command to be sent
        or received. 

        Args:
            command (String): [description]
            param (String): [description]
            cBytes (byte): [description]
        """
        self.__command = command
        self.__params = param
        self.__commandBytes = cBytes
        self.__paramBytes = pBytes
        
    #------------------------------------------------
    #--------------------Setters---------------------
    #------------------------------------------------
    
    def SetCommand(self, cmd):
        """
        Sets the command name of this trace.

        Args:
            cmd (str): Command name
        """
        self.__command = cmd
        
    def SetCommandCode(self, code):
        """
        Sets the byte combination that 
        represents the command. 

        Args:
            code (bytes): Byte list
        """
        self.__commandBytes = code
        
    def SetParameters(self, params):
        """
        Sets the parameters that come with the command.

        Args:
            params (str): String with the parameters
        """
        self.__params = params
        
    def SetParametersBytes(self, bParams):
        """
        Sets the value of the parameters translated to
        byte codes. 

        Args:
            bParams (list): Byte list
        """
        self.__paramBytes = bParams
        
    def SetIsString(self, string):
        """
        Set the type of trace that is going to be sent.

        Args:
            string (bool): Trace type
        """
        self.__isstring = string
        
    def SetTimeStamp(self, t):
        """
        Set the timsetamp of this trace.

        Args:
            t (timestamp): Epoch Unix timestamp
        """
        self.__timestamp = t
    
    #------------------------------------------------
    #--------------------Setters---------------------
    #------------------------------------------------        
        
    #------------------------------------------------
    #--------------------Getters---------------------
    #------------------------------------------------
        
    def GetCommand(self):
        """
        Method used to return the command value.

        Returns:
            str: Command name in string value
        """
        return self.__command
    
    def GetParams(self):
        """
        Method that provides access to the parameters 
        of this command

        Returns:
            str: Parameters of the command
        """
        return self.__params
    
    def GetCommandCode(self):
        """
        Provides access to the command bytes.

        Returns:
            byte: List of the bytes that represent the command
        """
        return self.__commandBytes
    
    def GetParamBytes(self):
        """
        Provides access to the parameter bytes
        info.

        Returns:
            bytes: Byte list of the parameters
        """
        return self.__paramBytes
    
    def GetIsString(self):
        """
        Method to get if the trace is a string-type
        trace or a byte-type trace.
        
        True = string-type
        False = byte-type

        Returns:
            bool: Trace type
        """
        return self.__isstring
    
    def GetTimeStamp(self):
        """
        Method to access the timestamp of this 
        trace. 

        Returns:
            timestamp: Epoch Unix timestamp
        """
        return self.__timestamp

    #------------------------------------------------
    #--------------------Getters---------------------
    #------------------------------------------------