# AnsibleNetlab

A Containerlab-based CCNA network lab built as code. Defines the network topology declaratively in a Containerlab YAML file. Deploys the topology as Docker containers connected by virtual Ethernet links. Configures the devices automatically with Ansible and Jinja2 templates. Verifies the network with automated tests using pytest.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Project-Structure](#Project-Structure)
- [Additional-Information](#Additional-Info)

## Introduction

The core of the project is `topology.clab.yml`. This file describes the entire lab: routers, hosts, container images, and links. For example, a minimal CCNA-style lab might define two FRR routers and two Alpine hosts :

- `r1` and `r2` use the FRRouting container image and act as routers
- `host1` and `host2` use Alpine and act as end hosts
- Links create virtual Ethernet pairs between containers, such as `r1:eth1` to `r2:eth1`

Running `containerlab deploy -t topology.clab.yml` causes Containerlab to :

- Start each node as a Docker container
- Create the veth links between containers
- Attach containers to the correct virtual networks

The result is a running network lab made of lightweight containers. FRR containers provide routing protocols such as OSPF. Alpine containers provide simple Linux hosts for ping and reachability tests. For VLAN labs, the topology can be extended with a Linux bridge acting as a switch, or by using VLAN sub-interfaces such as `eth1.10` and `eth1.20` on FRR routers to simulate router-on-a-stick.

Once containers are running, they need configurations. The project uses Ansible with Jinja2 templates to generate FRR configuration files dynamically.

After deployment and configuration, pytest verifies that the network actually works. The `pytest-clab` plugin manages the Containerlab lifecycle, so tests can deploy a fresh lab, wait for nodes to be ready, run assertions, and tear everything down afterward.

## Features

- Declarative topology via `topology/topology.clab.yml`
- FRR routers with OSPF area 0 and point-to-point adjacency
- Alpine end hosts for ping-based reachability tests
- Ansible + Jinja2 configuration automation
- pytest test suite covering OSPF, reachability, and VLAN isolation
- One-command deploy / configure / test / destroy workflow
- GitHub Actions CI that runs the full pipeline on every push

## Project-Structure

```bash
AnsibleNetlab/
├── ansible/
│   ├── group_vars/
│   │   └── all.yml
│   │
│   ├── host_vars/
│   │   ├── host1.yml
│   │   ├── host2.yml
│   │   ├── r1.yml
│   │   └── r2.yml
│   │
│   ├── templates/
│   │       ├── frr.conf.j2
│   │       └── host-interfaces.j2
│   │
│   ├── configure.yml
│   └── inventory.yml
│
├── docs/
│   ├── Demo.md
│   ├── ToDo.md
│   └── Troubleshooting.md
│
├── scripts/
│   ├── configure.sh
│   ├── deploy.sh
│   ├── destroy.sh
│   └── test.sh
│
├── tests/
│   ├── conftest.py
│   ├── test_ospf.py
│   ├── test_reachability.py
│   └── test_vlan_isolation.py
│
├── topology/
│   └── topology.clab.yml
│
├── ansible.cfg
├── Makefile
├── pytest.ini
├── README.md
└── requirements.txt
```

## Additional-Info

This portion is for logging or storing notes relevent to the project and its scope.
