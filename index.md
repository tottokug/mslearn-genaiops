---
title: GenAIOps Labs
permalink: index.html
layout: home
---

# GenAIOps Hands-on Labs

Welcome to the GenAIOps hands-on labs! These labs provide practical experience with **monitoring** and **tracing** generative AI applications using Azure AI Foundry and GitHub Actions.

## 🚀 Quick Start Guide

### Prerequisites
- Azure subscription with AI services quota
- GitHub account
- Basic familiarity with Python and Azure AI services

### Setup Instructions

1. **Fork this repository** to your GitHub account
2. **Clone your fork** to your local machine:
   ```bash
   git clone https://github.com/YourUsername/mslearn-genaiops.git
   cd mslearn-genaiops
   ```

3. **Set up Azure AI Foundry** (if you don't have one):
   - Open [Azure AI Foundry](https://ai.azure.com)
   - Create a new AI hub and project
   - Deploy a GPT-4o model (or any available chat model)
   - Note your project connection string

4. **Configure GitHub Secrets**:
   - In your GitHub repository, go to **Settings > Secrets and variables > Actions**
   - Add these secrets:
     - `AZURE_CREDENTIALS`: Azure service principal JSON (see setup guide below)
     - `PROJECT_CONNECTION_STRING`: Your Azure AI Foundry project connection string

5. **Run the labs** via GitHub Actions:
   - Go to the **Actions** tab in your repository
   - Select the lab you want to run
   - Click **Run workflow**

## 📚 Available Labs

{% assign labs = site.pages | where_exp:"page", "page.url contains '/Instructions'" %}
{% for activity in labs  %}
---
### [{{ activity.lab.title }}]({{ site.github.url }}{{ activity.url }})

{{activity.lab.description}}

**GitHub Actions Workflow**: `.github/workflows/lab-{% if activity.url contains '07' %}07-monitor{% elsif activity.url contains '08' %}08-trace{% endif %}.yml`

{% endfor %}

## ⚙️ Azure Service Principal Setup

To run labs via GitHub Actions, you need to create an Azure service principal:

1. **Install Azure CLI** and log in:
   ```bash
   az login
   ```

2. **Create service principal**:
   ```bash
   az ad sp create-for-rbac --name "github-genaiops-labs" \
     --role "Contributor" \
     --scopes "/subscriptions/YOUR_SUBSCRIPTION_ID" \
     --sdk-auth
   ```

3. **Copy the output JSON** and add it as `AZURE_CREDENTIALS` secret in GitHub

4. **Grant additional permissions**:
   ```bash
   az role assignment create \
     --assignee SERVICE_PRINCIPAL_ID \
     --role "Cognitive Services Contributor" \
     --scope "/subscriptions/YOUR_SUBSCRIPTION_ID"
   ```

## 🔄 Lab Execution Workflow

1. **Navigate to Actions tab** in your GitHub repository
2. **Select a lab workflow**:
   - `Lab 07: Monitor GenAI Application`
   - `Lab 08: Trace GenAI Application`
3. **Click "Run workflow"**
4. **Choose environment**: dev, staging, or prod
5. **Monitor execution** in real-time
6. **Download results** from the artifacts section

## 📊 Understanding Lab Results

### Lab 07: Monitoring
- **Telemetry Generation**: Creates sample requests to your AI model
- **Metrics Collection**: Captures response times, success rates, and usage patterns
- **Dashboard Setup**: Configures Azure Monitor for ongoing monitoring

### Lab 08: Tracing
- **Distributed Tracing**: Traces multi-step AI workflows
- **Error Analysis**: Demonstrates debugging with trace data
- **Performance Insights**: Identifies bottlenecks and optimization opportunities

## 🔍 Viewing Results

After running labs, check these locations:

- **GitHub Actions**: Download JSON results and logs
- **Azure AI Foundry**: View monitoring and tracing dashboards
- **Application Insights**: Detailed telemetry and trace analysis
- **Pull Request Comments**: Automated result summaries (if running on PRs)

## 💡 Tips for Success

- **Start with Lab 07** to set up monitoring before tracing
- **Use dev environment** for learning and experimentation
- **Check Azure quotas** before running labs
- **Review logs** if labs fail for troubleshooting hints
- **Customize parameters** in workflow inputs for different scenarios

## 🆘 Troubleshooting

Common issues and solutions:

- **Authentication errors**: Verify service principal permissions
- **Missing resources**: Ensure Azure AI Foundry project exists
- **Quota limits**: Check Azure OpenAI service quotas
- **Connection strings**: Verify project connection string format

## 📖 Learning Resources

- [Azure AI Foundry Documentation](https://docs.microsoft.com/azure/ai-services/openai/)
- [Azure Monitor OpenTelemetry](https://docs.microsoft.com/azure/azure-monitor/app/opentelemetry-enable)
- [GitHub Actions Documentation](https://docs.github.com/actions)
- [Microsoft Learn: Operationalize GenAI Apps](https://learn.microsoft.com/training/paths/operationalize-gen-ai-apps/)

---

Ready to start? Choose a lab and click **Run workflow** in the Actions tab! 🚀
