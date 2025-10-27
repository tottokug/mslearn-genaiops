# GenAIOps Monitoring and Tracing Labs

This repository contains hands-on labs for learning **monitoring** and **tracing** of generative AI applications using Azure AI Foundry and GitHub Actions.

## 🎯 Lab Overview

Students will complete two focused labs that demonstrate essential GenAIOps practices:

- **Lab 07:** [Monitor GenAI Applications](labs/07-observability/) - Set up comprehensive monitoring and telemetry collection
- **Lab 08:** [Trace GenAI Applications](labs/08-tracing/) - Implement distributed tracing for debugging and optimization

## 🌐 100% Cloud-Based Setup

**No local development environment required!** Everything runs in the cloud:

### For Students
1. **Visit the [GitHub Pages site](https://microsoftlearning.github.io/mslearn-genaiops/)** for complete setup instructions
2. **Fork this repository** using GitHub's web interface
3. **Set up Azure AI Foundry** via [ai.azure.com](https://ai.azure.com)
4. **Create service principal** using [Azure Cloud Shell](https://shell.azure.com)
5. **Configure GitHub secrets** in your forked repository
6. **Run labs via GitHub Actions** with one-click execution

### Cloud-Only Setup Summary
1. 🍴 Fork this repo on GitHub.com
2. ☁️ Create Azure AI Foundry project at ai.azure.com
3. 🛡️ Set up service principal via shell.azure.com
4. 🔐 Add secrets in GitHub Settings → Secrets and variables → Actions
5. 🚀 Execute labs in GitHub Actions tab

## 📊 Lab Execution via GitHub Actions

Each lab runs as a GitHub Actions workflow:

### Lab 07: Monitor GenAI Application
- **Workflow**: `.github/workflows/lab-07-monitor.yml`
- **Script**: `labs/07-observability/monitor_genai.py`
- **Trigger**: Manual workflow dispatch or code changes
- **Duration**: ~5-10 minutes
- **Outputs**: Monitoring setup, telemetry data, performance metrics

### Lab 08: Trace GenAI Application
- **Workflow**: `.github/workflows/lab-08-trace.yml`
- **Script**: `labs/08-tracing/trace_genai.py`
- **Trigger**: Manual workflow dispatch or code changes
- **Duration**: ~5-10 minutes
- **Outputs**: Distributed traces, workflow analysis, error scenarios

## 💻 Local Development (Optional)

You can also run labs locally for development:

```bash
# Clone your fork
git clone https://github.com/YourUsername/mslearn-genaiops.git
cd mslearn-genaiops

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export PROJECT_CONNECTION_STRING="your_ai_foundry_connection_string"

# Run a lab
cd labs/07-observability
python monitor_genai.py --ci-mode

cd ../08-tracing
python trace_genai.py --ci-mode
```

## 📁 Repository Structure

```
mslearn-genaiops/
├── .github/workflows/          # GitHub Actions lab workflows
│   ├── lab-07-monitor.yml     # Monitoring lab automation
│   └── lab-08-trace.yml       # Tracing lab automation
├── labs/                       # Lab implementations
│   ├── 07-observability/      # Monitoring lab
│   │   ├── monitor_genai.py   # Main monitoring script
│   │   └── README.md          # Lab instructions
│   └── 08-tracing/            # Tracing lab
│       ├── trace_genai.py     # Main tracing script
│       └── README.md          # Lab instructions
├── Instructions/               # GitHub Pages instructions (Jekyll)
│   ├── 07-Monitor-GenAI-application.md
│   └── 08-Tracing-GenAI-application.md
├── Files/                      # Supporting lab assets
│   ├── 07/                    # Monitoring assets
│   └── 08/                    # Tracing assets (sample Python files)
├── index.md                    # GitHub Pages entry point
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## 🎓 Learning Objectives

### Lab 07: Monitoring
- Configure Azure Monitor integration for AI applications
- Generate and analyze telemetry data
- Set up performance monitoring dashboards
- Implement alerting for AI application health

### Lab 08: Tracing
- Implement distributed tracing for multi-step AI workflows
- Debug AI applications with detailed trace information
- Analyze performance bottlenecks in AI pipelines
- Handle error scenarios with comprehensive tracing

## 🔧 Technical Requirements

### Azure Resources
- Azure AI Foundry hub and project (hub-based required for tracing)
- Deployed chat completion model (GPT-4o or similar)
- Application Insights resource (connected to AI project)
- Azure subscription with AI services quota

### GitHub Configuration
- Service principal with Contributor and Cognitive Services Contributor roles
- GitHub repository secrets configured
- Actions enabled in repository settings

### Dependencies
- `azure-ai-projects>=1.0.0`
- `azure-ai-inference>=1.0.0`
- `azure-identity>=1.15.0`
- `azure-monitor-opentelemetry>=1.2.0`
- `python-dotenv>=1.0.0`

## 🎯 Success Criteria

Students successfully complete labs when they:

1. **Lab 07**: Generate monitoring data visible in Azure AI Foundry and Application Insights
2. **Lab 08**: Create distributed traces viewable in Azure AI Foundry tracing dashboard
3. **Both Labs**: Demonstrate understanding through GitHub Actions execution results

## 💡 Key Benefits

- **Hands-on Experience**: Real Azure AI Foundry integration
- **Industry Standards**: OpenTelemetry and Azure Monitor practices
- **Automation Ready**: GitHub Actions CI/CD integration
- **Scalable Patterns**: Production-ready monitoring and tracing setup

## 🆘 Support

- **Setup Issues**: Check the [GitHub Pages guide](https://microsoftlearning.github.io/mslearn-genaiops/)
- **Lab Problems**: Review individual lab README files
- **Technical Issues**: Open GitHub issues in this repository
- **Azure Questions**: Consult [Azure AI Foundry documentation](https://docs.microsoft.com/azure/ai-services/)

## 📚 Additional Resources

- [Azure AI Foundry](https://ai.azure.com)
- [Azure Monitor OpenTelemetry](https://docs.microsoft.com/azure/azure-monitor/app/opentelemetry-enable)
- [GitHub Actions Documentation](https://docs.github.com/actions)
- [Microsoft Learn: Operationalize GenAI](https://learn.microsoft.com/training/paths/operationalize-gen-ai-apps/)

---

**Ready to start?** Visit the [setup guide](https://microsoftlearning.github.io/mslearn-genaiops/) and run your first lab! 🚀