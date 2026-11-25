
from datetime import date, datetime


ARQUIVO_CUIDADOS = "registro_cuidado.txt"
ARQUIVO_AGENDA = "agenda_alertas.txt"
ARQUIVO_ANIMAIS = "animais.txt"


def ler_animais():
    try:
        arquivo = open(ARQUIVO_ANIMAIS, "r", encoding="utf-8")
    except FileNotFoundError:
        try:
            arquivo = open("animais/animais.txt", "r", encoding="utf-8")
        except FileNotFoundError:
            return []

    linhas = arquivo.readlines()
    arquivo.close()

    animais = []
    for linha in linhas:
        campos = linha.strip().split(";")
        if len(campos) >= 7:
            animal = {
                "nome": campos[0],
                "especie": campos[1],
                "raca": campos[2],
                "idade": campos[3],
                "saude": campos[4],
                "chegada": campos[5],
                "comportamento": campos[6],
            }
            animais.append(animal)

    return animais


def ler_agenda():
    try:
        arquivo = open(ARQUIVO_AGENDA, "r", encoding="utf-8")
    except FileNotFoundError:
        return []

    linhas = arquivo.readlines()
    arquivo.close()

    registros = []
    for linha in linhas:
        campos = linha.strip().split(";")
        if len(campos) == 9:
            registro = {
                "tipo": campos[0],
                "data": campos[1],
                "situacao": campos[2],
                "nome": campos[3],
                "especie": campos[4],
                "raca": campos[5],
                "idade": campos[6],
                "saude": campos[7],
                "comportamento": campos[8],
            }
            registros.append(registro)

    return registros


def salvar_agenda(registros):
    arquivo = open(ARQUIVO_AGENDA, "w", encoding="utf-8")

    for registro in registros:
        linha = (
            registro["tipo"] + ";" + registro["data"] + ";"
            + registro["situacao"] + ";" + registro["nome"] + ";"
            + registro["especie"] + ";" + registro["raca"] + ";"
            + registro["idade"] + ";" + registro["saude"] + ";"
            + registro["comportamento"] + "\n"
        )
        arquivo.write(linha)

    arquivo.close()


def pedir_data():
    while True:
        texto = input("Data prevista (dd/mm/aaaa): ").strip()
        try:
            data = datetime.strptime(texto, "%d/%m/%Y").date()
            return data.strftime("%d/%m/%Y")
        except ValueError:
            print("Data inválida. Use o formato dd/mm/aaaa.")


def carregar_alertas():
    hoje = date.today()
    alertas = []

    try:
        arquivo = open(ARQUIVO_CUIDADOS, "r", encoding="utf-8")
        linhas = arquivo.readlines()
        arquivo.close()
    except FileNotFoundError:
        linhas = []

    for linha in linhas:
        partes = linha.strip().split(" | ")
        if len(partes) >= 3 and partes[1] == "Vacina":
            texto_data = partes[2].replace("Data da vacina: ", "").strip()
            try:
                data = datetime.strptime(texto_data, "%d/%m/%Y").date()
                dias = (data - hoje).days
                if dias < 0:
                    prazo = "atrasado há " + str(-dias) + " dia(s)"
                elif dias == 0:
                    prazo = "previsto para hoje"
                else:
                    prazo = "previsto em " + str(dias) + " dia(s)"

                alerta = {
                    "tipo": "Vacina",
                    "data": data,
                    "prazo": prazo,
                    "animal": "Não informado no registro antigo",
                    "registro": partes[0],
                    "situacao": "Data registrada",
                }
                alertas.append(alerta)
            except ValueError:
                continue

    registros = ler_agenda()
    for registro in registros:
        if registro["situacao"] == "Pendente":
            try:
                data = datetime.strptime(registro["data"], "%d/%m/%Y").date()
                dias = (data - hoje).days
                if dias < 0:
                    prazo = "atrasado há " + str(-dias) + " dia(s)"
                elif dias == 0:
                    prazo = "previsto para hoje"
                else:
                    prazo = "previsto em " + str(dias) + " dia(s)"

                alerta = {
                    "tipo": registro["tipo"],
                    "data": data,
                    "prazo": prazo,
                    "animal": registro["nome"],
                    "registro": registro,
                    "situacao": registro["situacao"],
                }
                alertas.append(alerta)
            except ValueError:
                continue

    return alertas


def cadastrar_previsao():
    animais = ler_animais()
    if len(animais) == 0:
        print("Cadastre um animal antes de registrar uma previsão.")
        return

    print("\n--- ANIMAIS ---")
    numero = 1
    for animal in animais:
        print("[" + str(numero) + "] " + animal["nome"] + " | " + animal["especie"])
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

    data = pedir_data()
    registros = ler_agenda()
    registro = {
        "tipo": tipo,
        "data": data,
        "situacao": "Pendente",
        "nome": animal["nome"],
        "especie": animal["especie"],
        "raca": animal["raca"],
        "idade": animal["idade"],
        "saude": animal["saude"],
        "comportamento": animal["comportamento"],
    }
    registros.append(registro)
    salvar_agenda(registros)
    print("Previsão registrada como pendente.")


def mostrar_detalhes(alerta):
    print("\n--- DETALHES DO ALERTA ---")
    print("Cuidado: " + alerta["tipo"])
    print("Data prevista: " + alerta["data"].strftime("%d/%m/%Y"))
    print("Prazo: " + alerta["prazo"])

    if alerta["animal"] == "Não informado no registro antigo":
        print("Animal: não informado no registro antigo.")
        print("Registro: " + alerta["registro"])
    else:
        animal = alerta["registro"]
        print("Animal: " + animal["nome"])
        print("Espécie: " + animal["especie"])
        print("Raça: " + animal["raca"])
        print("Idade: " + animal["idade"])
        print("Saúde: " + animal["saude"])
        print("Comportamento: " + animal["comportamento"])


def mostrar_alertas():
    alertas = carregar_alertas()
    if len(alertas) == 0:
        print("Nenhum alerta com data prevista foi encontrado.")
        return

    print("\n--- ALERTAS ---")
    numero = 1
    for alerta in alertas:
        data = alerta["data"].strftime("%d/%m/%Y")
        texto = (
            "[" + str(numero) + "] " + alerta["tipo"] + " | "
            + alerta["animal"] + " | " + data + " | " + alerta["prazo"]
        )
        print(texto)
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


def menu_alertas():
    while True:
        print("\n--- VER ALERTAS ---")
        print("[1] Ver alertas  [2] Registrar previsão  [0] Voltar")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            mostrar_alertas()
        elif opcao == "2":
            cadastrar_previsao()
        elif opcao == "0":
            return
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    menu_alertas()
