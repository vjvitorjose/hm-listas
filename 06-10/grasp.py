import argparse
import math
import os
import random
import sys
import time


ALFA = 0.3


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


def construir_solucao(distancias, alfa=ALFA):
	quantidade = len(distancias)
	rota = [0]
	nao_visitadas = set(range(1, quantidade))
	atual = 0

	while nao_visitadas:
		candidatos = [
			(cidade, distancias[atual][cidade])
			for cidade in nao_visitadas
		]
		cmin = min(custo for _, custo in candidatos)
		cmax = max(custo for _, custo in candidatos)
		limite = cmin + alfa * (cmax - cmin)
		lrc = [cidade for cidade, custo in candidatos if custo <= limite]
		proxima = random.choice(lrc)
		rota.append(proxima)
		nao_visitadas.remove(proxima)
		atual = proxima

	return rota


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


def grasp(distancias, grasp_max):
	melhor_rota = None
	melhor_custo = math.inf
	iteracoes = 0

	while iteracoes < grasp_max:
		rota = construir_solucao(distancias)
		rota, custo = busca_local(rota, distancias)
		if custo < melhor_custo:
			melhor_rota = rota
			melhor_custo = custo
		iteracoes += 1

	return melhor_rota, melhor_custo, iteracoes


def executar_instancia(nome_arquivo, grasp_max):
	coordenadas = ler_instancia(nome_arquivo)
	distancias = calcular_distancias(coordenadas)
	inicio = time.perf_counter()
	rota, custo, iteracoes = grasp(distancias, grasp_max)
	tempo = time.perf_counter() - inicio
	rota_formatada = " ".join(str(cidade + 1) for cidade in rota)

	print(f"Instancia: {nome_arquivo} ({len(coordenadas)} cidades)")
	print(f"  Melhor valor: {custo}")
	print(f"  Iteracoes GRASP: {iteracoes}")
	print(f"  Alfa: {ALFA}")
	print(f"  Tempo de execucao: {tempo:.9f} s")
	print(f"  Rota: {rota_formatada} {rota[0] + 1}")


def criar_parser():
	parser = argparse.ArgumentParser(
		description="GRASP para o problema do caixeiro viajante."
	)
	parser.add_argument(
		"graspMax", type=int,
		help="numero maximo de iteracoes GRASP",
	)
	parser.add_argument(
		"arquivos", nargs="*",
		help="arquivos TSPLIB de entrada",
	)
	return parser


def main():
	argumentos = criar_parser().parse_args()
	if argumentos.graspMax <= 0:
		print("Erro: graspMax deve ser positivo.", file=sys.stderr)
		return 1

	arquivos = argumentos.arquivos or [
		os.path.join(os.path.dirname(__file__), "tsp_5"),
		os.path.join(os.path.dirname(__file__), "tsp_51"),
	]

	try:
		for nome_arquivo in arquivos:
			executar_instancia(nome_arquivo, argumentos.graspMax)
	except (OSError, ValueError) as erro:
		print(f"Erro: {erro}", file=sys.stderr)
		return 1
	return 0


if __name__ == "__main__":
	sys.exit(main())
