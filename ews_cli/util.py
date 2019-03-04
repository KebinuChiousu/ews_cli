import os
from datetime import datetime, timedelta
import time
from exchangelib import errors, Folder
from . import cui

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


def create_folder(account, folder):
    folders = folder.split("/")
    account.root.refresh()
    f_inst = get_folder(account.inbox, folder)
    if f_inst is None:
        check = get_folder(account.inbox, folders[0])
        if check is None:
            f = Folder(parent=account.inbox, name=folders[0])
            f.save()
            f = None

    parent = folders[0]
    folders.pop(0)
    create_subfolder(account, parent, "/".join(folders))


def create_subfolder(account, parent, folder):
    folders = folder.split("/")

    # Any subfolders left to process?
    if folders[0] != "":

        # Refresh Inbox
        account.root.refresh()

        # Check for Folder
        check = get_folder(account.inbox, parent + "/" + folders[0])
        p_folder = get_folder(account.inbox, parent)

        if check is None:
            # Folder doesn't exist
            try:
                f = Folder(parent=p_folder, name=folders[0])
                f.save()
                f = None
            except errors.ErrorFolderExists:
                print("Tried to create folder: " + parent + "/" + folders[0])
                print("It already exists!")
                cui.pause()

        # Process Next SubFolder
        parent = parent + "/" + folders[0]
        folders.pop(0)
        create_subfolder(account, parent, "/".join(folders))


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
