import argparse
import math
import os
import random
import sys
import time


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


def busca_local(rota, distancias):
	rota = rota[:]
	quantidade = len(rota)

	while True:
		melhor_delta = 0
		melhor_troca = None
		for inicio in range(quantidade - 1):
			for fim in range(inicio + 2, quantidade):
				if inicio == 0 and fim == quantidade - 1:
					continue
				delta = (
					distancias[rota[inicio]][rota[fim]]
					+ distancias[rota[inicio + 1]][rota[(fim + 1) % quantidade]]
					- distancias[rota[inicio]][rota[inicio + 1]]
					- distancias[rota[fim]][rota[(fim + 1) % quantidade]]
				)
				if delta < melhor_delta:
					melhor_delta = delta
					melhor_troca = (inicio, fim)

		if melhor_troca is None:
			break
		inicio, fim = melhor_troca
		rota[inicio + 1:fim + 1] = reversed(rota[inicio + 1:fim + 1])

	return rota, custo_rota(rota, distancias)


def alterar_vizinhanca(rota, k):
	vizinho = rota[:]
	quantidade = len(vizinho)
	if quantidade < 3:
		return vizinho

	for _ in range(k):
		posicao_a, posicao_b = random.sample(range(1, quantidade), 2)
		vizinho[posicao_a], vizinho[posicao_b] = (
			vizinho[posicao_b],
			vizinho[posicao_a],
		)
	return vizinho


def vns(distancias, max_iteracoes_sem_melhora):
	quantidade = len(distancias)
	rota_atual = [0] + random.sample(range(1, quantidade), quantidade - 1)
	melhor_rota, melhor_custo = busca_local(rota_atual, distancias)
	max_vizinhancas = max(1, quantidade - 1)
	vizinhanca = 1
	iteracoes_sem_melhora = 0
	iteracoes = 0

	while iteracoes_sem_melhora < max_iteracoes_sem_melhora:
		rota_candidata = alterar_vizinhanca(melhor_rota, vizinhanca)
		rota_candidata, custo_candidato = busca_local(rota_candidata, distancias)
		iteracoes += 1

		if custo_candidato < melhor_custo:
			melhor_rota = rota_candidata
			melhor_custo = custo_candidato
			iteracoes_sem_melhora = 0
			vizinhanca = 1
		else:
			iteracoes_sem_melhora += 1
			if vizinhanca == max_vizinhancas:
				vizinhanca = 1
			else:
				vizinhanca += 1

	return melhor_rota, melhor_custo, iteracoes


def executar_instancia(nome_arquivo, max_iteracoes_sem_melhora):
	coordenadas = ler_instancia(nome_arquivo)
	distancias = calcular_distancias(coordenadas)
	inicio = time.perf_counter()
	rota, custo, iteracoes = vns(distancias, max_iteracoes_sem_melhora)
	tempo = time.perf_counter() - inicio
	rota_formatada = " ".join(str(cidade + 1) for cidade in rota)

	print(f"Instancia: {nome_arquivo} ({len(coordenadas)} cidades)")
	print(f"  Melhor valor: {custo}")
	print(f"  Iteracoes VNS: {iteracoes}")
	print(f"  Tempo de execucao: {tempo:.9f} s")
	print(f"  Rota: {rota_formatada} {rota[0] + 1}")


def criar_parser():
	parser = argparse.ArgumentParser(
		description="VNS para o problema do caixeiro viajante."
	)
	parser.add_argument(
		"max_iteracoes_sem_melhora",
		type=int,
		help="numero maximo de iteracoes consecutivas sem melhora",
	)
	parser.add_argument(
		"arquivos",
		nargs="*",
		help="arquivos TSPLIB de entrada",
	)
	return parser


def main():
	argumentos = criar_parser().parse_args()
	if argumentos.max_iteracoes_sem_melhora <= 0:
		print(
			"Erro: o numero maximo de iteracoes sem melhora deve ser positivo.",
			file=sys.stderr,
		)
		return 1

	arquivos = argumentos.arquivos or [
		os.path.join(os.path.dirname(__file__), "tsp_5"),
		os.path.join(os.path.dirname(__file__), "tsp_51"),
	]

	try:
		for nome_arquivo in arquivos:
			executar_instancia(
				nome_arquivo,
				argumentos.max_iteracoes_sem_melhora,
			)
	except (OSError, ValueError) as erro:
		print(f"Erro: {erro}", file=sys.stderr)
		return 1
	return 0


if __name__ == "__main__":
	sys.exit(main())