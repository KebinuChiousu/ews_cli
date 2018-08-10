import os, sys
from . import util

def menu_main(owa):

    while True:

        _=os.system("clear")

        menu = [ "Filter Mail", 
                 "Show Unread Count", 
                 "Show Mail", 
                 "Show Exchange Tree", 
                 "Configure Settings", 
                 "Exit" 
               ]

        ret = util.submenu(menu, "EWS CLI - Main Menu", True)

        if ret == 0:
            owa.filter_mail()
            util.pause()
        elif ret == 1:
            owa.show_unread_count()
        elif ret == 2:
            owa.show_mail()
        elif ret == 3:
            owa.show_tree()
        elif ret == 4:
            menu_config(owa)
        elif ret == 5:
            sys.exit(0)
        else:
            print("Invalid Option!")
            util.pause()

def menu_account(owa):

    owa.dirty = False

    while True:

        _=os.system("clear")

        menu = [ util.get_entry('Server: {0}',owa.server),
                 util.get_entry('Domain: {0}',owa.domain),
                 util.get_entry('Email: {0}',owa.email),
                 util.get_entry('User: {0}',owa.user),
                 util.get_entry('Password Set: {0}', owa.has_password),
                 'Save Changes',
                 'Config Menu'
                ]

        ret = util.submenu(menu, "EWS Account Setup", True)

        if ret == 0:
            owa.server = input("Enter Server Name: ")
            owa.dirty = True
        elif ret == 1:
            owa.domain = input("Enter Domain: ")
            owa.dirty = True
        elif ret == 2:
            owa.email = input("Enter Email: ")
            owa.dirty = True
        elif ret == 3:
            owa.user = input("Enter User: ")
            owa.dirty = True
        elif ret == 4:
            owa.password = getpass.getpass("Enter Password: ")
            owa.has_password = True
        elif ret == 5:
            owa.config_save()
            util.pause()
            menu_config(owa)
        elif ret == 6:
            if owa.dirty:
                ret = menu_save()
                if ret == "Yes":
                    owa.config_save()
            menu_config(owa)
        else:
            print("Invalid Option!")
            util.pause()

def menu_config(owa):

    while True:

        _=os.system("clear")

        menu = [ "EWS Account Setup", "Main Menu" ]

        ret = util.submenu(menu, "Configure Settings", True)

        if ret == 0:
            menu_account(owa)
        if ret == 1:
            menu_main(owa)
        else:
            print("Invalid Option!")
            util.pause()

def menu_save():

    while True:

        _=os.system("clear")

        menu = ['Yes', 'No']
        ret = util.submenu(menu, "Save Changes?")

        if ret == 'Yes':
            return ret
        if ret == 'No':
            return ret
        else:
            print("Invalid Option!")
            util.pause()
