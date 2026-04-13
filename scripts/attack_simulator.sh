#!/bin/bash
# SOC Lab Attack Simulator
# Usage: sudo ./attack_simulator.sh <target_ip>
# WARNING: Run ONLY inside your isolated lab network

TARGET=${1:-10.0.2.5}
echo "================================================"
echo " SOC Lab Attack Simulator — Target: $TARGET"
echo " Run inside isolated lab VMs only"
echo "================================================"

pause() { echo ""; sleep 2; }

echo "[1/5] SSH Brute Force (T1110.001)"
echo "       Sending 15 failed SSH attempts to trigger rule 100001..."
for i in {1..15}; do
  sshpass -p "wrongpassword$i" ssh -o StrictHostKeyChecking=no \
    -o ConnectTimeout=2 baduser@$TARGET 2>/dev/null
done
echo "       Done — check Wazuh for alert rule.id:100001"
pause

echo "[2/5] Nmap Port Scan (T1595.001)"
echo "       Running SYN scan against $TARGET..."
nmap -sS -T4 --top-ports 1000 $TARGET -oN /tmp/nmap_output.txt 2>/dev/null
echo "       Done — scan saved to /tmp/nmap_output.txt"
pause

echo "[3/5] Simulated C2 Beacon (T1071.001)"
echo "       Attempting outbound connection on port 4444..."
nc -zv $TARGET 4444 2>/dev/null || true
curl -s --connect-timeout 2 http://$TARGET:8888 >/dev/null 2>&1 || true
echo "       Done — check Wazuh for alert rule.id:100005"
pause

echo "[4/5] File enumeration (T1083)"
echo "       Listing sensitive paths on local system..."
find /etc -name "*.conf" 2>/dev/null | head -20
find /var/log -name "*.log" 2>/dev/null | head -10
echo "       Done — FIM alerts should fire for /etc writes"
pause

echo "[5/5] Failed sudo attempt (T1548.003)"
echo "       Attempting privilege escalation..."
sudo -u root id 2>/dev/null || true
echo "       Done — check Wazuh for sudo failure alert"

echo ""
echo "All scenarios complete. Review Wazuh dashboard for alerts."
echo "URL: https://10.0.2.4:443"
