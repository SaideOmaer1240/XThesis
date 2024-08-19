def main():
    print("Iniciando o script de testes")

    # Suponha que você tenha uma lista de dicionários para trabalhar
    lista_de_dicionarios = [
        {"nome": "João", "idade": 25},
        {"nome": "Maria", "idade": 30},
        {"nome": "Pedro", "idade": 22}
    ]

    print("Lista de dicionários carregada:", lista_de_dicionarios)

    # Iterar sobre a lista de dicionários
    for dicionario in lista_de_dicionarios:
        # Verificar se algum valor do dicionário contém a sílaba "ma"
        if any("ma" in str(valor).lower() for valor in dicionario.values()):
            # Imprimir o dicionário e quebrar a iteração
            print("Dicionário encontrado:", dicionario)
            break
    else:
        print("Nenhum dicionário encontrado com a sílaba 'ma' nos valores")

if __name__ == "__main__":
    main()

