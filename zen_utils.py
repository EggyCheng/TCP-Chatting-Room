import argparse, socket, time, memcache

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
    message = sock.recv(4096)
    message = message.decode()
    print (message)
    if (message.endswith("90187580da9e36b02149")):
        v_response(message,sock)
    else:
        m_response(message,sock)

#the login request response
def v_response(message,sock):
    """Return the string response to a particular Zen-of-Python aphorism."""
    mc = memcache.Client(['127.0.0.1:11211'])
    # setting the user info (:1 means user1,:2 means user2 .........)
    mc.set('uname:1','aaaa')
    mc.set('uname:2','cccc')
    mc.set('passwd:1','bbbb')
    mc.set('passwd:2','dddd')
    mc.set('alive:1','offline')
    mc.set('alive:2','offline')
    #time.sleep(1.0)  # increase to simulate an expensive operation
    uname = message.split(":")[0]
    passwd = message.split(":")[1]
    print("username:%s" % uname)
    print("password:%s" % passwd)
    if(mc.get('uname:1')==uname and mc.get('passwd:1')==passwd):
        print('user: %s login!!' % uname)
        sock.sendall(b'success')
        mc.set('alive:1','online')
    else if(mc.get('uname:2')==uname and mc.get('passwd:2')==passwd):
        print('user: %s login!!' % uname)
        sock.sendall(b'success')
        mc.set('alive:2','online')
    else:
        print('identity fail.QAQQAQQAQQAQQAQQAQQAQQAQQAQQAQQAQ')
        sock.sendall(b'fail')

#the message request
def m_response(message,sock):
    print("message!!")