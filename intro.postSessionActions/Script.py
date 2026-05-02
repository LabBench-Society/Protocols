from ftplib import FTP
from pathlib import Path
import tempfile


class AnonymousFTPClient:
    def __init__(self, host: str, port: int = 21, timeout: int = 30):
        self.host = host
        self.port = port
        self.timeout = timeout

    def upload_file(
        self,
        local_dir: str,
        local_filename: str,
        remote_dir: str | None = None,
        remote_filename: str | None = None
    ):
        local_path = Path(local_dir) / local_filename

        if not local_path.is_file():
            raise FileNotFoundError(f"File not found: {local_path}")

        if remote_filename is None:
            remote_filename = local_filename

        with FTP() as ftp:
            ftp.connect(self.host, self.port, timeout=self.timeout)
            ftp.login()

            if remote_dir is not None:
                ftp.cwd(remote_dir)

            with local_path.open("rb") as f:
                ftp.storbinary(f"STOR {remote_filename}", f)

        print(f"Uploaded '{local_filename}' to ftp://{self.host}:{self.port}/{remote_filename}")


def CreateUploader(context):
    return AnonymousFTPClient("127.0.0.1", port=2121)


def main():
    # Create a temporary directory
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)

        # Create a dummy file
        filename = "test_upload.txt"
        file_path = tmp_path / filename

        content = "Hello FTP 👋\nThis is a test file.\n"
        file_path.write_text(content, encoding="utf-8")

        print(f"Created test file: {file_path}")

        # Upload it
        client = AnonymousFTPClient("127.0.0.1", port=2121)

        client.upload_file(
            local_dir=str(tmp_path),
            local_filename=filename
        )

        print("Done.")


if __name__ == "__main__":
    main()