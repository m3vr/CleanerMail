#! /usr/bin/python3

import config  # Config file
import cleanerschedule
import smtplib
import sys
import argparse
from email.message import EmailMessage
from datetime import date


def main():
    parser = argparse.ArgumentParser(description='This program sends the weekly cleaning schedule to contacts.')
    parser.add_argument("subject", help="the subject of the email to be send",
                    type=str)
    parser.add_argument("-a", "--send-all", help="sends email to all contacts, otherwise only to the cleaners",
                    action="store_true")
    parser.add_argument("-s", "--single-email", help="send only an email to this adress",
                    type=str)
    parser.add_argument("-w", "--skip-weeks", help="number of weeks to skip",
                    type=int, default=0)
    parser.add_argument("-d", "--debug", help="will not actually send emails",
                    action="store_true")
    parser.add_argument("-v", "--verbose", help="increase output verbosity",
                    action="store_true")

    args = parser.parse_args()
    
    # PRINT STATUS MESSAGES
    print()
    if args.verbose: print("--verbose mode enabled--\n")
    if args.debug: print("--debug mode enabled--\n")
    if args.verbose: print(f"INFO: Email subject: {args.subject}")
    if args.verbose: print("INFO: Message all contacts" if args.send_all else "INFO: Message cleaners only")

    if len(config.contacts) % len(config.jobs) == 0:
        print("ERROR: The combination between the amount of residents and jobs is not yet supported!")
        sys.exit(1)

    send_CleanerMail(args)

def send_CleanerMail(args):
    cleaners = cleanerschedule.get_cleaners(sorted(list(config.contacts.keys())), config.jobs, args)

    if args.single_email:
        sendTo = {"<NAME>": args.single_email}
    elif args.send_all:
        sendTo = config.contacts
    else:
        keys = [cleaners["floor"], cleaners["surface"]]
        sendTo = {x: config.contacts[x] for x in keys}

    with smtplib.SMTP_SSL('smtp.strato.com', 465) as smtp:
        smtp.login(config.email.get("adress"), config.email.get("password"))
        for name, email in sendTo.items():
            msg = EmailMessage()
            msg['Subject'] = args.subject
            msg['From'] = str("Club Huyzch <"+config.email.get("adress")+">")
            msg['To'] = "m.evers95@gmail.com"
            # msg.set_content(
            #     'Weeknummer: '+str(date.today().isocalendar()[1]) +
            #     '\nVloer: '+cleaners["floor"] +
            #     '\nOppervlaktes: '+cleaners["surface"]
            # )
            msg.add_alternative("""\
<!DOCTYPE html
    PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">

<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <title>Club Huyzch Schoonmaakrooster</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
</head>

<body style="margin: 0; padding: 0; text-align: center;">
    <table border="0" cellpadding="0" cellspacing="0" width="100%">
        <tr>
            <td style="padding: 10px 0 30px 0;">
                <table align="center" border="0" cellpadding="0" cellspacing="0" width=825
                    style="border: 1px solid #cccccc; border-collapse: collapse;">
                    <tr>
                        <td align="center" bgcolor="#153643"
                            style="padding: 30px 0 30px 0; color: #153643; font-size: 28px; font-weight: bold; font-family: Arial, sans-serif;">
                            <img src="http://www.clubhuyzch.nl/images/logo_white-2x.png" alt="Club Huyzch logo"
                                width="200" style="display: block;" />
                        </td>
                    </tr>
                    <tr>
                        <td bgcolor="#ffffff" style="padding: 40px 30px 30px 30px;">
                            <table border="0" cellpadding="0" cellspacing="0" width="100%">
                                <tr>
                                    <td
                                        style="color: #000000; font-family: Arial, sans-serif;text-align: center; font-size: 30px;">
                                        <b>Schoonmaakrooster</b>
                                    </td>
                                </tr>
                                <tr>
                                    <td
                                        style="padding: 20px 0 30px 0; color: #153643; font-family: Arial, sans-serif; font-size: 16px; line-height: 20px;">
                                        Halloooo """+str(name)+"""! Er mag weer lekker geschrobt en
                                        geboend worden. Hieronder staan de schoonmakers voor week
                                        """+str(date.today().isocalendar()[1])+""".
                                    </td>
                                </tr>
                                <tr>
                                    <td>
                                        <table border="0" cellpadding="0" cellspacing="0" width="100%">
                                            <tr>

                                                <td width="260" valign="top">
                                                    <table border="0" cellpadding="0" cellspacing="0" width="100%">
                                                        <tr>
                                                            <td>
                                                                <h2 style="margin: 0px;">Vloeren</h2>
                                                            </td>
                                                        </tr>
                                                        <tr>
                                                            <td
                                                                style="color: #153643; font-family: Arial, sans-serif; font-size: 16px; line-height: 20px;">
                                                                """+str(cleaners.get("Vloeren"))+"""
                                                            </td>
                                                        </tr>
                                                    </table>
                                                </td>
                                                <td width="260" valign="top">
                                                    <table border="0" cellpadding="0" cellspacing="0" width="100%">
                                                        <tr>
                                                            <td>
                                                                <h2 style="margin: 0px;">Schoonmaken</h2>
                                                            </td>
                                                        </tr>
                                                        <tr>
                                                            <td
                                                                style="color: #153643; font-family: Arial, sans-serif; font-size: 16px; line-height: 20px;">
                                                                """+str(cleaners.get("Schoonmaken"))+"""
                                                            </td>
                                                        </tr>
                                                    </table>
                                                </td>
                                                <td width="260" valign="top">
                                                    <table border="0" cellpadding="0" cellspacing="0" width="100%">
                                                        <tr>
                                                            <td>
                                                                <h2 style="margin: 0px;">Wegbrengen</h2>
                                                            </td>
                                                        </tr>
                                                        <tr>
                                                            <td
                                                                style="color: #153643; font-family: Arial, sans-serif; font-size: 16px; line-height: 20px;">
                                                                """+str(cleaners.get("Wegbrengen"))+"""
                                                            </td>
                                                        </tr>
                                                    </table>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                                <tr>
                                    <td style="padding-top: 40px;">
                                        <p style="margin: 0px;">
                                            <i><b>Vloeren:</b> """+str(config.jobs.get("Vloeren"))+"""</i>
                                        </p>
                                        <p style="margin: 0px;">
                                            <i><b>Schoonmaken:</b> """+str(config.jobs.get("Schoonmaken"))+"""</i>
                                        </p>
                                        <p style="margin: 0px;">
                                            <i><b>Wegbrengen:</b> """+str(config.jobs.get("Wegbrengen"))+"""</i>
                                        </p>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
            """, subtype='html')
            if args.debug:
                print(f"INFO: Email sent to {name} \t-> {email}")
            else:
                if args.verbose: print(f"INFO: Email sent to {name} \t-> {email}")
                smtp.send_message(msg)

if __name__ == "__main__":
    main()
