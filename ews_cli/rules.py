""" Handle Rule Processing """

import os.path
import yaml
from . import util, msg

class RuleFilter:
    """ Class to hold Rule information """

    def __init__(self, name, folder, sender, author, to, reply_to, subject, partial):
        self.name = name
        self.folder = folder
        self.sender = sender
        self.author = author
        self.to = to                  # pylint: disable=C0103
        self.reply_to = reply_to
        self.subject = subject
        self.partial = partial

class FilterCollection:
    """ A collection of Rule Filters """

    def __init__(self):
        self.load_rules()

    def __getitem__(self, index):
        return self.filters[index]

    def __setitem__(self, index, value):
        self.filters[index] = value

    def __delitem__(self, index):
        del self.filters[index]

    def __len__(self):
        return len(self.filters)

    def add_filter(self, name, folder, sender='', author='', to='',                        #pylint: disable=R0913,C0103
                   reply_to='', subject='', partial=False):
        """ Add RuleFilter to Collection """

        flt = RuleFilter(name, folder, sender, author, to, reply_to, subject, partial)
        self.filters.append(flt)

    def load_rules(self):
        """ Load rules from filters.yaml file, if it exists. """
        self.filters = []

        cfg = util.get_config("filters.yaml")

        if os.path.isfile(cfg):

            stream = open(cfg, 'r')

            flt = yaml.load(stream)

            for data in flt:

                name = data['filter_name']
                folder = data['target_folder']

                header = data['header']

                sender = header['sender']
                author = header['from']
                to = header['to']                                                           # pylint: disable=C0103
                reply_to = header['reply_to']
                subject = header['subject']

                if data['match'] == 'full':
                    partial = False
                else:
                    partial = True

                self.add_filter(name, folder, sender, author, to, reply_to, subject, partial)

            try:
                from . import rules_custom as rc
                rc.load_custom(self)
            except ImportError:
                print('No Custom Rules Found... skipping...')

    def save_rules(self):
        """ Save Filter Collection to filters.yaml file. """
        flt = []

        for rule in self.filters:
            data = {}
            header = {}

            data['filter_name'] = rule.name
            data['target_folder'] = rule.folder

            header['sender'] = rule.sender
            header['from'] = rule.author
            header['to'] = rule.to
            header['reply_to'] = rule.reply_to
            header['subject'] = rule.subject

            data['header'] = header

            if rule.partial:
                data['match'] = 'partial'
            else:
                data['match'] = 'full'

            flt.append(data)

        if flt:
            cfg = util.get_config("filters.yaml")
            stream = open(cfg, 'w')
            yaml.dump(flt, stream)

    def process_msg(self, item):
        """ Process email message thru filter collection """

        m_hdr = msg.Header(item)

        for rule in self.filters:
            # Sender:
            if m_hdr.sender != '':
                if rule.sender != '':
                    if rule.partial is False:
                        if rule.sender == m_hdr.sender:
                            return rule.folder
                    else:
                        if rule.sender in m_hdr.sender:
                            return rule.folder
            # From:
            if m_hdr.author != '':
                if rule.author != '':
                    if rule.partial is False:
                        if rule.author == m_hdr.author:
                            return rule.folder
                    else:
                        if rule.author in m_hdr.author:
                            return rule.folder
            # To: or CC:
            if m_hdr.to_email != '' or m_hdr.cc_email != '':
                if rule.to != '':
                    for to_email in m_hdr.to_or_cc_list:
                        to_list = rule.to.split(';')
                        for entry in to_list:
                            if rule.partial is False:
                                if entry == to_email:
                                    return rule.folder
                            else:
                                if entry in to_email:
                                    return rule.folder
            # Reply-To:
            if m_hdr.reply_to != '':
                if rule.reply_to != '':
                    if rule.partial is False:
                        if rule.reply_to == m_hdr.reply_to:
                            return rule.folder
                    else:
                        if rule.reply_to in m_hdr.reply_to:
                            return rule.folder
            # Subject:
            if m_hdr.subject != '':
                if rule.subject != '':
                    if rule.partial is False:
                        if rule.subject == m_hdr.subject:
                            return rule.folder
                    else:
                        if rule.subject in m_hdr.subject:
                            return rule.folder

        # No Match
        return ''
