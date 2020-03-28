import env
from os import path

artifacts_dir_name = 'artifacts'
hadoop_tar_name = 'hadoop-3.2.1.tar.gz'
java = 'jdk-8u231-linux-x64.tar.gz'


def get_artifacts_local_path():
    return f'{artifacts_dir_name}'


def get_artifacts_full_path():
    return path.abspath(get_artifacts_local_path())


def hadoop_tar_exists():
    if path.isfile(f'{get_artifacts_full_path()}/{hadoop_tar_name}'):
        return True
    return False


def hadoop_folder_exists():
    java_path = f"{env.environ.get('HADOOP_USER_HOME', None)}/hadoop"
    return path.exists(java_path)


def java_tar_exists():
    if path.isfile(f'{get_artifacts_full_path()}/{java}'):
        return True
    return False


def java_folder_exists():
    java_path = f"{env.environ.get('HADOOP_USER_HOME', None)}/java"
    return path.exists(java_path)
