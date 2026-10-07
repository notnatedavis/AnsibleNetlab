#   tests/test_vlan_isolation.py
#   Negative test: hosts on different VLANs must not reach each other
#      without inter-VLAN routing configured

def test_vlan_isolation(lab) :
    host1 = lab.nodes["host1"]
    result = host1.cmd("ping -c 1 10.0.20.10")
    assert "100% packet loss" in result