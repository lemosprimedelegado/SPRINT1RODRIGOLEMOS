# persistencia_artista.py

from artista import Artista

def gravar_artista(nome_ficheiro, artista):
    with open(nome_ficheiro, 'a', encoding='latin1') as f:
        f.write(str(artista) + '\n')
    print(f"Artistas gravados {nome_ficheiro} com sucesso")

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
    
    
