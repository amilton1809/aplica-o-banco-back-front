from flask import Flask, jsonify, request
from flask_cors import CORS 
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Produto, Estoque, Venda, LogVenda

app = Flask(__name__)

# Adicionando CORS à aplicação
CORS(app)  # Permite todas as origens (origins) por padrão

engine = create_engine('sqlite:///loja.db')
Session = sessionmaker(bind=engine)
session = Session()

# Rota para a página inicial (evitar erro 404)
@app.route('/')
def home():
    return "Bem-vindo à página inicial da loja!"

# Rota para listar produtos
@app.route('/produtos', methods=['GET'])
def get_produtos():
    produtos = session.query(Produto).all()
    result = []
    for produto in produtos:
        estoques = [{'tamanho': estoque.tamanho, 'quantidade': estoque.quantidade} for estoque in produto.estoques]
        result.append({'id': produto.id, 'nome': produto.nome, 'estoques': estoques})
    return jsonify(result)

# Rota para vender produto
@app.route('/vender', methods=['POST'])
def vender_produto():
    data = request.json
    produto_id = data['produto_id']
    tamanho = data['tamanho']
    quantidade = data['quantidade']
    
    # Lógica de venda
    estoque = session.query(Estoque).filter_by(produto_id=produto_id, tamanho=tamanho).first()
    if estoque and estoque.quantidade >= quantidade:
        estoque.quantidade -= quantidade
        venda = Venda(produto_id=produto_id, tamanho=tamanho, quantidade=quantidade)
        session.add(venda)

        log = LogVenda(produto_nome=estoque.produto.nome, tamanho=tamanho, quantidade_vendida=quantidade)
        session.add(log)
        session.commit()
        
        return jsonify({'message': 'Venda realizada com sucesso!'})
    else:
        return jsonify({'message': 'Estoque insuficiente!'}), 400

if __name__ == '__main__':
    app.run(debug=True)
