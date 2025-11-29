You are a Senior Marketing Analyst. Analyze the following weekly data trends:

{data_trends}

Task:
1. Identify the main trend in ROAS and Spend (Increasing, Decreasing, Flat).
2. Provide a hypothesis for WHY this is happening based on the relationship between Spend, CTR, and ROAS.
   - If Spend is UP and ROAS is DOWN, consider "Efficiency Loss" or "Scaling issues".
   - If CTR is DOWN, consider "Creative Fatigue".

Return STRICT JSON:
{{
    "primary_trend": "ROAS dropped from X to Y...",
    "hypothesis": "Efficiency decreased due to...",
    "reasoning": "Spend went up by 20% while revenue only grew 5%."
}}