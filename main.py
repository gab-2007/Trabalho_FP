from animais import menu_animais
from cuidados import menu_registro
from alertas import menu_alertas
from sugestoes import menu_sugestoes
from adocoes import menu_adocoes
from agendamentos import menu_agendamentos


def mostrar_menu():
    print("""
    SISTEMA DE ADOÇÃO DE ANIMAIS

    [1] Gerenciar animais
    [2] Cuidados e atividades
    [3] Ver alertas
    [4] Sugestões personalizadas
    [5] Adoções
    [6] Agendar visitas
    [0] Sair
    """)


def main():
    opcao = ""

    while opcao != "0":
        mostrar_menu()
        opcao = input("Digite uma opção: ").strip()

        if opcao == "1":
            menu_animais()
        elif opcao == "2":
            menu_registro()
        elif opcao == "3":
            menu_alertas()
        elif opcao == "4":
            menu_sugestoes()
        elif opcao == "5":
            menu_adocoes()
        elif opcao == "6":
            menu_agendamentos()
        elif opcao == "0":
            print("Saindo...")
        else:
            print("Opção inválida.")


main()
