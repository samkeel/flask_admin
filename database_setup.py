from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from datetime import datetime
from sqlalchemy.orm import backref

from sqlalchemy.orm import relationship

Base = declarative_base()


class Documents(Base):
    __tablename__ = 'documents'

    doc_id = Column(Integer, primary_key=True)
    project = Column(String(), nullable=True)
    doc_name = Column(String(), nullable=False)
    revision = Column(String(), nullable=False)
    pub_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    pub_update = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    # one-to-one relationship with DocTitles
    title = relationship("DocTitles", uselist=False, back_populates="doc_parent")


    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'doc_id': self.doc_id,
            'project': self.project,
            'doc_name': self.doc_name,
            'revision': self.revision,
            'pub_date': self.pub_date,
            'pub_update': self.pub_update,
            'title': self.title
            }


class DocTitles(Base):
    __tablename__ = 'doc_title'

    _id = Column(Integer, primary_key=True)
    doc_num = Column(Integer, ForeignKey('documents.doc_id'))
    doc_parent = relationship("Documents", back_populates="title")
    title_line_1 = Column(String(), nullable=True)
    title_line_2 = Column(String(), nullable=True)
    title_line_3 = Column(String(), nullable=True)
    title_line_4 = Column(String(), nullable=True)


    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            '_id': self._id,
            'doc_num': self.doc_num,
            'title_line_1': self.title_line_1,
            'title_line_2': self.title_line_2,
            'title_line_3': self.title_line_3,
            'title_line_4': self.title_line_4,
            'doc_parent': self.doc_parent
            }


engine = create_engine('sqlite:///docs.db')


Base.metadata.create_all(engine)