import yaml
from collections import defaultdict
from . import util, msg

class RuleFilter:

    def __init__(self, name, folder, sender, author, to, reply_to, subject, partial):
        self.name = name
        self.folder = folder
        self.sender = sender
        self.author = author
        self.to = to
        self.reply_to = reply_to
        self.subject = subject
        self.partial = partial

class FilterCollection:

    def __init__(self):
        self.load_rules()

    def __getitem__(self,index):
        return self.filters[index]

    def __setitem__(self,index,value):
        self.filters[index] = value

    def __delitem__(self,index):
        del self.filters[index]

    def __len__(self):
        return len(self.filters)

    def add_filter( self, name, folder, sender='', author='', to='', reply_to='', subject='', partial=False):
        f = RuleFilter(name,folder,sender,author,to,reply_to,subject,partial)
        self.filters.append(f)

    def load_rules(self):
        self.filters = []

        cfg = util.get_config("filters.yaml")
        stream = open(cfg, 'r')

        flt = yaml.load(stream)

        for data in flt:

            name = data['filter_name']
            folder = data['target_folder']

            header = data['header']

            sender = header['sender']
            author = header['from']
            to = header['to']
            reply_to = header['reply_to']
            subject = header['subject']

            if data['match'] == 'full':
                partial = False
            else:
                partial = True

            self.add_filter(name,folder,sender,author,to,reply_to,subject,partial)

        try:
            from . import rules_custom as rc
            rc.load_custom(self)
        except ImportError:
            print('No Custom Rules Found... skipping...')

    def save_rules(self):
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

        if len(flt) > 0:
            cfg = util.get_config("filters.yaml")
            stream = open(cfg, 'w')
            yaml.dump(flt, stream)

    def process_msg(self, item):

        m = msg.header(item)

        for rule in self.filters:
            # Sender:
            if m.sender != '':
                if rule.sender != '':
                    if rule.partial == False:
                        if rule.sender == m.sender:
                            return rule.folder
                    else:
                        if rule.sender in m.sender:
                            return rule.folder
            # From:
            if m.author != '':
                if rule.author != '':
                    if rule.partial == False:
                        if rule.author == m.author:
                            return rule.folder
                    else:
                        if rule.author in m.author:
                            return rule.folder
            # To: or CC:
            if m.to_email != '':
                if rule.to != '':
                    for to_email in m.to_or_cc_list:
                        to_list = rule.to.split(';')
                        for entry in to_list:
                            if rule.partial == False:
                                if entry == to_email:
                                    return rule.folder
                            else:
                                if entry in to_email:
                                    return rule.folder
            # Reply-To:
            if m.reply_to != '':
                if rule.reply_to != '':
                    if rule.partial == False:
                        if rule.reply_to == m.reply_to:
                            return rule.folder
                    else:
                        if rule.reply_to in m.reply_to:
                            return rule.folder
            # Subject:
            if m.subject != '':
                if rule.subject != '':
                    if rule.partial == False:
                        if rule.subject == m.subject:
                            return rule.folder
                    else:
                        if rule.subject in m.subject:
                            return rule.folder

        # No Match
        return ''
