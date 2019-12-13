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


def test_apache2_config(host):
    for filename in (
        ("/etc/apache2/apache2.conf"),
        ("/etc/apache2/sites-available/000-default.conf"),
    ):
        config = host.file(filename)
        assert config.exists
        assert config.is_file
        assert config.user == "root"
        assert config.uid == 0
        assert config.mode == 0o644


def test_apache2_listener(host):
    assert host.socket("tcp://0.0.0.0:80").is_listening


def test_apache2_service(host):
    service = host.service("apache2")

    assert service.is_enabled
    assert service.is_running


def test_apache2_port(host):
    ansible_vars = host.ansible.get_variables()
    addr = host.addr(ansible_vars["inventory_hostname"])

    assert addr.port(80).is_reachable


def test_apache2_connection(host):
    ansible_vars = host.ansible.get_variables()
    addr = host.addr(ansible_vars["inventory_hostname"])
    connection = http.client.HTTPConnection(addr.name, 80, timeout=5)
    connection.request("GET", "/")
    response = connection.getresponse()
    code = response.status

    assert code == 301
