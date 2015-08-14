#!/usr/bin/python

import sys, os, commands

def system_command(clicommand, type):
     try:           
         status, output = commands.getstatusoutput(clicommand)
     except TypeError:
         error_message = "Problem with command: %s" % (clicommand) 
         print >>sys.stderr, error_message
         send_email(os.environ['EMAIL_TO'], os.environ['EMAIL_FROM'], "PROBLEM: docker backup of " + sys.argv[1], error_message)
         if type == 'output':
             return ""
         else:
             return status
  
     if status == 0:
         if type == 'output':
             return output
         else:
             return status
     else:
         error_message = "Problem with command: %s\nError: %s" % (clicommand, output)
         print >>sys.stderr, error_message
         send_email(os.environ['EMAIL_TO'], os.environ['EMAIL_FROM'], "PROBLEM: docker backup of " + sys.argv[1], error_message)
         if type == 'output':
             return ""
         else:
             return status

def send_email(to, efrom, subject, message):
    if to == "":
       return
    import smtplib
    from email.mime.text import MIMEText
    print "Email: %s - %s" % (subject, message)
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = efrom
    msg['To'] = to
    s = smtplib.SMTP('localhost')
    try:
        s.sendmail(efrom, [efrom], msg.as_string())
    except:
        s.quit()
        print >>sys.stderr, 'ERROR: Problem with sending of email'
    s.quit()

sprefix = system_command('date +"' + os.environ['PREFIX'] + '"', 'output')
ssuffix = system_command('date +"' + os.environ['SUFFIX'] + '"', 'output')
tar = sprefix + sys.argv[1] + ssuffix + ".tar"

print "BACKUP: %s - %s" % (sys.argv[1], tar)
if system_command('/docker-backup/docker-backup ' + os.environ['OPTS'] + ' \
      -addr /docker.sock store "' + os.environ['BACKUPS'] + '/' + tar + '" "' \
       + sys.argv[1] + '"', 'status') != 0:
    sys.exit(1)

system_command('gzip "' + os.environ['BACKUPS'] + '/' + tar + '"', 'status')

print "UPLOAD: %s - %s" % (sys.argv[1], tar)
system_command('s3cmd --access_key="' + os.environ['ACCESS_KEY'] + '" --secret_key="' + os.environ['SECRET_KEY'] + '" \
          -c /dev/null ' + os.environ['S3CMD_OPTS'] + ' put "' + os.environ['BACKUPS'] + '/' + tar + '.gz" ' + \
          os.environ['BUCKET'], 'status')
system_command('rm "'+ os.environ['BACKUPS'] + '/' + tar + '.gz"', 'status')
