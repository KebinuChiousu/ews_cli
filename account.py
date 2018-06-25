#!/usr/bin/python3

import os
import sys
import argparse
import getpass
from configparser import SafeConfigParser
from collections import defaultdict
import keyring
from datetime import datetime, timedelta
import pytz
from exchangelib import DELEGATE, IMPERSONATION, Account, Credentials, ServiceAccount, \
    EWSDateTime, EWSTimeZone, Configuration, NTLM, GSSAPI, CalendarItem, Message, \
    Mailbox, Attendee, Q, ExtendedProperty, FileAttachment, ItemAttachment, \
    HTMLBody, Build, Version, FolderCollection

# exchangelib usage and info: GitHub repo.
# https://github.com/ecederstrand/exchangelib

keyring_service_name = 'outlook_web_access'

def pause():
    # Wait for user input.
    programPause = input("Press the <ENTER> key to continue...")

def ensure_dir(path):
    # Create directory if it doesn't exist.
    if not os.path.exists(path):
        os.makedirs(path)

def get_config():
    # Create the config dir if it doesn't exist and return path to config.
    home = os.path.expanduser("~")
    cfg = os.path.join(home,".owa")
    ensure_dir(cfg)

    return os.path.join(cfg,"config.ini")

def get_entry(text,value):
    # Substitute {0} in text with value.
    return text.format(value)

def submenu(values,prompt,input_value=False):
    inc=9
    start=0
    stop=inc
    np=0
    pp=0
 
    while True:
        print(prompt)
        print('')
        for i in range(start,len(values)):
            print(i, values[i])
            j=i
            # limit number of entries to stop var.
            if i >= stop:
                # Stop offering next if the last entry is reached.
                if i < (len(values)-1):
                    np=stop+1
                    i=i+1
                    print(np, "Next Page")
                    break
        #if stop > inc, allow prev page.
        if stop > inc:
            pp=i+1
            i=i+1
            print(pp, "Prev Page")
        print('')
        #parse input into number, blank is invalid.
        try:
            sel=int(input("Enter Selection: "))
        except:
            sel = j+1
        # Validate input is valid for current menu.
        if (sel >= start) and (sel <= j):
            if input_value:
                ret = sel
            else:
                ret = values[sel]
            break
        else:
            # Move 1 page ahead
            if sel == np:
                start=start+10
                stop=start+9
                _=os.system("clear")
            # Move 1 page back
            elif sel == pp:
                start=start-10
                stop=start+9
                _=os.system("clear")
            else:
                print("Unknown Option Selected!")
                pause()
                _=os.system("clear")

    return ret

def menu_save():

    _=os.system("clear")

    menu = ['Yes', 'No']
    ret = submenu(menu, "Save Changes?")

    return ret


