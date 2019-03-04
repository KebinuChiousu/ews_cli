""" Menu Display Code """

import os
import sys
import getpass
from . import util, cui, rules

EXCHANGE_ROOT = '/root/Top of Information Store/Inbox/'


def menu_main(owa):
    """ Main Menu """

    while True:

        _ = os.system("clear")

        menu = ["Filter Mail",
                "Manage Filter Rules",
                "Show Unread Count",
                "Show Mail",
                "Show Exchange Tree",
                "Configure Settings",
                "Exit"]

        ret = cui.submenu(menu, "EWS CLI - Main Menu", True)

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
    """ Manage Filter Rules """

    while True:

        _ = os.system("clear")

        menu_idx = 1
        menu = {}
        menu[0] = "Add Rule"
        if owa.filters:
            menu[menu_idx] = "Edit Rules"
            menu_idx = menu_idx + 1
            menu[menu_idx] = "Save Rules"
            menu_idx = menu_idx + 1
        menu[menu_idx] = "Main Menu"

        ret = cui.submenu(menu, "Filtering Rules")

        if ret == "Add Rule":
            menu_add_filter(owa)
        elif ret == "Edit Rules":
            menu_edit_filter(owa)
        elif ret == "Save Rules":
            owa.filters.save_rules()
        elif ret == "Main Menu":
            menu_main(owa)
        else:
            print("Invalid Option!")
            util.pause()


def menu_match():
    """ Email Filter Match Type """

    while True:

        menu = ['Full', 'Partial']

        ret = cui.submenu(menu, "Match Type")

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
    """ Choose Email Folder to move filtered message into. """

    menu = []
    print("Getting List of Folders...", flush=True)
    folders = owa.account.inbox.walk()

    for fldr in folders:
        menu.append(fldr.absolute.replace(EXCHANGE_ROOT, ''))

    ret = cui.submenu(menu, "Select Folder")

    return ret


def get_rule_input(owa, rule, ret):
    """ Handle input to create filter rule. """

    if ret == 0:
        rule.name = input("Enter Rule Name: ")
    if ret == 1:
        rule.folder = select_folder(owa)
    if ret == 2:
        rule.sender = input("Enter Sender: filter ")
    if ret == 3:
        rule.author = input("Enter From: filter ")
    if ret == 4:
        prompt = "Enter To: or CC: filter (split multiple entries with ;) "
        rule.to = input(prompt)
    if ret == 5:
        rule.reply_to = input("Enter Reply-To: filter ")
    if ret == 6:
        rule.subject = input("Enter Subject: filter ")
    if ret == 7:
        rule.partial = menu_match()

    return rule


def get_match(partial):
    """ Return str value for partial bool. """

    if partial is True:
        return 'partial'
    else:
        return 'full'


def menu_add_filter(owa):
    """ Add Filter Menu """

    rule = rules.RuleFilter('', '', '', '', '', '', '', False)

    while True:

        _ = os.system("clear")
        menu = []

        menu = [cui.get_entry('Name    : {0}', rule.name),
                cui.get_entry('Folder  : {0}', rule.folder),
                cui.get_entry('Sender  : {0}', rule.sender),
                cui.get_entry('From    : {0}', rule.author),
                cui.get_entry('To      : {0}', rule.to),
                cui.get_entry('Reply-To: {0}', rule.reply_to),
                cui.get_entry('Subject : {0}', rule.subject),
                cui.get_entry('Match   : {0}', get_match(rule.partial)),
                "Add Rule",
                "Prev Menu"]

        ret = cui.submenu(menu, "Add Rule", True)

        rule = get_rule_input(owa, rule, ret)

        if ret == 8:
            owa.filters.add_filter(rule.name,
                                   rule.folder,
                                   rule.sender,
                                   rule.author,
                                   rule.to,
                                   rule.reply_to,
                                   rule.subject,
                                   rule.partial)
            menu_rules(owa)
        if ret == 9:
            menu_rules(owa)


def menu_edit_filter(owa):
    """ Edit Filter Menu """

    idx = 0

    while True:

        _ = os.system("clear")
        menu = []

        rule = owa.filters[idx]

        menu = [cui.get_entry('Name    : {0}', rule.name),
                cui.get_entry('Folder  : {0}', rule.folder),
                cui.get_entry('Sender  : {0}', rule.sender),
                cui.get_entry('From    : {0}', rule.author),
                cui.get_entry('To      : {0}', rule.to),
                cui.get_entry('Reply-To: {0}', rule.reply_to),
                cui.get_entry('Subject : {0}', rule.subject),
                cui.get_entry('Match   : {0}', get_match(rule.partial)),
                "Update Rule",
                "Delete Rule"]

        menu_name = "Edit Filter: {0} - {1}".format(idx + 1, rule.name)

        ret = cui.submenu_nav(menu, menu_name, idx,
                              len(owa.filters) - 1, True, True)

        if ret == "Next":
            idx = idx + 1
        if ret == "Prev":
            idx = idx - 1
        if ret == "Go Back":
            menu_rules(owa)

        rule = get_rule_input(owa, rule, ret)

        if ret == 8:
            owa.filters[idx] = rule
        if ret == 9:
            del owa.filters[idx]


def menu_account(owa):
    """ EWS Account Config Menu """

    owa.dirty = False

    while True:

        _ = os.system("clear")

        menu = [cui.get_entry('Server: {0}', owa.server),
                cui.get_entry('Domain: {0}', owa.domain),
                cui.get_entry('Email: {0}', owa.email),
                cui.get_entry('User: {0}', owa.user),
                cui.get_entry('Password Set: {0}', owa.has_password),
                'Save Changes',
                'Config Menu']

        ret = cui.submenu(menu, "EWS Account Setup", True)

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
            pass1 = getpass.getpass("Enter Password: ")
            pass2 = getpass.getpass("Verify Password: ")
            if pass1 == pass2:
                owa.password = pass1
                owa.has_password = True
            else:
                owa.password = ""
                owa.has_password = False
        elif ret == 5:
            owa.config_save()
            cui.pause()
            menu_config(owa)
        elif ret == 6:
            if owa.dirty:
                ret = cui.menu_save()
                if ret == "Yes":
                    owa.config_save()
            menu_config(owa)
        else:
            print("Invalid Option!")
            util.pause()


def menu_config(owa):
    """ Config Menu """

    while True:

        _ = os.system("clear")

        menu = ["EWS Account Setup", "Main Menu"]

        ret = cui.submenu(menu, "Configure Settings", True)

        if ret == 0:
            menu_account(owa)
        elif ret == 1:
            menu_main(owa)
        else:
            print("Invalid Option!")
            util.pause()
