# persistencia.py

from artista import Artista  # Certifique-se de que a classe Artista está importada corretamente

def gravar_artista(nome_ficheiro, artista):
    with open(nome_ficheiro, 'a', encoding='latin1') as f:
        f.write(str(artista) + '\n')
    print(f"Artista gravado em {nome_ficheiro} com sucesso.")

def carregar_artistas(arquivo):
    artistas = []
    try:
        with open(arquivo, "r") as f:
            for linha in f:
                # Ignorar linhas em branco
                if not linha.strip():
                    continue
                
                # Tentar dividir a linha e verificar se tem 6 valores
                partes = linha.strip().split(',')
                if len(partes) != 6:
                    print(f"Linha ignorada (formato inválido): {linha.strip()}")
                    continue
                
                id, nome, genero, data_nascimento, contacto, discografia = partes
                artista = Artista(nome, genero, data_nascimento, contacto, discografia)  # Corrigido para 'Artista'
                artista.id = int(id)
                artistas.append(artista)
    except FileNotFoundError:
        print(f"O arquivo {arquivo} não foi encontrado.")
    return artistas

def carregar_concertos(arquivo):
    concertos = []
    try:
        with open(arquivo, "r") as f:
            for linha in f:
                # Ignorar linhas em branco
                if not linha.strip():
                    continue
                
                # Tentar dividir a linha e verificar se tem 4 valores
                partes = linha.strip().split(',')
                if len(partes) != 4:
                    print(f"Linha ignorada (formato inválido): {linha.strip()}")
                    continue
                
                artista, data, local, ingressos = partes
                concerto = Concerto(artista, data, local, int(ingressos))  # Cria a instância do concerto
                concertos.append(concerto)
    except FileNotFoundError:
        print(f"O arquivo {arquivo} não foi encontrado.")
    return concertos

def carregar_reservas(arquivo):
    reservas = []
    try:
        with open(arquivo, "r") as f:
            for linha in f:
                nome_cliente, artista, quantidade = linha.strip().split(',')
                reserva = Reserva(nome_cliente, artista, int(quantidade))
                reservas.append(reserva)
    except FileNotFoundError:
        print(f"O arquivo {arquivo} não foi encontrado.")
    return reservas
