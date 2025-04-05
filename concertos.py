import uuid
from datetime import datetime

FICHEIRO_CONCERTOS = "concertos.txt"

class Concerto:
    def __init__(self, id, artista, data, local, lugares_disponiveis, preco, bar_disponivel=False):
        self.id = id
        self.artista = artista
        self.data = data
        self.local = local
        self.lugares_disponiveis = lugares_disponiveis
        self.preco = preco
        self.bar_disponivel = bar_disponivel
        self.lugares_ocupados = 0

    def __str__(self):
        return f"{self.artista} - {self.local} - {self.data}"

def criar_concerto(concertos):
    print("\n=== Criar Concerto ===")
    
    nome = input("Nome do artista: ").strip()
    if not nome:
        print("O nome do artista não pode estar vazio!")
        return concertos
    
    local = input("Local do concerto: ").strip()
    if not local:
        print("O local não pode estar vazio!")
        return concertos

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
    lugares_disponiveis = int(input("Capacidade do estabelecimento: "))
    preco = float(input("Preço do bilhete (€): "))

    novo_concerto = Concerto(
        str(uuid.uuid4()),
        nome,
        data,
        local,
        lugares_disponiveis,
        preco
    )
    
    concertos.append(novo_concerto)
    
    try:
        with open(FICHEIRO_CONCERTOS, "a") as f:
            f.write(f"{novo_concerto.id},{novo_concerto.artista},{novo_concerto.data},"
                   f"{novo_concerto.local},{novo_concerto.lugares_disponiveis},{novo_concerto.preco}\n")
        print(f"Concerto de '{nome}' criado com sucesso! ID: {novo_concerto.id}")
    except Exception as e:
        print(f"Erro ao gravar o concerto no arquivo: {e}")
        return concertos

    return concertos

def eliminar_concerto(concertos):
    if not concertos:
        print("Não há concertos disponíveis para excluir.")
        return concertos

    print("\n=== Eliminar Concerto ===")
    for i, concerto in enumerate(concertos):
        print(f"{i + 1}. {concerto}")

    try:
        escolha = int(input("Escolha o número do concerto para excluir: "))
        if 1 <= escolha <= len(concertos):
            concerto_removido = concertos.pop(escolha - 1)
            print(f"Concerto '{concerto_removido}' removido com sucesso!")
        else:
            print("Escolha inválida!")
    except ValueError:
        print("Entrada inválida!")

    return concertos

def listar_concertos(concertos):
    if not concertos:
        print("Nenhum concerto cadastrado.")
        return concertos

    print("\n=== Lista de Concertos ===")
    for concerto in concertos:
        print(f"ID: {concerto.id} | Artista: {concerto.artista} | Local: {concerto.local} | "
              f"Data: {concerto.data} | Lugares disponíveis: {concerto.lugares_disponiveis} | "
              f"Preço: €{concerto.preco}")

    return concertos

def editar_concerto(concertos):
    if not concertos:
        print("Não há concertos disponíveis para editar.")
        return concertos

    print("\n=== Editar Concerto ===")
    for i, concerto in enumerate(concertos):
        print(f"{i + 1}. {concerto}")

    try:
        escolha = int(input("Escolha o número do concerto para editar: "))
        if 1 <= escolha <= len(concertos):
            concerto_selecionado = concertos[escolha - 1]
            print(f"Editando concerto: {concerto_selecionado}")

            novo_nome = input("Novo nome do artista (deixe vazio para manter): ").strip()
            novo_local = input("Novo local (deixe vazio para manter): ").strip()
            nova_data = input("Nova data (formato dd/mm/aaaa, deixe vazio para manter): ").strip()
            nova_capacidade = input("Nova capacidade (deixe vazio para manter): ").strip()
            novo_preco = input("Novo preço (deixe vazio para manter): ").strip()

            if novo_nome:
                concerto_selecionado.artista = novo_nome
            if novo_local:
                concerto_selecionado.local = novo_local
            if nova_data:
                try:
                    data_obj = datetime.strptime(nova_data, "%d/%m/%Y")
                    concerto_selecionado.data = data_obj.strftime("%d/%m/%Y")
                except ValueError:
                    print("Data inválida! Mantendo a data original.")
            if nova_capacidade:
                try:
                    concerto_selecionado.lugares_disponiveis = int(nova_capacidade)
                except ValueError:
                    print("Capacidade inválida! Mantendo a capacidade original.")
            if novo_preco:
                try:
                    concerto_selecionado.preco = float(novo_preco)
                except ValueError:
                    print("Preço inválido! Mantendo o preço original.")

            print(f"Concerto atualizado: {concerto_selecionado}")
        else:
            print("Escolha inválida!")
    except ValueError:
        print("Entrada inválida!")

    return concertos
