from sqlalchemy import Column, Integer, String, create_engine, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from fastapi_storages import FileSystemStorage
from fastapi_storages.integrations.sqlalchemy import FileType

storage = FileSystemStorage(path="tmp/")

Base = declarative_base()
engine = create_engine("sqlite:///tables.db")

class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True, unique=True)
    title = Column(String(100), nullable=False)
    description = Column(Text)
    image = Column(FileType(storage=storage))

    project_shots = relationship("ProjectShots", back_populates="project")

    def __str__(self):
        return self.title


class ProjectShots(Base):
    __tablename__ = "project_shots"

    id = Column(Integer, primary_key=True, unique=True)
    project_id = Column(Integer, ForeignKey('projects.id'))
    image = Column(FileType(storage=storage))

    project = relationship("Project", back_populates="project_shots")

    def __str__(self):
        return self.project.title



class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True, unique=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone_number = Column(String)
    message = Column(String)

class Application(Base):
    __tablename__ = 'applications'
    
    id = Column(Integer, primary_key=True, unique=True)
    phone = Column(String)
    message = Column(String)

Base.metadata.create_all(engine)