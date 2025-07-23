# React Agent Examples

Real examples and outputs from the react agent.

## cached_react

**Source**: `docs/source/agent_cache_react.json`

```json
{
  "agent_type": "react",
  "agent_name": "ReactAgent",
  "agent_class": "haive.agents.react.ReactAgent",
  "generated_at": "2025-07-18T12:10:32.945346",
  "executions": [
    {
      "execution_summary": {
        "start_time": "2025-07-18T12:10:53.436297",
        "end_time": "2025-07-18T12:10:56.593453",
        "duration_seconds": 3.157156,
        "total_events": 2,
        "total_steps": 0,
        "state_updates": 1
      },
      "execution_trace": [],
      "state_history": [
        {
          "timestamp": "2025-07-18T12:10:56.593449",
          "state": {
            "input": "What is 15 * 23 + 47? Please calculate step by step.",
            "output": "messages=[HumanMessage(content='What is 15 * 23 + 47? Please calculate step by step.', additional_kwargs={}, response_metadata={}, id='2c5059dd-3420-4f2a-84d3-f2bc673ac7d6'), AIMessage(content='To calculate \\\\(15 \\\\times 23 + 47\\\\) step by step, follow these steps:\\n\\n1. First, calculate the multiplication:\\n   \\\\[\\n   15 \\\\times 23 = 345\\n   \\\\]\\n\\n2. Next, add the result of the multiplication to 47:\\n   \\\\[\\n   345 + 47 = 392\\n   \\\\]\\n\\nTherefore, \\\\(15 \\\\times 23 + 47 = 392\\\\).', additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 94, 'prompt_tokens': 85, 'total_tokens': 179, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_name': 'gpt-4o-2024-08-06', 'system_fingerprint': 'fp_ee1d74bde0', 'prompt_filter_results': [{'prompt_index': 0, 'content_filter_results': {'hate': {'filtered': False, 'severity': 'safe'}, 'self_harm': {'filtered': False, 'severity': 'safe'}, 'sexual': {'filtered': False, 'severity': 'safe'}, 'violence': {'filtered': False, 'severity': 'safe'}}}], 'finish_reason': 'stop', 'logprobs': None, 'content_filter_results': {'hate': {'filtered': False, 'se

... (truncated)

```

---

## cached_react

**Source**: `docs/scripts/cache_generation/agent_cache_react.json`

```json
{
  "agent_type": "react",
  "agent_name": "ReactAgent",
  "agent_class": "haive.agents.react.ReactAgent",
  "generated_at": "2025-07-18T12:10:32.945346",
  "executions": [
    {
      "execution_summary": {
        "start_time": "2025-07-18T12:10:53.436297",
        "end_time": "2025-07-18T12:10:56.593453",
        "duration_seconds": 3.157156,
        "total_events": 2,
        "total_steps": 0,
        "state_updates": 1
      },
      "execution_trace": [],
      "state_history": [
        {
          "timestamp": "2025-07-18T12:10:56.593449",
          "state": {
            "input": "What is 15 * 23 + 47? Please calculate step by step.",
            "output": "messages=[HumanMessage(content='What is 15 * 23 + 47? Please calculate step by step.', additional_kwargs={}, response_metadata={}, id='2c5059dd-3420-4f2a-84d3-f2bc673ac7d6'), AIMessage(content='To calculate \\\\(15 \\\\times 23 + 47\\\\) step by step, follow these steps:\\n\\n1. First, calculate the multiplication:\\n   \\\\[\\n   15 \\\\times 23 = 345\\n   \\\\]\\n\\n2. Next, add the result of the multiplication to 47:\\n   \\\\[\\n   345 + 47 = 392\\n   \\\\]\\n\\nTherefore, \\\\(15 \\\\times 23 + 47 = 392\\\\).', additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 94, 'prompt_tokens': 85, 'total_tokens': 179, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_name': 'gpt-4o-2024-08-06', 'system_fingerprint': 'fp_ee1d74bde0', 'prompt_filter_results': [{'prompt_index': 0, 'content_filter_results': {'hate': {'filtered': False, 'severity': 'safe'}, 'self_harm': {'filtered': False, 'severity': 'safe'}, 'sexual': {'filtered': False, 'severity': 'safe'}, 'violence': {'filtered': False, 'severity': 'safe'}}}], 'finish_reason': 'stop', 'logprobs': None, 'content_filter_results': {'hate': {'filtered': False, 'se

... (truncated)

```

---

