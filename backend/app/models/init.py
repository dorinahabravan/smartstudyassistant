#Python file with all your models
from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from backend.app.database import Base
from datetime import datetime


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True , nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash= Column(String(255), nullable=False)
    created_at= Column(DateTime, default=datetime.utcnow)

class Topics(Base):
    __tablename__ = 'topics'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text)
    source = Column(String(50))
    date_fetched= Column(DateTime, default=datetime.utcnow)
    resources = Column(Text, nullable=True)  # ✅ Add this line

class Quizzes(Base):
    __tablename__ ='quizzes'

    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey('topics.id'))
    question = Column(String(255))
    correct_answer= Column(String(255), nullable=False)
    option_a= Column(String(255))
    option_b= Column(String(255))
    option_c= Column(String(255))
    option_d= Column(String(255))
    created_at= Column(DateTime, default=datetime.utcnow)

class UserProgress(Base):
    __tablename__ = 'user_progress'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    topic_id = Column(Integer, ForeignKey('topics.id'))
    quiz_score = Column(Integer)
    completed = Column(Boolean, default=False)
    updated_at= Column(DateTime, default=datetime.utcnow)

  
class TopicDependency(Base):
    __tablename__ = "topic_dependencies"

    id = Column(Integer, primary_key=True , index=True)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    prerequisite_id = Column(Integer, ForeignKey("topics.id"), nullable=False)