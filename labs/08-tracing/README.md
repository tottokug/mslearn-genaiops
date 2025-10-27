# Lab 08: Trace GenAI Application

This lab demonstrates distributed tracing for generative AI applications to analyze workflows, debug issues, and optimize performance.

## Learning Objectives

- Implement distributed tracing for multi-step AI workflows
- Trace individual AI model requests and responses
- Analyze error scenarios with detailed trace information
- Use tracing data for debugging and performance optimization

## Lab Overview

This lab will:

1. **Setup Tracing**: Configure Azure AI Inference tracing and Azure Monitor
2. **Trace Workflows**: Execute a multi-step hiking assistant workflow with tracing
3. **Error Tracing**: Demonstrate error scenario tracing for debugging
4. **Analyze Traces**: Review distributed traces and span information

## Prerequisites

- Azure AI Foundry hub-based project (required for tracing features)
- Deployed model (GPT-4o or similar) for chat completions
- Application Insights resource connected to your AI project
- Project connection string configured in environment variables

## Running the Lab

### Via GitHub Actions (Recommended)

1. Go to the **Actions** tab in your GitHub repository
2. Select **"Lab 08: Trace GenAI Application"**
3. Click **"Run workflow"**
4. Choose your environment (dev/staging/prod)
5. Click **"Run workflow"** to execute

### Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export PROJECT_CONNECTION_STRING="your_project_connection_string"

# Run the lab
cd labs/08-tracing
python trace_genai.py --ci-mode
```

## Lab Structure

- `trace_genai.py`: Main lab script that implements tracing workflows
- `tracing_results.json`: Generated results with trace analysis
- `README.md`: This file

## Workflow Scenarios

### Hiking Assistant Workflow
A multi-step AI application that:

1. **Analyzes User Preferences**: Extracts hiking preferences from user input
2. **Generates Trip Recommendations**: Uses AI to suggest hiking destinations
3. **Recommends Gear**: Provides outdoor equipment suggestions
4. **Finalizes Recommendations**: Compiles comprehensive trip plan

### Error Scenario Tracing
Demonstrates tracing capabilities for:

- Input validation errors
- Service failures
- Debugging information
- Error propagation through workflow steps

## Expected Results

After successful execution, you should see:

- ✅ Distributed tracing enabled
- ✅ Content recording activated
- ✅ Multi-step workflow traced
- ✅ Error scenarios captured
- ✅ Detailed span information

### Trace Metrics

- **Workflows Executed**: Number of complete workflows traced
- **Spans Created**: Total tracing spans generated
- **Success Rate**: Percentage of successful workflow steps
- **Error Scenarios**: Number of error conditions traced

## Viewing Trace Data

### Azure AI Foundry
1. Open your AI Foundry project
2. Navigate to **Tracing** section
3. Search for traces using session IDs
4. Analyze workflow execution paths

### Application Insights
1. Open Azure Portal
2. Navigate to your Application Insights resource
3. Use **Transaction search** with trace IDs
4. View **Application map** for service dependencies
5. Analyze **Performance** tab for response times

### Trace Analysis Features

- **End-to-End Tracing**: Complete request flow visualization
- **Span Details**: Individual operation timing and metadata
- **Error Context**: Detailed error information with stack traces
- **Custom Attributes**: Business logic data captured in spans

## Understanding Trace Data

### Span Hierarchy
```
hiking_trip_workflow (main span)
├── get_user_preferences
├── generate_trip_recommendations
├── generate_gear_recommendations
└── finalize_recommendations
```

### Span Attributes
- `session.id`: Unique workflow identifier
- `step`: Workflow step number
- `response.time_ms`: Operation duration
- `model.temperature`: AI model parameters
- `error.message`: Error details (if applicable)

## Troubleshooting

**Tracing Not Working:**
- Ensure you have a hub-based AI Foundry project (required for tracing)
- Verify Azure AI Inference SDK instrumentation
- Check Application Insights connection

**Missing Traces:**
- Confirm content recording is enabled
- Verify trace propagation headers
- Check Azure Monitor configuration

**Performance Issues:**
- Review span timing information
- Analyze model response times
- Identify workflow bottlenecks

## Advanced Usage

### Custom Span Creation
```python
with tracer.start_as_current_span("custom_operation") as span:
    span.set_attribute("custom.attribute", "value")
    # Your operation here
```

### Error Handling with Tracing
```python
try:
    # AI operation
    pass
except Exception as e:
    span.set_attribute("error.message", str(e))
    span.set_attribute("error.type", type(e).__name__)
    raise
```

## Next Steps

1. Implement tracing in your own AI applications
2. Set up custom dashboards for workflow monitoring
3. Create alerts for error rate thresholds
4. Use trace data to optimize AI model performance
5. Implement distributed tracing across microservices

## Learn More

- [Azure AI Foundry Tracing](https://docs.microsoft.com/azure/ai-services/openai/how-to/tracing)
- [OpenTelemetry Python SDK](https://opentelemetry.io/docs/instrumentation/python/)
- [Application Insights Distributed Tracing](https://docs.microsoft.com/azure/azure-monitor/app/distributed-tracing)
- [Azure AI Inference Tracing](https://docs.microsoft.com/azure/ai-services/inference-sdk/tracing)