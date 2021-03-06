import argparse, socket, time, memcache, json, time

socklist = dict()
talkcount = 0
talklist = dict()
fileinfo = list()
#0
def parse_command_line(description):
    """Parse command line and return a socket address."""
    parser = argparse.ArgumentParser(description=description)
    args = parser.parse_args()
    address = ('127.0.0.1', 1060)
    return address

#1
def create_srv_socket(address):
    """Build and return a listening server socket."""
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind(address)
    listener.listen(64)
    print('Listening at {}'.format(address))
    return listener
#2
def accept_connections_forever(listener):
    """Forever answer incoming connections on a listening socket."""
    while True:
        sock, address = listener.accept()
        print(sock)
        print('Accepted connection from {}'.format(address))
        handle_conversation(sock,address)

#let server handle conversation without stop
def handle_conversation(sock, address):
    """Converse with a client over `sock` until they are done talking."""
    try:
        while True:
            handle_request(sock)
    except EOFError:
        print('Client socket to {} has closed'.format(address))
    except Exception as e:
        print('Client {} error: {}'.format(address, e))
    finally:
        sock.close()

#call from handle_conversation
def handle_request(sock):
    """Receive a single client request on `sock` and send the answer."""
    talklist = list()
    message = sock.recv(4096)
    message = message.decode('utf-8')
    if (talkcount == 2):  # start talk statement
        talkto_start(message,sock)
    else:
        if (message.endswith("90187580da9e36b02149")):
            v_response(message,sock)
        elif (message.endswith("e0df606e8d8371318a75")):
            friendlist_response(message,sock)
        elif (message.endswith("c17761a60bf2277982bd")):
            logout_system(message,sock)
        elif (message.endswith("9b5ee10b35dc972542e8")):
            friendadd_response(message,sock)
        elif (message.endswith("7dd14502ccbdc835ed86")):
            frienddel_response(message,sock)
        elif (message.endswith("bd785c92b41f71e7c49b")):
            sendto_other(message,sock)
        elif (message.endswith("73556db3b27ba48e180a")):
            talkto_request(message,sock)
        elif (message.endswith("7f77e82579a5c857c310")):
            trans_file_toserver(message,sock)
        elif (message.endswith("f6990c57956cba967c3b")):
            trans_file_toclient(message,sock)
        elif (message.endswith("da724d3ba86ce29d7b82")):
            trans_file_denied(message,sock)
        elif (message.endswith("4b490bbe85a8fa282d2c")):
            change_password(message,sock)
        else:
            m_response(message,sock)

#the login request response
def v_response(message,sock):
    """Return the string response to a particular Zen-of-Python aphorism."""
    mc = memcache.Client(['127.0.0.1:11211'])
    global socklist
    uname = message.split(";")[0]
    passwd = message.split(";")[1]
    print("username:%s" % uname)
    print("password:%s" % passwd)
    if(mc.get('aaaa')[0]==uname and mc.get('aaaa')[1]==passwd and mc.get('aaaa')[2]=="offline"):
        print("======================================")
        print('user: %s login!! sock number is : %d' % (uname,sock.fileno()))
        print("======================================")
        loginmes = "success"
        sock.sendall(loginmes.encode())
        userinfo = mc.get('aaaa')
        userinfo[2] = "online"
        userinfo[4] = sock.fileno()
        socklist.setdefault(sock.fileno(),sock)
        mc.set('aaaa',userinfo)
        #write login record in log.txt
        f = open("log.txt","a+")
        ticks = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
        f.write("["+ticks+"]"+uname + " login success.")
        f.write("\n")

    elif(mc.get('cccc')[0]==uname and mc.get('cccc')[1]==passwd and mc.get('cccc')[2]=="offline"):
        print("======================================")
        print('user: %s login!! sock number is : %d' % (uname,sock.fileno()))
        print("======================================")
        loginmes = "success"
        sock.sendall(loginmes.encode())
        userinfo = mc.get('cccc')
        userinfo[2] = "online"
        userinfo[4] = sock.fileno()
        socklist.setdefault(sock.fileno(),sock)
        mc.set('cccc',userinfo)
        #write login record in log.txt
        f = open("log.txt","a+")
        ticks = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
        f.write("["+ticks+"]"+uname + " login success.")
        f.write("\n");
    else:
        print('identity fail.QAQQAQQAQQAQQAQQAQQAQQAQQAQQAQQAQ')
        sock.sendall(b'fail')
        sock.close()
        #write login record in log.txt
        f = open("log.txt","a+")
        ticks = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
        f.write("["+ticks+"]"+uname + " login fail.")
        f.write("\n");

