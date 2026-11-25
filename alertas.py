from datetime import date, datetime

ARQUIVO_ANIMAIS = "animais.txt"
ARQUIVO_CUIDADOS = "registro_cuidado.txt"
ARQUIVO_AGENDA = "agenda_alertas.txt"


def ler_animais():
    try:
        with open(ARQUIVO_ANIMAIS, "r", encoding="utf-8") as arquivo:
            linhas = arquivo.read().splitlines()
    except FileNotFoundError:
        try:
            with open("animais/animais.txt", "r", encoding="utf-8") as arquivo:
                linhas = arquivo.read().splitlines()
        except FileNotFoundError:
            return []

    animais = []
    for linha in linhas:
        campos = linha.split(";")
        if len(campos) >= 7:
            animais.append(campos)

    return animais


def ler_agenda():
    try:
        with open(ARQUIVO_AGENDA, "r", encoding="utf-8") as arquivo:
            linhas = arquivo.read().splitlines()
    except FileNotFoundError:
        return []

    registros = []
    for linha in linhas:
        campos = linha.split(";")
        if len(campos) == 9:
            registros.append(campos)

    return registros


def salvar_agenda(registros):
    with open(ARQUIVO_AGENDA, "w", encoding="utf-8") as arquivo:
        for registro in registros:
            arquivo.write(";".join(registro) + "\n")


def calcular_prazo(data):
    dias = (data - date.today()).days

    if dias < 0:
        return "atrasado há " + str(-dias) + " dia(s)"
    elif dias == 0:
        return "previsto para hoje"
    else:
        return "previsto em " + str(dias) + " dia(s)"


def mostrar_detalhes(alerta):
    print("\n--- DETALHES DO ALERTA ---")
    print("Cuidado:", alerta[0])
    print("Data prevista:", alerta[1].strftime("%d/%m/%Y"))
    print("Prazo:", alerta[2])

    if alerta[3] == "Não informado no registro antigo":
        print("Animal: não informado no registro antigo.")
        print("Registro:", alerta[4])
    else:
        animal = alerta[4]
        print("Animal:", animal[3])
        print("Espécie:", animal[4])
        print("Raça:", animal[5])
        print("Idade:", animal[6])
        print("Saúde:", animal[7])
        print("Comportamento:", animal[8])


def mostrar_alertas():
    alertas = []

    try:
        with open(ARQUIVO_CUIDADOS, "r", encoding="utf-8") as arquivo:
            cuidados = arquivo.read().splitlines()
    except FileNotFoundError:
        cuidados = []

    for linha in cuidados:
        campos = linha.split(" | ")

        if len(campos) >= 3 and campos[1] == "Vacina":
            texto_data = campos[2].replace("Data da vacina: ", "").strip()

            try:
                data = datetime.strptime(texto_data, "%d/%m/%Y").date()
            except ValueError:
                continue

            alerta = [
                "Vacina",
                data,
                calcular_prazo(data),
                "Não informado no registro antigo",
                campos[0],
            ]
            alertas.append(alerta)

    registros = ler_agenda()

    for registro in registros:
        if registro[2] == "Pendente":
            try:
                data = datetime.strptime(registro[1], "%d/%m/%Y").date()
            except ValueError:
                continue

            alerta = [
                registro[0],
                data,
                calcular_prazo(data),
                registro[3],
                registro,
            ]
            alertas.append(alerta)

    if len(alertas) == 0:
        print("Nenhum alerta com data prevista foi encontrado.")
        return

    print("\n--- ALERTAS ---")
    numero = 1

    for alerta in alertas:
        print(
            "[" + str(numero) + "] " + alerta[0]
            + " | " + alerta[3]
            + " | " + alerta[1].strftime("%d/%m/%Y")
            + " | " + alerta[2]
        )
        numero = numero + 1

    while True:
        opcao = input("[1] Ver detalhes  [0] Voltar: ").strip()

        if opcao == "0":
            return
        elif opcao == "1":
            try:
                numero = int(input("Número do alerta: "))
            except ValueError:
                print("Digite um número válido.")
                continue

            if numero >= 1 and numero <= len(alertas):
                mostrar_detalhes(alertas[numero - 1])
            else:
                print("Esse alerta não existe.")
        else:
            print("Opção inválida.")


def registrar_previsao():
    animais = ler_animais()

    if len(animais) == 0:
        print("Cadastre um animal antes de registrar uma previsão.")
        return

    print("\n--- ANIMAIS ---")
    numero = 1
    for animal in animais:
        print("[" + str(numero) + "] " + animal[0] + " | " + animal[1])
        numero = numero + 1

    try:
        numero = int(input("Número do animal: "))
    except ValueError:
        print("Digite um número válido.")
        return

    if numero < 1 or numero > len(animais):
        print("Esse animal não existe.")
        return

    animal = animais[numero - 1]
    tipo = input("Cuidado (Consulta/Banho/Tosa/Vacina/Outro cuidado): ").strip().capitalize()
    tipos_validos = ["Consulta", "Banho", "Tosa", "Vacina", "Outro cuidado"]

    if tipo not in tipos_validos:
        print("Tipo de cuidado inválido.")
        return

    while True:
        texto_data = input("Data prevista (dd/mm/aaaa): ").strip()

        try:
            data = datetime.strptime(texto_data, "%d/%m/%Y").date()
        except ValueError:
            print("Data inválida. Use o formato dd/mm/aaaa.")
            continue

        if data < date.today():
            print("A data prevista já passou.")
            continue

        break

    registro = [
        tipo,
        data.strftime("%d/%m/%Y"),
        "Pendente",
        animal[0],
        animal[1],
        animal[2],
        animal[3],
        animal[4],
        animal[6],
    ]

    registros = ler_agenda()
    registros.append(registro)
    salvar_agenda(registros)
    print("Previsão registrada como pendente.")


def menu_alertas():
    with open(ARQUIVO_AGENDA, "a", encoding="utf-8") as arquivo:
        pass

    while True:
        print("\n--- VER ALERTAS ---")
        print("[1] Ver alertas  [2] Registrar previsão  [0] Voltar")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            mostrar_alertas()
        elif opcao == "2":
            registrar_previsao()
        elif opcao == "0":
            return
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    menu_alertas()
