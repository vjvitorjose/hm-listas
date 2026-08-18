def ler_grafo(nome_arquivo):
    try:
        with open(nome_arquivo, 'r') as arquivo:
            primeira_linha = arquivo.readline().strip().split()
            num_vertices = int(primeira_linha[0])
            num_arestas = int(primeira_linha[1])

            matriz_adj = [[0] * num_vertices for _ in range(num_vertices)]
            lista_adj = [[] for _ in range(num_vertices)]

            for _ in range(num_arestas):
                linha = arquivo.readline().strip().split()
                if not linha:
                    continue
                
                u = int(linha[0]) - 1
                v = int(linha[1]) - 1
                custo = int(linha[2])

                matriz_adj[u][v] = custo
                matriz_adj[v][u] = custo  

                lista_adj[u].append((v, custo))
                lista_adj[v].append((u, custo))  

        return num_vertices, matriz_adj, lista_adj

    except FileNotFoundError:
        print(f"Erro: O arquivo '{nome_arquivo}' não foi encontrado.")
        return None, None, None

if __name__ == "__main__":
    V, matriz, lista = ler_grafo("input.txt")

    if V is not None:
        print("=== MATRIZ DE ADJACÊNCIA ===")
        print("   " + " ".join(f"{i+1:2}" for i in range(V)))
        for i, linha in enumerate(matriz):
            print(f"{i+1}: " + " ".join(f"{peso:2}" for peso in linha))

        print("\n=== LISTA DE ADJACÊNCIA ===")
        for i, vizinhos in enumerate(lista):
            conexoes = ", ".join([f"(v:{v+1}, custo:{c})" for v, c in vizinhos])
            print(f"Vértice {i+1} -> {conexoes}")