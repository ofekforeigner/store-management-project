from flask_mail import Mail, Message
from Xml import Xml
import itertools

class Mail_Class:
    def __init__(self, db, app, header, body, mail_address):
        self.db = db
        self.mycursor = self.db.cursor()
        self.app = app
        self.xml = Xml()
        self.mail = Mail(self.app)
        self.mail_address = mail_address
        self.header = header
        self.body = body

    # SEND AN EMAIL
    def send_mail(self):
        msg = Message(self.header, sender=self.xml.email_get(),
                      recipients=[self.mail_address])  # CONTAIN ALL MAIL DETAILS
        msg.body = self.body
        self.mail.send(msg)

    def get_names_for_mail(self):
        self.mycursor.execute(
            "SELECT fullname from contacts where status = 1")
        c_names = self.mycursor.fetchall()
        names_list = list(itertools.chain(*c_names))
        return names_list

    def read_email_encrypted_password(password):
        encrypt = ""
        for ch in password[::2]:
            encrypt += ch
        return encrypt