from datetime import datetime
import uuid

# Classe Artista
class Artista:
    def __init__(self, nome, genero, data_nascimento, contacto, discografia):
        self.id = str(uuid.uuid4())
        self.nome = nome
        self.genero = genero
        self.data_nascimento = data_nascimento
        self.contacto = contacto
        self.discografia = discografia

    def __str__(self):
        return f"{self.nome};{self.genero};{self.data_nascimento};{self.contacto};{self.discografia}"

    @classmethod
    def from_string(cls, data_str):
        try:
            nome, genero, data_nascimento, contacto, discografia = data_str.strip().split(';')
            return cls(nome, genero, data_nascimento, contacto, discografia)
        except ValueError:
            print(f"Erro ao ler linha: '{data_str}'. Formato esperado: 'nome;gênero;data_nascimento;contacto;discografia'")
            return None

# Banco de dados em memória
concertos = []
reservas = []

# Funções de persistência
def adicionar_concerto(concerto):
    concertos.append(concerto)

def obter_concertos():
    return concertos

def obter_concerto_por_id(concerto_id):
    for concerto in concertos:
        if concerto["id"] == concerto_id:
            return concerto
    return None

def adicionar_reserva(reserva):
    reservas.append(reserva)

def obter_reservas():
    return reservas

def atualizar_lugares_ocupados(concerto_id, lugares):
    concerto = obter_concerto_por_id(concerto_id)
    if concerto:
        concerto["lugares_ocupados"] += lugares

# Função para criar um concerto
def criar_concerto():
    print("\n=== Criar Concerto ===")
    nome = input("Nome do artista: ")
    local = input("Local do concerto: ")

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
    capacidade = int(input("Capacidade do estabelecimento: "))
    preco_bilhete = float(input("Preço do bilhete (€): "))
    bar_disponivel = input("Bar disponível (s/n): ").lower() == "s"

    artista = Artista(nome, "Gênero Desconhecido", "01/01/2000", "Contato Desconhecido", "Discografia Desconhecida")
    
    concerto = {
        "id": str(uuid.uuid4()),
        "artista": artista,
        "local": local,
        "data": data,
        "hora": hora,
        "capacidade": capacidade,
        "preco_bilhete": preco_bilhete,
        "bar_disponivel": bar_disponivel,
        "lugares_ocupados": 0,
    }
    adicionar_concerto(concerto)
    print(f"Concerto '{artista.nome}' criado com sucesso!")

# Função para listar concertos
def listar_concertos():
    print("\n=== Lista de Concertos ===")
    concertos = obter_concertos()
    if not concertos:
        print("Nenhum concerto disponível.")
        return
    for concerto in concertos:
        print(f"ID: {concerto['id']} | Artista: {concerto['artista'].nome} | Local: {concerto['local']} | "
              f"Data: {concerto['data']} | Hora: {concerto['hora']} | Capacidade: {concerto['capacidade']} | "
              f"Lugares Ocupados: {concerto['lugares_ocupados']}")

# Função para reservar lugares
def reservar_lugar():
    print("\n=== Reservar Lugar ===")
    listar_concertos()
    concerto_id = input("Insira o ID do concerto para reservar: ")
    concerto = obter_concerto_por_id(concerto_id)
    if not concerto:
        print("Concerto não encontrado!")
        return

    lugares = int(input("Quantos lugares deseja reservar? "))
    if concerto["lugares_ocupados"] + lugares > concerto["capacidade"]:
        print("Lugares insuficientes disponíveis!")
        return

    total = lugares * concerto["preco_bilhete"]
    reserva = {
        "id": str(uuid.uuid4()),
        "concerto_id": concerto_id,
        "lugares": lugares,
        "total": total,
        "data_reserva": datetime.now().strftime("%d/%m/%Y %H:%M"),
    }
    adicionar_reserva(reserva)
    atualizar_lugares_ocupados(concerto_id, lugares)
    print(f"Reserva efetuada com sucesso! Código da reserva: {reserva['id']}")

# Função para listar reservas
def listar_reservas():
    print("\n=== Lista de Reservas ===")
    reservas = obter_reservas()
    if not reservas:
        print("Nenhuma reserva encontrada.")
        return
    for reserva in reservas:
        concerto = obter_concerto_por_id(reserva["concerto_id"])
        print(f"Reserva ID: {reserva['id']} | Concerto: {concerto['artista'].nome} | Lugares: {reserva['lugares']} | "
              f"Total (€): {reserva['total']} | Data: {reserva['data_reserva']}")
