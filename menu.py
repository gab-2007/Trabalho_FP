from animais.Animais import menu_animais
from registros_cuidados.registrocuidados import menu_registro


def mostrar_menu():
    print('''
    [1]Gerenciar Animais
    [2]Cuidados e Atividades
    [3]Ver Alertas
    [4]Sugestões Personalizadas
    [5] Adocões
    [0]Sair
    ''')
def main():
    opcao = ""
    while opcao != "0":
        mostrar_menu()
        opcao = input("Digite uma opção: ")

        if opcao == "1":
            menu_animais()
        elif opcao == "2":
            menu_registro()
        elif opcao == "0":
            print("Saindo..")
        else:
            print("Opção inválida")
main()
