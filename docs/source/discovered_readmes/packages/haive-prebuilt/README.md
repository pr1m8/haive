# Haive Prebuilt - Domain-Specific Agent Solutions

## Overview

Haive Prebuilt provides 40+ ready-to-deploy agents for specific business domains and use cases. These are complete, production-ready solutions built on Haive's agent architectures, configured and optimized for particular industries and applications.

## Domain Solutions

### 1. Business & Startup Solutions

**Company Researcher**

- Deep company analysis with financial data, news, competitors
- Integrates multiple data sources (APIs, web, databases)
- Outputs comprehensive company profiles

**Startup Suite**

- **Ideation Agent**: Generates and validates startup ideas
- **Market Research**: Analyzes market size, competition, trends
- **Business Model Canvas**: Creates strategic business plans
- **Pitch Deck Generator**: Builds investor-ready presentations

**Sales Call Analyzer**

- Transcribes and analyzes sales conversations
- Identifies key moments, objections, successful tactics
- Provides coaching recommendations

### 2. Content & Creative Solutions

**Blog Writer Agent**

- SEO-optimized content generation
- Researches topics and creates outlines
- Includes meta descriptions and keywords

**Podcast Generator**

- Complete podcast production pipeline
- Generates scripts, interview questions
- Creates show notes and timestamps

**GIF Generator**

- Creates animated GIFs from descriptions
- Optimizes for social media platforms

**Business Meme Generator**

- Creates viral business content
- Understands current trends and formats

### 3. Legal & Compliance Solutions

**Contract Analysis**

- Reviews contracts for risks and opportunities
- Compares against standard templates
- Highlights unusual clauses

**Clause AI**

- Generates specific legal clauses
- Ensures compliance with regulations
- Multiple jurisdiction support

**EU Green Compliance**

- Checks compliance with EU environmental regulations
- Generates compliance reports
- Suggests remediation steps

### 4. Professional Services

**Project Manager**

- Creates project plans and timelines
- Tracks dependencies and resources
- Generates status reports

**Career Assistant**

- Resume optimization
- Job search strategy
- Interview preparation
- Career path planning

**Customer Support**

- Automated tier-1 support
- Escalation detection
- Knowledge base integration

### 5. Academic & Research

**Academic Task Learning**

- Helps students understand complex topics
- Creates study guides and summaries
- Generates practice questions

**Essay Grading**

- Automated grading with rubrics
- Detailed feedback generation
- Plagiarism detection

**Scientific Paper Agent**

- Helps write research papers
- Formats citations correctly
- Checks methodology sections

**Systematic Review**

- Literature search and analysis
- PRISMA compliance
- Meta-analysis support

### 6. E-commerce & Consumer

**Shop Genie**

- Product recommendation engine
- Price comparison across platforms
- Review analysis and summarization

**Car Buyer Agent**

- Compares vehicles based on needs
- Analyzes reviews and reliability
- Negotiation tips and fair pricing

### 7. Travel & Lifestyle

**Travel Planner**

- Creates detailed itineraries
- Books accommodations and transport
- Local recommendations and tips

**Weather Disaster Management**

- Emergency response planning
- Risk assessment for locations
- Evacuation route planning

### 8. Development & Technical

**E2E Testing Agent**

- Generates end-to-end test scenarios
- Creates test data
- Identifies edge cases

**Prompt Writing Agent**

- Optimizes prompts for different models
- A/B testing recommendations
- Prompt library management

**DB Discovery**

- Explores database schemas
- Generates documentation
- Identifies optimization opportunities

### 9. Specialized Analytics

**Content Intelligence**

- Content strategy recommendations
- Performance analysis
- Competitor content analysis

**Open Researcher**

- General-purpose research on any topic
- Multiple source verification
- Bias detection and mitigation

**People Researcher**

- Comprehensive profiles of individuals
- Professional history and achievements
- Public information aggregation

## Key Features

### Industry-Specific Optimizations

Each agent is pre-configured with:

- Domain-specific prompts
- Relevant tool integrations
- Industry knowledge bases
- Compliance requirements

### Ready-to-Deploy

```python
from haive.prebuilt import CompanyResearcher

agent = CompanyResearcher()
report = agent.analyze("Apple Inc")
# Returns complete company analysis
```

### Customizable

```python
# Adjust for specific needs
agent = BlogWriter(
    style="technical",
    target_audience="developers",
    seo_focus=True
)
```

### Integration-Ready

- API endpoints included
- Webhook support
- Database connections
- Third-party service integrations

## Use Cases by Industry

### Finance

- Company analysis
- Market research
- Compliance checking
- Risk assessment

### Legal

- Contract review
- Compliance verification
- Document generation
- Case research

### Marketing

- Content creation
- SEO optimization
- Social media management
- Market analysis

### Education

- Automated grading
- Study material generation
- Research assistance
- Learning optimization

### Healthcare

- Systematic reviews
- Research synthesis
- Compliance checking
- Patient education

## Deployment Options

### SaaS Mode

```python
# Deploy as service
from haive.prebuilt import deploy_as_service

deploy_as_service(
    agent=ContractAnalysis(),
    port=8080,
    auth=True
)
```

### Embedded Mode

```python
# Embed in existing application
from haive.prebuilt import embed

analyzer = embed(
    SalesCallAnalyzer(),
    into=your_crm_system
)
```

### Batch Processing

```python
# Process multiple items
agent = InvoiceProcessor()
results = agent.batch_process(invoice_folder)
```

## Best Practices

1. **Start with Defaults**: Each agent has optimized default settings
2. **Monitor Usage**: Built-in analytics and logging
3. **Iterate Based on Feedback**: Continuous improvement loops
4. **Respect Rate Limits**: Automatic throttling included
5. **Handle Errors Gracefully**: Comprehensive error handling

_Note: Each prebuilt agent includes documentation, examples, and deployment guides. These are production-tested solutions used by real businesses._
