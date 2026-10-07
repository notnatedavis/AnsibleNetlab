#   tests/conftest.py
#   session-scoped fixture that manages Containerlab lifecycle
#   deploys the topology, runs Ansible to push configs, tears down after

import subprocess
import pytest

@pytest.fixture(scope="session")
def lab(clab) :
    # deploy topology once per session & tear down after
    lab = clab("topology/topology.clab.yml")

    # push FRR + host config before any test runs
    subprocess.run(
        [
            "ansible-playbook",
            "-i", "ansible/inventory.yml",
            "ansible/configure.yml",
        ],
        check=True,
    )

    return lab