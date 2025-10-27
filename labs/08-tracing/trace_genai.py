#!/usr/bin/env python3
"""
Lab 08: Tracing GenAI Application
Implement distributed tracing for debugging and analyzing generative AI applications
"""

import argparse
import json
import logging
import os
import sys
import time
import uuid
from pathlib import Path

# Lab 08: Trace GenAI Application

try:
    from dotenv import load_dotenv
    from azure.identity import DefaultAzureCredential
    from azure.ai.projects import AIProjectClient
    from azure.ai.inference.tracing import AIInferenceInstrumentor
    from azure.ai.inference.models import SystemMessage, UserMessage
    from azure.monitor.opentelemetry import configure_azure_monitor
    from opentelemetry import trace
except ImportError as e:
    print(f"Missing required packages. Install with: pip install azure-ai-projects azure-identity azure-monitor-opentelemetry azure-ai-inference python-dotenv")
    sys.exit(1)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def setup_tracing(project_client):
    """Set up distributed tracing with Azure AI Inference"""
    logger.info("Setting up distributed tracing...")
    
    try:
        # Enable content recording for detailed tracing
        os.environ['AZURE_TRACING_GEN_AI_CONTENT_RECORDING_ENABLED'] = 'true'
        
        # Get Application Insights connection string
        ai_conn_str = project_client.telemetry.get_connection_string()
        
        if ai_conn_str:
            # Configure Azure Monitor for telemetry
            configure_azure_monitor(connection_string=ai_conn_str)
            logger.info("Azure Monitor configured for tracing")
        else:
            logger.warning("No Application Insights connection string found")
        
        # Instrument AI Inference SDK for automatic tracing
        AIInferenceInstrumentor().instrument()
        logger.info("Azure AI Inference instrumentation enabled")
        
        return True
        
    except Exception as e:
        logger.error(f"Failed to setup tracing: {e}")
        return False

