# coding: utf-8

from stat import S_ISDIR
import os
import re
import time
import paramiko

DEFAULT_TIMEOUT=180000

class SshClient():
    def __init__(self):
        self.host = None
        self.username = None
        self.passwd = None
        self.port = None
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.prompts = [
            '> ',
            '# ',
            ': ',
            '? ',
            '$ ',
            '>',
            ':',
            ']',
            '?',
            '#',
            '$'
        ]
        self.sftp = None
        self.transport = None

    def connect(self,host,username,passwd,port=22,**kwargs):
        self.host = host
        self.username = username
        self.passwd = passwd
        self.port = port
        self.ssh.connect(self.host,self.port,self.username,self.passwd,look_for_keys=False,**kwargs)
        self.channel = self.ssh.invoke_shell(width=320)
        self.channel.settimeout(DEFAULT_TIMEOUT)
        print(self.recv())
        self.transport = paramiko.Transport((self.host,self.port))
        self.transport.connect(username=self.username,password=self.passwd)
        self.sftp = paramiko.SFTPClient.from_transport(self.transport)
        time.sleep(2)
    
    def command(self,command):
        stdin,stdout,stderr = self.ssh.exec_command(command)
        output = stdout.readlines()
        return output
    
    def send(self,command):
        self.channel.send(command+'\n')

    def recv(self,timeout=None,num=1024):
        if timeout is not None:
            self.channel.settimeout(timeout)
        buff = ''
        while not self.recv_ok(buff.strip()):
            curbuff = self.channel.recv(num)
            curbuff = curbuff.decode('GBK')
            curbuff = re.sub('\033\[\d*;?\d*[mK]\017?','',curbuff)
            buff += curbuff
        if timeout is not None:
            self.channel.settimeout(DEFAULT_TIMEOUT)
        return buff

    def recv_ok(self,buff):
        for prompt in self.prompts:
            if buff.endswith(prompt):
                return True
            return False

    def ssh_close(self):
        self.ssh.close()

    def __reconnect(self):
        if not self.sftp or self.sftp.sock.closed:
            t = paramiko.Transport((self.host,self.port))
            t.connect(username=self.username,password=self.passwd)
            self.sftp = paramiko.SFTPClient.from_transport(t)

    def upload(self,local,remote):
        self.__reconnect()
        try:
            self.sftp.put(local,remote)
        except IOError as e:
            if 'size mismatch in put' not in str(e):
                raise e
        else:
            print(e)
        
    def download(self,remote,local):
        self.__reconnect()
        self.sftp.get(remote,local)
    
    def download_dir(self,remote_dir,local_dir):
        self.__reconnect()
        files = self.sftp.listdir_attr(remote_dir)
        for f in files:
            if S_ISDIR(f.st_mode):
                continue
            else:
                fullname = remote_dir + os.sep + f.filename
                self.sftp.get(fullname,os.path.join(local_dir,f.filename))

    def close(self):
        self.ssh.close()
        if self.transport:
            self.transport.close()
def main():
    ssh = SshClient()
    ssh.connect('192.168.128.129','grape','123456')
    res = ssh.command('ls /home')
    print(res)
    ssh.close()

if __name__ == '__main__':
    main()
