#!/usr/bin/env python3
"""
Lab 07: Monitor GenAI Application
Set up monitoring and generate telemetry data for a generative AI application
"""

import argparse
import json
import logging
import os
import sys
import time
import uuid
from pathlib import Path

# Lab 07: Monitor GenAI Application

try:
    from dotenv import load_dotenv
    from azure.identity import DefaultAzureCredential
    from azure.ai.projects import AIProjectClient
    from azure.ai.inference.models import SystemMessage, UserMessage
    from azure.monitor.opentelemetry import configure_azure_monitor
    from opentelemetry import trace
except ImportError as e:
    print(f"Missing required packages. Install with: pip install azure-ai-projects azure-identity azure-monitor-opentelemetry python-dotenv")
    sys.exit(1)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def setup_monitoring(project_client):
    """Set up Azure Monitor integration"""
    logger.info("Setting up Azure Monitor integration...")
    
    try:
        # Get Application Insights connection string
        ai_conn_str = project_client.telemetry.get_connection_string()
        
        if not ai_conn_str:
            logger.warning("No Application Insights connection string found")
            return False
        
        # Configure Azure Monitor
        configure_azure_monitor(connection_string=ai_conn_str)
        logger.info("Azure Monitor configured successfully")
        return True
        
    except Exception as e:
        logger.error(f"Failed to setup monitoring: {e}")
        return False

def generate_telemetry_data(project_client, num_requests=5):
    """Generate telemetry data by making requests to the deployed model"""
    logger.info(f"Generating {num_requests} requests for telemetry data...")
    
    # Get tracer
    tracer = trace.get_tracer(__name__)
    
    # Sample prompts for testing
    test_prompts = [
        "What is the weather like today?",
        "Tell me a joke about programming",
        "Explain quantum computing in simple terms",
        "What are the benefits of renewable energy?",
        "How do neural networks work?"
    ]
    
    results = []
    
    try:
        # Get chat client
        chat_client = project_client.inference.get_chat_completions_client()
        
        for i in range(num_requests):
            with tracer.start_as_current_span(f"chat_request_{i+1}") as span:
                try:
                    # Add span attributes
                    span.set_attribute("request.id", str(uuid.uuid4()))
                    span.set_attribute("request.index", i+1)
                    
                    # Select prompt
                    prompt = test_prompts[i % len(test_prompts)]
                    span.set_attribute("request.prompt", prompt)
                    
                    messages = [
                        SystemMessage(content="You are a helpful AI assistant. Keep responses concise."),
                        UserMessage(content=prompt)
                    ]
                    
                    logger.info(f"Request {i+1}: {prompt}")
                    
                    # Make request
                    start_time = time.time()
                    response = chat_client.complete(
                        messages=messages,
                        max_tokens=100,
                        temperature=0.7
                    )
                    end_time = time.time()
                    
                    # Extract response
                    response_text = response.choices[0].message.content
                    response_time = end_time - start_time
                    
                    # Add more span attributes
                    span.set_attribute("response.time_ms", response_time * 1000)
                    span.set_attribute("response.tokens", len(response_text.split()))
                    span.set_attribute("response.success", True)
                    
                    result = {
                        'request_id': str(uuid.uuid4()),
                        'prompt': prompt,
                        'response': response_text,
                        'response_time_ms': response_time * 1000,
                        'token_count': len(response_text.split()),
                        'status': 'success'
                    }
                    
                    results.append(result)
                    logger.info(f"Request {i+1} completed in {response_time:.2f}s")
                    
                    # Small delay between requests
                    time.sleep(1)
                    
                except Exception as e:
                    logger.error(f"Request {i+1} failed: {e}")
                    span.set_attribute("response.success", False)
                    span.set_attribute("error.message", str(e))
                    
                    result = {
                        'request_id': str(uuid.uuid4()),
                        'prompt': prompt,
                        'status': 'error',
                        'error': str(e)
                    }
                    results.append(result)
        
        return results
        
    except Exception as e:
        logger.error(f"Error generating telemetry data: {e}")
        return []

