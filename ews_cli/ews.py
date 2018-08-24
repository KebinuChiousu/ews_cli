""" Main Program """

import os
import sys
import traceback
from configparser import SafeConfigParser
from datetime import datetime, timedelta
import time
import keyring
from exchangelib import DELEGATE, IMPERSONATION, Account, Credentials, ServiceAccount, EWSDateTime  # pylint: disable=W0611
from exchangelib import EWSTimeZone, Configuration, NTLM, GSSAPI, CalendarItem, Message, Mailbox    # pylint: disable=W0611
from exchangelib import Attendee, Q, ExtendedProperty, FileAttachment, ItemAttachment, HTMLBody     # pylint: disable=W0611
from exchangelib import Build, Version, FolderCollection, Folder                                    # pylint: disable=W0611

from . import gui, util, msg, rules

# exchangelib usage and info: GitHub repo.
# https://github.com/ecederstrand/exchangelib

KEYRING_SERVICE_NAME = 'outlook_web_access'

class ExchangeWebAccess:
    """ Main Application Class """

    def __init__(self, program_args):
        self.unread = 0
        self.account = None
        self.server = ''
        self.domain = ''
        self.email = ''
        self.user = ''
        self.password = ''
        self.has_password = False
        self.filters = rules.FilterCollection()

        ret = self.config_load()

        if ret == 1:
            if program_args.daemon:
                print('ERROR: No Valid Config Found! Exiting...')
                sys.exit(1)
            else:
                gui.menu_account(self)

        if ret == 0:

            if program_args.daemon:
                while True:
                    self.filter_mail()
                    try:
                        print("Sleeping for 5 minutes")
                        for i in range(1, 300, 1):
                            sec = timedelta(seconds=int(i))
                            d = datetime(1, 1, 1) + sec         # pylint: disable=C0103
                            print("%d:%02d" % (d.minute, d.second), end='\r', flush=True)
                            time.sleep(1)
                        print('', end='\n')
                    except KeyboardInterrupt:
                        sys.exit(0)
            else:
                try:
                    self.connect()
                    gui.menu_main(self)
                except Exception as ex:                                  # pylint: disable=W0703
                    if self.account is None:
                        print(ex)
                        util.pause()
                        gui.menu_account(self)
                    else:
                        traceback.print_exc(file=sys.stdout)
                        util.pause()
                        sys.exit(1)

    def connect(self):
        """ Establish connection to EWS Server """

        print("Connecting to EWS...")

        # Specify your credentials. Username is usually in WINDOMAIN\username format,
        # where WINDOMAIN is the name of the Windows Domain your username is connected to, but
        # some servers also accept usernames in PrimarySMTPAddress ('myusername@example.com')
        # format (Office365 requires it). UPN format is also supported, if your server expects that.
        self.credentials = Credentials(username='{0}\\{1}'.format(self.domain, self.user),
                                       password=self.password)

        # If the server doesn't support autodiscover, or you want to avoid the overhead of
        # autodiscover, use a Configuration object to set the server location instead:
        self.config = Configuration(server=self.server,
                                    credentials=self.credentials, auth_type=NTLM)
        self.account = Account(primary_smtp_address=self.email, config=self.config,
                               autodiscover=False, access_type=DELEGATE)

        # If you're connecting to the same account very often, you can cache the autodiscover
        # result for later so you can skip the autodiscover lookup:
        self.ews_url = self.account.protocol.service_endpoint
        self.ews_auth_type = self.account.protocol.auth_type
        self.primary_smtp_address = self.account.primary_smtp_address

        # You can also get the local timezone defined in your operating system
        self.tz = EWSTimeZone.localzone()                                       # pylint: disable=C0103

    def get_unread_count(self):
        """ Get unread email count. """

        if self.account is None:
            self.connect()

        self.account.inbox.total_count                                          # pylint: disable=E1101,W0104
        self.account.inbox.child_folder_count                                   # pylint: disable=E1101,W0104
        self.account.inbox.unread_count                                         # pylint: disable=E1101,W0104
        # Update the counters
        self.account.inbox.refresh()                                            # pylint: disable=E1101
        # The folder structure is cached after first access.
        # To clear the cache, refresh the root folder
        # account.root.refresh()

        self.unread = self.account.inbox.unread_count               # pylint: disable=E1101

    def show_unread_count(self):
        """ Display Unread email count. """
        self.get_unread_count()
        print(util.get_entry("Unread Messages: {0}", self.unread))
        util.pause()

    def show_tree(self):
        """ Show Email Folders """
        if self.account is None:
            self.connect()

        print(self.account.inbox.tree())                            # pylint: disable=E1101
        util.pause()

    def filter_mail(self):
        """ Filter email """
        if self.account is None:
            self.connect()

        self.account.inbox.refresh()                               # pylint: disable=E1101
        total = self.account.inbox.total_count                     # pylint: disable=E1101
        idx = 1
        if total > 0:
            print("Getting mail in INBOX...", flush=True)
            inbox_items = self.account.inbox.all()                 # pylint: disable=E1101
            status = "Process msg {0} of {1}"
            for item in inbox_items:
                print(status.format(idx, total), end='\r', flush=True)
                folder = self.filters.process_msg(item)
                if folder != '':
                    f_inst = util.get_folder(self.account.inbox, folder)
                    if f_inst is not None:
                        item.move(to_folder=f_inst)
                    else:
                        print('\n')
                        print(util.get_entry('Error moving msg into folder: {0}', folder),
                              flush=True)
                idx = idx + 1
            print('\n')

    def show_mail(self):
        """ Display Message Headers for each email """
        if self.account is None:
            self.connect()

        total = self.account.inbox.total_count                    # pylint: disable=E1101
        idx = 1
        if total > 0:
            print("Getting mail in INBOX...", flush=True)
            status = "Displaying msg {0} of {1}"
            for item in self.account.inbox.all():                 # pylint: disable=E1101
                print(status.format(idx, total), flush=True)
                hdr = msg.Header(item)
                self.print_header(hdr)
                util.pause()
                idx = idx + 1
                os.system("clear")

    def print_header(self, headers):
        """ Actually print email headers """

        print(util.get_entry("sender: {0}", headers.sender))
        print(util.get_entry("from: {0}", headers.author))
        print(util.get_entry("to: {0}", headers.to_email))
        print(util.get_entry("cc: {0}", headers.cc_email))
        print(util.get_entry("reply-to: {0}", headers.reply_to))
        print(util.get_entry("subject: {0}", headers.subject))

    def config_load(self):
        """ load config from ini file """

        config = SafeConfigParser()

        cfg = util.get_config()

        if os.path.isfile(cfg):
            config.read(cfg)

            if not config.has_section('setup'):
                config.add_section('setup')

            self.server = config.get('setup', 'server')
            self.domain = config.get('setup', 'domain')
            self.email = config.get('setup', 'email')
            self.user = config.get('setup', 'user')

            keyring.get_keyring()
            self.password = keyring.get_password(KEYRING_SERVICE_NAME, 'password')

            if self.password != '':
                self.has_password = True

            return 0
        else:
            return 1

    def config_save(self):
        """ Save config to ini file """

        config = SafeConfigParser()

        cfg = util.get_config()

        config.read(cfg)

        if not config.has_section('setup'):
            config.add_section('setup')

        config.set('setup', 'server', self.server)
        config.set('setup', 'domain', self.domain)
        config.set('setup', 'email', self.email)
        config.set('setup', 'user', self.user)

        # Obtain keyring from OS
        keyring.get_keyring()

        keyring.set_password(KEYRING_SERVICE_NAME, 'password', self.password)

        with open(cfg, 'w') as cfg_file:
            config.write(cfg_file)
