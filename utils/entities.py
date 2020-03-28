""" Uses the /etc/hosts file to locate the master and the workers """

etc_hosts_file_path = '/etc/hosts'
workers_identifier = 'worker'
master_identifier = 'master'


def get_master():
    """ Grabs the master ip and hostname in a dictionary form of ip:hostname """

    master_dict = {}
    with open(etc_hosts_file_path, "r") as f:
        for line in f:
            try:
                ip, hostname = line.split()
                if master_identifier in hostname:
                    master_dict['ip'] = ip
                    master_dict['hostname'] = hostname
            except ValueError:
                continue

    return master_dict


def get_workers():
    """ Grabs all the workers ips and hostnames in a dictionary form of ip:hostname """

    workers_list = []
    with open(etc_hosts_file_path, "r") as f:
        for line in f:
            try:
                ip, hostname = line.split()
                if workers_identifier in hostname:
                    workers_list.append(
                        {
                            'ip': ip,
                            'hostname': hostname
                        }
                    )
            except ValueError:
                continue

    return workers_list
