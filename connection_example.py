import socket
import threading
import SocketServer

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        data = self.request.recv(1024)
        cur_thread = threading.current_thread()
        response = "{}: {}".format(cur_thread.name, data)
        self.request.sendall(response)


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass


def client(ip, port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    try:
        sock.sendall(message)
        response = sock.recv(1024)
        print "Received: {}".format(response)
    finally:
        sock.close()


def create_server(host, port):
    server = ThreadedTCPServer((host, port), ThreadedTCPRequestHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    print "Server loop running in thread:", server_thread.name
    return server

if __name__ == "__main__":
    HOST, PORT = "localhost", 0

    server = create_server(HOST, PORT)
    server2 = create_server(HOST, PORT)

    ip, port = server.server_address
    ip, port2 = server2.server_address

    client(ip, port, "Hi world")
    client(ip, port2, "Hullo world")
    client(ip, port, "Sup world")
    client(ip, port2, "Goodbye world")

    server.shutdown()
    server2.shutdown()
