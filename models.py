from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from pydantic import BaseModel
from datetime import datetime

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

class ImageMetadata(BaseModel):
    """
    Represents the image metadata model for data validation.
    """
    title: str
    description: str
    timestamp: datetime
    filepath: str

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

    def add_image_metadata(self, title: str, description: str, filepath: str):
        """
        Adds image metadata to the database.

        Args:
            title (str): The title of the image.
            description (str): The description of the image.
            filepath (str): The filepath of the image.

        Returns:
            ImageMetadataModel: The newly created image metadata.
        """
        with SessionLocal() as session:
            new_image_metadata = ImageMetadataModel(
                title=title,
                description=description,
                filepath=filepath
            )
            session.add(new_image_metadata)
            session.commit()
            return new_image_metadata