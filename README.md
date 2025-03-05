# RUFUS: Retrieval and Understanding Framework for Unstructured Sources

RUFUS is a Python-based information retrieval system designed to efficiently retrieve and rank content from various sources on the web and is being developed with the idea of seamless integration with Retrieval-Augmented Generation (RAG) pipelines. Using AI-powered web crawling, RUFUS navigates complex web structures to selectively retrieve and synthesize relevant data into structured JSON format. This simplifies the process of collecting and structuring online data for AI models and applications.

Disclaimer: This project was developed as a solution to a timed case study by Chima AI.

# Features

- Intelligent Web Scraping: Extract structured data from websites effortlessly.
- Scalable and Flexible: Modular architecture allows for easy integration and extension of components without extensive refactoring.
- Content Ranking: Determines the importance of documents and ranks them accordingly, allowing for highly tuned, relevant document retrieval.
- Seamless RAG Integration: Plug-and-Play tool with RAG pipelines for improved data retrieval.
- Customizable Configs: Tailor extraction rules with YAML configuration files.
- Efficient: Handles recursive URL traces with optimized scraping algorithms.

# How does RUFUS work?
RUFUS primarily works on web scraping through recursive HTML scraping from the user-provided URL. Users can configure the maximum depth i.e. the number of nested links that should be opened from the starter URL, along with several other parameters. These configurations can be stored in YAML and provided to the RufusClient API.

In the event that the URL is invalid or offline, RUFUS leverages LLMs and web search to generate and search the web for links that are likely to yield relevant content for the user's prompt. The collected documents are then processed and structured for use in other applications, including storage and RAG applications.

# Usage

```python
from rufus import RufusClient
from rufus.utils import load_config

config = load_config("config.yaml")

client = RufusClient(**config)

start_url = "https://www.apple.com"
prompt = "List all the services and products offered by Apple."

docs = client.scrape(start_url, prompt, **config)
