
import aiohttp
import random

from tenacity import retry, wait_random, stop_after_attempt

from utils.log_utils import logger


class TopicService:
    """
    Service responsible for fetching trending topics from Reddit.
    """

    BASE_URL = "https://www.reddit.com/r/{subreddit}/hot.json"

    @retry(wait=wait_random(min=1, max=3), stop=stop_after_attempt(3))
    async def get_trending_topics(
        self,
        subreddit: str = "programing",
        limit: int = 15,
        time_range: str = "day",
        sample_size: int = 1
    ) -> list[str]:
        """
        Fetches trending topics from a specified subreddit and returns random samples.

        Args:
            subreddit (str): The subreddit to fetch topics from (default: "technology").
            limit (int): Number of topics to fetch from Reddit (default: 15).
            time_range (str): Time filter for the Reddit API (not used for /hot, kept for future flexibility).
            sample_size (int): Number of random topics to return (default: 1).

        Returns:
            list[str]: A list containing random topic titles.

        Raises:
            Exception: If the request fails or no topics are found.
        """
        logger.info(f"Fetching trending topics from r/{subreddit}...")
        url = self.BASE_URL.format(subreddit=subreddit)
        params = {"limit": str(limit)}
        headers = {"User-Agent": "BlogAgent/1.0"}

        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url, params=params) as response:
                if response.status != 200:
                    raise Exception(f"Failed to fetch topics: {response.status}")

                data = await response.json()
                
                posts = data.get("data", {}).get("children", [])
                logger.info(f"Received {len(posts)} raw posts from Reddit")

                all_titles = [post["data"]["title"] for post in posts]
                logger.info(f"Fetched {len(all_titles)} topics from r/{subreddit}")
                if not all_titles:
                    raise Exception("No topics found in the subreddit.")
                choice = random.sample(all_titles, k=min(sample_size, len(all_titles)))
                return choice

