import sys
import time


def ler_instancia(nome_arquivo):
	with open(nome_arquivo, "r", encoding="utf-8") as arquivo:
		primeira_linha = arquivo.readline().split()
		quantidade = int(primeira_linha[0])
		capacidade = int(primeira_linha[1])
		itens = []

		for indice in range(quantidade):
			valor, peso = map(int, arquivo.readline().split())
			itens.append((indice, valor, peso))

	return capacidade, itens


def selecionar_itens(itens, capacidade, chave):
	selecionados = [0] * len(itens)
	peso_total = 0
	valor_total = 0
	iteracoes = 0

	for indice, valor, peso in sorted(itens, key=chave):
		iteracoes += 1
		if peso_total + peso <= capacidade:
			selecionados[indice] = 1
			peso_total += peso
			valor_total += valor

	return selecionados, valor_total, peso_total, iteracoes


def por_melhor_custo_beneficio(item):
	indice, valor, peso = item
	return (-(valor / peso), indice)


def por_itens_mais_leves(item):
	indice, _, peso = item
	return (peso, indice)


def executar_algoritmo(nome, itens, capacidade, chave):
	inicio = time.perf_counter()
	solucao, valor, peso, iteracoes = selecionar_itens(itens, capacidade, chave)
	tempo = time.perf_counter() - inicio

	print(f"  {nome:<25} valor: {valor} | peso: {peso}/{capacidade}")
	print(f"  Iteracoes: {iteracoes} | tempo: {tempo:.9f} s")
	print(f"  Solucao: {''.join(map(str, solucao))}")
	print(f"  Itens selecionados: {[indice + 1 for indice, bit in enumerate(solucao) if bit]}")


def executar_instancia(nome_arquivo):
	capacidade, itens = ler_instancia(nome_arquivo)
	print(f"Instancia: {nome_arquivo} ({len(itens)} itens, capacidade {capacidade})")
	executar_algoritmo(
		"Melhor custo-beneficio", itens, capacidade, por_melhor_custo_beneficio
	)
	executar_algoritmo("Itens mais leves", itens, capacidade, por_itens_mais_leves)
	print()


def main():
	arquivos = sys.argv[1:] or ["15-09/mochila_4_20", "15-09/mochila_100_1000_1"]
	try:
		for nome_arquivo in arquivos:
			executar_instancia(nome_arquivo)
	except (OSError, ValueError, ZeroDivisionError) as erro:
		print(f"Erro: {erro}", file=sys.stderr)
		return 1
	return 0


if __name__ == "__main__":
	sys.exit(main())
