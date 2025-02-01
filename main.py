from artista import Artista
from persistencia_artista import gravar_artista, carregar_artistas
import random
from datetime import datetime

FICHEIRO_ARTISTAS = "artistas.txt"
FICHEIRO_ = "eventos.txt"

def calcular_idade(data_nascimento):
    hoje = datetime.now()
    dia, mes, ano = map(int, data_nascimento.split('/'))
    idade = hoje.year - ano
    # Reduz 1 ano se ainda não chegou ao aniversário este ano
    if (hoje.month, hoje.day) < (mes, dia):
        idade -= 1
    return idade

def main(): 
    artistas = []
    id_counter = 1
    while True:
        print("1. Adicionar Artista")
        print("2. Listar Artistas")
        print("3. Gravar Artistas")
        print("4. Pesquisar Artista")
        print("5. Sair")
        opção = input("Escolha uma opção: ")
        if opção == "1":
            nome = input("Nome do artista: ")
            genero = input("Gênero musical: ")
            
            while True:
                data = input("Data de nascimento: ")
                # Adiciona as barras automaticamente se o usuário não colocar
                if len(data) == 8 and data.isdigit():
                    data = f"{data[:2]}/{data[2:4]}/{data[4:]}"
                try:
                    dia, mes, ano = data.split('/')
                    dia = int(dia)
                    mes = int(mes)
                    ano = int(ano)
                    
                    # Validações básicas com tratamento de ano com 2 dígitos
                    if len(str(ano)) == 2:
                        # Se ano for menor que 25, assume-se 2000+
                        # Se for maior, assume-se 1900+
                        ano = 2000 + ano if ano < 25 else 1900 + ano
                    
                    # Validação de ano mínimo
                    if ano < 1900:
                        print("Data inválida! O ano não pode ser anterior a 1900.")
                        continue
                    
                    # Validação de data futura
                    data_atual = datetime.now()
                    if ano > data_atual.year or \
                       (ano == data_atual.year and mes > data_atual.month) or \
                       (ano == data_atual.year and mes == data_atual.month and dia > data_atual.day):
                        print("Data inválida! Não é possível usar uma data futura.")
                        continue
                    
                    if mes < 1 or mes > 12 or dia < 1 or dia > 31:
                        print("Data inválida!")
                        continue
                        
                    break
                except:
                    print("Data inválida!")
            
            contacto = input("Contacto: ")
            discografia = input("Discografia: ")
            
            # Garantindo que a data está no formato correto antes de criar o objeto
            data_formatada = f"{dia:02d}/{mes:02d}/{ano}"
            
            artista = Artista(nome, genero, data_formatada, contacto, discografia)
            artista.id = id_counter
            id_counter += 1
            artistas.append(artista)
            print(f"Artista adicionado com sucesso! ID: {artista.id}")
            
        elif opção == "2":
            if not artistas:
                print("Não há artistas cadastrados!")
                continue
            for artista in artistas:
                print(f"\nID: {artista.id}")
                print(f"Nome: {artista.nome}")
                print(f"Gênero: {artista.gênero}")
                print(f"Data de Nascimento: {artista.data_nascimento}")
                idade = calcular_idade(artista.data_nascimento)
                print(f"Idade: {idade} anos")
                print(f"Contacto: {artista.contacto}")
                print(f"Discografia: {artista.discografia}")
                print("-" * 30)
                
        elif opção == "3":
            for artista in artistas:
                gravar_artista(FICHEIRO_ARTISTAS, artista)
            print("Artistas gravados com sucesso!")
            
        elif opção == "4":
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
                            print(f"Gênero: {artista.gênero}")
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
                        print(f"Gênero: {artista.gênero}")
                        print(f"Data de Nascimento: {artista.data_nascimento}")
                        idade = calcular_idade(artista.data_nascimento)
                        print(f"Idade: {idade} anos")
                        print(f"Contacto: {artista.contacto}")
                        print(f"Discografia: {artista.discografia}")
                else:
                    print("Nenhum artista encontrado!")
            
            else:
                print("Opção inválida!")
                
        elif opção == "5":
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    main()
