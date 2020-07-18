#coding:utf-8
import smtplib
from email.mime.text import MIMEText
from email.header import Header

class Mail:
    def __init__(self):
        # 第三方 SMTP 服务

        self.mail_host="smtp.qq.com"       #设置服务器:这个是qq邮箱服务器，直接复制就可以
        self.mail_pass="uheaehxkxeqibedb"           #刚才我们获取的授权码
        self.sender = '909656765@qq.com'      #你的邮箱地址 
        self.receivers = ['909656765@qq.com']  # 收件人的邮箱地址，可设置为你的QQ邮箱或者其他邮箱，可多个

    def send(self):

        content = '你好，我是join'
        message = MIMEText(content, 'plain', 'utf-8')

        message['From'] = Header("AAAAAA", 'utf-8')  
        message['To'] =  Header("BBBBBB", 'utf-8')
        
        subject = 'thumb1'  #发送的主题，可自由填写
        message['Subject'] = Header(subject, 'utf-8') 
        try:
            smtpObj = smtplib.SMTP_SSL(self.mail_host, 465) 
            print('ready to login...')
            smtpObj.login(self.sender,self.mail_pass) 
            print('login ok, send mail...')
            smtpObj.sendmail(self.sender, self.receivers, message.as_string())
            smtpObj.quit()
            print('邮件发送成功')
        except smtplib.SMTPException as e:
            print('邮件发送失败')



if  __name__ == '__main__':
    mail = Mail()
    mail.send()