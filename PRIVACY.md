# Privacy Policy - Data Arsenal v1

**Last updated:** March 13, 2026

## What Data We Access

Data Arsenal accesses your Google Analytics 4 data in **read-only** mode using the `analytics.readonly` scope. This includes:

- Account and property metadata (property names, IDs)
- Analytics metrics (sessions, users, conversions, revenue)
- Analytics dimensions (channels, sources, landing pages, devices, events)

## How Data Is Used

All data processing happens **locally on your machine**. Data Arsenal:

- Generates performance reports and health checks from your GA4 data
- Stores OAuth credentials locally at `~/.config/data-arsenal/credentials.json`
- Does **not** send your analytics data to any external server
- Does **not** store your data anywhere other than your local machine

## Data Storage

- **OAuth tokens**: Stored locally on your device only
- **Analytics data**: Fetched on demand, displayed in your terminal, never persisted
- **No server-side storage**: Data Arsenal has no backend server or database

## Third-Party Services

Data Arsenal communicates only with Google's APIs:
- Google Analytics Data API (for reports)
- Google Analytics Admin API (for property listing)

No other third-party services receive your data.

## Data Sharing

We do not sell, share, or transfer your data to any third party.

## Your Rights

You can revoke Data Arsenal's access at any time:
1. Visit https://myaccount.google.com/permissions
2. Find "Data Arsenal" and click "Remove Access"
3. Delete local credentials: `rm ~/.config/data-arsenal/credentials.json`

## Contact

For questions about this privacy policy: https://github.com/ivanovzlatan2/data-arsenal-v1/issues
