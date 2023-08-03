import os

from pyvesync import VeSync

def run(email, password):
  manager = VeSync(email, password)
  manager.login()
  manager.update()
  outlet = next(_ for _ in manager.outlets if _.device_name == 'Garage')
  outlet.display()

if __name__ == "__main__":
  email = os.environ.get('VESYNC_EMAIL')
  password = os.environ.get('VESYNC_PASSWORD')

  run(email, password)
