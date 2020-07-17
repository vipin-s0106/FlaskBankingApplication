import smtplib
from Utils.ConfigReader import getInstance

def send_email(subject, msg,to_address):
    try:
        reader = getInstance()
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(reader.get("GmailConfig", "Email"), reader.get("GmailConfig", "pwd"))
        message = 'Subject: {}\n\n{}'.format(subject, msg)
        server.sendmail(to_address,to_address,message)
        server.quit()
        print("Success: Email sent!")
    except Exception as e:
        print(e.message)
