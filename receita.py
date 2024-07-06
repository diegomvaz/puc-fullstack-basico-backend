from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, JSON, Boolean
from flask_sqlalchemy import SQLAlchemy


Base = declarative_base()
db = SQLAlchemy(model_class=Base)

class Receita(db.Model):
    __tablename__ = 'receita'

    id = Column(Integer, primary_key=True)
    nome = Column(String)
    ingredientes = Column(JSON)
    descricao = Column(String)
    imagemBase64 = Column(String)
    like = Column(Boolean, default=False)


