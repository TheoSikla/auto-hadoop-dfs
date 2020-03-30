from os import environ
from utils.entities import get_master

environ["HOSTS_FILE"] = "/etc/hosts"
environ["WORKER_IDENTIFIER"] = "worker"
environ["MASTER_IDENTIFIER"] = "master"

environ["HADOOP_USER_HOME"] = "/home/hadoop"
hadoop_user_home = environ.get('HADOOP_USER_HOME', None)
environ["HADOOP_HOME"] = "/home/hadoop/hadoop"
hadoop_home = environ.get('HADOOP_HOME', None)

environ["HADOOP_INSTALL"] = hadoop_home
environ["HADOOP_MAPRED_HOME"] = hadoop_home
environ["HADOOP_COMMON_HOME"] = hadoop_home
environ["HADOOP_HDFS_HOME"] = hadoop_home
environ["YARN_HOME"] = hadoop_home
environ["HADOOP_COMMON_LIB_NATIVE_DIR"] = f"{hadoop_home}/lib/native"
environ["PATH"] = f"{environ.get('PATH', None)}:{hadoop_home}/sbin:{hadoop_home}/bin"
environ["HADOOP_LOG_DIR"] = f"{hadoop_home}/logs"
environ["MASTER_IP"] = get_master()['ip']

environ["HADOOP_STABLE_VERSION"] = "3.2.1"
environ["HADOOP_STABLE_VERSION_NAME"] = f"hadoop-{environ.get('HADOOP_STABLE_VERSION', None)}"
environ["HADOOP_STABLE_VERSION_NAME_TAR"] = f"{environ.get('HADOOP_STABLE_VERSION_NAME', None)}.tar.gz"
environ["HADOOP_STABLE_VERSION_TAR_URL"] = f"http://apache.otenet.gr/dist/hadoop/common/stable/" \
                                           f"{environ.get('HADOOP_STABLE_VERSION_NAME_TAR', None)}"

environ["HADOOP_CONF_DIR"] = f"{hadoop_home}/etc/hadoop"
environ["HADOOP_CONF_DIR_ETC"] = f"{hadoop_home}/etc"
environ["HADOOP_FAILSAFE_CONF_DIR"] = "hadoop-default-conf"
environ["HADOOP_CUSTOM_CONF_DIR"] = "hadoop-custom-conf"
environ["HADOOP_CUSTOM_GENERATED_CONF_DIR"] = "hadoop-custom-generated-conf"

environ["JAVA_DIR_NAME"] = "jdk1.8.0_231"
environ["JAVA_TAR_FILE_NAME"] = "jdk-8u231-linux-x64.tar.gz"
environ["JAVA_HOME"] = f"{hadoop_user_home}/java"

environ["WORKERS_USERNAME"] = "hadoop"
environ["WORKERS_PASS"] = "hadoop"
environ["SSH_KEY"] = f"{hadoop_user_home}/.ssh/id_rsa"
environ["SSH_KEY_PUB"] = f"{hadoop_user_home}/.ssh/id_rsa.pub"
environ["REMOTE_PATH"] = hadoop_user_home
