from persistencia import carregar_artistas, carregar_concertos, carregar_reservas
from artista import adicionar_artista, listar_artistas, atualizar_artista, eliminar_artista
from concertos import criar_concerto, listar_concertos  # Importando a função de visualizar concertos
from reservas import reservar_lugar, listar_reservas  # Certifique-se de que listar_reservas está importado
from uteis import calcular_idade
import webbrowser  # Nova importação para abrir o navegador

def main():
    artistas = carregar_artistas("artistas.txt")  # Carregar artistas do arquivo
    concertos = carregar_concertos("concertos.txt")  # Carregar concertos do arquivo
    reservas = carregar_reservas("reservas.txt")  # Carregar reservas do arquivo
    id_counter = len(artistas) + 1  # Inicializa o contador de IDs

    while True:
        print("\n=== Sistema de Gestão ===")
        print("1. Adicionar Artista")
        print("2. Listar Artistas")
        print("3. Atualizar Artista")
        print("4. Eliminar Artista")
        print("5. Criar Concerto")
        print("6. Visualizar Concertos") 
        print("7. Reservar Lugar")
        print("8. Listar Reservas")
        print("9. Sair do Sistema")  # Nova opção 10 para sair do sistema
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            adicionar_artista(artistas, id_counter)  # Passa o id_counter
            id_counter += 1  # Incrementa o contador de IDs
        elif opcao == "2":
            listar_artistas(artistas)
        elif opcao == "3":
            atualizar_artista(artistas)
        elif opcao == "4":
            eliminar_artista(artistas)
        elif opcao == "5":
            criar_concerto(artistas)  # Modificado: passando a lista de artistas como parâmetro
        elif opcao == "6":
            listar_concertos()  # Chama a função para visualizar concertos
        elif opcao == "7":
            reservar_lugar(reservas, concertos)  # Corrigido: passando os argumentos necessários
        elif opcao == "8":
            listar_reservas(reservas, concertos)  # Passa reservas e concertos
        elif opcao == "9":
            print("Saindo do sistema. Até mais!")  # Mensagem de saída
            break  # Sai do loop

if __name__ == "__main__":
    main()
