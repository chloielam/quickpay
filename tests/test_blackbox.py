import json
import os
import socket
import subprocess
import tempfile
import time
import unittest
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


ROOT_DIR = Path(__file__).resolve().parents[1]


def find_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


class QuickPayBlackBoxTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.temp_dir = tempfile.TemporaryDirectory()
        cls.port = find_free_port()
        cls.base_url = f"http://127.0.0.1:{cls.port}"
        cls.user_id_counter = 1000

        env = os.environ.copy()
        env["QUICKPAY_DB_PATH"] = str(Path(cls.temp_dir.name) / "quickpay-test.db")

        cls.server = subprocess.Popen(
            [
                str(ROOT_DIR / "venv" / "bin" / "python"),
                "-m",
                "uvicorn",
                "app.main:app",
                "--host",
                "127.0.0.1",
                "--port",
                str(cls.port),
            ],
            cwd=ROOT_DIR,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        cls._wait_for_server()

    @classmethod
    def tearDownClass(cls) -> None:
        if hasattr(cls, "server"):
            cls.server.terminate()
            try:
                cls.server.wait(timeout=5)
            except subprocess.TimeoutExpired:
                cls.server.kill()
                cls.server.wait(timeout=5)
        if hasattr(cls, "temp_dir"):
            cls.temp_dir.cleanup()

    @classmethod
    def _wait_for_server(cls) -> None:
        deadline = time.time() + 10
        last_error = None
        while time.time() < deadline:
            if cls.server.poll() is not None:
                stdout, stderr = cls.server.communicate(timeout=1)
                raise RuntimeError(
                    "Uvicorn exited before startup.\n"
                    f"stdout:\n{stdout}\n"
                    f"stderr:\n{stderr}"
                )
            try:
                response = cls.request("GET", "/")
                if response["status"] == 200:
                    return
            except Exception as exc:  # noqa: BLE001
                last_error = exc
                time.sleep(0.1)
        raise RuntimeError(f"Server did not become ready: {last_error}")

    @classmethod
    def request(cls, method: str, path: str, payload: dict | None = None) -> dict:
        data = None
        headers = {}
        if payload is not None:
            data = json.dumps(payload).encode("utf-8")
            headers["Content-Type"] = "application/json"
        req = Request(f"{cls.base_url}{path}", data=data, headers=headers, method=method)
        try:
            with urlopen(req, timeout=5) as response:
                body = response.read().decode("utf-8")
                return {
                    "status": response.status,
                    "json": json.loads(body) if body else None,
                }
        except HTTPError as exc:
            body = exc.read().decode("utf-8")
            return {
                "status": exc.code,
                "json": json.loads(body) if body else None,
            }
        except URLError as exc:
            raise RuntimeError(f"Request failed: {exc}") from exc