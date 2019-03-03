#Contains different functions for commands and stuff

_ModList = []   #Will contain the list of all the moderators

def disconnect(Sock, user):
    if user.lower() in _ModList:
        print("Command Recieved : Disconnect")
        Sock.send("DISCONNECT\n".encode())
        Sock.close()
        exit()

def processSay(TcpSocket, user, message):
    message = message.split()
    cmd = message[0].lower()
    print(cmd)
    if cmd == "!disconnect" or cmd == "!dc":
        disconnect(TcpSocket, user)


if __name__ != "__main__":
    mods = open("modlist.txt", "r").read().split()
    for mod in mods:
        _ModList.append(mod.lower())