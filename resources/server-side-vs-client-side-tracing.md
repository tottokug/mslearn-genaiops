# Server-Side vs Client-Side Tracing in Microsoft Foundry

## Overview

When working with Microsoft Foundry tracing, you'll encounter two types of instrumentation: **server-side** and **client-side**. Understanding the difference is crucial for implementing comprehensive observability in your AI applications.

---

## Definitions

### Server-Side Tracing
**Where it runs**: Microsoft Foundry's cloud infrastructure (Azure)

**What it captures**: Automatic instrumentation of agents, workflows, and LLM interactions that run on Microsoft's servers

**Setup required**: Minimal - just enable Application Insights in your Foundry project

**Code changes**: None - completely automatic

### Client-Side Tracing
**Where it runs**: Your application environment (your laptop, servers, containers, or wherever your app runs)

**What it captures**: Custom instrumentation of your application code that calls Foundry agents

**Setup required**: Install SDKs and add instrumentation code

**Code changes**: Yes - you need to add tracing code to your application

---

## Visual Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                       YOUR ENVIRONMENT                          │
│                      (Client-Side)                              │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Your Application Code                                   │  │
│  │  ┌────────────────────────────────────────────────────┐  │  │
│  │  │ import opentelemetry                               │  │  │
│  │  │ from azure.ai.projects import AIProjectClient      │  │  │
│  │  │                                                     │  │  │
│  │  │ # YOUR instrumentation code here                   │  │  │
│  │  │ # Traces: API calls, custom logic, user actions    │  │  │
│  │  └────────────────────────────────────────────────────┘  │  │
│  │              │                          │                  │  │
│  │              │                          │                  │  │
│  │              │ Agent API Request        │ Client Traces    │  │
│  │              │ (HTTPS)                  │ (OpenTelemetry)  │  │
│  │              │                          │                  │  │
│  └──────────────│──────────────────────────│──────────────────┘  │
└─────────────────│──────────────────────────│─────────────────────┘
                  │                          │
                  ▼                          │
┌───────────────────────────────────────────┐│
│    MICROSOFT FOUNDRY CLOUD                ││
│      (Server-Side)                        ││
│                                           ││
│  ┌────────────────────────────────────┐  ││
│  │  Foundry Agent Service             │  ││
│  │  ┌──────────────────────────────┐  │  ││
│  │  │ ✓ Auto Instrumentation       │  │  ││
│  │  │                              │  │  ││
│  │  │ • Prompt agents              │  │  ││
│  │  │ • Host agents                │  │  ││
│  │  │ • Workflows                  │  │  ││
│  │  │ • LLM calls                  │  │  ││
│  │  │ • Tool executions            │  │  ││
│  │  └──────────────────────────────┘  │  ││
│  └────────────────────────────────────┘  ││
│                  │                        ││
│                  │ Server Traces          ││
│                  │ (OpenTelemetry)        ││
└──────────────────│────────────────────────┘│
                   │                         │
                   ▼                         ▼
       ┌────────────────────────────────────────────────┐
       │    Azure Application Insights                  │
       │    (Unified Trace Storage - 90 days)           │
       │                                                │
       │  ┌──────────────────────────────────────────┐ │
       │  │  Client Traces + Server Traces           │ │
       │  │  (Correlated by trace context)           │ │
       │  └──────────────────────────────────────────┘ │
       └────────────────────────────────────────────────┘
```

**Key Point**: Both client and server send traces **independently and directly** to Application Insights. They don't go through each other - they are parallel telemetry streams that get correlated using trace context (correlation IDs).

---

## Request Flow Example

Here's what happens when a user interacts with your AI application:

```
User clicks button in your web app
         │
         │ CLIENT-SIDE TRACE: "Button clicked, calling agent"
         ▼
Your code calls Foundry agent API
         │
         │ ← API call over internet →
         ▼
