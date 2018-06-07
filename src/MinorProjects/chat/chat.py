from __future__ import print_function, unicode_literals, division
import socket
import argparse
import threading
import time
import select


def get_host_ip(address=('8.8.8.8', 80)):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(address)
        ip = sock.getsockname()[0]
    finally:
        sock.close()
    return ip


class UDPServer(threading.Thread):
    """docstring for Server"""

    def __init__(
        self, address=('127.0.0.1', 54321),
        sock_mode=(socket.AF_INET, socket.SOCK_DGRAM),
        show_msg=print,
        buffer_size=4096,
    ):
        super(UDPServer, self).__init__(name='UDPServer')
        if address[0] != '127.0.0.1':
            address = get_host_ip(), address[1]
        self.address = address
        self.sock_mode = sock_mode
        self.show_msg = show_msg
        self.buffer_size = buffer_size
        self.sock = socket.socket(*self.sock_mode)
        self.sock.setblocking(False)

        self.running_status = True

        self.bind()

    def __del__(self):
        self.stop()

    def stop(self):
        self.running_status = False
        self.sock.close()

    def bind(self):
        err_code = 0
        server_ok = False

        while self.running_status and not server_ok:
            try:
                self.sock.bind(self.address)
                server_ok = True
                self.show_msg('Server started at {}:{}'.format(*self.address))
            except OSError as e:
                if e.args[0] != err_code:
                    self.show_msg(e)
                    err_code = e.args[0]
                time.sleep(1)

    def run(self):
        try:
            while self.running_status:
                try:
                    data, addr = self.recv()
                except OSError as e:
                    self.show_msg(e)
                if data is not None:
                    self.enqueue(addr, data.decode('utf-8'))
        except (KeyboardInterrupt, EOFError):
            pass

    def recv(self):
        ready = select.select((self.sock,), (), (), 0.1)
        data, addr = None, ()
        if ready[0]:
            data, addr = self.sock.recvfrom(self.buffer_size)
        return data, addr

    def enqueue(self, *data):
        print(data)


class UDPClient(object):
    def __init__(self, sock_mode=(socket.AF_INET, socket.SOCK_DGRAM)):
        self.sock_mode = sock_mode
        self.sock = socket.socket(*sock_mode)

    def sendto(self, address, msg):
        self.sock.sendto(bytes(msg, 'utf-8'), address)

    def __del__(self):
        self.sock.close()


def print_loop(address):
    client = UDPClient()
    running_status = True

    try:
        while running_status:
            time.sleep(0.01)
            msg = input('> ')
            client.sendto(address, msg)
    except (KeyboardInterrupt, EOFError):
        running_status = False



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
    thread = UDPServer(address, sock_mode)
    thread.start()
    print_loop(address)
    thread.stop()
    print('bye')


if __name__ == '__main__':
    main()
