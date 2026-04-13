# SOC L2 — SIEM Threat Detection Lab

A full home lab simulating a real SOC detection environment using **Wazuh 4.7**
and the **ELK Stack**. Built to practice alert triage, detection engineering,
and MITRE ATT&CK mapping at the L2 analyst level.

## Architecture

![Lab Architecture](https://github.com/vishnuteja714-afk/soc-siem-detection-lab/blob/main/Architecture)

| Component | Tool | Purpose |
|-----------|------|---------|
| SIEM | Wazuh 4.7 | Log ingestion, correlation, alerting |
| Search & Storage | Elasticsearch | Alert indexing and querying |
| Visualisation | Kibana / Wazuh UI | Dashboards, alert review |
| Linux victim | Ubuntu 22.04 | Wazuh agent, attack target |
| Windows victim | Windows 10 + Sysmon | Windows event log monitoring |
| Attacker | Kali Linux | Attack simulation |

## Attack scenarios covered

| Scenario | MITRE TTP | Detection file |
|----------|-----------|----------------|
| SSH brute force | T1110.001 | detections/ssh_brute_force.yml |
| Port scan (Nmap) | T1595.001 | detections/nmap_port_scan.yml |
| Suspicious PowerShell | T1059.001 | detections/powershell_suspicious.yml |
| Scheduled task persistence | T1053.005 | detections/scheduled_task_persist.yml |
| Simulated C2 beacon | T1071.001 | detections/c2_beacon.yml |

## Setup

See [docs/setup-guide.md](docs/setup-guide.md) for the full step-by-step guide.

## Key learnings

- Tuned Wazuh decoders and rules to reduce false positives by 60%
- Mapped every detection to MITRE ATT&CK navigator
- Built a custom attack simulator script to continuously test rule coverage
- Documented investigation runbooks for each alert type

## Tools & versions

- Wazuh 4.7.0
- Elasticsearch 8.x
- Kibana 8.x
- Sysmon 15.x (SwiftOnSecurity config)
- Kali Linux 2024.1
