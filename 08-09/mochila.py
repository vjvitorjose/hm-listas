import random
import sys
import time
from pathlib import Path


def ler_mochila(nome_arquivo):
	with open(nome_arquivo, "r") as arquivo:
		primeira_linha = arquivo.readline().split()
		num_itens = int(primeira_linha[0])
		capacidade = int(primeira_linha[1])

		valores = []
		pesos = []
		for _ in range(num_itens):
			valor, peso = map(int, arquivo.readline().split())
			valores.append(valor)
			pesos.append(peso)

	return capacidade, valores, pesos


def avaliar(solucao, valores, pesos):
	valor = sum(bit * item_valor for bit, item_valor in zip(solucao, valores))
	peso = sum(bit * item_peso for bit, item_peso in zip(solucao, pesos))
	return valor, peso


def gerar_solucao_inicial(valores, pesos, capacidade):
	solucao = [random.randint(0, 1) for _ in valores]

	while avaliar(solucao, valores, pesos)[1] > capacidade:
		itens_selecionados = [indice for indice, bit in enumerate(solucao) if bit]
		indice = random.choice(itens_selecionados)
		solucao[indice] = 0

	return solucao


def busca_local(valores, pesos, capacidade, max_iteracoes):
	solucao = gerar_solucao_inicial(valores, pesos, capacidade)
	melhor_valor, melhor_peso = avaliar(solucao, valores, pesos)
	iteracao = 0

	while iteracao < max_iteracoes:
		melhor_vizinho = None
		melhor_valor_vizinho = melhor_valor
		melhor_peso_vizinho = melhor_peso

		for indice in range(len(solucao)):
			vizinho = solucao.copy()
			vizinho[indice] = 1 - vizinho[indice]
			valor, peso = avaliar(vizinho, valores, pesos)

			if peso <= capacidade and valor > melhor_valor_vizinho:
				melhor_vizinho = vizinho
				melhor_valor_vizinho = valor
				melhor_peso_vizinho = peso

		iteracao += 1
		if melhor_vizinho is None:
			break

		solucao = melhor_vizinho
		melhor_valor = melhor_valor_vizinho
		melhor_peso = melhor_peso_vizinho

	return solucao, melhor_valor, melhor_peso, iteracao


def executar(nome_arquivo, max_iteracoes):
	capacidade, valores, pesos = ler_mochila(nome_arquivo)
	inicio = time.perf_counter()
	solucao, valor, peso, iteracoes = busca_local(
		valores, pesos, capacidade, max_iteracoes
	)
	fim = time.perf_counter()

	print(f"Instancia: {nome_arquivo}")
	print(f"Solucao: {''.join(map(str, solucao))}")
	print(f"Valor: {valor}")
	print(f"Peso: {peso}/{capacidade}")
	print(f"Iteracoes: {iteracoes}")
	print(f"Tempo de execucao: {fim - inicio:.6f} segundos")


def main():
	if len(sys.argv) not in (2, 3):
		print(f"Uso: python {sys.argv[0]} <max_iteracoes> [arquivo]" )
		return 1

	try:
		max_iteracoes = int(sys.argv[1])
		if max_iteracoes < 0:
			raise ValueError("max_iteracoes deve ser maior ou igual a zero")

		arquivos = [sys.argv[2]] if len(sys.argv) == 3 else [
			"mochila_4_20",
			"mochila_100_1000_1",
		]
		for nome_arquivo in arquivos:
			if len(sys.argv) == 2:
				nome_arquivo = str(Path(__file__).resolve().parent / nome_arquivo)
			executar(nome_arquivo, max_iteracoes)
			if len(arquivos) > 1:
				print()
	except (OSError, ValueError) as erro:
		print(f"Erro: {erro}")
		return 1

	return 0


if __name__ == "__main__":
	sys.exit(main())
