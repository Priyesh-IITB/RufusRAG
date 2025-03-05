import asyncio
from rufus.core.crawler import Crawler

class RufusClient:
    def __init__(self, max_depth=2, delay=1.5, num_search_results=10, do_rank=True, structured_output=True, log_file="rufus.log", log_level="INFO", headers=None, timeout=30, **kwargs):
        """
        Initialize the RufusClient.

        :param max_depth: int, maximum depth to crawl
        :param delay: float, delay between requests in seconds
        :param num_search_results: int, number of search results to use
        :param do_rank: boolean, whether to do ranking or not
        :param structured_output: boolean, whether to return structured output or not
        :param log_file: string, path to log file
        :param log_level: string, log level
        :param headers: dict, headers to add to requests
        :param timeout: int, timeout for HTTP requests in seconds
        """
        self.num_search_results = num_search_results
        self.do_rank = do_rank
        self.structured_output = structured_output
        self.crawler = Crawler(
            max_depth=max_depth,
            delay=delay,
            log_file=log_file,
            log_level=log_level,
            headers=headers,
            num_search_results=num_search_results,
            timeout=timeout
        )
    
    async def start(self, start_url, prompt, **kwargs):
        """Start crawling and ranking asynchronously."""
        results = await self.crawler.start_crawl(start_url, prompt, **kwargs)
        return results
    
    def scrape(self, start_url, prompt, **kwargs):
        """Start crawling and ranking synchronously using asyncio event loop."""
        return asyncio.run(self.start(start_url, prompt, **kwargs))
