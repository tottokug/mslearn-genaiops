import os
import uuid  # TRACING: For generating unique session IDs
import json
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
# TRACING: Import Azure Monitor for sending telemetry to Application Insights
from azure.monitor.opentelemetry import configure_azure_monitor
# TRACING: Import OpenTelemetry instrumentor to automatically capture OpenAI API calls
from opentelemetry.instrumentation.openai_v2 import OpenAIInstrumentor

# Load environment and set session ID
load_dotenv()
# TRACING: Generate a unique session ID to correlate all operations in this run
SESSION_ID = str(uuid.uuid4())
# TRACING: Enable capturing of message content (prompts and responses) in traces
os.environ['OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT'] = 'true'

myEndpoint = os.getenv("AZURE_EXISTING_AIPROJECT_ENDPOINT")

project_client = AIProjectClient(
    endpoint=myEndpoint,
    credential=DefaultAzureCredential(),
)

# TRACING: Configure telemetry and instrument tracing
# Get Application Insights connection string from the AI project
ai_conn_str = project_client.telemetry.get_application_insights_connection_string()
# Configure Azure Monitor to send all telemetry to Application Insights
configure_azure_monitor(connection_string=ai_conn_str)
# Instrument OpenAI client to automatically create spans for all agent calls
OpenAIInstrumentor().instrument()

myAgent = os.getenv("AZURE_EXISTING_AGENT_ID")
# Get an existing agent
agent = project_client.agents.get(agent_name=myAgent)
print(f"Retrieved agent: {agent.name}")

openai_client = project_client.get_openai_client()

# Mock product database as a string for the prompt
mock_product_database = """
Available Products in Lakeshore Retail Database:
1. Alpine Trekking Boots - Heavy-duty hiking boots
2. Waterproof Backpack - 40L capacity backpack
3. Carbon Fiber Hiking Poles - Lightweight trekking poles
4. Thermal Base Layers - Cold weather clothing
5. Ultralight Tent - 2-person camping tent
6. Solar-Powered Lantern - Rechargeable camping light
7. Comfort Fit Hiking Shoes - Day hiking footwear
8. Insulated Water Bottles - Temperature control bottles
9. Lightweight Dog Harness - Pet hiking gear
10. Dog Hiking Saddle Bags - Pet cargo bags
11. Compact First Aid Kit - Emergency medical supplies
12. Multi-Tool Knife - Camping utility tool
13. Trail Mix Energy Bars - Hiking snacks
"""

# ---- Main Flow ----
if __name__ == "__main__":
   print("\n--- Trail Guide AI Assistant with Agent ---")
   preferences = input("Tell me what kind of hike you're looking for (location, difficulty, scenery):\n> ")
   
   # STEP 1: Recommend a hike
   hike_prompt = f"""
You are a hiking trail guide. Based on these user preferences, recommend a specific named hiking trail:

USER PREFERENCES: {preferences}

Provide the trail name and a one-sentence summary.
Return your response in this EXACT JSON format:
{{
  "hikeName": "Trail Name Here",
  "hikeSummary": "One sentence description"
}}

Return ONLY valid JSON, no markdown formatting or extra text.
"""

   response = openai_client.responses.create(
       input=[{"role": "user", "content": hike_prompt}],
       extra_body={"agent": {"name": agent.name, "type": "agent_reference"}},
   )

   output = response.output_text

   print("🔍 Hike recommendation response:", output)

   try:
       hike_result = json.loads(output)
       hike_name = hike_result['hikeName']
       hike_summary = hike_result['hikeSummary']
       print(f"\n✅ Recommended Hike: {hike_name}")
       print(f"   {hike_summary}")
   except json.JSONDecodeError as e:
       print("❌ JSON decode error:", e)
       exit(1)

   # STEP 2: Generate trip profile
   profile_prompt = f"""
You are a hiking expert. For the following hike, create a detailed trip profile:

HIKE: {hike_name}

Generate a trip profile with:
- Trail type (e.g., loop, out-and-back, point-to-point)
- Typical weather conditions
- Recommended gear (list 3-5 essential items as short names like "boots", "backpack", "poles")

Return your response in this EXACT JSON format:
{{
  "trailType": "loop/out-and-back/point-to-point",
  "typicalWeather": "Weather description",
  "recommendedGear": ["item1", "item2", "item3"]
}}

Return ONLY valid JSON, no markdown formatting or extra text.
"""

   response = openai_client.responses.create(
       input=[{"role": "user", "content": profile_prompt}],
       extra_body={"agent": {"name": agent.name, "type": "agent_reference"}},
   )

   output = response.output_text

   print("🔍 Trip profile response:", output)

   try:
       profile = json.loads(output)
       print(f"\n📋 Trip Profile:")
       print(f"   Trail Type: {profile['trailType']}")
       print(f"   Weather: {profile['typicalWeather']}")
       print(f"   Recommended Gear: {', '.join(profile['recommendedGear'])}")
   except json.JSONDecodeError as e:
       print("❌ JSON decode error:", e)
       exit(1)

   # STEP 3: Match products from database (using LLM as a "database lookup tool")
   product_prompt = f"""
You are a product database lookup tool. Match the following gear items with products from our database:

GEAR ITEMS TO MATCH: {', '.join(profile['recommendedGear'])}

PRODUCT DATABASE:
{mock_product_database}

Find products in the database that match the gear items. Match based on keywords and relevance.

Return your response in this EXACT JSON format:
{{
  "matchedProducts": ["Product Name 1", "Product Name 2", "Product Name 3"]
}}

Only include products that actually exist in the database above.
Return ONLY valid JSON, no markdown formatting or extra text.
"""

   response = openai_client.responses.create(
       input=[{"role": "user", "content": product_prompt}],
       extra_body={"agent": {"name": agent.name, "type": "agent_reference"}},
   )

   output = response.output_text

   print("🔍 Product matching response:", output)

   try:
       product_result = json.loads(output)
       matched_products = product_result['matchedProducts']
       
       print(f"\n🛒 Matched Products from Lakeshore Retail:")
       for product in matched_products:
           print(f"   - {product}")
   except json.JSONDecodeError as e:
       print("❌ JSON decode error:", e)

   # TRACING: Print session ID so you can search for this session's traces in Application Insights
   print(f"\n🔍 Session ID for Application Insights: {SESSION_ID}")
