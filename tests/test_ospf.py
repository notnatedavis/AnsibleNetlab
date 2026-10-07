#   tests/test_ospf.py
#   OSPF adjacency and route-table assertions

def test_ospf_neighbors_full(lab) :
    # r1 and r2 must reach the Full state
    r1 = lab.nodes["r1"]
    output = r1.cmd("vtysh -c 'show ip ospf neighbor'")
    assert "Full" in output

def test_ospf_route_present(lab) :
    # r1 must learn the remote LAN via OSPF
    r1 = lab.nodes["r1"]
    output = r1.cmd("vtysh -c 'show ip route ospf'")
    assert "10.0.2.0/24" in output