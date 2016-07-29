# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText

msg = MIMEText('body')
msg['Subject'] = 'Pokemon Bot Status'
me = 'pokemongobotdev@gmail.com'
you = 'darcy.qiu@gmail.com'
msg['From'] = me
msg['To'] = you

# Send the message via our own SMTP server, but don't include the
# envelope header.
s = smtplib.SMTP('smtp.gmail.com', 587)
s.ehlo()
s.starttls()
s.ehlo()
s.login(me, 'Darcy0217')
s.sendmail(me, [you], msg.as_string())
s.quit()