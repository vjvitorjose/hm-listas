import math
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


def construir_rota(distancias, escolher_vizinho):
	quantidade = len(distancias)
	rota = [0]
	visitadas = {0}
	custo = 0
	atual = 0

	while len(rota) < quantidade:
		proxima = escolher_vizinho(atual, visitadas, distancias)
		rota.append(proxima)
		visitadas.add(proxima)
		custo += distancias[atual][proxima]
		atual = proxima

	custo += distancias[atual][rota[0]]
	return rota, custo


def vizinho_mais_proximo(atual, visitadas, distancias):
	return min(
		(cidade for cidade in range(len(distancias)) if cidade not in visitadas),
		key=lambda cidade: distancias[atual][cidade],
	)


def vizinho_mais_distante(atual, visitadas, distancias):
	return max(
		(cidade for cidade in range(len(distancias)) if cidade not in visitadas),
		key=lambda cidade: distancias[atual][cidade],
	)


def executar_algoritmo(nome, distancias, escolher_vizinho):
	inicio = time.perf_counter()
	rota, custo = construir_rota(distancias, escolher_vizinho)
	tempo = time.perf_counter() - inicio

	rota_formatada = " ".join(str(cidade + 1) for cidade in rota)
	print(
		f"  {nome:<22} custo: {custo} | "
		f"iteracoes: {len(rota) - 1} | tempo: {tempo:.9f} s"
	)
	print(f"  Rota: {rota_formatada} 1")


def executar_instancia(nome_arquivo):
	coordenadas = ler_instancia(nome_arquivo)
	distancias = calcular_distancias(coordenadas)
	print(f"Instancia: {nome_arquivo} ({len(coordenadas)} cidades)")
	executar_algoritmo("Vizinho mais proximo", distancias, vizinho_mais_proximo)
	executar_algoritmo("Vizinho mais distante", distancias, vizinho_mais_distante)
	print()


def main():
	arquivos = sys.argv[1:] or ["15-09/tsp_5", "15-09/tsp_51"]
	try:
		for nome_arquivo in arquivos:
			executar_instancia(nome_arquivo)
	except (OSError, ValueError) as erro:
		print(f"Erro: {erro}", file=sys.stderr)
		return 1
	return 0


if __name__ == "__main__":
	sys.exit(main())
