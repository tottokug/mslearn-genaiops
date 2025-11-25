# Microsoft Foundry Tracing - Key Skills and Tasks

*Extracted from: [How to set up tracing in Microsoft Foundry](https://learn.microsoft.com/en-us/azure/ai-foundry/observability/how-to/trace-agent-setup?view=foundry)*

## Overview
Tracing is a powerful observability tool for understanding agent behavior, identifying performance issues, debugging runtime exceptions, and improving prompt engineering and retrieval quality.

---

## Key Skills Required

### 1. Azure Resource Management
- **Azure Application Insights**: Understanding how to create and connect Application Insights resources
- **Azure Monitor**: Knowledge of Azure Monitor for viewing and analyzing traces
- **Role-Based Access Control (RBAC)**: Assigning the Log Analytics Reader role for accessing trace data
- **Microsoft Entra ID**: Configuring authentication for project endpoints

### 2. OpenTelemetry
- Understanding OpenTelemetry Semantic Conventions for GenAI
- Working with OTLP-compatible collectors
- Using OpenTelemetry SDK for instrumentation

### 3. Python Development
- Installing and managing Python packages via pip
- Working with Azure SDKs (`azure-ai-projects`, `azure-identity`)
- Implementing OpenTelemetry instrumentation in code

### 4. AI Agent Development
- Building agents using Foundry Agents Service
- Integrating with agent frameworks (OpenAI, Anthropic, LangChain)
- Understanding agent workflows and conversation patterns

### 5. Visual Studio Code
- Using AI Toolkit extension
- Local debugging and development with VS Code tools
- Viewing traces in local development environment

---

## Key Tasks

### Setup Tasks

#### Task 1: Enable Tracing in Foundry Project
**Objective**: Configure Application Insights for trace storage

**Steps**:
1. Navigate to Foundry project monitor settings
2. Create or connect an Azure Application Insights resource
3. Verify tracing is enabled (traces available for past 90 days)

**Prerequisites**:
- Log Analytics Reader role assigned to Application Insights resource
- Proper Azure role assignments via Azure portal

---

#### Task 2: Install Required Dependencies
**Objective**: Set up client-side tracing SDK

**Command**:
```bash
pip install azure-ai-projects azure-identity opentelemetry-sdk azure-core-tracing-opentelemetry
```

**Components**:
- `azure-ai-projects`: Microsoft Foundry SDK
- `azure-identity`: Azure authentication
- `opentelemetry-sdk`: OpenTelemetry core
- `azure-core-tracing-opentelemetry`: Azure SDK tracing plugin

---

### Instrumentation Tasks

#### Task 3: Implement Server-Side Tracing
**Objective**: Enable automatic tracing for Foundry agents

**Auto-instrumentation Features**:
- Prompt agents (automatically logged)
- Host agents (automatically logged)
- Workflows in Foundry portal (automatically logged)
- Agent framework integrations (require setup)

**Action**: No code changes needed for basic server-side tracing of Foundry-hosted agents

---

#### Task 4: Implement Client-Side Tracing
**Objective**: Add custom tracing to your application code

**Resources**:
- [SDK tracing instructions](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-projects#tracing)
- [Code samples](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-projects/samples/agents/telemetry)

**Use Case**: Custom instrumentation for client applications calling Foundry agents

---

#### Task 5: Set Up Local Tracing with AI Toolkit
**Objective**: Enable local trace viewing during development

**Setup**:
1. Install AI Toolkit extension in VS Code
2. Configure local OTLP-compatible collector
3. View traces instantly in VS Code without cloud access

**Supported Frameworks**:
- Foundry Agents Service
- OpenAI
- Anthropic
- LangChain

**Reference**: [Tracing in AI Toolkit](https://code.visualstudio.com/docs/intelligentapps/tracing)

---

### Analysis Tasks

#### Task 6: View and Analyze Traces in Foundry Portal
**Objective**: Monitor and debug agent behavior

**Access**: Navigate to **Traces** tab in your agents or workflows

**Capabilities**:
- Search traces (last 90 days)
- Filter by various criteria
- Sort ingested traces
- Step through individual spans
- Identify latency issues
- Debug runtime exceptions
- Analyze prompt effectiveness
- Evaluate retrieval quality

**Workflow**:
1. Select a trace from the list
2. Step through each span
3. Identify issues (latency, errors, etc.)
4. Observe application responses

---

#### Task 7: View Traces in Azure Monitor
**Objective**: Leverage Azure Monitor's advanced analytics

**Integration**: Traces automatically sent to Application Insights

**Use Cases**:
- Advanced querying with KQL (Kusto Query Language)
- Custom dashboards
- Alerting on trace patterns
- Long-term trace analysis

**Reference**: [Azure Monitor OpenTelemetry documentation](https://learn.microsoft.com/en-us/azure/azure-monitor/app/opentelemetry-enable)

---

#### Task 8: Analyze Conversation Results
**Objective**: Review end-to-end dialogue history and agent performance

**Access**: **Traces** page in Foundry portal

**Search Options**:
- By Conversation ID
- By Response ID
- By Trace ID

**Available Information**:
- Conversation history details
- Response information and token usage per run
- Ordered actions and run steps
- Tool calls and their sequence
- Inputs and outputs between user and agent

**Use Cases**:
- Understanding conversation flow
- Debugging multi-turn interactions
- Analyzing token consumption
- Reviewing tool usage patterns

---

## Troubleshooting Skills

### Issues to Identify and Debug
1. **Latency**: Performance bottlenecks in agent execution
2. **Runtime Exceptions**: Errors during agent operation
3. **Incorrect Prompts**: Prompt engineering issues
4. **Poor Retrieval**: RAG and knowledge base problems
5. **Token Usage**: Monitoring and optimizing token consumption
6. **Tool Call Issues**: Debugging agent tool execution

---

## Best Practices

1. **Start with Auto-Instrumentation**: Use built-in server-side tracing before adding custom instrumentation
2. **Use Local Tracing First**: Debug locally with AI Toolkit before deploying to cloud
3. **Leverage Microsoft Entra Groups**: Manage user access more efficiently
4. **Monitor Past 90 Days**: Regularly review trace history for patterns and trends
5. **Integrate with Agent Frameworks**: Use provided integrations for popular frameworks
6. **Use Application Insights Connection String**: When not using Entra ID authentication

---

## Security and Access Considerations

- **Required Role**: Log Analytics Reader role for Application Insights access
- **Authentication**: Microsoft Entra ID configuration for project endpoint access
- **Alternative**: Use Application Insights connection string without Entra ID
- **Group Management**: Use Microsoft Entra groups for easier access management

---

## Development Environments

### Production
- Foundry portal with Application Insights
- 90-day trace retention
- Full conversation analysis

### Development
- AI Toolkit in VS Code
- Local OTLP collector
- Instant trace viewing
- No cloud access required

---

## Additional Resources

- [Agent Framework Integration Guide](https://learn.microsoft.com/en-us/azure/ai-foundry/observability/how-to/trace-agent-framework?view=foundry)
- [Azure SDK for Python Tracing](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-projects#tracing)
- [Tracing Samples](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-projects/samples/agents/telemetry)
- [AI Toolkit Tracing](https://code.visualstudio.com/docs/intelligentapps/tracing)
- [Azure Monitor OpenTelemetry](https://learn.microsoft.com/en-us/azure/azure-monitor/app/opentelemetry-enable)
- [RBAC in Azure AI Foundry](https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/rbac-azure-ai-foundry?view=foundry)
