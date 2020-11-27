# -*- coding: utf-8 -*-
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email import encoders
from pypinyin import pinyin, Style
import re
from .config import mail_host, mail_user, mail_pass, sender, book_path

pwd_path = os.path.abspath(os.path.dirname(__file__))


def __get_pinyin__(filename):
    name_pinyins = pinyin(filename, style=Style.NORMAL)
    name_pinyin = ''
    for np in name_pinyins:
        name_pinyin += ''.join(np) + '_'
    name_pinyin = name_pinyin[:-1]
    name_pinyin = re.sub('[^a-zA-Z0-9_.]', '', name_pinyin)
    return name_pinyin


def push_book(receivers, filename, bookid):
    send_email(receivers, filename, filename, filename, bookid)


def send_email(receivers, subject, content, filename=None, bookid=None):
    message = MIMEMultipart()
    content_part = MIMEText(content, 'plain', 'utf-8')  # 内容, 格式, 编码
    message.attach(content_part)
    if filename and bookid:
        with open(os.path.join(pwd_path, book_path, bookid + '_' + filename), 'rb') as f:
            attachment_part = MIMEApplication(f.read())
            encoders.encode_base64(attachment_part)
            attachment_part.add_header('Content-Disposition', 'attachment; filename=' + __get_pinyin__(filename))
            message.attach(attachment_part)

    message['From'] = "{}".format(sender)
    message['To'] = ",".join(receivers)
    message['Subject'] = subject
    try:
        smtpObj = smtplib.SMTP_SSL(mail_host, 465)  # 启用SSL发信, 端口一般是465
        smtpObj.login(mail_user, mail_pass)  # 登录验证
        smtpObj.sendmail(sender, receivers, message.as_string())  # 发送
        smtpObj.quit()
        print("mail has been send successfully.")
    except smtplib.SMTPException as e:
        print(e)
