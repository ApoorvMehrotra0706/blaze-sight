import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

#Sender email
email = "sjsuprojectalert@gmail.com"
password = "Pranjay@014611922"

#reciever number and email address
#sms_gateway = '5855246544@tmomail.net'  #tmomail.net is used for tmobile numbers
#receiver_email = "pranjay.sagar@sjsu.edu"

# Using smtp server we use is gmail smtp server ( the port comes by default with the gmail server)
smtp = "smtp.gmail.com" 
port = 587
#enable_starttls_auto= True
#authentication:'plain'
#what we want the body and subject contents to be
subject_content="ALERT 911\n"
body_content_1="Fire detected, we  need assistance!!"



#login


# To send sms text message
def send_msg(modileNo,percentage):
    server = smtplib.SMTP(smtp,port)
    server.starttls()
    server.login(email,password)

    sms_gateway = str(modileNo) + '@tmomail.net'
    textmsg = MIMEMultipart()
    textmsg['From'] = "BLAZE SIGHT"
    textmsg['To'] = sms_gateway
    textmsg['Subject'] = subject_content
    body = body_content_1
    textmsg.attach(MIMEText(body, 'plain'))
    sms = textmsg.as_string()
    server.sendmail(email,sms_gateway,sms)
    server.quit()

# Send Email
def send_email(receiver_email,percentage):
    #starts pythons email server
    server = smtplib.SMTP(smtp,port)
    server.starttls()
    server.login(email,password)
    emailMessage = MIMEMultipart()
    emailMessage['From'] = "BLAZE SIGHT"
    emailMessage['To'] = receiver_email
    emailMessage['Subject'] = subject_content
    body = body_content_1
    emailMessage.attach(MIMEText(body, 'plain'))
    mailAlert = emailMessage.as_string()
    server.sendmail(email,receiver_email,mailAlert)
    server.quit()
