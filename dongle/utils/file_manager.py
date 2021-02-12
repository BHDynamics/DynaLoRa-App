# Data saver, interacts with the OS
# Satelite will be in a JSON(?)
import os
import time 
import rapidjson
import errno

t = time.localtime()
currentTime = time.strftime("%Y%m%d", t)
print(currentTime)
savingDir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'data/logs'))
print(savingDir)

class Opener:
    """
    This class is opening files storing 
    logs and information about the app and 
    the user's activity.
    """
    def OpenFile(self, dirname, filename):
        """
        This function opens a file and returns it 
        as a file type variable. 

        Args:
            dirname (str): Directory name
            filename (str): File name 

        Returns:
            (File): Opened file
        """
        # Create filepath for opening
        f = os.path.join(dirname, filename)
        
        # Open file
        return open(f, 'r')
    
    def OpenJSONFile(self, dirname, filename):
        """
        This function opens a file and decodes it into
        an object using JSON utilities.

        Args:
            dirname (str): Directory
            filename (str): filename

        Returns:
            Object: File decoded as JSON
        """
        # Create filepath for opening
        f = os.path.join(dirname, filename)
        
        # Open file and decode JSON
        with open(f, 'r') as file:
            data = rapidjson.load(file)
            
            return data
                
    def OpenAndReadFile(self, dirname, filename):
        """
        Opens a file and reads all the data stored
        in it. Saves all that data into a list of 
        strings and then returns it for the app to 
        use it. 

        Args:
            dirname (str): Folder direction
            filename (str): Filename

        Returns:
            List: List of strings with all the data
        """
        # Create filepath for opening
        f = os.path.join(dirname, filename)
        
        # Open file
        with open(f, 'r') as log:
            # Read all file and translate to string list
            data = log.read()
            strings = list(data)
            log.close()
            
            return strings

class Saver:
    """
    This class manages saving information into 
    files, whereas in a specified file and folder
    or in an application generated file. 
    """
    
    _savingDir = None
    
    def __init__(self):
        # Get the path where all data savings and configs will go
        self._savingDir = os.path.dirname(__file__)
        print(self._savingDir)
        self._savingDir = os.path.abspath(os.path.join(os.path.expanduser(os.getenv('USERPROFILE')), 'BHDYN/DynaLoRa-USBa/data/logs'))
        if not os.path.exists(os.path.dirname(self._savingDir)):
            try:
                os.makedirs(os.path.dirname(self._savingDir))
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    raise
        print(self._savingDir)
        
    def GetSavingDir(self):
        return self._savingDir
        
    def SaveTextLog(self, data):
        """
        Saves data into a file generated in a specific location
        within the application with normal string format. 

        Args:
            data (String/List): Data to save.
        """
        # Get time for creating a fileName
        t = time.localtime()
        currentTime = time.strftime("%Y%m%d%H%M%S", t) + ".log"
        fileDir = os.path.join(self._savingDir, currentTime)
        
        print(fileDir)
        
        # Then open file and dump data into it
        d = "".join(data)
        with open(fileDir, 'w') as raw:
            raw.write(d)
            raw.close()
            
    def SaveTextLogAs(self, dirname, filename, data):
        """
        Saves data into a specific file and location with 
        a normal string format. 

        Args:
            dirname (String): Folder direction
            filename (String): File name
            data (String/List): Data to save
        """
        # Create filename and data to save
        fileDir = os.path.join(dirname, filename)
        d = "".join(data)
        
        # Open file and dump data into it
        with open(fileDir, 'w') as raw:
            raw.write(d)
            raw.close()