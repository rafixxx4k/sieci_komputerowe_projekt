import socket
import _thread

PORT = 1100
HOST = "127.0.0.1"


def echo(conn):
    with conn:
        while True:
            msg = conn.recv(1024)
            if not msg:
                break
            print('msg: ', msg)
            conn.send(msg)
        conn.close()


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
    soc.bind((HOST, PORT))
    soc.listen()
    while True:
        conn, addr = soc.accept()
        print('connected by:', addr)
        _thread.start_new_thread(echo, (conn,))
    soc.close()
