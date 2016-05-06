import argparse, random, socket, client_utils
from threading import Thread


def start_threads(sock, workers=2):
    s = (sock,)
    for i in range(workers):
        #Thread(target=client_utils.accept_connections_forever, args=s).start()
        #call client_utils.accept_connections_forever(sock)
        Thread(target=client_utils.typecmd, args=s).start()
        #call client_utils.typecmd()


if __name__ == '__main__':
    address = client_utils.parse_command_line('chatting room client')
    sock = client_utils.v_request()
    if sock is not None:
        start_threads(sock)
