import json
import socket
import hashlib


def send_msg(ip, port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    try:
        sock.sendall(message)
        response = sock.recv(1024)
        print "Received: {}".format(response)
    finally:
        sock.close()


def send_offer(ip, port, id, offer, price=1):
    d = {
        'id': id,
        'offer': offer,
        'price': price
    }
    msg = json.dumps(d)
    send_msg(ip, port, msg)
