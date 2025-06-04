from sqlalchemy import Column, Integer, String, Text, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class Documento(Base):
    __tablename__ = "documentos"

    id = Column(Integer, primary_key=True)
    nome_arquivo = Column(String(255))
    data_vencimento = Column(String(50))
    condicionantes = Column(Text)

engine = create_engine("sqlite:///database.db", echo=True)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
    