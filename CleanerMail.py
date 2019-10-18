import config # Config file

import sys
import smtplib
import schedule
import time

from email.message import EmailMessage
from datetime import date

def main():
    send_CleanerMail()

def get_cleaners(skip, residents):
    weekNumber = date.today().isocalendar()[1] + skip
    if (len(residents) % 2 == 0):
        workNumber = weekNumber * 2 % len(residents*2)
        if (workNumber >= len(residents)):
            workNumber -= len(residents)
            floorCleaner = workNumber
            surfaceCleaner = workNumber + 1
        else:
            floorCleaner = workNumber + 1
            surfaceCleaner = workNumber
        return{'floor': residents[floorCleaner], 'surface': residents[surfaceCleaner]}
    else:
        workNumber = weekNumber * 2 % len(residents)
        floorCleaner = workNumber
        if (workNumber + 1 >= len(residents)):
            surfaceCleaner = 0
        else:
            surfaceCleaner = workNumber + 1
        return{'floor': residents[floorCleaner], 'surface': residents[surfaceCleaner]}

def send_CleanerMail():
    cleaners = get_cleaners(0, config.residents)

    with smtplib.SMTP_SSL('smtp.strato.com', 465) as smtp:
        smtp.login(config.email.get("adress"), config.email.get("password"))

        msg = EmailMessage()
        msg['Subject'] = "Schoonmaakrooster"
        msg['From'] = config.email.get("adress")
        msg['To'] = config.contacts
        msg.set_content(
            'Weeknummer: '+str(date.today().isocalendar()[1])+
            '\nVloer: '+cleaners["floor"]+
            '\nOppervlaktes: '+cleaners["surface"]
            )
        # msg.add_alternative("""\
        # <!DOCTYPE html>
        # <html>
        #     <body>
        #         <h1 style="color:SlateGray;">This is an HTML Email!</h1>
        #     </body>
        # </html>
        #     """, subtype='html')
        smtp.send_message(msg)
        print("Email sent.")


schedule.every(2).minutes.do(send_CleanerMail)
print("--- To exit the program press ctrl+c ---")

while 1:
    try:
        schedule.run_pending()
        time.sleep(1)
    except KeyboardInterrupt:
        print("\n--------------------")
        print("Closing "+sys.argv[0]+"...")
        schedule.clear()
        print("All jobs stopped. System will exit")
        sys.exit(0)
       
