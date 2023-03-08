# kill_server.py

import os
import subprocess
import re

def kill_server(host, port):
    port = port
    host = host
    cmd_newlines = r'\r\n'

    host_port = host + ':' + str(port)
    pid_regex = re.compile(r'[0-9]+$')

    netstat = subprocess.run(['netstat', '-n', '-a', '-o'], stdout=subprocess.PIPE)
    # Doesn't return correct PID info without precisely these flags
    netstat = str(netstat)
    lines = netstat.split(cmd_newlines)

    for line in lines:
        if host_port in line:
            pid = pid_regex.findall(line)
            if pid:
                pid = pid[0]
                os.system('taskkill /F /PID ' + str(pid))

    # And finally delete the .pyc cache
    os.system('del /S *.pyc')