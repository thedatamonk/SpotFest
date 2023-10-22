from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime
from decouple import config
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    # Add additional fields as needed (e.g., profile picture, bio, etc.)

    rsvps = relationship("RSVP", back_populates="user")
    events = relationship("Event", back_populates="host")

    def verify_password(self, plain_password):
        return pwd_context.verify(plain_password, self.hashed_password)

    @staticmethod
    def get_password_hash(plain_password):
        return pwd_context.hash(plain_password)
    

class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    location = Column(String, nullable=False)
    date_time = Column(DateTime, default=datetime.utcnow)
    host_id = Column(Integer, ForeignKey('users.id'))
    category_id = Column(Integer, ForeignKey('categories.id'))

    host = relationship("User", back_populates="events")
    rsvps = relationship("RSVP", back_populates="event")
    category = relationship("Category", back_populates="events")

class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    events = relationship("Event", back_populates="category")

class RSVP(Base):
    __tablename__ = 'rsvps'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    event_id = Column(Integer, ForeignKey('events.id'))
    # attending = Column(Boolean, default=True)

    user = relationship("User", back_populates="rsvps")
    event = relationship("Event", back_populates="rsvps")



DATABASE_URL = f"postgresql://{config('DEFAULT_USER')}:{config('DEFAULT_PASSWORD')}@localhost/{config('DATABASE_NAME')}"
engine = create_engine(DATABASE_URL)

# Create tables
Base.metadata.create_all(engine)
