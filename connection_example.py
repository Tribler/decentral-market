import datetime

from trade_server import create_server
from trade_client import send_offer

if __name__ == "__main__":
    HOST, PORT = "localhost", 0

    server_list = [create_server(HOST, PORT) for x in range(8)]
    address_list = [server.server_address for server in server_list]
    print address_list

    offer = {
            'type': 'offer',
            'timestamp': datetime.datetime.now().isoformat(),
            'id': 1,
            'quantity': 20,
            'price': 101,
    }

    try:
        ip, port = address_list[0]
        send_offer(ip, port, offer)
        send_offer(ip, port, offer)
        while True:
            pass
    except KeyboardInterrupt:
        map(lambda server: server.shutdown(), server_list)
