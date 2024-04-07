from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from pydantic import BaseModel
from datetime import datetime
from typing import List
from PIL import Image, ImageEnhance, ImageOps, ImageFilter
import numpy as np
import os

Base = declarative_base()
SessionLocal = sessionmaker()

class ImageMetadataModel(Base):
    """
    Represents the image metadata table in the database.
    """
    __tablename__ = 'image_metadata'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    filepath = Column(String, nullable=False)
    tags = Column(String, nullable=True)

class ImageMetadata(BaseModel):
    """
    Represents the image metadata model for data validation.
    """
    title: str
    description: str
    timestamp: datetime
    filepath: str
    tags: List[str]

class ImageMetadataDAO:
    """
    Data Access Object for image metadata operations. This provides abstraction for the database operations to make them more pythonic and readable.
    """
    def __init__(self, database_url='sqlite:///image_metadata.db'):
        """
        Initializes the ImageMetadataDAO with the given database URL.
        """
        self.engine = create_engine(database_url, echo=False)
        SessionLocal.configure(bind=self.engine)
        Base.metadata.create_all(bind=self.engine)

    def add_image_metadata(self, title: str, description: str, filepath: str, tags: List[str]):
        """
        Adds image metadata to the database.

        Args:
            title (str): The title of the image.
            description (str): The description of the image.
            filepath (str): The filepath of the image.
            tags (List[str]): The tags associated with the image.

        Returns:
            ImageMetadataModel: The newly created image metadata.
        """
        with SessionLocal() as session:
            new_image_metadata = ImageMetadataModel(
                title=title,
                description=description,
                filepath=filepath,
                tags = ', '.join(tag for tag in tags) #added a list comprehension here for the purpose of the assignment, although in this case it swould be more streamlined to simply do ', '.join(tags)
            )
            session.add(new_image_metadata)
            session.commit()
            return new_image_metadata

    def get_all_image_metadata(self):
        """
        Fetches all image metadata from the database.

        Returns:
            List[ImageMetadataModel]: A list of all image metadata.
        """
        with SessionLocal() as session:
            return session.query(ImageMetadataModel).all()

    def update_image_metadata(self, id: int, title: str, description: str, tags: List[str]):
        """
        Updates image metadata in the database.

        Args:
            id (int): The ID of the image metadata to update.
            title (str): The new title of the image.
            description (str): The new description of the image.
            tags (List[str]): The new tags associated with the image.

        Returns:
            ImageMetadataModel: The updated image metadata.
        """
        print(", ".join(tags))
        with SessionLocal() as session:
            image_metadata = session.query(ImageMetadataModel).filter(ImageMetadataModel.id == id).one()
            image_metadata.title = title
            image_metadata.description = description
            image_metadata.tags = ",".join(tags)  # Convert list of strings to a single string
            print(image_metadata.tags, type(image_metadata.tags))
            session.commit()
            return image_metadata

    def get_image_metadata(self, id: int):
        """
        Fetches a single image metadata entry from the database by its ID.

        Args:
            id (int): The ID of the image metadata to fetch.

        Returns:
            ImageMetadataModel: The requested image metadata.
        """
        with SessionLocal() as session:
            return session.query(ImageMetadataModel).filter(ImageMetadataModel.id == id).one()

    def delete_image_metadata(self, id: int):
        """
        Deletes image metadata from the database.

        Args:
            id (int): The ID of the image metadata to delete.
        """
        with SessionLocal() as session:
            image_metadata = session.query(ImageMetadataModel).filter(ImageMetadataModel.id == id).one()
            session.delete(image_metadata)
            session.commit()

    def apply_greyscale_effect(self, id: int):
        with SessionLocal() as session:
            image_metadata = session.query(ImageMetadataModel).filter(ImageMetadataModel.id == id).one()

            try:
                img = Image.open(image_metadata.filepath)
                img = img.convert("L")
                img.save(image_metadata.filepath)
            except Exception as e:
                print(f"Error applying greyscale effect: {e}")
                raise e

    def apply_sepia_effect(self, filepath):
        try:
            img = Image.open(filepath)
            img = img.convert("L")
            sepia = np.array(img)
            sepia = Image.fromarray(sepia)
            sepia = ImageOps.colorize(sepia, (107, 74, 47), (207, 190, 183))
            sepia.save(filepath)
        except Exception as e:
            print(f"Error applying sepia effect: {e}")
            raise e

    def apply_invert_effect(self, filepath):
        try:
            img = Image.open(filepath)
            img = ImageOps.invert(img)
            img.save(filepath)
        except Exception as e:
            print(f"Error applying invert effect: {e}")
            raise e

    def apply_sketch_effect(self, filepath):
        try:
            img = Image.open(filepath)
            img = img.convert("L")  # Convert to grayscale
            edges = img.filter(ImageFilter.FIND_EDGES)
            sketch = ImageOps.invert(edges)
            sketch.save(filepath)
        except Exception as e:
            print(f"Error applying sketch effect: {e}")
            raise e

    def adjust_brightness(self, filepath, factor):
        try:
            img = Image.open(filepath)
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(factor)
            img.save(filepath)
        except Exception as e:
            print(f"Error adjusting brightness: {e}")
            raise e

    def adjust_contrast(self, filepath, factor):
        try:
            img = Image.open(filepath)
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(factor)
            img.save(filepath)
        except Exception as e:
            print(f"Error adjusting contrast: {e}")
            raise e

    def restore_original(self, filepath):
        try:
            original_path = f"{filepath[:-4]}-ORIGINAL.png"
            if os.path.exists(original_path):
                img = Image.open(original_path)
                img.save(filepath)
        except Exception as e:
            print(f"Error restoring original image: {e}")
            raise e

    





