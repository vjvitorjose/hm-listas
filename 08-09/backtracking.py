import sys
import time
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from read_input import ler_grafo


def imprimir_permutacoes_validas(matriz_adj):
	"""Imprime caminhos que visitam todas as cidades sem repetir cidades."""
	num_cidades = len(matriz_adj)
	permutacao = []
	visitadas = [False] * num_cidades

	def buscar():
		if len(permutacao) == num_cidades:
			print(" ".join(str(cidade + 1) for cidade in permutacao))
			return

		for cidade in range(num_cidades):
			if visitadas[cidade]:
				continue

			if permutacao and matriz_adj[permutacao[-1]][cidade] == 0:
				continue

			permutacao.append(cidade)
			visitadas[cidade] = True
			buscar()
			visitadas[cidade] = False
			permutacao.pop()

	buscar()


def main():
	nome_arquivo = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
	_, matriz_adj, _ = ler_grafo(nome_arquivo)

	if matriz_adj is None:
		return 1

	inicio = time.perf_counter()
	imprimir_permutacoes_validas(matriz_adj)
	fim = time.perf_counter()
	print(f"Tempo de execucao: {fim - inicio:.6f} segundos")
	return 0


if __name__ == "__main__":
	sys.exit(main())
