from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

def start_ftp_server(root_dir=".", port=2121):
    authorizer = DummyAuthorizer()
    
    # Anonymous user with full permissions
    authorizer.add_anonymous(root_dir, perm="elradfmw")

    handler = FTPHandler
    handler.authorizer = authorizer

    server = FTPServer(("127.0.0.1", port), handler)
    print(f"FTP server running on ftp://127.0.0.1:{port}")
    server.serve_forever()


if __name__ == "__main__":
    start_ftp_server()