from orange.mail import MailClient, mail_config, Mail
from orange import R


def conf():
    Pattern = R / r"(?P<user>.*?):(?P<passwd>.*?)@(?P<host>.*?)"
    s = input("Please enter the email server config, Format: user:passwd@host :")
    p = Pattern.fullmatch(s)
    if p:
        print(p.groupdict())
