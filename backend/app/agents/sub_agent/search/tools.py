import logging
import asyncio
from typing import List
from scholarly import scholarly, ProxyGenerator

from models.document import Document

logger = logging.getLogger(__name__)

def _setup_scholarly():
    """Setup scholarly with proxy to avoid blocking"""
    try:
        pg = ProxyGenerator()
        # FreeProxies might raise exceptions if it fails to find proxies
        pg.FreeProxies() 
        logger.info("Attempting to set scholarly proxy...")
        # The warning originates from this call potentially due to internal httpx client init issues
        scholarly.use_proxy(pg)
        logger.info("Scholarly proxy setup completed (check logs for warnings).")
    except TypeError as e:
        # Catch the specific TypeError related to the warning
        if "__init__" in str(e) and "proxies" in str(e):
            logger.warning(f"Handled known proxy setup issue: {e}. Scholarly might still function.")
        else:
            # Re-raise unexpected TypeErrors
            logger.error(f"Unexpected TypeError during proxy setup: {e}")
            raise e
    except Exception as e:
        # Catch other potential exceptions during setup
        logger.error(f"Failed to setup proxy due to an unexpected error: {e}")
        # Decide if failure to set proxy should halt execution or just be logged

async def search(query: str, number: int = 10) -> List[Document]:
    """
    Search for papers on Google Scholar based on the given query.
    Args:
        query (str): The search query
        number (int): Maximum number of results (default: 10)
    Returns:
        List[Document]: A list of documents containing the search results
    """
    
    
    
    if not query or not isinstance(query, str):
        raise ValueError("Query must be a non-empty string")
    if not isinstance(number, int) or number < 1:
        raise ValueError("Number must be a positive integer")

    logger.info(f"Searching for: {query}")
    results = []
        
    try:
        search_query = scholarly.search_pubs(query)
        for i, result in enumerate(search_query):
            if i >= number:
                break
                    
            try:
                # Extract fields with fallbacks for missing data
                bib_data = result.get('bib', {})
                authors_raw = bib_data.get('author', 'Unknown Author')
                
                # Handle authors whether it's a string or list
                if isinstance(authors_raw, str):
                    authors = authors_raw.split(' and ')
                elif isinstance(authors_raw, list):
                    authors = authors_raw # Assume Document expects a list
                else:
                    authors = ['Unknown Author']

                document = Document(
                    title=bib_data.get('title', 'Untitled'),
                    authors=authors, 
                    year=bib_data.get('pub_year', 'Unknown'), # Use 'pub_year'
                    abstract=bib_data.get('abstract', 'No abstract available'),
                    url=result.get('pub_url', '') # Use 'pub_url'
                )
                results.append(document)
            except Exception as e:
                logger.error(f"Error processing result {i}: {e}")
                logger.debug(f"Problematic result data: {result}") # Add debug log
                continue
                    
    except Exception as e:
        logger.error(f"Search failed: {e}")
        raise RuntimeError(f"Failed to perform search: {e}")
            
    logger.info(f"Found {len(results)} results")
    return results

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    query = "Gemini 2.0 Flash"
    number = 5
    results = asyncio.run(search(query, number)) 
    for doc in results:
        print(f"Title: {doc.title}, Authors: {doc.authors}, Year: {doc.year}, Abstract: {doc.abstract}, URL: {doc.url}")