# Troubleshooting

Common failure modes for the AnsibleNetlab stack, ordered roughly from
"first deploy" to "CI".

## Containerlab

### `containerlab deploy` fails with `permission denied`

Docker daemon is not reachable by the current user.

```bash
sudo usermod -aG docker "$USER"
newgrp docker
```

Log out and back in if `newgrp` is not available on your shell.

### `image pull failed` for `quay.io/frrouting/frr`

Corporate proxy or DNS issue. Confirm with:

```bash
docker pull quay.io/frrouting/frr:10.0.1
```

If the pull works but Containerlab still fails, check that
`~/.config/containerlab/` is writable.

### Nodes start but `containerlab inspect` shows `exited`

Almost always a missing `privileged: true` on the FRR nodes. The FRR daemon
tries to open raw sockets and is killed by the runtime without it.

### Port conflicts on WSL2

Containerlab’s management network occasionally collides with the WSL2 host
network. Set a non-default management subnet in `topology.clab.yml`:

```yaml
mgmt:
  network: clab-mgmt
  ipv4-subnet: 172.20.20.0/24
```

## Ansible

### `wait_for_connection` times out

The container is up but not yet accepting Ansible’s docker exec. Rare on a
healthy host; usually means the Docker daemon is under load. Increase
`timeout` in `ansible/configure.yml`.

### `src: templates/frr.conf.j2` resolves to the wrong path

Ansible resolves `src:` relative to the playbook directory, not the CWD. If
you run `ansible-playbook` from anywhere other than the repo root, prefix
the paths:

```bash
ansible-playbook -i ansible/inventory.yml ansible/configure.yml
```

The `scripts/configure.sh` wrapper already does this.

### `vtysh` shows no OSPF neighbors after a successful playbook run

Check the daemon toggle:

```bash
docker exec clab-ccna-lab-r1 grep '^ospfd' /etc/frr/daemons
```

It must be `ospfd=yes`. If it is not, a task was skipped — re-run
`./scripts/configure.sh` and look for the `Enable ospfd daemon` task.

## Alpine hosts

### `ifup: not found`

The Alpine base image does not ship `ifup`. The playbook installs
`ifupdown-ng` first; if you skipped that task, install it manually:

```bash
docker exec clab-ccna-lab-host1 apk add --no-cache ifupdown-ng
```

### `eth1` has no address after `ifup`

Confirm `/etc/network/interfaces` contains a `static` stanza for `eth1`:

```bash
docker exec clab-ccna-lab-host1 cat /etc/network/interfaces
```

Then bring it up manually and inspect:

```bash
docker exec clab-ccna-lab-host1 ip addr show eth1
```

## pytest / pytest-clab

### `fixture 'clab' not found`

`pytest-clab` is not installed in the active virtualenv.

```bash
pip install -r requirements.txt
```

### Tests pass individually but fail when run together

The `lab` fixture is `scope="session"`, but a previous run may have left
stale containers behind.

```bash
./scripts/destroy.sh
./scripts/test.sh
```

### Ansible config does not run before the tests

`tests/conftest.py` invokes Ansible inside the `lab` fixture. If you see
`test_ospf` failing with an empty neighbor table, check the fixture’s
`subprocess.run(..., check=True)` actually completed — it will raise on
non‑zero exit.

## CI

### GitHub Actions runner runs out of disk

Cache the FRR and Alpine images between runs:

```yaml
- uses: actions/cache@v4
  with:
    path: /var/lib/docker
    key: docker-${{ runner.os }}-${{ hashFiles('topology/topology.clab.yml') }}
```

Alternatively, run `docker system prune -af` before `deploy.sh`.

### `containerlab` install fails on Ubuntu runners

The install script fetches from `get.containerlab.dev`, which occasionally
rate‑limits. Retry once:

```bash
bash -c "$(curl -sL https://get.containerlab.dev)" || \
  bash -c "$(curl -sL https://get.containerlab.dev)"
```

## Getting unstuck

If none of the above fits:

1. `containerlab inspect -t topology/topology.clab.yml` — is the lab even up?
2. `docker logs clab-ccna-lab-r1` — did FRR start cleanly?
3. `docker exec clab-ccna-lab-r1 vtysh -c 'show running-config'` — did the
   config land?
4. `pytest -vv -x` — stop at the first failure and read the full traceback.