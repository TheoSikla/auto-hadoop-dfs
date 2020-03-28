import env
import re
from os import path, makedirs, system, listdir
from utils.checks import get_artifacts_full_path

env_var_regex = r'{ \$[A-Z_]* }|{\$[A-Z_]*}'  # :)


def map_env_variables_to_be_replaced():
    """ Maps all the env variables to be replaced with actual values in custom xml configuration files """

    # mapped env variables inside xml files to be replaced during custom xml config generation
    magical_map = {}
    hadoop_custom_conf_dir_full_path = f"{get_artifacts_full_path()}/{env.environ.get('HADOOP_CUSTOM_CONF_DIR', None)}"
    for file in listdir(hadoop_custom_conf_dir_full_path):
        full_file_path = f"{hadoop_custom_conf_dir_full_path}/{file}"
        if not path.isdir(full_file_path):
            with open(full_file_path) as f:
                file = f.read()
                # Env variables found in opened xml file (List)
                env_vars = re.findall(re.compile(env_var_regex), file)

                for env_var in env_vars:
                    filtered_env_var = re.sub('[{ $}]', '', env_var)
                    retrieved_env_var = env.environ.get(filtered_env_var, None)
                    if retrieved_env_var:
                        magical_map[env_var] = retrieved_env_var
                    else:
                        print(f"[-] Env {filtered_env_var} was found in a configuration file but it is not set up in "
                              f"the env file.")
                        exit(-1)
    return magical_map


def generate():
    """ Generates the appropriate custom configuration """

    hadoop_custom_conf_dir_full_path = f"{get_artifacts_full_path()}/{env.environ.get('HADOOP_CUSTOM_CONF_DIR', None)}"
    hadoop_custom_generated_conf_dir_name = f"{get_artifacts_full_path()}/" \
                                            f"{env.environ.get('HADOOP_CUSTOM_GENERATED_CONF_DIR', None)}"
    if not path.exists(hadoop_custom_generated_conf_dir_name):
        makedirs(hadoop_custom_generated_conf_dir_name)

    # All the env variables found in files configuration under artifacts/hadoop-custom-conf
    mapped_env_vars = map_env_variables_to_be_replaced()

    for file in listdir(hadoop_custom_conf_dir_full_path):
        full_file_path = f"{hadoop_custom_conf_dir_full_path}/{file}"
        if not path.isdir(full_file_path):
            with open(full_file_path) as f:
                custom_file = f.read()
                for env_in_xml, mapped_env in mapped_env_vars.items():
                    if env_in_xml in custom_file:
                        custom_file = custom_file.replace(env_in_xml, mapped_env)
                with open(f"{hadoop_custom_generated_conf_dir_name}/{file}", "w") as w:
                    w.write(custom_file)

    # Copies all the generated configuration in the user's hadoop configuration directory
    system(f"cp -r {hadoop_custom_generated_conf_dir_name}/* {env.environ.get('HADOOP_CONF_DIR', None)}")
