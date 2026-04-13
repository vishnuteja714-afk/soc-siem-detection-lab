# Incident Analysis Report

| Field | Value |
|-------|-------|
| Date | 2024-01-15 |
| Analyst | your-name |
| Severity | High |
| Status | Closed — True Positive |

## Summary

SSH brute force attack detected originating from Kali Linux VM (10.0.2.7) targeting
Ubuntu agent (10.0.2.5). Attack lasted 4 minutes and involved 87 failed authentication
attempts. No successful login occurred. Attacker used the `rockyou.txt` wordlist via Hydra.

## Timeline

| Time | Event |
|------|-------|
| 14:02:11 | First failed SSH login from 10.0.2.7 |
| 14:02:15 | Wazuh rule 100001 fired (10+ failures in 60s) |
| 14:06:08 | Last failed login attempt |
| 14:06:10 | Analyst reviewed and confirmed |

## IOCs

- Source IP: 10.0.2.7
- Target: 10.0.2.5:22
- Usernames attempted: root, admin, ubuntu, vishnu, test
- Tool detected: Hydra (User-Agent pattern)

## MITRE ATT&CK

- T1110.001 — Brute Force: Password Guessing

## Response actions

1. Source IP blocked via iptables on victim
2. Alert tagged True Positive in Wazuh
3. No escalation required (lab environment)

## Lessons learned

Rule 100001 triggered correctly at threshold of 10 failures/60s. Consider lowering
threshold to 5 for production environments to reduce dwell time before detection.
