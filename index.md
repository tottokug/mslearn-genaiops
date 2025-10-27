---
title: GenAIOps Labs
permalink: index.html
layout: home
---

# GenAIOps Hands-on Labs

Welcome to the GenAIOps hands-on labs! These labs provide practical experience with **monitoring** and **tracing** generative AI applications using Azure AI Foundry and GitHub Actions.

> **🌐 100% Cloud-Based Labs!** 
> 
> No local development environment required! Everything runs in the cloud:
> - Use GitHub's web interface to fork and configure
> - Use Azure Cloud Shell for service principal setup
> - Use GitHub Actions to execute labs automatically
> - View results in Azure AI Foundry and GitHub

## 🚀 Quick Start Guide

### Prerequisites
- Azure subscription with AI services quota
- GitHub account
- Basic familiarity with Python and Azure AI services

### Setup Instructions (100% Cloud-Based - No Local Setup Required!)

1. **Fork this repository** to your GitHub account:
   - Click the **Fork** button at the top of this repository page
   - Choose your GitHub account as the destination

2. **Set up Azure AI Foundry** in your Azure tenant:
   - Open [Azure AI Foundry](https://ai.azure.com) in a new tab
   - Sign in with your Azure credentials
   - Click **+ Create new** → **AI hub resource**
   - Create a hub and project in your preferred region
   - Deploy a GPT-4o model (or any available chat model)
   - Copy your **project connection string** from the project overview

3. **Create Azure Service Principal** using Azure Cloud Shell:
   - Open [Azure Cloud Shell](https://shell.azure.com) (no local Azure CLI needed!)
   - Run the service principal creation commands (see detailed steps below)
   - Copy the JSON output for GitHub secrets

4. **Configure GitHub Secrets** in your forked repository:
   - In your forked repo, go to **Settings > Secrets and variables > Actions**
   - Add the required secrets (details below)

5. **Run the labs** via GitHub Actions:
   - Go to the **Actions** tab in your forked repository
   - Select a lab workflow and click **Run workflow**
   - No local development environment required!

## 📚 Available Labs

{% assign labs = site.pages | where_exp:"page", "page.url contains '/Instructions'" %}
{% for activity in labs  %}
---
### [{{ activity.lab.title }}]({{ site.github.url }}{{ activity.url }})

{{activity.lab.description}}

**GitHub Actions Workflow**: `.github/workflows/lab-{% if activity.url contains '07' %}07-monitor{% elsif activity.url contains '08' %}08-trace{% endif %}.yml`

{% endfor %}

## ⚙️ Azure Service Principal Setup (Using Azure Cloud Shell)

Create an Azure service principal using Azure Cloud Shell - no local setup required:

1. **Open Azure Cloud Shell**:
   - Go to [shell.azure.com](https://shell.azure.com) or click the Cloud Shell icon in Azure Portal
   - Choose **Bash** or **PowerShell** (both work)
   - You're automatically authenticated to your Azure subscription

2. **Get your subscription ID**:
   ```bash
   az account show --query "id" --output tsv
   ```
   Copy this subscription ID for the next steps.

3. **Create service principal**:
   ```bash
   az ad sp create-for-rbac --name "github-genaiops-labs" \
     --role "Contributor" \
     --scopes "/subscriptions/YOUR_SUBSCRIPTION_ID" \
     --sdk-auth
   ```
   Replace `YOUR_SUBSCRIPTION_ID` with the ID from step 2.

4. **Copy the entire JSON output** - you'll need this for GitHub secrets

5. **Grant AI Services permissions**:
   ```bash
   # Get the service principal ID from the JSON output above
   az role assignment create \
     --assignee "CLIENT_ID_FROM_JSON" \
     --role "Cognitive Services Contributor" \
     --scope "/subscriptions/YOUR_SUBSCRIPTION_ID"
   ```

6. **Get your Azure AI Foundry project connection string**:
   - In [Azure AI Foundry](https://ai.azure.com), open your project
   - Go to **Settings** (gear icon)
   - Copy the **Connection string** (starts with something like `https://...`)

7. **Add secrets to your GitHub repository**:
   - Go to your forked repository on GitHub
   - Navigate to **Settings > Secrets and variables > Actions**
   - Click **New repository secret** and add:
     - **Name**: `AZURE_CREDENTIALS`
     - **Value**: The entire JSON output from step 4
   - Add another secret:
     - **Name**: `PROJECT_CONNECTION_STRING`
     - **Value**: Your Azure AI Foundry project connection string from step 6

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

- **Authentication errors**: 
  - Verify service principal was created correctly in Azure Cloud Shell
  - Check that both `AZURE_CREDENTIALS` and `PROJECT_CONNECTION_STRING` secrets are set
  - Ensure service principal has "Contributor" and "Cognitive Services Contributor" roles
- **Missing resources**: 
  - Confirm Azure AI Foundry project exists and has a deployed model
  - Verify you're using the correct subscription and resource group
- **Quota limits**: 
  - Check Azure OpenAI service quotas in your subscription
  - Try different Azure regions if quota is exhausted
- **Connection string format**: 
  - Ensure connection string starts with `https://` and includes your project details
  - Copy the full connection string from Azure AI Foundry project settings

## 📖 Learning Resources

- [Azure AI Foundry Documentation](https://docs.microsoft.com/azure/ai-services/openai/)
- [Azure Monitor OpenTelemetry](https://docs.microsoft.com/azure/azure-monitor/app/opentelemetry-enable)
- [GitHub Actions Documentation](https://docs.github.com/actions)
- [Microsoft Learn: Operationalize GenAI Apps](https://learn.microsoft.com/training/paths/operationalize-gen-ai-apps/)

---

Ready to start? Choose a lab and click **Run workflow** in the Actions tab! 🚀
