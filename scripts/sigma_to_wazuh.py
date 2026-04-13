#!/usr/bin/env python3
"""
Minimal Sigma → Wazuh XML rule converter for the lab.
Reads .yml files from detections/ and outputs Wazuh rule XML snippets.
"""

import yaml, glob, sys

RULE_ID_START = 100100

def convert(path, rule_id):
    with open(path) as f:
        sig = yaml.safe_load(f)

    level_map = {"critical": 15, "high": 12, "medium": 8, "low": 5, "informational": 3}
    level     = level_map.get(sig.get("level", "medium"), 8)
    title     = sig.get("title", "Converted Sigma Rule")
    mitre_ids = sig.get("tags", [])
    mitre_xml = "\n      ".join(
        f"<id>{t.replace('attack.','').upper()}</id>"
        for t in mitre_ids if t.startswith("attack.t")
    )

    xml = f"""  <!-- {title} — converted from {path} -->
  <rule id="{rule_id}" level="{level}">
    <description>{title}</description>
    {"<mitre>" + chr(10) + "      " + mitre_xml + chr(10) + "    </mitre>" if mitre_xml else ""}
    <group>sigma,soc-lab,</group>
  </rule>
"""
    return xml

if __name__ == "__main__":
    files = glob.glob("detections/*.yml")
    print("<group name=\"sigma-converted\">")
    for i, f in enumerate(files):
        try:
            print(convert(f, RULE_ID_START + i))
        except Exception as e:
            print(f"  <!-- ERROR converting {f}: {e} -->", file=sys.stderr)
    print("</group>")
