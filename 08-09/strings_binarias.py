import sys
import time


def imprimir_strings_binarias(n):
	if n < 0:
		raise ValueError("n deve ser maior ou igual a zero")

	def gerar(prefixo, tamanho_restante):
		if tamanho_restante == 0:
			print(prefixo)
			return

		gerar(prefixo + "0", tamanho_restante - 1)
		gerar(prefixo + "1", tamanho_restante - 1)

	gerar("", n)


def main():
	if len(sys.argv) != 2:
		print(f"Uso: python {sys.argv[0]} <n>")
		return 1

	try:
		n = int(sys.argv[1])
		inicio = time.perf_counter()
		imprimir_strings_binarias(n)
		fim = time.perf_counter()
		print(f"Tempo de execucao: {fim - inicio:.6f} segundos")
	except ValueError as erro:
		print(f"Erro: {erro}")
		return 1

	return 0


if __name__ == "__main__":
	sys.exit(main())
