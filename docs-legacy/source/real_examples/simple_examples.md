# Simple Agent Examples

Real examples and outputs from the simple agent.

## cached_simple

**Source**: `docs/source/agent_cache_simple.json`

```json
{
  "agent_type": "simple",
  "agent_name": "SimpleAgent",
  "agent_class": "haive.agents.simple.SimpleAgent",
  "generated_at": "2025-07-18T11:50:03.851783",
  "executions": [
    {
      "execution_summary": {
        "start_time": "2025-07-18T11:50:24.268484",
        "end_time": "2025-07-18T11:50:26.775342",
        "duration_seconds": 2.506858,
        "total_events": 1,
        "total_steps": 0,
        "state_updates": 1
      },
      "execution_trace": [],
      "state_history": [
        {
          "timestamp": "2025-07-18T11:50:26.775327",
          "state": {
            "input": "Hello! Can you introduce yourself and explain what you can do?",
            "output": "messages=[HumanMessage(content='Hello! Can you introduce yourself and explain what you can do?', additional_kwargs={}, response_metadata={}, id='44a3f4cf-fab4-41d8-bf72-0ee59d30f186'), AIMessage(content=\"Hello! I'm an AI assistant designed to help with a wide range of tasks. I can provide information, answer questions, assist with problem-solving, help with learning new topics, and offer recommendations. Whether you need help with homework, want to know the latest news, need advice on a project, or just want to chat, I'm here to assist you. Let me know how I can help!\", additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 80, 'prompt_tokens': 30, 'total_tokens': 110, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_name': 'gpt-4o-2024-08-06', 'system_fingerprint': 'fp_ee1d74bde0', 'prompt_filter_results': [{'prompt_index': 0, 'content_filter_results': {'hate': {'filtered': False, 'severity': 'safe'}, 'self_harm': {'filtered': False, 'severity': 'safe'}, 'sexual': {'filtered': False, 'severity': 'safe'}, 'violence': {'filtered': False, 'severity': 'safe'}}}], 'finish_reason': 'stop', 'logp

... (truncated)

```

---

## cached_simple

**Source**: `docs/scripts/cache_generation/agent_cache_simple.json`

```json
{
  "agent_type": "simple",
  "agent_name": "SimpleAgent",
  "agent_class": "haive.agents.simple.SimpleAgent",
  "generated_at": "2025-07-18T11:50:03.851783",
  "executions": [
    {
      "execution_summary": {
        "start_time": "2025-07-18T11:50:24.268484",
        "end_time": "2025-07-18T11:50:26.775342",
        "duration_seconds": 2.506858,
        "total_events": 1,
        "total_steps": 0,
        "state_updates": 1
      },
      "execution_trace": [],
      "state_history": [
        {
          "timestamp": "2025-07-18T11:50:26.775327",
          "state": {
            "input": "Hello! Can you introduce yourself and explain what you can do?",
            "output": "messages=[HumanMessage(content='Hello! Can you introduce yourself and explain what you can do?', additional_kwargs={}, response_metadata={}, id='44a3f4cf-fab4-41d8-bf72-0ee59d30f186'), AIMessage(content=\"Hello! I'm an AI assistant designed to help with a wide range of tasks. I can provide information, answer questions, assist with problem-solving, help with learning new topics, and offer recommendations. Whether you need help with homework, want to know the latest news, need advice on a project, or just want to chat, I'm here to assist you. Let me know how I can help!\", additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 80, 'prompt_tokens': 30, 'total_tokens': 110, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_name': 'gpt-4o-2024-08-06', 'system_fingerprint': 'fp_ee1d74bde0', 'prompt_filter_results': [{'prompt_index': 0, 'content_filter_results': {'hate': {'filtered': False, 'severity': 'safe'}, 'self_harm': {'filtered': False, 'severity': 'safe'}, 'sexual': {'filtered': False, 'severity': 'safe'}, 'violence': {'filtered': False, 'severity': 'safe'}}}], 'finish_reason': 'stop', 'logp

... (truncated)

```

---
