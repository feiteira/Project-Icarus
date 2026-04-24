#!/usr/bin/env python3
import paramiko, sys

HOST = '213.239.213.155'
# Try different users
users = ['admin', 'root', 'ubuntu', 'feiteira', 'debian']
PASS = 'WikiPass123'

for USER in users:
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(HOST, username=USER, password=PASS, timeout=8)
        print(f"SUCCESS with user: {USER}")
        stdin, stdout, stderr = client.exec_command('whoami; ls /etc/nginx/sites-enabled/ 2>/dev/null')
        print(stdout.read().decode())
        client.close()
        break
    except paramiko.ssh_exception.AuthenticationException:
        print(f"Failed: {USER}")
    except Exception as e:
        print(f"Error {USER}: {e}")