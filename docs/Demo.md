# Demo

A short, repeatable walkthrough of the AnsibleNetlab project suitable for a
portfolio page or an interview. Each step lists the exact command and the
evidence to capture.

## Prerequisites

- Docker, Containerlab, Ansible, Python 3.11+
- `pip install -r requirements.txt`
- `containerlab version` and `ansible --version` both succeed

## 1. Show the topology as code

```bash
cat topology/topology.clab.yml
```

## 2. Deploy the lab

```bash
./scripts/deploy.sh
```

Expected output highlights:

- `Containerlab` creates `clab-ccna-lab-r1`, `-r2`, `-host1`, `-host2`
- Three veth pairs appear: `r1 ↔ r2`, `r1 ↔ host1`, `r2 ↔ host2`
- The summary table lists every node as `running`

## 3. Push configuration with Ansible

```bash
./scripts/configure.sh
```

## 4. Verify the network with pytest

```bash
./scripts/test.sh
```

The suite (driven by `pytest-clab`) proves:

- `test_ospf.py` — OSPF neighbor reaches **Full** and the remote LAN is learned
- `test_reachability.py` — `host1` can ping `host2` with **0% packet loss**
- `test_vlan_isolation.py` — a negative test: an unrouted VLAN address is
  unreachable (100% loss)

All three passing is the demo’s headline evidence.

## 5. Interactive inspection

```bash
docker exec -it clab-ccna-lab-r1 vtysh
```

Inside vtysh:

```
show ip ospf neighbor
show ip route ospf
show interface brief
```

## 6. Failure scenario — prove the test suite catches regressions

In one terminal, start a continuous ping:

```bash
docker exec -it clab-ccna-lab-host1 ping 10.0.2.10
```

In another, shut the backbone link:

```bash
docker exec -it clab-ccna-lab-r1 ip link set eth1 down
```

Observe:

- The ping stops returning replies
- `show ip ospf neighbor` shows the adjacency drops
- Re-running `./scripts/test.sh` **fails** on `test_reachability`

Restore the link:

```bash
docker exec -it clab-ccna-lab-r1 ip link set eth1 up
```

Wait for OSPF to reconverge, re-run the suite — **all tests pass again**.

## 7. Tear down

```bash
./scripts/destroy.sh
```