# persistencia.py

from artista import Artista  # Certifique-se de que a classe Artista está importada corretamente
from concertos import Concerto
from reservas import Reserva
from datetime import datetime

def validar_data(data_str):
    try:
        data = datetime.strptime(data_str, '%Y-%m-%d')
        ano = data.year
        if 1880 <= ano <= 2024:
            return True
        return False
    except ValueError:
        return False

def gravar_artista(nome_ficheiro, artista):
    with open(nome_ficheiro, 'a', encoding='latin1') as f:
        f.write(str(artista) + '\n')
    print(f"Artista gravado em {nome_ficheiro} com sucesso.")

def carregar_artistas(filename):
    artistas = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                if line.strip():
                    dados = line.strip().split(',')
                    if len(dados) >= 4:
                        id, nome, estilo, data_nascimento = dados[:4]
                        contacto = dados[4] if len(dados) > 4 else ""
                        discografia = dados[5] if len(dados) > 5 else ""
                        artistas.append(Artista(int(id), nome, estilo, data_nascimento, 
                                              contacto, discografia))
    except FileNotFoundError:
        open(filename, 'w', encoding='utf-8').close()
    return artistas

def carregar_concertos(filename):
    concertos = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                if line.strip():
                    dados = line.strip().split(',')
                    if len(dados) >= 7:
                        id, artista, data, local, lugares, preco, bar_disponivel = dados[:7]
                        concertos.append(Concerto(
                            int(id), 
                            artista, 
                            data, 
                            local, 
                            int(lugares), 
                            float(preco),
                            bar_disponivel.lower() == 'true'
                        ))
    except FileNotFoundError:
        open(filename, 'w', encoding='utf-8').close()
    return concertos

def carregar_reservas(filename):
    reservas = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                if line.strip():
                    dados = line.strip().split(',')
                    if len(dados) == 7:
                        id, cliente, concerto, data, lugares, valor, status = dados
                        reservas.append(Reserva(int(id), cliente, concerto, data, int(lugares), float(valor), status))
    except FileNotFoundError:
        open(filename, 'w', encoding='utf-8').close()
    return reservas

def salvar_artistas(artistas, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        for artista in artistas:
            file.write(f"{artista.id},{artista.nome},{artista.estilo},"
                      f"{artista.data_nascimento},{artista.contacto},{artista.discografia}\n")

def salvar_concertos(concertos, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        for concerto in concertos:
            file.write(f"{concerto.id},{concerto.artista},{concerto.data},{concerto.local},"
                      f"{concerto.lugares_disponiveis},{concerto.preco},{concerto.bar_disponivel}\n")

def salvar_reservas(reservas, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        for reserva in reservas:
            file.write(f"{reserva.id},{reserva.nome_cliente},{reserva.concerto},{reserva.data_reserva},{reserva.num_lugares},{reserva.valor_total},{reserva.status}\n")
