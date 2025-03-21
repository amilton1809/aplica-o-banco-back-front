from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Produto, Estoque, Venda, LogVenda

# Configuração do banco
engine = create_engine('sqlite:///loja.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

def processar_venda(produto_id, tamanho, quantidade):
    estoque = session.query(Estoque).filter_by(produto_id=produto_id, tamanho=tamanho).first()
    produto = session.query(Produto).filter_by(id=produto_id).first()
    
    if estoque and estoque.quantidade >= quantidade:
        estoque.quantidade -= quantidade
        venda = Venda(produto_id=produto_id, tamanho=tamanho, quantidade=quantidade)
        session.add(venda)
        
        log = LogVenda(
            produto_nome=produto.nome,
            tamanho=tamanho,
            quantidade_vendida=quantidade
        )
        session.add(log)
        session.commit()
        print(f"Venda realizada: {quantidade} unidade(s) de {produto.nome} - {tamanho}.")
    else:
        print("Estoque insuficiente!")

if __name__ == '__main__':
    # Exemplo de uso (só executa se o arquivo for rodado diretamente)
    processar_venda(1, "M", 2)  # Venda de Camisa M
    processar_venda(2, "42", 3) # Venda de Shorts 42

    # Consulta de estoque atualizado
    produtos = session.query(Produto).all()
    for produto in produtos:
        print(f"\nProduto: {produto.nome}")
        for estoque in produto.estoques:
            print(f"  Tamanho: {estoque.tamanho}, Quantidade: {estoque.quantidade}")

    # Exibir logs
    print("\n=== Logs de Vendas ===")
    logs = session.query(LogVenda).all()
    for log in logs:
        print(f"{log.produto_nome} {log.tamanho} VENDIDOS {log.quantidade_vendida} unid")