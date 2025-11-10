import httpx
import json

BASE_URL = "http://127.0.0.1:8000"

def criar_produto(produto):
    resp = httpx.post(
        f"{BASE_URL}/produtos",
        json = {"nome":produto.get("nome"),"categoria":produto.get("categoria"),"preco":produto.get("preco")}
    )
    print(resp.json())

def listar_produtos():
    resp = httpx.get(f"{BASE_URL}/produtos")
    print("\n--- LISTA ATUAL DE PRODUTOS ---")
    print(json.dumps(resp.json(), indent=2, ensure_ascii=False))

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

def obter_media_precos():
    resp = httpx.get(f"{BASE_URL}/produtos/analise/media-precos")
    print("\n--- ANÁLISE: Média de Preços ---")
    print(resp.json())

def obter_maior_preco():
    resp = httpx.get(f"{BASE_URL}/produtos/analise/maior-preco")
    print("\n--- ANÁLISE: Produto Mais Caro ---")
    print(resp.json())

def obter_menor_preco():
    resp = httpx.get(f"{BASE_URL}/produtos/analise/menor-preco")
    print("\n--- ANÁLISE: Produto Mais Barato ---")
    print(resp.json())

def obter_acima_media():
    resp = httpx.get(f"{BASE_URL}/produtos/analise/acima-media")
    print("\n--- ANÁLISE: Produtos Acima da Média ---")
    print(json.dumps(resp.json(), indent=2, ensure_ascii=False))

def obter_abaixo_media():
    resp = httpx.get(f"{BASE_URL}/produtos/analise/abaixo-media")
    print("\n--- ANÁLISE: Produtos Abaixo da Média ---")
    print(json.dumps(resp.json(), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    
    # 1. Criação (POST)
    #criar_produto({"nome":"SSD 8TB", "categoria": "Armazenamento", "preco": 1300.00})
    
    # 2. Listagem (GET)
    listar_produtos()
    
    # 3. Teste dos Serviços de Análise
    obter_media_precos()
    obter_maior_preco()
    obter_menor_preco()
    obter_acima_media()
    obter_abaixo_media()
    
    # 4. Atualização (PUT)
    # atualizar_produto(2, {"nome":"Teclado Mecânico PRO (Editado)", "categoria": "Periférico", "preco": 400.00})
    
    # 5. Deleção (DELETE)
    # apagar_produto(3)
    
    # 6. Busca por ID (GET {id})
    obter_produto(2)
    obter_produto(9999) # Testa erro 404
    