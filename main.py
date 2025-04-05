from persistencia import carregar_artistas, carregar_concertos, carregar_reservas
from artista import adicionar_artista, listar_artistas, atualizar_artista, eliminar_artista
from concertos import criar_concerto, listar_concertos, eliminar_concerto, editar_concerto  # Importando funções adicionais
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
        print("9. Eliminar Concerto")
        print("10. Editar Concerto")
        print("11. Sair do sistema")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            adicionar_artista(artistas, id_counter)
        elif opcao == "2":
            listar_artistas(artistas)
        elif opcao == "3":
            artistas = atualizar_artista(artistas)
        elif opcao == "4":
            artistas = eliminar_artista(artistas)
        elif opcao == "5":
            concertos = criar_concerto(concertos)
        elif opcao == "6":
            concertos = listar_concertos(concertos)
        elif opcao == "7":
            reservas, concertos = reservar_lugar(reservas, concertos)
        elif opcao == "8":
            reservas, concertos = listar_reservas(reservas, concertos)
        elif opcao == "9":
            concertos = eliminar_concerto(concertos)
        elif opcao == "10":
            concertos = editar_concerto(concertos)
        elif opcao == "11":
            print("Saindo do sistema. Até mais!")
            break
        else:
            print("Opção inválida! Tente novamente.")

if __name__ == "__main__":
    main()
