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
    print('The server said', reply)
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
        else:
            text = uname + ";" + text

        sock.sendall(text.encode())

# #1
# def create_srv_socket(address):
#     """Build and return a listening server socket."""
#     listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#     listener.bind(address)
#     listener.listen(64)
#     print('Listening at {}'.format(address))
#     return listener

#2
# def accept_connections_forever(listener):
#     """Forever answer incoming connections on a listening socket."""
#     while True:
#         sock, address = listener.accept()
#         print('Accepted connection from {}'.format(address))
#         handle_request(sock)

#3
# def handle_conversation(sock, address):
#     """Converse with a client over `sock` until they are done talking."""
#     try:
#         while True:
#             handle_request(sock)
#     except EOFError:
#         print('Client socket to {} has closed'.format(address))
#     except Exception as e:
#         print('Client {} error: {}'.format(address, e))
#     finally:
#         sock.close()
#4
# def handle_request(sock):
#     """Receive a single client request on `sock` and send the answer."""
#     acc = recv_until(sock)
#     answer = get_answer(acc)
#     sock.sendall(answer)
#     print (acc.decode())

# #5
# def recv_until(sock):
#     """Receive bytes over socket `sock` until we receive the `suffix`."""
#     message = sock.recv(4096)
#     if not message:
#         raise EOFError('socket closed')
#     return message
