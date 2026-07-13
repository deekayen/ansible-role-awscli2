# Changelog

All notable changes to this role are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Changed

- Modernized CI/testing: pinned toolchain versions, current GitHub Actions
  action versions, `amazonlinux2023` (required) and `debian13` in the
  molecule matrix (replacing EOL `centos7`/`centos8`/`debian9`/`debian10`),
  fixed `/sys/fs/cgroup` mount from `ro` to `rw` (required on cgroup v2
  hosts), removed play-level `become: true` from the test scenario
  (breaks amazonlinux2023's minimal PAM stack; the docker connection
  already execs as root).
- Added `meta/argument_specs.yml` for variable validation.
- Converted all task module references to FQCN
  (`ansible.builtin.*`) per current ansible-lint standards.
- Fixed `ansible_distribution_major_version` comparisons to cast with
  `| int` - comparing the raw string against an int now fails under
  current ansible-core's stricter type handling.
