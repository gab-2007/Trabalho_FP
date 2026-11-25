ARQUIVO_ADOCOES = "adocoes.txt"
ARQUIVO_ANIMAIS = "animais.txt"

def ler_adocoes():
    try:
        with open(ARQUIVO_ADOCOES, "r", encoding="utf-8") as arquivo:
            linhas = arquivo. read().splitlines()
        return linhas
    except FileNotFoundError:
        return[]

def salvar_adocoes(linhas):
    with open(ARQUIVO_ADOCOES, "w", encoding="utf-8") as arquivo:
        arquivo.writelines(linha + "\n" for linha in linhas)
def ler_animais():
    try:
        with open(ARQUIVO_ANIMAIS, "r", encoding="utf-8") as arquivo:
            linhas = arquivo.read().splitlines()
        return linhas
    except FileNotFoundError:
        return []
def registrar_adocao():
    animais = ler_animais()
    if len(animais) == 0:
        print("Nenhum animal cadastrado. Cadastre um animal primeiro.")
        return
    print("Animais cadastrados:")
    numero = 1
    for linha in animais:
        partes = linha.split(";")
        print(numero, "-", partes[0], "|", partes[1], "|", partes[2])
        numero = numero + 1
    try:
        escolha = int(input("Número do animal que será adotado: "))
    except ValueError:
        print("Digite apenas números!")
        return

    if escolha < 1 or escolha > len(animais):
        print("Esse número não existe!")
        return
    nome_animal = animais[escolha - 1].split(";")[0]

    adocoes = ler_adocoes()
    for linha in adocoes:
        partes = linha.split(";")
        if partes[0].lower() == nome_animal.lower():
            print("Esse animal já foi adotado!")
            return
    adotante = input("Nome do adotante: ").strip()
    data = input("Data da adoção (dd/mm/aaaa): ").strip()

    if adotante == "" or data == "":
        print("Erro: todos os campos são obrigatórios!")
        return

    linha = nome_animal + ";" + adotante + ";" + data
    adocoes.append(linha)
    salvar_adocoes(adocoes)
    print("Adoção registrada!")


def listar_adocoes():
    adocoes = ler_adocoes()
    if len(adocoes) == 0:
        print("Nenhuma adoção registrada.")
        return

    numero = 1
    for linha in adocoes:
        partes = linha.split(";")
        print(numero, "- Animal:", partes[0], "| Adotante:", partes[1], "| Data:", partes[2])
        numero = numero + 1


def ver_historico():
    adocoes = ler_adocoes()
    if len(adocoes) == 0:
        print("Nenhuma adoção registrada.")
        return

    # Mostra todas as adoções de um adotante
    nome = input("Nome do adotante: ").strip()

    encontrou = False
    for linha in adocoes:
        partes = linha.split(";")
        # .lower() ignora maiúscula/minúscula
        if partes[1].lower() == nome.lower():
            print("- Adotou", partes[0], "em", partes[2])
            encontrou = True

    if encontrou == False:
        print("Esse adotante não tem adoções registradas.")


def menu_adocoes():
    opcao = ""
    while opcao != "0":
        print("""
        [1] Registrar adoção
        [2] Listar adoções
        [3] Ver histórico
        [0] Voltar
        """)
        opcao = input("Digite uma opção: ")

        if opcao == "1":
            registrar_adocao()
        elif opcao == "2":
            listar_adocoes()
        elif opcao == "3":
            ver_historico()
        elif opcao == "0":
            print("Voltando...")
        else:
            print("Opção inválida")


if __name__ == "__main__":
    menu_adocoes()
