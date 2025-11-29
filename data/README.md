# Facebook Ads Dataset

This dataset represents synthetic e-commerce performance data for undergarment products.

## Columns

| Column Name | Description | Type |
| :--- | :--- | :--- |
| `date` | Daily aggregation date | Date |
| `campaign_name` | Name of the marketing campaign | String |
| `adset_name` | Name of the specific ad set (Audience) | String |
| `spend` | Amount spent in currency | Float |
| `impressions` | Number of times ads were shown | Integer |
| `clicks` | Number of clicks on the ads | Integer |
| `ctr` | Click-Through Rate (Clicks / Impressions) | Float |
| `purchases` | Total number of purchases | Integer |
| `revenue` | Total value of purchases | Float |
| `roas` | Return on Ad Spend (Revenue / Spend) | Float |
| `creative_message` | The ad copy/headline text | String |
| `audience_type` | Type of audience (Broad, Lookalike, Retargeting) | String |
| `platform` | Placement platform (Facebook, Instagram) | String |

## Usage
This data is loaded by `src/agents/data_agent.py` to calculate weekly trends and identify low-performing creatives (CTR < 1%).