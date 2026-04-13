#!/usr/bin/env python3
"""
Export Wazuh alerts to CSV for offline analysis and GitHub reports.
Requires: pip install requests pandas
"""

import requests
import pandas as pd
import json
import urllib3
from datetime import datetime, timedelta

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

WAZUH_API  = "https://10.0.2.4:55000"
USERNAME   = "wazuh-wui"
PASSWORD   = "your-api-password"   # from /var/ossec/api/configuration/api.yaml

def get_token():
    r = requests.post(
        f"{WAZUH_API}/security/user/authenticate",
        auth=(USERNAME, PASSWORD),
        verify=False
    )
    return r.json()["data"]["token"]

def get_alerts(token, hours=24):
    headers = {"Authorization": f"Bearer {token}"}
    params  = {
        "limit": 500,
        "sort":  "-timestamp",
        "q":     f"timestamp>{(datetime.utcnow()-timedelta(hours=hours)).isoformat()}Z"
    }
    r = requests.get(f"{WAZUH_API}/alerts", headers=headers, params=params, verify=False)
    return r.json().get("data", {}).get("affected_items", [])

def main():
    print("[*] Authenticating to Wazuh API...")
    token  = get_token()
    alerts = get_alerts(token)
    print(f"[*] Retrieved {len(alerts)} alerts from last 24 hours")

    rows = []
    for a in alerts:
        rows.append({
            "timestamp":   a.get("timestamp", ""),
            "rule_id":     a.get("rule", {}).get("id", ""),
            "rule_level":  a.get("rule", {}).get("level", ""),
            "description": a.get("rule", {}).get("description", ""),
            "agent_name":  a.get("agent", {}).get("name", ""),
            "agent_ip":    a.get("agent", {}).get("ip", ""),
            "mitre_id":    ", ".join(a.get("rule", {}).get("mitre", {}).get("id", [])),
            "groups":      ", ".join(a.get("rule", {}).get("groups", [])),
        })

    df = pd.DataFrame(rows)
    out = f"reports/wazuh_alerts_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
    df.to_csv(out, index=False)
    print(f"[+] Saved to {out}")

    print("\n--- Top 10 triggered rules ---")
    print(df.groupby(["rule_id","description"])["rule_id"].count()
            .sort_values(ascending=False).head(10).to_string())

if __name__ == "__main__":
    main()
