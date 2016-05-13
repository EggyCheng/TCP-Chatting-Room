import argparse, socket, time, memcache
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
        elif(message.endswith("578fdbe645445ab95fab")):  #get file data message from user
            uname = message.split(";")[0]
            filename = message.split(";")[1]
            filedata = message.split(";")[2]
            if (uname == "aaaa"):
                with open('cccc_client_file/'+filename, 'wb+') as output:
                     output.write(filedata.encode('utf-8'))
                print("The %s send file : %s to you." % (uname,filename))
            elif (uname == "cccc"):
                with open('aaaa_client_file/'+filename, 'wb+') as output:
                     output.write(filedata.encode('utf-8'))
                print("The %s send file : %s to you." % (uname,filename))
        elif(message.endswith("7f77e82579a5c857c310")):  #get file data message confirm from user
            mc = memcache.Client(['127.0.0.1:11211'])
            recname = message.split(";")[2]
            userinfo = mc.get(recname)
            userinfo[6] = 1
            mc.set(recname,userinfo)
            message = message.split(";")[0]
            print('The server said : ', message)
        else:
            print('The server said : ', message)
            if(message=="bye"):
                print ("bye~bye~")
                break
                sock.close()
                #self.exit.set()
                #return 20
            

def typecmd(sock,uname):
    while True:
        mc = memcache.Client(['127.0.0.1:11211'])
        transfile = 0
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
        elif(text.startswith("filesend")):
            token = "7f77e82579a5c857c310"
            send = text.split(":")[0]
            recname = send.split(" ")[1]
            filename = text.split(":")[1]
            transfile = 1
            if (uname == "aaaa"):
                with open ("aaaa_client_file/"+filename,'rb') as filedata:
                     text = uname + ";" + recname + ";" + filename + ";" +str(filedata.read(5000)) + ";" + token      
                     sock.send(text.encode())
            elif (uname == "cccc"):
                with open ("cccc_client_file/"+filename,'rb') as filedata:
                     text = uname + ";" + recname + ";" + filename + ";" +str(filedata.read(5000)) + ";" + token      
                     sock.send(text.encode())
        elif(mc.get('uname')[6]==1):
            print("test")

        else:
            text = uname + ";" + text
        
        if transfile == 0: 
            sock.sendall(text.encode())
