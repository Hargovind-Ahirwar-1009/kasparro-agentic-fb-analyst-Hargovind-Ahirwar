# Kasparro Agentic Architecture

This system uses a multi-agent hierarchical flow to ensure data accuracy and prevent LLM hallucinations.

## Architecture Diagram

```mermaid
graph TD
    Start[User Query] --> Planner
    
    subgraph "Phase 1: Strategy"
    Planner[Planner Agent] -->|JSON Plan| DataAgent
    end
    
    subgraph "Phase 2: Analysis"
    DataAgent[Data Agent (Pandas)] -->|Statistical Summary| InsightAgent
    InsightAgent[Insight Agent (LLM)] -->|Hypothesis| Evaluator
    end
    
    subgraph "Phase 3: Validation & Action"
    Evaluator[Evaluator Agent] -->|Confidence Score| Decision{Score > 0.7?}
    
    Decision -- Yes --> CreativeAgent[Creative Agent]
    Decision -- No --> Report[Final Report]
    
    CreativeAgent -->|New Ad Copy| Report
    end