import aiohttp
import asyncio
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from rufus.utils import setup_logging, persistent_request, is_valid_url, is_url_online, format_results
from rufus.core.extraction import extract_text
from rufus.llms.method import generate_search_query
from rufus.search_engines.method import get_search_results
from rufus.content_rankers.method import rank_content

class Crawler:
    def __init__(self, max_depth=2, delay=1.5, log_file="rufus.log", log_level="DEBUG", headers=None, num_search_results=10, **kwargs):
        self.url_tracker = set()
        self.max_depth = max_depth
        self.request_delay = delay
        self.logger = setup_logging(log_file=log_file, level=log_level)
        self.headers = headers
        self.num_search_results = num_search_results
        self.timeout = kwargs.get("timeout", 5)
    
    async def _fetch_page(self, url, session, retries=3):
        return await persistent_request(url, session, retries, self.request_delay, self.headers, self.timeout, self.logger)
    
    def _validate_url(self, url):
        return is_valid_url(url)
    
    async def _check_url_online(self, url):
        return await is_url_online(url, self.timeout)
    
    def _parse_links(self, soup, curr_url):
        links = []
        for link in soup.find_all("a", href=True):
            url = urljoin(curr_url, link["href"])
            if url not in self.url_tracker and self._validate_url(url):
                links.append(url)
        return links
    
    async def _crawl(self, url, depth=0, session=None):
        if depth > self.max_depth or url in self.url_tracker:
            return []
        
        self.logger.info(f"Crawling: {url}")
        self.url_tracker.add(url)
        
        html_content = await self._fetch_page(url, session)
        if html_content is None:
            return []
        
        cleaned_text = extract_text(html_content)
        soup = BeautifulSoup(html_content, "lxml")
        data = [cleaned_text]
        
        links = self._parse_links(soup, url)
        tasks = [self._crawl(link, depth + 1, session) for link in links]
        results = await asyncio.gather(*tasks)
        
        for result in results:
            data.extend(result)
        
        return data
    
    async def start_crawl(self, start_url, prompt, do_rank=True, structured_output=True, **kwargs):
        if not self._validate_url(start_url):
            self.logger.error(f"Invalid URL: {start_url}")
            query = generate_search_query(prompt, start_url, **kwargs)
            search_results = get_search_results(query, num_results=self.num_search_results, **kwargs)
        else:
            is_online = await self._check_url_online(start_url)
            if not is_online:
                self.logger.error(f"URL offline: {start_url}")
                query = generate_search_query(prompt, start_url, **kwargs)
                search_results = get_search_results(query, num_results=self.num_search_results, **kwargs)
            else:
                search_results = [start_url]
        
        async def crawl_with_semaphore(url, session):
            async with asyncio.Semaphore(10):
                return await self._crawl(url, 0, session)
        
        search_data = []
        async with aiohttp.ClientSession() as session:
            tasks = [crawl_with_semaphore(url, session) for url in search_results]
            results = await asyncio.gather(*tasks)
        
        for result in results:
            if result:
                search_data.extend(result)
        
        if do_rank and search_data:
            search_data = rank_content(ref_txt=[prompt] * len(search_data), candidate_txt=search_data, **kwargs)
        
        if structured_output:
            search_data = format_results(search_data, start_url, prompt)
        
        return search_data
