import argparse, random, socket, client_utils
from threading import Thread


def start_threads(sock,uname, workers=2):
    s = (sock,uname)
    th1 = Thread(target=client_utils.accept_connections_forever, args=s)  
    th2 = Thread(target=client_utils.typecmd, args=s)  
    threads = [th1, th2]
    for t in threads:
        t.setDaemon(True)  
        t.start()
    t.join()
if __name__ == '__main__':
    address = client_utils.parse_command_line('chatting room client')
    sock,uname = client_utils.v_request()
    if sock is not None:
        start_threads(sock,uname)

