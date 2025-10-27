# Lab 07: Monitor GenAI Application

This lab demonstrates how to set up monitoring for generative AI applications using Azure AI Foundry and Azure Monitor.

## Learning Objectives

- Configure Azure Monitor integration for AI applications
- Generate telemetry data from AI model interactions
- Set up monitoring dashboards and alerts
- Analyze performance metrics and usage patterns

## Lab Overview

This lab will:

1. **Setup Monitoring**: Configure Azure Monitor and Application Insights integration
2. **Generate Telemetry**: Create sample AI requests to generate monitoring data
3. **Validate Setup**: Verify monitoring configuration and data collection
4. **Analyze Results**: Review generated metrics and telemetry data

## Prerequisites

- Azure AI Foundry project with deployed model (GPT-4o or similar)
- Application Insights resource connected to your AI project
- Project connection string configured in environment variables

## Running the Lab

### Via GitHub Actions (Recommended)

1. Go to the **Actions** tab in your GitHub repository
2. Select **"Lab 07: Monitor GenAI Application"**
3. Click **"Run workflow"**
4. Choose your environment (dev/staging/prod)
5. Specify number of telemetry requests to generate (default: 5)
6. Click **"Run workflow"** to execute

### Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export PROJECT_CONNECTION_STRING="your_project_connection_string"

# Run the lab
cd labs/07-observability
python monitor_genai.py --ci-mode --requests 10
```

## Lab Structure

- `monitor_genai.py`: Main lab script that sets up monitoring and generates telemetry
- `monitoring_results.json`: Generated results with metrics and analysis
- `README.md`: This file

## Expected Results

After successful execution, you should see:

- ✅ Azure Monitor configured
- ✅ Application Insights connected
- ✅ Sample telemetry data generated
- ✅ Performance metrics collected

### Sample Metrics

- **Total Requests**: Number of AI model requests made
- **Success Rate**: Percentage of successful requests
- **Average Response Time**: Mean response time in milliseconds
- **Token Usage**: AI model token consumption patterns

## Viewing Monitoring Data

### Azure AI Foundry
1. Open your AI Foundry project
2. Navigate to **Monitoring** section
3. View real-time metrics and dashboards

### Application Insights
1. Open Azure Portal
2. Navigate to your Application Insights resource
3. Use **Transaction search** to find specific requests
4. Create custom dashboards and alerts

## Troubleshooting

**Authentication Issues:**
- Verify PROJECT_CONNECTION_STRING is correct
- Check Azure credentials and permissions

**No Telemetry Data:**
- Ensure Application Insights is connected to your AI project
- Verify the deployed model is accessible
- Check Azure service quotas

**Monitoring Not Working:**
- Confirm Azure Monitor SDK installation
- Validate Application Insights connection string
- Check network connectivity to Azure services

## Next Steps

1. Set up custom alerts for high error rates or slow responses
2. Create monitoring dashboards for different user scenarios
3. Configure budget alerts to track AI service costs
4. Implement automated performance testing with continuous monitoring

## Learn More

- [Azure AI Foundry Monitoring](https://docs.microsoft.com/azure/ai-services/openai/how-to/monitoring)
- [Application Insights for AI Applications](https://docs.microsoft.com/azure/azure-monitor/app/app-insights-overview)
- [Azure Monitor OpenTelemetry](https://docs.microsoft.com/azure/azure-monitor/app/opentelemetry-enable)