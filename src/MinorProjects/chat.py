import socket
import argparse
import threading
import time

running = True


def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip


def start_server(address, sock_mode):
    global running
    server_ok = False
    err_code = 0

    server_ip = get_host_ip()
    sock = socket.socket(*sock_mode)
    while running and not server_ok:
        try:
            sock.bind((server_ip, address[1]))
            print('Server started at {}:{}'.format(server_ip, address[1]))
            server_ok = True
        except OSError as e:
            if e.args[0] != err_code:
                print(e)
                err_code = e.args[0]
            time.sleep(1)

    try:
        while running:
            data, addr = sock.recvfrom(2048)
            print(addr, data.decode('utf-8'), sep=': ')
    except (KeyboardInterrupt, EOFError):
        pass
    finally:
        sock.close()


def start_client(address, sock_mode):
    global running
    sock = socket.socket(*sock_mode)

    try:
        while running:
            time.sleep(0.01)
            msg = input('> ')
            sock.sendto(bytes(msg, 'utf-8'), address)
    except (KeyboardInterrupt, EOFError):
        running = False
        sock.sendto(b'bye', address)
    finally:
        sock.close()


def parse_args():
    parser = argparse.ArgumentParser(description='Python p2p chat by Charles Xu')
    parser.add_argument('-a', '--address', default='127.0.0.1', help='target IP address')
    parser.add_argument('-p', '--port', default=8899, type=int, help='remote port')
    args = parser.parse_args()
    address = (args.address, args.port)
    sock_mode = (socket.AF_INET, socket.SOCK_DGRAM)
    return address, sock_mode


def main():
    address, sock_mode = parse_args()
    print('Connect to:')
    print(address, sock_mode, sep='\n', end='\n\n')
    thread = threading.Thread(target=start_server, args=(address, sock_mode))
    thread.start()
    start_client(address, sock_mode)
    print('bye')


if __name__ == '__main__':
    main()
