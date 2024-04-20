import socket
from threading import Thread
from multiprocessing import Process, Manager

from handle import Handler

# create a socket for the load balancer
HOST = '127.0.0.1'
PORT = 1310

s = socket.socket()

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s.bind((HOST, PORT))
s.listen()

print(f'Load balancer listening on {HOST}:{PORT}')

# main loop
if __name__ == '__main__':
    redis_servers = [
        '127.0.0.1:1111',
        '127.0.0.1:2222',
        '127.0.0.1:3333',
    ]
    connections_count = {server : 0 for server in redis_servers}

    while True:
        try:
            conn, addr = s.accept()
            Thread(target=Handler, args=(
                conn, addr, redis_servers, connections_count
            ), daemon=True).start()
        except Exception as e:
            print(f'Unexpected error: {e}')
        except KeyboardInterrupt:
            s.shutdown(socket.SHUT_RDWR)
            s.close()
            break
