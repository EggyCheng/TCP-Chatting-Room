import argparse, random, socket, client_utils
from threading import Thread
from multiprocessing.pool import ThreadPool


def start_threads(sock,uname, workers=2):
    s = (sock,uname)
    for i in range(workers):
        Thread(target=client_utils.accept_connections_forever, args=s).start()
       #call client_utils.accept_connections_forever(sock)
        Thread(target=client_utils.typecmd, args=s).start()
        #call client_utils.typecmd()


if __name__ == '__main__':
    address = client_utils.parse_command_line('chatting room client')
    sock,uname = client_utils.v_request()
    if sock is not None:
        start_threads(sock,uname)

