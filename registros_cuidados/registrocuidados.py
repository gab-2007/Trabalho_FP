from datetime import datetime
import os
print(os.path.abspath('registro_cuidados.txt'))
with open('registro_cuidado.txt','a', encoding='utf-8') as arquivo:
    pass
print(os.getcwd())

def escolher_cuidado():
    cuidado = input('''
Escolha um cuidado:
Banho
Tosa
Vacina
Consulta
> ''').strip().capitalize()

    while cuidado not in ['Banho', 'Tosa', 'Vacina', 'Consulta']:
        cuidado = input('Opção inválida. Tente novamente: ').strip().capitalize()

    return cuidado


def registrar_cuidado():
    print('\n--- REGISTRAR CUIDADO ---')
    cuidado = escolher_cuidado()

    detalhe = ''
    if cuidado == 'Vacina':
        while True:
            data = input('Data da vacina (dd/mm/aaaa): ')
            try:
                datetime.strptime(data, '%d/%m/%Y')
                break
            except ValueError:
                print('Data inválida!')

        detalhe = ' | Data da vacina: ' + data


    agora = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    registro = f'Registrado em: {agora} | {cuidado}{detalhe}\n'

    with open('registro_cuidado.txt', 'a', encoding='utf-8') as arquivo:
        arquivo.write(registro)

    print('Cuidado registrado com sucesso!')


def listar_cuidados():
    try:
        with open('registro_cuidado.txt', 'r', encoding='utf-8') as arquivo:
            cuidados = arquivo.readlines()
    except FileNotFoundError:
        cuidados = []

    if len(cuidados) == 0:
        print('Nenhum cuidado registrado.')
    else:
        print('\n--- CUIDADOS REGISTRADOS ---')
        for i in range(len(cuidados)):
            print(f'[{i + 1}] {cuidados[i].strip()}')

    return cuidados


def editar_cuidados():
    cuidados = listar_cuidados()
    if len(cuidados) == 0:
        return

    try:
        numero = int(input('Número do cuidado para editar: '))
    except ValueError:
        print('Digite um número válido!')
        return

    if numero < 1 or numero > len(cuidados):
        print('Cuidado não encontrado!')
        return

    partes = cuidados[numero - 1].strip().split(' | ')
    data_registro = partes[0]


    if 'Registrado em:' not in data_registro:
        agora = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        data_registro = 'Registrado em: ' + agora

    novo_cuidado = escolher_cuidado()
    detalhe = ''

    if novo_cuidado == 'Vacina':
        while True:
            data = input('Data da vacina (dd/mm/aaaa): ')
            try:
                datetime.strptime(data, '%d/%m/%Y')
                break
            except ValueError:
                print('Data inválida!')

        detalhe = ' | Data da vacina: ' + data

    cuidados[numero - 1] = f'{data_registro} | {novo_cuidado}{detalhe}\n'

    with open('registro_cuidado.txt', 'w', encoding='utf-8') as arquivo:
        arquivo.writelines(cuidados)

    print('Cuidado editado com sucesso!')


def excluir_cuidados():
    cuidados = listar_cuidados()
    if len(cuidados) == 0:
        return

    try:
        numero = int(input('Número do cuidado para excluir: '))
    except ValueError:
        print('Digite um número válido!')
        return

    if numero < 1 or numero > len(cuidados):
        print('Cuidado não encontrado!')
        return

    cuidados.pop(numero - 1)

    with open('registro_cuidado.txt', 'w', encoding='utf-8') as arquivo:
        arquivo.writelines(cuidados)

    print('Cuidado excluído com sucesso!')


def menu_registro():
    while True:
        print('''
--- CADASTRO DE CUIDADOS ---
[1] Registrar cuidado
[2] Listar cuidados
[3] Editar cuidado
[4] Excluir cuidado
[0] Sair
''')

        escolha = input('Escolha uma opção: ')

        if escolha == '1':
            registrar_cuidado()
        elif escolha == '2':
            listar_cuidados()
        elif escolha == '3':
            editar_cuidados()
        elif escolha == '4':
            excluir_cuidados()
        elif escolha == '0':
            print('Saindo...')
            break
        else:
            print('Opção inválida!')


menu_registro()
