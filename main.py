import uuid
from datetime import datetime
from artista import Artista
from persistencia import gravar_artista, carregar_artistas
from artista import criar_concerto, listar_concertos, reservar_lugar, listar_reservas

# Lista para armazenar os concertos e reservas
concertos = []
reservas = []

FICHEIRO_ARTISTAS = "artistas.txt"
FICHEIRO_EVENTOS  = "eventos.txt"
FICHEIRO_CONCERTOS = "concertos.txt"  # Adicionando o arquivo para concertos

# Função para calcular a idade do artista
def calcular_idade(data_nascimento):
    hoje = datetime.now()
    dia, mes, ano = map(int, data_nascimento.split('/'))
    idade = hoje.year - ano
    if (hoje.month, hoje.day) < (mes, dia):
        idade -= 1
    return idade

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
    capacidade = int(input("Capacidade do estabelecimento: "))
    preco_bilhete = float(input("Preço do bilhete (€): "))
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
    concertos.append(concerto)
    print(f"Concerto '{nome}' criado com sucesso!")

def listar_concertos():
    print("\n=== Lista de Concertos ===")
    if not concertos:
        print("Nenhum concerto disponível.")
        return
    for concerto in concertos:
        print(f"ID: {concerto['id']} | Nome: {concerto['nome']} | Local: {concerto['local']} | "
              f"Data: {concerto['data']} | Hora: {concerto['hora']} | Capacidade: {concerto['capacidade']} | "
              f"Lugares Ocupados: {concerto['lugares_ocupados']}")

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
    print(f"Reserva efetuada com sucesso! Código da reserva: {reserva['id']}")

def listar_reservas():
    print("\n=== Lista de Reservas ===")
    if not reservas:
        print("Nenhuma reserva encontrada.")
        return
    for reserva in reservas:
        concerto = next((c for c in concertos if c["id"] == reserva["concerto_id"]), None)
        print(f"Reserva ID: {reserva['id']} | Concerto: {concerto['nome']} | Lugares: {reserva['lugares']} | "
              f"Total (€): {reserva['total']} | Data: {reserva['data_reserva']}")

def gravar_concertos(arquivo):
    with open(arquivo, "w") as f:
        for concerto in concertos:
            f.write(
                f"{concerto['id']},{concerto['nome']},{concerto['local']},{concerto['data']},{concerto['hora']},{concerto['capacidade']},{concerto['preco_bilhete']},{concerto['bar_disponivel']},{concerto['lugares_ocupados']}\n")
    print("Concertos gravados no arquivo com sucesso!")

def carregar_concertos(arquivo):
    try:
        with open(arquivo, "r") as f:
            for linha in f:
                id, nome, local, data, hora, capacidade, preco_bilhete, bar_disponivel, lugares_ocupados = linha.strip().split(
                    ",")
                concertos.append(
                    {"id": id, "nome": nome, "local": local, "data": data, "hora": hora, "capacidade": int(capacidade),
                     "preco_bilhete": float(preco_bilhete), "bar_disponivel": bar_disponivel == "True",
                     "lugares_ocupados": int(lugares_ocupados)})
        print("Concertos carregados do arquivo com sucesso!")
    except FileNotFoundError:
        print("Arquivo não encontrado. Nenhum concerto carregado.")

