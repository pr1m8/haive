# Planning and Reasoning Examples

Build intelligent agents that can break down complex tasks, create detailed plans, and execute them systematically. These examples showcase advanced reasoning capabilities and strategic thinking.

## Purpose

Planning agents excel at complex, multi-step problems that require strategic thinking, resource allocation, and adaptive execution. Learn to build agents that can plan, reason about constraints, and adapt to changing conditions.

## Prerequisites

- Strong understanding of multi-agent patterns
- Basic knowledge of search algorithms and optimization
- Familiarity with constraint satisfaction problems
- Understanding of state spaces and goal-oriented planning

## Examples

### Basic Planning

#### `task_planner.py`

**Break down complex tasks into steps**

- Goal decomposition strategies
- Sequential task planning
- Dependency management
- Progress tracking

#### `resource_planner.py`

**Plan with resource constraints**

- Resource allocation optimization
- Constraint satisfaction
- Budget and time management
- Trade-off analysis

#### `adaptive_planner.py`

**Plans that adapt to changing conditions**

- Dynamic re-planning
- Plan monitoring and adjustment
- Failure recovery strategies
- Real-time constraint updates

### Advanced Planning

#### `hierarchical_planner.py`

**Multi-level planning system**

- Strategic and tactical planning
- Plan decomposition across levels
- Abstract and concrete actions
- Top-down and bottom-up planning

#### `collaborative_planner.py`

**Multi-agent planning system**

- Distributed task allocation
- Negotiation and coordination
- Conflict resolution
- Consensus building

#### `temporal_planner.py`

**Time-aware planning**

- Scheduling and timing constraints
- Deadline management
- Temporal dependencies
- Calendar integration

### Reasoning Systems

#### `logical_reasoner.py`

**Logic-based reasoning agent**

- Propositional and predicate logic
- Inference and deduction
- Knowledge representation
- Consistency checking

#### `causal_reasoner.py`

**Causal reasoning and analysis**

- Cause-and-effect relationships
- Intervention planning
- Counterfactual reasoning
- Root cause analysis

#### `strategic_reasoner.py`

**Game-theoretic and strategic reasoning**

- Multi-party strategy development
- Nash equilibrium analysis
- Risk assessment and mitigation
- Competitive advantage planning

### Production Planning

#### `project_manager.py`

**Complete project management system**

- Project initialization and scoping
- Resource allocation and scheduling
- Progress monitoring and reporting
- Stakeholder communication

#### `workflow_optimizer.py`

**Business process optimization**

- Workflow analysis and improvement
- Bottleneck identification
- Process automation planning
- Performance optimization

#### `crisis_manager.py`

**Emergency response planning**

- Rapid situation assessment
- Emergency response protocols
- Resource mobilization
- Crisis communication planning

## Key Components

### Planning Architecture

```python
from haive.agents.planning import PlannerAgent
from haive.core.planning import Goal, Action, Constraint

# Define planning problem
goal = Goal(
    description="Launch new product",
    success_criteria=["market_ready", "legal_compliance", "budget_met"]
)

constraints = [
    Constraint("budget", "max", 100000),
    Constraint("timeline", "before", "2024-06-01"),
    Constraint("team_size", "max", 10)
]

# Create planner
planner = PlannerAgent(
    name="project_planner",
    planning_algorithm="hierarchical_task_network",
    constraint_solver="backtracking"
)

# Generate plan
plan = await planner.create_plan(goal=goal, constraints=constraints)
```

### Multi-Agent Planning

```python
# Specialized planning agents
strategic_planner = StrategicPlannerAgent(
    name="strategy",
    focus="high_level_goals",
    time_horizon="long_term"
)

tactical_planner = TacticalPlannerAgent(
    name="tactics",
    focus="implementation_details",
    time_horizon="medium_term"
)

operational_planner = OperationalPlannerAgent(
    name="operations",
    focus="daily_execution",
    time_horizon="short_term"
)

# Hierarchical planning system
planning_system = HierarchicalPlanningWorkflow([
    strategic_planner,
    tactical_planner,
    operational_planner
])
```

### Adaptive Execution

