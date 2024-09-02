# Lista de exemplo
minha_lista = ["1. Algo","1.1 Algo", "2.0 Outra coisa", "1.5 Teste", "3.0 Exemplo", "1.9 Final", "1.23 Outro item"]

# Remover itens que começam com "1.1" ou "1." seguido de qualquer número de 1 a 9
minha_lista = [item for item in minha_lista if not (item.startswith("1.1") or any(item.startswith(f"1.{i}") for i in range(2, 10)))]

print(minha_lista)
