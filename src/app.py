# APP VERSION: 1.0.01
import sys
sys.path.append("./")

import time
from threading import Thread

from src.logs import BaseLogger, Names
from src.controllers.main_controller import MainController
from src.globals import Meta, Accounts

def run():
    logger = BaseLogger.get(Names.ROOT_LOG)
    processes = []
    logger.info("Starting all threads")
    logger.info("Meta: {}".format(Meta.__dict__))
    logger.info("Number of dev accounts: {}".format(Accounts.num_dev_accounts))
    num_threads = Meta.default_num_threads if Meta.test_mode else Accounts.num_dev_accounts
    for index in range(num_threads):
        account =  Accounts.get_test_account(index) if Meta.test_mode else Accounts.get_dev_account(index)
        p = Thread(name="Process {}".format(index), target=MainController.subprocess, args=(index, account,))
        p.start()
        time.sleep(2)
        logger.info("Thread {} started".format(index))
        processes.append(p)
    for p in processes:
        p.join()

    logger.info("All threads are done")

if __name__ == '__main__':
    try:
        run()
    except Exception as e:
        logger = BaseLogger.get(Names.ROOT_LOG)
        logger.exception("Caught exception" + str(e))
