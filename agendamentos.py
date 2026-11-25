from datetime import date, datetime

ARQUIVO_ANIMAIS = "animais.txt"
ARQUIVO_AGENDAMENTOS = "agendamentos.txt"


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


def ler_agendamentos():
    try:
        with open(ARQUIVO_AGENDAMENTOS, "r", encoding="utf-8") as arquivo:
            linhas = arquivo.read().splitlines()
    except FileNotFoundError:
        return []

    agendamentos = []
    for linha in linhas:
        campos = linha.split(";")
        if len(campos) == 5:
            agendamentos.append(campos)

    return agendamentos


def salvar_agendamentos(agendamentos):
    with open(ARQUIVO_AGENDAMENTOS, "w", encoding="utf-8") as arquivo:
        for agendamento in agendamentos:
            arquivo.write(";".join(agendamento) + "\n")


def mostrar_agendamentos(agendamentos):
    print("\n--- VISITAS AGENDADAS ---")
    numero = 1

    for agendamento in agendamentos:
        print(
            "[" + str(numero) + "] " + agendamento[0]
            + " | " + agendamento[1]
            + " | Animal: " + agendamento[2]
            + " | " + agendamento[3]
            + " às " + agendamento[4]
        )

        try:
            data_hora = datetime.strptime(
                agendamento[3] + " " + agendamento[4], "%d/%m/%Y %H:%M"
            )
            dias = (data_hora.date() - date.today()).days

            if dias == 0:
                print("A visita é hoje!")
            elif dias > 0:
                print("Faltam " + str(dias) + " dia(s) para a visita.")
            else:
                print("A visita passou há " + str(-dias) + " dia(s).")
        except ValueError:
            print("A data ou o horário deste registro é inválido.")

        numero = numero + 1


def cadastrar_visita():
    animais = ler_animais()

    if len(animais) == 0:
        print("Nenhum animal cadastrado.")
        return

    print("\n--- ANIMAIS CADASTRADOS ---")
    numero = 1
    for animal in animais:
        print("[" + str(numero) + "] " + animal[0] + " | " + animal[1])
        numero = numero + 1

    interessado = input("Nome do interessado: ").strip()
    telefone = input("Telefone para contato: ").strip()

    if interessado == "" or telefone == "":
        print("Nome e telefone são obrigatórios.")
        return

    nome_animal = input("Animal que deseja conhecer: ").strip()
    animal_encontrado = False

    for animal in animais:
        if animal[0].lower() == nome_animal.lower():
            nome_animal = animal[0]
            animal_encontrado = True
            break

    if animal_encontrado == False:
        print("Esse animal não está cadastrado.")
        return

    agendamentos = ler_agendamentos()

    while True:
        texto_data = input("Data da visita (dd/mm/aaaa): ").strip()
        horario = input("Horário da visita (hh:mm): ").strip()

        try:
            data_hora = datetime.strptime(
                texto_data + " " + horario, "%d/%m/%Y %H:%M"
            )
        except ValueError:
            print("Data ou horário inválido. Use dd/mm/aaaa e hh:mm.")
            continue

        if data_hora < datetime.now():
            print("A data e o horário da visita já passaram.")
            continue

        conflito = False
        for agendamento in agendamentos:
            if agendamento[3] == texto_data and agendamento[4] == horario:
                conflito = True

        if conflito:
            print("Já existe uma visita nesse dia e horário.")
            continue

        break

    novo_agendamento = [
        interessado,
        telefone,
        nome_animal,
        texto_data,
        horario,
    ]
    agendamentos.append(novo_agendamento)
    salvar_agendamentos(agendamentos)
    print("Visita agendada com sucesso.")


def listar_visitas():
    agendamentos = ler_agendamentos()

    if len(agendamentos) == 0:
        print("Nenhuma visita agendada.")
        return

    mostrar_agendamentos(agendamentos)


def editar_agendamento():
    agendamentos = ler_agendamentos()

    if len(agendamentos) == 0:
        print("Nenhuma visita agendada para editar.")
        return

    mostrar_agendamentos(agendamentos)

    try:
        escolha = int(input("Número da visita para editar: "))
    except ValueError:
        print("Digite um número válido.")
        return

    if escolha < 1 or escolha > len(agendamentos):
        print("Essa visita não existe.")
        return

    interessado = input("Nome do interessado: ").strip()
    telefone = input("Telefone para contato: ").strip()

    if interessado == "" or telefone == "":
        print("Nome e telefone são obrigatórios.")
        return

    animais = ler_animais()
    nome_animal = input("Animal que deseja conhecer: ").strip()
    animal_encontrado = False

    for animal in animais:
        if animal[0].lower() == nome_animal.lower():
            nome_animal = animal[0]
            animal_encontrado = True
            break

    if animal_encontrado == False:
        print("Esse animal não está cadastrado.")
        return

    while True:
        texto_data = input("Data da visita (dd/mm/aaaa): ").strip()
        horario = input("Horário da visita (hh:mm): ").strip()

        try:
            data_hora = datetime.strptime(
                texto_data + " " + horario, "%d/%m/%Y %H:%M"
            )
        except ValueError:
            print("Data ou horário inválido. Use dd/mm/aaaa e hh:mm.")
            continue

        if data_hora < datetime.now():
            print("A data e o horário da visita já passaram.")
            continue

        conflito = False
        for numero in range(len(agendamentos)):
            if numero != escolha - 1:
                agendamento = agendamentos[numero]
                if agendamento[3] == texto_data and agendamento[4] == horario:
                    conflito = True

        if conflito:
            print("Já existe outra visita nesse dia e horário.")
            continue

        break

    agendamentos[escolha - 1] = [
        interessado,
        telefone,
        nome_animal,
        texto_data,
        horario,
    ]
    salvar_agendamentos(agendamentos)
    print("Agendamento atualizado com sucesso.")


def cancelar_visita():
    agendamentos = ler_agendamentos()

    if len(agendamentos) == 0:
        print("Nenhuma visita agendada para cancelar.")
        return

    mostrar_agendamentos(agendamentos)

    try:
        escolha = int(input("Número da visita para cancelar: "))
    except ValueError:
        print("Digite um número válido.")
        return

    if escolha < 1 or escolha > len(agendamentos):
        print("Essa visita não existe.")
        return

    agendamentos.pop(escolha - 1)
    salvar_agendamentos(agendamentos)
    print("Visita cancelada.")


def menu_agendamentos():
    with open(ARQUIVO_AGENDAMENTOS, "a", encoding="utf-8") as arquivo:
        pass

    while True:
        print("""
        --- AGENDAMENTO DE VISITAS ---
        [1] Cadastrar visita
        [2] Listar visitas agendadas
        [3] Editar agendamento
        [4] Cancelar visita
        [5] Voltar ao menu principal
        """)

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            cadastrar_visita()
        elif opcao == "2":
            listar_visitas()
        elif opcao == "3":
            editar_agendamento()
        elif opcao == "4":
            cancelar_visita()
        elif opcao == "5":
            print("Voltando ao menu principal...")
            return
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    menu_agendamentos()
