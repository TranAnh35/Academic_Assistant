# services/integrations/google_scholar.py
import logging
import asyncio
from typing import List
from scholarly import scholarly, ProxyGenerator

from models.document import Document # Đường dẫn mới

logger = logging.getLogger(__name__)

# Cấu hình proxy nếu cần thiết (ví dụ: chạy trên môi trường bị chặn)
# try:
#     pg = ProxyGenerator()
#     # Cấu hình proxy của bạn ở đây, ví dụ:
#     # success = pg.Tor_Internal(tor_sock_port=9050, tor_control_port=9051, tor_password="your_password")
#     # if success:
#     #     scholarly.use_proxy(pg)
#     #     logger.info("Using Tor proxy for scholarly.")
#     # else:
#     #     logger.warning("Failed to configure Tor proxy for scholarly.")
#     # Hoặc dùng FreeProxy
#     # pg.FreeProxies()
#     # scholarly.use_proxy(pg)
# except Exception as e:
#      logger.error(f"Error setting up proxy for scholarly: {e}")


async def search(query: str, number: int = 10) -> List[Document]:
    """
    Search for papers on Google Scholar based on the given query.
    Args:
        query (str): The search query
        number (int): Maximum number of results (default: 10)
    Returns:
        List[Document]: A list of documents containing the search results
    Raises:
        ValueError: If input arguments are invalid.
        RuntimeError: If the search fails.
    """
    if not query or not isinstance(query, str):
        logger.error(f"Invalid query received: {query}")
        raise ValueError("Query must be a non-empty string")
    if not isinstance(number, int) or number < 1:
        logger.error(f"Invalid number received: {number}")
        raise ValueError("Number must be a positive integer")

    logger.info(f"Initiating Google Scholar search for: '{query}' (max {number} results)")
    results = []

    try:
        loop = asyncio.get_running_loop()
        search_generator = await loop.run_in_executor(
            None,
            lambda: scholarly.search_pubs(query)
        )

        processed_count = 0
        while processed_count < number:
            try:
                result = await loop.run_in_executor(None, lambda: next(search_generator, None))
                if result is None: # Hết kết quả
                    break

                # Fill a publication (lấy thêm chi tiết) - cũng là blocking I/O
                # result = await loop.run_in_executor(None, lambda: scholarly.fill(result))
                # Lưu ý: fill() có thể làm chậm đáng kể và dễ bị block. Cân nhắc chỉ dùng thông tin cơ bản.

                bib_data = result.get('bib', {})
                authors_raw = bib_data.get('author', 'Unknown Author')

                if isinstance(authors_raw, str):
                    authors = [a.strip() for a in authors_raw.split(' and ')]
                elif isinstance(authors_raw, list):
                    authors = authors_raw
                else:
                    authors = ['Unknown Author']

                doc = Document(
                    title=bib_data.get('title', 'Untitled'),
                    authors=authors,
                    year=str(bib_data.get('pub_year', 'Unknown')),
                    abstract=bib_data.get('abstract', 'No abstract available'),
                    url=result.get('eprint_url', result.get('pub_url', 'No URL available'))
                )
                results.append(doc)
                processed_count += 1
                logger.debug(f"Processed result {processed_count}: {doc.title}")

            except StopIteration:
                logger.info("Reached end of search results.")
                break
            except Exception as e:
                logger.error(f"Error processing individual search result: {e}", exc_info=True)
                logger.debug(f"Problematic result data (if available): {result}")

    except Exception as e:
        logger.error(f"Google Scholar search failed for query '{query}': {e}", exc_info=True)
        raise RuntimeError(f"Failed to perform search for '{query}': {e}")

    logger.info(f"Found {len(results)} results for query: '{query}'")
    return results

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    query = "Gemini 2.0 Flash"
    number = 5
    results = asyncio.run(search(query, number)) 
    for doc in results:
        print(f"Title: {doc.title}, Authors: {doc.authors}, Year: {doc.year}, Abstract: {doc.abstract}, URL: {doc.url}")