def validate_monitoring_setup(project_client):
    """Validate that monitoring is properly configured"""
    logger.info("Validating monitoring setup...")
    
    validation_results = {
        'application_insights_connected': False,
        'telemetry_enabled': False,
        'project_accessible': False
    }
    
    try:
        # Check project access
        project_info = project_client.get_project()
        validation_results['project_accessible'] = True
        logger.info(f"Project accessible: {project_info.name}")
        
        # Check Application Insights connection
        try:
            ai_conn_str = project_client.telemetry.get_connection_string()
            if ai_conn_str:
                validation_results['application_insights_connected'] = True
                validation_results['telemetry_enabled'] = True
                logger.info("Application Insights connection validated")
            else:
                logger.warning("No Application Insights connection string found")
        except Exception as e:
            logger.warning(f"Could not validate Application Insights connection: {e}")
        
    except Exception as e:
        logger.error(f"Error validating monitoring setup: {e}")
    
    return validation_results

def main(ci_mode=False):
    """Main lab execution function"""
    logger.info("=== Lab 07: Monitor GenAI Application ===")
    
    results = {
        'lab': '07-observability',
        'status': 'running',
        'monitoring_setup': {},
        'validation_results': {},
        'telemetry_data': [],
        'summary': {}
    }
    
    try:
        # Load environment variables
        if not ci_mode:
            load_dotenv()
        
        # Get connection string
        conn_str = os.getenv("PROJECT_CONNECTION_STRING")
        if not conn_str:
            raise ValueError("Missing PROJECT_CONNECTION_STRING environment variable")
        
        # Initialize AI Project Client
        logger.info("Connecting to Azure AI Foundry project...")
        credential = DefaultAzureCredential()
        project_client = AIProjectClient.from_connection_string(conn_str, credential=credential)
        
        # Setup monitoring
        monitoring_success = setup_monitoring(project_client)
        results['monitoring_setup'] = {
            'azure_monitor_configured': monitoring_success,
            'timestamp': time.time()
        }
        
        # Validate monitoring setup
        validation_results = validate_monitoring_setup(project_client)
        results['validation_results'] = validation_results
        
        # Generate telemetry data
        telemetry_data = generate_telemetry_data(project_client, num_requests=5)
        results['telemetry_data'] = telemetry_data
        
        # Summary
        successful_requests = len([r for r in telemetry_data if r.get('status') == 'success'])
        total_requests = len(telemetry_data)
        
        results['summary'] = {
            'monitoring_enabled': monitoring_success,
            'application_insights_connected': validation_results.get('application_insights_connected', False),
            'total_requests_generated': total_requests,
            'successful_requests': successful_requests,
            'success_rate': f"{(successful_requests/total_requests)*100:.1f}%" if total_requests > 0 else "0%",
            'avg_response_time_ms': sum(r.get('response_time_ms', 0) for r in telemetry_data if 'response_time_ms' in r) / max(successful_requests, 1)
        }
        
        results['status'] = 'success'
        logger.info(f"Lab completed successfully! Generated {total_requests} requests, {successful_requests} successful")
        
        return results
        
    except Exception as e:
        logger.error(f"Lab execution failed: {e}")
        results['status'] = 'failed'
        results['error'] = str(e)
        return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Lab 07: Monitor GenAI Application")
    parser.add_argument("--ci-mode", action="store_true", help="Run in CI mode (no interactive prompts)")
    parser.add_argument("--requests", type=int, default=5, help="Number of requests to generate for telemetry")
    args = parser.parse_args()
    
    results = main(ci_mode=args.ci_mode)
    
    # Save results
    results_file = Path(__file__).parent / "monitoring_results.json"
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to: {results_file}")
    print(f"Lab status: {results['status']}")
    
    if results.get('summary'):
        summary = results['summary']
        print(f"Monitoring enabled: {summary.get('monitoring_enabled', False)}")
        print(f"Requests generated: {summary.get('total_requests_generated', 0)}")
        print(f"Success rate: {summary.get('success_rate', '0%')}")
    
    if results['status'] != 'success':
        sys.exit(1)