"""
Data Arsenal v1 - Shared GA4 Library
Auth, API clients, query helpers, impact scoring
"""

import os
import sys
import json
import time
from datetime import date, timedelta

# Constants
CONFIG_DIR = os.path.expanduser('~/.config/data-arsenal')
CREDENTIALS_FILE = os.path.join(CONFIG_DIR, 'credentials.json')
SCRIPTS_DIR = os.path.join(CONFIG_DIR, 'scripts')
SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
MIN_VOLUME = 5
MAX_ROWS = 15
RELATIVE_CAP = 200

BUNDLED_CLIENT_CONFIG = {
    "installed": {
        "client_id": "1054174457426-g5crq5rgsg9op7rle4mu1mj1plg5lbe4.apps.googleusercontent.com",
        "client_secret": "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",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "redirect_uris": ["http://localhost"]
    }
}


# --- Auth ---

def authenticate():
    """Run OAuth flow, save credentials. Returns Credentials object."""
    from google_auth_oauthlib.flow import InstalledAppFlow

    os.makedirs(CONFIG_DIR, exist_ok=True)

    flow = InstalledAppFlow.from_client_config(BUNDLED_CLIENT_CONFIG, SCOPES)
    creds = flow.run_local_server(port=0, prompt='consent')
    save_credentials(creds)
    return creds


def load_credentials():
    """Load credentials from JSON, auto-refresh if expired. Returns Credentials or None."""
    if not os.path.exists(CREDENTIALS_FILE):
        return None

    try:
        with open(CREDENTIALS_FILE, 'r') as f:
            data = json.load(f)

        from google.oauth2.credentials import Credentials
        creds = Credentials(
            token=data.get('token'),
            refresh_token=data.get('refresh_token'),
            token_uri=data.get('token_uri', 'https://oauth2.googleapis.com/token'),
            client_id=data.get('client_id'),
            client_secret=data.get('client_secret'),
            scopes=data.get('scopes', SCOPES)
        )

        if creds.expired and creds.refresh_token:
            import google.auth.transport.requests
            creds.refresh(google.auth.transport.requests.Request())
            save_credentials(creds)

        return creds
    except Exception as e:
        print(f"Error loading credentials: {e}", file=sys.stderr)
        return None


def save_credentials(creds):
    """Serialize credentials to JSON file."""
    os.makedirs(CONFIG_DIR, exist_ok=True)
    data = {
        'token': creds.token,
        'refresh_token': creds.refresh_token,
        'token_uri': creds.token_uri,
        'client_id': creds.client_id,
        'client_secret': creds.client_secret,
        'scopes': list(creds.scopes) if creds.scopes else SCOPES
    }
    with open(CREDENTIALS_FILE, 'w') as f:
        json.dump(data, f, indent=2)


def require_credentials():
    """Load credentials or exit with helpful message."""
    creds = load_credentials()
    if not creds:
        print("Not authenticated. Run ga4-setup first.", file=sys.stderr)
        sys.exit(1)
    return creds


# --- API Clients ---

def get_data_service(creds):
    """Build GA4 Data API v1beta service."""
    from googleapiclient.discovery import build
    return build('analyticsdata', 'v1beta', credentials=creds, cache_discovery=False)


def get_admin_service(creds):
    """Build GA4 Admin API v1beta service."""
    from googleapiclient.discovery import build
    return build('analyticsadmin', 'v1beta', credentials=creds, cache_discovery=False)


def list_properties(creds):
    """List all accessible GA4 properties. Returns list of dicts."""
    admin = get_admin_service(creds)
    properties = []
    page_token = None

    while True:
        resp = admin.accountSummaries().list(pageSize=200, pageToken=page_token).execute()
        for account in resp.get('accountSummaries', []):
            account_name = account.get('displayName', 'Unknown')
            for prop in account.get('propertySummaries', []):
                prop_id = prop.get('property', '').replace('properties/', '')
                properties.append({
                    'property_id': prop_id,
                    'display_name': prop.get('displayName', 'Unknown'),
                    'account_name': account_name
                })
        page_token = resp.get('nextPageToken')
        if not page_token:
            break

    return properties


# --- Query Helpers ---