class outlook_web_access:
    
    def __init__(self, program_args):
        self.server = ''
        self.domain = ''
        self.email = ''
        self.user = ''
        self.password = ''
        self.has_password = False

        ret = self.config_load()

        if ret == 1:
            if program_args.daemon:
                print('ERROR: No Valid Config Found! Exiting...')
                sys.exit(1)
            else:
                self.menu_account()

        if ret == 0:

            self.connect_owa()

            if program_args.daemon:
                print("Not Implemented")
                sys.exit(2)
            else:
                self.menu_main()

    def connect_owa(self):
        
        print("Connecting to OWA...")
        
        # Specify your credentials. Username is usually in WINDOMAIN\username format, where WINDOMAIN is
        # the name of the Windows Domain your username is connected to, but some servers also
        # accept usernames in PrimarySMTPAddress ('myusername@example.com') format (Office365 requires it).
        # UPN format is also supported, if your server expects that.
        self.credentials = Credentials(username='{0}\\{1}'.format(self.domain,self.user), password=self.password)

        # If the server doesn't support autodiscover, or you want to avoid the overhead of autodiscover,
        # use a Configuration object to set the server location instead:
        self.config = Configuration(server=self.server, credentials=self.credentials, auth_type=NTLM)
        self.account = Account(primary_smtp_address=self.email, config=self.config,
                          autodiscover=False, access_type=DELEGATE)

        # If you're connecting to the same account very often, you can cache the autodiscover result for
        # later so you can skip the autodiscover lookup:
        self.ews_url = self.account.protocol.service_endpoint
        self.ews_auth_type = self.account.protocol.auth_type
        self.primary_smtp_address = self.account.primary_smtp_address

        # You can also get the local timezone defined in your operating system
        self.tz = EWSTimeZone.localzone()

    def get_unread_email(self):

        self.account.inbox.total_count
        self.account.inbox.child_folder_count
        self.account.inbox.unread_count
        # Update the counters
        self.account.inbox.refresh()
        # The folder structure is cached after first access. To clear the cache, refresh the root folder
        # account.root.refresh()

        print(self.account.inbox.unread_count)

        pause()

    def menu_main(self):

        while True:

            _=os.system("clear")

            menu = [ "Unread", "Configure Settings", "Exit" ]

            ret = submenu(menu, "OWA CLI - Main Menu")

            if ret == "Configure Settings":
                self.menu_config()
            elif ret == "Unread":
                self.get_unread_email()
            else:
                sys.exit(0)

    def menu_config(self):
        
        while True:

            _=os.system("clear")

            menu = [ "OWA Account Setup", "Main Menu" ]

            ret = submenu(menu, "Configure Settings")

            if ret == "OWA Account Setup":
                self.menu_account()
            else:
                self.menu_main()

    def menu_account(self):

        self.dirty = False

        while True:

            _=os.system("clear")


            menu = [ get_entry('Server: {0}',self.server),
                    get_entry('Domain: {0}',self.domain),
                    get_entry('Email: {0}',self.email),
                    get_entry('User: {0}',self.user),
                    get_entry('Password Set: {0}', self.has_password),
                    'Save Changes',
                    'Config Menu'
                   ]

            ret = submenu(menu, "OWA Account Setup", True)

            if ret == 0:
                self.server = input("Enter Server Name: ")
                self.dirty = True
            elif ret == 1:
                self.domain = input("Enter Domain: ")
                self.dirty = True
            elif ret == 2:
                self.email = input("Enter Email: ")
                self.dirty = True
            elif ret == 3:
                self.user = input("Enter User: ")
                self.dirty = True
                print(self.dirty)
            elif ret == 4:
                self.password = getpass.getpass("Enter Password: ")
                self.has_password = True
            elif ret == 5:
                self.config_save()
                pause
                self.menu_config()
            elif ret == 6:
                if self.dirty:
                    ret = menu_save()
                    if ret == "Yes":
                        self.config_save()
                self.menu_config()



    def config_load(self):

        config = SafeConfigParser()

        cfg = get_config()

        if os.path.isfile(cfg):
            config.read(cfg)

            if not config.has_section('setup'):
                config.add_section('setup')

            self.server = config.get('setup','server')
            self.domain = config.get('setup','domain')
            self.email = config.get('setup','email')
            self.user = config.get('setup','user')

            keyring.get_keyring()
            self.password = keyring.get_password(keyring_service_name, 'password')

            if self.password != '':
                self.has_password = True

            return 0
        else:
            return 1


    def config_save(self):

        config = SafeConfigParser()

        cfg = get_config()

        config.read(cfg)

        if not config.has_section('setup'):
            config.add_section('setup')

        config.set('setup','server',self.server)
        config.set('setup','domain',self.domain)
        config.set('setup','email',self.email)
        config.set('setup','user',self.user)

        # Obtain keyring from OS
        keyring.get_keyring()

        keyring.set_password(keyring_service_name, 'password', self.password)

        with open(cfg, 'w') as f:
            config.write(f)

def main():
    parser = argparse.ArgumentParser(description=('Outlook Web Access CLI Client'))
    parser.add_argument('-d', '--daemon', required=False, action='store_true', help='Run non-interactive')
    
    args = parser.parse_args()
    
    owa = outlook_web_access(args)

if __name__ == "__main__":
    sys.exit(main())
