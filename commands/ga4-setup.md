---
description: "Set up Data Arsenal - install dependencies, authenticate with Google Analytics"
allowed-tools: ["Bash"]
---

# /ga4-setup - First-Time Setup

Run the setup script to install Python dependencies, authenticate with Google, and verify GA4 access.

## Steps

1. **Find and run the setup script.** Check these locations in order:

```bash
if [ -f ~/.config/data-arsenal/scripts/ga4-setup ]; then
  python3 ~/.config/data-arsenal/scripts/ga4-setup
elif [ -f scripts/ga4-setup ]; then
  python3 scripts/ga4-setup
else
  SCRIPT=$(find ~ -maxdepth 6 -path "*/data-arsenal*/scripts/ga4-setup" -type f 2>/dev/null | head -1)
  if [ -n "$SCRIPT" ]; then
    python3 "$SCRIPT"
  else
    echo "Cannot find ga4-setup. Run from the data-arsenal-v1 directory: python3 scripts/ga4-setup"
  fi
fi
```

2. If setup succeeds, show the user their properties and suggest next steps:
   - `/ga4-audit <property_id>` to run health checks
   - `/ga4-brief <property_id>` for what-changed analysis
   - `/ga4-context <client>` to create a business context file

3. If setup fails, help diagnose:
   - Python version issues: need 3.8+
   - pip install failures: suggest `pip3 install --user -r requirements.txt`
   - OAuth failures: check browser access, try again
   - No properties: verify Google account has GA4 access
