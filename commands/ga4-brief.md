---
description: "Run what-changed analysis on a GA4 property with AI-powered insights"
allowed-tools: ["Bash", "Read"]
---

# /ga4-brief - What-Changed Analysis

Runs 6 what-changed reports and provides AI-powered analysis with business context.

## Usage
`/ga4-brief <property_id> [--context <client>] [--days 7]`

## Steps

1. **Load context** (if specified): Read `contexts/<client>.md` from the plugin directory. If no context file exists, warn that analysis will be limited and suggest `/ga4-context`.

2. **Run what-changed reports**:
```bash
python3 ~/.config/data-arsenal/scripts/ga4-what-changed <property_id> --days <N>
```

3. **Analyze the output** using these thinking patterns:

   - **Totals masking opposite trends**: If total sessions are flat, check if one channel grew while another declined. The 100K trap - stable totals hiding volatile segments.
   - **Device-specific anomalies**: A drop only on mobile = likely site bug, not marketing problem.
   - **Channel quality shifts**: More traffic + lower engagement = bad traffic, not growth.
   - **Funnel bottleneck changes**: If conversions dropped, which funnel step broke?
   - **Landing page disappearances**: Sudden drop in a page's traffic = 404, redirect, or de-indexed.
   - **New vs returning divergence**: Acquisition problem (new users down) vs retention problem (returning down).
   - **Revenue without transactions**: Revenue metric moving without purchase events = data quality issue.

4. **Check for anti-patterns** before concluding:
   - Drawing conclusions from <100 sessions
   - Comparing partial weeks (incomplete data)
   - Ignoring consent gaps (30-50% data loss is normal)
   - Attributing all changes to one cause without checking segments
   - Trusting 100% engagement rate (duplicate tracking)

5. **Output format**:
   - Lead with the single biggest insight (one sentence)
   - List 3-5 findings ranked by business impact
   - For each finding: what changed, why it likely matters, what to do
   - End with "What to investigate next" section
   - If context file was loaded, reference business goals and recent changes

## Communication Style
- Lead with the insight, not the methodology
- Plain language, not GA4 jargon
- Never say "interesting" - say whether it matters and why
- Always end with specific, actionable next steps