```python
# Plan execution with monitoring
class AdaptivePlanExecutor:
    def __init__(self, planner: PlannerAgent, monitor: MonitoringAgent):
        self.planner = planner
        self.monitor = monitor

    async def execute_plan(self, plan: Plan):
        for step in plan.steps:
            # Execute step
            result = await self.execute_step(step)

            # Monitor progress
            status = await self.monitor.assess_progress(plan, result)

            # Adapt if needed
            if status.requires_replanning:
                plan = await self.planner.replan(
                    current_plan=plan,
                    new_constraints=status.constraints,
                    failure_analysis=status.failures
                )
```

## Running Examples

```bash
# Basic planning
poetry run python examples_new/04_specialized/planning/task_planner.py
poetry run python examples_new/04_specialized/planning/resource_planner.py

# Advanced planning
poetry run python examples_new/04_specialized/planning/hierarchical_planner.py
poetry run python examples_new/04_specialized/planning/collaborative_planner.py

# Production systems
poetry run python examples_new/04_specialized/planning/project_manager.py
poetry run python examples_new/04_specialized/planning/workflow_optimizer.py
```

## Planning Algorithms

### Classical Planning

- **STRIPS**: Basic action planning with preconditions and effects
- **PDDL**: Planning Domain Definition Language
- **GraphPlan**: Graph-based planning algorithm
- **Fast Forward (FF)**: Heuristic search planner

### Hierarchical Planning

- **HTN**: Hierarchical Task Networks
- **SHOP**: Simple Hierarchical Ordered Planner
- **HTN-DL**: Description Logic HTN Planning

### Modern Approaches

- **Monte Carlo Tree Search**: For stochastic domains
- **Reinforcement Learning**: Learning optimal policies
- **Large Language Models**: Natural language planning

## Reasoning Patterns

### Deductive Reasoning

```python
class DeductiveReasoner:
    def __init__(self):
        self.knowledge_base = []
        self.inference_engine = InferenceEngine()

    def add_rule(self, premise: str, conclusion: str):
        """Add logical rule to knowledge base."""
        self.knowledge_base.append(Rule(premise, conclusion))

    def infer(self, facts: List[str]) -> List[str]:
        """Derive new facts from existing knowledge."""
        return self.inference_engine.forward_chain(
            facts, self.knowledge_base
        )
```

### Abductive Reasoning

```python
class AbductiveReasoner:
    def find_explanations(self, observation: str, knowledge: List[str]) -> List[str]:
        """Find possible explanations for observation."""
        explanations = []
        for hypothesis in self.generate_hypotheses(observation):
            if self.explains(hypothesis, observation, knowledge):
                explanations.append(hypothesis)
        return explanations
```

### Causal Reasoning

```python
class CausalReasoner:
    def __init__(self):
        self.causal_graph = CausalGraph()

    def identify_causes(self, effect: str) -> List[str]:
        """Identify potential causes of an effect."""
        return self.causal_graph.get_parents(effect)

    def predict_intervention(self, intervention: str, target: str) -> float:
        """Predict effect of intervention on target."""
        return self.causal_graph.do_calculus(intervention, target)
```

## Constraint Handling

### Constraint Types

```python
from enum import Enum

class ConstraintType(Enum):
    RESOURCE = "resource"      # Limited resources
    TEMPORAL = "temporal"      # Time constraints
    LOGICAL = "logical"        # Logic constraints
    PREFERENCE = "preference"  # Soft constraints

class Constraint:
    def __init__(self, name: str, type: ConstraintType, condition: str):
        self.name = name
        self.type = type
        self.condition = condition
        self.violated = False
        self.penalty = 0.0
```

### Constraint Satisfaction

```python
class ConstraintSolver:
    def __init__(self, algorithm="backtracking"):
        self.algorithm = algorithm

    def solve(self, variables: List[Variable], constraints: List[Constraint]) -> Solution:
        """Find assignment that satisfies all constraints."""
        if self.algorithm == "backtracking":
            return self.backtrack_search(variables, constraints)
        elif self.algorithm == "local_search":
            return self.local_search(variables, constraints)
        elif self.algorithm == "constraint_propagation":
            return self.arc_consistency(variables, constraints)
```

## Common Use Cases

### Project Management

```python
# Software development project
project_planner = ProjectManagerAgent(
    name="dev_project_manager",
    methodologies=["agile", "waterfall"],
    resources=team_resources,
    constraints=project_constraints
)

# Plan development phases
development_plan = await project_planner.create_plan(
    goal="deliver_software_v1",
    requirements=requirements_doc,
    timeline=six_months
)
```

