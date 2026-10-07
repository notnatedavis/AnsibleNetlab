#   tests/test_reachability.py
#   End-to-end reachability between hosts

def test_host1_to_host2(lab):
    # ping across routed core must succeed with 0% loss
    host1 = lab.nodes["host1"]
    result = host1.cmd("ping -c 3 10.0.2.10")
    assert "0% packet loss" in result