def simulate_hiking_assistant(project_client, tracer):
    """Simulate a multi-step hiking trip assistant with tracing"""
    logger.info("Simulating hiking trip assistant workflow...")
    
    with tracer.start_as_current_span("hiking_trip_workflow") as main_span:
        session_id = str(uuid.uuid4())
        main_span.set_attribute("session.id", session_id)
        main_span.set_attribute("workflow.type", "hiking_assistant")
        
        results = []
        
        try:
            # Step 1: Get user preferences
            with tracer.start_as_current_span("get_user_preferences") as prefs_span:
                user_input = "I want a moderate difficulty hike in the mountains for 2 days"
                prefs_span.set_attribute("user.input", user_input)
                prefs_span.set_attribute("step", 1)
                
                logger.info(f"Step 1 - User input: {user_input}")
                
                # Analyze preferences
                preferences = {
                    'difficulty': 'moderate',
                    'terrain': 'mountains',
                    'duration': '2 days',
                    'group_size': 1
                }
                prefs_span.set_attribute("preferences.difficulty", preferences['difficulty'])
                prefs_span.set_attribute("preferences.terrain", preferences['terrain'])
                prefs_span.set_attribute("preferences.duration", preferences['duration'])
                
                results.append({
                    'step': 1,
                    'name': 'get_user_preferences',
                    'input': user_input,
                    'output': preferences,
                    'status': 'success'
                })
            
            # Step 2: Generate trip recommendations
            with tracer.start_as_current_span("generate_trip_recommendations") as trip_span:
                trip_span.set_attribute("step", 2)
                
                try:
                    chat_client = project_client.inference.get_chat_completions_client()
                    
                    messages = [
                        SystemMessage(content="""You are a hiking trip planner. Based on user preferences, 
                        recommend specific hiking destinations with details about trails, difficulty, 
                        and what to expect. Keep recommendations concise."""),
                        UserMessage(content=f"Recommend hiking destinations for: {user_input}")
                    ]
                    
                    logger.info("Step 2 - Generating trip recommendations...")
                    start_time = time.time()
                    
                    response = chat_client.complete(
                        messages=messages,
                        max_tokens=200,
                        temperature=0.7
                    )
                    
                    end_time = time.time()
                    response_time = end_time - start_time
                    
                    trip_recommendations = response.choices[0].message.content
                    trip_span.set_attribute("response.time_ms", response_time * 1000)
                    trip_span.set_attribute("response.length", len(trip_recommendations))
                    trip_span.set_attribute("model.temperature", 0.7)
                    
                    logger.info("Step 2 - Trip recommendations generated successfully")
                    
                    results.append({
                        'step': 2,
                        'name': 'generate_trip_recommendations',
                        'input': user_input,
                        'output': trip_recommendations,
                        'response_time_ms': response_time * 1000,
                        'status': 'success'
                    })
                    
                except Exception as e:
                    logger.error(f"Step 2 failed: {e}")
                    trip_span.set_attribute("error.message", str(e))
                    trip_span.set_attribute("error.occurred", True)
                    
                    results.append({
                        'step': 2,
                        'name': 'generate_trip_recommendations',
                        'status': 'error',
                        'error': str(e)
                    })
                    return results
            
            # Step 3: Generate gear recommendations
            with tracer.start_as_current_span("generate_gear_recommendations") as gear_span:
                gear_span.set_attribute("step", 3)
                
                try:
                    messages = [
                        SystemMessage(content="""You are an outdoor gear expert. Based on hiking trip details,
                        recommend essential gear and equipment. Focus on safety and comfort items.
                        Provide a concise list with brief explanations."""),
                        UserMessage(content=f"Recommend gear for: {preferences['difficulty']} difficulty, "
                                          f"{preferences['terrain']} terrain, {preferences['duration']} trip")
                    ]
                    
                    logger.info("Step 3 - Generating gear recommendations...")
                    start_time = time.time()
                    
                    response = chat_client.complete(
                        messages=messages,
                        max_tokens=150,
                        temperature=0.5
                    )
                    
                    end_time = time.time()
                    response_time = end_time - start_time
                    
                    gear_recommendations = response.choices[0].message.content
                    gear_span.set_attribute("response.time_ms", response_time * 1000)
                    gear_span.set_attribute("response.length", len(gear_recommendations))
                    gear_span.set_attribute("model.temperature", 0.5)
                    
                    logger.info("Step 3 - Gear recommendations generated successfully")
                    
                    results.append({
                        'step': 3,
                        'name': 'generate_gear_recommendations',
                        'input': preferences,
                        'output': gear_recommendations,
                        'response_time_ms': response_time * 1000,
                        'status': 'success'
                    })
                    
                except Exception as e:
                    logger.error(f"Step 3 failed: {e}")
                    gear_span.set_attribute("error.message", str(e))
                    gear_span.set_attribute("error.occurred", True)
                    
                    results.append({
                        'step': 3,
                        'name': 'generate_gear_recommendations',
                        'status': 'error',
                        'error': str(e)
                    })
            
            # Step 4: Finalize recommendations
            with tracer.start_as_current_span("finalize_recommendations") as final_span:
                final_span.set_attribute("step", 4)
                
                successful_steps = len([r for r in results if r.get('status') == 'success'])
                total_steps = len(results)
                
                final_span.set_attribute("workflow.successful_steps", successful_steps)
                final_span.set_attribute("workflow.total_steps", total_steps)
                final_span.set_attribute("workflow.success_rate", successful_steps / total_steps)
                
                final_recommendations = {
                    'trip_preferences': preferences,
                    'recommendations_generated': successful_steps,
                    'workflow_complete': successful_steps >= 2  # At least preferences and one recommendation
                }
                
                results.append({
                    'step': 4,
                    'name': 'finalize_recommendations',
                    'output': final_recommendations,
                    'status': 'success'
                })
                
                logger.info(f"Step 4 - Workflow completed with {successful_steps}/{total_steps} successful steps")
        
        except Exception as e:
            logger.error(f"Workflow error: {e}")
            main_span.set_attribute("workflow.error", str(e))
            main_span.set_attribute("workflow.failed", True)
        
        return results

