import json
import threading
import socket
import SocketServer

from orderbook import asks, bids, match_incoming_ask, trade_offer


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
            response_dict = handle_ask(data)
        elif data['type'] == 'bid':
            response_dict = handle_bid(data)
        elif data['type'] == 'greeting':
            response_dict = handle_greeting(data)
        elif data['type'] == 'trade':
            response_dict = handle_trade(data)
        elif data['type'] == 'confirm':
            response_dict = handle_confirm(data)
        return json.dumps(response_dict), data['type']
    except ValueError, e:
        print e.message
        return e.message


def handle_ask(ask):
    bid = match_incoming_ask(ask)
    if bid:
        return trade_offer(ask, bid)
    else:
        asks.append(ask)
        return 'Your ask got processed!'


def handle_bid(bid):
    bids.append(bid)


def handle_trade(trade):
    return 'Trade succesful!'


def handle_confirm(confirm):
    return 'Trade succesful!'


def handle_greeting(greeting):
    return 'Hi!'