#the message request
def m_response(message,sock):
    print (message)
    message = message.encode()
    wrongcli = "You send a invalid command."
    sock.sendall(wrongcli.encode())
    if not message:
        raise EOFError('socket closed')

def friendlist_response(message,sock):
    mc = memcache.Client(['127.0.0.1:11211'])
    uname = message.split(";")[0]
    if (uname=="aaaa"):
        friendlist = mc.get('aaaa')[3]
        for val in friendlist:
            fdlive = mc.get(val)[2]
            message = val + " "+ fdlive
            print(val + " "+ fdlive)
            message = message.encode()
            sock.sendall(message)
    elif (uname=="cccc"):
        friendlist = mc.get('cccc')[3]
        for val in friendlist:
            fdlive = mc.get(val)[2]
            message = val + " "+ fdlive
            print(val + " "+ fdlive)
            message = message.encode()
            sock.sendall(message)

def friendadd_response(message,sock):
    mc = memcache.Client(['127.0.0.1:11211'])
    uname = message.split(";")[0]
    addfd = message.split(";")[1]
    addfd = addfd.split(" ")[1]
    if (uname=="aaaa"):
        userinfo = mc.get('aaaa')
        friendlist = userinfo[3]
        fdlive=0
        for val in friendlist:
            if (val == addfd):
                errormess = "You haved added this friend. You can't do it again."
                sock.sendall(errormess.encode())
                fdlive = 1
        if (fdlive == 0):
            friendlist.append(addfd)
            userinfo[3] = friendlist
            mc.set('aaaa',userinfo)
            successmess = "Add " + addfd + " success!!"
            sock.sendall(successmess.encode())
    elif (uname=="cccc"):
        userinfo = mc.get('cccc')
        friendlist = userinfo[3]
        fdlive=0
        for val in friendlist:
            if (val == addfd):
                errormess = "You haved added this friend. You can't do it again."
                sock.sendall(errormess.encode())
                fdlive = 1
        if (fdlive == 0):
            friendlist.append(addfd)
            userinfo[3] = friendlist
            mc.set('cccc',userinfo)
            successmess = "Add " + addfd + " success!!"
            sock.sendall(successmess.encode())

def frienddel_response(message,sock):
    mc = memcache.Client(['127.0.0.1:11211'])
    uname = message.split(";")[0]
    delfd = message.split(";")[1]
    delfd = delfd.split(" ")[1]
    if (uname=="aaaa"):
        userinfo = mc.get('aaaa')
        friendlist = userinfo[3]
        friendlist.remove(delfd)
        userinfo[3] = friendlist
        mc.set('aaaa',userinfo)
    elif (uname=="cccc"):
        userinfo = mc.get('ccc')
        friendlist = userinfo[3]
        friendlist.remove(delfd)
        userinfo[3] = friendlist
        mc.set('cccc',userinfo)

def logout_system(message,sock):
    mc = memcache.Client(['127.0.0.1:11211'])
    uname = message.split(";")[0]
    if (mc.get('aaaa')[0] == uname ):
        userinfo = mc.get('aaaa')
        userinfo[2] = "offline"
        userinfo[4] = ""
        mc.set('aaaa',userinfo)
    elif (mc.get('cccc')[0] == uname ):
        userinfo = mc.get('cccc')
        userinfo[2] = "offline"
        userinfo[4] = ""
        mc.set('cccc',userinfo)
    byem = "bye"
    sock.sendall(byem.encode())
    if not message:
        raise EOFError('socket closed')

def sendto_other(message,sock):
    global socklist
    mc = memcache.Client(['127.0.0.1:11211'])
    uname = message.split(";")[0]
    recname = message.split(";")[1]
    mess = message.split(";")[2]
    onoff = 0
    allmess = uname + ";" + mess + ";" + "bd785c92b41f71e7c49b" #tell client it is send message
    for key in socklist:
        if (mc.get(recname)[4]==key):
            sendsock = socklist[key]
            sendsock.sendall(allmess.encode())
            onoff = 1
            break

    if(onoff == 0):
        failmess = recname + " is not online. Server have leave your message to him/her."
        sock.sendall(failmess.encode())
        userinfo = mc.get(recname)
        offlinemess = userinfo[5]
        print (uname + " leave a off line message:'" + mess + "' , to " + recname)
        offlinemess.append(allmess)
        userinfo[5] = offlinemess
        mc.set(recname,userinfo)

