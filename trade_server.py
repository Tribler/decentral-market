import threading
import SocketServer

messages = []

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        while True:
            data = self.request.recv(1024)
            if data:
                messages.append(data)
            print messages
            cur_thread = threading.current_thread()
            response = "{}: {}".format(cur_thread.name, data)
            self.request.sendall(response)


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass


def create_server(host="localhost", port=0):
    server = ThreadedTCPServer((host, port), ThreadedTCPRequestHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    return server
