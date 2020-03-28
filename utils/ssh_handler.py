import sys
from loguru import logger
from os import system
from paramiko import SSHClient, AutoAddPolicy, RSAKey, WarningPolicy
from paramiko.auth_handler import AuthenticationException, SSHException
from scp import SCPClient, SCPException
import env
import subprocess
import warnings

logger.add(sys.stderr,
           format="{time} {level} {message}",
           filter="client",
           level="INFO")
logger.add('logs/log_{time:YYYY-MM-DD}.log',
           format="{time} {level} {message}",
           filter="client",
           level="ERROR")

warnings.filterwarnings("ignore")

"""Remote host object to handle connections and actions."""


class RemoteClient:
    """Client to interact with a remote host via SSH & SCP."""

    def __init__(self, host, user, ssh_key_filepath, remote_path, upload_key=True):
        self.host = host
        self.user = user
        self.password = env.environ.get('WORKERS_PASS', None)
        self.ssh_key_filepath = ssh_key_filepath
        self.remote_path = remote_path
        self.client = None
        self.scp = None
        if upload_key:
            self.upload_ssh_key()

    def ensure_ssh_files_exists(self):
        command = 'if [ ! -d ".ssh" ]; then mkdir -p ~/.ssh; fi'

        try:
            client = SSHClient()
            client.load_system_host_keys()
            client.set_missing_host_key_policy(WarningPolicy)
            client.connect(self.host, port=22, username=self.user, password=self.password)
            client.exec_command(command)

            # check if the file authorized_keys exists
            command = 'if [ ! -f ".ssh/authorized_keys" ]; then touch ~/.ssh/authorized_keys; fi'
            client.exec_command(command)
        finally:
            if client:
                client.close()

    def check_ssh_key_exists(self):
        self.ensure_ssh_files_exists()

        command = 'cat .ssh/authorized_keys'

        try:
            client = SSHClient()
            client.load_system_host_keys()
            client.set_missing_host_key_policy(WarningPolicy)
            client.connect(self.host, port=22, username=self.user, password=self.password)
            stdin, stdout, stderr = client.exec_command(command)
            retrieved_authorized_keys = stdout.read().decode('utf-8')
            with open(env.environ.get('SSH_KEY_PUB', None)) as f:
                pub_key = f.read()
                if pub_key not in retrieved_authorized_keys:
                    return False
                return True
        finally:
            if client:
                client.close()

    def upload_ssh_key(self, append=False):
        """ Uploads an ssh public key """
        # override or append to authorized _keys
        write_delimiter = '>>' if append else '>'

        if not self.check_ssh_key_exists():
            with open(env.environ.get('SSH_KEY_PUB', None)) as f:
                key_pub = f.read()
                command = f'echo -e "{key_pub}" {write_delimiter} ~/.ssh/authorized_keys; ' \
                          f'chmod 600 ~/.ssh/authorized_keys'

                try:
                    client = SSHClient()
                    client.load_system_host_keys()
                    client.set_missing_host_key_policy(WarningPolicy)
                    client.connect(self.host, port=22, username=self.user, password=self.password)

                    print(f"[*] Dropping ssh key inside {self.host}...")
                    client.exec_command(command)
                    print(f"[+] SSH public key was dropped successfully in {self.host}.")
                except Exception:
                    print(f"[-] Failed to drop ssh public key in {self.host}.")
                finally:
                    if client:
                        client.close()
        else:
            print(f"[!] SSH public key already exists in {self.host}.")

    def __connect(self):
        """
        Open connection to remote host.
        """
        try:
            self.client = SSHClient()
            self.client.load_system_host_keys()
            self.client.set_missing_host_key_policy(AutoAddPolicy())
            self.client.connect(self.host,
                                username=self.user,
                                key_filename=self.ssh_key_filepath,
                                look_for_keys=True,
                                timeout=5000)
            self.scp = SCPClient(self.client.get_transport(), progress=self.progress)
        except AuthenticationException as error:
            logger.info('Authentication failed: did you remember to create an SSH key?')
            logger.error(error)
            raise error
        finally:
            return self.client

    def disconnect(self):
        """
        Close ssh connection.
        """
        self.client.close()
        self.scp.close()

    def execute_command(self, command):
        """
        Execute one command.

        :param command: A single string command.
        """
        if self.client is None:
            self.client = self.__connect()
        stdin, stdout, stderr = self.client.exec_command(command)
        stdout.channel.recv_exit_status()
        response = stdout.read().decode('utf-8')
        return response

    def execute_commands(self, commands):
        """
        Execute multiple commands in succession.

        :param commands: List of unix commands as strings.
        """
        if self.client is None:
            self.client = self.__connect()
        for cmd in commands:
            stdin, stdout, stderr = self.client.exec_command(cmd)
            stdout.channel.recv_exit_status()
            response = stdout.read().decode('utf-8')
            print(response)

    def bulk_upload(self, files):
        """
        Upload multiple files to a remote directory.

        :param files: List of strings representing file paths to local files.
        """
        if self.client is None:
            self.client = self.__connect()
        uploads = [self.upload(file) for file in files]
        print(f'Finished uploading {len(uploads)} files to {self.remote_path} on {self.host}')

    def upload(self, file, remote_path=None):
        """
        Upload a single file to a remote directory.

        :param remote_path:
        :param file: A file path.
        """
        if remote_path is None:
            remote_path = self.remote_path
        try:
            self.scp.put(file,
                         recursive=True,
                         remote_path=remote_path)
        except SCPException as error:
            logger.error(error)
            raise error
        finally:
            print(f'[+] Uploaded {file} to {self.remote_path}')

    def progress(self, filename, size, sent):
        sys.stdout.write("%s\'s progress: %.2f%%   \r" % (filename, float(sent) / float(size) * 100))
