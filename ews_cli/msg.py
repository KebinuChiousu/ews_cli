""" Store email headers in easy to use class. """

from . import cui


class Header:
    """ Store Email Headers """

    def __init__(self, msg):

        self.sep = ', '
        self.subject = ''
        self.author = ''
        self.sender = ''
        self.to_list = []
        self.cc_list = []
        self.to_email = ''
        self.cc_email = ''
        self.reply_to = ''

        self.to_or_cc_list = []

        self.get_email_headers(msg)

    def get_email_headers(self, msg):
        """ Process exchangelib email msg and extract headers. """

        self.sender = msg.sender.email_address
        self.author = msg.author.email_address
        self.subject = msg.subject

        if msg.to_recipients is not None:

            for eml in msg.to_recipients:
                if eml.email_address is not None:
                    self.to_list.append(eml.email_address)

            self.to_email = self.sep.join(self.to_list)

        if msg.cc_recipients is not None:

            for eml in msg.cc_recipients:
                if eml.email_address is not None:
                    self.cc_list.append(eml.email_address)

            self.cc_email = self.sep.join(self.cc_list)

        self.to_or_cc_list = self.to_list + self.cc_list

        if msg.reply_to is not None:
            self.reply_to = msg.reply_to.email_address

    def show_headers(self):
        """ Show headers for debugging. """
        print('Message Headers', flush=True)
        print(cui.get_entry('Subject : {0}', self.subject), flush=True)
        print(cui.get_entry('Sender  : {0}', self.sender), flush=True)
        print(cui.get_entry('From    : {0}', self.author), flush=True)
        print(cui.get_entry('To      : {0}', self.to_email), flush=True)
        print(cui.get_entry('CC      : {0}', self.cc_email), flush=True)
        print(cui.get_entry('Reply-To: {0}', self.reply_to), flush=True)
