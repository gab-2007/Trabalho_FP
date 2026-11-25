ARQUIVO_ANIMAIS = "animais.txt"
ARQUIVO = ARQUIVO_ANIMAIS

def ler_linhas_animais():
    try:
        with open(ARQUIVO, "r", encoding="utf-8") as arquivo:
            linhas = arquivo.read().splitlines()
        return linhas
    except FileNotFoundError:
        try:
            with open("animais/animais.txt", "r", encoding="utf-8") as arquivo:
                linhas = arquivo.read().splitlines()
            return linhas
        except FileNotFoundError:
            return []


def salvar_linhas_animais(linhas):
    with open(ARQUIVO, "w", encoding="utf-8") as arquivo:
        arquivo.writelines(linha + "\n" for linha in linhas)


def cadastrar_animal():
    nome = input("Nome: ")
    especie = input("Espécie (Cachorro/Gato/Outro): ")
    raca = input("Raça: ")
    idade = input("Idade: ")
    saude = input("Estado de saúde: ")
    chegada = input("Data de chegada (dd/mm/aaaa): ")
    comportamento = input("Comportamento: ")

    linha = nome + ";" + especie + ";" + raca + ";" + idade + ";" + saude + ";" + chegada + ";" + comportamento

    linhas = ler_linhas_animais()
    linhas.append(linha)
    salvar_linhas_animais(linhas)
    print("Animal cadastrado!")


def listar_animais():
    linhas = ler_linhas_animais()
    if len(linhas) == 0:
        print("Nenhum animal cadastrado.")
        return

    numero = 1
    for linha in linhas:
        partes = linha.split(";")
        print(numero, "-", partes[0], "|", partes[1], "|", partes[2], "|", partes[3], "anos |", partes[4], "|", partes[5], "|", partes[6])
        numero = numero + 1


def editar_animal():
    linhas = ler_linhas_animais()
    if len(linhas) == 0:
        print("Nenhum animal cadastrado.")
        return

    listar_animais()

    try:
        numero = int(input("Número do animal que quer editar: "))
    except ValueError:
        print("Digite apenas números!")
        return

    if numero < 1 or numero > len(linhas):
        print("Esse número não existe!")
        return

    print("Digite os novos dados:")
    nome = input("Nome: ")
    especie = input("Espécie (Cachorro/Gato/Outro): ")
    raca = input("Raça: ")
    idade = input("Idade: ")
    saude = input("Estado de saúde: ")
    chegada = input("Data de chegada (dd/mm/aaaa): ")
    comportamento = input("Comportamento: ")

    linha = nome + ";" + especie + ";" + raca + ";" + idade + ";" + saude + ";" + chegada + ";" + comportamento

    linhas[numero - 1] = linha
    salvar_linhas_animais(linhas)
    print("Animal editado!")


def excluir_animal():
    linhas = ler_linhas_animais()
    if len(linhas) == 0:
        print("Nenhum animal cadastrado.")
        return

    listar_animais()

    try:
        numero = int(input("Número do animal que quer excluir: "))
    except ValueError:
        print("Digite apenas números!")
        return

    if numero < 1 or numero > len(linhas):
        print("Esse número não existe!")
        return

    linhas.pop(numero - 1)
    salvar_linhas_animais(linhas)
    print("Animal excluído!")


def menu_animais():
    opcao = ""
    while opcao != "0":
        print("""
        [1] Cadastrar Animal
        [2] Listar Animais
        [3] Editar Animal
        [4] Excluir Animal
        [0] Voltar
        """)
        opcao = input("Digite uma opção: ")

        if opcao == "1":
            cadastrar_animal()
        elif opcao == "2":
            listar_animais()
        elif opcao == "3":
            editar_animal()
        elif opcao == "4":
            excluir_animal()
        elif opcao == "0":
            print("Voltando...")
        else:
            print("Opção inválida")
