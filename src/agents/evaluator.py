from src.utils.logger import setup_logger

logger = setup_logger("evaluator_agent")

class EvaluatorAgent:
    def validate(self, insight, data_summary):
        logger.info("Validating insights against hard data...")
        
        trends = data_summary.get('trends', [])
        if len(trends) < 2:
            return {"status": "neutral", "confidence": 0.5, "reason": "Not enough data"}

        latest = trends[-1]
        prev = trends[-2]
        
        # Logic: Check if data supports the text "drop" or "increase"
        roas_change = latest['roas'] - prev['roas']
        insight_text = str(insight).lower()
        
        is_roas_down = roas_change < 0
        claims_drop = "drop" in insight_text or "decreas" in insight_text or "down" in insight_text
        
        confidence = 0.5
        status = "uncertain"

        if is_roas_down and claims_drop:
            confidence = 0.95
            status = "verified"
        elif not is_roas_down and claims_drop:
            confidence = 0.1
            status = "hallucination_detected"
            logger.warning("Insight claimed drop, but data shows increase.")
        else:
            confidence = 0.8
            status = "plausible"
            
        return {
            "status": status,
            "confidence_score": confidence,
            "metric_check": f"ROAS change: {roas_change:.2f}"
        }