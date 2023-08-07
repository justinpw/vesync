import io, os, contextlib, sys
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from pyvesync import VeSync

DEVICE_NAME = 'Garage'
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 465
VESYNC_EMAIL = os.environ.get('VESYNC_EMAIL')
VESYNC_PASSWORD = os.environ.get('VESYNC_PASSWORD')
SENDER = os.environ.get('GMAIL_ADDRESS')
GMAIL_APP_PASSWORD = os.environ.get('GMAIL_APP_PASSWORD')
RECIPIENTS = tuple(_.strip() for _ in os.environ.get('GARAGE_RECIPIENTS').split(','))

def get_outlet_details():
  manager = VeSync(VESYNC_EMAIL, VESYNC_PASSWORD)
  manager.login()
  manager.update()
  outlet = next(_ for _ in manager.outlets if _.device_name == DEVICE_NAME)

  stringio = io.StringIO()
  
  with contextlib.redirect_stdout(stringio):
    outlet.display()
  
  details = stringio.getvalue()

  return details

def send_email(subject, text):
  message = MIMEText(details)
  message['Subject'] = f'{DEVICE_NAME} {subject}'
  message['From'] = SENDER
  message['To'] = ', '.join(RECIPIENTS)

  with SMTP_SSL(SMTP_SERVER, SMTP_PORT) as smtp:
    smtp.login(SENDER, GMAIL_APP_PASSWORD)
    smtp.sendmail(SENDER, RECIPIENTS, message.as_string())

def run():
  arg = sys.argv[-1]
  details = get_outlet_details()
  print(details)

  if arg == 'report':
    send_email(f'{DEVICE_NAME} status', details)

  elif arg == 'alarm' and 'off' in details:
    send_email('Garage alarm', details)

if __name__ == "__main__":
  run()
