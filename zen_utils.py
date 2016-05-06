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
        print('Accepted connection from {}'.format(address))
        handle_conversation(sock, address)

#3
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
#4
def handle_request(sock):
    """Receive a single client request on `sock` and send the answer."""
    acc = recv_until(sock)
    answer = get_answer(acc)
    sock.sendall(answer)

#5
def recv_until(sock):
    """Receive bytes over socket `sock` until we receive the `suffix`."""
    message = sock.recv(4096)
    if not message:
        raise EOFError('socket closed')
    return message

#6
def get_answer(acc):
    """Return the string response to a particular Zen-of-Python aphorism."""
    mc = memcache.Client(['127.0.0.1:11211'])
    mc.set('user:1','aaaa')
    mc.set('user:2','egg')
    mc.set('passwd:1','bbbb')
    mc.set('passwd:2','1111')
    time.sleep(1.0)  # increase to simulate an expensive operation
    bacc = acc
    acc = acc.decode()
    uname = acc.split(":")[0]
    passwd = acc.split(":")[1]
    print("username:%s" % uname)
    print("password:%s" % passwd)
    if(mc.get('user:1')==uname and mc.get('passwd:1')==passwd):
        print('user: %s login!!' % uname)
        return b'success'
    else:
        print('identity fail.QAQQAQQAQQAQQAQQAQQAQQAQQAQQAQQAQ')
        return b'fail'