from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from datetime import datetime
from sqlalchemy.orm import backref, relationship


Base = declarative_base()

# Parent
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(25), nullable=False)
    # pw = Column(String(25), nullable=False)
    email = Column(String(100), nullable=False)
    display_name = Column(String(50), nullable=False)
    # relationship
    docs = relationship("Documents")

# Child
class Documents(Base):
    __tablename__ = 'documents'

    doc_id = Column(Integer, primary_key=True)
    # relationship
    user_id = Column(Integer, ForeignKey('user.id'))
    # Document details
    doc_title = Column(String(255), nullable=False)
    # tested for large paragraphs. no loss of text on 978 word test
    doc_contents = Column(String(), nullable=True)
    doc_summary = Column(String(255), nullable=True)
    # datetime columns
    pub_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    pub_update = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)


engine = create_engine('postgresql://testuser:test123@localhost/docs')


Base.metadata.create_all(engine)
