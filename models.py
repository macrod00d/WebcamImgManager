from pydantic import BaseModel
from datetime import datetime
from typing import List

class ImageMetadata(BaseModel):
    """
    Represents the metadata of an image.

    Attributes:
        title (str): The title of the image.
        description (str): The description of the image.
        timestamp (datetime): The timestamp of when the image was created.
        filepath (str): The filepath of the image.
    """

    title: str
    description: str
    timestamp: datetime
    filepath: str  # New attribute for the filepath of the image

    def update_metadata(self, title: str, description: str, tags: List[str], filepath: str):
        """
        Updates the metadata of the image.

        Args:
            title (str): The new title of the image.
            description (str): The new description of the image.
            filepath (str): The new filepath of the image.
        """
        self.title = title
        self.description = description
        self.filepath = filepath  # Update the filepath of the image