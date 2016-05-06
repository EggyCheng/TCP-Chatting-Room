import argparse, random, socket, client_utils
from threading import Thread


def start_threads(listener, workers=4):
    t = (listener,)
    for i in range(workers):
        Thread(target=client_utils.accept_connections_forever, args=t).start()
        #call client_utils.accept_connections_forever(listener)


def client(address, cause_error=False):
    uname = input('usernmae:')
    passwd = input('password:')
    acc = uname + ":" + passwd

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(address)
    sock.sendall(acc.encode())
    sock.close()

if __name__ == '__main__':
    address = client_utils.parse_command_line('chatting room client')
    listener = client_utils.verify()
    start_threads(listener)
