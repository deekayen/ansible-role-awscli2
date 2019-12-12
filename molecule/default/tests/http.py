import os
import http.client
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_apache2_connection(host):
    print(host)
    conn = http.client.HTTPConnection(host, 80, timeout=5)
    conn.request("GET", "/")
    response = conn.getresponse()

    assert response.status == "200"
