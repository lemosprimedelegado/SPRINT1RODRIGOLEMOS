from datetime import datetime

class Artista:
    def __init__(self, nome, genero, data_nascimento, contacto, discografia):
        self.nome = nome
        self.genero = genero
        self.data_nascimento = data_nascimento
        self.contacto = contacto
        self.discografia = discografia
        self.id = None  # Inicializa o ID como None

    def atualizar(self, novos_dados):
        self.genero = novos_dados.get('genero', self.genero)
        self.data_nascimento = novos_dados.get('data_nascimento', self.data_nascimento)
        self.contacto = novos_dados.get('contacto', self.contacto)
        self.discografia = novos_dados.get('discografia', self.discografia)
        print(f"Artista {self.nome} atualizado com sucesso.")

def calcular_idade(data_nascimento):
    dia, mes, ano = map(int, data_nascimento.split('/'))
    nascimento = datetime(ano, mes, dia)
    idade = (datetime.now() - nascimento).days // 365
    return idade

def listar_artistas(artistas):
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

def adicionar_artista(artistas, id_counter):
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
        except ValueError:
            print("Formato de data inválido! Tente novamente.")

    contacto = input("Contacto: ")
    discografia = input("Discografia: ")
    data_formatada = f"{dia:02d}/{mes:02d}/{ano}"
    artista = Artista(nome, genero, data_formatada, contacto, discografia)
    artista.id = id_counter  # Atribui o ID ao artista
    artistas.append(artista)
    print(f"Artista {nome} adicionado com sucesso! ID: {artista.id}")

    # Gravar artista no arquivo automaticamente
    with open("artistas.txt", "a") as f:
        f.write(f"{artista.id},{artista.nome},{artista.genero},{artista.data_nascimento},{artista.contacto},{artista.discografia}\n")

def eliminar_artista(artistas):
    if not artistas:
        print("Não há artistas cadastrados!")
        return

    try:
        id_busca = int(input("Digite o ID do artista a ser eliminado: "))
        artista_encontrado = None

        for artista in artistas:
            if artista.id == id_busca:
                artista_encontrado = artista
                break

        if artista_encontrado:
            artistas.remove(artista_encontrado)
            print(f"Artista {artista_encontrado.nome} eliminado com sucesso!")

            # Atualizar o arquivo com as informações restantes
            with open("artistas.txt", "w") as f:
                for a in artistas:
                    f.write(f"{a.id},{a.nome},{a.genero},{a.data_nascimento},{a.contacto},{a.discografia}\n")
        else:
            print("Artista não encontrado!")
    except ValueError:
        print("ID inválido!")

def atualizar_artista(artistas):
    if not artistas:
        print("Não há artistas cadastrados!")
        return
    
    for i, artista in enumerate(artistas, 1):
        print(f"{i}. {artista.nome}")
    
    try:
        indice = int(input("Escolha o número do artista para atualizar: ")) - 1
        if indice < 0 or indice >= len(artistas):
            print("Número inválido!")
            return
        
        artista = artistas[indice]
        
        novos_dados = {}
        while True:
            print("\nQual informação deseja atualizar?")
            print("1. Gênero")
            print("2. Contacto")
            print("3. Discografia")
            print("4. Voltar ao menu principal")
            
            escolha = input("Escolha uma opção: ")
            
            if escolha == "1":
                novo_genero = input(f"Gênero atual: {artista.genero}\nNovo gênero: ").strip()
                if novo_genero:
                    novos_dados['genero'] = novo_genero
                    
            elif escolha == "2":
                novo_contacto = input(f"Contacto atual: {artista.contacto}\nNovo contacto: ").strip()
                if novo_contacto:
                    novos_dados['contacto'] = novo_contacto
                    
            elif escolha == "3":
                nova_discografia = input(f"Discografia atual: {artista.discografia}\nNova discografia: ").strip()
                if nova_discografia:
                    novos_dados['discografia'] = nova_discografia
                    
            elif escolha == "4":  # Voltar ao menu principal
                break
                
            else:
                print("Opção inválida!")
        
        artista.atualizar(novos_dados)

        # Atualizar o arquivo com as informações atualizadas
        with open("artistas.txt", "w") as f:
            for a in artistas:
                f.write(f"{a.id},{a.nome},{a.genero},{a.data_nascimento},{a.contacto},{a.discografia}\n")
    
    except ValueError:
        print("Entrada inválida!")

# Outras funções...
