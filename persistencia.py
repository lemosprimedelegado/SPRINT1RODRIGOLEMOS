# Lista para armazenar os concertos, reservas e artistas
concertos = []
reservas = []

class Artista:
    def __init__(self, nome, genero):
        self.nome = nome
        self.genero = genero
    
    def __str__(self):
        return f"{self.nome},{self.genero}"
    
    @staticmethod
    def from_string(dados):
        partes = dados.strip().split(',')
        if len(partes) == 2:
            return Artista(partes[0], partes[1])
        return None

def adicionar_concerto(concerto):
    concertos.append(concerto)

def adicionar_reserva(reserva):
    reservas.append(reserva)

def obter_concerto_por_id(concerto_id):
    return next((c for c in concertos if c["id"] == concerto_id), None)

def obter_reservas():
    return reservas

def obter_concertos():
    return concertos

def atualizar_lugares_ocupados(concerto_id, lugares):
    concerto = obter_concerto_por_id(concerto_id)
    if concerto:
        concerto["lugares_ocupados"] += lugares

def gravar_artista(nome_ficheiro, artista):
    with open(nome_ficheiro, 'a', encoding='latin1') as f:
        f.write(str(artista) + '\n')
    print(f"Artista gravado em {nome_ficheiro} com sucesso")

def carregar_artistas(nome_ficheiro):
    artistas = []
    try:
        with open(nome_ficheiro, 'r', encoding='latin1') as f:
            for linha in f:
                print(f"Tentando ler linha: '{linha}'")  # Debug
                artista = Artista.from_string(linha)
                if artista:
                    artistas.append(artista)
    except FileNotFoundError:
        print(f"Arquivo {nome_ficheiro} não encontrado.")
    return artistas
