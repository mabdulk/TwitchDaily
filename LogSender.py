from traceback import format_exc
import EmailService
from datetime import date, datetime

EmailList = ['mustafa.khalil101@gmail.com', 'diaak995@gmail.com']

for email in EmailList:
    EmailService.send_mail_with_attachment('WordlYEnts@gmail.com',email,f"Wordly Logs for {datetime.today().strftime('%Y-%m-%d')}", "Check attachment for loggs",['C:\\Users\\theVmAdmin\\Documents\\YoutubeAutomationPY\\log.txt'])