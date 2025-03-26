# /services/topic_service.py

import aiohttp


class TopicService:
    BASE_URL = "https://www.reddit.com/r/{subreddit}/hot.json?limit=10"

    async def get_trending_topics(self, subreddit="brazil", limit=5, time_range="day") -> list[str]:
        url = self.BASE_URL.format(subreddit=subreddit)
        params = {"limit": str(limit), "t": time_range}
        headers = {"User-Agent": "BlogAgent/1.0"}

        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url, params=params) as response:
                if response.status != 200:
                    raise Exception(f"Failed to fetch topics: {response.status}")
                
                data = await response.json()
                posts = data.get("data", {}).get("children", [])
                return [post["data"]["title"] for post in posts]
