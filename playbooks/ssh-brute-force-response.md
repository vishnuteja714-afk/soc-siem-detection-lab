# Playbook — SSH brute force response

**Alert:** Rule 100001 — SSH brute force attempt  
**MITRE:** T1110.001  
**Severity:** High

## Triage steps

1. **Identify source IP**
   - Wazuh UI → Security Events → filter `rule.id:100001`
   - Note `data.srcip` field

2. **Check if IP is internal or external**
   - Internal → possible compromised host → escalate
   - External → add to blocklist

3. **Check volume and timing**
   - Is this automated (>50 attempts/min) or manual (slow/low)?
   - Review `data.dstuser` — is it root, a service account, or a real user?

4. **Check for successful login after failures**
   - Search: `rule.id:5715 AND data.srcip:<attacker_ip>`
   - If yes → **CRITICAL** — treat as active compromise, escalate to IR

5. **Containment**
   - Block IP at firewall / iptables
```bash
   sudo iptables -A INPUT -s <attacker_ip> -j DROP
```
   - If account was compromised: `passwd -l <username>`

6. **Evidence collection**
```bash
   sudo grep <attacker_ip> /var/log/auth.log > /tmp/evidence_ssh.txt
   last -n 50 > /tmp/evidence_last.txt
```

7. **Close and document**
   - Record in `reports/` with IOCs, timeline, and disposition
   - Tag alert in Wazuh as `True Positive` or `False Positive`

## Escalation criteria

Escalate to Tier 3 / Incident Response if:
- Any successful login detected from the attacking IP
- Attacking IP belongs to your own network range
- Attack volume exceeds 1,000 attempts
