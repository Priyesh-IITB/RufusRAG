import logging
import numpy as np
from urllib.parse import urlparse
import aiohttp
import asyncio
import yaml
import json

def setup_logging(log_file="rufus.log", level="DEBUG"):
    """Set up logging for RUFUS."""
    logging.basicConfig(
        filename=log_file,
        filemode='a',
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=getattr(logging, level),
    )
    logger = logging.getLogger("RUFUSLogger")
    return logger

def format_results(output, start_url=None, prompt=None):
    """Structure the output of crawl/ranked crawl."""
    structured_data = {
        "start_url": start_url,
        "prompt": prompt,
        "results": []
    }
    if isinstance(output, list) and all(isinstance(item, tuple) for item in output):
        structured_data['results'] = [{"doc": doc, "rank_score": float(rank_score)} for doc, rank_score in output]
    elif isinstance(output, list) and all(isinstance(item, str) for item in output):
        structured_data['results'] = [{"doc": doc} for doc in output]
    else:
        structured_data['results'] = output
    return structured_data

def load_config(filename="config.yaml"):
    """Load YAML config file."""
    with open(filename, 'r') as stream:
        return yaml.safe_load(stream)

def save_dict_to_json(data, filename="data.json"):
    """Save a dictionary to a JSON file."""
    with open(filename, "w") as json_file:
        json.dump(data, json_file, indent=4)

def is_valid_url(url):
    """Check if the URL is valid and properly formatted."""
    parsed_url = urlparse(url)
    return bool(parsed_url.scheme in ["http", "https"] and parsed_url.netloc)

async def is_url_online(url, timeout=30):
    """Check if the URL is online by sending a HEAD request."""
    try:
        client_timeout = aiohttp.ClientTimeout(
            total=timeout,
            sock_connect=timeout/2,
            sock_read=timeout/2
        )
        async with aiohttp.ClientSession() as session:
            async with session.head(url, timeout=client_timeout, ssl=False) as response:
                return 200 <= response.status < 400
    except (aiohttp.ClientError, asyncio.TimeoutError, asyncio.CancelledError):
        # Try with GET request as some servers don't support HEAD
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=client_timeout, ssl=False) as response:
                    return 200 <= response.status < 400
        except:
            return False

async def persistent_request(url, session=None, retries=3, delay=1.5, headers=None, timeout=30, logger=None):
    """Fetch webpage content with retries, handling timeouts and client errors."""
    if logger is None:
        logger = logging.getLogger("RUFUSLogger")
    attempts = 0
    while attempts < retries:
        try:
            # Create a client timeout with reasonable parameters
            client_timeout = aiohttp.ClientTimeout(
                total=timeout,
                sock_connect=timeout/2,
                sock_read=timeout/2
            )
            
            if session:
                async with session.get(url, headers=headers, timeout=client_timeout, ssl=False) as response:
                    response.raise_for_status()
                    return await response.text()
            else:
                async with aiohttp.ClientSession() as temp_session:
                    async with temp_session.get(url, headers=headers, timeout=client_timeout, ssl=False) as response:
                        response.raise_for_status()
                        return await response.text()
        except (aiohttp.ClientError, asyncio.TimeoutError, asyncio.CancelledError) as e:
            attempts += 1
            logger.warning(f"Attempt {attempts} for {url} failed: {e}")
            if attempts == retries:
                logger.error(f"All {retries} attempts failed for {url}")
                return None
            await asyncio.sleep(delay)
    return None

def cosine_similarity(a, b):
    """Compute cosine similarity between two arrays."""
    a = np.array(a)
    b = np.array(b)
    a_norm = a / np.linalg.norm(a, axis=-1, keepdims=True)
    b_norm = b / np.linalg.norm(b, axis=-1, keepdims=True)
    return np.sum(a_norm * b_norm, axis=-1)

def pairwise_distance(a, b):
    """Compute Euclidean similarity between two arrays."""
    a = np.array(a)
    b = np.array(b)
    diff = a[..., np.newaxis, :] - b[np.newaxis, ...]
    distances = np.sqrt(np.sum(diff ** 2, axis=-1))
    return 1 / (1 + distances)