import os, sys
from . import util, rules

def menu_main(owa):

    while True:

        _=os.system("clear")

        menu = [ "Filter Mail", 
                 "Manage Filter Rules", 
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
            menu_rules(owa)
        elif ret == 2:
            owa.show_unread_count()
        elif ret == 3:
            owa.show_mail()
        elif ret == 4:
            owa.show_tree()
        elif ret == 5:
            menu_config(owa)
        elif ret == 6:
            sys.exit(0)
        else:
            print("Invalid Option!")
            util.pause()

def menu_rules(owa):

    while True:

        _=os.system("clear")

        menu_idx = 1
        menu = {}
        menu[0] = "Add Rule"
        if len(owa.filters) > 0:
            menu[menu_idx] = "Edit Rules"
            menu_idx = menu_idx + 1
            menu[menu_idx] = "Save Rules"
            menu_idx = menu_idx + 1
        menu[menu_idx] = "Main Menu"

        ret = util.submenu(menu, "Filtering Rules")

        if ret == "Add Rule":
            menu_add_filter(owa)
        elif ret == "Edit Rules":
            menu_show_filter(owa)
        elif ret == "Save Rules":
            owa.filters.save_rules()
        elif ret == "Main Menu":
            menu_main(owa)
        else:
            print("Invalid Option!")
            util.pause()

def menu_add_filter(owa):

    rule = rules.RuleFilter('','','','','','','',False)

    while True:

        _=os.system("clear")
        menu = []

        menu = [ util.get_entry('Name    : {0}',rule.name), 
                 util.get_entry('Folder  : {0}',rule.folder), 
                 util.get_entry('Sender  : {0}',rule.sender), 
                 util.get_entry('From    : {0}',rule.author), 
                 util.get_entry('To      : {0}',rule.to)), 
                 util.get_entry('Reply-To: {0}',rule.reply_to),
                 util.get_entry('Subject : {0}',rule.subject),
                 util.get_entry('Match   : {0}',get_match(rule.partial)),
                 "Add Rule",
                 "Prev Menu"
               ]

        ret = util.submenu(menu,"Add Rule",True)

        rule = update_rule(owa, rule,ret)

        if ret == 8:
            owa.filters.add_filter( rule.name,
                                    rule.folder,
                                    rule.sender,
                                    rule.author,
                                    rule.to,
                                    rule.reply_to,
                                    rule.subject,
                                    rule.partial
                                  )
            menu_rules(owa)
        if ret == 9:
            menu_rules(owa)

def get_match(partial):
    if partial == True:
        return 'partial'
    else:
        return 'full'

def menu_match():

    while True:

        menu = [ 'Full', 'Partial' ]

        ret = util.submenu(menu, "Match Type")

        if ret == "Full":
            partial = False
            break
        elif ret == "Partial":
            partial = True
            break
        else:
            print("Invalid Option!")
            util.pause()

    return partial

def select_folder(owa):

    menu = []

    for f in owa.account.inbox.walk():
        menu.append(f.absolute.replace('/root/Top of Information Store/Inbox/',''))

    ret = util.submenu(menu,"Select Folder")

    return ret

def update_rule(owa, rule, ret):

    if ret == 0:
        rule.name = input("Enter Rule Name: ")
    if ret == 1:
        rule.folder = select_folder(owa)
        print(rule.folder)
        util.pause()
    if ret == 2:
        rule.sender = input("Enter Sender: filter ")
    if ret == 3:
        rule.author = input("Enter From: filter ")
    if ret == 4:
        rule.to_list = input("Enter To: or CC: filter (split multiple entries with ;) ")
    if ret == 5:
        rule.reply_to = input("Enter Reply-To: filter ")
    if ret == 6: 
        rule.subject = input("Enter Subject: filter ")
    if ret == 7:
        rule.partial = menu_match()

    return rule

def menu_show_filter(owa):

    idx = 0

    while True:

        _=os.system("clear")
        menu = []

        rule = owa.filters[idx]

        menu = [ util.get_entry('Name    : {0}',rule.name), 
                 util.get_entry('Folder  : {0}',rule.folder), 
                 util.get_entry('Sender  : {0}',rule.sender), 
                 util.get_entry('From    : {0}',rule.author), 
                 util.get_entry('To      : {0}',';'.join(rule.to_list)), 
                 util.get_entry('Reply-To: {0}',rule.reply_to),
                 util.get_entry('Subject : {0}',rule.subject),
                 util.get_entry('Match   : {0}',get_match(rule.partial)),
                 "Update Rule",
                 "Delete Rule"
               ]

        menu_name = "Edit Filter: {0} - {1}".format(idx+1,rule.name)

        ret = util.submenu_nav(menu, menu_name,idx,len(owa.filters)-1, True,True)

        if ret == "Next":
            idx = idx + 1
        if ret == "Prev":
            idx = idx - 1
        if ret == "Go Back":
            menu_rules(owa)

        rule = update_rule(owa, rule,ret)

        if ret == 8:
            owa.filters[idx] = rule
        if ret == 9:
            del owa.filters[idx]

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
        elif ret == 1:
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
        elif ret == 'No':
            return ret
        else:
            print("Invalid Option!")
            util.pause()
