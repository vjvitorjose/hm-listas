import argparse
import math
import os
import random
import sys
import time


ITERACOES_POR_TEMPERATURA = 100


def ler_instancia(nome_arquivo):
	coordenadas = []
	lendo_coordenadas = False

	with open(nome_arquivo, "r", encoding="utf-8") as arquivo:
		for linha in arquivo:
			linha = linha.strip()
			if linha == "NODE_COORD_SECTION":
				lendo_coordenadas = True
				continue
			if linha == "EOF":
				break
			if lendo_coordenadas:
				partes = linha.split()
				if len(partes) >= 3:
					coordenadas.append((float(partes[1]), float(partes[2])))

	if len(coordenadas) < 2:
		raise ValueError(f"instancia invalida: {nome_arquivo}")
	return coordenadas


def calcular_distancias(coordenadas):
	quantidade = len(coordenadas)
	distancias = [[0] * quantidade for _ in range(quantidade)]

	for origem in range(quantidade):
		for destino in range(origem + 1, quantidade):
			dx = coordenadas[origem][0] - coordenadas[destino][0]
			dy = coordenadas[origem][1] - coordenadas[destino][1]
			distancia = int(math.floor(math.hypot(dx, dy) + 0.5))
			distancias[origem][destino] = distancia
			distancias[destino][origem] = distancia

	return distancias


def custo_rota(rota, distancias):
	return sum(
		distancias[rota[indice]][rota[(indice + 1) % len(rota)]]
		for indice in range(len(rota))
	)


def gerar_vizinho(rota):
	inicio, fim = sorted(random.sample(range(1, len(rota)), 2))
	vizinho = rota[:]
	vizinho[inicio:fim] = reversed(vizinho[inicio:fim])
	return vizinho


def simulated_annealing(distancias, temperatura_inicial, taxa_resfriamento,
						max_iteracoes):
	rota_atual = list(range(len(distancias)))
	random.shuffle(rota_atual)
	custo_atual = custo_rota(rota_atual, distancias)
	melhor_rota = rota_atual[:]
	melhor_custo = custo_atual
	temperatura = temperatura_inicial
	iteracoes = 0

	while iteracoes < max_iteracoes:
		for _ in range(ITERACOES_POR_TEMPERATURA):
			if iteracoes >= max_iteracoes:
				break
			vizinho = gerar_vizinho(rota_atual)
			custo_vizinho = custo_rota(vizinho, distancias)
			iteracoes += 1

			diferenca = custo_atual - custo_vizinho
			if diferenca > 0 or random.random() < math.exp(diferenca / temperatura):
				rota_atual = vizinho
				custo_atual = custo_vizinho

				if custo_atual < melhor_custo:
					melhor_rota = rota_atual[:]
					melhor_custo = custo_atual

		temperatura *= taxa_resfriamento

	return melhor_rota, melhor_custo, iteracoes


def executar_instancia(nome_arquivo, temperatura_inicial, taxa_resfriamento,
					   max_iteracoes):
	coordenadas = ler_instancia(nome_arquivo)
	distancias = calcular_distancias(coordenadas)
	inicio = time.perf_counter()
	rota, custo, iteracoes = simulated_annealing(
		distancias,
		temperatura_inicial,
		taxa_resfriamento,
		max_iteracoes,
	)
	tempo = time.perf_counter() - inicio
	rota_formatada = " ".join(str(cidade + 1) for cidade in rota)

	print(f"Instancia: {nome_arquivo} ({len(coordenadas)} cidades)")
	print(f"  Melhor valor: {custo}")
	print(f"  Iteracoes: {iteracoes}")
	print(f"  Tempo de execução: {tempo:.9f} s")
	print(f"  Rota: {rota_formatada} {rota[0] + 1}")


def criar_parser():
	parser = argparse.ArgumentParser(
		description="Simulated annealing para o problema do caixeiro viajante."
	)
	parser.add_argument(
		"temperatura_inicial", nargs="?", type=float,
		help="temperatura inicial",
	)
	parser.add_argument(
		"taxa_resfriamento", nargs="?", type=float,
		help="fator multiplicativo de resfriamento",
	)
	parser.add_argument(
		"max_iteracoes", nargs="?", type=int,
		help="numero maximo de iteracoes",
	)
	parser.add_argument(
		"arquivos", nargs="*",
		help="arquivos TSPLIB de entrada",
	)
	return parser


def main():
	argumentos = criar_parser().parse_args()
	if None in (
		argumentos.temperatura_inicial,
		argumentos.taxa_resfriamento,
		argumentos.max_iteracoes,
	):
		print(
			"Uso: python 22-09/tsp.py <temperatura_inicial> "
			"<taxa_resfriamento> <max_iteracoes> [arquivos]",
			file=sys.stderr,
		)
		return 1
	if argumentos.temperatura_inicial <= 0:
		print("Erro: a temperatura inicial deve ser positiva.", file=sys.stderr)
		return 1
	if not 0 < argumentos.taxa_resfriamento < 1:
		print("Erro: a taxa de resfriamento deve estar entre 0 e 1.", file=sys.stderr)
		return 1
	if argumentos.max_iteracoes <= 0:
		print("Erro: o numero maximo de iteracoes deve ser positivo.", file=sys.stderr)
		return 1

	arquivos = argumentos.arquivos or [
		os.path.join(os.path.dirname(__file__), "tsp_5"),
		os.path.join(os.path.dirname(__file__), "tsp_51"),
	]

	try:
		for nome_arquivo in arquivos:
			executar_instancia(
				nome_arquivo,
				argumentos.temperatura_inicial,
				argumentos.taxa_resfriamento,
				argumentos.max_iteracoes,
			)
	except (OSError, ValueError) as erro:
		print(f"Erro: {erro}", file=sys.stderr)
		return 1
	return 0


if __name__ == "__main__":
	sys.exit(main())
