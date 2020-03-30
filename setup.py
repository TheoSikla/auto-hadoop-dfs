from utils.setup_master import master_init
from utils.entities import get_workers
from utils.setup_worker import worker_init


master_init()
for worker in get_workers():
    worker_init(worker['hostname'])


