from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from database import Base

class DocumentMetadata(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    upload_date = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String) # "PENDING", "PROCESSED", "ERROR"
    doc_type = Column(String) # "ORDONNANCE", "COMPTE-RENDU", etc.