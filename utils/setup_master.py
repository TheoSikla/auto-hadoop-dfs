import env
from utils.setup_hadoop import setup_hadoop
from utils.setup_java import setup_java
from utils.generate_xml_conf import generate
from os import system, path

create_failsafe_dot_profile = f'if [ ! -f {env.hadoop_user_home}/.profile2 ]; then ' \
                              f'cp {env.hadoop_user_home}/.profile {env.hadoop_user_home}/.profile2;' \
                              f'chown hadoop:hadoop {env.hadoop_user_home}/.profile2; fi'

export_path_with_new_binaries = f'cat {env.hadoop_user_home}/.profile2 > {env.hadoop_user_home}/.profile;' \
                                f'echo "PATH={env.hadoop_user_home}/java/bin:{env.hadoop_user_home}/hadoop/bin:{env.hadoop_user_home}/hadoop/sbin:\$PATH" >> ' \
                                f'{env.hadoop_user_home}/.profile;'


def master_init():
    print("[+] Initiating master node...")
    setup_java()
    setup_hadoop()

    print("[+] Generating custom configuration...")
    generate()
    system(create_failsafe_dot_profile)
    system(export_path_with_new_binaries)

    if not path.isfile(f"{env.environ.get('SSH_KEY')}") or not path.isfile(f"{env.environ.get('SSH_KEY_PUB')}"):
        if not path.isdir('~/.ssh'):
            system('mkdir ~/.ssh')

        print("[!] SSH key does not exist.")
        print("[+] Generating new SSH key...")
        system("ssh-keygen -t rsa -b 4096 -N '' -f ~/.ssh/id_rsa")
        print("[+] SSH key was created successfully.")

    if not path.isfile('~/.ssh/authorized_keys'):
        system('touch ~/.ssh/authorized_keys;')
        system(f"cat {env.environ.get('SSH_KEY_PUB')} > ~/.ssh/authorized_keys")

    print("[+] Master was set up successfully!\n")
