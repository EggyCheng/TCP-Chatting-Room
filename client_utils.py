import argparse, socket, time, memcache, json
from getpass import getpass

def parse_command_line(description):
    """Parse command line and return a socket address."""
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-p', metavar='port', type=int, default=1070,
                        help='TCP port (default 1070)')
    args = parser.parse_args()
    address = ('127.0.0.1', args.p)
    return address

def v_request():
    mc = memcache.Client(['127.0.0.1:11211'])
    uname = input('usernmae:')
    passwd = getpass()
    token = "90187580da9e36b02149"
    acc =  uname + ";" + passwd + ";" + token
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('127.0.0.1', 1060))
    sock.sendall(acc.encode())
    reply = sock.recv(4096)
    print('The server said login ', reply.decode())
    if (reply.decode()=="success"):
        userinfo =  mc.get(uname)
        alloffmess = userinfo[5]
        if userinfo[5]:
            for val in alloffmess:
                uname = val.split(";")[0]
                offmess = val.split(";")[1]
                print ("user:(" + uname + ") leave a offline message to you:" + offmess) 
           
            alloffmess[:] = [] 
            userinfo[5] = alloffmess
            mc.set('cccc',userinfo)

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
        elif(message.endswith("73556db3b27ba48e180a")):  #get talk message from user
            uname = message.split(";")[0]
            message = message.split(";")[1]
            print("The %s said : %s" % (uname,message))
        elif(message.endswith("f6990c57956cba967c3b")):  #get file data message from user
            message = message.split("f6990c57956cba967c3b")[0]
            message = json.loads(message)
            filename = message['filename']
            filedata = message['filedata']
            if (uname == "aaaa"):
                with open('aaaa_client_file/'+filename, 'wb+') as output:
                     output.write(filedata.encode('utf-8'))
                print("You got the file : %s." % (filename))
            elif (uname == "cccc"):
                with open('cccc_client_file/'+filename, 'wb+') as output:
                     output.write(filedata.encode('utf-8'))
                print("You got the file : %s." % (filename))
        elif(message.endswith("440f7a4f63c49279efb8")):  #get file data message confirm from user
            mc = memcache.Client(['127.0.0.1:11211'])
            recname = message.split(";")[1]
            userinfo = mc.get(recname)
            userinfo[6] = "receive"
            mc.set(recname,userinfo)
            message = message.split(";")[0]
            print('The server said : ', message)
        else:
            if(message=="bye"):
                print ("bye~bye~")
                break
                sock.close()
            else:
                print(message)
            

def typecmd(sock,uname):
    print ("========================================================")
    print ("#friendlist [to show all your friend and online/offline]")
    print ("#friendadd <user name> [to add a friend]")
    print ("#frienddel <user name> [to delete a friend]")
    print ("#send <user name> : <message> [to send other user a message]")
    print ("#talk <user name> [to entry a talk mode with other user (exittalk to stop talking)]")
    print ("#filesend <user name> : <filename> [to send file to other user]")
    print ("*#chpasswd <password> [to change passwordd]")
    print ("*log.txt is the login log file")
    print ("*talk_history.txt is the talk history file")
    print ("#exit [to logout]")
    print ("========================================================")
    while True:
        mc = memcache.Client(['127.0.0.1:11211'])
        transfile = 0
        text = input("")
        userinfo = mc.get(uname)
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
        elif(text.startswith("chpasswd")):
            token = "4b490bbe85a8fa282d2c"
            text = uname + ";" +text + ";" + token
        elif(text.startswith("filesend")):
            token = "7f77e82579a5c857c310"
            send = text.split(":")[0]
            recname = send.split(" ")[1]
            filename = text.split(":")[1]
            transfile = 1
            message = dict()
            message.setdefault('uname',uname)
            message.setdefault('recname',recname)
            message.setdefault('filename',filename)
            if (uname == "aaaa"):
                with open ("aaaa_client_file/"+filename,'rb') as filedata:
                     message.setdefault('filedata',str(filedata.read(5000)))
                     sendmess = json.dumps(message) + token
                     sendmess = sendmess.encode('utf-8')      
                     sock.send(sendmess)
            elif (uname == "cccc"):
                with open ("cccc_client_file/"+filename,'rb') as filedata:
                     message.setdefault('filedata',str(filedata.read(5000)))
                     sendmess = json.dumps(message) + token
                     sendmess = sendmess.encode('utf-8')      
                     sock.send(sendmess)
        elif(userinfo[6]=="receive"):
            if (text == "y" or text == "yes"):
                text = text + "f6990c57956cba967c3b"
                sock.send(text.encode())
                userinfo[6] = ""
                mc.set(uname, userinfo)
                transfile = 1
            elif (text == "n" or text == "no"):
                text = text + "da724d3ba86ce29d7b82"
                sock.send(text.encode())
                userinfo[6] = ""
                mc.set(uname, userinfo)
                transfile = 1
            else:
                print("Please accept or non accept the file transmit.")

        else:
            text = uname + ";" + text
        
        if transfile == 0: 
            sock.sendall(text.encode())
