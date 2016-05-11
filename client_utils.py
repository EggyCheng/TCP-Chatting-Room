import argparse, socket, time, memcache

def parse_command_line(description):
    """Parse command line and return a socket address."""
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-p', metavar='port', type=int, default=1070,
                        help='TCP port (default 1070)')
    args = parser.parse_args()
    address = ('127.0.0.1', args.p)
    return address

def v_request():
    uname = input('usernmae:')
    passwd = input('password:')
    token = "90187580da9e36b02149"
    acc =  uname + ";" + passwd + ";" + token
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('127.0.0.1', 1060))
    sock.sendall(acc.encode())
    reply = sock.recv(4096)
    print('The server said login ', reply.decode())
    if (reply.decode()=="success"):
        return sock,uname
    else:
        print ("login fail")
        sock.close()

def accept_connections_forever(sock,uname):
    while True:
        reply = sock.recv(4096)
        message = reply.decode()
        if(message.endswith("bd785c92b41f71e7c49b")):  #get send message from user
            uname = message.split(";")[0]
            message = message.split(";")[1]
            print("The %s said : %s" % (uname,message))
        elif(message.endswith("73556db3b27ba48e180a")):  #get send message from user
            uname = message.split(";")[0]
            message = message.split(";")[1]
            print("The %s said : %s" % (uname,message))
        else:
            print('The server said : ', message)
            print()
            if(message=="bye"):
                print ("bye~bye~")
                break
                sock.close()
                #self.exit.set()
                #return 20
            

def typecmd(sock,uname):
    while True:
        text = input("Me:")
        if(text=="friendlist"):
            token = "e0df606e8d8371318a75"
            text = uname + ";" +text + ";" + token
        elif(text.startswith("friendadd")):
            token = "9b5ee10b35dc972542e8"
            fname = text.split(" ")[1]
            text = uname + ";" +text + ";" + token
        elif(text.startswith("frienddel")):
            token = "7dd14502ccbdc835ed86"
            fname = text.split(" ")[1]
            text = uname + ";" +text + ";" + token
        elif(text.startswith("send")):
            token = "bd785c92b41f71e7c49b"
            send = text.split(":")[0]
            recname = send.split(" ")[1]
            mess = text.split(":")[1]
            text = uname + ";" + recname + ";" + mess + ";" + token
        elif(text.startswith("talk")):
            token = "73556db3b27ba48e180a"
            recname = text.split(" ")[1]
            text = uname + ";" + recname + ";" + token
        elif(text=="exit"):
            token = "c17761a60bf2277982bd"
            text = uname + ";" +text + ";" + token
        elif(text.startswith("offmess")):
            token = "4e52fc424c0dd00271a0"
            send = text.split(":")[0]
            recname = send.split(" ")[1]
            mess = text.split(":")[1]
            text = uname + ";" + recname + ";" + mess + ";" + token
        else:
            text = uname + ";" + text

        sock.sendall(text.encode())