import config  # Config file
import smtplib
import sys
from email.message import EmailMessage
from datetime import date


def main():
    if len(sys.argv) != 2:
        send_CleanerMail(1)
    else:
        send_CleanerMail(sys.argv[1])


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


def send_CleanerMail(send_all):
    cleaners = get_cleaners(0, sorted(list(config.contacts.keys())))
    print("Floor: \t\t"+cleaners["floor"])
    print("Surface: \t"+cleaners["surface"])

    if send_all:
        subject = "Schoonmaakrooster"
        sendTo = config.contacts
    else:
        subject = "HERINNERING Schoonmaakrooster"
        keys = [cleaners["floor"],cleaners["surface"]]
        sendTo = {x:config.contacts[x] for x in keys}

    with smtplib.SMTP_SSL('smtp.strato.com', 465) as smtp:
        smtp.login(config.email.get("adress"), config.email.get("password"))
        for name, email in sendTo.items():
            msg = EmailMessage()
            msg['Subject'] = subject
            msg['From'] = str("Club Huyzch <"+config.email.get("adress")+">")
            msg['To'] = email
            msg.set_content(
                'Weeknummer: '+str(date.today().isocalendar()[1]) +
                '\nVloer: '+cleaners["floor"] +
                '\nOppervlaktes: '+cleaners["surface"]
            )
            msg.add_alternative("""\
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
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
          <table
            align="center"
            border="0"
            cellpadding="0"
            cellspacing="0"
            width="600"
            style="border: 1px solid #cccccc; border-collapse: collapse;"
          >
            <tr>
              <td
                align="center"
                bgcolor="#153643"
                style="padding: 30px 0 30px 0; color: #153643; font-size: 28px; font-weight: bold; font-family: Arial, sans-serif;"
              >
                <img
                  src="http://www.clubhuyzch.nl/images/logo_white-2x.png"
                  alt="Club Huyzch logo"
                  width="200"
                  style="display: block;"
                />
              </td>
            </tr>
            <tr>
              <td bgcolor="#ffffff" style="padding: 40px 30px 30px 30px;">
                <table border="0" cellpadding="0" cellspacing="0" width="100%">
                  <tr>
                    <td
                      style="color: #000000; font-family: Arial, sans-serif;text-align: center; font-size: 30px;"
                    >
                      <b>Schoonmaakrooster</b>
                    </td>
                  </tr>
                  <tr>
                    <td
                      style="padding: 20px 0 30px 0; color: #153643; font-family: Arial, sans-serif; font-size: 16px; line-height: 20px;"
                    >
                      Halloooo """+str(name)+"""! Er mag weer lekker geschrobt en
                      geboend worden. Hieronder staan de schoonmakers voor week
                      """+str(date.today().isocalendar()[1])+""".
                    </td>
                  </tr>
                  <tr>
                    <td>
                      <table
                        border="0"
                        cellpadding="0"
                        cellspacing="0"
                        width="100%"
                      >
                        <tr>
                          <td width="260" valign="top">
                            <table
                              border="0"
                              cellpadding="0"
                              cellspacing="0"
                              width="100%"
                            >
                              <tr>
                                <td>
                                  <h2 style="margin: 0px;">Vloeren</h2>
                                </td>
                              </tr>
                              <tr>
                                <td
                                  style="color: #153643; font-family: Arial, sans-serif; font-size: 16px; line-height: 20px;"
                                >
                                  """+cleaners["floor"]+"""
                                </td>
                              </tr>
                            </table>
                          </td>
                          <td style="font-size: 0; line-height: 0;" width="20">
                            &nbsp;
                          </td>
                          <td width="260" valign="top">
                            <table
                              border="0"
                              cellpadding="0"
                              cellspacing="0"
                              width="100%"
                            >
                              <tr>
                                <td>
                                  <h2 style="margin: 0px;">Opruimen</h2>
                                </td>
                              </tr>
                              <tr>
                                <td
                                  style="color: #153643; font-family: Arial, sans-serif; font-size: 16px; line-height: 20px;"
                                >
                                  """+cleaners["surface"]+"""
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
                        <i
                          ><b>Vloeren:</b> Stofzuigen en dweilen van de gang,
                          keuken en woonkamer. (en nee niet de gang dweilen)</i
                        >
                      </p>
                      <p style="margin: 0px;">
                        <i
                          ><b>Opruimen:</b> Opruimen van de keuken en woonkamer,
                          het doen van de huiswas en het karton weg brengen.</i
                        >
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
            smtp.send_message(msg)
            print("Email sent to "+ name+" \t ->  "+email)

if __name__ == "__main__":
    main()
