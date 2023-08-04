import io, os, contextlib
from smtplib import SMTP_SSL
from email.mime.text import MIMEText

from pyvesync import VeSync

DEVICE_NAME = 'Garage'
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 465

def run():
  vesync_email = os.environ.get('VESYNC_EMAIL')
  vesync_password = os.environ.get('VESYNC_PASSWORD')
  sender = os.environ.get('GMAIL_ADDRESS')
  gmail_app_password = os.environ.get('GMAIL_APP_PASSWORD')
  recipients = tuple(_.strip() for _ in os.environ.get('GARAGE_RECIPIENTS').split(','))
  
  manager = VeSync(vesync_email, vesync_password)
  manager.login()
  manager.update()
  outlet = next(_ for _ in manager.outlets if _.device_name == DEVICE_NAME)

  stringio = io.StringIO()
  
  with contextlib.redirect_stdout(stringio):
    outlet.display()
  
  details = stringio.getvalue()
  message = MIMEText(details)
  message['Subject'] = f'{DEVICE_NAME} status'
  message['From'] = sender
  message['To'] = ', '.split(recipients)

  with SMTP_SSL(SMTP_SERVER, SMTP_PORT) as smtp:
    smtp.login(sender, gmail_app_password)
    smtp.sendmail(sender, recipients, message.to_string())
    
if __name__ == "__main__":
  run()
