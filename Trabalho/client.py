import httpx

BASE_URL = "http://127.0.0.1:8000"

def criar_produto(produto):
    resp = httpx.post(
        f"{BASE_URL}/produtos",
        json = {"nome":produto.get("nome"),"categoria":produto.get("categoria"),"preco":produto.get("preco")}
    )
    return resp

def listar_produtos():
    resp = httpx.get(f"{BASE_URL}/produtos")
    print("\n--- LISTA ATUAL DE PRODUTOS ---")
    print(resp.json())

def obter_produto(id):
    resp = httpx.get(f"{BASE_URL}/produtos/{id}")
    print(f"\n--- BUSCA ID {id} ---")
    if resp.status_code == 200:
        print(resp.json())
    else:
        print(f"ERRO {resp.status_code}: {resp.json().get('detail')}")

def atualizar_produto(id, dados_produto):
    resp = httpx.put(
        f"{BASE_URL}/produtos/{id}",
        json = dados_produto
    )
    print(f"\n--- ATUALIZAÇÃO ID {id} ---")
    print(resp.json())

def apagar_produto(id):
    resp = httpx.delete(f"{BASE_URL}/produtos/{id}")
    print(f"\n--- REMOÇÃO ID {id} ---")
    print(resp.json())


if __name__ == "__main__":
    
    # 1. Criação (POST)
    criar_produto({"nome":"Webcam HD", "categoria": "Vídeo", "preco": 180.90})
    
    # 2. Listagem (GET)
    listar_produtos()
    
    # 3. Atualização (PUT) - Atualiza o ID 2 (Teclado)
    atualizar_produto(2, {"nome":"Teclado Mecânico PRO", "categoria": "Periférico", "preco": 400.00})
    
    # 4. Deleção (DELETE) - Remove o ID 1 (Mouse Óptico)
    apagar_produto(1)
    
    # 5. Busca por ID (GET {id})
    obter_produto(2)
    obter_produto(100) # Testa erro 404
    
    # 6. Listagem Final
    listar_produtos()