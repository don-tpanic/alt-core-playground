"""Response models for the prompts."""

from pydantic import BaseModel, Field


class SummarizeMethods(BaseModel):
    """Output for summarize_methods prompt."""

    methods: str = Field(description="Summary of the paper's methods in sentence form")
