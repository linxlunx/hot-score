from app import app
import argparse

if __name__ == '__main__':
    argparse = argparse.ArgumentParser()
    argparse.add_argument('-s', '--server-host', type=str, default='127.0.0.1', help='Server Host')
    argparse.add_argument('-p', '--server-port', type=int, default=5000, help='Server Port')
    args = argparse.parse_args()
    app.run(host=args.server_host, port=args.server_port)
