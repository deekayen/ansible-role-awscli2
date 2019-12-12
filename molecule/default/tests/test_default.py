import os
import http.client
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_apache2_installed(host):
    assert host.package("apache2").is_installed


def test_apache2_etc(host):
    assert host.file("/etc/apache2").is_directory


def test_apache2_logs(host):
    for filename in (
        ("/var/log/apache2/access.log"),
        ("/var/log/apache2/error.log"),
    ):
        log = host.file(filename)
        assert log.exists
        assert log.is_file


def test_apache2_listener(host):
    assert host.socket("tcp://0.0.0.0:80").is_listening


def test_apache2_service(host):
    service = host.service("apache2")

    assert service.is_enabled
    assert service.is_running


def test_apache2_port(host):
    assert host.port(80).is_reachable


def test_apache2_connection(host):
    connection = http.client.HTTPConnection(host.name, 80, timeout=5)
    connection.request("GET", "/")
    response = connection.getresponse()
    code = response.status()

    assert code == "200"
