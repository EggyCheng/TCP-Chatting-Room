import argparse, socket, time, memcache


def parse_command_line(description):
    """Parse command line and return a socket address."""
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-p', metavar='port', type=int, default=1070,
                        help='TCP port (default 1070)')
    args = parser.parse_args()
    address = ('127.0.0.1', args.p)
    return address

#send verfication request to server port: 1060
def v_request():
    uname = input('usernmae:')
    passwd = input('password:')
    token = "90187580da9e36b02149"
    acc =  uname + ":" + passwd + ":" + token
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('127.0.0.1', 1060))
    sock.sendall(acc.encode())
    reply = sock.recv(4096)
    print('The server said', reply)
    if (reply.decode()=="success"):
        return sock
    else:
        print ("login fail")
        sock.close()

def accept_connections_forever(sock):
    """Forever answer incoming connections on a listening socket."""
    #print("communication start!")


def typecmd(sock):
        while True:
            text = input("Me:")
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
