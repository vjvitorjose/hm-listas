import sys
import time


def imprimir_permutacoes(n):
	if n < 0:
		raise ValueError("n deve ser maior ou igual a zero")

	numeros = list(range(1, n + 1))

	def gerar(posicao):
		if posicao == n:
			print(" ".join(map(str, numeros)))
			return

		for indice in range(posicao, n):
			numeros[posicao], numeros[indice] = numeros[indice], numeros[posicao]
			gerar(posicao + 1)
			numeros[posicao], numeros[indice] = numeros[indice], numeros[posicao]

	gerar(0)


def main():
	if len(sys.argv) != 2:
		print(f"Uso: python {sys.argv[0]} <n>")
		return 1

	try:
		n = int(sys.argv[1])
		inicio = time.perf_counter()
		imprimir_permutacoes(n)
		fim = time.perf_counter()
		print(f"Tempo de execucao: {fim - inicio:.6f} segundos")
	except ValueError as erro:
		print(f"Erro: {erro}")
		return 1

	return 0


if __name__ == "__main__":
	sys.exit(main())
