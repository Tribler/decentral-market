from trade_server import create_server

if __name__ == "__main__":
    HOST, PORT = "localhost", 0

    server_list = [create_server(HOST, PORT) for x in range(8)]
    address_list = [server.server_address for server in server_list]

    print address_list
    try:
        while True:
            pass
    except KeyboardInterrupt:
        map(lambda server: server.shutdown(), server_list)
