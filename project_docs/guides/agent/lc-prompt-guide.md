# The Complete Markdown Guide to Advanced Prompt Templates in LangChain

> **Purpose**
> This living document distills best-practice patterns for building, scaling, and maintaining sophisticated prompt templates in LangChain. It focuses on **string-level** and **chat-level** templates, highlights _partial_ and _optional_ variables, and shows how to bind or inject values from agent or graph state.

---

## 1. Why Templates Matter

Modern LLM agents are only as reliable as the instructions they receive. Prompt templates give you:

1. **Reusability** – Centralise canonical instructions instead of scattering `"You are…"` strings throughout code[33].
2. **Safety** – Define an allow-list of required variables; missing keys raise early errors[7].
3. **Cost control** – Inject only the most recent `n` messages via `MessagesPlaceholder` to keep context windows lean[38].
4. **Observability** – Store template versions in a prompt CMS (e.g. Langfuse) and track performance across deployments[65].

---

## 2. Anatomy of a High-Quality Template

A mature template normally contains six logical blocks:

| #   | Block                       | Required? | Typical Size                    |
| --- | --------------------------- | --------- | ------------------------------- |
| 1   | **Identity / System role**  | ✓         | 1-3 sentences                   |
| 2   | **Task & Success Criteria** | ✓         | 1 paragraph                     |
| 3   | **Operational Constraints** | ✓         | bullet list                     |
| 4   | **Context Variables**       | ✓         | placeholders (`{product_spec}`) |
| 5   | **Few-Shot Examples**       | ⬤         | 2-5 exemplars                   |
| 6   | **Output Schema**           | ✓         | JSON, Markdown, etc.            |

⬤ = recommended for specialised reasoning tasks.

```python
from langchain_core.prompts import PromptTemplate

template = """
You are {agent_role}.
Goal: {objective}
{constraints}

Examples:
{few_shots}

When you respond use this JSON schema:
{output_schema}
"""

prompt = PromptTemplate(
    input_variables=[
        "agent_role", "objective", "constraints",
        "few_shots", "output_schema"
    ]
)
```

---

## 3. Partial Variables

Partial variables let you _pre-bind_ values that you discover early in a chain and forward the partially-filled template downstream[1][13].

### 3.1 Binding Static Strings

```python
from langchain_core.prompts import PromptTemplate

base = PromptTemplate.from_template("{salutation} {name}! How can I help?")

with_salutation = base.partial(salutation="Hello")
print(with_salutation.format(name="Ada"))
# » Hello Ada! How can I help?
```

### 3.2 Binding Functions (dynamic)

```python
import datetime as dt

get_date = lambda: dt.date.today().isoformat()

prompt = PromptTemplate(
    template="Today is {date}. Question: {question}",
    input_variables=["question"],
    partial_variables={"date": get_date}
)
```

_The function is executed at format-time, so the value is always fresh._

### 3.3 Advantages

- Avoids plumbing the same constant through every node.
- Encourages composable templates – swap the dynamic part in tests.

---

## 4. Optional Variables

Optional variables are **place-holders that _may_ be omitted** without raising a formatting error[7][17]. They are invaluable when context is present only in some turns (e.g. `tool_output`).

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts.chat import MessagesPlaceholder

chat = ChatPromptTemplate([
    ("system", "You are a data analyst."),
    MessagesPlaceholder("history", optional=True),
    ("human", "{question}")
],
    optional_variables=["history"],
)

chat.invoke({"question": "Show sales by month."})  # no history works!
```

⚠️ GitHub issue #24884 notes that some older versions mis-handled `optional_variables`. Upgrade to ≥ 0.2.25 to ensure correct behaviour[2].

---

## 5. Populating Variables from State

### 5.1 SequentialChain State

Use `output_key` / `input_key` mappings to thread values between steps[3].

### 5.2 Memory Injection

When using `ConversationBufferMemory`, declare a matching placeholder:

```python
prompt = ChatPromptTemplate([
    ("system", "You are helpful."),
    MessagesPlaceholder("history"),
    ("human", "{input}")
])
```

LangChain will auto-populate `history` every call.

### 5.3 LangGraph Annotated State

With `InjectedState`, tools can read parts of the graph state without exposing internals to the model[12].

---

## 6. Template Formats

| Format                   | Pros                                                   | Cons                                               |
| ------------------------ | ------------------------------------------------------ | -------------------------------------------------- |
| **f-string** _(default)_ | Fast, native Python, safe                              | No loops/conditionals when rendering               |
| **Jinja2**               | Powerful control flow, ideal for JSON or lists[52][59] | Higher risk; never accept from untrusted users[60] |

Use `template_format="jinja2"` if you need constructs like:

```jinja2
{% for item in todos %}- {{loop.index}}. {{item}}
{% endfor %}
```

---

## 7. System vs. Human Messages

For chat models separate _instructions_ from _user queries_:

```python
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a compliance auditor."),
    ("human", "Audit the following text:\n{text}")
])
```

This alignment matches OpenAI’s recommended API roles and yields more predictable completions[21].

---

## 8. Design Checklist

1. **Declare all input, partial, and optional variables explicitly.** Avoid silent shadowing.
2. **Keep identity blocks short.** Models ignore overly long role descriptions.
3. **Fail fast.** Let missing _required_ variables raise an error at `format()` time.
4. **Document version hashes.** Store a `template_id` alongside agent logs for rollback.
5. **Unit-test** every template with edge-case dictionaries.

---

## 9. Troubleshooting FAQ

| Symptom                           | Likely Cause                                   | Fix                                        |
| --------------------------------- | ---------------------------------------------- | ------------------------------------------ |
| `KeyError: 'history'`             | Placeholder not marked optional                | Add `optional=True` or supply value        |
| Extra blank lines in Jinja output | Jinja keeps newline after blocks               | Enable `trim_blocks` & `lstrip_blocks`[64] |
| Optional var still required       | Upgrade to LangChain >= 0.2.25 (bug #24884)[2] |
| JSON braces collide with f-string | Switch to `jinja2` format[59]                  |

---

## 10. Reference Snippets

- **Partial variable docs** – LangChain Python[1] / JS[13].
- **Optional variables API** – `PromptTemplate.optional_variables`[7].
- **MessagesPlaceholder** for dynamic history[38].
- **State injection** – `InjectedState` annotation[12].

---

### Contributing

Spotted an error or improvement? Open a PR against `lc-prompt-guide.md` with the rationale and a test.

---

_Last updated: 2025-07-18_
