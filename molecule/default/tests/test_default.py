import os
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_awscli2_bin(host):
    assert host.file("/usr/local/bin").is_directory
    assert host.file("/usr/local/aws-cli").is_directory
    assert host.file("/usr/local/bin/aws").is_symlink
    assert host.file("/usr/local/bin/aws_completer").is_symlink
    assert host.file("/usr/local/aws-cli/v2/current/bin/aws").is_file
