import os
from datetime import datetime, timedelta
import time

EXCHANGE_ROOT = '/root/Top of Information Store/Inbox/'


def get_config(config="config.ini"):
    # Create the config dir if it doesn't exist and return path to config.
    home = os.path.expanduser("~")
    folder = os.path.join(home, ".owa")
    ensure_dir(folder)

    return os.path.join(folder, config)


def ensure_dir(path):
    # Create directory if it doesn't exist.
    if not os.path.exists(path):
        os.makedirs(path)


def get_folder(folder, target):
    ret = None
    f = None
    f2 = ''

    if folder.absolute.replace(EXCHANGE_ROOT, '') == target:
        return folder

    for f in folder.children:
        f2 = f.absolute.replace(EXCHANGE_ROOT, '')
        if f2 in target:
            break

    if f2 == target:
        ret = f
    else:
        if f is None:
            return None
        else:
            ret = get_folder(f, target)

    return ret


def sleep(seconds):
    sec = timedelta(seconds=int(seconds))
    d = datetime(1, 1, 1) + sec         # pylint: disable=C0103
    print("Sleeping for %02d:%02d" % (d.minute, d.second), flush=True)
    for i in range(seconds, 0, -1):
        sec = timedelta(seconds=int(i))
        d = datetime(1, 1, 1) + sec         # pylint: disable=C0103
        print("%02d:%02d" % (d.minute, d.second), end='\r', flush=True)
        time.sleep(1)
    print('', end='\n')
