# Agent Call Comparison: With and Without Tracing

## Without Tracing (Minimal Code)

```python
import os
import json
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

load_dotenv()

project_client = AIProjectClient(
    endpoint=os.getenv("AZURE_EXISTING_AIPROJECT_ENDPOINT"),
    credential=DefaultAzureCredential(),
)

agent = project_client.agents.get(agent_name=os.getenv("AZURE_EXISTING_AGENT_ID"))
openai_client = project_client.get_openai_client()

# Make an agent call - no tracing
response = openai_client.responses.create(
    input=[{"role": "user", "content": "What hikes are near Madrid?"}],
    extra_body={"agent": {"name": agent.name, "type": "agent_reference"}},
)

print(response.output_text)
```

**Result:** Agent call works, but **NO telemetry** is sent to Application Insights. You can't see traces, logs, or performance metrics.

---

## With Tracing (Current solution-prompt-simple.py)

```python
import os
import uuid  # ADDED FOR TRACING
import json
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.monitor.opentelemetry import configure_azure_monitor  # ADDED FOR TRACING
from opentelemetry.instrumentation.openai_v2 import OpenAIInstrumentor  # ADDED FOR TRACING

load_dotenv()

# TRACING: Generate session ID for correlation
SESSION_ID = str(uuid.uuid4())

# TRACING: Enable message content capture
os.environ['OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT'] = 'true'

project_client = AIProjectClient(
    endpoint=os.getenv("AZURE_EXISTING_AIPROJECT_ENDPOINT"),
    credential=DefaultAzureCredential(),
)

# TRACING: Configure Application Insights
ai_conn_str = project_client.telemetry.get_application_insights_connection_string()
configure_azure_monitor(connection_string=ai_conn_str)

# TRACING: Instrument OpenAI calls to create traces automatically
OpenAIInstrumentor().instrument()

agent = project_client.agents.get(agent_name=os.getenv("AZURE_EXISTING_AGENT_ID"))
openai_client = project_client.get_openai_client()

# Make an agent call - now with automatic tracing
response = openai_client.responses.create(
    input=[{"role": "user", "content": "What hikes are near Madrid?"}],
    extra_body={"agent": {"name": agent.name, "type": "agent_reference"}},
)

print(response.output_text)
print(f"Session ID: {SESSION_ID}")  # TRACING: For searching in App Insights
```

**Result:** Agent call works **AND** telemetry is automatically sent to Application Insights:
- Traces with operation details
- Performance metrics (latency, duration)
- Input/output messages (prompts and responses)
- Agent metadata (model, temperature, etc.)
- Correlation across multiple calls

---

## Key Differences Summary

| Aspect | Without Tracing | With Tracing |
|--------|----------------|--------------|
| **Imports** | Basic SDK only | + Azure Monitor + OpenTelemetry |
| **Configuration** | None | `configure_azure_monitor()` + `OpenAIInstrumentor()` |
| **Environment Variables** | None | `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT` |
| **Session Tracking** | Not available | Session ID for correlation |
| **Visibility in Portal** | None | Full traces in Application Insights |
| **Code Complexity** | ~15 lines | ~25 lines (+10 for tracing setup) |

---

## What You Get in Application Insights with Tracing

1. **Traces** showing each agent invocation with:
   - `gen_ai.agent.id` - Which agent was called
   - `gen_ai.response.model` - Which model was used (e.g., gpt-4o)
   - `gen_ai.response.id` - Unique response ID
   - `gen_ai.input.messages` - The full prompt sent
   - Output messages in events

2. **Dependencies** showing:
   - Duration of each call
   - Success/failure status
   - Timestamps

3. **Correlation** across:
   - Multiple agent calls in same session
   - Different services if part of larger application

4. **Searchability**:
   - Query by session ID
   - Filter by agent name
   - Analyze performance patterns
