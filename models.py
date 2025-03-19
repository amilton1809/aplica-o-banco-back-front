from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

# Base do ORM
Base = declarative_base()

# Definição da tabela Produto
class Produto(Base):
    __tablename__ = 'produtos'
    id = Column(Integer, primary_key=True)
    nome = Column(String, unique=True, nullable=False)
    # Relacionamento com Estoque
    estoques = relationship("Estoque", back_populates="produto")

# Definição da tabela Estoque
class Estoque(Base):
    __tablename__ = 'estoque'
    id = Column(Integer, primary_key=True)
    produto_id = Column(Integer, ForeignKey('produtos.id'))
    tamanho = Column(String, nullable=False)
    quantidade = Column(Integer, nullable=False)
    # Relacionamento com Produto
    produto = relationship("Produto", back_populates="estoques")

# Definição da tabela Venda
class Venda(Base):
    __tablename__ = 'vendas'
    id = Column(Integer, primary_key=True)
    produto_id = Column(Integer, ForeignKey('produtos.id'))
    tamanho = Column(String, nullable=False)
    quantidade = Column(Integer, nullable=False)

# Definição da tabela LogVenda
class LogVenda(Base):
    __tablename__ = 'logs_vendas'
    id = Column(Integer, primary_key=True)
    produto_nome = Column(String, nullable=False)
    tamanho = Column(String, nullable=False)
    quantidade_vendida = Column(Integer, nullable=False)

# Configuração do banco de dados SQLite
engine = create_engine('sqlite:///loja.db', echo=True)

# Criando todas as tabelas
Base.metadata.create_all(engine)

# Criando uma sessão para interagir com o banco
Session = sessionmaker(bind=engine)
session = Session()

# Exemplo para limpar os dados das tabelas e garantir que as tabelas estão vazias
session.query(LogVenda).delete()
session.query(Venda).delete()
session.query(Estoque).delete()
session.query(Produto).delete()
session.commit()

# Adicionar alguns dados de exemplo
camisa = Produto(nome="Camisa")
shorts = Produto(nome="Shorts")

session.add_all([camisa, shorts])
session.commit()

estoques = [
    Estoque(produto_id=camisa.id, tamanho="P", quantidade=10),
    Estoque(produto_id=camisa.id, tamanho="M", quantidade=8),
    Estoque(produto_id=camisa.id, tamanho="G", quantidade=15),
    Estoque(produto_id=shorts.id, tamanho="38", quantidade=10),
    Estoque(produto_id=shorts.id, tamanho="42", quantidade=8),
    Estoque(produto_id=shorts.id, tamanho="46", quantidade=15)
]

session.add_all(estoques)
session.commit()

print("Banco de dados populado com sucesso!")
