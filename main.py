#!/usr/bin/python3
import socket
import time
import hashlib
import threading

#TcpSocket
TcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


#Connect to server
def connect(ip, port, user, passw, tries=0):
    if(tries==3):
        print("Connection failed.")
        return

    try:
        print("Connecting to ", str(ip), str(port))
        TcpSocket.connect((ip, port))
        print("Connected!")
        print("Logging in ")

        loginSend = "mlogin " + str(user) + " " + str(passw) + " 0 0\n"
        TcpSocket.send(loginSend.encode())

        print("Logged in")
        TcpSocket.send("SPEC\n".encode())
    except:
        print("Failed... Retrying...")
        connect(ip, port, user, passw, tries+1)
        


#Recieve from server
def recieve():
    print("Recieving..\n")
    LogFile = open("LogFile", "a")
    LogFile.write("-----------" + time.asctime() + "-----------\n\n\n\n")

    while(True):
        recieve = TcpSocket.recv(1024)
        if(len(recieve)>=0):
            LogFile.write("--" +time.asctime() + "--\n" + recieve.decode(encoding="ISO-8859-1") + "\n----\n\n")
            process(recieve.decode(encoding="ISO-8859-1"))
            #print("Recieved : " + recieve.decode())
        else:
            break

    LogFile.close()
    print("Closing...")
    TcpSocket.close()


#Process info and send
def process(rcv):
    rcv = rcv.split("\n")
    for i in rcv[:-1]:  #[:-1] to avoid empty list at the end
        i = i.split()
        if i[0] == "SAY":
            try:
                user = i[1].split("^")[1][2:]
                message = " ".join(i[2:])
                print(user + " : " + message)
            except:
                1+1


#Ping the server to keep connection alive
def ping():
    pingData = "PING\n".encode()
    while(True): 
        time.sleep(10)
        TcpSocket.send(pingData)
        #print("Sent: " + pingData.decode())


def main():
    #Server info
    server_ip = "144.76.163.135"
    server_port = int(input("Enter the port Number: "))

    #UserInfo
    cred = open("Creds.txt", "r").read().split()
    username = cred[0]
    password = cred[1]
    password = hashlib.md5(password.encode()).hexdigest()

    #Connect
    connect(server_ip, server_port, username, password)

    #Opens a thread to Ping every 10 sec
    PingThread = threading.Thread(target=ping)
    PingThread.daemon = True
    PingThread.start()

    recieve()

if __name__ == "__main__":
    main()
