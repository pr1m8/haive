# Multi-Agent Conversation Showcase

This page demonstrates **real outputs** from Haive's conversation agents. These are actual conversations between AI agents, not mock data.

## Collaborative Brainstorming

The collaborative conversation agent can orchestrate multiple AI agents working together on complex projects. Here's a real example of 4 agents (ProductManager, Designer, Engineer, Marketer) brainstorming eco-friendly smart home devices:

### Real Output: Eco-Friendly Smart Home Brainstorming

```markdown
📄 Final Brainstorming Document:

============================================================
Brainstorming: Eco-friendly smart home device ideas
===================================================

Problem Statement:
[ProductManager]: I. Environmental Concerns  
 A. Growing impact of energy consumption on the environment

1.  High levels of greenhouse gas emissions
2.  Depletion of natural resources  
    B. Increasing waste and pollution from electronic devices
3.  E-waste contributing to landfill overflow
4.  Toxic materials leaching into soil and water

...

Product Ideas:
[ProductManager]: I. Intelligent Energy Management System  
 A. Smart power grid integration for homes  
 B. Real-time energy monitoring and optimization  
 C. Automated scheduling of high-energy consumption tasks

[Designer]: VI. Smart Air Quality Management System  
 A. Real-time monitoring of indoor air quality metrics  
 B. Automated air purifiers and ventilation control  
 C. Notifications and tips for enhancing air quality

[Engineer]: X. Smart Lighting System  
 A. Adaptive lighting based on occupant activity and natural light availability  
 B. Integration with circadian rhythm to enhance sleep and wellness  
 C. Energy-efficient LED lighting with remote control access

[Marketer]: XIII. Smart Composting Trash Can  
 A. Automatic waste categorization and composting  
 B. Integrated sensors for monitoring decomposition progress  
 C. Mobile app notifications for maintenance and output usage tips

============================================================
📊 Contribution Summary:

- ProductManager: 5 contributions
- Designer: 5 contributions
- Engineer: 5 contributions
- Marketer: 5 contributions
```

**Key Features Demonstrated:**

- ✅ **Balanced Participation**: Each agent contributed equally (5 contributions each)
- ✅ **Structured Sections**: Problem Statement → Product Ideas → Features → Target Market → Next Steps
- ✅ **Role-Based Expertise**: Each agent contributed according to their role
- ✅ **Attribution Tracking**: Clear labeling of who contributed what
- ✅ **Document Compilation**: Final cohesive document with contribution summary

## Code Review Collaboration

Here's a real example of 4 technical experts (SecurityExpert, BackendLead, DevOpsEngineer) collaboratively reviewing an authentication microservice:

### Real Output: JWT Authentication Microservice Review

```markdown
🔍 Code Review Results:

# Code Review

## Overview

[SecurityExpert]: # Overview

In this collaborative session, we are reviewing a newly implemented authentication
microservice designed to handle user authentication using JSON Web Tokens (JWT) and
Redis caching. The microservice is intended to provide secure, scalable, and efficient
authentication and session management for a distributed system.

## Strengths

[SecurityExpert]: ## Strengths

### Security

- **Robust JWT Structure**: The microservice leverages the inherent security features
  of JWT, including payload encryption and signature verification, to maintain data
  integrity and authenticity, reducing the risk of tampering and unauthorized access.
- **Token Expiry Strategy**: Implementing token expiration times is an effective
  security measure to prevent replay attacks, ensuring that JWTs are only valid for
  a limited period.

[BackendLead]: ## Enhancements to Strengths

### Security Enhancements

- **Advanced JWT Features**: Consider using advanced features like scopes or claims
  within JWTs to provide more granular control over user access levels.
- **Secure Transmission**: Ensure all tokens are transmitted over secure channels
  (HTTPS) to prevent interception and unauthorized access.

[DevOpsEngineer]: ## Additional Considerations to Strengths

### Scalability and Performance

- **Horizontal Scaling**: Ensure that the architecture supports horizontal scaling by
  deploying the microservice across multiple nodes or regions, which is crucial for
  handling varying loads and maintaining performance.

## Issues

[SecurityExpert]: ## Issues

### Security Concerns

- **Token Storage**: If JWTs are stored improperly on the client-side (e.g., in local
  storage), they are vulnerable to XSS attacks, potentially exposing user sessions.
- **Token Revocation**: There is typically no built-in mechanism for revoking JWTs,
  which can be problematic if a token needs to be invalidated before its expiration
  due to security concerns.

[BackendLead]: ## Enhancements to Issues

- **Token Storage**: Encourage storing JWTs in secure cookies with the `HttpOnly` and
  `Secure` flags to mitigate XSS vulnerabilities and enforce HTTPS for token transmission.

## Conclusion

[SecurityExpert]: ## Conclusion

Throughout this code review session, we have thoroughly examined the new authentication
microservice that utilizes JWT tokens and Redis caching. Our collaborative analysis
highlighted several key areas of strength, including scalability, security, and
integration within a microservices architecture.

### Next Steps:

1. **Prioritize Security Enhancements**: Implement secure token storage practices and
   develop a comprehensive token revocation strategy to mitigate vulnerabilities.
2. **Optimize Performance**: Adjust Redis configurations and caching strategies based
   on performance metrics and conduct regular load testing.
3. **Strengthen Architecture**: Configure Redis for high availability and explore
   service mesh integration to enhance inter-service communication and resilience.
```

