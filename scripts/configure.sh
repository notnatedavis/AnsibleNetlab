#   scripts/configure.sh
#   run Ansible playbook against running lab

set -euo pipefail
ansible-playbook -i ansible/inventory.yml ansible/configure.yml