def main():
    artistas = carregar_artistas(FICHEIRO_ARTISTAS)  # Carregar artistas do arquivo
    id_counter = len(artistas) + 1  # Definir o contador de ID com base no número de artistas carregados
    carregar_concertos(FICHEIRO_CONCERTOS)  # Carregar concertos do arquivo

    while True:
        print("\n=== Sistema de Gestão ===")
        print("1. Adicionar Artista")
        print("2. Listar Artistas")
        print("3. Gravar Artistas")
        print("4. Pesquisar Artista")
        print("5. Criar Concerto")
        print("6. Listar Concertos")
        print("7. Reservar Lugar")
        print("8. Listar Reservas")
        print("9. Gravar Concertos")
        print("10. Sair")
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            nome = input("Nome do artista: ")
            genero = input("Gênero musical: ")
            while True:
                data = input("Data de nascimento (DD/MM/AAAA): ")
                if len(data) == 8 and data.isdigit():
                    data = f"{data[:2]}/{data[2:4]}/{data[4:]}"
                try:
                    dia, mes, ano = map(int, data.split('/'))
                    if len(str(ano)) == 2:
                        ano = 2000 + ano if ano < 25 else 1900 + ano
                    if ano < 1900 or datetime(ano, mes, dia) > datetime.now():
                        print("Data inválida! Tente novamente.")
                        continue
                    break
                except:
                    print("Formato de data inválido! Tente novamente.")
            
            contacto = input("Contacto: ")
            discografia = input("Discografia: ")
            data_formatada = f"{dia:02d}/{mes:02d}/{ano}"
            artista = Artista(nome, genero, data_formatada, contacto, discografia)
            artista.id = id_counter
            id_counter += 1
            artistas.append(artista)

            # Mensagem de confirmação
            print(f"Artista adicionado com sucesso! ID: {artista.id}")
            
        elif opcao == "2":
            if not artistas:
                print("Não há artistas cadastrados!")
            for artista in artistas:
                print(f"\nID: {artista.id}\nNome: {artista.nome}\nGênero: {artista.genero}\nData de Nascimento: {artista.data_nascimento}\nIdade: {calcular_idade(artista.data_nascimento)} anos\nContacto: {artista.contacto}\nDiscografia: {artista.discografia}\n{'-' * 30}")
                
        elif opcao == "3":
            for artista in artistas:
                gravar_artista(FICHEIRO_ARTISTAS, artista)
            print("Artistas gravados com sucesso!")
            
        elif opcao == "4":
            if not artistas:
                print("Não há artistas cadastrados!")
                continue

            print("\nPesquisar por:")
            print("1. ID")
            print("2. Nome")
            escolha = input("Escolha uma opção: ")

            if escolha == "1":
                try:
                    id_busca = int(input("Digite o ID do artista: "))
                    encontrado = False
                    for artista in artistas:
                        if artista.id == id_busca:
                            print("\nInformações do Artista:")
                            print(f"ID: {artista.id}")
                            print(f"Nome: {artista.nome}")
                            print(f"Gênero: {artista.genero}")
                            print(f"Data de Nascimento: {artista.data_nascimento}")
                            idade = calcular_idade(artista.data_nascimento)
                            print(f"Idade: {idade} anos")
                            print(f"Contacto: {artista.contacto}")
                            print(f"Discografia: {artista.discografia}")
                            encontrado = True
                            break
                    if not encontrado:
                        print("Artista não encontrado!")
                except ValueError:
                    print("ID inválido!")

            elif escolha == "2":
                nome_busca = input("Digite o nome do artista: ").lower()
                encontrados = []
                for artista in artistas:
                    if nome_busca in artista.nome.lower():
                        encontrados.append(artista)

                if encontrados:
                    print("\nArtistas encontrados:")
                    for artista in encontrados:
                        print("\nInformações do Artista:")
                        print(f"ID: {artista.id}")
                        print(f"Nome: {artista.nome}")
                        print(f"Gênero: {artista.genero}")
                        print(f"Data de Nascimento: {artista.data_nascimento}")
                        idade = calcular_idade(artista.data_nascimento)
                        print(f"Idade: {idade} anos")
                        print(f"Contacto: {artista.contacto}")
                        print(f"Discografia: {artista.discografia}")
                else:
                    print("Nenhum artista encontrado!")

            else:
                print("Opção inválida!")
        
        elif opcao == "5":
            criar_concerto()
        elif opcao == "6":
            listar_concertos()
            # Adicionando a funcionalidade para listar e gravar concertos
            print("Concertos listados e gravados com sucesso!")
        elif opcao == "7":
            reservar_lugar()
        elif opcao == "8":
            listar_reservas()
        elif opcao == "9":
            gravar_concertos(FICHEIRO_CONCERTOS)
        elif opcao == "10":
            print("Saindo do sistema. Até mais!")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
