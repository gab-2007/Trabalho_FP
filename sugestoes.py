def ler_animais_sugestoes():
    try:
        arquivo = open("animais.txt", "r", encoding="utf-8")
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
                "cuidados_especiais": [],
            }
            animais.append(animal)

    return animais


def ler_lista(rotulo):
    while True:
        texto = input(rotulo)
        itens = texto.split(",")
        lista = []

        for item in itens:
            item = item.strip()
            if item != "":
                lista.append(item)

        if len(lista) > 0:
            return lista

        print("Informe pelo menos uma opção.")


def ler_idade(rotulo):
    while True:
        try:
            idade = int(input(rotulo))
            if idade >= 0:
                return idade
        except ValueError:
            print("Digite uma idade válida em anos.")
            continue

        print("Digite uma idade válida em anos.")


def coletar_adotantes():
    while True:
        try:
            quantidade = int(
                input("Quantos possíveis adotantes deseja comparar? ")
            )
            if quantidade >= 0:
                break
        except ValueError:
            print("Digite zero ou um número positivo.")

        print("Digite zero ou um número positivo.")

    adotantes = []

    for numero in range(quantidade):
        print("\n--- POSSÍVEL ADOTANTE " + str(numero + 1) + " ---")
        nome = input("Nome: ").strip()
        especies = ler_lista("Espécies de interesse (separe por vírgula): ")
        idade_minima = ler_idade("Idade mínima aceita: ")
        idade_maxima = ler_idade("Idade máxima aceita: ")

        while idade_maxima < idade_minima:
            print("A idade máxima não pode ser menor que a mínima.")
            idade_maxima = ler_idade("Idade máxima aceita: ")

        comportamentos = ler_lista(
            "Comportamentos aceitos (separe por vírgula): "
        )

        adotante = {
            "nome": nome,
            "especies_interesse": especies,
            "idade_minima": idade_minima,
            "idade_maxima": idade_maxima,
            "comportamentos_aceitos": comportamentos,
        }
        adotantes.append(adotante)

    return adotantes


def sugerir_adotantes(animal, adotantes):
    sugestoes = []

    try:
        idade_animal = int(animal["idade"])
    except (KeyError, TypeError, ValueError):
        idade_animal = -1

    for adotante in adotantes:
        compativel = True
        especie_encontrada = False
        comportamento_encontrado = False

        if idade_animal < adotante["idade_minima"]:
            compativel = False
        if idade_animal > adotante["idade_maxima"]:
            compativel = False

        for especie in adotante["especies_interesse"]:
            if animal["especie"].lower() == especie.lower():
                especie_encontrada = True

        for comportamento in adotante["comportamentos_aceitos"]:
            if animal["comportamento"].lower() == comportamento.lower():
                comportamento_encontrado = True

        if especie_encontrada == False:
            compativel = False
        if comportamento_encontrado == False:
            compativel = False

        if compativel:
            sugestoes.append(adotante)

    if len(sugestoes) > 0:
        print("\nPossíveis adotantes encontrados:")
        for adotante in sugestoes:
            print("- " + adotante["nome"])
    else:
        print("\nNenhum adotante compatível foi encontrado.")

    print("\nCuidados especiais:")
    cuidados = animal["cuidados_especiais"]
    if len(cuidados) > 0:
        for cuidado in cuidados:
            print("- " + cuidado)
    else:
        print("Nenhum cuidado especial registrado no cadastro atual.")

    return sugestoes


def menu_sugestoes():
    print("\n===== SUGESTÕES PERSONALIZADAS =====")
    animais = ler_animais_sugestoes()

    if len(animais) == 0:
        print("Nenhum animal cadastrado.")
        return

    numero = 1
    for animal in animais:
        print(
            "[" + str(numero) + "] " + animal["nome"]
            + " | " + animal["especie"]
        )
        numero = numero + 1

    try:
        numero = int(input("Escolha o animal: "))
    except ValueError:
        print("Digite um número válido.")
        return

    if numero < 1 or numero > len(animais):
        print("Esse animal não existe.")
        return

    animal = animais[numero - 1]
    print("\nAnimal: " + animal["nome"])
    print("Espécie: " + animal["especie"])
    print("Idade: " + animal["idade"])
    print("Comportamento: " + animal["comportamento"])

    adotantes = coletar_adotantes()
    sugerir_adotantes(animal, adotantes)
