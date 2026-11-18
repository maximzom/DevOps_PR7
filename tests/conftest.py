import os
import subprocess
import sys
import urllib.error
import urllib.request
import pytest

if sys.platform == "win32":
    from testinfra.backend.docker import DockerBackend

    def _win_docker_run(self, command, *args, **kwargs):
        cmd = self.get_command(command, *args)
        docker_cmd = ["docker", "exec"]
        if getattr(self, "user", None):
            docker_cmd.extend(["-u", self.user])
        docker_cmd.extend([self.name, "/bin/sh", "-c", cmd])
        env = {**os.environ, "MSYS_NO_PATHCONV": "1"}
        proc = subprocess.run(docker_cmd, capture_output=True, env=env)
        return self.result(proc.returncode, cmd, proc.stdout, proc.stderr)

    DockerBackend.run = _win_docker_run


@pytest.fixture(scope="session")
def base_url() -> str:
    return os.getenv("BASE_URL", "http://127.0.0.1:8080").rstrip("/")


@pytest.fixture(scope="session")
def expected_release() -> str:
    return os.getenv("EXPECTED_RELEASE", "devops_7-homework")


@pytest.fixture(scope="session")
def http_timeout() -> float:
    return float(os.getenv("HTTP_TIMEOUT", "3.0"))


@pytest.fixture
def http_get(base_url: str, http_timeout: float):
    def _get(path: str) -> tuple[int, str]:
        url = f"{base_url}{path}"
        request = urllib.request.Request(url, method="GET")
        try:
            with urllib.request.urlopen(request, timeout=http_timeout) as response:
                body = response.read().decode("utf-8")
                return response.status, body
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            return exc.code, body

    return _get