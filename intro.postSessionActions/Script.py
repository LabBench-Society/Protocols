from ftplib import FTP
from pathlib import Path
import tempfile
from typing import Optional


class AnonymousFTPClient:
    def __init__(self, context, host: str, port: int = 21, timeout: int = 30):
        self.context = context
        self.host = host
        self.port = port
        self.timeout = timeout

    def upload_file(
        self,
        local_filename: str,
        remote_dir: Optional[str] = None,
        remote_filename: Optional[str] = None
    ):
        local_path = Path(self.context.ExportLocation) / local_filename

        if not local_path.is_file():
            raise FileNotFoundError(f"File not found: {local_path}")

        if remote_filename is None:
            remote_filename = local_filename

        with FTP() as ftp:
            ftp.connect(self.host, self.port, timeout=self.timeout)
            ftp.login()

            # Helps avoid passive/active mode issues in some environments
            ftp.set_pasv(True)

            if remote_dir is not None:
                ftp.cwd(remote_dir)

            with open(str(local_path), "rb") as f:  # safer for IronPython
                ftp.storbinary(f"STOR {remote_filename}", f)

        print(f"Uploaded '{local_filename}' to ftp://{self.host}:{self.port}/{remote_filename}")
        return True


def CreateUploader(context):
    return AnonymousFTPClient(context, "127.0.0.1", port=2121)


class DummyContext:
    def __init__(self, directory):
        self.ExportLocation = directory


def main():
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)

        filename = "test_upload.txt"
        file_path = tmp_path / filename

        content = "Hello FTP 👋\nThis is a test file.\n"
        file_path.write_text(content, encoding="utf-8")

        print(f"Created test file: {file_path}")

        context = DummyContext(tmp_path)
        client = AnonymousFTPClient(context, "127.0.0.1", port=2121)

        client.upload_file(filename)

        print("Done.")


if __name__ == "__main__":
    main()