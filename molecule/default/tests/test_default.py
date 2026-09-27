"""Testinfra checks for the AWS CLI v2 role."""


def test_unzip_installed(host):
    assert host.package("unzip").is_installed


def test_install_tree(host):
    assert host.file("/usr/local/aws-cli").is_directory
    aws = host.file("/usr/local/aws-cli/v2/current/bin/aws")
    assert aws.exists
    assert aws.mode & 0o111


def test_bin_symlinks(host):
    for name in ("aws", "aws_completer"):
        link = host.file("/usr/local/bin/" + name)
        assert link.is_symlink
        assert link.linked_to.startswith("/usr/local/aws-cli/")


def test_aws_reports_v2(host):
    version = host.check_output("/usr/local/bin/aws --version")
    assert version.startswith("aws-cli/2.")
