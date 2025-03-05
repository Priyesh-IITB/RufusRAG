import pytest
import aiohttp
import asyncio
from rufus.core.crawler import Crawler

@pytest.mark.asyncio
async def test_crawl():
    crawler = Crawler(max_depth=0, delay=0.5)
    start_url = "https://www.wikipedia.org/"
    prompt = "What are the different names of mango in each language on Wikipedia?"
    config = {
        "llm_provider": "google",
        "llm_api_key": "AIzaSyAfn-WV-ZhcpT-GwpRY6J-FyQcMn5zlT14",
        "llm_name": "models/gemini-1.5-flash-latest",
        "embd_model_provider": "google",
        "embd_model_api_key": "AIzaSyAfn-WV-ZhcpT-GwpRY6J-FyQcMn5zlT14",
        "embd_model_name": "models/text-embedding-004"
    }
    async with aiohttp.ClientSession() as session:
        result = await crawler.start_crawl(start_url, prompt, **config)
    assert len(result) > 0
