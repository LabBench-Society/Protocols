from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

from pathlib import Path


def get_default_ftp_root():
    # Resolve "Documents/ftp_server" in a cross-platform way
    documents = Path.home() / "Documents"
    ftp_root = documents / "ftp_server"

    # Ensure directory exists
    ftp_root.mkdir(parents=True, exist_ok=True)

    return ftp_root


def start_ftp_server(port=2121):
    root_dir = get_default_ftp_root()

    authorizer = DummyAuthorizer()

    # Anonymous user with full permissions
    authorizer.add_anonymous(str(root_dir), perm="elradfmw")

    handler = FTPHandler
    handler.authorizer = authorizer

    server = FTPServer(("127.0.0.1", port), handler)

    print("=" * 50)
    print("FTP SERVER STARTED")
    print("=" * 50)
    print(f"Address:        ftp://127.0.0.1:{port}")
    print(f"Root directory: {root_dir}")
    print("Permissions:    anonymous (full access)")
    print("")
    print("Uploaded files will appear here:")
    print(f"  {root_dir}")
    print("")
    print("Press CTRL+C (or stop the process) to stop the server.")
    print("=" * 50)

    server.serve_forever()


if __name__ == "__main__":
    start_ftp_server()