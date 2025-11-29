import argparse
import yaml
import json
import os
from datetime import datetime
from src.utils.llm_client import LLMClient
from src.agents.planner import PlannerAgent
from src.agents.data_agent import DataAgent
from src.agents.insight_agent import InsightAgent
from src.agents.evaluator import EvaluatorAgent
from src.agents.creative_generator import CreativeAgent

# Load Config
try:
    with open("config/config.yaml", "r") as f:
        config = yaml.safe_load(f)
except FileNotFoundError:
    print("Error: config/config.yaml not found. Please create it.")
    exit(1)

def generate_markdown_report(query, summary, insights, validation, creatives):
    """
    Converts the JSON analysis into a readable Markdown report (report.md)
    """
    report = []
    report.append(f"#  Kasparro Marketing Analyst Report")
    report.append(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    report.append(f"**Query:** {query}\n")
    
    report.append("## 1. Executive Summary")
    report.append(f"**Diagnosis:** {insights.get('primary_trend', 'N/A')}")
    report.append(f"**Hypothesis:** {insights.get('hypothesis', 'N/A')}")
    report.append(f"**Confidence Score:** {validation.get('confidence_score', 0) * 100:.0f}% ({validation.get('status', 'unknown')})")
    
    report.append("\n## 2. Key Data Trends")
    # Create a simple text table for the last few weeks of data
    if 'trends' in summary:
        report.append("| Date | Spend | Revenue | ROAS | CTR |")
        report.append("|---|---|---|---|---|")
        for week in summary['trends']:
            report.append(f"| {week['date']} | ${week['spend']:,.0f} | ${week['revenue']:,.0f} | {week['roas']:.2f} | {week['ctr']*100:.2f}% |")
    
    report.append("\n## 3. Validation Logic")
    report.append(f"The Evaluator agent checked the hypothesis against the data:")
    report.append(f"> *{validation.get('validation_logic', 'No logic provided')}*")
    
    report.append("\n## 4. Recommended Actions (Creatives)")
    if creatives and 'recommendations' in creatives:
        for i, rec in enumerate(creatives['recommendations'], 1):
            report.append(f"### Option {i}")
            report.append(f"- **Original Ad:** \"{rec.get('original', 'N/A')}\"")
            report.append(f"- **Improved Ad:** \"{rec.get('improved', 'N/A')}\"")
            report.append(f"- **Tactic Used:** {rec.get('tactic', 'N/A')}")
            report.append("")
    else:
        report.append("_No creative recommendations generated (Confidence too low or not required)._")

    return "\n".join(report)

def main():
    parser = argparse.ArgumentParser(description="Kasparro Agentic Analyst")
    parser.add_argument("query", type=str, help="The analysis question")
    args = parser.parse_args()

    print(f" Starting Analysis for: {args.query}")
    
    # Initialize
    try:
        llm = LLMClient(model=config.get('model', 'llama-3.3-70b-versatile'))
    except ValueError as e:
        print(f" Configuration Error: {e}")
        return

    # 1. Plan
    planner = PlannerAgent(llm)
    plan = planner.create_plan(args.query)
    print(f" Plan created: {plan}")

    # 2. Data
    data_agent = DataAgent(config['data']['raw_path'])
    metrics = plan.get('metrics', ['roas', 'spend', 'ctr']) if plan else ['roas']
    summary = data_agent.get_summary(metrics)
    
    if not summary:
        print(" Error: No data found or CSV missing.")
        return

    print(f" Data Processed. Rows analyzed: {len(summary.get('trends', []))}")

    # 3. Insights
    insight_agent = InsightAgent(llm)
    raw_insight = insight_agent.generate_insights(summary)
    print(" Hypothesis generated.")

    # 4. Evaluation
    evaluator = EvaluatorAgent()
    validation = evaluator.validate(raw_insight, summary)
    print(f" Validation: {validation['status']} (Score: {validation['confidence_score']})")

    # 5. Creative Action (if needed)
    new_creatives = {}
    if validation['confidence_score'] > config['thresholds']['confidence_min']:
        creative_agent = CreativeAgent(llm)
        new_creatives = creative_agent.improve_creatives(summary.get('low_performing_creatives', []))
        print(" New creatives generated.")
    else:
        print(" Skipping creative gen due to low confidence in diagnosis.")

    # 6. Save Outputs (Split into 3 files)
    os.makedirs("reports", exist_ok=True)

    # A. Insights.json (Combines Hypothesis + Validation)
    final_insights = {
        "analysis_query": args.query,
        "hypothesis": raw_insight,
        "validation": validation,
        "metrics_summary": summary.get('trends')[-1] if summary.get('trends') else {}
    }
    with open("reports/insights.json", "w", encoding="utf-8") as f:
        json.dump(final_insights, f, indent=2)
    print(" Saved reports/insights.json")

    # B. Creatives.json
    with open("reports/creatives.json", "w", encoding="utf-8") as f:
        json.dump(new_creatives, f, indent=2)
    print("Saved reports/creatives.json")

    # C. Report.md (Human Readable)
    markdown_content = generate_markdown_report(args.query, summary, raw_insight, validation, new_creatives)
    with open("reports/report.md", "w", encoding="utf-8") as f:
        f.write(markdown_content)
    print(" Saved reports/report.md")

if __name__ == "__main__":
    main()