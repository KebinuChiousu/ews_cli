class header:

    def __init__(self, msg):

        self.sep=', '
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

        self.sender = msg.sender.email_address
        self.author = msg.author.email_address
        self.subject = msg.subject

        if msg.to_recipients != None:

            for mb in msg.to_recipients:
                self.to_list.append(mb.email_address)

            self.to_email = self.sep.join(self.to_list)

        if msg.cc_recipients != None:

            for mb in msg.cc_recipients:
                self.cc_list.append(mb.email_address)

        self.cc_email = self.sep.join(self.cc_list)

        self.to_or_cc_list = self.to_list + self.cc_list

        if msg.reply_to != None:
            self.reply_to = msg.reply_to.email_address
