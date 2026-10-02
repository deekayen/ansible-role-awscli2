# deekayen.awscli2

[![CI](https://github.com/deekayen/ansible-role-awscli2/actions/workflows/ci.yml/badge.svg)](https://github.com/deekayen/ansible-role-awscli2/actions/workflows/ci.yml) [![Ansible Galaxy](https://img.shields.io/badge/galaxy-deekayen.awscli2-blue.svg)](https://galaxy.ansible.com/ui/standalone/roles/deekayen/awscli2/) [![Project Status: Inactive – The project has reached a stable, usable state but is no longer being actively developed; support/maintenance will be provided as time allows.](https://www.repostatus.org/badges/latest/inactive.svg)](https://www.repostatus.org/#inactive) ![BSD 3-Clause license](https://img.shields.io/badge/license-BSD%203--Clause-blue)

An Ansible role that installs AWS CLI v2 on Linux from the official AWS installer bundle instead of `pip`.

The role downloads `awscli-exe-linux-<architecture>.zip` from `awscli.amazonaws.com`, unpacks it on the target, and runs the bundled `install` script. The CLI lands in `/usr/local/aws-cli`, with `aws` and `aws_completer` symlinked into `/usr/local/bin`. The architecture comes from `ansible_facts.architecture`, so the same play covers `x86_64` and `aarch64` hosts.

## Requirements

- ansible-core 2.15 or newer on the controller.
- Outbound HTTPS from the target host to `awscli.amazonaws.com`.
- Privilege escalation on the target. Run the play with `become: true`; the role installs `unzip` with the system package manager and writes to `/usr/local`.

## Supported platforms

From `meta/main.yml`, and each one runs through Molecule in CI:

| Platform | Versions |
| --- | --- |
| EL (Rocky Linux in CI) | 9, 10 |
| Amazon Linux | 2023 |
| Debian | 12 (bookworm), 13 (trixie) |
| Ubuntu | 22.04 (jammy), 24.04 (noble), 26.04 (resolute) |

## Installation

From Ansible Galaxy:

```bash
ansible-galaxy role install deekayen.awscli2
```

Or pin it in `requirements.yml`:

```yaml
---
roles:
  - name: deekayen.awscli2
    src: https://github.com/deekayen/ansible-role-awscli2.git
    scm: git
    version: main
```

```bash
ansible-galaxy role install -r requirements.yml
```

## Role variables

| Variable | Default | Description |
| --- | --- | --- |
| `executable_temp_dir` | `/tmp` | Absolute path where the installer zip is unpacked and executed. The role asserts that it starts with `/`. Use a different path on hardened hosts that mount `/tmp` with `noexec`. |

## Behavior

- The install task is guarded by `creates: /usr/local/bin/aws`. A host that already has AWS CLI v2 there is left alone, so the role installs but does not upgrade. To move to a newer release, remove `/usr/local/bin/aws` and `/usr/local/aws-cli` before running the role again.
- The unpacked installer stays in `{{ executable_temp_dir }}/aws` after the run. Its presence also short-circuits the download task on later runs.
- The role refreshes the apt or dnf cache on every run before installing `unzip`.

## Dependencies

None.

## Example playbook

```yaml
---
- name: Install AWS CLI v2.
  hosts: build_agents
  become: true

  vars:
    executable_temp_dir: /var/tmp

  roles:
    - deekayen.awscli2
```

## Development

CI runs on every push to `main` and every pull request (see `.github/workflows/ci.yml`):

1. Lint: `ansible-lint --profile production` and `flake8 molecule/`.
2. Molecule: converge, idempotence, and testinfra verification in Docker against each distribution in the table above.

To run the same checks locally with Docker available:

```bash
pip3 install ansible-core ansible-lint flake8 molecule "molecule-plugins[docker]" docker pytest-testinfra
ansible-lint --profile production
flake8 molecule/
MOLECULE_DISTRO=rockylinux9 molecule test
```

`MOLECULE_DISTRO` selects a `geerlingguy/docker-<distro>-ansible` image. The values CI uses are `rockylinux9`, `rockylinux10`, `amazonlinux2023`, `ubuntu2204`, `ubuntu2404`, `ubuntu2604`, `debian12`, and `debian13`. The testinfra checks in `molecule/default/tests/test_default.py` confirm that `unzip` is installed, `/usr/local/aws-cli` exists, the `/usr/local/bin` symlinks resolve, and `aws --version` reports `aws-cli/2.`.

### Repository layout

| Path | Purpose |
| --- | --- |
| `tasks/main.yml` | Package cache refresh, `unzip` install, download, and installer run. |
| `tasks/assert.yml` | Input validation, tagged `always`. |
| `defaults/main.yml` | The one user-facing variable. |
| `meta/main.yml` | Galaxy metadata and the supported platform list. |
| `molecule/default/` | Molecule scenario: `prepare.yml`, `converge.yml`, and testinfra tests. |
| `.github/workflows/` | `ci.yml` for lint and Molecule, `release.yml` for Galaxy import. |

## Releases

Pushing a git tag runs `.github/workflows/release.yml`, which imports the tagged commit into Ansible Galaxy as `deekayen.awscli2`. The import needs a `GALAXY_API_KEY` repository or organization secret.

## License

BSD 3-Clause. See [LICENSE](LICENSE).

## Author

[David Norman](https://github.com/deekayen). Sponsorship links are in [.github/FUNDING.yml](.github/FUNDING.yml).
