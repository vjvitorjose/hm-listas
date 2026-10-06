import math
import sys
import time
from pathlib import Path


def ler_mochila(nome_arquivo):
	with open(nome_arquivo, "r") as arquivo:
		primeira_linha = arquivo.readline().split()
		num_itens = int(primeira_linha[0])
		capacidade = int(primeira_linha[1])
		itens = [tuple(map(int, arquivo.readline().split())) for _ in range(num_itens)]

	return capacidade, itens


def avaliar(solucao, itens):
	valor = sum(bit * item[0] for bit, item in zip(solucao, itens))
	peso = sum(bit * item[1] for bit, item in zip(solucao, itens))
	return valor, peso


def gerar_solucao_gulosa(itens, capacidade):
	ordem = sorted(
		range(len(itens)),
		key=lambda indice: itens[indice][0] / itens[indice][1],
		reverse=True,
	)
	solucao = [0] * len(itens)
	peso_atual = 0

	for indice in ordem:
		valor, peso = itens[indice]
		if peso_atual + peso <= capacidade:
			solucao[indice] = 1
			peso_atual += peso

	return solucao


def busca_tabu(itens, capacidade, max_sem_melhora, prazo_tabu=None):
	solucao = gerar_solucao_gulosa(itens, capacidade)
	valor_atual, _ = avaliar(solucao, itens)
	melhor_solucao = solucao.copy()
	melhor_valor = valor_atual
	sem_melhora = 0
	iteracoes = 0
	prazo_tabu = prazo_tabu or max(1, round(math.sqrt(len(itens))))
	lista_tabu = {}

	while sem_melhora < max_sem_melhora:
		vizinhos = []
		for indice in range(len(solucao)):
			vizinho = solucao.copy()
			vizinho[indice] = 1 - vizinho[indice]
			valor, peso = avaliar(vizinho, itens)
			if peso <= capacidade:
				vizinhos.append((valor, indice, vizinho))

		if not vizinhos:
			break

		# A aspiracao regional libera o melhor vizinho tabu se ele melhora s.
		melhor_regional = max(vizinhos, key=lambda candidato: candidato[0])
		admissiveis = [
			candidato
			for candidato in vizinhos
			if candidato[1] not in lista_tabu
			or candidato[0] > melhor_valor
		]
		if (
			melhor_regional[1] in lista_tabu
			and melhor_regional[0] > valor_atual
			and melhor_regional not in admissiveis
		):
			admissiveis.append(melhor_regional)

		if admissiveis:
			valor, indice, proxima_solucao = max(
				admissiveis, key=lambda candidato: candidato[0]
			)
		else:
			# Se todos estiverem tabu, libera o movimento com menor prazo restante.
			valor, indice, proxima_solucao = min(
				vizinhos, key=lambda candidato: lista_tabu[candidato[1]]
			)

		lista_tabu = {
			item: prazo - 1
			for item, prazo in lista_tabu.items()
			if prazo - 1 > 0
		}
		lista_tabu[indice] = prazo_tabu
		solucao = proxima_solucao
		valor_atual = valor
		iteracoes += 1

		if valor > melhor_valor:
			melhor_solucao = solucao.copy()
			melhor_valor = valor
			sem_melhora = 0
		else:
			sem_melhora += 1

	return melhor_solucao, melhor_valor, avaliar(melhor_solucao, itens)[1], iteracoes


def executar(nome_arquivo, max_sem_melhora, prazo_tabu=None):
	capacidade, itens = ler_mochila(nome_arquivo)
	inicio = time.perf_counter()
	solucao, valor, peso, iteracoes = busca_tabu(
		itens, capacidade, max_sem_melhora, prazo_tabu
	)
	fim = time.perf_counter()

	print(f"Instancia: {nome_arquivo}")
	print(f"Solucao: {''.join(map(str, solucao))}")
	print(f"Valor: {valor}")
	print(f"Peso: {peso}/{capacidade}")
	print(f"Iteracoes: {iteracoes}")
	print(f"Tempo de execucao: {fim - inicio:.6f} segundos")


def main():
	if len(sys.argv) not in (2, 3, 4):
		print(
			f"Uso: python {sys.argv[0]} <max_sem_melhora> "
			"[arquivo] [prazo_tabu]"
		)
		return 1

	try:
		max_sem_melhora = int(sys.argv[1])
		if max_sem_melhora < 0:
			raise ValueError("max_sem_melhora deve ser maior ou igual a zero")

		prazo_tabu = int(sys.argv[3]) if len(sys.argv) == 4 else None
		if prazo_tabu is not None and prazo_tabu <= 0:
			raise ValueError("prazo_tabu deve ser maior que zero")

		arquivos = [sys.argv[2]] if len(sys.argv) >= 3 else [
			"mochila_4_20",
			"mochila_100_1000_1",
		]
		for nome_arquivo in arquivos:
			if len(sys.argv) == 2:
				nome_arquivo = str(Path(__file__).resolve().parent / nome_arquivo)
			executar(nome_arquivo, max_sem_melhora, prazo_tabu)
			if len(arquivos) > 1:
				print()
	except (OSError, ValueError, ZeroDivisionError) as erro:
		print(f"Erro: {erro}")
		return 1

	return 0


if __name__ == "__main__":
	sys.exit(main())
