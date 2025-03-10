import uuid
from datetime import datetime

# Lista para armazenar os concertos e reservas
concertos = []
reservas = []

FICHEIRO_CONCERTOS = "concertos.txt"  # Arquivo para salvar os concertos

def criar_concerto(artistas):
    print("\n=== Criar Novo Concerto ===")
    
    # Mostrar artistas disponíveis
    print("\nArtistas disponíveis:")
    for artista in artistas:
        print(f"ID: {artista.id} - Nome: {artista.nome}")
    
    id_artista = input("Digite o ID do artista: ")
    # Verificar se o artista existe
    artista_encontrado = False
    nome_artista = ""
    for artista in artistas:
        if str(artista.id) == id_artista:
            artista_encontrado = True
            nome_artista = artista.nome
            break
    
    if not artista_encontrado:
        print("Artista não encontrado!")
        return

    local = input("Local do concerto: ")

    # Validação da data
    while True:
        data = input("Data do concerto (formato dd/mm/aaaa): ")
        try:
            data_obj = datetime.strptime(data, "%d/%m/%Y")
            if data_obj < datetime(2025, 1, 1):
                print("A data do concerto não pode ser antes de 01/01/2025!")
                continue
            data = data_obj.strftime("%d/%m/%Y")
            break
        except ValueError:
            print("Data inválida! Use o formato dd/mm/aaaa.")

    hora = input("Hora do concerto (HH:MM): ")
    
    while True:
        try:
            capacidade = int(input("Capacidade do estabelecimento: "))
            if capacidade <= 0:
                print("A capacidade deve ser maior que zero!")
                continue
            break
        except ValueError:
            print("Por favor, digite um número válido para a capacidade!")

    while True:
        try:
            preco_bilhete = float(input("Preço do bilhete (€): "))
            if preco_bilhete < 0:
                print("O preço não pode ser negativo!")
                continue
            break
        except ValueError:
            print("Por favor, digite um valor válido para o preço!")

    bar_disponivel = input("Bar disponível (s/n): ").lower() == "s"

    # Criar o dicionário do concerto
    concerto = {
        "id": str(uuid.uuid4()),
        "artista_id": id_artista,
        "artista_nome": nome_artista,
        "local": local,
        "data": data,
        "hora": hora,
        "capacidade": capacidade,
        "preco_bilhete": preco_bilhete,
        "bar_disponivel": bar_disponivel,
        "lugares_ocupados": 0,
    }
    
    # Adicionar à lista de concertos
    concertos.append(concerto)
    
    # Gravar diretamente no arquivo
    try:
        with open("concertos.txt", "a") as f:
            f.write(f"{concerto['id']},{concerto['artista_nome']},{concerto['local']},"
                   f"{concerto['data']},{concerto['hora']},{concerto['capacidade']},{concerto['preco_bilhete']},"
                   f"{concerto['bar_disponivel']},{concerto['lugares_ocupados']}\n")
        print(f"Concerto de '{nome_artista}' criado com sucesso! ID: {concerto['id']}")
    except Exception as e:
        print(f"Erro ao gravar o concerto no arquivo: {e}")
        return None
    return concerto['id']

## Função para listar concertos
def listar_concertos():
    print("\n=== Visualizar Concertos ===")
    try:
        with open("concertos.txt", "r") as arquivo:
            concertos = [linha.strip().split(",") for linha in arquivo.readlines()]
    except FileNotFoundError:
        print("Nenhum concerto encontrado.")
        return

    print(f"Total de concertos disponíveis: {len(concertos)}")
    id_concerto = input("Insira o ID do concerto para visualizar: ")

    for concerto in concertos:
        if concerto[0].strip() == id_concerto.strip():  # Adicionado .strip() para remover espaços extras
            print("\n=== Detalhes do Concerto ===")
            print(f"ID: {concerto[0]}")
            print(f"Artista: {concerto[1]}")
            print(f"Local: {concerto[2]}")
            print(f"Data: {concerto[3]}")
            print(f"Hora: {concerto[4]}")
            print(f"Capacidade: {concerto[5]}")
            print(f"Preço: {concerto[6]}€")
            print(f"Bar disponível: {'Sim' if concerto[7] == 'True' else 'Não'}")
            print(f"Lugares ocupados: {concerto[8]}")
            return

    print("Concerto não encontrado.")

# Função para gravar concertos no arquivo
def gravar_concertos(arquivo):
    try:
        with open(arquivo, "w") as f:
            for concerto in concertos:
                f.write(
                    f"{concerto['id']},{concerto['nome']},{concerto['local']},{concerto['data']},{concerto['hora']},"
                    f"{concerto['capacidade']},{concerto['preco_bilhete']},{concerto['bar_disponivel']},"
                    f"{concerto['lugares_ocupados']}\n")
        print("Concertos gravados no arquivo com sucesso!")
    except Exception as e:
        print(f"Erro ao gravar concertos: {e}")

# Função para carregar concertos do arquivo
def carregar_concertos(arquivo):
    try:
        with open(arquivo, "r") as f:
            for linha in f:
                id, nome, local, data, hora, capacidade, preco_bilhete, bar_disponivel, lugares_ocupados = linha.strip().split(",")
                concertos.append(
                    {"id": id, "nome": nome, "local": local, "data": data, "hora": hora, "capacidade": int(capacidade),
                     "preco_bilhete": float(preco_bilhete), "bar_disponivel": bar_disponivel == "True",
                     "lugares_ocupados": int(lugares_ocupados)})
        print("Concertos carregados do arquivo com sucesso!")
    except FileNotFoundError:
        print("Arquivo não encontrado. Nenhum concerto carregado.")

