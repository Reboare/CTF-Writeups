> original data: "El Psy Congroo"
encrypted data: "IFhiPhZNYi0KWiUcCls="
encrypted flag: "I3gDKVh1Lh4EVyMDBFo="  
The flag is not in the traditional gigem{flag} format. 

``` python
>>> import base64 
>>> msg = "El Psy Congroo" 
>>> enc_data =  "IFhiPhZNYi0KWiUcCls=" 
>>> enc_flag = "I3gDKVh1Lh4EVyMDBFo=" 
>>> enc_data = base64.b64decode(enc_data) 
>>> enc_flag = base64.b64decode(enc_flag) 
>>> ''.join([chr(ord(a) ^ ord(b)) for a,b in zip(enc_data,msg)]) 
'e4Bne4Bne4Bne4' 
>>> ''.join([chr(ord(a) ^ ord(b)) for a,b in zip(enc_flag, 'e4Bne4Bne4Bne4')]) 
'FLAG=Alpacaman' 
``` 
