#!/usr/bin/env python3
"""Documentation structural release checks. Semantic glossary review remains mandatory."""
from pathlib import Path

root = Path(__file__).resolve().parents[1]
required = ["README.md","INSTALL.md","GLOSSARY.md","SPEC.md","THREAT_MODEL.md",
            "SECURITY.md","LICENSE","NOTICE","COMMERCIAL.md","skills/mcp-driftguard/SKILL.md"]
missing = [path for path in required if not (root/path).is_file()]
assert not missing, f"Missing required documents: {missing}"
readme=(root/"README.md").read_text()
install=(root/"INSTALL.md").read_text()
glossary=(root/"GLOSSARY.md").read_text()
skill=(root/"skills/mcp-driftguard/SKILL.md").read_text()
licence=(root/"LICENSE").read_text()
notice=(root/"NOTICE").read_text()
assert all(f"]({name})" in readme for name in ("INSTALL.md","GLOSSARY.md","LICENSE","NOTICE"))
assert "Apache License" in licence and "Version 2.0" in licence
assert "Valentyn Rukhaylo" in notice
assert all(term in glossary for term in ("Baseline approval","Capability drift","MCP surface","Probe failure","Agent skill","Prompt injection","EDRG release gate"))
assert "not automatically approved" in glossary.lower() or "not automatically approved" in install.lower()
assert "MCPDRIFT_BEARER_TOKEN" in skill
assert "real-agent" in install and "pre-release" in readme.lower()
assert "## Change procedure" in glossary
print("Documentation structure, canonical glossary links, licensing and safety references: PASS")
print("Manual technical terminology and legal review: STILL REQUIRED")