def build_query(date_ranges, metrics, dimensions=None, limit=10000,
                dimension_filter=None, order_bys=None):
    """Build a GA4 Data API request body."""
    body = {
        'dateRanges': date_ranges if isinstance(date_ranges, list) else [date_ranges],
        'metrics': [{'name': m} for m in metrics],
        'limit': limit
    }
    if dimensions:
        body['dimensions'] = [{'name': d} for d in dimensions]
    if dimension_filter:
        body['dimensionFilter'] = dimension_filter
    if order_bys:
        body['orderBys'] = order_bys
    return body


def run_report(service, property_id, body, retries=2):
    """Execute GA4 report with retry logic. Returns response dict or raises."""
    from googleapiclient.errors import HttpError

    prop = property_id if property_id.startswith('properties/') else f'properties/{property_id}'
    last_error = None

    for attempt in range(retries + 1):
        try:
            return service.properties().runReport(property=prop, body=body).execute()
        except HttpError as e:
            try:
                detail = json.loads(e.content.decode())['error']['message']
            except Exception:
                detail = str(e)
            raise RuntimeError(f"GA4 API error: {detail}")
        except Exception as e:
            last_error = e
            if attempt < retries:
                time.sleep(0.5 * (attempt + 1))
                continue
            raise RuntimeError(f"GA4 API error after {retries + 1} attempts: {last_error}")


def get_property_name(creds, property_id):
    """Get display name for a property ID."""
    try:
        admin = get_admin_service(creds)
        prop = property_id if property_id.startswith('properties/') else f'properties/{property_id}'
        info = admin.properties().get(name=prop).execute()
        return info.get('displayName', property_id)
    except Exception:
        return property_id


# --- Response Parsing ---

def parse_rows(response, metrics, dimensions=None):
    """Parse GA4 response into list of dicts."""
    if not response.get('rows'):
        return []

    rows = []
    for row in response['rows']:
        d = {}
        if dimensions:
            for i, dim in enumerate(dimensions):
                try:
                    d[dim] = row['dimensionValues'][i]['value']
                except (KeyError, IndexError):
                    d[dim] = '(not set)'
        for i, metric in enumerate(metrics):
            try:
                val = row['metricValues'][i]['value']
                try:
                    d[metric] = float(val)
                except ValueError:
                    d[metric] = val
            except (KeyError, IndexError):
                d[metric] = 0.0
        rows.append(d)
    return rows


# --- Impact Scoring ---

def calculate_impact(current, previous):
    """Calculate impact score using Trackian's formula.

    impact = abs_diff * min(abs(pct_diff), RELATIVE_CAP) / 100
    """
    current = float(current)
    previous = float(previous)
    abs_diff = abs(current - previous)

    if previous == 0:
        pct_diff = 100.0 if current >= MIN_VOLUME else 0.0
    else:
        pct_diff = (current - previous) / previous * 100

    capped_pct = min(abs(pct_diff), RELATIVE_CAP)
    return abs_diff * capped_pct / 100


def format_change(current, previous, is_rate=False):
    """Format change as string with direction arrow."""
    current = float(current)
    previous = float(previous)
    diff = current - previous

    if previous == 0:
        pct = 100.0 if current > 0 else 0.0
    else:
        pct = diff / previous * 100

    if is_rate:
        sign = '+' if diff >= 0 else ''
        return f"{sign}{diff:.1f}pp", pct
    else:
        sign = '+' if diff >= 0 else ''
        return f"{sign}{diff:,.0f}", pct


def format_number(val, is_rate=False):
    """Format a number for display."""
    val = float(val)
    if is_rate:
        return f"{val:.1f}%"
    if val >= 1000000:
        return f"{val:,.0f}"
    if val >= 100:
        return f"{val:,.0f}"
    if val == int(val):
        return f"{int(val)}"
    return f"{val:.2f}"


# --- Date Helpers ---

def get_date_ranges(days=7):
    """Get current and previous date ranges for comparison.

    Returns two date range dicts for dual-range GA4 queries.
    """
    end = date.today() - timedelta(days=1)  # yesterday (today's data is incomplete)
    start = end - timedelta(days=days - 1)
    prev_end = start - timedelta(days=1)
    prev_start = prev_end - timedelta(days=days - 1)

    return [
        {'startDate': start.strftime('%Y-%m-%d'), 'endDate': end.strftime('%Y-%m-%d')},
        {'startDate': prev_start.strftime('%Y-%m-%d'), 'endDate': prev_end.strftime('%Y-%m-%d')}
    ], start, end, prev_start, prev_end
