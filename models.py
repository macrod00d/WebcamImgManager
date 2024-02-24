from pydantic import BaseModel
from datetime import datetime
from typing import List

class ImageMetadata(BaseModel):
    """
    Represents the metadata of an image.

    Attributes:
        title (str): The title of the image.
        description (str): The description of the image.
        tags (List[str]): The tags associated with the image.
        timestamp (datetime): The timestamp of when the image was created.
    """

    title: str
    description: str
    tags: List[str]
    timestamp: datetime

    def update_metadata(self, title: str, description: str, tags: List[str]):
        """
        Updates the metadata of the image.

        Args:
            title (str): The new title of the image.
            description (str): The new description of the image.
            tags (List[str]): The new tags associated with the image.
        """
        self.title = title
        self.description = description
        self.tags = tags