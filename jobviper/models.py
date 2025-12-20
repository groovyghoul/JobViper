from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    company = Column(String, nullable=False)
    title = Column(String, nullable=False)
    applied_date = Column(Date, nullable=False)
    status = Column(String, default="applied")
    source = Column(String)

    contacts = relationship("Contact", back_populates="job")
    results = relationship("Result", back_populates="job")

    def __repr__(self):
        return f"<Job(id={self.id}, company='{self.company}', title='{self.title}')>"

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"))
    date = Column(Date, nullable=False)
    type = Column(String)
    person = Column(String)
    notes = Column(String)

    job = relationship("Job", back_populates="contacts")

    def __repr__(self):
        return f"<Contact(id={self.id}, job_id={self.job_id}, type='{self.type}')>"

class Result(Base):
    __tablename__ = "results"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"))
    date = Column(Date, nullable=False)
    status = Column(String, nullable=False)
    notes = Column(String)

    job = relationship("Job", back_populates="results")

    def __repr__(self):
        return f"<Result(id={self.id}, job_id={self.job_id}, status='{self.status}')>"
