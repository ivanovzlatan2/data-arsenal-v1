# Data Arsenal v1 - AI-Powered GA4 Analyst

Open-source Claude Code plugin that turns Claude into a senior GA4 analyst. 6 what-changed reports with impact scoring, 10 health checks, and context engineering for dramatically better analysis.

**No registration required.** Bundled OAuth - just sign in with your Google account.

## Quick Start (5 minutes)

### 1. Clone and install the plugin

```bash
git clone https://github.com/ivanovzlatan2/data-arsenal-v1.git
cd data-arsenal-v1
claude plugin install .
```

### 2. Set up (one time)

```
/ga4-setup
```

This opens your browser for Google sign-in. Grant read-only access to Google Analytics. That's it.

### 3. Analyze

```
/ga4-audit 123456789         # Health check (10 checks, 30 seconds)
/ga4-brief 123456789         # What-changed analysis (AI-powered insights)
```

## Commands

| Command | What it does |
|---------|-------------|
| `/ga4-setup` | One-time setup: install deps, authenticate, verify access |
| `/ga4-audit <property_id>` | 10 built-in health checks with health score |
| `/ga4-brief <property_id>` | What-changed analysis with business context |
| `/ga4-context <client>` | Create/update business context file (interactive) |
| `/ga4-report <property_id>` | Custom GA4 report with any metrics/dimensions |

### Options

```
/ga4-brief 123456789 --days 14              # Compare last 14 days vs previous 14
/ga4-brief 123456789 --context my-store     # Use business context file
/ga4-report 123456789 --metrics sessions,activeUsers --dimensions date --days 30
```

## What You Get

### What-Changed Reports (6 reports)
- **Overview**: Key metrics comparison (sessions, users, conversions, revenue, engagement)
- **Channels**: Which channels grew or declined, ranked by impact
- **Sources**: Source/medium level changes
- **Landing Pages**: Pages gaining or losing traffic
- **Products**: Product performance changes (e-commerce only, auto-detected)
- **Devices**: Device-specific anomalies

Each change is scored using impact formula: `absolute_change * min(percentage_change, 200%) / 100`. This surfaces changes that are both large AND significant.

### Health Checks (10 checks)
1. Data Volume - enough traffic for reliable analysis?
2. Duplicate Tracking - engagement rate suspiciously high?
3. Enhanced Measurement - key auto-events present?
4. Conversion Events - any conversions tracking?
5. E-commerce Completeness - full purchase funnel?
6. Referral Spam - suspicious traffic sources?
7. Self-Referral - own domain as referral?
8. (not set) Landing Pages - tracking gap indicator
9. High Bounce Pages - broken or mismatched pages
10. Event Variety - under-tracked or over-tracked?

### Context Engineering
Create business context files that make analysis 10x better. Claude uses your goals, funnel, competitors, and recent changes to explain WHY numbers moved - not just what changed.

## Standalone Usage (without Claude Code)

The Python scripts work independently:

```bash
# Setup
python3 scripts/ga4-setup

# Health checks
python3 scripts/ga4-audit 123456789

# What-changed reports
python3 scripts/ga4-what-changed 123456789
python3 scripts/ga4-what-changed 123456789 --days 14 --format json

# Custom reports
python3 scripts/ga4-report 123456789 --metrics sessions,activeUsers --dimensions date --days 30
```

## Requirements

- Python 3.8+
- Google account with GA4 access
- Claude Code (for plugin features) or standalone Python usage

Dependencies (installed automatically by `ga4-setup`):
- google-auth
- google-auth-oauthlib
- google-api-python-client

## How It Works

1. **Auth**: Bundled OAuth client ID (Google-verified). `ga4-setup` runs `InstalledAppFlow` - opens browser, user signs in, tokens saved locally to `~/.config/data-arsenal/credentials.json`. Read-only scope (`analytics.readonly`).

2. **Reports**: Each what-changed report uses dual date ranges in a single GA4 API call (current period vs previous). Changes are scored by impact and ranked.

3. **Analysis**: Claude applies 7 analytical thinking patterns (channel masking, device anomalies, quality shifts, etc.) and 5 anti-patterns to avoid (small samples, partial periods, consent gaps, etc.).

4. **Context**: Business context files give Claude the "why" layer that raw data can't provide.

## Full Audit Upgrade

The built-in `/ga4-audit` runs 10 basic checks using the Data API. For a comprehensive **50-check audit** including Admin API settings, GTM container analysis, consent mode verification, PII scanning, and more - visit [audit.dataarsenal.com](https://audit.dataarsenal.com).

## License

MIT
