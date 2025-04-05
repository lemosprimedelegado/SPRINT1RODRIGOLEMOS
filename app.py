from flask import Flask, request, jsonify, render_template
from persistencia import carregar_artistas, carregar_concertos, carregar_reservas, salvar_artistas, salvar_concertos, salvar_reservas
from artista import Artista
from concertos import Concerto
from reservas import Reserva
from datetime import datetime

app = Flask(__name__, template_folder='templates')

# Lists to store data
artistas = []
concertos = []
reservas = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/artistas/')
def listar_artistas():
    search = request.args.get('search', '').lower()
    if search:
        filtered_artistas = [
            artista for artista in artistas 
            if search in str(artista.id).lower() or search in artista.nome.lower()
        ]
    else:
        filtered_artistas = artistas
    return render_template('artistas.html', artistas=filtered_artistas)

@app.route('/concertos/')
def listar_concertos():
    search = request.args.get('search', '').lower()
    if search:
        filtered_concertos = [
            concerto for concerto in concertos 
            if search in str(concerto.id).lower() or search in concerto.artista.lower()
        ]
    else:
        filtered_concertos = concertos
    return render_template('concertos.html', concertos=filtered_concertos, artistas=artistas)

@app.route('/reservas/')
def listar_reservas():
    return render_template('reservas.html', reservas=reservas)

