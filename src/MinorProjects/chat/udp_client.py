import sys
import socket


if len(sys.argv) != 4:
    print('Usage: python udp_client.py host port message')
    exit()

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(bytes(sys.argv[3], 'utf-8'), (sys.argv[1], int(sys.argv[2])))
sock.close()

