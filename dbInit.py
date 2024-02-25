from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.sqlite import JSON
from datetime import datetime

# Import the Pydantic model from models.py
from models import ImageMetadata as PydanticImageMetadata

Base = declarative_base()

class ImageMetadataModel(Base):
    __tablename__ = 'image_metadata'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    filepath = Column(String, nullable=False)

    def __repr__(self):
        return (f"<ImageMetadata(title='{self.title}', description='{self.description}', "
                f"timestamp={self.timestamp}, filepath='{self.filepath}')>")

# Create the SQLite database and tables
engine = create_engine('sqlite:///image_metadata.db', echo=False)
Base.metadata.create_all(engine)