from datetime import datetime

ARQUIVO_ADOCOES = "adocoes.txt"
ARQUIVO_ANIMAIS = "animais.txt"


def ler_animais():
    try:
        with open(ARQUIVO_ANIMAIS, "r", encoding="utf-8") as arquivo:
            linhas = arquivo.readlines()
    except FileNotFoundError:
        try:
            with open("animais/animais.txt", "r", encoding="utf-8") as arquivo:
                linhas = arquivo.readlines()
        except FileNotFoundError:
            return []

    animais = []

    for linha in linhas:
        campos = linha.strip().split(";")
        if len(campos) >= 7:
            animais.append(linha.strip())

    return animais


def ler_adocoes():
    try:
        with open(ARQUIVO_ADOCOES, "r", encoding="utf-8") as arquivo:
            linhas = arquivo.readlines()
    except FileNotFoundError:
        return []

    adocoes = []

    for linha in linhas:
        campos = linha.strip().split(";")
        if len(campos) >= 3:
            adocoes.append(";".join(campos[:3]))

    return adocoes


def salvar_adocoes(adocoes):
    with open(ARQUIVO_ADOCOES, "w", encoding="utf-8") as arquivo:
        for adocao in adocoes:
            arquivo.write(adocao + "\n")


def registrar_adocao():
    animais = ler_animais()

    if len(animais) == 0:
        print("Nenhum animal cadastrado. Cadastre um animal primeiro.")
        return

    print("\n--- ANIMAIS CADASTRADOS ---")

    numero = 1
    for linha in animais:
        campos = linha.split(";")
        print(numero, "-", campos[0], "|", campos[1], "|", campos[2])
        numero = numero + 1

    try:
        escolha = int(input("Número do animal que será adotado: "))
    except ValueError:
        print("Digite apenas números.")
        return

    if escolha < 1 or escolha > len(animais):
        print("Esse número não existe.")
        return

    campos_animal = animais[escolha - 1].split(";")
    nome_animal = campos_animal[0]
    adocoes = ler_adocoes()

    for linha in adocoes:
        campos_adocao = linha.split(";")
        if campos_adocao[0].lower() == nome_animal.lower():
            print("Esse animal já foi adotado.")
            return

    adotante = input("Nome do adotante: ").strip()

    if adotante == "":
        print("O nome do adotante é obrigatório.")
        return

    while True:
        data = input("Data da adoção (dd/mm/aaaa): ").strip()

        try:
            datetime.strptime(data, "%d/%m/%Y")
            break
        except ValueError:
            print("Data inválida. Use o formato dd/mm/aaaa.")

    adocao = nome_animal + ";" + adotante + ";" + data
    adocoes.append(adocao)
    salvar_adocoes(adocoes)
    print("Adoção registrada.")


def listar_adocoes():
    adocoes = ler_adocoes()

    if len(adocoes) == 0:
        print("Nenhuma adoção registrada.")
        return

    print("\n--- ADOÇÕES REGISTRADAS ---")

    numero = 1
    for linha in adocoes:
        campos = linha.split(";")
        print(
            numero,
            "- Animal:", campos[0],
            "| Adotante:", campos[1],
            "| Data:", campos[2]
        )
        numero = numero + 1


def ver_historico():
    adocoes = ler_adocoes()

    if len(adocoes) == 0:
        print("Nenhuma adoção registrada.")
        return

    nome = input("Nome do adotante: ").strip()

    if nome == "":
        print("Digite o nome do adotante.")
        return

    encontrou = False

    for linha in adocoes:
        campos = linha.split(";")
        if campos[1].lower() == nome.lower():
            print("- Adotou", campos[0], "em", campos[2])
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
            print("Opção inválida.")


if __name__ == "__main__":
    menu_adocoes()
