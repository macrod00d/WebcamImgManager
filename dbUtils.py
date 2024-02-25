from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

engine = create_engine('sqlite:///image_metadata.db', echo=False)
Session = sessionmaker(bind=engine)
Base = declarative_base()

class ImageMetadataModel(Base):
    __tablename__ = 'image_metadata'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    filepath = Column(String, nullable=False)

def insert_image_metadata(title: str, description: str, filepath: str) -> None:
    session = Session()
    try:
        new_image_metadata = ImageMetadataModel(
            title=title,
            description=description,
            filepath=filepath
        )
        session.add(new_image_metadata)
        session.commit()
        print(f"Image metadata for '{title}' added successfully.")
    except Exception as e:
        session.rollback()
        print(f"An error occurred: {e}")
    finally:
        session.close()

def init_db():
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    init_db()