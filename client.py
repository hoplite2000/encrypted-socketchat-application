import socket,sys,os 
from datetime import datetime 
from colorama import Fore,init,Style 
from cryptography.fernet import Fernet

#variables
buff_size = 1048

#timestamp
def gettime():
    n = datetime.now()
    now = "%s:%s:%s" % (n.hour, n.minute, n.second)
    return now

#colors
init()
w = Style.BRIGHT + Fore.WHITE
r = Style.BRIGHT + Fore.RED
g = Style.BRIGHT + Fore.GREEN
c = Style.BRIGHT + Fore.CYAN
y = Style.BRIGHT + Fore.YELLOW

#socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP
s_addr = ("localhost", 1337)

#encryption-decryption
def encryption(msg,f):
    sys.stdout.write(w+"\r ["+c+"%s"%(gettime())+w+"] ["+g+"INFO"+w+"]"+g+" Encrypting Package..")
    sys.stdout.flush()
    encrypted_msg = f.encrypt(msg.encode())
    print(w+"ENCRYPTED")
    return encrypted_msg

def decryption(pkg,f):
    sys.stdout.write(w+"\r ["+c+"%s"%(gettime())+w+"] ["+g+"INFO"+w+"]"+g+" Decrypting Package..")
    sys.stdout.flush()
    msg = f.decrypt(pkg)
    decrypted_msg = msg.decode()
    print(w+"DECRYPTED")
    return decrypted_msg

#MAIN
os.system("cls") #WINDOWS
sys.stdout.write(w+"\r ["+c+"%s"%(gettime())+w+"] ["+g+"INFO"+w+"]"+g+" Connecting to %s"%(str((s_addr))))
sys.stdout.flush()
try:
    s.connect(s_addr)
    print(w+"CONNECTED")
except socket.error as e:
    print(r+"FAILED")
    print(e)
    s.close()
    quit()
pwd = input("Password=> ")
key = input("Encryption-Key=> ")
f = Fernet(key.encode())
pkg = encryption(pwd,f)
sys.stdout.write(w+"\r ["+c+"%s"%(gettime())+w+"] ["+g+"INFO"+w+"]"+g+" Sending Packet..")
sys.stdout.flush()
try:
    s.send(pkg)
    print(w+"SENT")
except socket.error as e:
    print(r+"ERROR")
    print(e)
    s.close()
    quit()
sys.stdout.write(w+"\r ["+c+"%s"%(gettime())+w+"] ["+g+"INFO"+w+"]"+g+" Waiting for response from Server..")
sys.stdout.flush()
try:
    pkg = s.recv(buff_size)
    print(w+"RECEIVED")
except socket.error as e:
    print(r+"ERROR")
    print(e)
    s.close()
    quit()
msg = decryption(pkg,f)
print(w+"\r ["+c+"%s"%(gettime())+w+"] ["+g+"SERVER"+w+"]"+g+" Message=> %s"%(msg))
if (msg == "false pwd"):
    s.close()
    quit()
while True:
    print("\n\n")
    msg = input("Your Message>> ")
    pkg = encryption(msg,f)
    sys.stdout.write(w+"\r ["+c+"%s"%(gettime())+w+"] ["+g+"INFO"+w+"]"+g+" Sending Packet..")
    sys.stdout.flush()
    try:
        s.send(pkg)
        print(w+"SENT")
    except socket.error as e:
        print(r+"ERROR")
        print(e)
        s.close()
        quit()
    sys.stdout.write(w+"\r ["+c+"%s"%(gettime())+w+"] ["+g+"INFO"+w+"]"+g+" Waiting for response from Server..")
    sys.stdout.flush()
    try:
        pkg = s.recv(buff_size)
        print(w+"RECEIVED")
    except socket.error as e:
        print(r+"ERROR")
        print(e)
        s.close()
        quit()
    msg = decryption(pkg,f)
    print(w+"\r ["+c+"%s"%(gettime())+w+"] ["+g+"SERVER"+w+"]"+g+" Message=> %s"%(msg))