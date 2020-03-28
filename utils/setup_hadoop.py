import env
from os import system, path, makedirs
from utils.checks import hadoop_tar_exists, get_artifacts_full_path, hadoop_folder_exists
from utils.which import which


def unpack_hadoop(dest='.'):
    system(f"tar -xzf {get_artifacts_full_path()}/{env.environ.get('HADOOP_STABLE_VERSION_NAME_TAR', None)} "
           f"-C {dest}")


def get_default_hadoop_settings_files():
    print(f"[+] Copying default hadoop settings in failsafe directory "
          f"artifacts/{env.environ.get('HADOOP_FAILSAFE_CONF_DIR', 'default-conf')}")

    conf_dir_name = f"{get_artifacts_full_path()}/{env.environ.get('HADOOP_FAILSAFE_CONF_DIR', None)}"
    if not path.exists(conf_dir_name):
        makedirs(conf_dir_name)
    system(f"cp -r {env.environ.get('HADOOP_CONF_DIR', None)}/* {conf_dir_name}")


def setup_hadoop():
    if not hadoop_tar_exists():
        try:
            print("[+] Downloading hadoop...")
            if which('curl'):
                system(f"curl -o {get_artifacts_full_path()}/{env.environ.get('HADOOP_STABLE_VERSION_NAME_TAR', None)} "
                       f"{env.environ.get('HADOOP_STABLE_VERSION_TAR_URL', None)}")
            elif which('wget'):
                system(f"wget -P {get_artifacts_full_path()} {env.environ.get('HADOOP_STABLE_VERSION_TAR_URL', None)}")
            else:
                print("Please install to your system the tools curl or wget in order to download hadoop.")
                raise Exception

            if hadoop_tar_exists():
                print("[+] Unpacking hadoop...")
                home = env.environ.get('HADOOP_USER_HOME', None)
                unpack_hadoop(home)
                if hadoop_folder_exists():
                    system(f"rm -rf {env.environ.get('HADOOP_USER_HOME', None)}/hadoop")
                system(f"mv -f {home}/{env.environ.get('HADOOP_STABLE_VERSION_NAME', None)} {home}/hadoop")
                get_default_hadoop_settings_files()
            else:
                raise Exception
        except Exception:
            print("[-] Unable to download hadoop 3.2.1")
            exit(-1)
    else:
        print("[!] Hadoop is already downloaded.")
        print("[+] Unpacking hadoop...")
        home = env.environ.get('HADOOP_USER_HOME', None)
        unpack_hadoop(home)
        if hadoop_folder_exists():
            system(f"rm -rf {env.environ.get('HADOOP_USER_HOME', None)}/hadoop")
        system(f"mv -f {home}/{env.environ.get('HADOOP_STABLE_VERSION_NAME', None)} {home}/hadoop")
        get_default_hadoop_settings_files()
