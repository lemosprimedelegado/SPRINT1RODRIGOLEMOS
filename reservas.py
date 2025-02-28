import uuid
from datetime import datetime

class Reserva:
    def __init__(self, nome_cliente, concerto, quantidade):
        self.nome_cliente = nome_cliente
        self.concerto = concerto
        self.quantidade = quantidade
        self.id = None  # Inicializa o ID como None

def listar_reservas(reservas, concertos):
    print("\n=== Lista de Reservas ===")
    if not reservas:
        print("Nenhuma reserva encontrada.")
        return
    for reserva in reservas:
        concerto = next((c for c in concertos if c.id == reserva.concerto), None)  # Ajuste para acessar o ID do concerto
        if concerto:
            print(f"Reserva ID: {reserva.id} | Concerto: {concerto.artista} | Lugares: {reserva.quantidade} | "
                  f"Total (€): {reserva.quantidade * 10} | Data: {reserva.data_reserva}")  # Exemplo de cálculo de total
        else:
            print(f"Reserva ID: {reserva.id} | Concerto não encontrado | Lugares: {reserva.quantidade}")

def reservar_lugar(reservas, concertos):
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
    print(f"Reserva efetuada com sucesso! Código da reserva: {reserva['id']}")

    # Gravar reserva no arquivo
    with open("reservas.txt", "a") as f:
        f.write(f"{reserva['id']},{concerto_id},{lugares},{total},{reserva['data_reserva']}\n")
