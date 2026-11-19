import subprocess
from check_service import check_service


def test_check_service_success_with_env(monkeypatch, capsys):
    monkeypatch.setenv("BASE_URL", "http://127.0.0.1:9090")
    monkeypatch.setenv("EXPECTED_RELEASE", "release-test-99")
    monkeypatch.setenv("CHECK_TIMEOUT", "4.5")

    captured_call = {}

    def fake_run(cmd, capture_output, text, timeout):
        captured_call["cmd"] = cmd
        captured_call["capture_output"] = capture_output
        captured_call["text"] = text
        captured_call["timeout"] = timeout
        return subprocess.CompletedProcess(
            args=cmd,
            returncode=0,
            stdout="<h1>release-test-99</h1>",
            stderr="",
        )

    monkeypatch.setattr(subprocess, "run", fake_run)

    exit_code = check_service()
    out = capsys.readouterr().out

    assert exit_code == 0
    assert captured_call["cmd"] == ["curl", "-sS", "-f", "http://127.0.0.1:9090"]
    assert captured_call["capture_output"] is True
    assert captured_call["text"] is True
    assert captured_call["timeout"] == 4.5
    assert "[OK]" in out
    assert "release-test-99" in out


def test_check_service_wrong_release(monkeypatch, capsys):
    monkeypatch.setenv("BASE_URL", "http://127.0.0.1:8080")
    monkeypatch.setenv("EXPECTED_RELEASE", "devops_7-homework")
    monkeypatch.setenv("CHECK_TIMEOUT", "3")

    def fake_run(cmd, **kwargs):
        return subprocess.CompletedProcess(
            args=cmd,
            returncode=0,
            stdout="<h1>wrong-release</h1>",
            stderr="",
        )

    monkeypatch.setattr(subprocess, "run", fake_run)

    exit_code = check_service()
    out = capsys.readouterr().out

    assert exit_code == 1
    assert "[FAIL]" in out
    assert "devops_7-homework" in out


def test_check_service_curl_error(monkeypatch, capsys):
    monkeypatch.setenv("BASE_URL", "http://127.0.0.1:8080")
    monkeypatch.setenv("EXPECTED_RELEASE", "devops_7-homework")

    def fake_run(cmd, **kwargs):
        return subprocess.CompletedProcess(
            args=cmd,
            returncode=7,
            stdout="",
            stderr="curl: (7) Failed to connect to 127.0.0.1 port 8080",
        )

    monkeypatch.setattr(subprocess, "run", fake_run)

    exit_code = check_service()
    out = capsys.readouterr().out

    assert exit_code == 1
    assert "[FAIL]" in out
    assert "Failed to connect" in out


def test_check_service_timeout(monkeypatch, capsys):
    monkeypatch.setenv("BASE_URL", "http://127.0.0.1:8080")
    monkeypatch.setenv("EXPECTED_RELEASE", "devops_7-homework")
    monkeypatch.setenv("CHECK_TIMEOUT", "2")

    def fake_run(cmd, **kwargs):
        raise subprocess.TimeoutExpired(cmd=cmd, timeout=2.0)

    monkeypatch.setattr(subprocess, "run", fake_run)

    exit_code = check_service()
    out = capsys.readouterr().out

    assert exit_code == 2
    assert "[TIMEOUT]" in out
    assert "2.0" in out