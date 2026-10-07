#   scripts/destroy.sh
#   tear down Containerlab topology

set -euo pipefail
containerlab destroy -t topology/topology.clab.yml --cleanup