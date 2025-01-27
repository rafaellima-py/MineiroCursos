from sqlalchemy import Column, Integer, String
from  sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
Base = declarative_base()
engine = create_engine('sqlite:///cursos.db')
Session = sessionmaker(bind=engine)
session = Session()

class Curso(Base):
    __tablename__ = "cursos"

    id = Column(Integer, primary_key=True, index=True)
    imagem = Column(String, nullable=True)
    nome = Column(String, nullable=False)
    categoria = Column(String, nullable=True)
    tipo = Column(String, nullable=True)
    tamanho = Column(String, nullable=True)
    duracao = Column(String, nullable=True)
    autor = Column(String, nullable=True)
    link_curso = Column(String, nullable=True)
#Base.metadata.create_all(engine)



def insert_curso( imagem=None,
                    nome=None,
                    categoria=None,
                    tipo=None, tamanho=None, duracao=None, autor=None, link_curso=None):
    session.add(Curso(nome=nome, imagem=imagem, tamanho=tamanho,tipo=tipo,
                           categoria=categoria,
                           duracao=duracao, autor=autor, link_curso=link_curso))
    session.commit()
    
    session.close()


