---
description: "Run a custom GA4 report with specified metrics and dimensions"
allowed-tools: ["Bash"]
---

# /ga4-report - Custom Report Runner

Runs a custom GA4 report with user-specified metrics and dimensions.

## Usage
`/ga4-report <property_id> [--metrics sessions,activeUsers] [--dimensions date] [--days 30] [--limit 100]`

## Steps

1. **Parse the request**: If the user gives a natural language request instead of exact parameters, translate to GA4 metrics and dimensions:
   - "show me traffic by channel" -> `--metrics sessions,activeUsers --dimensions sessionDefaultChannelGroup`
   - "daily sessions this month" -> `--metrics sessions --dimensions date --days 30`
   - "top landing pages" -> `--metrics sessions,bounceRate --dimensions landingPage`
   - "revenue by source" -> `--metrics totalRevenue,ecommercePurchases --dimensions sessionSourceMedium`

2. **Run the report**:
```bash
python3 ~/.config/data-arsenal/scripts/ga4-report <property_id> --metrics <metrics> --dimensions <dims> --days <N> --limit <L>
```

3. **Present results** with brief interpretation if the data warrants it.

## Common Metrics
- Traffic: sessions, activeUsers, newUsers, totalUsers
- Engagement: engagementRate, bounceRate, averageSessionDuration, screenPageViews
- Conversions: conversions, eventCount
- E-commerce: totalRevenue, ecommercePurchases, purchaseRevenue

## Common Dimensions
- Time: date, hour, dayOfWeek
- Source: sessionSourceMedium, sessionDefaultChannelGroup, sessionSource
- Content: landingPage, pagePath, pageTitle
- User: deviceCategory, country, city, userAgeBracket
- Events: eventName
