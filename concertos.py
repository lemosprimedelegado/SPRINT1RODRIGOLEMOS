import uuid
from datetime import datetime

# Lista para armazenar os concertos e reservas
concertos = []
reservas = []

FICHEIRO_CONCERTOS = "concertos.txt"  # Arquivo para salvar os concertos

# Função para criar um concerto
def criar_concerto():
    print("\n=== Criar Concerto ===")
    nome = input("Nome do artista: ")
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
        "nome": nome,
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
            f.write(f"{concerto['id']},{concerto['nome']},{concerto['local']},{concerto['data']},{concerto['hora']},"
                   f"{concerto['capacidade']},{concerto['preco_bilhete']},{concerto['bar_disponivel']},{concerto['lugares_ocupados']}\n")
        print(f"Concerto '{nome}' criado com sucesso! ID: {concerto['id']}")
    except Exception as e:
        print(f"Erro ao gravar o concerto no arquivo: {e}")
        return None

    return concerto['id']

# Função para listar concertos
def listar_concertos():
    print("\n=== Lista de Concertos ===")
    if not concertos:
        print("Nenhum concerto disponível.")
        return
    for concerto in concertos:
        print(f"ID: {concerto['id']} | Nome: {concerto['nome']} | Local: {concerto['local']} | "
              f"Data: {concerto['data']} | Hora: {concerto['hora']} | Capacidade: {concerto['capacidade']} | "
              f"Lugares Ocupados: {concerto['lugares_ocupados']}")

# Função para reservar lugar
def reservar_lugar():
    print("\n=== Reservar Lugar ===")
    listar_concertos()
    concerto_id = input("Insira o ID do concerto para reservar: ")

    # Verificar se o concerto existe
    concerto = next((c for c in concertos if c["id"] == concerto_id), None)
    if not concerto:
        print("Concerto não encontrado!")
        return

    lugares = int(input("Quantos lugares deseja reservar? "))
    if concerto["lugares_ocupados"] + lugares > concerto["capacidade"]:
        print("Lugares insuficientes disponíveis!")
        return

    # Calcular preço total
    total = lugares * concerto["preco_bilhete"]

    # Criar reserva
    reserva = {
        "id": str(uuid.uuid4()),
        "concerto_id": concerto_id,
        "lugares": lugares,
        "total": total,
        "data_reserva": datetime.now().strftime("%d/%m/%Y %H:%M"),
    }
    reservas.append(reserva)
    concerto["lugares_ocupados"] += lugares
    print(f"Reserva efetuada com sucesso! ID: {reserva['id']}")

# Função para listar reservas
def listar_reservas():
    print("\n=== Lista de Reservas ===")
    if not reservas:
        print("Nenhuma reserva encontrada.")
        return
    for reserva in reservas:
        concerto = next((c for c in concertos if c["id"] == reserva["concerto_id"]), None)
        print(f"Reserva ID: {reserva['id']} | Concerto: {concerto['nome']} | Lugares: {reserva['lugares']} | "
              f"Total (€): {reserva['total']} | Data: {reserva['data_reserva']}")

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

# Função para visualizar concertos
def visualizar_concertos():
    # Carregar concertos do arquivo
    try:
        concertos.clear()  # Limpa a lista atual
        with open("concertos.txt", "r") as f:
            for linha in f:
                id, nome, local, data, hora, capacidade, preco_bilhete, bar_disponivel, lugares_ocupados = linha.strip().split(",")
                concertos.append({
                    "id": id,
                    "nome": nome,
                    "local": local,
                    "data": data,
                    "hora": hora,
                    "capacidade": int(capacidade),
                    "preco_bilhete": float(preco_bilhete),
                    "bar_disponivel": bar_disponivel == "True",
                    "lugares_ocupados": int(lugares_ocupados)
                })
    except FileNotFoundError:
        print("Nenhum concerto disponível.")
        return

    if not concertos:
        print("Nenhum concerto disponível.")
        return
    
    concerto_id = input("Digite o ID do concerto: ")
    if not concerto_id:
        return
    
    concerto = next((c for c in concertos if c["id"] == concerto_id), None)
    if not concerto:
        print("Concerto não encontrado!")
        return
    
    print("\n=== Detalhes do Concerto ===")
    print(f"Nome: {concerto['nome']}")
    print(f"Local: {concerto['local']}")
    print(f"Data: {concerto['data']} | Hora: {concerto['hora']}")
    print(f"Capacidade: {concerto['capacidade']} | Lugares Ocupados: {concerto['lugares_ocupados']}")
    print(f"Preço do Bilhete: €{concerto['preco_bilhete']}")
    print(f"Bar Disponível: {'Sim' if concerto['bar_disponivel'] else 'Não'}")
