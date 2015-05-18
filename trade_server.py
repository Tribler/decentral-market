import json
import threading
import socket
import SocketServer

from orderbook import asks, bids, match_incoming_ask, match_incoming_bid


class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        try:
            while True:
                data = self.request.recv(1024)
                response = ''

                if data:
                    handled_data, data_type = handle_data(data)
                    if handled_data:
                        response = handled_data

                self.request.sendall(response)

                if data:
                    break

        except socket.error:
            # Surpress errno 13 Broken Pipe
            pass


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass


def create_server(host="localhost", port=0):
    server = ThreadedTCPServer((host, port), ThreadedTCPRequestHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    return server


def handle_data(data):
    try:
        data = json.loads(data)
        if data['type'] == 'ask':
            return handle_ask(data), 'ask'
        elif data['type'] == 'bid':
            return handle_bid(data), 'bid'
        elif data['type'] == 'greeting':
            return handle_greeting(data), 'greeting'
    except ValueError, e:
        print e.message
        return e.message


def handle_ask(ask):
    own_bid = match_incoming_ask(ask)
    if own_bid:
        return ''
    else:
        asks.append(ask)
        print asks
        return ''


def handle_bid(bid):
    bids.append(bid)


def handle_greeting(greeting):
    return 'Hi!'
