from pydantic import BaseModel, Field

class AutonomousPostInput(BaseModel):
    subreddit: str = Field(..., example="technology", description="Subreddit to fetch trending topics from.")