### Supply Chain Optimization

```python
# Supply chain planning
supply_planner = SupplyChainPlanner(
    name="logistics_optimizer",
    suppliers=supplier_network,
    warehouses=warehouse_locations,
    demand_forecast=demand_data
)

# Optimize distribution
distribution_plan = await supply_planner.optimize_distribution(
    products=product_catalog,
    constraints=capacity_constraints,
    objective="minimize_cost"
)
```

### Financial Planning

```python
# Investment planning
financial_planner = FinancialPlannerAgent(
    name="investment_advisor",
    market_data=market_feeds,
    risk_models=risk_assessment_models,
    regulations=compliance_rules
)

# Create investment strategy
investment_plan = await financial_planner.create_strategy(
    portfolio=current_portfolio,
    goals=investment_goals,
    risk_tolerance="moderate"
)
```

### Emergency Response

```python
# Crisis management
crisis_manager = CrisisManagerAgent(
    name="emergency_coordinator",
    resources=emergency_resources,
    protocols=response_protocols,
    communication=alert_systems
)

# Develop response plan
response_plan = await crisis_manager.develop_response(
    crisis_type="natural_disaster",
    severity="high",
    affected_areas=impact_zones
)
```

## Performance Optimization

### Planning Efficiency

1. **Heuristic Search**: Use domain-specific heuristics
2. **Pruning**: Eliminate infeasible branches early
3. **Caching**: Cache computed plans and subplans
4. **Parallelization**: Distribute planning computation

### Reasoning Speed

1. **Indexed Knowledge**: Efficient knowledge base indexing
2. **Compiled Rules**: Pre-compile frequent inference patterns
3. **Approximate Reasoning**: Trade accuracy for speed when appropriate
4. **Incremental Updates**: Update reasoning incrementally

### Memory Management

1. **Plan Compression**: Store plans efficiently
2. **Garbage Collection**: Clean up unused plan branches
3. **Working Memory**: Limit active reasoning context
4. **Streaming**: Process large problems in chunks

## Quality Metrics

### Planning Quality

- **Plan Optimality**: Distance from optimal solution
- **Plan Validity**: Constraint satisfaction rate
- **Plan Robustness**: Performance under uncertainty
- **Plan Efficiency**: Resource utilization effectiveness

### Reasoning Quality

- **Logical Consistency**: No contradictions in conclusions
- **Completeness**: Coverage of relevant inferences
- **Soundness**: Validity of reasoning steps
- **Relevance**: Focus on goal-relevant reasoning

## Best Practices

### Planning Design

1. **Modular Plans**: Break complex plans into manageable modules
2. **Flexible Constraints**: Design adaptable constraint systems
3. **Monitoring Integration**: Build in plan execution monitoring
4. **Failure Recovery**: Design robust failure handling

### Reasoning Architecture

1. **Layered Reasoning**: Separate different types of reasoning
2. **Uncertainty Handling**: Account for incomplete information
3. **Explanation Generation**: Provide reasoning explanations
4. **Knowledge Maintenance**: Keep knowledge bases current

### Testing Strategies

1. **Plan Validation**: Verify plans before execution
2. **Scenario Testing**: Test across diverse scenarios
3. **Stress Testing**: Test under resource constraints
4. **Ablation Studies**: Test individual components

## Common Challenges

### Computational Complexity

- **Problem**: Planning is computationally expensive
- **Solutions**: Approximation algorithms, heuristics, parallel processing

### Uncertainty Handling

- **Problem**: Real-world conditions are uncertain
- **Solutions**: Probabilistic planning, robust optimization, contingency planning

### Dynamic Environments

- **Problem**: Conditions change during execution
- **Solutions**: Monitoring systems, adaptive re-planning, online learning

### Knowledge Representation

- **Problem**: Encoding domain knowledge effectively
- **Solutions**: Structured representations, learning from examples, expert systems

## Next Steps

1. **[Games](../games/)** - Interactive planning environments
2. **[Business Applications](../business/)** - Enterprise planning systems
3. **[Advanced Examples](../../05_advanced/)** - Custom planning architectures

## Resources

- [Planning Algorithms Book](http://lavalle.pl/planning/)
- [PDDL Planning](https://planning.wiki/)
- [Fast Downward Planner](https://www.fast-downward.org/)
- [Classical Planning Papers](https://github.com/AI-Planning)