Foundry agent receives request
         │
         │ SERVER-SIDE TRACE: "Agent started"
         │ SERVER-SIDE TRACE: "Prompt sent to LLM"
         │ SERVER-SIDE TRACE: "LLM response received"
         │ SERVER-SIDE TRACE: "Tool called: search_database"
         │ SERVER-SIDE TRACE: "Agent completed"
         ▼
Response sent back to your app
         │
         │ CLIENT-SIDE TRACE: "Response received, showing to user"
         ▼
User sees result
```

---

## Comparison Table

| Aspect | Server-Side Tracing | Client-Side Tracing |
|--------|-------------------|---------------------|
| **Location** | Microsoft Foundry cloud | Your application environment |
| **Setup Complexity** | Simple (enable in portal) | Moderate (install SDKs, add code) |
| **Code Changes** | None required | Required |
| **What It Traces** | Agent logic, LLM calls, workflows, tools | Your app logic, API calls, user interactions |
| **Automatic** | ✅ Yes | ❌ No (manual instrumentation) |
| **Captures** | • Prompt agent execution<br>• Host agent execution<br>• Workflow steps<br>• LLM requests/responses<br>• Tool calls | • User actions<br>• Business logic<br>• API calls to Foundry<br>• Custom events<br>• Application errors |
| **Data Storage** | Application Insights (automatic) | Application Insights (via SDK) |
| **Retention** | 90 days | 90 days |

---

## When to Use Each

### Use Server-Side Tracing When:
- ✅ You want to understand what happens inside your Foundry agents
- ✅ You need to debug prompt engineering issues
- ✅ You want to monitor LLM performance and token usage
- ✅ You need to see tool execution details
- ✅ You want zero-code observability

### Use Client-Side Tracing When:
- ✅ You need to trace your application's logic
- ✅ You want to monitor end-to-end user journeys
- ✅ You need to capture custom business events
- ✅ You want to correlate user actions with agent behavior
- ✅ You're debugging issues in your application code

### Use Both When:
- ✅ You want complete observability (recommended!)
- ✅ You need to see the entire request flow from user to agent and back
- ✅ You're optimizing end-to-end performance
- ✅ You need to troubleshoot complex issues spanning client and server

---

## Setup Guide

### Server-Side Tracing Setup

1. **Enable Application Insights in Foundry Project**
   - Navigate to your Foundry project settings
   - Go to Monitor settings
   - Create or connect an Application Insights resource
   - Tracing is now enabled automatically!

2. **Verify Access**
   - Ensure you have the **Log Analytics Reader** role
   - Navigate to the **Traces** tab in your Foundry project
   - View traces for agents and workflows

**That's it!** No code changes needed.

---

### Client-Side Tracing Setup

1. **Install Required Packages**
   ```bash
   pip install azure-ai-projects azure-identity opentelemetry-sdk azure-core-tracing-opentelemetry
   ```

2. **Add Instrumentation to Your Code**
   ```python
   from azure.ai.projects import AIProjectClient
   from azure.identity import DefaultAzureCredential
   from opentelemetry import trace
   from azure.core.tracing.ext.opentelemetry_span import OpenTelemetrySpan
   
   # Initialize tracing
   tracer = trace.get_tracer(__name__)
   
   # Your application code
   with tracer.start_as_current_span("user_request") as span:
       span.set_attribute("user_id", "12345")
       
       # Call Foundry agent
       client = AIProjectClient(
           credential=DefaultAzureCredential(),
           # ... your config
       )
       
       response = client.agents.run(...)
       
       span.set_attribute("response_length", len(response))
   ```

3. **Configure Trace Export**
   - Set up OpenTelemetry to send traces to Application Insights
   - Use the same Application Insights resource as your Foundry project

4. **View Combined Traces**
   - Navigate to **Traces** tab in Foundry portal
   - See both your app traces and agent traces in one view

---

## Local Development

For local development and debugging, you can use **AI Toolkit for VS Code**:

```
┌─────────────────────────────────────┐
│      VS Code (Your Laptop)          │
│                                     │
│  ┌──────────────────────────────┐  │
│  │  Your Application Code       │  │
│  └──────────┬───────────────────┘  │
│             │                       │
│             │ Traces                │
│             ▼                       │
│  ┌──────────────────────────────┐  │
│  │  Local OTLP Collector        │  │
│  │  (AI Toolkit)                │  │
│  └──────────┬───────────────────┘  │
│             │                       │
│             │ Display               │
│             ▼                       │
│  ┌──────────────────────────────┐  │
│  │  Trace Viewer in VS Code     │  │
│  │  (Instant feedback!)         │  │
│  └──────────────────────────────┘  │
└─────────────────────────────────────┘
```

**Benefits**:
- No cloud connection needed
- Instant trace viewing
- Faster debugging cycle
- Works with multiple AI frameworks

---

## Best Practices

### 1. Start with Server-Side
Always enable server-side tracing first. It's free, automatic, and gives you immediate insights into your agents.

### 2. Add Client-Side for Production
For production applications, implement client-side tracing to get the complete picture of user journeys.

### 3. Use Correlation IDs
Pass correlation IDs between client and server to link traces together:
```python
span.set_attribute("correlation_id", request_id)
```

### 4. Don't Over-Instrument
Focus on tracing important operations:
- ✅ API calls to Foundry
- ✅ Major business logic steps
- ✅ Error conditions
- ❌ Every single line of code

### 5. Add Meaningful Attributes
Enrich traces with context:
```python
span.set_attribute("user_id", user_id)
span.set_attribute("conversation_id", conv_id)
span.set_attribute("model_version", "gpt-4")
```

---

## Troubleshooting Scenarios

### Scenario 1: Slow Agent Response
**What to check:**
- **Server-side traces**: LLM latency, tool execution time
- **Client-side traces**: Network latency, request preparation time

### Scenario 2: Incorrect Agent Output
**What to check:**
- **Server-side traces**: Prompt content, LLM response, tool outputs
- **Client-side traces**: User input, context passed to agent

### Scenario 3: Application Errors
**What to check:**
- **Client-side traces**: Where the error occurred in your code
- **Server-side traces**: Whether the agent completed successfully

---

## Data Flow Summary

```
┌─────────────────────────────────────────────────────────────┐
│                    YOUR APPLICATION                         │
│                                                             │
│  User Action → Your Code → Agent API Call                  │
│                    │              │                         │
└────────────────────│──────────────│─────────────────────────┘
                     │              │
                     │              └────────────────┐
                     │                               │
      Client Traces  │                               │ Agent Request
      (OpenTelemetry)│                               │ (HTTPS)
                     │                               │
                     ▼                               ▼
        ┌─────────────────────────┐    ┌────────────────────────┐
        │  Application Insights   │    │  Foundry Agent Service │
        │                         │    │                        │
        │  ← Client traces here   │    │  Processes request     │
        │                         │    │  Auto-instrumentation  │
        └─────────────────────────┘    └───────────┬────────────┘
                     ▲                              │
                     │                              │
                     │               Server Traces  │
                     │               (OpenTelemetry)│
                     │                              │
                     └──────────────────────────────┘

           Both streams stored in same Application Insights
                    Correlated by trace context
                              │
                              ▼
                ┌──────────────────────────┐
                │  View traces in:         │
                │  • Foundry Traces Portal │
                │  • Azure Monitor         │
                │  • Custom Dashboards     │
                └──────────────────────────┘
```

**Key Points**: 
- Client and server both send traces **directly to Application Insights**
- They are **independent, parallel streams** - not routed through each other
- Traces are **correlated using trace context** (correlation IDs, span IDs)
- You see a **unified view** in the Foundry portal even though they come from different sources

---

## Summary

- **Server-Side = Automatic**: Foundry instruments agents for you
- **Client-Side = Manual**: You instrument your application code
- **Both = Complete**: Together they provide end-to-end observability
- **Storage = Shared**: All traces go to Application Insights
- **Access = Unified**: View everything in Foundry portal or Azure Monitor

Start with server-side tracing for quick insights, then add client-side tracing for production-grade observability.
