import pandas as pd
from src.utils.logger import setup_logger

logger = setup_logger("data_agent")

class DataAgent:
    def __init__(self, csv_path):
        self.path = csv_path
        try:
            self.df = pd.read_csv(csv_path)
            self.df['date'] = pd.to_datetime(self.df['date'])
            logger.info(f"Loaded data: {len(self.df)} rows")
        except Exception as e:
            logger.error(f"Failed to load CSV: {e}")
            self.df = pd.DataFrame()

    def get_summary(self, metrics, aggregation='W'):
        if self.df.empty:
            return {}
            
        # Normalize aggregation for Pandas (W=Weekly, D=Daily)
        rule = 'W-MON' if aggregation.upper().startswith('W') else 'D'
        
        # Group by aggregation
        agg_df = self.df.groupby(pd.Grouper(key='date', freq=rule)).agg({
            'spend': 'sum',
            'revenue': 'sum',
            'impressions': 'sum',
            'clicks': 'sum'
        }).reset_index()
        
        # Calculate KPIs safely
        agg_df['roas'] = agg_df.apply(lambda x: x['revenue'] / x['spend'] if x['spend'] > 0 else 0, axis=1)
        agg_df['ctr'] = agg_df.apply(lambda x: x['clicks'] / x['impressions'] if x['impressions'] > 0 else 0, axis=1)
        agg_df['cpc'] = agg_df.apply(lambda x: x['spend'] / x['clicks'] if x['clicks'] > 0 else 0, axis=1)
        
        # Convert dates to string for JSON serialization
        agg_df['date'] = agg_df['date'].dt.strftime('%Y-%m-%d')
        
        # Take last 5 periods for context
        summary_dict = agg_df.tail(5).to_dict(orient='records')
        
        # Get low performing ads (CTR < 1%)
        low_ads = self.df[self.df['ctr'] < 0.01][['creative_message', 'ctr', 'spend', 'roas']].head(5).to_dict(orient='records')
        
        return {
            "trends": summary_dict,
            "low_performing_creatives": low_ads
        }