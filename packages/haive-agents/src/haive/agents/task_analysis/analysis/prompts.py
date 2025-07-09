# src/haive/agents/task_analysis/analysis/prompts.py

from langchain_core.prompts import ChatPromptTemplate

INTEGRATED_ANALYSIS_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a senior task analyst integrating multiple analysis dimensions into comprehensive insights.

Your role is to:
- Synthesize findings from all analysis components
- Identify cross-cutting concerns
- Generate actionable recommendations
- Prioritize improvements
- Assess overall feasibility""",
        ),
        (
            "human",
            """Integrate these analyses:

**Task**: {task_description}

**Decomposition Results**:
{decomposition_summary}

**Complexity Analysis**:
{complexity_scores}

**Execution Plan**:
{execution_summary}

**Context Requirements**:
{context_summary}

**Tree Analysis**:
{tree_metrics}

Provide:
1. **Executive Summary**
   - Key findings
   - Overall assessment
   - Critical risks

2. **Integrated Insights**
   - Cross-component patterns
   - Conflicting requirements
   - Synergy opportunities

3. **Prioritized Recommendations**
   - Quick wins
   - Strategic improvements
   - Risk mitigations

4. **Success Factors**
   - Critical requirements
   - Key dependencies
   - Success metrics

5. **Implementation Roadmap**
   - Phased approach
   - Milestone markers
   - Decision points

Return comprehensive analysis summary.""",
        ),
    ]
)

FEASIBILITY_ASSESSMENT_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are assessing overall task feasibility based on comprehensive analysis.""",
        ),
        (
            "human",
            """Assess feasibility for:

**Task**: {task_description}
**Complexity Score**: {complexity_score}
**Resource Requirements**: {resources}
**Constraints**: {constraints}
**Risks**: {identified_risks}

Evaluate:
1. Technical feasibility
2. Resource feasibility
3. Time feasibility
4. Risk acceptability
5. Success probability

Return feasibility assessment with go/no-go recommendation.""",
        ),
    ]
)

OPTIMIZATION_RECOMMENDATIONS_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are generating optimization recommendations based on comprehensive task analysis.""",
        ),
        (
            "human",
            """Generate optimizations for:

**Current Plan**: {current_plan}
**Bottlenecks**: {bottlenecks}
**Complexity Factors**: {complexity_factors}
**Resource Constraints**: {constraints}

Provide:
1. Task restructuring options
2. Parallelization improvements
3. Resource optimization
4. Complexity reduction strategies
5. Risk mitigation approaches

Prioritize by impact and feasibility.""",
        ),
    ]
)
