import re
import random
import json
from time import sleep
import redis

def get_route(respond):
    route = re.match(r'GET(.*?)[A-Z]', respond).group(1)
    return route.strip()

# least connections algorithm
def find_server(servers, connections_count):
    return min(connections_count, key=lambda host: connections_count[host])

class Handler:
    def __init__(self, conn, addr, redis_servers, connections_count):
        self.conn = conn
        self.addr = addr
        self.redis_servers = redis_servers
        self.connections_count = connections_count 

        self.handle()

    def handle(self):
        print(f"Receive connection from {self.addr}")
        with self.conn:
            data = self.conn.recv(1024)
            route = get_route(data.decode())

            key = route.split('/')[1]
            if key.startswith('favicon'):
                print("--> favicon socket")
                return self.conn.send(data)

            self.get_client()
            sleep(3) # imaginary delay
            message = self.display() if not key else self.display_item(key)

            self.conn.send(message.encode())

        print(f"after {self.addr}", self.connections_count)

    def get_client(self):
        redis_server = find_server(self.redis_servers, self.connections_count)
        host, port = redis_server.split(':')
        port = int(port)

        self.connections_count[redis_server] += 1
        print(self.connections_count)

        self.redis_server = redis_server
        self.redis_client = redis.Redis(host=host, port=port, socket_timeout=5)

    def display(self):
        disp = (
            "Append the key to the path i.e localhost:port/key\n\n"
            "Here are the keys:\n"
        )
        keys = self.redis_client.keys("*")
        if not keys:
            disp += "No keys found!\n"
        else:
            for key in keys:
                key = key.decode()
                disp += f'\t{key}\n'

        self.connections_count[self.redis_server] -= 1
        return disp

    def display_item(self, key):
        data = self.redis_client.hgetall(key)
        if not data: disp = f"{key} not existed!"
        else:
            data = {k.decode(): v.decode() for k,v in data.items()}
            disp = json.dumps(data, indent=2)

        self.connections_count[self.redis_server] -= 1
        return disp
