#   scripts/deploy.sh
#   deploy Containerlab topology defined in topology/

set -euo pipefail
containerlab deploy -t topology/topology.clab.yml