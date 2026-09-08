import math
import random
import sys
import time
from pathlib import Path


def ler_instancia(nome_arquivo):
	coordenadas = []
	lendo_coordenadas = False

	with open(nome_arquivo, "r") as arquivo:
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

	return coordenadas


def calcular_distancias(coordenadas):
	num_cidades = len(coordenadas)
	distancias = [[0] * num_cidades for _ in range(num_cidades)]

	for cidade in range(num_cidades):
		for outra_cidade in range(cidade + 1, num_cidades):
			dx = coordenadas[cidade][0] - coordenadas[outra_cidade][0]
			dy = coordenadas[cidade][1] - coordenadas[outra_cidade][1]
			distancia = int(math.sqrt(dx * dx + dy * dy) + 0.5)
			distancias[cidade][outra_cidade] = distancia
			distancias[outra_cidade][cidade] = distancia

	return distancias


def distancia_rota(rota, distancias):
	return sum(
		distancias[rota[indice]][rota[(indice + 1) % len(rota)]]
		for indice in range(len(rota))
	)


def busca_local(distancias, max_iteracoes):
	num_cidades = len(distancias)
	solucao = list(range(num_cidades))
	random.shuffle(solucao)
	melhor_distancia = distancia_rota(solucao, distancias)
	iteracao = 0

	while iteracao < max_iteracoes:
		melhor_vizinho = None
		melhor_distancia_vizinho = melhor_distancia

		for inicio in range(num_cidades - 1):
			for fim in range(inicio + 1, num_cidades):
				vizinho = solucao[:]
				vizinho[inicio:fim + 1] = reversed(vizinho[inicio:fim + 1])
				distancia = distancia_rota(vizinho, distancias)

				if distancia < melhor_distancia_vizinho:
					melhor_vizinho = vizinho
					melhor_distancia_vizinho = distancia

		iteracao += 1
		if melhor_vizinho is None:
			break

		solucao = melhor_vizinho
		melhor_distancia = melhor_distancia_vizinho

	return solucao, melhor_distancia, iteracao


def executar(nome_arquivo, max_iteracoes):
	coordenadas = ler_instancia(nome_arquivo)
	if not coordenadas:
		raise ValueError("a instancia nao possui coordenadas validas")

	distancias = calcular_distancias(coordenadas)
	inicio = time.perf_counter()
	solucao, distancia, iteracoes = busca_local(distancias, max_iteracoes)
	fim = time.perf_counter()

	rota = " ".join(str(cidade + 1) for cidade in solucao)
	print(f"Instancia: {nome_arquivo}")
	print(f"Rota: {rota} {solucao[0] + 1}")
	print(f"Distancia total: {distancia}")
	print(f"Iteracoes: {iteracoes}")
	print(f"Tempo de execucao: {fim - inicio:.6f} segundos")


def main():
	if len(sys.argv) not in (2, 3):
		print(f"Uso: python {sys.argv[0]} <max_iteracoes> [arquivo]")
		return 1

	try:
		max_iteracoes = int(sys.argv[1])
		if max_iteracoes < 0:
			raise ValueError("max_iteracoes deve ser maior ou igual a zero")

		arquivos = [sys.argv[2]] if len(sys.argv) == 3 else [
			"tsp_5",
			"tsp_51",
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
