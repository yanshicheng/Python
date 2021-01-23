# 执行命令
'''
import paramiko

# 创建 SSH 对象
ssh = paramiko.SSHClient()

# 允许链接不在 know_hosts 文件中的主机
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# 连接服务器
ssh.connect(hostname='127.0.0.1', port=22, username='root', password='devops')

# 执行命令
stdin, stdout, stderr = ssh.exec_command('df -h')

# stdin.write('y')

# 获取命令结果
result = stdout.read()
print(result.decode('utf-8'))

# 关闭连接
ssh.close()
'''

# ########## 基于秘钥连接服务器

'''
import paramiko

private_key = paramiko.RSAKey.from_private_key_file('/root/.ssh/id_rsa')

# 创建 SSH 对象
ssh = paramiko.SSHClient()

# 允许连接不在 know_hosts 文件中的主机
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# 连接服务器

ssh.connect(hostname='127.0.0.1', port=22, username='root', pkey=private_key)

# 执行命令
stdin, stdout, stderr = ssh.exec_command('df -h')

# 获取命令结果
result = stdout.read()
print(result.decode('utf-8'))

# 关闭连接
ssh.close()
'''

# 上传下载文件
'''
import paramiko

transport = paramiko.Transport(('127.0.0.1', 22))
transport.connect(username='root', password='devops')

sftp = paramiko.SFTPClient.from_transport(transport)

# 上传文件
sftp.put('/tmp/l', '/tmp/lls')

# 下载文件
sftp.get('/tmp/lls', '/root/ls.rxt')

transport.close()
'''

# paramiko 模块重新封装
import paramiko


class SSHProxy(object):

    def __init__(self, hostname, port, username, password=None, private_key_path=None):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.private_key_path = private_key_path
        self.password = password
        self.transport = None

    def open(self):
        if self.private_key_path:
            private_key = paramiko.RSAKey.from_private_key_file(self.private_key_path)
            self.transport = paramiko.Transport((self.hostname, self.port))
            self.transport.connect(username=self.username, pkey=private_key)
        else:
            self.transport = paramiko.Transport((self.hostname, self.port))
            self.transport.connect(username=self.username, password=self.password)

    def close(self):
        self.transport.close()

    def command(self, cmd):
        ssh = paramiko.SSHClient()
        ssh._transport = self.transport
        stdin, stdout, stderr = ssh.exec_command(cmd)
        result = stdout.read()
        return result.decode('utf-8')

    def upload(self, local_path, remote_path):
        sftp = paramiko.SFTPClient.from_transport(self.transport)
        sftp.put(local_path, remote_path)
        sftp.close()

    def download(self, local_path, remote_path):
        sftp = paramiko.SFTPClient.from_transport(self.transport)
        sftp.get(local_path, remote_path)
        sftp.close()

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


if __name__ == '__main__':
    with SSHProxy('127.0.0.1', 22, 'root', 'devops') as ssh:
        v1 = ssh.command('sudo ip a')
        print(v1)
