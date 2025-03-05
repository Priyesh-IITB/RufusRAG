from rufus.utils import load_config, save_dict_to_json
from rufus import RufusClient

config = load_config("config.yaml")

client = RufusClient(**config)

output_filename = "result.json"

start_url = "https://www.google.com/"
prompt = "List all the services Google offers."

results = client.scrape(start_url, prompt, **config)

save_dict_to_json(results, output_filename)
