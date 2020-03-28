from os import system
import env
from utils.checks import java_tar_exists, get_artifacts_full_path, java_folder_exists


def unpack_java(dest='.'):
    if java_tar_exists():
        system(f"tar zxf {get_artifacts_full_path()}/{env.environ.get('JAVA_TAR_FILE_NAME', None)} -C {dest}")
    else:
        print("[-] Unable to unpack java, tar file does not exist under artifacts folder.")
        exit(-1)


def setup_java():
    print("[+] Unpacking Java...")
    home = env.environ.get('HADOOP_USER_HOME', None)
    unpack_java(home)
    if java_folder_exists():
        system(f"rm -rf {env.environ.get('HADOOP_USER_HOME', None)}/java")
    system(f"mv -f {home}/{env.environ.get('JAVA_DIR_NAME', None)} {home}/java")