def talkto_request(message,sock):
    global socklist
    global talkcount
    global talklist
    mc = memcache.Client(['127.0.0.1:11211'])
    uname = message.split(";")[0]
    recname = message.split(";")[1]
    mess = uname + " want to talk with you."
    onoff = 0
    for key in socklist:
        if (mc.get(recname)[4]==key):
            sendsock = socklist[key]
            sendsock.sendall(mess.encode())
            talklist.setdefault(uname ,recname)
            onoff = 1
            talkcount += 1
            break

    if(onoff == 0):
        failmess = recname + " is not online."
        sock.sendall(failmess.encode())

def talkto_start(message,sock):
    global socklist
    global talklist
    global talkcount
    mc = memcache.Client(['127.0.0.1:11211'])
    uname = message.split(";")[0]
    mess = message.split(";")[1]
    onoff = 0
    
    for user in talklist:  #ex {'aaaa':'cccc','cccc':'aaaa'}
        if(uname == user):
            recname = talklist[user]
            for key in socklist: #ex {'aaaa':sock,'cccc',sock}
                if (mc.get(recname)[4]==key):
                    sendsock = socklist[key]
                    if (mess == "exittalk"):
                          talkcount = 0
                          talkstopmess = "The talk in stop."
                          sendsock.sendall(talkstopmess.encode())
                          sock.sendall(talkstopmess.encode())


                    allmess = uname + ";" + mess + ";" + "73556db3b27ba48e180a" #tell client it is talk message
                    f = open("talk_history.txt","a+")
                    ticks = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
                    f.write("["+ticks+"]"+uname + "->" + recname + ":" + mess)
                    f.write("\n")
                    sendsock.sendall(allmess.encode())
                    onoff = 1
                    break

    if(onoff == 0):
        failmess = recname + " is not online."
        sock.sendall(failmess.encode())

def trans_file_toserver(message,sock):
    global socklist
    global fileinfo
    mc = memcache.Client(['127.0.0.1:11211'])
    message = message.split("7f77e82579a5c857c310")[0]
    message = json.loads(message)
    uname = message['uname']
    recname = message['recname']
    filename = message['filename']
    filedata = message['filedata']
    # #save file in server_file
    filedata = repr(filedata)[2:-1]
    with open('server_file/'+filename, 'wb+') as output:
                       output.write(filedata.encode('utf-8'))
    for key in socklist:
        if (mc.get(recname)[4]==key):
            sendsock = socklist[key]
            confrimmess = "Do you want to get the file from " +  uname + "(y/n) ?;" + recname + ";440f7a4f63c49279efb8"
            sendsock.sendall(confrimmess.encode())
            ackmess = "waiting for " +  recname
            sock.sendall(ackmess.encode())
            # fileinfo[0] = uname
            # fileinfo[1] = sock
            # fileinfo[2] = recname
            # fileinfo[3] = sendsock
            # fileinfo[4] = filename
            # fileinfo[5] = filedata
            fileinfo.append(uname)
            fileinfo.append(sock)
            fileinfo.append(recname)
            fileinfo.append(sendsock)
            fileinfo.append(filename)
            fileinfo.append(filedata)
            break


def trans_file_toclient(message,sock):
    global fileinfo
    uname = fileinfo[0]
    osock = fileinfo[1]
    recname = fileinfo[2]
    #sendsock = fileinfo[3]
    filename = fileinfo[4]
    filedata = fileinfo[5]
    sendmess = dict()
    sendmess.setdefault('filename',filename)
    sendmess.setdefault('filedata',filedata)
    sendmess = json.dumps(sendmess) + "f6990c57956cba967c3b"
    sock.sendall(sendmess.encode('utf-8'))
    successmess = "You transmited the " + filename + " to " + recname + " successfully."
    osock.sendall(successmess.encode())
    fileinfo.clear()
    

def trans_file_denied(message,sock):
    global fileinfo
    uname = fileinfo[0]
    sock = fileinfo[1]
    recname = fileinfo[2]
    sendsock = fileinfo[3]
    socksendmess = "File transmit denied by " + recname + "."
    senddsocksendmess = "You have denied the file from " + uname + "."
    sendsock.sendall(senddsocksendmess.encode('utf-8'))
    sock.sendall(socksendmess.encode('utf-8'))
    fileinfo.clear()

def change_password(message,sock):
    mc = memcache.Client(['127.0.0.1:11211'])
    uname = message.split(";")[0]
    message = message.split(";")[1]
    passwd = message.split(" ")[1]
    userinfo = mc.get(uname)
    userinfo[1] = passwd
    mc.set(uname,userinfo)
    successmess = "You changed your password successfully."
    sock.sendall(successmess.encode())