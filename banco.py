from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

# Criar conexão com SQLite
engine = create_engine('sqlite:///loja.db', echo=True)

# Base para o ORM
Base = declarative_base()

# Definição da tabela Produto
class Produto(Base):
    __tablename__ = 'produtos'
    id = Column(Integer, primary_key=True)
    nome = Column(String, unique=True, nullable=False)
    estoques = relationship("Estoque", back_populates="produto")

# Definição da tabela Estoque
class Estoque(Base):
    __tablename__ = 'estoque'
    id = Column(Integer, primary_key=True)
    produto_id = Column(Integer, ForeignKey('produtos.id'))
    tamanho = Column(String, nullable=False)
    quantidade = Column(Integer, nullable=False)
    produto = relationship("Produto", back_populates="estoques")

# Definição da tabela Vendas
class Venda(Base):
    __tablename__ = 'vendas'
    id = Column(Integer, primary_key=True)
    produto_id = Column(Integer, ForeignKey('produtos.id'))
    tamanho = Column(String, nullable=False)
    quantidade = Column(Integer, nullable=False)

# Definição da tabela Logs de Vendas
class LogVenda(Base):
    __tablename__ = 'logs_vendas'
    id = Column(Integer, primary_key=True)
    produto_nome = Column(String, nullable=False)
    tamanho = Column(String, nullable=False)
    quantidade_vendida = Column(Integer, nullable=False)

# Criar o banco de dados e as tabelas
Base.metadata.create_all(engine)

# Criar uma sessão para interagir com o banco
Session = sessionmaker(bind=engine)
session = Session()

# Limpar tabelas
session.query(LogVenda).delete()
session.query(Venda).delete()
session.query(Estoque).delete()
session.query(Produto).delete()
session.commit()

# Adicionar produtos
camisa = Produto(nome="Camisa")
shorts = Produto(nome="Shorts")
session.add_all([camisa, shorts])
session.commit()

# Adicionar estoques
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

# Função para processar vendas e registrar logs
def processar_venda(produto_id, tamanho, quantidade):
    estoque = session.query(Estoque).filter_by(produto_id=produto_id, tamanho=tamanho).first()
    produto = session.query(Produto).filter_by(id=produto_id).first()
    if estoque and estoque.quantidade >= quantidade:
        estoque.quantidade -= quantidade
        venda = Venda(produto_id=produto_id, tamanho=tamanho, quantidade=quantidade)
        session.add(venda)
        
        # Registrar no log de vendas
        log = LogVenda(produto_nome=produto.nome, tamanho=tamanho, quantidade_vendida=quantidade)
        session.add(log)
        
        session.commit()
        print(f"Venda realizada: {quantidade} unidade(s) de {produto.nome} - {tamanho}.")
    else:
        print("Estoque insuficiente!")

# Exemplo de venda
processar_venda(camisa.id, "M", 2)
processar_venda(shorts.id, "42", 3)

# Consulta de estoque atualizada
produtos = session.query(Produto).all()
for produto in produtos:
    print(f"\nProduto: {produto.nome}")
    for estoque in produto.estoques:
        print(f"  Tamanho: {estoque.tamanho}, Quantidade: {estoque.quantidade}")

# Exibir logs de vendas
print("\n=== Logs de Vendas ===")
logs = session.query(LogVenda).all()
for log in logs:
    print(f"{log.produto_nome} {log.tamanho} VENDIDOS {log.quantidade_vendida} unid")
