---
description: "Create or update a business context file for better GA4 analysis"
allowed-tools: ["Read", "Write", "Bash"]
---

# /ga4-context - Business Context Builder

Creates a business context file that makes GA4 analysis dramatically more useful. Walk through 6 business questions + what-changed section interactively.

## Usage
`/ga4-context <client_name>`

## Steps

1. **Check for existing context**: Look for `contexts/<client_name>.md` in the plugin directory. If it exists, ask if they want to update it or start fresh.

2. **Read the template**: Load `contexts/_template.md` from the plugin directory.

3. **Walk through each section interactively**:

   Ask the user these questions one section at a time. Be conversational, not robotic. If they don't know an answer, skip it and move on.

   **Section 1 - Goals**: What are your revenue/lead targets? What's the key metric you're optimizing?

   **Section 2 - Funnel**: What are your main acquisition channels? What's the expected user journey? Average conversion rate and order value?

   **Section 3 - Returning Clients**: What percentage of revenue from returning customers? Any loyalty programs or email flows?

   **Section 4 - Seasonality**: Peak and low months? Upcoming promotions?

   **Section 5 - Competitors**: Who are the main competitors? What do they do better? What do you do better?

   **Section 6 - Differentiator**: Why do customers choose you? Strongest product/service?

   **What Changed section**: Any recent campaign changes? Site updates? Technical changes? This is the most important section for weekly analysis.

4. **Save the context file** to `contexts/<client_name>.md` in the plugin directory.

5. **Confirm and suggest next step**: Context saved. Now run `/ga4-brief <property_id> --context <client_name>` for context-aware analysis.

## Tips
- Don't require perfect answers - partial context is infinitely better than no context
- The "What Changed" section should be updated regularly (weekly or when something happens)
- For e-commerce: focus on AOV, conversion rate, top product categories
- For lead gen: focus on lead quality, cost per lead, sales cycle
