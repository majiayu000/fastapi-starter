from typing import List
from pydantic import BaseModel, Field


class SearchResult(BaseModel):
    id: int = Field(..., description="The unique identifier of the search result")


class SearchRecord(BaseModel):
    id: int = Field(..., description="The unique identifier of the search record")
    user_id: int = Field(..., description="The ID of the user")
    user_grade_id: str = Field(..., description="The current grade level of the user")
    search_content: str = Field(
        ..., description="The search keyword entered by the user"
    )
    search_time: str = Field(
        ...,
        description="The time when the user performed the search (format: YYYY-MM-DD HH:MM)",
    )
    search_results_id: SearchResult = Field(
        ..., description="The unique identifier of the search results"
    )
    search_results_id_list: List[int] = Field(
        ..., description="The list of unique identifiers for sample documents"
    )
    search_time_taken: float = Field(
        ..., description="The time taken for the search request in seconds"
    )
    user_device: str = Field(
        ..., description="The device used by the user during the search"
    )