def simulate_error_scenario(project_client, tracer):
    """Simulate an error scenario to demonstrate tracing capabilities"""
    logger.info("Simulating error scenario for tracing analysis...")
    
    with tracer.start_as_current_span("error_scenario_workflow") as error_span:
        session_id = str(uuid.uuid4())
        error_span.set_attribute("session.id", session_id)
        error_span.set_attribute("workflow.type", "error_simulation")
        
        try:
            # Simulate invalid input processing
            with tracer.start_as_current_span("process_invalid_input") as input_span:
                invalid_input = ""  # Empty input to trigger error
                input_span.set_attribute("input.value", invalid_input)
                input_span.set_attribute("input.length", len(invalid_input))
                
                if not invalid_input.strip():
                    error_message = "Empty input provided - cannot process request"
                    input_span.set_attribute("error.message", error_message)
                    input_span.set_attribute("error.type", "validation_error")
                    logger.error(error_message)
                    raise ValueError(error_message)
                
        except Exception as e:
            error_span.set_attribute("workflow.error_occurred", True)
            error_span.set_attribute("workflow.error_type", type(e).__name__)
            error_span.set_attribute("workflow.error_message", str(e))
            
            return {
                'error_scenario': 'invalid_input',
                'error_type': type(e).__name__,
                'error_message': str(e),
                'traced': True
            }

def main(ci_mode=False):
    """Main lab execution function"""
    logger.info("=== Lab 08: Tracing GenAI Application ===")
    
    results = {
        'lab': '08-tracing',
        'status': 'running',
        'tracing_setup': {},
        'workflow_traces': [],
        'error_traces': [],
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
        
        # Setup tracing
        tracing_success = setup_tracing(project_client)
        results['tracing_setup'] = {
            'instrumentation_enabled': tracing_success,
            'content_recording_enabled': os.getenv('AZURE_TRACING_GEN_AI_CONTENT_RECORDING_ENABLED') == 'true',
            'timestamp': time.time()
        }
        
        # Get tracer
        tracer = trace.get_tracer(__name__)
        
        # Run hiking assistant workflow with tracing
        workflow_results = simulate_hiking_assistant(project_client, tracer)
        results['workflow_traces'] = workflow_results
        
        # Run error scenario for tracing
        error_results = simulate_error_scenario(project_client, tracer)
        results['error_traces'] = [error_results]
        
        # Summary
        successful_workflow_steps = len([r for r in workflow_results if r.get('status') == 'success'])
        total_workflow_steps = len(workflow_results)
        
        results['summary'] = {
            'tracing_enabled': tracing_success,
            'workflows_executed': 2,  # hiking assistant + error scenario
            'total_spans_created': total_workflow_steps + 1,  # workflow steps + error span
            'successful_workflow_steps': successful_workflow_steps,
            'workflow_success_rate': f"{(successful_workflow_steps/total_workflow_steps)*100:.1f}%" if total_workflow_steps > 0 else "0%",
            'error_scenarios_traced': 1,
            'content_recording_enabled': results['tracing_setup']['content_recording_enabled']
        }
        
        results['status'] = 'success'
        logger.info(f"Lab completed successfully! Traced {total_workflow_steps} workflow steps and 1 error scenario")
        
        return results
        
    except Exception as e:
        logger.error(f"Lab execution failed: {e}")
        results['status'] = 'failed'
        results['error'] = str(e)
        return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Lab 08: Tracing GenAI Application")
    parser.add_argument("--ci-mode", action="store_true", help="Run in CI mode (no interactive prompts)")
    args = parser.parse_args()
    
    results = main(ci_mode=args.ci_mode)
    
    # Save results
    results_file = Path(__file__).parent / "tracing_results.json"
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to: {results_file}")
    print(f"Lab status: {results['status']}")
    
    if results.get('summary'):
        summary = results['summary']
        print(f"Tracing enabled: {summary.get('tracing_enabled', False)}")
        print(f"Workflows executed: {summary.get('workflows_executed', 0)}")
        print(f"Spans created: {summary.get('total_spans_created', 0)}")
        print(f"Content recording: {summary.get('content_recording_enabled', False)}")
    
    if results['status'] != 'success':
        sys.exit(1)