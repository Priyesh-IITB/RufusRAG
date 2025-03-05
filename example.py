from rufus.utils import load_config, save_dict_to_json
from rufus import RufusClient
import sys

# Load configuration
config = load_config("config.yaml")

# Initialize client with configuration
client = RufusClient(**config)

# Set output filename
output_filename = "result.json"

# Default URL and prompt
start_url = "https://www.example.com/"
prompt = "Summarize what this website is about."

# Allow command line args to specify URL
if len(sys.argv) > 1:
    start_url = sys.argv[1]
    
if len(sys.argv) > 2:
    prompt = sys.argv[2]

# Print information about the request
print(f"Crawling URL: {start_url}")
print(f"With prompt: {prompt}")

try:
    # Execute the web crawling and analysis
    results = client.scrape(start_url, prompt, **config)
    
    # Save results to JSON file
    save_dict_to_json(results, output_filename)
    
    print(f"Results saved to {output_filename}")
except Exception as e:
    print(f"Error occurred: {e}")
    import traceback
    traceback.print_exc()
