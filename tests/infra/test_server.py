import os
import pytest


@pytest.mark.parametrize(
    "file_path",
    [
        "/etc/nginx/nginx.conf",
        "/usr/share/nginx/html/index.html",
        "/usr/share/nginx/html/health.json",
    ],
)
def test_required_files_exist(host, file_path: str):
    target = host.file(file_path)
    assert target.exists
    assert target.is_file


def test_nginx_configuration(host):
    result = host.run("nginx -t")
    assert result.rc == 0, result.stderr


def test_release_content(host):
    expected_release = os.getenv("EXPECTED_RELEASE", "devops_7-homework")
    page = host.file("/usr/share/nginx/html/index.html")
    assert page.is_file
    assert page.contains(expected_release)