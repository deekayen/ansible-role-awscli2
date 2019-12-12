import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_httpd_installed(host):
    apache = host.package("apache2")

    assert apache.is_installed


def test_httpd_listener(host):
    listener = host.socket("tcp://0.0.0.0:80")

    assert listener.is_listening


def test_httpd_service(host):
    service = host.service("apache2")

    assert service.is_enabled
    assert service.is_running


def test_httpd_etc(host):
    assert host.file("/etc/apache2").is_directory


def test_httpd_logs(host):
    for filename in (
        ("/var/log/apache2/access.log"),
        ("/var/log/apache2/error.log"),
    ):
        log = host.file(filename)
        assert log.exists
        assert log.is_file
