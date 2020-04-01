import env
from utils.ssh_handler import RemoteClient
from utils.checks import get_artifacts_full_path
from utils.entities import get_master, get_workers

java_tar_file_name = env.environ.get('JAVA_TAR_FILE_NAME', None)
hadoop_tar_file_name = env.environ.get('HADOOP_STABLE_VERSION_NAME_TAR', None)
pub_key_file_path = env.environ.get('SSH_KEY_PUB', None)
hadoop_worker_user_name = env.environ.get('WORKERS_USERNAME', None)

# Available commands
check_java_tar_exists = f'if [ ! -f "{env.hadoop_user_home}/{java_tar_file_name}" ]; then ' \
                        f'echo "False"; else echo "True"; fi'

check_java_dir_exists = f'if [ ! -d "{env.hadoop_user_home}/java" ]; then ' \
                        f'echo "False"; else echo "True"; fi'

delete_java_dir = f'rm -rf {env.hadoop_user_home}'

unpack_java_tar = f'tar zxf {env.hadoop_user_home}/{java_tar_file_name} -C {env.hadoop_user_home}'

check_hadoop_tar_exists = f'if [ ! -f "{env.hadoop_user_home}/{hadoop_tar_file_name}" ]; then ' \
                        f'echo "False"; else echo "True"; fi'

check_hadoop_dir_exists = f'if [ ! -d "{env.hadoop_user_home}/hadoop" ]; then ' \
                        f'echo "False"; else echo "True"; fi'

unpack_hadoop_tar = f'tar zxf {env.hadoop_user_home}/{hadoop_tar_file_name} -C {env.hadoop_user_home}'

create_failsafe_dot_profile = f'if [ ! -f {env.hadoop_user_home}/.profile2 ]; then ' \
                              f'cp {env.hadoop_user_home}/.profile {env.hadoop_user_home}/.profile2;' \
                              f'chown hadoop:hadoop {env.hadoop_user_home}/.profile2; fi'

export_path_with_new_binaries = f'cat {env.hadoop_user_home}/.profile2 > {env.hadoop_user_home}/.profile;' \
                                f'echo "PATH={env.hadoop_user_home}/java/bin:{env.hadoop_user_home}/hadoop/bin:{env.hadoop_user_home}/hadoop/sbin:\$PATH" >> ' \
                                f'{env.hadoop_user_home}/.profile;'

is_wsl = f'if grep -q Microsoft /proc/version; then ' \
         f'echo "True"; else echo "False"; fi'

create_failsafe_hosts_file = f'if [ ! -f {env.hadoop_user_home}/hosts ]; then ' \
                             f'cp {env.environ.get("HOSTS_FILE", None)} "$HOME/hosts"; fi'


def append_to_hosts_file(rc):
    payload = get_workers()
    payload.append(get_master())
    hosts_file = env.environ.get('HOSTS_FILE', None)
    rc.execute_command(f'if [ -f {env.hadoop_user_home}/hosts ]; then cat "$HOME/hosts" > {hosts_file}; fi')
    for entry in list(reversed(payload)):
        ip = entry['ip']
        hostname = entry['hostname']
        rc.execute_command(f'echo -e "{ip}\t{hostname}" >> {hosts_file}')

    if translate_to_bool(rc.execute_command(is_wsl)):
        retrieved_hostfile = rc.execute_command(f'cat {hosts_file}')
        lines_to_write = []
        for line in retrieved_hostfile.split('\n'):
            flag = False
            for item in line.split('\t'):
                if 'DESKTOP' in item:
                    flag = True
            if flag:
                items = line.split('\t')
                line = f'{items[0]}\t{rc.host}\t'
                line += '\t'.join([_ for _ in items[1:]])
            lines_to_write.append(line)
        lines_to_write = '\n'.join(lines_to_write)
        rc.execute_command(f'echo -e "{lines_to_write}" > {hosts_file}')


def translate_to_bool(string):
    string = string.strip()
    if string == "True":
        return True
    return False


def transfer_custom_hadoop_conf(remote_client, hostname):
    print(f"[+] Copying master hadoop configuration to {hostname}...")
    remote_client.upload(env.environ.get('HADOOP_CONF_DIR', None),
                         remote_path=env.environ.get('HADOOP_CONF_DIR_ETC', None))
    print(f"[+] Configuration copy finished successfully.")


def worker_init(hostname, unpack=True):
    workers_username = env.environ.get('WORKERS_USERNAME', None)
    ssh_key_path = env.environ.get('SSH_KEY', None)
    remote_path = env.environ.get('REMOTE_PATH', None)
    rc = RemoteClient(hostname, workers_username, ssh_key_path, remote_path)

    print(f"[+] Connected to {hostname}.")

    # Check if java exists
    if not translate_to_bool(rc.execute_command(check_java_dir_exists)):
        if not translate_to_bool(rc.execute_command(check_java_tar_exists)):
            print("[+] Uploading java tar...")
            rc.upload(f"{get_artifacts_full_path()}/{java_tar_file_name}")
            print("[+] Upload completed successfully.")
            print("[+] Unpacking java tar...")
            rc.execute_command(unpack_java_tar)
            print("[+] Unpacking completed successfully.")
            rc.execute_command(f"mv -f {env.hadoop_user_home}/{env.environ.get('JAVA_DIR_NAME', None)} "
                               f"{env.hadoop_user_home}/java")
        else:
            print("[+] Java tar already uploaded.")
            if unpack:
                print("[+] Unpacking java tar...")
                rc.execute_command(unpack_java_tar)
                print("[+] Unpacking completed successfully.")
                rc.execute_command(f"mv -f {env.hadoop_user_home}/{env.environ.get('JAVA_DIR_NAME', None)} "
                                   f"{env.hadoop_user_home}/java")

    # Check if hadoop exists
    if not translate_to_bool(rc.execute_command(check_hadoop_dir_exists)):
        if not translate_to_bool(rc.execute_command(check_hadoop_tar_exists)):
            print("[+] Uploading hadoop...")
            rc.upload(f"{get_artifacts_full_path()}/{hadoop_tar_file_name}")
            print("[+] Upload completed successfully.")
            print("[+] Unpacking hadoop tar...")
            rc.execute_command(unpack_hadoop_tar)
            print("[+] Unpacking completed successfully.")
            rc.execute_command(f"mv -f {env.hadoop_user_home}/{env.environ.get('HADOOP_STABLE_VERSION_NAME', None)} "
                               f"{env.hadoop_user_home}/hadoop")
            transfer_custom_hadoop_conf(rc, hostname)
        else:
            print("[+] Hadoop tar already uploaded.")
            if unpack:
                print("[+] Unpacking hadoop tar...")
                rc.execute_command(unpack_hadoop_tar)
                print("[+] Unpacking completed successfully.")
                rc.execute_command(f"mv -f {env.hadoop_user_home}/{env.environ.get('HADOOP_STABLE_VERSION_NAME', None)} "
                                   f"{env.hadoop_user_home}/hadoop")
            transfer_custom_hadoop_conf(rc, hostname)

    rc.execute_command(create_failsafe_dot_profile)
    rc.execute_command(export_path_with_new_binaries)

    # Configure /etc/hosts file
    rc.execute_command(create_failsafe_hosts_file)
    append_to_hosts_file(rc)

    print(f"[+] {hostname} setup was completed successfully!\n")

    rc.disconnect()
