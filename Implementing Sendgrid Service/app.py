import smtplib
import sendgrid
import os
from sendgrid.helpers.mail import Mail,Email, To,Content
SUBJECT = "Congratulations for the offers"
s = smtplib.SMTP('smtp.gmail.com', 587)
def sendmail(TEXT,email):
    print("Glad to hear back from you")
    s = smtplib.SMTP('smtp.gmail.com',587)
    s.starttls()
    s.login("sanjana19097@smartinternz.com","password")
    message = 'Subject : {}\n\n{}'.format(SUBJECT,TEXT)
    s.sendmail("sanjana19097@smartinternz.com",email,message)
    s.quit()

def sendgridmail(user,TEXT):
    sg = sendgrid.SendGridAPIClient('SG.nouVVMwQTSYtih73r1TxQ.3H0dhuefhdwwf2r7fgb7qvtjyZ_nhPbki3zeZnc')
    from_email = Email("ranjani@gmail.com")
    to_email = To(user)
    subject = "Join with Us"
    content = Content("text/plain",TEXT)
    mail = Mail(from_email, to_email, subject, content)
    mail_rr = mail.get()
    response = sg.client.mail.send.post(request_body=mail_json)
    print(response.status_code)
    print(response.header)