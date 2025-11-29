import unittest
from src.agents.evaluator import EvaluatorAgent

class TestEvaluatorAgent(unittest.TestCase):
    def setUp(self):
        self.evaluator = EvaluatorAgent()

    def test_validate_roas_drop_verified(self):
        # Mock data showing a drop in ROAS
        data_summary = {
            "trends": [
                {"date": "2025-01-01", "roas": 3.0},
                {"date": "2025-01-08", "roas": 1.5} # Drop
            ]
        }
        # Hypothesis correctly identifies the drop
        insight = {
            "primary_trend": "ROAS dropped significantly last week."
        }
        
        result = self.evaluator.validate(insight, data_summary)
        
        # Should be high confidence because data matches text
        self.assertEqual(result["status"], "verified")
        self.assertGreater(result["confidence_score"], 0.8)

    def test_validate_hallucination_detected(self):
        # Mock data showing ROAS INCREASE
        data_summary = {
            "trends": [
                {"date": "2025-01-01", "roas": 1.5},
                {"date": "2025-01-08", "roas": 3.0} # Increase
            ]
        }
        # Hypothesis incorrectly claims a drop
        insight = {
            "primary_trend": "ROAS dropped significantly."
        }
        
        result = self.evaluator.validate(insight, data_summary)
        
        # Should catch the lie
        self.assertEqual(result["status"], "hallucination_detected")
        self.assertLess(result["confidence_score"], 0.3)

if __name__ == '__main__':
    unittest.main()