import env
from utils.setup_hadoop import setup_hadoop
from utils.setup_java import setup_java
from utils.generate_xml_conf import generate
from os import system

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
    print("[+] Master was set up successfully!")
