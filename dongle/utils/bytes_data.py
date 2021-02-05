class ByteCodes:
    SOF = 0xF0
    SOF_R = 0xF1
    EOF = 0x0F
    EOF_R = 0x1F
    ACK = bytes([SOF_R, 0, 0, 0, EOF_R])
    
    # Bytes codification and hashing
    def crc16(self, data, poly=0x8408):
        """
        Method to calculate the checksum of the 
        different traces when they are going to
        be sent to the device. 
        
        This one calculates the hash code using the 
        CRC-16/CCITT standard.

        Args:
            data (bytes): byte list to calculate hash
            poly (hexadecimal, optional): Type. Defaults to 0x8408.

        Returns:
            bytes: has of the trace as a byte list
        """
        data = bytearray(data)
        crc = 0xFFFF
        for b in data:
            currByte = 0xFF & b
            for _ in range(0, 8):
                # Logic operations using AND and XOR
                if(crc & 0x0001) ^ (currByte & 0x0001):
                    crc = (crc >> 1) ^poly
                else:
                    # Right shifting byte
                    crc >>= 1
                
                # Right shifting byte
                currByte >>= 1
        
        crc = (~crc & 0xFFFF)
        crc = (crc << 8) | ((crc >> 8) & 0xFF)
        
        return crc & 0xFFFF
                