@app.route('/add_artista', methods=['POST'])
def add_artista():
    try:
        data = request.get_json()
        id = len(artistas) + 1
        nome = data.get('nome')
        estilo = data.get('estilo')
        data_nascimento = data.get('data_nascimento')
        contacto = data.get('contacto')
        discografia = data.get('discografia')

        if not nome or not estilo or not data_nascimento:
            return jsonify({'error': 'Dados incompletos'}), 400

        novo_artista = Artista(id, nome, estilo, data_nascimento, contacto, discografia)
        artistas.append(novo_artista)
        salvar_artistas(artistas, "artistas.txt")

        return jsonify({'message': 'Artista adicionado com sucesso!'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/remove_artista', methods=['DELETE'])
def remove_artista():
    try:
        data = request.get_json()
        id = data.get('id')

        if not id:
            return jsonify({'error': 'ID não fornecido'}), 400

        global artistas
        artistas = [artista for artista in artistas if artista.id != id]
        salvar_artistas(artistas, "artistas.txt")  # Save after removing

        return jsonify({'message': 'Artista removido com sucesso!'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/update_artista', methods=['PUT'])
def update_artista():
    try:
        data = request.get_json()
        id = data.get('id')
        nome = data.get('nome')
        estilo = data.get('estilo')
        data_nascimento = data.get('data_nascimento')
        contacto = data.get('contacto')
        discografia = data.get('discografia')

        if not all([id, nome, estilo, data_nascimento]):
            return jsonify({'error': 'Dados incompletos'}), 400

        artista = next((a for a in artistas if a.id == id), None)
        if not artista:
            return jsonify({'error': 'Artista não encontrado'}), 404

        artista.nome = nome
        artista.estilo = estilo
        artista.data_nascimento = data_nascimento
        artista.contacto = contacto or ""
        artista.discografia = discografia or ""

        salvar_artistas(artistas, "artistas.txt")
        return jsonify({'message': 'Artista atualizado com sucesso!'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/add_concerto', methods=['POST'])
def add_concerto():
    try:
        data = request.get_json()
        id = len(concertos) + 1
        artista = data.get('artista')
        data_concerto = data.get('data')
        local = data.get('local')
        lugares = data.get('lugares_disponiveis')
        preco = data.get('preco')
        bar_disponivel = data.get('bar_disponivel', '').lower() == 's'

        if not all([artista, data_concerto, local, lugares, preco]):
            return jsonify({'error': 'Dados incompletos'}), 400

        # Validate concert date
        try:
            data_concerto_obj = datetime.strptime(data_concerto, '%Y-%m-%d')
            if data_concerto_obj.year < 2025:
                return jsonify({'error': 'Data inválida. O concerto deve ser realizado a partir de 2025'}), 400
        except ValueError:
            return jsonify({'error': 'Formato de data inválido. Use YYYY-MM-DD'}), 400

        novo_concerto = Concerto(id, artista, data_concerto, local, 
                                int(lugares), float(preco), bar_disponivel)
        concertos.append(novo_concerto)
        salvar_concertos(concertos, "concertos.txt")

        return jsonify({
            'message': f'Concerto Adicionado! ID: {id}',
            'id': id
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/add_reserva', methods=['POST'])
def add_reserva():
    try:
        data = request.get_json()
        id = len(reservas) + 1
        nome_cliente = data.get('nome_cliente')
        concerto_id = data.get('concerto_id')
        num_lugares = data.get('num_lugares')
        
        if not all([nome_cliente, concerto_id, num_lugares]):
            return jsonify({'error': 'Dados incompletos'}), 400

        # Encontrar o concerto
        concerto = next((c for c in concertos if c.id == concerto_id), None)
        if not concerto:
            return jsonify({'error': 'Concerto não encontrado'}), 404

        if concerto.lugares_disponiveis < int(num_lugares):
            return jsonify({'error': 'Lugares insuficientes'}), 400

        valor_total = float(concerto.preco) * int(num_lugares)
        nova_reserva = Reserva(id, nome_cliente, concerto_id, data.get('data_reserva', ''), 
                             num_lugares, valor_total)
        
        reservas.append(nova_reserva)
        concerto.lugares_disponiveis -= int(num_lugares)
        
        salvar_reservas(reservas, "reservas.txt")
        salvar_concertos(concertos, "concertos.txt")

        return jsonify({'message': 'Reserva realizada com sucesso!', 
                       'valor_total': valor_total}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/remove_concerto', methods=['DELETE'])
def remove_concerto():
    try:
        data = request.get_json()
        id = data.get('id')

        if not id:
            return jsonify({'error': 'ID não fornecido'}), 400

        global concertos
        concerto = next((c for c in concertos if c.id == id), None)
        if not concerto:
            return jsonify({'error': 'Concerto não encontrado'}), 404

        concertos.remove(concerto)
        salvar_concertos(concertos, "concertos.txt")
        return jsonify({'message': 'Concerto removido com sucesso!'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/update_concerto', methods=['PUT'])
def update_concerto():
    try:
        data = request.get_json()
        id = data.get('id')
        artista = data.get('artista')
        data_concerto = data.get('data')
        local = data.get('local')
        lugares = data.get('lugares_disponiveis')
        preco = data.get('preco')
        bar_disponivel = data.get('bar_disponivel', '').lower() == 's'

        if not all([id, artista, data_concerto, local, lugares, preco]):
            return jsonify({'error': 'Dados incompletos'}), 400

        # Validate concert date
        try:
            data_concerto_obj = datetime.strptime(data_concerto, '%Y-%m-%d')
            if data_concerto_obj.year < 2025:
                return jsonify({'error': 'Data inválida. O concerto deve ser realizado a partir de 2025'}), 400
        except ValueError:
            return jsonify({'error': 'Formato de data inválido. Use YYYY-MM-DD'}), 400

        concerto = next((c for c in concertos if c.id == id), None)
        if not concerto:
            return jsonify({'error': 'Concerto não encontrado'}), 404

        concerto.artista = artista
        concerto.data = data_concerto
        concerto.local = local
        concerto.lugares_disponiveis = int(lugares)
        concerto.preco = float(preco)
        concerto.bar_disponivel = bar_disponivel

        salvar_concertos(concertos, "concertos.txt")
        return jsonify({'message': 'Concerto atualizado com sucesso!'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/cancel_reserva', methods=['DELETE'])
def cancel_reserva():
    try:
        data = request.get_json()
        id = data.get('id')

        if not id:
            return jsonify({'error': 'ID não fornecido'}), 400

        global reservas
        reserva = next((r for r in reservas if r.id == id), None)
        if not reserva:
            return jsonify({'error': 'Reserva não encontrada'}), 404

        # Devolver lugares ao concerto
        concerto = next((c for c in concertos if c.id == reserva.concerto), None)
        if concerto:
            concerto.lugares_disponiveis += reserva.num_lugares

        reservas = [r for r in reservas if r.id != id]
        
        salvar_reservas(reservas, "reservas.txt")
        salvar_concertos(concertos, "concertos.txt")

        return jsonify({'message': 'Reserva cancelada com sucesso!'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Carregar dados iniciais
    artistas = carregar_artistas("artistas.txt")
    concertos = carregar_concertos("concertos.txt")
    reservas = carregar_reservas("reservas.txt")
    app.run(debug=True)
