AWS CLI v2
=========

[![CI](https://github.com/deekayen/ansible-role-awscli2/workflows/CI/badge.svg?branch=main)](https://github.com/deekayen/ansible-role-awscli2/actions?query=workflow%3ACI) [![Project Status: Inactive – The project has reached a stable, usable state but is no longer being actively developed; support/maintenance will be provided as time allows.](https://www.repostatus.org/badges/latest/inactive.svg)](https://www.repostatus.org/#inactive) ![BSD 3-Clause license](https://img.shields.io/badge/license-BSD%203--Clause-blue) ![Linux platform](https://img.shields.io/badge/platform-linux-lightgrey)

Install AWS CLI v2 using the official install binary instead of using `pip`.

Requirements
------------
1. Outbound internet connection.
2. unzip 

Role Variables
--------------

| variable | hints |
| ---      | ---   |
| executable_temp_dir | download location for the installer, must be executable, don't use /tmp on hardened OSes|

Dependencies
------------

None.

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables
passed in as parameters) is always nice for users too:

    - hosts: servers
      roles:
         - deekayen.awscli2

License
-------

BSD

Author Information
------------------

David Norman
https://github.com/sponsors/deekayen
