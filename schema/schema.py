from pydantic.v1 import BaseModel, Field
from typing import List, Optional


class UserIntent(BaseModel):
    """Tag the text with the following information.
    If you are not sure, you can leave the field empty.
    """

    name: str = Field(
        description="Travel destination that the user is talking about."
    )
    intent: str = Field(
        description="""The topic the user wants to talk about. Can be one of the following:
                         - "airports": The user wants to know the airports near the travel destination.
                         - "hotels": The user wants to know the hotels near the travel destination.
                         - "restraunts": The user wants to know the restraunts near the travel destination."""
    )
