# create list for 1000 peers
# read the .csv and assign msgId's to the peers with %1000
# somehow create a unique trader.py for every peer.
# somehow pass the assigned messages to the right trader.py
import csv
from udpsend import create_peer
from twisted.internet import reactor
import threading

PEER_AMOUNT = 100
allocated_msgs = [list() for x in range(PEER_AMOUNT)]


def get_orders():
    orders = []
    with open("orderlist.csv") as f:
        reader = csv.reader(f)
        for ind, row in enumerate(reader):
            if not row[0] == 'T':
                orders.append(row)
            if ind > 20:
                break
    print "Orderlist read."
    return orders


def allocate_msgs():
    orders = get_orders()
    for index, order in enumerate(orders):
        allocated_msgs[index % PEER_AMOUNT].append(order)
    print "Messages allocated."


def start_peer(index):
    print "Creating peer and sending messages."
    for message in allocated_msgs[index]:
        create_peer(str(index), message[4], message[5], message[0])
    return


def simulate():
    print "Starting simulation.."
    allocate_msgs()
    for i in range(PEER_AMOUNT):
        print "Attempting to start thread for peer" + str(i)
        threading.Thread(target=start_peer, args=(i,)).start()
        print "Started peer" + str(i)

simulate()