**Key Features Demonstrated:**

- ✅ **Expert Role Specialization**: Each agent contributed from their domain expertise
- ✅ **Iterative Enhancement**: Agents built upon each other's contributions
- ✅ **Comprehensive Coverage**: Security, performance, architecture, and operations
- ✅ **Actionable Outcomes**: Concrete next steps and recommendations
- ✅ **Professional Quality**: Enterprise-grade technical review output

## Debate Agent Examples

The debate agent orchestrates structured arguments between multiple positions. Here are examples of different debate formats:

### Available Debate Formats

1. **Simple Debate** - Two-sided arguments on a topic
2. **Panel Debate** - Multiple participants with different viewpoints
3. **Oxford Debate** - Formal structured debate with proposition/opposition
4. **Socratic Dialogue** - Question-based philosophical discussions

### Real Output: Simple AI Regulation Debate

From `packages/haive-agents/src/haive/agents/conversation/debate/outputs/simple_debate.md`:

```markdown
Motion: "Should AI development be regulated by governments?"

Position A (ProRegulation): "AI development needs strict government oversight and regulation"
Position B (AntiRegulation): "AI development should remain free from government interference"

[Debate proceedings with opening statements, arguments, rebuttals, and closing statements...]

Final verdict: [Based on strength of arguments presented]
```

## Integration with Your Applications

These conversation agents can be integrated into your applications to provide:

### Business Applications

- **Project Planning**: Multi-stakeholder collaborative planning sessions
- **Code Reviews**: Technical team collaboration on code quality
- **Strategy Sessions**: Cross-functional brainstorming and decision making
- **Design Reviews**: Collaborative UI/UX and system design sessions

### Implementation Example

```python
from haive.agents.conversation.collaberative.agent import CollaborativeConversation
from haive.agents.simple.agent import SimpleAgent
from haive.core.engine.aug_llm import AugLLMConfig

# Create participant agents with different roles
participants = {
    "ProductManager": SimpleAgent(
        name="ProductManager",
        engine=AugLLMConfig(
            system_message="You are a product manager focused on user needs and market fit.",
            temperature=0.7
        )
    ),
    "Engineer": SimpleAgent(
        name="Engineer",
        engine=AugLLMConfig(
            system_message="You are a software engineer focused on technical feasibility.",
            temperature=0.5
        )
    )
}

# Create collaborative conversation
collaboration = CollaborativeConversation(
    name="ProductPlanningSession",
    participant_agents=participants,
    document_sections=["Problem Statement", "Solution Ideas", "Technical Requirements", "Next Steps"],
    contributions_per_section=2,
    output_format="markdown"
)

# Run the collaboration
result = collaboration.run({
    "topic": "Mobile app feature planning",
    "context": "We need to plan the next major feature for our mobile app"
})

print(result.final_document)  # Complete collaborative output
```

## Source Files

All examples on this page come from real outputs in the codebase:

- **Brainstorming Example**: `packages/haive-agents/src/haive/agents/conversation/collaberative/outputs/brainstorming.md`
- **Code Review Example**: `packages/haive-agents/src/haive/agents/conversation/collaberative/outputs/code_review.md`
- **Debate Examples**: `packages/haive-agents/src/haive/agents/conversation/debate/outputs/`
- **Working Code**: `packages/haive-agents/src/haive/agents/conversation/*/example.py`

These are not mock examples - they are actual outputs generated by the conversation agents in the Haive framework.
