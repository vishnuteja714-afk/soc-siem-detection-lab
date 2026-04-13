# Lab Setup Guide

## Prerequisites

- Host machine: 16 GB RAM, 8 cores, 100 GB free disk
- VirtualBox 7.x or VMware Workstation
- Ubuntu 22.04 Server ISO
- Windows 10 ISO (evaluation from Microsoft)
- Kali Linux ISO

## Network design

All VMs connect to a VirtualBox NAT Network named `soc-lab` (10.0.2.0/24).

| VM | IP |
|----|----|
| wazuh-manager | 10.0.2.4 |
| ubuntu-agent | 10.0.2.5 |
| win10-agent | 10.0.2.6 |
| kali-attacker | 10.0.2.7 |

## Step 1 — Install Wazuh all-in-one

```bash
curl -sO https://packages.wazuh.com/4.7/wazuh-install.sh
sudo bash wazuh-install.sh -a
```

Dashboard: https://10.0.2.4:443

## Step 2 — Enrol agents

See README.md Phase 4 and Phase 5.

## Step 3 — Configure Sysmon on Windows

Import `configs/sysmonconfig.xml` when installing Sysmon.

## Step 4 — Load custom detection rules

Copy `configs/local_rules.xml` to `/var/ossec/etc/rules/` on the manager, then:

```bash
sudo systemctl restart wazuh-manager
```

## Step 5 — Run the attack simulator

```bash
chmod +x scripts/attack_simulator.sh
sudo ./scripts/attack_simulator.sh 10.0.2.5
```

## Step 6 — Verify alerts in dashboard

Navigate to Wazuh UI → Security Events → filter by `rule.level >= 10`
