### Installation

1. Install ansible (https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html) on your system, and make sure the binaries are available (`which ansible` and `which ansible-playbook` should return something)
1. Set `HAW_USER` and `HAW_PASSWORD` as environment variables
1. Make sure that there is an entry for `pnskss.informatik.haw-hamburg.de` in your `/etc/hosts` file pointing to the container harbor
1. Run `python create_inventory.py`. This generates the *inventory* file, the XML File for Draw.io, and a file with a list of server hostnames, called `servers` (You can ignore that one)

### Ansible Execution

Run the scripts in the following order (Make sure that on your harbor there is ONLY the servers for the pns1 project available and NOTHING else! Else nothing will work.)

Make sure your at the project root directory.

1. Run `ansible-playbook -i inventory playbooks/setup.yml`
1. Run `ansible-playbook -i inventory playbooks/routing.yml`. (This can be only run once, every successive run will result in an error, but nothing bad will happen. The routes already exist and can only be added once)
1. Run `ansible-playbook --skip-tags flush -i inventory playbooks/firewall.yml`
