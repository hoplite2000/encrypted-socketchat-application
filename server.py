import socket, time, sys
from cryptography.fernet import Fernet 
from datetime import datetime 
from colorama import Fore,Style,init 

#variables
crash = False 
buff_size = 1048
socket_pwd = '/mnfncal!()OA='

#timestamp
def gettime():
    n = datetime.now()
    now = "%s:%s:%s"%(n.hour,n.minute,n.second)
    return now 

#colors 
init()
w = Style.BRIGHT + Fore.WHITE 
r = Style.BRIGHT + Fore.RED 
g = Style.BRIGHT + Fore.GREEN 
c = Style.BRIGHT + Fore.CYAN 
y = Style.BRIGHT + Fore.YELLOW 

#socket
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #TCP
s_addr = ("localhost",1337)

#encrytion-decryption
key = Fernet.generate_key()
print("\n\n ENCRYPTION-KEY=> %s\n\n"%(key.decode()))
f = Fernet(key)

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

#server
class socket_server:
    def __init__(self, f, s, s_addr, buff_size, socket_pwd):
        self.f = f 
        self.buff_size = buff_size
        self.socket_pwd = socket_pwd

    def create_socket(self):
        sys.stdout.write(w+"\r ["+c+"%s"%(gettime())+w+"] ["+g+"INFO"+w+"]"+g+" Binding Address..")
        sys.stdout.flush()
        try:
            s.bind(s_addr)
            print(w+"BINDED") 
        except:
            print(r+"ERROR")
            s.close()
            quit()
        sys.stdout.write(w+"\r ["+c+"%s"%(gettime())+w+"] ["+g+"INFO"+w+"]"+g+" Waiting for Client..")
        sys.stdout.flush()
        s.listen(1)
        (client,addr) = s.accept()
        self.client = client 
        self.addr = addr 
        print(w+"CONNECTION ESTABLISHED => %s"%(str(addr)))

    def run_server(self):
        sys.stdout.write(w+"\r ["+c+"%s"%(gettime())+w+"] ["+g+"INFO"+w+"]"+g+" Waiting for Password..")
        sys.stdout.flush()
        try:
            encr_pkg = self.client.recv(buff_size)
            print(w+"RECEIVED")
        except socket.error as e:
            print(r+"ERROR")
            print(e)
            self.client.close()
            s.close()
            quit()
        print(w+" ["+c+"%s"%(gettime())+w+"] ["+g+"INFO"+w+"]"+g+" Message=> %s"%(decryption(encr_pkg,f)))
        if (decryption(encr_pkg,f) == socket_pwd):
            print(g+"Correct Password!")
            msg = "correct pwd"
            pkg = encryption(msg,f)
        else:
            print(r+"False Password!")
            msg = "false pwd"
            pkg = encryption(msg,f)
        sys.stdout.write(w+"\r ["+c+"%s"%(gettime())+w+"] ["+g+"INFO"+w+"]"+g+" Sending Message..")
        sys.stdout.flush()
        try:
            self.client.send(pkg)
            print(w+"SENT")
        except socket.error as e:
            print(r+"ERROR")
            print(e)
            self.client.close()
            s.close()
            quit()
        if (msg == 'false pwd'):
            self.client.close()
            s.close()
            quit()
        while True:
            sys.stdout.write(w+"\r ["+c+"%s"%(gettime())+w+"] ["+g+"INFO"+w+"]"+g+" Waiting for Message from Client..")
            sys.stdout.flush()
            try:
                encr_pkg = self.client.recv(buff_size)
                print(w+"RECEIVED")
            except socket.error as e:
                print(r+"ERROR")
                print(e)
                self.client.close()
                s.close()
                False
            print(w+"\n ["+c+"%s"%(gettime())+w+"] ["+g+"CLIENT"+w+"]"+g+" Message=> %s\n"%(decryption(encr_pkg,f)))
            msg = input(w+"Your Message>> ")
            pkg = encryption(msg, f)
            sys.stdout.write(w+"\r ["+c+"%s"%(gettime())+w+"] ["+g+"INFO"+w+"]"+g+" Sending Message..")
            sys.stdout.flush()
            try:
                self.client.send(pkg)
                print(w+"SENT")
            except socket.error as e:
                print(r+"ERROR")
                print(e)
                self.client.close()
                s.close()
                False

#MAIN
while (crash != True):
    try:
        server = socket_server(f, s, s_addr, buff_size, socket_pwd)
        server.create_socket()
        server.run_server()
    except KeyboardInterrupt:
        crash = True 
s.close()